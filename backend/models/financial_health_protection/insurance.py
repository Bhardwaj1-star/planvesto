from typing import Any, Literal
from pydantic import BaseModel, ConfigDict, Field

InsuranceSource = Literal["manual", "pdf"]


class InsurancePolicy(BaseModel):
    model_config = ConfigDict(extra="forbid")

    policy_id: str
    planning_unit_id: str
    policy_name: str
    insurer: str | None = None
    policy_number: str | None = None
    policy_type: str | None = None
    premium: float | None = Field(default=None, ge=0)
    premium_frequency: str | None = None
    sum_assured: float | None = Field(default=None, ge=0)
    current_value: float | None = Field(default=None, ge=0)
    maturity_date: str | None = None
    maturity_value: float | None = Field(default=None, ge=0)
    asset_id: str | None = None
    expense_id: str | None = None
    source: InsuranceSource = "manual"
    created_at: str | None = None
    updated_at: str | None = None


class InsuranceProtectionSummary(BaseModel):
    model_config = ConfigDict(extra="forbid")

    total_sum_assured: float = 0.0
    life_cover: float = 0.0
    health_cover: float = 0.0
    policy_count: int = 0
    policies: list[InsurancePolicy] = Field(default_factory=list)
