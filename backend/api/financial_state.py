from fastapi import APIRouter, Header, HTTPException, Query

from api.auth import authenticate_user, verify_investor_ownership, verify_planning_unit_ownership
from data.financial_state_repository import FinancialStateSnapshotRepository
from schemas.financial_state import FinancialStateRequest
from services.financial_state_service import FinancialStateService

router = APIRouter(prefix="/api/financial-state", tags=["Financial State"])


def _validate_scope(planning_unit_id: str, scope: str, investor_id: str | None, user_id: str) -> None:
    verify_planning_unit_ownership(planning_unit_id, user_id)
    if scope == "individual":
        if not investor_id:
            raise HTTPException(status_code=400, detail="investor_id is required for individual scope")
        verify_investor_ownership(planning_unit_id, investor_id, user_id)
    elif scope == "family":
        if investor_id:
            raise HTTPException(status_code=400, detail="investor_id is only valid for individual scope")
    else:
        raise HTTPException(status_code=400, detail="scope must be family or individual")


@router.post("/build")
def build_financial_state(request: FinancialStateRequest, authorization: str | None = Header(default=None)):
    user_id = authenticate_user(authorization)
    _validate_scope(request.planning_unit_id, request.scope, request.investor_id, user_id)
    return FinancialStateService().build(request.planning_unit_id, request.scope, request.investor_id)


@router.get("/latest/{planning_unit_id}")
def get_latest_financial_state_snapshot(planning_unit_id: str, scope: str = Query(default="family"), investor_id: str | None = Query(default=None), authorization: str | None = Header(default=None)):
    user_id = authenticate_user(authorization)
    _validate_scope(planning_unit_id, scope, investor_id, user_id)
    snapshot = FinancialStateSnapshotRepository().get_latest(planning_unit_id, scope, investor_id)
    if snapshot is None:
        return FinancialStateService().build(planning_unit_id, scope, investor_id)
    return snapshot


@router.get("/history/{planning_unit_id}")
def get_financial_state_snapshot_history(planning_unit_id: str, scope: str = Query(default="family"), investor_id: str | None = Query(default=None), limit: int = Query(default=20, ge=1, le=100), authorization: str | None = Header(default=None)):
    user_id = authenticate_user(authorization)
    _validate_scope(planning_unit_id, scope, investor_id, user_id)
    return FinancialStateSnapshotRepository().get_history(planning_unit_id, scope, investor_id, limit)
