from fastapi import APIRouter, Header, HTTPException, Query
from api.auth import authenticate_user, verify_assets_ownership, verify_goal_ownership, verify_planning_unit_ownership
from models.goal_funding import GoalFundingAssessment
from schemas.goal_funding import GoalFundingAssessmentRequest
from services.goal_funding_service import GoalFundingService

router = APIRouter(prefix="/api/goal-funding", tags=["Goal Funding Strategy"])


@router.post("/assess", response_model=GoalFundingAssessment)
def assess_goal_funding(request: GoalFundingAssessmentRequest, authorization: str | None = Header(default=None)):
    user_id = authenticate_user(authorization)
    verify_goal_ownership(request.planning_unit_id, request.goal_id, user_id)
    asset_ids = list({decision.asset_id for path in (request.self_money, request.self_money_financing) for decision in path.asset_decisions})
    if asset_ids:
        verify_assets_ownership(request.planning_unit_id, asset_ids, user_id)
    try:
        return GoalFundingService().assess(request)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.get("/{goal_id}/latest", response_model=GoalFundingAssessment | None)
def get_latest_goal_funding(goal_id: str, planning_unit_id: str = Query(...), authorization: str | None = Header(default=None)):
    user_id = authenticate_user(authorization)
    verify_goal_ownership(planning_unit_id, goal_id, user_id)
    return GoalFundingService().latest(planning_unit_id, goal_id)


@router.get("/{goal_id}/history")
def get_goal_funding_history(goal_id: str, planning_unit_id: str = Query(...), authorization: str | None = Header(default=None)):
    user_id = authenticate_user(authorization)
    verify_goal_ownership(planning_unit_id, goal_id, user_id)
    return GoalFundingService().history(planning_unit_id, goal_id)
