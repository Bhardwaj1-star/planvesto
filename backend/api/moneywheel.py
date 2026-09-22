from fastapi import APIRouter, Header

from api.auth import authenticate_user, verify_planning_unit_ownership
from data.moneywheel_repository import MoneywheelRepository
from schemas.moneywheel import MoneywheelCalculateRequest, MoneywheelResponse
from services.financial_state_service import FinancialStateService
from services.moneywheel_service import MoneywheelService

router = APIRouter(prefix="/api/moneywheel", tags=["Moneywheel"])


def _service():
    return MoneywheelService(MoneywheelRepository())


@router.post("/calculate", response_model=MoneywheelResponse)
def calculate_moneywheel(request: MoneywheelCalculateRequest, authorization: str | None = Header(default=None)):
    user_id = authenticate_user(authorization)
    verify_planning_unit_ownership(request.planning_unit_id, user_id)
    # Client-provided financial_state_snapshot is intentionally ignored.
    financial_state = FinancialStateService().build(request.planning_unit_id, "family")
    return MoneywheelResponse(result=_service().calculate_from_financial_state(financial_state))


@router.get("/latest/{planning_unit_id}")
def latest_moneywheel(planning_unit_id: str, authorization: str | None = Header(default=None)):
    user_id = authenticate_user(authorization)
    verify_planning_unit_ownership(planning_unit_id, user_id)
    return _service().repository.get_latest(planning_unit_id)


@router.get("/history/{planning_unit_id}")
def moneywheel_history(planning_unit_id: str, authorization: str | None = Header(default=None)):
    user_id = authenticate_user(authorization)
    verify_planning_unit_ownership(planning_unit_id, user_id)
    return _service().repository.get_history(planning_unit_id)
