from fastapi import APIRouter, Header, Query
from api.auth import authenticate_user, verify_assets_ownership, verify_investor_ownership, verify_planning_unit_ownership
from models.defined_goal import DefinedGoal, DefinedGoalVersionSummary
from schemas.goals import GoalCalculateRequest, GoalInput, GoalSummary
from services.goal_service import GoalService

router = APIRouter(prefix="/api/goals", tags=["Goal Planner & DefinedGoal"])


def _validate_goal_request(request: GoalInput, user_id: str) -> None:
    verify_planning_unit_ownership(request.planning_unit_id, user_id)
    if request.investor_id:
        verify_investor_ownership(request.planning_unit_id, request.investor_id, user_id)
    verify_assets_ownership(request.planning_unit_id, [m.asset_id for m in request.asset_mappings], user_id)


@router.get("", response_model=list[GoalSummary])
def list_goals(planning_unit_id: str = Query(...), authorization: str | None = Header(default=None)):
    user_id = authenticate_user(authorization)
    verify_planning_unit_ownership(planning_unit_id, user_id)
    return GoalService().repository.list_goals(planning_unit_id)


@router.post("/calculate", response_model=DefinedGoal)
def calculate_goal_preview(request: GoalCalculateRequest, authorization: str | None = Header(default=None)):
    user_id = authenticate_user(authorization)
    _validate_goal_request(request, user_id)
    return GoalService().calculate_preview(request)


@router.post("", response_model=DefinedGoal)
def save_and_define_goal(request: GoalInput, authorization: str | None = Header(default=None)):
    user_id = authenticate_user(authorization)
    _validate_goal_request(request, user_id)
    return GoalService().save_and_define_goal(request)


@router.get("/{goal_id}/defined/latest", response_model=DefinedGoal)
def get_latest_defined_goal(goal_id: str, planning_unit_id: str = Query(...), authorization: str | None = Header(default=None)):
    user_id = authenticate_user(authorization)
    verify_planning_unit_ownership(planning_unit_id, user_id)
    return GoalService().get_latest_defined_goal(planning_unit_id, goal_id)


@router.get("/{goal_id}/defined/versions", response_model=list[DefinedGoalVersionSummary])
def get_defined_goal_versions(goal_id: str, planning_unit_id: str = Query(...), authorization: str | None = Header(default=None)):
    user_id = authenticate_user(authorization)
    verify_planning_unit_ownership(planning_unit_id, user_id)
    return GoalService().get_version_history(planning_unit_id, goal_id)


@router.get("/{goal_id}/defined/versions/{version}", response_model=DefinedGoal)
def get_defined_goal_version(goal_id: str, version: int, planning_unit_id: str = Query(...), authorization: str | None = Header(default=None)):
    user_id = authenticate_user(authorization)
    verify_planning_unit_ownership(planning_unit_id, user_id)
    return GoalService().get_defined_goal_version(planning_unit_id, goal_id, version)
