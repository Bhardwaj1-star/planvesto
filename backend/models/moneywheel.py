from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator


MoneywheelStatus = Literal["excellent", "healthy", "attention", "critical", "unavailable"]


class MoneywheelRatio(BaseModel):
    key: str
    name: str
    value: float | None = None
    unit: str
    status: MoneywheelStatus
    formula: str
    explanation: str
    available: bool = True


class MoneywheelInput(BaseModel):
    planning_unit_id: str
    gross_monthly_income: float | None = None
    savings: float | None = None
    essential_monthly_expenses: float | None = None
    monthly_expenses: float | None = None
    liquid_assets: float | None = None
    short_term_liabilities: float | None = None
    monthly_debt_payments: float | None = None
    total_assets: float | None = None
    total_liabilities: float | None = None
    financial_assets: float | None = None

    @model_validator(mode="after")
    def validate_non_negative(self) -> "MoneywheelInput":
        for field in (
            "gross_monthly_income", "savings", "essential_monthly_expenses",
            "monthly_expenses", "liquid_assets", "short_term_liabilities",
            "monthly_debt_payments", "total_assets", "total_liabilities",
            "financial_assets",
        ):
            value = getattr(self, field)
            if value is not None and value < 0:
                raise ValueError(f"{field} cannot be negative")
        return self


class MoneywheelResult(BaseModel):
    planning_unit_id: str
    status: Literal["excellent", "healthy", "attention", "critical", "incomplete"]
    ratios: list[MoneywheelRatio] = Field(min_length=9, max_length=9)
    rule_set_version: str
    calculated_at: str
    metadata: dict[str, Any] = Field(default_factory=dict)
