from typing import Literal
from pydantic import Field
from schemas.base import StrictRequestModel


class FinancialStateRequest(StrictRequestModel):
    planning_unit_id: str = Field(min_length=1, max_length=100)
    scope: Literal["family", "individual"] = "family"
    investor_id: str | None = Field(default=None, min_length=1, max_length=100)
