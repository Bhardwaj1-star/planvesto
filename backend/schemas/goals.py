from typing import Literal
from pydantic import BaseModel, Field


class AssetMappingInput(BaseModel):
    asset_id: str
    allocation_type: Literal["currency", "percentage"]
    allocation_value: float = Field(ge=0)
    expected_return: float | None = Field(default=None, ge=-0.99, le=1.0)
    return_frequency: Literal["annual", "semi-annual", "semiannual", "half-yearly", "quarterly", "monthly"] = "annual"


class GoalInput(BaseModel):
    planning_unit_id: str
    goal_id: str | None = None
    investor_id: str | None = None
    goal_name: str = Field(min_length=1, max_length=200)
    goal_type: str = Field(min_length=1, max_length=100)
    today_cost: float = Field(gt=0)
    target_month: int = Field(ge=1, le=12)
    target_year: int = Field(ge=2026, le=2200)
    inflation_rate: float | None = Field(default=None, ge=0, le=1)
    priority: str = Field(default="Important", min_length=1, max_length=50)
    flexibility: str = Field(default="Flexible", min_length=1, max_length=50)
    status: str = Field(default="Active", min_length=1, max_length=30)
    asset_mappings: list[AssetMappingInput] = Field(default_factory=list, max_length=100)


class GoalCalculateRequest(GoalInput):
    pass


class GoalSummary(BaseModel):
    goal_id: str
    planning_unit_id: str
    goal_name: str
    target_amount: float
    target_date: str | None = None
    priority: str | None = None
    flexibility: str | None = None
