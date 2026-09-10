from typing import Any

from pydantic import BaseModel, Field

from models.moneywheel import MoneywheelInput, MoneywheelResult


class MoneywheelCalculateRequest(MoneywheelInput):
    financial_state_snapshot: dict[str, Any] = Field(default_factory=dict)


class MoneywheelResponse(BaseModel):
    result: MoneywheelResult
