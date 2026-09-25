from __future__ import annotations

import re
from typing import Any

import pymupdf


def _first_match(text: str, patterns: list[str]) -> str | None:
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE)
        if match:
            return match.group(1).strip()
    return None


def extract_policy_pdf(data: bytes) -> dict[str, Any]:
    """Extract policy-document text locally with PyMuPDF.

    For scanned/image-only pages, use PyMuPDF's Tesseract OCR fallback when
    Tesseract language data is installed on the server.
    """
    doc = pymupdf.open(stream=data, filetype="pdf")
    pages: list[str] = []
    ocr_pages = 0

    for page in doc:
        text = page.get_text("text").strip()
        if not text:
            try:
                text = page.get_text(textpage=page.get_textpage_ocr(language="eng")).strip()
                ocr_pages += 1
            except Exception:
                text = ""
        pages.append(text)

    text = "\n\n".join(p for p in pages if p)
    doc.close()

    fields = {
        "policy_name": _first_match(text, [
            r"(?:policy\s+name|plan\s+name|product\s+name)\s*[:\-]\s*(.+)",
        ]),
        "insurer": _first_match(text, [
            r"(?:insurer|insurance\s+company|life\s+insurer)\s*[:\-]\s*(.+)",
        ]),
        "policy_number": _first_match(text, [
            r"(?:policy\s+(?:no|number)|pol\.\s*no)\s*[:\-]\s*([A-Z0-9\-/]+)",
        ]),
        "sum_assured": _first_match(text, [
            r"(?:sum\s+assured|life\s+cover)\s*[:\-]?\s*(?:₹|rs\.?|inr)?\s*([\d,]+(?:\.\d+)?)",
        ]),
        "premium": _first_match(text, [
            r"(?:premium|installment\s+premium)\s*[:\-]?\s*(?:₹|rs\.?|inr)?\s*([\d,]+(?:\.\d+)?)",
        ]),
        "premium_frequency": _first_match(text, [
            r"(?:premium\s+(?:payment\s+)?frequency|payment\s+mode)\s*[:\-]\s*(monthly|quarterly|half[- ]yearly|yearly|annual)",
        ]),
        "maturity_date": _first_match(text, [
            r"(?:maturity\s+date|date\s+of\s+maturity)\s*[:\-]\s*([\d\-/]+)",
        ]),
        "maturity_value": _first_match(text, [
            r"(?:maturity\s+(?:benefit|value)|maturity\s+amount)\s*[:\-]?\s*(?:₹|rs\.?|inr)?\s*([\d,]+(?:\.\d+)?)",
        ]),
        "current_surrender_value": _first_match(text, [
            r"(?:surrender\s+value|current\s+(?:fund|surrender)\s+value)\s*[:\-]?\s*(?:₹|rs\.?|inr)?\s*([\d,]+(?:\.\d+)?)",
        ]),
    }

    return {
        "pages": len(pages),
        "ocr_pages": ocr_pages,
        "fields": fields,
        "text": text,
    }
