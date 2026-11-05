from typing import Any
from pydantic import BaseModel, Field


class DashboardGoal(BaseModel):
    goal_id: str
    goal_name: str
    goal_type: str
    target_amount: float
    target_date: str | None = None
    priority: str | None = None
    flexibility: str | None = None
    funding_status: str | None = None
    funding_gap: float | None = None
    projected_mapped_asset_value: float | None = None
    coverage_percentage: float | None = None
    image_key: str = "default"


class DashboardResponse(BaseModel):
    planning_unit_id: str
    scope: str
    financial_state: dict[str, Any] = Field(default_factory=dict)
    goals: list[DashboardGoal] = Field(default_factory=list)
