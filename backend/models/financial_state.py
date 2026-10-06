from typing import Any
from pydantic import BaseModel, ConfigDict, Field


class Metric(BaseModel):
    model_config = ConfigDict(extra="forbid")

    value: float | None = None
    available: bool = True
    reason: str | None = None


class FinancialState(BaseModel):
    model_config = ConfigDict(extra="forbid")

    scope: str
    planning_unit_id: str
    investor_id: str | None = None
    income_monthly: Metric
    income_annual: Metric
    income_breakdown: list[dict[str, Any]] = Field(default_factory=list)
    expenses_monthly: Metric
    expenses_annual: Metric
    essential_monthly_expenses: Metric = Field(default_factory=Metric)
    expense_breakdown: list[dict[str, Any]] = Field(default_factory=list)
    investable_surplus_monthly: Metric
    investable_surplus_annual: Metric
    total_assets: Metric
    liquid_assets: Metric = Field(default_factory=Metric)
    financial_assets: Metric = Field(default_factory=Metric)
    asset_breakdown: list[dict[str, Any]] = Field(default_factory=list)
    asset_allocation: list[dict[str, Any]] = Field(default_factory=list)
    liquidity_breakdown: list[dict[str, Any]] = Field(default_factory=list)
    total_liabilities: Metric
    liability_breakdown: list[dict[str, Any]] = Field(default_factory=list)
    liability_allocation: list[dict[str, Any]] = Field(default_factory=list)
    emi_burden_monthly: Metric
    total_insurance_sum_assured: Metric = Field(default_factory=Metric)
    total_insurance_annual_premium: Metric = Field(default_factory=Metric)
    total_insurance_monthly_premium: Metric = Field(default_factory=Metric)
    total_insurance_current_value: Metric = Field(default_factory=Metric)
    insurance_breakdown: list[dict[str, Any]] = Field(default_factory=list)

