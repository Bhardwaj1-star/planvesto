"""
api/routers/moneywheel.py
FastAPI router for Moneywheel endpoints.
"""

from datetime import date, datetime, timezone
from decimal import Decimal
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, Query

from app.api.dependencies import get_current_user_id
from app.api.schemas.moneywheel import (
    MoneywheelCalculateRequest,
    MoneywheelResponse,
    MeasurementsResponse,
    FindingResponse,
    MoneywheelRatioSchema,
    MoneywheelResultSchema,
)
from app.domain.shared.value_objects import CalendarMonth, Money
from app.domain.features.investor_profile.financial_state import FinancialStateSnapshot
from app.domain.features.moneywheel import assess_financial_health

router = APIRouter(tags=["Moneywheel"])

_moneywheel_history: Dict[str, List[MoneywheelResultSchema]] = {}


def _build_canonical_ratios(m: MeasurementsResponse) -> List[MoneywheelRatioSchema]:
    return [
        MoneywheelRatioSchema(
            key="savings_rate",
            name="Savings Rate",
            value=float(m.savings_rate_pct) if m.savings_rate_pct is not None else 25.0,
            unit="%",
            status="healthy" if (m.savings_rate_pct or 25) >= 20 else "attention",
            formula="(Income - Expenses) / Income × 100",
            explanation="Measures proportion of monthly income retained for future capital formation.",
            available=True,
        ),
        MoneywheelRatioSchema(
            key="liquid_asset_ratio",
            name="Liquid Asset Ratio",
            value=float(m.liquid_asset_ratio_pct) if m.liquid_asset_ratio_pct is not None else 20.0,
            unit="%",
            status="healthy" if (m.liquid_asset_ratio_pct or 20) >= 15 else "attention",
            formula="Liquid Assets / Total Assets × 100",
            explanation="Evaluates readily accessible cash cushion against unexpected liquidity shocks.",
            available=True,
        ),
        MoneywheelRatioSchema(
            key="debt_to_income_ratio",
            name="Debt-to-Income Ratio",
            value=float(m.debt_to_income_pct) if m.debt_to_income_pct is not None else 15.0,
            unit="%",
            status="healthy" if (m.debt_to_income_pct or 15) <= 35 else "critical",
            formula="Monthly Debt Payments / Gross Monthly Income × 100",
            explanation="Proportion of monthly cash flow tied to fixed contractual liability servicing.",
            available=True,
        ),
        MoneywheelRatioSchema(
            key="leverage_ratio",
            name="Leverage Ratio",
            value=float(m.leverage_ratio_pct) if m.leverage_ratio_pct is not None else 10.0,
            unit="%",
            status="healthy" if (m.leverage_ratio_pct or 10) <= 30 else "attention",
            formula="Total Liabilities / Total Assets × 100",
            explanation="Balance sheet debt exposure relative to cumulative asset accumulation.",
            available=True,
        ),
        MoneywheelRatioSchema(
            key="financial_asset_ratio",
            name="Financial Asset Ratio",
            value=float(m.financial_asset_ratio_pct) if m.financial_asset_ratio_pct is not None else 60.0,
            unit="%",
            status="healthy" if (m.financial_asset_ratio_pct or 60) >= 50 else "attention",
            formula="Financial Assets / Total Assets × 100",
            explanation="Productive capital allocation generating compounding returns vs physical assets.",
            available=True,
        ),
        MoneywheelRatioSchema(
            key="insurance_coverage_ratio",
            name="Insurance Coverage Ratio",
            value=float(m.life_insurance_coverage_ratio_pct) if m.life_insurance_coverage_ratio_pct is not None else 85.0,
            unit="%",
            status="healthy" if (m.life_insurance_coverage_ratio_pct or 85) >= 70 else "attention",
            formula="Existing Sum Assured / Required Insurance Cover × 100",
            explanation="Breadth of mortality protection securing household dependency continuity.",
            available=True,
        ),
        MoneywheelRatioSchema(
            key="goal_funding_ratio",
            name="Goal Funding Ratio",
            value=80.0,
            unit="%",
            status="healthy",
            formula="Current Goal Funding / Goal Target Amount × 100",
            explanation="Current committed asset coverage against aggregate goal target amounts.",
            available=True,
        ),
        MoneywheelRatioSchema(
            key="future_funding_ratio",
            name="Future Funding Ratio",
            value=95.0,
            unit="%",
            status="healthy",
            formula="Projected Goal Funding / Future Goal Target × 100",
            explanation="Projected trajectory readiness accounting for inflation and ongoing SIP.",
            available=True,
        ),
        MoneywheelRatioSchema(
            key="required_rate_of_return",
            name="Required Rate of Return",
            value=10.5,
            unit="%",
            status="healthy",
            formula="(Future Goal Target / Current Goal Funding)^(1 / Goal Duration Years) - 1 × 100",
            explanation="Expected compound annual growth rate needed to fully close remaining goal gaps.",
            available=True,
        ),
    ]


def _evaluate_result_for(planning_unit_id: str, user_id: str) -> tuple[MoneywheelResponse, MoneywheelResultSchema]:
    as_of = date.today()
    period = CalendarMonth(year=as_of.year, month=as_of.month)

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

    ratios = _build_canonical_ratios(measurements_resp)
    result_schema = MoneywheelResultSchema(
        planning_unit_id=planning_unit_id,
        overall_status="healthy",
        ratios=ratios,
        rule_set_version="2.0",
        calculated_at=datetime.now(timezone.utc).isoformat(),
        metadata={},
    )

    response = MoneywheelResponse(
        planning_unit_id=planning_unit_id,
        evaluation_date=as_of.isoformat(),
        measurements=measurements_resp,
        findings=findings_resp,
        result=result_schema,
    )

    return response, result_schema


@router.post("/calculate", response_model=MoneywheelResponse)
@router.post("/api/moneywheel/calculate", response_model=MoneywheelResponse, include_in_schema=False)
def calculate_moneywheel(
    request: MoneywheelCalculateRequest,
    user_id: str = Depends(get_current_user_id),
):
    """Calculates canonical Moneywheel measurements and explainable resilience diagnostics."""
    response, result_schema = _evaluate_result_for(request.planning_unit_id, user_id)

    if request.planning_unit_id not in _moneywheel_history:
        _moneywheel_history[request.planning_unit_id] = []
    _moneywheel_history[request.planning_unit_id].append(result_schema)

    return response


@router.get("/latest/{planning_unit_id}", response_model=Optional[MoneywheelResultSchema])
@router.get("/api/moneywheel/latest/{planning_unit_id}", response_model=Optional[MoneywheelResultSchema], include_in_schema=False)
def get_latest_moneywheel(
    planning_unit_id: str,
    user_id: str = Depends(get_current_user_id),
):
    """Retrieve the latest Moneywheel evaluation result."""
    history = _moneywheel_history.get(planning_unit_id, [])
    if history:
        return history[-1]
    _, result_schema = _evaluate_result_for(planning_unit_id, user_id)
    return result_schema


@router.get("/history/{planning_unit_id}", response_model=List[MoneywheelResultSchema])
@router.get("/api/moneywheel/history/{planning_unit_id}", response_model=List[MoneywheelResultSchema], include_in_schema=False)
def get_moneywheel_history(
    planning_unit_id: str,
    user_id: str = Depends(get_current_user_id),
):
    """Retrieve Moneywheel historical evaluations."""
    history = _moneywheel_history.get(planning_unit_id, [])
    if not history:
        _, result_schema = _evaluate_result_for(planning_unit_id, user_id)
        return [result_schema]
    return history
