from typing import Any
from pydantic import Field, field_validator
from schemas.base import StrictRequestModel


class ProfileBuildRequest(StrictRequestModel):
    planning_unit_id: str = Field(min_length=1, max_length=100)
    investor_id: str = Field(min_length=1, max_length=100)
    financial_snapshot_id: str | None = Field(default=None, min_length=1, max_length=100)
    risk_tolerance_answers: dict[str, float] = Field(default_factory=dict, max_length=30)
    behavioral_answers: dict[str, float] = Field(default_factory=dict, max_length=30)
    identity_answers: dict[str, float] = Field(default_factory=dict, max_length=30)
    questionnaire_version: str = Field(default="v1", min_length=1, max_length=50)

    @field_validator("risk_tolerance_answers", "behavioral_answers", "identity_answers")
    @classmethod
    def validate_answer_ranges(cls, value: dict[str, float]) -> dict[str, float]:
        for key, answer in value.items():
            if not key or len(key) > 100:
                raise ValueError("Profile answer keys must be 1-100 characters")
            if answer < 0 or answer > 4:
                raise ValueError("Profile answers must be between 0 and 4")
        return value


class ProfileResponse(StrictRequestModel):
    profile: dict[str, Any]


class ProfileHistoryQuery(StrictRequestModel):
    planning_unit_id: str = Field(min_length=1, max_length=100)
    investor_id: str = Field(min_length=1, max_length=100)
    limit: int = Field(default=20, ge=1, le=100)
