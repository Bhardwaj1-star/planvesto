from typing import Literal
from pydantic import BaseModel, Field


class AssetMappingInput(BaseModel):
    asset_id: str
    allocation_type: Literal["currency", "percentage"]
    allocation_value: float
    expected_return: float | None = None
    return_frequency: str = "annual"


class GoalInput(BaseModel):
    planning_unit_id: str
    goal_id: str | None = None
    investor_id: str | None = None
    goal_name: str
    goal_type: str
    today_cost: float
    target_month: int
    target_year: int
    inflation_rate: float | None = None
    priority: str = "Important"
    flexibility: str = "Flexible"
    status: str = "Active"
    asset_mappings: list[AssetMappingInput] = Field(default_factory=list)


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
