"""
main.py

FastAPI service that ties parser.py (Docling + Pydantic extraction) and
validator.py (46 CFR Part 541 completeness check) into one endpoint:

    POST /api/v1/audit-invoice   (multipart/form-data, field: file)

INSTALL:
    pip install fastapi uvicorn python-multipart pdfplumber pydantic --break-system-packages

RUN:
    uvicorn main:app --reload

Then POST a PDF to http://127.0.0.1:8000/api/v1/audit-invoice
"""

from __future__ import annotations

import logging
import tempfile
import uuid
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from parser import InvoiceParseError, parse_invoice
from validator import audit_invoice_completeness

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("dd-audit")

app = FastAPI(
    title="D&D Invoice Audit API",
    description="Parses ocean D&D invoices and audits them against 46 CFR Part 541.",
    version="1.0.0",
)

# CORS: open by default for local frontend development.
# Tighten allow_origins to your actual frontend domain(s) before deploying.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MAX_UPLOAD_BYTES = 25 * 1024 * 1024  # 25 MB


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/v1/audit-invoice")
async def audit_invoice(file: UploadFile = File(...)):
    """
    Accepts a PDF invoice, extracts structured fields, and returns a
    completeness/enforceability audit against 46 CFR Part 541.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file was uploaded.")

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type for '{file.filename}'. Only PDF is accepted.",
        )

    contents = await file.read()

    if not contents:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    if len(contents) > MAX_UPLOAD_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"File exceeds the {MAX_UPLOAD_BYTES // (1024 * 1024)}MB upload limit.",
        )

    # Write to a temp file with a random name so concurrent uploads
    # (and repeated uploads of the same filename) never collide.
    tmp_dir = Path(tempfile.gettempdir())
    tmp_path = tmp_dir / f"dd-audit-{uuid.uuid4().hex}.pdf"

    try:
        tmp_path.write_bytes(contents)
    except OSError as e:
        logger.exception("Failed to write temp file")
        raise HTTPException(
            status_code=500, detail=f"Could not save uploaded file: {e}"
        ) from e

    try:
        try:
            invoice_data = parse_invoice(tmp_path)
        except InvoiceParseError as e:
            raise HTTPException(status_code=422, detail=str(e)) from e
        except Exception as e:
            # Anything unexpected from Docling/pydantic that InvoiceParseError
            # didn't already wrap — surface it as a 500, not a silent failure.
            logger.exception("Unexpected error during PDF parsing")
            raise HTTPException(
                status_code=500, detail=f"Unexpected error while parsing PDF: {e}"
            ) from e

        try:
            audit = audit_invoice_completeness(invoice_data)
        except TypeError as e:
            logger.exception("Validator received malformed invoice data")
            raise HTTPException(
                status_code=500, detail=f"Validation step failed: {e}"
            ) from e

        # Reshape defects to the requested {code, issue} keys.
        defects_found = [
            {"code": d["code"], "issue": d["description"]}
            for d in audit["defects_found"]
        ]

        # An unenforceable invoice puts the FULL charged amount in dispute,
        # since 46 CFR 541.5 removes the payment obligation entirely when
        # required info is missing — not just for the missing line items.
        potential_disputable_amount = (
            invoice_data.total_charged
            if not audit["is_legally_enforceable"] and invoice_data.total_charged is not None
            else 0.0
        )

        return {
            "filename": file.filename,
            "extracted_data": invoice_data.model_dump(),
            "audit_result": {
                "completeness_score": audit["completeness_score"],
                "is_legally_enforceable": audit["is_legally_enforceable"],
                "defects_found": defects_found,
                "potential_disputable_amount": potential_disputable_amount,
            },
        }

    finally:
        # Always clean up the temp file, whether parsing succeeded or not.
        try:
            tmp_path.unlink(missing_ok=True)
        except OSError:
            logger.warning("Could not remove temp file: %s", tmp_path)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
