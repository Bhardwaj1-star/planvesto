from fastapi import APIRouter, Header, HTTPException, Query

from api.auth import authenticate_user, verify_planning_unit_ownership
from data.financial_state_repository import FinancialStateSnapshotRepository
from schemas.financial_state import FinancialStateRequest
from services.financial_state_service import FinancialStateService

router = APIRouter(prefix="/api/financial-state", tags=["Financial State"])

# Backwards compatibility aliases
_authenticate = authenticate_user
_verify_planning_unit = verify_planning_unit_ownership


@router.post("/build")
def build_financial_state(request: FinancialStateRequest, authorization: str | None = Header(default=None)):
    user_id = _authenticate(authorization)
    _verify_planning_unit(request.planning_unit_id, user_id)
    return FinancialStateService().build(request.planning_unit_id, request.scope, request.investor_id)


def _validate_snapshot_request(
    planning_unit_id: str,
    scope: str,
    investor_id: str | None,
    user_id: str,
) -> None:
    _verify_planning_unit(planning_unit_id, user_id)
    if scope == "individual" and not investor_id:
        raise HTTPException(status_code=400, detail="investor_id is required for individual scope")
    if scope not in ("family", "individual"):
        raise HTTPException(status_code=400, detail="scope must be family or individual")


@router.get("/latest/{planning_unit_id}")
def get_latest_financial_state_snapshot(
    planning_unit_id: str,
    scope: str = Query(default="family"),
    investor_id: str | None = Query(default=None),
    authorization: str | None = Header(default=None),
):
    user_id = _authenticate(authorization)
    _validate_snapshot_request(planning_unit_id, scope, investor_id, user_id)
    snapshot = FinancialStateSnapshotRepository().get_latest(planning_unit_id, scope, investor_id)
    if snapshot is None:
        raise HTTPException(status_code=404, detail="Financial State snapshot not found")
    return snapshot


@router.get("/history/{planning_unit_id}")
def get_financial_state_snapshot_history(
    planning_unit_id: str,
    scope: str = Query(default="family"),
    investor_id: str | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    authorization: str | None = Header(default=None),
):
    user_id = _authenticate(authorization)
    _validate_snapshot_request(planning_unit_id, scope, investor_id, user_id)
    return FinancialStateSnapshotRepository().get_history(planning_unit_id, scope, investor_id, limit)
