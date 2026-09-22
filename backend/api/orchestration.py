from fastapi import APIRouter, Header, HTTPException

from api.auth import (
    authenticate_user,
    verify_defined_goal_ownership,
    verify_investor_ownership,
    verify_planning_unit_ownership,
    verify_strategy_version_ownership,
)
from schemas.orchestration import PlanningOrchestrationRequest
from services.planning_orchestration_service import PlanningOrchestrationService

router = APIRouter(prefix="/api/orchestration", tags=["Planning Orchestration"])


@router.post("/context")
def build_planning_context(
    request: PlanningOrchestrationRequest,
    authorization: str | None = Header(default=None),
):
    user_id = authenticate_user(authorization)
    verify_planning_unit_ownership(request.planning_unit_id, user_id)

    if request.scope == "individual":
        if not request.investor_id:
            raise HTTPException(status_code=400, detail="investor_id is required for individual scope")
        verify_investor_ownership(request.planning_unit_id, request.investor_id, user_id)
    elif request.investor_id:
        raise HTTPException(status_code=400, detail="investor_id is only valid for individual scope")

    for defined_goal_id in request.goal_version_ids:
        verify_defined_goal_ownership(request.planning_unit_id, defined_goal_id, user_id)

    if request.strategy_version_id:
        verify_strategy_version_ownership(request.planning_unit_id, request.strategy_version_id, user_id)

    return PlanningOrchestrationService().build_context(**request.model_dump())
