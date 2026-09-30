from __future__ import annotations

from pydantic import BaseModel, Field


class GoalBasket(BaseModel):
    """Logical client-defined grouping of existing goals.

    A basket groups goals for planning/orchestration; it does not replace an
    individual goal or become a strategy itself.
    """

    basket_id: str
    planning_unit_id: str
    name: str
    description: str | None = None
    goal_ids: list[str] = Field(default_factory=list)
    priority: str | None = None
    status: str = "active"


class GoalBasketSummary(BaseModel):
    basket_id: str
    planning_unit_id: str
    name: str
    goal_count: int
    goal_ids: list[str]
    total_required_monthly_contribution: float
    total_funding_gap: float
    priorities: list[str] = Field(default_factory=list)
    goal_names: list[str] = Field(default_factory=list)
