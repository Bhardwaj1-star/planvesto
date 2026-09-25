from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


MoneywheelStatus = Literal["excellent", "healthy", "attention", "critical", "unavailable"]


class MoneywheelRatio(BaseModel):
    model_config = ConfigDict(extra="forbid")
    key: str
    name: str
    value: float | None = None
    unit: str
    status: MoneywheelStatus
    formula: str
    explanation: str
    available: bool = True


class MoneywheelInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    planning_unit_id: str = Field(min_length=1, max_length=100)
    gross_monthly_income: float | None = Field(default=None, ge=0, allow_inf_nan=False)
    savings: float | None = Field(default=None, ge=0, allow_inf_nan=False)
    essential_monthly_expenses: float | None = Field(default=None, ge=0, allow_inf_nan=False)
    monthly_expenses: float | None = Field(default=None, ge=0, allow_inf_nan=False)
    liquid_assets: float | None = Field(default=None, ge=0, allow_inf_nan=False)
    short_term_liabilities: float | None = Field(default=None, ge=0, allow_inf_nan=False)
    monthly_debt_payments: float | None = Field(default=None, ge=0, allow_inf_nan=False)
    total_assets: float | None = Field(default=None, ge=0, allow_inf_nan=False)
    total_liabilities: float | None = Field(default=None, ge=0, allow_inf_nan=False)
    financial_assets: float | None = Field(default=None, ge=0, allow_inf_nan=False)
    existing_sum_assured: float | None = Field(default=None, ge=0, allow_inf_nan=False)
    required_insurance_cover: float | None = Field(default=None, ge=0, allow_inf_nan=False)
    current_goal_funding: float | None = Field(default=None, ge=0, allow_inf_nan=False)
    goal_target_amount: float | None = Field(default=None, ge=0, allow_inf_nan=False)
    projected_goal_funding: float | None = Field(default=None, ge=0, allow_inf_nan=False)
    future_goal_target: float | None = Field(default=None, ge=0, allow_inf_nan=False)

    @model_validator(mode="after")
    def validate_non_negative(self) -> "MoneywheelInput":
        return self


class MoneywheelResult(BaseModel):
    model_config = ConfigDict(extra="forbid")
    planning_unit_id: str
    overall_status: Literal["excellent", "healthy", "attention", "critical", "incomplete"] | None = None
    ratios: list[MoneywheelRatio] = Field(min_length=12, max_length=12)
    rule_set_version: str
    calculated_at: str
    metadata: dict[str, Any] = Field(default_factory=dict, max_length=50)
