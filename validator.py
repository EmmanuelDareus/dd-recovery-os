"""
validator.py

Deterministic completeness/compliance check for ocean D&D invoices against
the Federal Maritime Commission's minimum-information requirements
(46 CFR Part 541, Subpart A).

Legal basis (verified against the current eCFR text as of Aug 2026):
  - 46 CFR 541.6 sets the minimum information a demurrage/detention
    invoice must contain (identifying, timing, rate, and contact info).
  - 46 CFR 541.5 states that failure to include any of that required
    minimum information eliminates the billed party's obligation to
    pay the applicable charge.

NOTE: This module is a deterministic completeness checker, not a legal
opinion. It flags MISSING statutory fields; it does not evaluate whether
present values are themselves accurate, timely, or correctly calculated.
Field labels beginning with a code like "D01" are this project's own
naming convention, not an official FMC designation. For anything with
real money on the line, have counsel confirm the read of Part 541.

USAGE:
    from parser import InvoiceSchema
    from validator import audit_invoice_completeness

    result = audit_invoice_completeness(invoice)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from parser import InvoiceSchema


# --------------------------------------------------------------------------
# Defect code -> (field name, human description)
# Order matters: this is also the order defects are reported in.
# --------------------------------------------------------------------------

DEFECT_MAP: list[tuple[str, str, str]] = [
    ("D01", "bol_number", "Missing Bill of Lading (BOL) number"),
    ("D02", "container_number", "Missing Container number"),
    ("D03", "port_of_discharge", "Missing Port of Discharge"),
    ("D05", "invoice_date", "Missing Invoice Date"),
    ("D06", "due_date", "Missing Due Date"),
    ("D07", "allowed_free_days", "Missing Allowed Free Time"),
    ("D08", "free_time_start", "Missing Free Time Start"),
    ("D09", "free_time_end", "Missing Free Time End"),
    ("D13", "daily_rate", "Missing Daily Rate"),
    ("D15", "dispute_contact", "Missing Dispute Contact"),
]

NON_ENFORCEABLE_REASON = (
    "Incomplete invoice eliminates billed party obligation to pay."
)


def audit_invoice_completeness(invoice_data: "InvoiceSchema") -> dict:
    """
    Deterministically check an InvoiceSchema for missing statutory fields.

    Args:
        invoice_data: a validated InvoiceSchema instance (see parser.py).

    Returns:
        dict with:
            completeness_score (float, 0.0-100.0): percent of the
                statutory fields checked here that are present.
            defects_found (list[dict]): each with "code" and "description"
                for every missing field, in DEFECT_MAP order.
            is_legally_enforceable (bool): False if any statutory field
                is missing.
            reason (str | None): explanation when not enforceable,
                citing 46 CFR 541.5. None when the invoice is complete.

    Raises:
        TypeError: if invoice_data isn't an object with the expected
            attributes (e.g. not an InvoiceSchema instance).
    """
    defects_found: list[dict] = []

    total_fields = len(DEFECT_MAP)
    missing_count = 0

    for code, field_name, description in DEFECT_MAP:
        try:
            value = getattr(invoice_data, field_name)
        except AttributeError as e:
            raise TypeError(
                f"invoice_data is missing expected field '{field_name}' — "
                "is this an InvoiceSchema instance?"
            ) from e

        is_missing = value is None or value == "" or (
            isinstance(value, str) and not value.strip()
        )

        if is_missing:
            missing_count += 1
            defects_found.append({"code": code, "description": description})

    completeness_score = round(
        100.0 * (total_fields - missing_count) / total_fields, 2
    )

    is_legally_enforceable = missing_count == 0

    return {
        "completeness_score": completeness_score,
        "defects_found": defects_found,
        "is_legally_enforceable": is_legally_enforceable,
        "reason": None if is_legally_enforceable else NON_ENFORCEABLE_REASON,
    }


# --------------------------------------------------------------------------
# CLI / quick manual test
# --------------------------------------------------------------------------

def _demo():
    """Run against a couple of hand-built examples — no PDF needed."""
    from parser import InvoiceSchema

    complete = InvoiceSchema(
        invoice_number="INV-001",
        bol_number="BOL123456",
        container_number="MSCU1234567",
        port_of_discharge="Port of Long Beach",
        invoice_date="2026-07-01",
        due_date="2026-07-31",
        allowed_free_days=5,
        free_time_start="2026-06-20",
        free_time_end="2026-06-25",
        daily_rate=150.0,
        total_charged=750.0,
        dispute_contact="disputes@carrier.com",
    )

    incomplete = InvoiceSchema(
        invoice_number="INV-002",
        container_number="MSCU7654321",
        invoice_date="2026-07-01",
    )

    import json
    print("Complete invoice:")
    print(json.dumps(audit_invoice_completeness(complete), indent=2))
    print("\nIncomplete invoice:")
    print(json.dumps(audit_invoice_completeness(incomplete), indent=2))


if __name__ == "__main__":
    _demo()
