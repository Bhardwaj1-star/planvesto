from __future__ import annotations

from typing import Any, Literal
from pydantic import BaseModel, Field
from engines.orchestration.models import GoalPriorityLevel

ConstraintSeverity = Literal["hard", "warning", "info"]
RatioStatus = Literal["excellent", "healthy", "attention", "critical"]


class FinancialRatioResult(BaseModel):
    ratio_key: str
    name: str
    value: float | None = None
    unit: str
    status: RatioStatus | None = None
    benchmark: str = ""
    evidence: dict[str, Any] = Field(default_factory=dict)


class ConstraintCheckResult(BaseModel):
    rule_id: str
    goal_id: str | None = None
    severity: ConstraintSeverity
    passed: bool
    message: str
    suggested_override_priority: GoalPriorityLevel | None = None
    override_reason: str | None = None
    ratio_evidence: dict[str, Any] = Field(default_factory=dict)


class RatioConstraintAssessment(BaseModel):
    ratios: list[FinancialRatioResult] = Field(default_factory=list)
    constraints: list[ConstraintCheckResult] = Field(default_factory=list)
    hard_constraints: list[ConstraintCheckResult] = Field(default_factory=list)
    warnings: list[ConstraintCheckResult] = Field(default_factory=list)
    suggested_overrides: dict[str, dict[str, Any]] = Field(default_factory=dict)
