"""Risk Profile domain contracts.

Consolidates the three locked dimensions:
1. Risk Required — canonical financial fact (consumed, not locally recalculated).
2. Risk Capacity — objective financial capacity derived from observable financial constraints.
3. Risk Tolerance — behavioral evidence derived from BehavioralRules (observed dimensions, soft, product selection only).

Every constraint retains:
    key + value + unit + kind + source + evidence + confidence + validity
"""
from __future__ import annotations

from typing import Any, Literal
from pydantic import BaseModel, Field

RiskAssessmentStatus = Literal["complete", "partial", "requires_review"]


class RiskDimension(BaseModel):
    """Structured view of a single risk dimension."""
    name: str
    value: float | None = None
    unit: str | None = None
    available: bool = False
    source: str
    evidence: list[dict[str, Any]] = Field(default_factory=list)
    constraints: list[dict[str, Any]] = Field(default_factory=list)
    confidence: float = 1.0
    status: str = "unavailable"

    def __getitem__(self, item: str) -> Any:
        if hasattr(self, item):
            return getattr(self, item)
        raise KeyError(item)

    def get(self, item: str, default: Any = None) -> Any:
        return getattr(self, item, default)

    def __contains__(self, item: str) -> bool:
        return hasattr(self, item)


class RiskProfile(BaseModel):
    """Authoritative combined risk view consumed by investment planning.

    Consolidates:
        Canonical Risk Required + Risk Capacity + Risk Tolerance -> RiskProfile
    """
    risk_required: RiskDimension
    risk_capacity: RiskDimension
    risk_tolerance: RiskDimension
    status: RiskAssessmentStatus = "requires_review"
    constraints: list[dict[str, Any]] = Field(default_factory=list)
    decision_boundary: dict[str, Any] = Field(default_factory=dict)
    dimensions: dict[str, list[dict[str, Any]]] = Field(default_factory=dict)
    has_sufficient_evidence: bool = False
    conflicts: list[dict[str, Any]] = Field(default_factory=list)

    def is_complete(self) -> bool:
        return all(
            d.available
            for d in (self.risk_required, self.risk_capacity, self.risk_tolerance)
        )

    def __getitem__(self, item: str) -> Any:
        if hasattr(self, item):
            val = getattr(self, item)
            if isinstance(val, BaseModel):
                return val.model_dump()
            return val
        raise KeyError(item)

    def get(self, item: str, default: Any = None) -> Any:
        try:
            return self[item]
        except KeyError:
            return default

    def __contains__(self, item: str) -> bool:
        return hasattr(self, item)
