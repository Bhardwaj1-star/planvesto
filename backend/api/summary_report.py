from fastapi import APIRouter, Header, Response
from fastapi.responses import JSONResponse
from services.summary_report_service import SummaryReportService
from api.auth import authenticate_user, verify_planning_unit_ownership

router = APIRouter(prefix="/api/summary-report", tags=["Summary Financial Planning Report"])

@router.get("/json")
def get_summary_report(
    planning_unit_id: str,
    authorization: str | None = Header(default=None),
):
    """Return the aggregated SummaryReport as JSON.
    The endpoint validates the user and planning‑unit ownership, then
    delegates to the service layer.
    """
    user_id = authenticate_user(authorization)
    verify_planning_unit_ownership(planning_unit_id, user_id)
    report = SummaryReportService.generate(planning_unit_id)
    return JSONResponse(content=report.dict())

@router.get("/pdf")
def get_summary_report_pdf(
    planning_unit_id: str,
    authorization: str | None = Header(default=None),
):
    """Generate and download the SummaryReport as a PDF.
    The PDF rendering implementation is a placeholder – replace with the
    real renderer when available.
    """
    user_id = authenticate_user(authorization)
    verify_planning_unit_ownership(planning_unit_id, user_id)
    # Use the real PDF renderer
    report = SummaryReportService.generate(planning_unit_id)
    from services.summary_report_renderer import SummaryReportRenderer
    pdf_bytes = SummaryReportRenderer().render(report)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=summary-report.pdf"},
    )
