from fastapi import APIRouter, Header
from fastapi.responses import Response

from api.auth import authenticate_user, verify_planning_unit_ownership
from services.basket_report_service import BasketReportService

router = APIRouter(prefix="/api/basket-report", tags=["Goal Basket Reports"])


@router.post("")
def build_basket_report(
    planning_unit_id: str,
    basket_name: str,
    goal_ids: list[str],
    authorization: str | None = Header(default=None),
):
    user_id = authenticate_user(authorization)
    verify_planning_unit_ownership(planning_unit_id, user_id)
    return BasketReportService().build_report(planning_unit_id, basket_name, goal_ids)


@router.post("/pdf")
def download_basket_report_pdf(
    planning_unit_id: str,
    basket_name: str,
    goal_ids: list[str],
    authorization: str | None = Header(default=None),
):
    user_id = authenticate_user(authorization)
    verify_planning_unit_ownership(planning_unit_id, user_id)
    pdf = BasketReportService().generate_pdf(planning_unit_id, basket_name, goal_ids)
    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=goal-basket-report.pdf"},
    )
