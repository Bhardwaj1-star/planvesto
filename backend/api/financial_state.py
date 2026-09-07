from fastapi import APIRouter, Header, HTTPException

from data.supabase import get_supabase
from schemas.financial_state import FinancialStateRequest
from services.financial_state_service import FinancialStateService

router = APIRouter(prefix="/api/financial-state", tags=["Financial State"])


def _authenticate(authorization: str | None) -> str:
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization token required")
    token = authorization.removeprefix("Bearer ").strip()
    try:
        result = get_supabase().auth.get_user(token)
    except Exception as exc:
        raise HTTPException(status_code=401, detail="Invalid authorization token") from exc
    user = getattr(result, "user", None)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authorization token")
    return user.id


def _verify_planning_unit(planning_unit_id: str, user_id: str) -> None:
    result = (get_supabase().table("planning_units").select("planning_unit_id")
              .eq("planning_unit_id", planning_unit_id).eq("user_id", user_id).maybe_single().execute())
    if not result.data:
        raise HTTPException(status_code=403, detail="Planning unit does not belong to authenticated user")


@router.post("/build")
def build_financial_state(request: FinancialStateRequest, authorization: str | None = Header(default=None)):
    user_id = _authenticate(authorization)
    _verify_planning_unit(request.planning_unit_id, user_id)
    return FinancialStateService().build(request.planning_unit_id, request.scope, request.investor_id)
