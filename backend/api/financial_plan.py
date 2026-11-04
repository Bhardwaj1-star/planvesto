from fastapi import APIRouter, Header, Query
from fastapi.responses import Response

from api.auth import authenticate_user, verify_planning_unit_ownership
from schemas.financial_plan import FinancialPlanBuildRequest
from services.financial_plan_service import FinancialPlanService

router = APIRouter(prefix="/api/financial-plan", tags=["Financial Plan"])


@router.post("/build")
def build_financial_plan(request: FinancialPlanBuildRequest, authorization: str | None = Header(default=None)):
    user_id = authenticate_user(authorization)
    verify_planning_unit_ownership(request.planning_unit_id, user_id)
    return FinancialPlanService().build_plan(
        request.planning_unit_id,
        rule_overrides=request.rule_overrides,
    )


@router.get("")
def get_financial_plan(planning_unit_id: str = Query(...), authorization: str | None = Header(default=None)):
    user_id = authenticate_user(authorization)
    verify_planning_unit_ownership(planning_unit_id, user_id)
    return FinancialPlanService().build_plan(planning_unit_id)


@router.get(".pdf")
def download_financial_plan_pdf(planning_unit_id: str = Query(...), authorization: str | None = Header(default=None)):
    user_id = authenticate_user(authorization)
    verify_planning_unit_ownership(planning_unit_id, user_id)
    pdf = FinancialPlanService().generate_pdf(planning_unit_id)
    return Response(content=pdf, media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename=complete-financial-plan-{planning_unit_id}.pdf"})
