from fastapi import APIRouter, Header, HTTPException, Query

from api.auth import authenticate_user, verify_investor_ownership, verify_planning_unit_ownership
from services.dashboard_service import DashboardService

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("")
def get_dashboard(
    planning_unit_id: str = Query(...),
    scope: str = Query(default="family"),
    investor_id: str | None = Query(default=None),
    authorization: str | None = Header(default=None),
):
    user_id = authenticate_user(authorization)
    verify_planning_unit_ownership(planning_unit_id, user_id)
    if scope not in ("family", "individual"):
        raise HTTPException(status_code=400, detail="scope must be family or individual")
    if scope == "individual":
        if not investor_id:
            raise HTTPException(status_code=400, detail="investor_id is required for individual scope")
        verify_investor_ownership(planning_unit_id, investor_id, user_id)
    elif investor_id:
        raise HTTPException(status_code=400, detail="investor_id is only valid for individual scope")
    return DashboardService().build(planning_unit_id, scope, investor_id)
