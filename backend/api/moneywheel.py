from fastapi import APIRouter, Header

from api.auth import authenticate_user, verify_planning_unit_ownership
from data.moneywheel_repository import MoneywheelRepository
from models.financial_state import FinancialState
from schemas.moneywheel import MoneywheelCalculateRequest, MoneywheelResponse
from services.moneywheel_service import MoneywheelService

router = APIRouter(prefix="/api/moneywheel", tags=["Moneywheel"])


def _service():
    return MoneywheelService(MoneywheelRepository())


@router.post("/calculate", response_model=MoneywheelResponse)
def calculate_moneywheel(
    request: MoneywheelCalculateRequest,
    authorization: str | None = Header(default=None),
):
    user_id = authenticate_user(authorization)
    verify_planning_unit_ownership(request.planning_unit_id, user_id)

    service = _service()
    if request.financial_state_snapshot:
        financial_state = FinancialState.model_validate(request.financial_state_snapshot)
        result = service.calculate_from_financial_state(financial_state)
    else:
        data = request.model_dump(exclude={"financial_state_snapshot"})
        result = service.calculate(
            request.__class__.model_validate(data),
            request.financial_state_snapshot,
        )
    return MoneywheelResponse(result=result)


@router.get("/latest/{planning_unit_id}")
def latest_moneywheel(
    planning_unit_id: str,
    authorization: str | None = Header(default=None),
):
    user_id = authenticate_user(authorization)
    verify_planning_unit_ownership(planning_unit_id, user_id)
    return _service().repository.get_latest(planning_unit_id)


@router.get("/history/{planning_unit_id}")
def moneywheel_history(
    planning_unit_id: str,
    authorization: str | None = Header(default=None),
):
    user_id = authenticate_user(authorization)
    verify_planning_unit_ownership(planning_unit_id, user_id)
    return _service().repository.get_history(planning_unit_id)
