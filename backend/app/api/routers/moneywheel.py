"""
api/routers/moneywheel.py
FastAPI router for Moneywheel endpoints.
"""

from datetime import date
from decimal import Decimal
from typing import List
from fastapi import APIRouter, Depends

from app.api.dependencies import get_current_user_id
from app.api.schemas.moneywheel import (
    MoneywheelCalculateRequest,
    MoneywheelResponse,
    MeasurementsResponse,
    FindingResponse,
)
from app.domain.shared.value_objects import CalendarMonth, Money
from app.domain.features.investor_profile.financial_state import FinancialStateSnapshot
from app.domain.features.moneywheel import (
    assess_financial_health,
)

router = APIRouter(tags=["Moneywheel"])


@router.post("/calculate", response_model=MoneywheelResponse)
@router.post("/api/moneywheel/calculate", response_model=MoneywheelResponse, include_in_schema=False)
def calculate_moneywheel(
    request: MoneywheelCalculateRequest,
    user_id: str = Depends(get_current_user_id),
):
    """Calculates canonical Moneywheel measurements and explainable resilience diagnostics."""
    as_of = date.today()
    target_month = request.target_month or as_of.month
    target_year = request.target_year or as_of.year
    period = CalendarMonth(year=target_year, month=target_month)

    snapshot = FinancialStateSnapshot(
        investor_id=user_id,
        as_of_date=as_of,
        incomes=[],
        expenses=[],
        assets=[],
        liabilities=[],
        insurances=[],
    )

    assessment = assess_financial_health(snapshot, period)
    m = assessment.measurements

    findings_resp: List[FindingResponse] = [
        FindingResponse(
            dimension=f.dimension.value,
            finding=f.finding,
            evidence=f.evidence,
            impact=f.impact,
            uncertainty=f.uncertainty,
            investor_consideration=f.investor_consideration,
        )
        for f in assessment.findings
    ]

    measurements_resp = MeasurementsResponse(
        net_worth=m.net_worth.amount,
        net_monthly_income=m.net_monthly_income.amount,
        monthly_expenses=m.monthly_expenses.amount,
        available_monthly_surplus=m.available_monthly_surplus.amount,
        savings_rate_pct=m.savings_rate.percentage if m.savings_rate else None,
        debt_to_income_pct=m.debt_to_income_ratio.percentage if m.debt_to_income_ratio else None,
        leverage_ratio_pct=m.leverage_ratio.percentage if m.leverage_ratio else None,
        liquid_asset_ratio_pct=m.liquid_asset_ratio.percentage if m.liquid_asset_ratio else None,
        financial_asset_ratio_pct=m.financial_asset_ratio.percentage if m.financial_asset_ratio else None,
        concentration_pct=m.portfolio_concentration.percentage if m.portfolio_concentration else None,
        weighted_debt_rate_pct=m.weighted_debt_rate.percentage if m.weighted_debt_rate else None,
        required_life_cover=m.required_life_cover.amount,
        existing_life_sum_assured=m.existing_life_sum_assured.amount,
        life_insurance_coverage_ratio_pct=m.life_insurance_coverage_ratio.percentage if m.life_insurance_coverage_ratio else None,
        has_active_health_insurance=m.has_active_health_insurance,
    )

    return MoneywheelResponse(
        planning_unit_id=request.planning_unit_id,
        evaluation_date=as_of.isoformat(),
        measurements=measurements_resp,
        findings=findings_resp,
    )
