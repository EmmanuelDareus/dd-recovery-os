"""
parser.py — dd-recovery-os

Parses ocean Demurrage & Detention (D&D) invoice PDFs into a strict,
validated schema using pdfplumber (extraction) + Pydantic (validation).

INSTALL:
    pip install pdfplumber pydantic --break-system-packages

USAGE:
    python parser.py /path/to/invoice.pdf

    or import it:
        from parser import parse_invoice
        result = parse_invoice("invoice.pdf")
"""

from __future__ import annotations

import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import pdfplumber
from pydantic import BaseModel, field_validator


# --------------------------------------------------------------------------
# Schema
# --------------------------------------------------------------------------

class InvoiceSchema(BaseModel):
    invoice_number: Optional[str] = None
    bol_number: Optional[str] = None
    container_number: Optional[str] = None
    port_of_discharge: Optional[str] = None
    invoice_date: Optional[str] = None       # ISO-8601 (YYYY-MM-DD)
    due_date: Optional[str] = None           # ISO-8601 (YYYY-MM-DD)
    allowed_free_days: Optional[int] = None
    free_time_start: Optional[str] = None    # ISO-8601 (YYYY-MM-DD)
    free_time_end: Optional[str] = None      # ISO-8601 (YYYY-MM-DD)
    daily_rate: Optional[float] = None
    total_charged: Optional[float] = None
    dispute_contact: Optional[str] = None

    @field_validator(
        "invoice_date", "due_date", "free_time_start", "free_time_end",
        mode="before",
    )
    @classmethod
    def normalize_date(cls, v):
        if v is None or v == "":
            return None
        return _to_iso_date(v) or v  # fall back to raw string if unparsable

    @field_validator("allowed_free_days", mode="before")
    @classmethod
    def clean_int(cls, v):
        if v is None or v == "":
            return None
        if isinstance(v, str):
            digits = re.sub(r"[^\d]", "", v)
            return int(digits) if digits else None
        return v

    @field_validator("daily_rate", "total_charged", mode="before")
    @classmethod
    def clean_float(cls, v):
        if v is None or v == "":
            return None
        if isinstance(v, str):
            cleaned = re.sub(r"[^\d.\-]", "", v)
            return float(cleaned) if cleaned else None
        return v


# --------------------------------------------------------------------------
# Parsing errors
# --------------------------------------------------------------------------

class InvoiceParseError(Exception):
    """Raised when a PDF cannot be read or converted at all."""


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------

DATE_PATTERNS = [
    "%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", "%B %d, %Y", "%b %d, %Y",
    "%d-%b-%Y", "%d %B %Y", "%m-%d-%Y",
]


def _to_iso_date(raw: str) -> Optional[str]:
    raw = raw.strip()
    for fmt in DATE_PATTERNS:
        try:
            return datetime.strptime(raw, fmt).date().isoformat()
        except ValueError:
            continue
    return None


FIELD_PATTERNS: dict[str, list[str]] = {
    "invoice_number": [r"invoice\s*(?:no\.?|number|#)\s*[:\-]?\s*([A-Za-z0-9\-\/]+)"],
    "bol_number": [
        # "Bill of Lading (BOL): X", "Bill of Lading No: X", "Bill of Lading: X"
        r"bill\s*of\s*lading\s*(?:\([^)]*\))?\s*(?:no\.?|number)?\s*[:\-]?\s*([A-Za-z0-9\-\/]+)",
        # "B/L: X", "B/L No: X", "BL Number: X"
        r"b\/?l\s*(?:no\.?|number)?\s*[:\-]\s*([A-Za-z0-9\-\/]+)",
        # standalone "BOL: X", "BOL No: X" (not preceded by "Bill of Lading", already
        # handled above, and not matching the unrelated word "boldly" etc. thanks to \b)
        r"\bbol\s*(?:no\.?|number)?\s*[:\-]\s*([A-Za-z0-9\-\/]+)",
    ],
    "container_number": [r"container\s*(?:no\.?|number|#)\s*[:\-]?\s*([A-Z]{4}\d{6,7})"],
    "port_of_discharge": [r"port\s*of\s*discharge\s*[:\-]?\s*([A-Za-z0-9\s,]+?)(?:\n|$)"],
    "invoice_date": [
        # "Invoice Date: X" — checked first since it's the more specific label
        r"invoice\s*date\s*[:\-]?\s*([A-Za-z0-9,\/\-\s]+?)(?:\n|$)",
        # bare "Date: X", but never "Due Date:" (that belongs to due_date)
        r"(?<!due )(?<!due)\bdate\s*[:\-]\s*([A-Za-z0-9,\/\-\s]+?)(?:\n|$)",
    ],
    "due_date": [r"due\s*date\s*[:\-]?\s*([A-Za-z0-9,\/\-\s]+?)(?:\n|$)"],
    "allowed_free_days": [
        # "Free Time Allowed: 4 Days", "Free Days Allowed: 4"
        r"free\s*(?:time|days)\s*allowed\s*[:\-]?\s*(\d+)(?:\s*days?)?",
        # "Allowed Free Time: 4 Days", "Allowed Free Days: 5"
        r"allowed\s*free\s*(?:time|days)\s*[:\-]?\s*(\d+)(?:\s*days?)?",
        # generic fallback: "Free Time: 4 Days" / "Free Days: 4"
        r"free\s*(?:time|days)\s*[:\-]?\s*(\d+)(?:\s*days?)?",
    ],
    "free_time_start": [r"free\s*time\s*start\s*[:\-]?\s*([A-Za-z0-9,\/\-\s]+?)(?:\n|$)"],
    "free_time_end": [r"free\s*time\s*end\s*[:\-]?\s*([A-Za-z0-9,\/\-\s]+?)(?:\n|$)",
                       r"last\s*free\s*day\s*[:\-]?\s*([A-Za-z0-9,\/\-\s]+?)(?:\n|$)"],
    "daily_rate": [r"daily\s*rate\s*[:\-]?\s*\$?\s*([\d,]+\.?\d*)",
                    r"per\s*day\s*rate\s*[:\-]?\s*\$?\s*([\d,]+\.?\d*)"],
    "total_charged": [
        # "Total Charges Due: $X", "Total Charges: $X"
        r"total\s*charges?\s*(?:due)?\s*[:\-]?\s*\$?\s*([\d,]+\.?\d*)",
        # "Total Due: $X"
        r"total\s*due\s*[:\-]?\s*\$?\s*([\d,]+\.?\d*)",
        # fallback: "Total Amount: $X", "Total Charged: $X"
        r"total\s*(?:charged|amount)\s*[:\-]?\s*\$?\s*([\d,]+\.?\d*)",
    ],
    "dispute_contact": [r"dispute\s*(?:contact|inquiries)?\s*[:\-]?\s*([A-Za-z0-9@\.\s,\-]+?)(?:\n|$)"],
}


def _extract_field(pattern_list: list[str], text: str) -> Optional[str]:
    for pattern in pattern_list:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value = match.group(1).strip()
            if value:
                return value
    return None


def _extract_from_tables(tables: list[list[list]], field_data: dict) -> None:
    """pdfplumber returns each table as a list of rows (list of cell strings).
    Scan label/value pairs for anything the prose regex pass missed."""
    for table in tables:
        for row in table:
            cells = [str(c).strip() for c in row if c and str(c).strip()]
            if len(cells) < 2:
                continue
            label, value = cells[0], " ".join(cells[1:])
            label_lower = label.lower()

            for field_name in FIELD_PATTERNS:
                if field_data.get(field_name):
                    continue  # already found via prose text
                key_hint = field_name.replace("_", " ").split()[0]
                if key_hint in label_lower:
                    field_data[field_name] = value


# --------------------------------------------------------------------------
# Main parsing function
# --------------------------------------------------------------------------

def parse_invoice(pdf_path: str | Path) -> InvoiceSchema:
    """
    Parse a D&D invoice PDF into a validated InvoiceSchema.

    Raises:
        InvoiceParseError: if the file is missing, not a PDF, corrupt,
                            or pdfplumber fails to open/read it.
    """
    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise InvoiceParseError(f"File not found: {pdf_path}")
    if pdf_path.suffix.lower() != ".pdf":
        raise InvoiceParseError(f"Not a PDF file: {pdf_path}")
    if pdf_path.stat().st_size == 0:
        raise InvoiceParseError(f"File is empty: {pdf_path}")

    full_text_parts: list[str] = []
    all_tables: list[list[list]] = []

    try:
        with pdfplumber.open(pdf_path) as pdf:
            if len(pdf.pages) == 0:
                raise InvoiceParseError(f"PDF has no pages: {pdf_path.name}")

            for page in pdf.pages:
                try:
                    page_text = page.extract_text()
                    if page_text:
                        full_text_parts.append(page_text)
                except Exception:
                    # A single unreadable page shouldn't kill the whole parse.
                    continue

                try:
                    page_tables = page.extract_tables()
                    if page_tables:
                        all_tables.extend(page_tables)
                except Exception:
                    continue

    except InvoiceParseError:
        raise
    except Exception as e:
        raise InvoiceParseError(
            f"pdfplumber failed to open/read '{pdf_path.name}': {e}"
        ) from e

    full_text = "\n".join(full_text_parts)

    if not full_text.strip():
        raise InvoiceParseError(
            f"No extractable text found in '{pdf_path.name}' "
            "(it may be a scanned image with no OCR layer — pdfplumber "
            "does not perform OCR)."
        )

    field_data: dict[str, Optional[str]] = {}
    for field_name, patterns in FIELD_PATTERNS.items():
        field_data[field_name] = _extract_field(patterns, full_text)

    # Tables often hold structured values (rates, dates) more reliably
    # than prose — fill in anything prose extraction missed.
    _extract_from_tables(all_tables, field_data)

    try:
        return InvoiceSchema(**field_data)
    except Exception as e:
        raise InvoiceParseError(
            f"Extracted data did not match InvoiceSchema: {e}"
        ) from e


# --------------------------------------------------------------------------
# CLI entry point
# --------------------------------------------------------------------------

def main():
    if len(sys.argv) != 2:
        print("Usage: python parser.py <path_to_invoice.pdf>")
        sys.exit(1)

    pdf_path = sys.argv[1]

    try:
        invoice = parse_invoice(pdf_path)
    except InvoiceParseError as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    print(invoice.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
