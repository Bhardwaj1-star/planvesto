from typing import Any, Literal
from pydantic import BaseModel, ConfigDict, Field

from schemas.base import StrictRequestModel

InsuranceSource = Literal["manual", "pdf"]


class InsurancePolicyCreateRequest(StrictRequestModel):
    planning_unit_id: str = Field(min_length=1)
    policy_name: str = Field(min_length=1)
    insurer: str | None = None
    policy_number: str | None = None
    policy_type: str | None = None
    premium: float | None = Field(default=None, ge=0)
    premium_frequency: str | None = None
    sum_assured: float | None = Field(default=None, ge=0)
    current_value: float | None = Field(default=None, ge=0)
    maturity_date: str | None = None
    maturity_value: float | None = Field(default=None, ge=0)
    source: InsuranceSource = "manual"


class InsurancePolicyUpdateRequest(StrictRequestModel):
    policy_name: str | None = Field(default=None, min_length=1)
    insurer: str | None = None
    policy_number: str | None = None
    policy_type: str | None = None
    premium: float | None = Field(default=None, ge=0)
    premium_frequency: str | None = None
    sum_assured: float | None = Field(default=None, ge=0)
    current_value: float | None = Field(default=None, ge=0)
    maturity_date: str | None = None
    maturity_value: float | None = Field(default=None, ge=0)
    source: InsuranceSource | None = None


class InsurancePolicyResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    policy_id: str
    planning_unit_id: str
    policy_name: str
    insurer: str | None = None
    policy_number: str | None = None
    policy_type: str | None = None
    premium: float | None = None
    premium_frequency: str | None = None
    sum_assured: float | None = None
    current_value: float | None = None
    maturity_date: str | None = None
    maturity_value: float | None = None
    asset_id: str | None = None
    expense_id: str | None = None
    source: str = "manual"
    created_at: str | None = None
    updated_at: str | None = None


class InsuranceProtectionResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    total_sum_assured: float
    life_cover: float
    health_cover: float
    policy_count: int
