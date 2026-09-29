from fastapi import APIRouter, Header, Query
from fastapi.responses import Response
from api.auth import authenticate_user, verify_goal_ownership, verify_planning_unit_ownership, verify_strategy_run_ownership
from models.strategy import StrategyRun
from schemas.strategy import CustomScenarioRequest, FinancialPlanBuildRequest, PriorityWeightsRequest, StrategyBuildRequest, StrategySelectRequest
from services.strategy_service import StrategyService
from services.retirement_report_pdf_service import RetirementReportPDFService
from services.goal_report_service import GoalReportService
from services.financial_plan_service import FinancialPlanService

router = APIRouter(prefix="/api/strategy", tags=["Strategy Builder"])


@router.post("/build", response_model=StrategyRun)
def build_strategy(request: StrategyBuildRequest, authorization: str | None = Header(default=None)):
    user_id = authenticate_user(authorization)
    verify_goal_ownership(request.planning_unit_id, request.goal_id, user_id)
    return StrategyService().build_strategy(request.planning_unit_id, request.goal_id, request.investor_priorities)


@router.post("/financial-plan/build")
def build_financial_plan(request: FinancialPlanBuildRequest, authorization: str | None = Header(default=None)):
    user_id = authenticate_user(authorization)
    verify_planning_unit_ownership(request.planning_unit_id, user_id)
    return FinancialPlanService().build_plan(request.planning_unit_id, request.investor_priorities)


@router.get("/financial-plan")
def get_financial_plan(planning_unit_id: str = Query(...), authorization: str | None = Header(default=None)):
    user_id = authenticate_user(authorization)
    verify_planning_unit_ownership(planning_unit_id, user_id)
    return FinancialPlanService().build_plan(planning_unit_id)


@router.get("/financial-plan.pdf")
def download_financial_plan_pdf(planning_unit_id: str = Query(...), authorization: str | None = Header(default=None)):
    user_id = authenticate_user(authorization)
    verify_planning_unit_ownership(planning_unit_id, user_id)
    pdf = FinancialPlanService().generate_pdf(planning_unit_id)
    return Response(content=pdf, media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename=complete-financial-plan-{planning_unit_id}.pdf"})


@router.post("/scenarios/custom", response_model=StrategyRun)
def add_custom_scenario(request: CustomScenarioRequest, authorization: str | None = Header(default=None)):
    user_id = authenticate_user(authorization)
    verify_strategy_run_ownership(request.planning_unit_id, request.strategy_run_id, user_id)
    return StrategyService().add_custom_scenario(request)


@router.post("/priorities", response_model=StrategyRun)
def update_priorities(request: PriorityWeightsRequest, authorization: str | None = Header(default=None)):
    user_id = authenticate_user(authorization)
    verify_strategy_run_ownership(request.planning_unit_id, request.strategy_run_id, user_id)
    return StrategyService().update_priorities(request)


@router.post("/select", response_model=StrategyRun)
def select_strategy(request: StrategySelectRequest, authorization: str | None = Header(default=None)):
    user_id = authenticate_user(authorization)
    verify_strategy_run_ownership(request.planning_unit_id, request.strategy_run_id, user_id)
    return StrategyService().select_strategy(request)


@router.get("/runs/{goal_id}/latest", response_model=StrategyRun)
def get_latest_run(goal_id: str, planning_unit_id: str = Query(...), authorization: str | None = Header(default=None)):
    user_id = authenticate_user(authorization)
    verify_goal_ownership(planning_unit_id, goal_id, user_id)
    return StrategyService().get_latest_run(planning_unit_id, goal_id)


@router.get("/runs/{goal_id}/history")
def get_run_history(goal_id: str, planning_unit_id: str = Query(...), authorization: str | None = Header(default=None)):
    user_id = authenticate_user(authorization)
    verify_goal_ownership(planning_unit_id, goal_id, user_id)
    return StrategyService().get_run_history(planning_unit_id, goal_id)


@router.get("/runs/{strategy_run_id}/report")
def get_goal_strategy_report(strategy_run_id: str, planning_unit_id: str = Query(...), authorization: str | None = Header(default=None)):
    user_id = authenticate_user(authorization)
    verify_strategy_run_ownership(planning_unit_id, strategy_run_id, user_id)
    return GoalReportService().build_report(planning_unit_id, strategy_run_id)


@router.get("/runs/{strategy_run_id}/report.pdf")
def download_goal_strategy_report_pdf(strategy_run_id: str, planning_unit_id: str = Query(...), authorization: str | None = Header(default=None)):
    user_id = authenticate_user(authorization)
    verify_strategy_run_ownership(planning_unit_id, strategy_run_id, user_id)
    pdf = GoalReportService().generate_pdf(planning_unit_id, strategy_run_id)
    return Response(content=pdf, media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename=goal-strategy-report-{strategy_run_id}.pdf"})


@router.get("/runs/{strategy_run_id}/retirement-report")
def get_retirement_report(strategy_run_id: str, planning_unit_id: str = Query(...), authorization: str | None = Header(default=None)):
    user_id = authenticate_user(authorization)
    verify_strategy_run_ownership(planning_unit_id, strategy_run_id, user_id)
    return StrategyService().get_retirement_report(planning_unit_id, strategy_run_id)


@router.get("/runs/{strategy_run_id}/retirement-report.pdf")
def download_retirement_report_pdf(strategy_run_id: str, planning_unit_id: str = Query(...), authorization: str | None = Header(default=None)):
    user_id = authenticate_user(authorization)
    verify_strategy_run_ownership(planning_unit_id, strategy_run_id, user_id)
    pdf = RetirementReportPDFService().generate(planning_unit_id, strategy_run_id)
    return Response(content=pdf, media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename=retirement-planning-report-{strategy_run_id}.pdf"})
