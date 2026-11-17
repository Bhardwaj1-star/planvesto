"""
api/routers/reports.py
FastAPI router for Basket Reports and Summary Financial Reports.
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, Query, Response

from app.api.dependencies import get_current_user_id
from app.api.schemas.strategy_builder import BasketReportRequest
from app.infrastructure.persistence.repositories.goal_planner import GoalPlannerRepository

router = APIRouter(tags=["Reports"])

_goal_repo = GoalPlannerRepository()


def _pdf_response(title: str, filename: str) -> Response:
    pdf_content = f"""%PDF-1.4
1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj
2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj
3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >> endobj
4 0 obj << /Length 72 >> stream
BT
/F1 18 Tf
50 720 Td
({title}) Tj
ET
endstream endobj
5 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj
xref
0 6
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000229 00000 n 
0000000350 00000 n 
trailer << /Size 6 /Root 1 0 R >>
startxref
421
%%EOF"""
    return Response(
        content=pdf_content.encode("utf-8"),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.post("/basket-report")
@router.post("/api/basket-report", include_in_schema=False)
def build_basket_report(
    request: BasketReportRequest,
    user_id: str = Depends(get_current_user_id),
):
    """Builds an aggregated planning basket report across multiple goals."""
    goals = _goal_repo.list_goals(request.planning_unit_id)
    filtered = [g for g in goals if g.get("goal_id") in request.goal_ids] if request.goal_ids else goals
    return {
        "basket_name": request.basket_name or "Primary Basket",
        "planning_unit_id": request.planning_unit_id,
        "goals_count": len(filtered),
        "goals": filtered,
        "consolidated_status": "feasible",
    }


@router.post("/basket-report/pdf")
@router.post("/api/basket-report/pdf", include_in_schema=False)
def download_basket_report_pdf(
    request: BasketReportRequest,
    user_id: str = Depends(get_current_user_id),
):
    """Downloads PDF for Planning Basket Report."""
    return _pdf_response("PlanVesto Planning Basket Report", "basket-report.pdf")


@router.get("/summary-report/pdf")
@router.get("/api/summary-report/pdf", include_in_schema=False)
def download_summary_report_pdf(
    planning_unit_id: str = Query(...),
    user_id: str = Depends(get_current_user_id),
):
    """Downloads PDF for Investor Summary Report."""
    return _pdf_response("PlanVesto Investor Summary Report", f"summary-report-{planning_unit_id}.pdf")
