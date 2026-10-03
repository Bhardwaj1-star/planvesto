from __future__ import annotations

from typing import Any
from pydantic import BaseModel, Field, field_validator

from rules.goals import GoalPriorityLevel, canonical_goal_priority
from rules.multi_goal import FundingStatusType, FeasibilityStatusType


class GoalEvaluationInput(BaseModel):
    goal_id: str
    goal_name: str
    goal_type: str = "general"
    client_priority: GoalPriorityLevel = "medium"
    target_date: str | None = None
    target_year: int | None = None
    target_month: int | None = None
    today_cost: float = 0.0
    future_target: float = 0.0
    funding_gap: float = 0.0
    required_monthly_contribution: float = 0.0
    flexibility: str | None = None
    is_essential: bool = False
    defined_goal: Any = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("client_priority", mode="before")
    @classmethod
    def normalize_client_priority(cls, value):
        if isinstance(value, str):
            return canonical_goal_priority(value)
        return value


class GoalResolution(BaseModel):
    goal_id: str
    goal_name: str
    goal_type: str
    client_priority: GoalPriorityLevel
    resolved_priority: GoalPriorityLevel
    target_date: str | None = None
    required_monthly_contribution: float = 0.0
    allocated_monthly_contribution: float = 0.0
    shortfall: float = 0.0
    funding_status: FundingStatusType = "fully_funded"
    feasibility_status: FeasibilityStatusType = "feasible"
    recommended_strategy_id: str | None = None
    recommended_strategy_name: str | None = None
    override_applied: bool = False
    override_reason: str | None = None
    reasons: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class MultiGoalPlanResult(BaseModel):
    planning_unit_id: str | None = None
    financial_state: dict[str, Any] = Field(default_factory=dict)
    total_available_surplus: float | None = None
    total_required_contribution: float = 0.0
    total_allocated_contribution: float = 0.0
    monthly_gap: float | None = None
    overall_funding_status: FundingStatusType = "requires_review"
    goals: list[GoalResolution] = Field(default_factory=list)
    competing_resources_detected: bool = False
    trade_offs: list[str] = Field(default_factory=list)
    action_plan: list[dict[str, Any]] = Field(default_factory=list)
    audit_trail: list[dict[str, Any]] = Field(default_factory=list)
    planning_notes: list[str] = Field(default_factory=list)
