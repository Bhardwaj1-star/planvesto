from fastapi import APIRouter, File, Header, HTTPException, UploadFile

from api.auth import authenticate_user
from services.pdf_policy_extractor import extract_policy_pdf

router = APIRouter(prefix="/api/insurance", tags=["Insurance"])


@router.post("/extract-policy-pdf")
async def extract_policy_pdf_endpoint(
    file: UploadFile = File(...),
    authorization: str | None = Header(default=None),
):
    """Extract policy fields from an authenticated, optional policy PDF.

    Parsing is local and read-only. The client must review/confirm extracted
    fields before any financial data is persisted.
    """
    authenticate_user(authorization)

    if file.content_type not in {"application/pdf", "application/x-pdf"}:
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    data = await file.read()
    if not data:
        raise HTTPException(status_code=400, detail="Uploaded PDF is empty")
    if len(data) > 15 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="PDF must be 15 MB or smaller")

    try:
        return extract_policy_pdf(data)
    except Exception as exc:
        raise HTTPException(status_code=422, detail=f"Could not read policy PDF: {exc}") from exc
