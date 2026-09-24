from typing import Any
from pydantic import BaseModel, Field


class ProfileConstraint(BaseModel):
    key: str
    value: Any
    unit: str | None = None
    kind: str
    source: str
    evidence: list[Any] = Field(default_factory=list)
    confidence: float
    priority_rank: int | None = None
    valid_from: str | None = None
    valid_until: str | None = None


class ProfileConflict(BaseModel):
    key: str
    status: str
    reason: str
    sources: list[str] = Field(default_factory=list)
    hard_constraint_present: bool = False


class InvestorProfile(BaseModel):
    profile_run_id: str | None = None
    planning_unit_id: str
    investor_id: str
    version: int
    profile_version: str
    engine_version: str
    financial_snapshot_id: str | None = None
    constraints: list[ProfileConstraint] = Field(default_factory=list)
    priorities: list[dict[str, int]] = Field(default_factory=list)
    conflicts: list[ProfileConflict] = Field(default_factory=list)
    input_snapshot: dict[str, Any] = Field(default_factory=dict)
    created_at: str | None = None
