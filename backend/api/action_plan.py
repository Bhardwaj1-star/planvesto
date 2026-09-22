from fastapi import APIRouter, Header, HTTPException

from api.auth import authenticate_user, verify_action_ownership, verify_planning_unit_ownership, verify_strategy_version_ownership
from data.action_plan_repository import ActionPlanRepository
from data.strategy_repository import StrategyRepository
from models.action_plan import ActionPlanItem, ActionDecisionRecord
from schemas.action_plan import ActionCompletionRequest, ActionCreateRequest, ActionDecisionRequest, ActionDecisionResponse
from services.action_plan_service import ActionPlanService
from services.financial_state_service import FinancialStateService

router = APIRouter(prefix="/api/action-plan", tags=["Action Plan"])


def _service():
    return ActionPlanService(ActionPlanRepository(StrategyRepository().db))


@router.get("/actions", response_model=list[ActionPlanItem])
def list_actions(planning_unit_id: str, authorization: str | None = Header(default=None)):
    user_id = authenticate_user(authorization)
    verify_planning_unit_ownership(planning_unit_id, user_id)
    return _service().repository.list_actions(planning_unit_id)


@router.post("/actions/generate", response_model=list[ActionPlanItem])
def generate_actions(planning_unit_id: str, strategy_version_id: str, authorization: str | None = Header(default=None)):
    user_id = authenticate_user(authorization)
    verify_strategy_version_ownership(planning_unit_id, strategy_version_id, user_id)
    from services.strategy_action_generator import StrategyActionGenerator
    try:
        return StrategyActionGenerator(_service().repository).generate(planning_unit_id, strategy_version_id)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.get("/actions/{action_id}", response_model=ActionPlanItem)
def get_action(action_id: str, planning_unit_id: str, authorization: str | None = Header(default=None)):
    user_id = authenticate_user(authorization)
    verify_action_ownership(planning_unit_id, action_id, user_id)
    action = _service().repository.get_action(planning_unit_id, action_id)
    if action is None:
        raise HTTPException(status_code=404, detail="Action not found")
    return action


@router.get("/decisions", response_model=list[ActionDecisionRecord])
def list_decision_history(planning_unit_id: str, action_id: str | None = None, authorization: str | None = Header(default=None)):
    user_id = authenticate_user(authorization)
    verify_planning_unit_ownership(planning_unit_id, user_id)
    if action_id:
        verify_action_ownership(planning_unit_id, action_id, user_id)
    return _service().repository.list_decision_history(planning_unit_id, action_id)


@router.post("/actions")
def create_action(request: ActionCreateRequest, authorization: str | None = Header(default=None)):
    user_id = authenticate_user(authorization)
    verify_strategy_version_ownership(request.planning_unit_id, request.strategy_version_id, user_id)
    try:
        return _service().build_action(**request.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.post("/actions/{action_id}/complete", response_model=ActionPlanItem)
def complete_action(
    action_id: str,
    request: ActionCompletionRequest,
    authorization: str | None = Header(default=None),
):
    user_id = authenticate_user(authorization)
    verify_action_ownership(request.planning_unit_id, action_id, user_id)
    if request.action_id != action_id:
        raise HTTPException(status_code=400, detail="action_id in path and body must match")
    service = _service()
    action = service.repository.get_action(request.planning_unit_id, action_id)
    if action is None:
        raise HTTPException(status_code=404, detail="Action not found")
    actual_state = request.actual_state
    if not actual_state:
        actual_state = FinancialStateService().build(request.planning_unit_id).model_dump(mode="json")
    try:
        updated, _, _ = service.complete_action_with_actual_state(action, actual_state, request.completion_preview)
        return updated
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.post("/decisions", response_model=ActionDecisionResponse)
def confirm_action_decision(request: ActionDecisionRequest, authorization: str | None = Header(default=None)):
    user_id = authenticate_user(authorization)
    verify_action_ownership(request.planning_unit_id, request.action_id, user_id)
    service = _service()
    action = service.repository.get_action(request.planning_unit_id, request.action_id)
    if action is None:
        raise HTTPException(status_code=404, detail="Action not found")
    record = service.confirm_decision(action, request.decision, request.impact_preview, request.after_state)
    return ActionDecisionResponse(
        decision_id=record.decision_id,
        action_id=record.action_id,
        decision=record.decision,
        confirmed_at=record.confirmed_at,
        historical=record.historical,
    )
