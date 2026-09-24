from typing import Any
from pydantic import BaseModel, Field


class ProfileDimension(BaseModel):
    key: str
    score: float
    band: str
    confidence: float
    components: dict[str, float] = Field(default_factory=dict)
    explanations: list[str] = Field(default_factory=list)


class InvestorProfile(BaseModel):
    profile_run_id: str | None = None
    planning_unit_id: str
    investor_id: str
    version: int
    engine_version: str
    questionnaire_version: str
    financial_snapshot_id: str | None = None
    risk_capacity: ProfileDimension
    risk_tolerance: ProfileDimension
    behavioral_profile: ProfileDimension
    investor_identity: ProfileDimension
    completeness: float
    input_snapshot: dict[str, Any] = Field(default_factory=dict)
    created_at: str | None = None
