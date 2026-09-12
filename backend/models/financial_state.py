from typing import Any
from pydantic import BaseModel, Field


class Metric(BaseModel):
    value: float | None = None
    available: bool = True
    reason: str | None = None


class FinancialState(BaseModel):
    scope: str
    planning_unit_id: str
    investor_id: str | None = None
    income_monthly: Metric
    income_annual: Metric
    income_breakdown: list[dict[str, Any]] = Field(default_factory=list)
    expenses_monthly: Metric
    expenses_annual: Metric
    expense_breakdown: list[dict[str, Any]] = Field(default_factory=list)
    investable_surplus_monthly: Metric
    investable_surplus_annual: Metric
    cash_flow_ratio: Metric
    savings_investment_rate: Metric
    total_assets: Metric
    asset_breakdown: list[dict[str, Any]] = Field(default_factory=list)
    asset_allocation: list[dict[str, Any]] = Field(default_factory=list)
    liquidity_breakdown: list[dict[str, Any]] = Field(default_factory=list)
    total_liabilities: Metric
    liability_breakdown: list[dict[str, Any]] = Field(default_factory=list)
    liability_allocation: list[dict[str, Any]] = Field(default_factory=list)
    emi_burden_monthly: Metric
    net_worth: Metric
    safety_reserve_months: Metric
    safety_reserve_required_amount: Metric
