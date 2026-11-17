"""
api/schemas/moneywheel.py
Transport schemas for Moneywheel endpoints.
"""

from decimal import Decimal
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class MoneywheelCalculateRequest(BaseModel):
    planning_unit_id: str
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


class MoneywheelResponse(BaseModel):
    planning_unit_id: str
    evaluation_date: str
    measurements: MeasurementsResponse
    findings: List[FindingResponse]
