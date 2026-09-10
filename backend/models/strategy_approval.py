from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator


SuitabilityStatus = Literal["Suitable", "Needs Attention", "Unsuitable"]


class SuitabilityAssessment(BaseModel):
    status: SuitabilityStatus
    diagnostics: list[dict[str, Any]] = Field(default_factory=list)
    rule_set_version: str = "framework-1.0"
    evaluated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class StrategyApprovalSnapshot(BaseModel):
    """Immutable final approval record for a strategy version."""

    approval_snapshot_id: str | None = None
    planning_unit_id: str
    strategy_id: str
    strategy_version_id: str
    strategy_version: int
    goal_id: str
    defined_goal_id: str
    defined_goal_version: int
    strategy_snapshot: dict[str, Any]
    suitability: SuitabilityAssessment
    acknowledgement_type: Literal["none", "needs_attention", "unsuitable"] = "none"
    acknowledgement_text: str | None = None
    acknowledged_at: str | None = None
    approved_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    is_primary: bool = False

    @model_validator(mode="after")
    def validate_acknowledgement(self) -> "StrategyApprovalSnapshot":
        if self.suitability.status == "Needs Attention" and self.acknowledgement_type != "needs_attention":
            raise ValueError("Needs Attention requires explicit acknowledgement")
        if self.suitability.status == "Unsuitable" and self.acknowledgement_type != "unsuitable":
            raise ValueError("Unsuitable requires explicit acknowledgement")
        if self.acknowledgement_type != "none" and not self.acknowledged_at:
            raise ValueError("Acknowledged approvals require acknowledged_at")
        return self
