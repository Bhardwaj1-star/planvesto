from fastapi import APIRouter, Header, HTTPException

from api.auth import authenticate_user, verify_planning_unit_ownership
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
