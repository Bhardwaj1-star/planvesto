from fastapi import APIRouter, Header, Query
from api.auth import authenticate_user, verify_planning_unit_ownership
from models.strategy import StrategyRun
from schemas.strategy import CustomScenarioRequest, PriorityWeightsRequest, StrategyBuildRequest, StrategySelectRequest
from services.strategy_service import StrategyService

router = APIRouter(prefix="/api/strategy", tags=["Strategy Builder"])


@router.post("/build", response_model=StrategyRun)
def build_strategy(request: StrategyBuildRequest, authorization: str | None = Header(default=None)):
    user_id = authenticate_user(authorization)
    verify_planning_unit_ownership(request.planning_unit_id, user_id)
    return StrategyService().build_strategy(request.planning_unit_id, request.goal_id, request.investor_priorities)


@router.post("/scenarios/custom", response_model=StrategyRun)
def add_custom_scenario(request: CustomScenarioRequest, authorization: str | None = Header(default=None)):
    user_id = authenticate_user(authorization)
    verify_planning_unit_ownership(request.planning_unit_id, user_id)
    return StrategyService().add_custom_scenario(request)


@router.post("/priorities", response_model=StrategyRun)
def update_priorities(request: PriorityWeightsRequest, authorization: str | None = Header(default=None)):
    user_id = authenticate_user(authorization)
    verify_planning_unit_ownership(request.planning_unit_id, user_id)
    return StrategyService().update_priorities(request)


@router.post("/select", response_model=StrategyRun)
def select_strategy(request: StrategySelectRequest, authorization: str | None = Header(default=None)):
    user_id = authenticate_user(authorization)
    verify_planning_unit_ownership(request.planning_unit_id, user_id)
    return StrategyService().select_strategy(request)


@router.get("/runs/{goal_id}/latest", response_model=StrategyRun)
def get_latest_run(goal_id: str, planning_unit_id: str = Query(...), authorization: str | None = Header(default=None)):
    user_id = authenticate_user(authorization)
    verify_planning_unit_ownership(planning_unit_id, user_id)
    return StrategyService().get_latest_run(planning_unit_id, goal_id)


@router.get("/runs/{goal_id}/history")
def get_run_history(goal_id: str, planning_unit_id: str = Query(...), authorization: str | None = Header(default=None)):
    user_id = authenticate_user(authorization)
    verify_planning_unit_ownership(planning_unit_id, user_id)
    return StrategyService().get_run_history(planning_unit_id, goal_id)
