from fastapi import APIRouter, Header, Query, HTTPException
from api.auth import authenticate_user, verify_investor_ownership, verify_financial_snapshot_ownership
from schemas.profile import ProfileBuildRequest
from services.profile_service import ProfileService

router = APIRouter(prefix="/api/profile", tags=["Profile Engine"])


@router.post("/build")
def build_profile(request: ProfileBuildRequest, authorization: str | None = Header(default=None)):
    user_id = authenticate_user(authorization)
    verify_investor_ownership(request.planning_unit_id, request.investor_id, user_id)
    if request.financial_snapshot_id:
        verify_financial_snapshot_ownership(request.planning_unit_id, request.financial_snapshot_id, user_id)
    try:
        return ProfileService().build(request)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.get("/latest")
def get_latest_profile(
    planning_unit_id: str = Query(...),
    investor_id: str = Query(...),
    authorization: str | None = Header(default=None),
):
    user_id = authenticate_user(authorization)
    verify_investor_ownership(planning_unit_id, investor_id, user_id)
    result = ProfileService().latest(planning_unit_id, investor_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Investor profile not found")
    return result


@router.get("/history")
def get_profile_history(
    planning_unit_id: str = Query(...),
    investor_id: str = Query(...),
    limit: int = Query(default=20, ge=1, le=100),
    authorization: str | None = Header(default=None),
):
    user_id = authenticate_user(authorization)
    verify_investor_ownership(planning_unit_id, investor_id, user_id)
    return ProfileService().history(planning_unit_id, investor_id, limit)
