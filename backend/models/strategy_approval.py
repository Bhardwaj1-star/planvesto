from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


SuitabilityStatus = Literal["Suitable", "Needs Attention", "Unsuitable"]


class SuitabilityAssessment(BaseModel):
    model_config = ConfigDict(extra="forbid")
    status: SuitabilityStatus
    diagnostics: list[dict[str, Any]] = Field(default_factory=list, max_length=100)
    rule_set_version: str = Field(default="framework-1.0", min_length=1, max_length=100)
    evaluated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat(), max_length=100)


class StrategyApprovalSnapshot(BaseModel):
    """Immutable final approval record for a strategy version."""
    model_config = ConfigDict(extra="forbid")
    approval_snapshot_id: str | None = None
    planning_unit_id: str = Field(min_length=1, max_length=100)
    strategy_id: str = Field(min_length=1, max_length=100)
    strategy_version_id: str = Field(min_length=1, max_length=100)
    strategy_version: int = Field(ge=1)
    goal_id: str = Field(min_length=1, max_length=100)
    defined_goal_id: str = Field(min_length=1, max_length=100)
    defined_goal_version: int = Field(ge=1)
    strategy_snapshot: dict[str, Any] = Field(max_length=100)
    suitability: SuitabilityAssessment
    acknowledgement_type: Literal["none", "needs_attention", "unsuitable"] = "none"
    acknowledgement_text: str | None = Field(default=None, max_length=2000)
    acknowledged_at: str | None = Field(default=None, max_length=100)
    approved_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat(), max_length=100)
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
