from typing import Any
from pydantic import Field, field_validator
from schemas.base import StrictRequestModel


class ProfileBuildRequest(StrictRequestModel):
    planning_unit_id: str = Field(min_length=1, max_length=100)
    investor_id: str = Field(min_length=1, max_length=100)
    financial_snapshot_id: str | None = Field(default=None, min_length=1, max_length=100)
    declared_constraints: list[dict[str, Any]] = Field(default_factory=list, max_length=100)
    observed_behavior: list[dict[str, Any]] = Field(default_factory=list, max_length=100)
    preferences: list[dict[str, Any]] = Field(default_factory=list, max_length=100)
    profile_version: str = Field(default="v2", min_length=1, max_length=50)

    @field_validator("declared_constraints", "observed_behavior", "preferences")
    @classmethod
    def validate_items(cls, value: list[dict[str, Any]]) -> list[dict[str, Any]]:
        for item in value:
            key = item.get("key")
            if not isinstance(key, str) or not 1 <= len(key) <= 100:
                raise ValueError("Constraint keys must be 1-100 characters")
            if "value" not in item:
                raise ValueError("Every profile constraint item requires a value")
        return value


class ProfileResponse(StrictRequestModel):
    profile: dict[str, Any]


class ProfileHistoryQuery(StrictRequestModel):
    planning_unit_id: str = Field(min_length=1, max_length=100)
    investor_id: str = Field(min_length=1, max_length=100)
    limit: int = Field(default=20, ge=1, le=100)
