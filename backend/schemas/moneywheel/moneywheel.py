from pydantic import Field

from models.moneywheel import MoneywheelInput, MoneywheelResult
from schemas.base import StrictRequestModel


class MoneywheelCalculateRequest(MoneywheelInput, StrictRequestModel):
    # Retained for backwards compatibility; the API deliberately ignores it and
    # rebuilds financial state from server-owned data.
    financial_state_snapshot: dict = Field(default_factory=dict, max_length=50)


class MoneywheelResponse(StrictRequestModel):
    result: MoneywheelResult
