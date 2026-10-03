from __future__ import annotations

from typing import Any, Literal
from pydantic import Field
from schemas.base import StrictRequestModel
from rules.goals import GoalPriority


class MultiGoalPlanRequest(StrictRequestModel):
    planning_unit_id: str = Field(min_length=1, max_length=100)
    rule_overrides: dict[str, dict[str, Any]] | None = None


class GoalPriorityOverrideItem(StrictRequestModel):
    goal_id: str = Field(min_length=1, max_length=100)
    resolved_priority: GoalPriority
    reason: str = Field(min_length=1, max_length=500)
