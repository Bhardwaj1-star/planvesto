from typing import Literal
from pydantic import BaseModel


class FinancialStateRequest(BaseModel):
    planning_unit_id: str
    scope: Literal["family", "individual"] = "family"
    investor_id: str | None = None
