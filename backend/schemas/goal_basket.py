from __future__ import annotations

from pydantic import BaseModel, Field


class GoalBasketBuildRequest(BaseModel):
    planning_unit_id: str
    basket_id: str
    name: str = Field(min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=500)
    goal_ids: list[str] = Field(min_length=1)
    priority: str | None = None


class GoalBasketResponse(BaseModel):
    basket_id: str
    planning_unit_id: str
    name: str
    description: str | None = None
    goal_ids: list[str]
    goal_count: int
    goal_names: list[str]
    priorities: list[str]
    total_required_monthly_contribution: float
    total_funding_gap: float
