"""Risk Profile domain contracts.

Risk Required is a canonical financial fact and is consumed here; it is not
recalculated by the Risk Profiler.

Risk Capacity is a financial assessment.
Risk Tolerance is a behavioural assessment/input.

No score thresholds or asset-allocation mapping is defined here. Those are
business rules that must be explicitly approved before implementation.
"""
from __future__ import annotations
from typing import Any, Literal
from pydantic import BaseModel, Field

RiskAssessmentStatus = Literal["complete", "partial", "requires_review"]

class RiskDimension(BaseModel):
    name: str
    value: float | None = None
    unit: str | None = None
    available: bool = False
    source: str
    evidence: list[dict[str, Any]] = Field(default_factory=list)

class RiskProfile(BaseModel):
    """Combined risk view consumed by investment planning."""
    risk_required: RiskDimension
    risk_capacity: RiskDimension
    risk_tolerance: RiskDimension
    status: RiskAssessmentStatus = "requires_review"
    constraints: list[dict[str, Any]] = Field(default_factory=list)
    decision_boundary: dict[str, Any] = Field(default_factory=dict)

    def is_complete(self) -> bool:
        return all(d.available for d in (
            self.risk_required, self.risk_capacity, self.risk_tolerance
        ))
