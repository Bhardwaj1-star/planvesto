from __future__ import annotations

from typing import Any, Literal
from pydantic import BaseModel, Field

GoalPriorityLevel = Literal["critical", "high", "medium", "low"]
FundingStatusType = Literal["fully_funded", "partially_funded", "unfunded", "within_surplus", "surplus_shortfall", "requires_review"]
FeasibilityStatusType = Literal["feasible", "constrained", "infeasible"]


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
