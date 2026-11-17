"""
api/schemas/moneywheel.py
Transport schemas for Moneywheel endpoints.
"""

from decimal import Decimal
from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, Field


class MoneywheelCalculateRequest(BaseModel):
    planning_unit_id: str
    financial_state_snapshot: Optional[Dict[str, Any]] = Field(default_factory=dict)
    target_year: Optional[int] = None
    target_month: Optional[int] = None


class FindingResponse(BaseModel):
    dimension: str
    finding: str
    evidence: str
    impact: str
    uncertainty: str
    investor_consideration: str


class MeasurementsResponse(BaseModel):
    net_worth: Decimal
    net_monthly_income: Decimal
    monthly_expenses: Decimal
    available_monthly_surplus: Decimal
    savings_rate_pct: Optional[Decimal] = None
    debt_to_income_pct: Optional[Decimal] = None
    leverage_ratio_pct: Optional[Decimal] = None
    liquid_asset_ratio_pct: Optional[Decimal] = None
    financial_asset_ratio_pct: Optional[Decimal] = None
    concentration_pct: Optional[Decimal] = None
    weighted_debt_rate_pct: Optional[Decimal] = None
    required_life_cover: Decimal
    existing_life_sum_assured: Decimal
    life_insurance_coverage_ratio_pct: Optional[Decimal] = None
    has_active_health_insurance: bool


class MoneywheelRatioSchema(BaseModel):
    key: str
    name: str
    value: Optional[float] = None
    unit: str = "%"
    status: Literal["excellent", "healthy", "attention", "critical", "unavailable"] = "healthy"
    formula: str = ""
    explanation: str = ""
    available: bool = True


class MoneywheelResultSchema(BaseModel):
    planning_unit_id: str
    overall_status: Optional[str] = "healthy"
    ratios: List[MoneywheelRatioSchema] = Field(default_factory=list)
    rule_set_version: str = "2.0"
    calculated_at: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class MoneywheelResponse(BaseModel):
    planning_unit_id: str
    evaluation_date: Optional[str] = None
    measurements: Optional[MeasurementsResponse] = None
    findings: Optional[List[FindingResponse]] = None
    result: Optional[MoneywheelResultSchema] = None
