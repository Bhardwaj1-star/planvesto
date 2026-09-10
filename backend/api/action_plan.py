from fastapi import APIRouter, Header

from api.auth import authenticate_user, verify_planning_unit_ownership
from data.action_plan_repository import ActionPlanRepository
from data.strategy_repository import StrategyRepository
from models.action_plan import ActionImpactPreview
from schemas.action_plan import ActionCreateRequest, ActionDecisionRequest, ActionDecisionResponse
from services.action_plan_service import ActionPlanService

router = APIRouter(prefix="/api/action-plan", tags=["Action Plan"])


def _service():
    return ActionPlanService(ActionPlanRepository(StrategyRepository().db))


@router.post("/actions")
def create_action(request: ActionCreateRequest, authorization: str | None = Header(default=None)):
    user_id = authenticate_user(authorization)
    verify_planning_unit_ownership(request.planning_unit_id, user_id)
    return _service().build_action(**request.model_dump())


@router.post("/decisions", response_model=ActionDecisionResponse)
def confirm_action_decision(request: ActionDecisionRequest, authorization: str | None = Header(default=None)):
    user_id = authenticate_user(authorization)
    verify_planning_unit_ownership(request.planning_unit_id, user_id)
    service = _service()
    action = service.repository.get_action(request.planning_unit_id, request.action_id)
    if action is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Action not found")
    record = service.confirm_decision(action, request.decision, request.impact_preview, request.after_state)
    return ActionDecisionResponse(
        decision_id=record.decision_id,
        action_id=record.action_id,
        decision=record.decision,
        confirmed_at=record.confirmed_at,
        historical=record.historical,
    )
