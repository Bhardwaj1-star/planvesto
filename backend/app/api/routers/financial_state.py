"""
api/routers/financial_state.py
FastAPI router for Financial State endpoints.
"""

from datetime import date
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.dependencies import get_current_user_id
from app.api.schemas.financial_state import (
    FinancialStateRequest,
    FinancialStateResponse,
)
from app.domain.shared.value_objects import CalendarMonth, Money
from app.domain.features.investor_profile.financial_state import (
    FinancialStateSnapshot,
    assess_data_readiness,
)
from app.infrastructure.persistence.repositories.investor_profile import (
    InvestorProfileRepository,
)

router = APIRouter(tags=["Financial State"])
_profile_repo = InvestorProfileRepository()


@router.post("/build", response_model=FinancialStateResponse)
@router.post("/api/financial-state/build", response_model=FinancialStateResponse, include_in_schema=False)
def build_financial_state(
    request: FinancialStateRequest,
    user_id: str = Depends(get_current_user_id),
):
    """Builds and normalizes Financial State snapshot for the planning unit."""
    as_of = date.today()
    target_month = request.target_month or as_of.month
    target_year = request.target_year or as_of.year
    period = CalendarMonth(year=target_year, month=target_month)

    # Empty/placeholder snapshot if database not connected yet
    snapshot = FinancialStateSnapshot(
        investor_id=request.investor_id or user_id,
        as_of_date=as_of,
        incomes=[],
        expenses=[],
        assets=[],
        liabilities=[],
        insurances=[],
    )

    readiness = assess_data_readiness(snapshot, period)

    return FinancialStateResponse(
        planning_unit_id=request.planning_unit_id,
        scope=request.scope,
        investor_id=request.investor_id,
        as_of_date=as_of.isoformat(),
        net_worth=snapshot.net_worth().amount,
        total_assets=snapshot.total_assets().amount,
        total_liabilities=snapshot.total_liabilities().amount,
        net_monthly_income=snapshot.get_actual_net_monthly_income(period).amount,
        monthly_expenses=snapshot.get_actual_monthly_expenses(period).amount,
        available_monthly_surplus=snapshot.calculate_available_monthly_surplus(period).amount,
        data_readiness={
            "is_ready_for_goal_feasibility": readiness.is_ready_for_goal_feasibility,
            "missing_inputs": readiness.missing_inputs_for_goal_planning,
        },
    )


@router.get("/latest/{planning_unit_id}")
@router.get("/api/financial-state/latest/{planning_unit_id}", include_in_schema=False)
def get_latest_financial_state(
    planning_unit_id: str,
    user_id: str = Depends(get_current_user_id),
):
    """Retrieve the latest financial state for a planning unit."""
    saved = _profile_repo.get_latest_financial_state_snapshot(planning_unit_id)
    if saved and "financial_state" in saved:
        return saved["financial_state"]

    metric_zero = {"value": 0.0, "available": True, "reason": None}
    return {
        "scope": "household",
        "planning_unit_id": planning_unit_id,
        "investor_id": user_id,
        "income_monthly": metric_zero,
        "income_annual": metric_zero,
        "income_breakdown": [],
        "expenses_monthly": metric_zero,
        "expenses_annual": metric_zero,
        "expense_breakdown": [],
        "investable_surplus_monthly": metric_zero,
        "investable_surplus_annual": metric_zero,
        "cash_flow_ratio": metric_zero,
        "savings_investment_rate": metric_zero,
        "total_assets": metric_zero,
        "asset_breakdown": [],
        "total_liabilities": metric_zero,
        "liability_breakdown": [],
        "emi_burden_monthly": metric_zero,
        "net_worth": metric_zero,
        "safety_reserve_months": metric_zero,
        "safety_reserve_required_amount": metric_zero,
    }


@router.get("/history/{planning_unit_id}")
@router.get("/api/financial-state/history/{planning_unit_id}", include_in_schema=False)
def get_financial_state_history(
    planning_unit_id: str,
    user_id: str = Depends(get_current_user_id),
):
    """Retrieve historical financial state snapshots."""
    latest = get_latest_financial_state(planning_unit_id, user_id)
    return [latest]
