from __future__ import annotations

from typing import Any
from pydantic import BaseModel, Field
from rules.goals import GoalPriorityLevel
from rules.multi_goal import FundingStatusType, FeasibilityStatusType


class GoalAllocationResult(BaseModel):
    goal_id: str
    goal_name: str
    goal_type: str = "general"
    client_priority: GoalPriorityLevel
    resolved_priority: GoalPriorityLevel
    target_date: str | None = None
    required_monthly_contribution: float = 0.0
    allocated_monthly_contribution: float = 0.0
    monthly_shortfall: float = 0.0
    funding_percentage: float = 0.0
    funding_status: FundingStatusType = "fully_funded"
    feasibility_status: FeasibilityStatusType = "feasible"
    allocation_reasoning: str = ""
    override_applied: bool = False
    override_reason: str | None = None
    trade_off_impact: str | None = None


class ConsolidatedAllocationResult(BaseModel):
    total_available_monthly_surplus: float | None = None
    total_required_monthly_contribution: float = 0.0
    total_allocated_monthly_contribution: float = 0.0
    net_monthly_gap: float | None = None
    overall_funding_status: FundingStatusType = "requires_review"
    competition_detected: bool = False
    allocations: list[GoalAllocationResult] = Field(default_factory=list)
    trade_offs: list[str] = Field(default_factory=list)
    decision_log: list[str] = Field(default_factory=list)
