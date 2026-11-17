"""
api/routers/financial_state.py
FastAPI router for Financial State endpoints.
"""

from datetime import date
from decimal import Decimal
import logging
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.dependencies import get_current_user_id
from app.api.schemas.financial_state import (
    FinancialStateRequest,
    FinancialStateResponse,
)
from app.domain.shared.value_objects import CalendarMonth, Money, Rate, FlowFrequency
from app.domain.features.investor_profile.financial_state import assess_data_readiness
from app.domain.canonical.financial_categories import (
    CanonicalIncomeCategoryId, CanonicalExpenseCategoryId,
    CanonicalAssetCategoryId, CanonicalLiabilityCategoryId,
)
from app.domain.features.investor_profile.financial_state.models import (
    FinancialStateSnapshot, IncomeRecord, ExpenseRecord, AssetRecord, LiabilityRecord,
)
from app.infrastructure.persistence.repositories.investor_profile import (
    InvestorProfileRepository,
)

router = APIRouter(tags=["Financial State"])
logger = logging.getLogger(__name__)
_profile_repo = InvestorProfileRepository()

_INCOME_CATEGORIES = {
    "salary": CanonicalIncomeCategoryId.SALARY, "business": CanonicalIncomeCategoryId.BUSINESS,
    "professional/freelance": CanonicalIncomeCategoryId.PROFESSIONAL_FREELANCE,
    "rental": CanonicalIncomeCategoryId.RENTAL, "interest": CanonicalIncomeCategoryId.INTEREST,
    "dividend": CanonicalIncomeCategoryId.DIVIDEND, "pension": CanonicalIncomeCategoryId.PENSION,
    "other": CanonicalIncomeCategoryId.OTHER,
}
_EXPENSE_CATEGORIES = {
    "housing": CanonicalExpenseCategoryId.HOUSING, "food & groceries": CanonicalExpenseCategoryId.FOOD_GROCERIES,
    "utilities": CanonicalExpenseCategoryId.UTILITIES, "transportation": CanonicalExpenseCategoryId.TRANSPORTATION,
    "education": CanonicalExpenseCategoryId.EDUCATION, "healthcare": CanonicalExpenseCategoryId.HEALTHCARE,
    "insurance": CanonicalExpenseCategoryId.INSURANCE, "debt payments": CanonicalExpenseCategoryId.DEBT_PAYMENTS,
    "family support": CanonicalExpenseCategoryId.FAMILY_SUPPORT, "travel": CanonicalExpenseCategoryId.TRAVEL,
    "entertainment": CanonicalExpenseCategoryId.ENTERTAINMENT, "shopping": CanonicalExpenseCategoryId.SHOPPING,
    "other": CanonicalExpenseCategoryId.OTHER,
}
_ASSET_CATEGORIES = {
    "bank / cash": CanonicalAssetCategoryId.BANK_CASH, "fixed deposits": CanonicalAssetCategoryId.FIXED_DEPOSITS,
    "mutual funds": CanonicalAssetCategoryId.MUTUAL_FUNDS, "stocks / equity": CanonicalAssetCategoryId.STOCKS_EQUITY,
    "bonds / debt": CanonicalAssetCategoryId.BONDS_DEBT, "epf / ppf": CanonicalAssetCategoryId.EPF_PPF,
    "nps": CanonicalAssetCategoryId.NPS, "gold": CanonicalAssetCategoryId.GOLD,
    "real estate": CanonicalAssetCategoryId.REAL_ESTATE, "business ownership": CanonicalAssetCategoryId.BUSINESS_OWNERSHIP,
    "vehicle": CanonicalAssetCategoryId.VEHICLE, "other": CanonicalAssetCategoryId.OTHER,
}
_LIABILITY_CATEGORIES = {
    "home loan": CanonicalLiabilityCategoryId.HOME_LOAN, "car loan": CanonicalLiabilityCategoryId.CAR_LOAN,
    "personal loan": CanonicalLiabilityCategoryId.PERSONAL_LOAN, "education loan": CanonicalLiabilityCategoryId.EDUCATION_LOAN,
    "business loan": CanonicalLiabilityCategoryId.BUSINESS_LOAN, "credit card": CanonicalLiabilityCategoryId.CREDIT_CARD,
    "other": CanonicalLiabilityCategoryId.OTHER,
}


def _monthly_amount(value: Any, frequency: Any) -> Decimal:
    amount = Decimal(str(value or 0))
    freq = str(frequency or "monthly").strip().lower().replace("-", "_")
    if freq in ("annual", "annually", "yearly"):
        return amount / Decimal("12")
    if freq in ("quarterly", "quarter"):
        return amount / Decimal("3")
    if freq in ("semi_annual", "semiannual", "half_yearly"):
        return amount / Decimal("6")
    if freq in ("one_off", "oneoff", "once"):
        return Decimal("0")
    return amount


def _metric(value: Decimal, available: bool = True, reason: Optional[str] = None) -> Dict[str, Any]:
    return {"value": float(value), "available": available, "reason": reason}


def _existing_goal_sips(planning_unit_id: str, assets_by_id: Dict[str, Dict[str, Any]]) -> Dict[str, float]:
    """Allocate recurring asset contributions to the goals they are mapped to."""
    client = _profile_repo.client
    if client is None:
        return {}
    mappings: List[Dict[str, Any]] = []
    try:
        latest = client.table("defined_goals").select("defined_goal_id, goal_id, status").eq(
            "planning_unit_id", planning_unit_id
        ).eq("is_latest", True).execute().data or []
        active = [row for row in latest if str(row.get("status", "")).lower() != "cancelled"]
        defined_ids = [row["defined_goal_id"] for row in active if row.get("defined_goal_id")]
        goal_by_defined = {row["defined_goal_id"]: row["goal_id"] for row in active}
        if defined_ids:
            rows = client.table("defined_goal_asset_mappings").select(
                "defined_goal_id, asset_id, allocation_type, allocated_amount, allocated_percentage"
            ).in_("defined_goal_id", defined_ids).execute().data or []
            mappings.extend({**row, "goal_id": goal_by_defined.get(row.get("defined_goal_id"))} for row in rows)
    except Exception as exc:
        logger.warning("Could not read defined-goal asset mappings for SIP allocation: %s", exc)
    try:
        legacy = client.table("goal_funding").select("goal_id, asset_id, allocation_percentage").execute().data or []
        existing_pairs = {(row.get("goal_id"), row.get("asset_id")) for row in mappings}
        mappings.extend(row for row in legacy if (row.get("goal_id"), row.get("asset_id")) not in existing_pairs)
    except Exception as exc:
        logger.warning("Could not read legacy goal-funding mappings for SIP allocation: %s", exc)

    result: Dict[str, Decimal] = {}
    for mapping in mappings:
        goal_id, asset_id = mapping.get("goal_id"), mapping.get("asset_id")
        asset = assets_by_id.get(str(asset_id))
        if not goal_id or not asset:
            continue
        contribution = Decimal(str(asset.get("monthly_contribution", 0) or 0))
        current_value = Decimal(str(asset.get("current_value", 0) or 0))
        allocation_type = str(mapping.get("allocation_type", "percentage")).lower()
        if allocation_type in ("currency", "amount", "fixed_amount") and current_value > 0:
            share = Decimal(str(mapping.get("allocated_amount", 0) or 0)) / current_value
        else:
            share = Decimal(str(mapping.get("allocated_percentage", mapping.get("allocation_percentage", 100)) or 0)) / Decimal("100")
        result[str(goal_id)] = result.get(str(goal_id), Decimal("0")) + contribution * min(Decimal("1"), max(Decimal("0"), share))
    return {key: float(value) for key, value in result.items()}


def _build_financial_state_snapshot(request: FinancialStateRequest, user_id: str, as_of: date, period: CalendarMonth):
    facts = _profile_repo.get_financial_facts(request.planning_unit_id)
    incomes: List[IncomeRecord] = []
    expenses: List[ExpenseRecord] = []
    assets: List[AssetRecord] = []
    liabilities: List[LiabilityRecord] = []
    savings: List[Money] = []
    income_breakdown: List[Dict[str, Any]] = []
    expense_breakdown: List[Dict[str, Any]] = []
    asset_breakdown: List[Dict[str, Any]] = []
    liability_breakdown: List[Dict[str, Any]] = []
    assets_by_id: Dict[str, Dict[str, Any]] = {}

    for row in facts.get("income", []):
        category = _INCOME_CATEGORIES.get(str(row.get("income_type", "other")).strip().lower(), CanonicalIncomeCategoryId.OTHER)
        monthly = _monthly_amount(row.get("amount"), row.get("frequency"))
        if monthly <= 0:
            continue
        incomes.append(IncomeRecord(
            id=str(row.get("income_id", "")), category=category, amount=Money.from_amount(monthly),
            is_net=True, frequency=FlowFrequency.MONTHLY, period=period,
        ))
        income_breakdown.append({"income_id": row.get("income_id"), "name": row.get("income_type"), "monthly_amount": float(monthly)})

    for row in facts.get("expenses", []):
        category = _EXPENSE_CATEGORIES.get(str(row.get("expense_type", "other")).strip().lower(), CanonicalExpenseCategoryId.OTHER)
        monthly = _monthly_amount(row.get("amount"), row.get("frequency"))
        if monthly <= 0:
            continue
        expenses.append(ExpenseRecord(
            id=str(row.get("expense_id", "")), category=category, amount=Money.from_amount(monthly), period=period,
        ))
        expense_breakdown.append({"expense_id": row.get("expense_id"), "name": row.get("expense_type"), "monthly_amount": float(monthly)})

    for row in facts.get("assets", []):
        raw_name = str(row.get("asset_name", "Other"))
        category_name = raw_name.split(" - ", 1)[0].strip().lower()
        category = _ASSET_CATEGORIES.get(category_name, CanonicalAssetCategoryId.OTHER)
        current_value = Decimal(str(row.get("current_value", 0) or 0))
        contribution = _monthly_amount(row.get("monthly_contribution_amount", 0), row.get("monthly_contribution_frequency", "Monthly"))
        assets_by_id[str(row.get("asset_id", ""))] = {
            "asset_id": row.get("asset_id"), "name": raw_name,
            "current_value": current_value, "monthly_contribution": contribution,
        }
        if contribution > 0:
            savings.append(Money.from_amount(contribution))
        assets.append(AssetRecord(
            id=str(row.get("asset_id", "")), category=category, name=raw_name,
            value=Money.from_amount(current_value), as_of_date=as_of,
            is_accessible=category in {
                CanonicalAssetCategoryId.BANK_CASH, CanonicalAssetCategoryId.MUTUAL_FUNDS,
                CanonicalAssetCategoryId.STOCKS_EQUITY, CanonicalAssetCategoryId.GOLD,
            },
        ))
        asset_breakdown.append({
            "asset_id": row.get("asset_id"), "name": raw_name, "current_value": float(current_value),
            "monthly_contribution": float(contribution), "category": category.value,
        })

    for row in facts.get("liabilities", []):
        raw_name = str(row.get("liability_name", "Other"))
        category = _LIABILITY_CATEGORIES.get(raw_name.split(" - ", 1)[0].strip().lower(), CanonicalLiabilityCategoryId.OTHER)
        monthly_payment = _monthly_amount(row.get("emi_amount"), row.get("frequency") or "Monthly")
        liabilities.append(LiabilityRecord(
            id=str(row.get("liability_id", "")), category=category, name=raw_name,
            outstanding_balance=Money.from_amount(row.get("outstanding_amount", 0) or 0),
            annual_interest_rate=Rate.from_percentage(row.get("interest_rate") or 0),
            monthly_payment=Money.from_amount(monthly_payment), as_of_date=as_of,
        ))
        liability_breakdown.append({
            "liability_id": row.get("liability_id"), "name": raw_name,
            "outstanding_amount": float(row.get("outstanding_amount", 0) or 0), "monthly_emi": float(monthly_payment),
        })

    snapshot = FinancialStateSnapshot(
        investor_id=request.investor_id or user_id, as_of_date=as_of,
        incomes=incomes, expenses=expenses, monthly_savings_investments=savings,
        assets=assets, liabilities=liabilities,
    )
    readiness = assess_data_readiness(snapshot, period)
    net_income = snapshot.get_actual_net_monthly_income(period).amount
    monthly_expenses = snapshot.get_actual_monthly_expenses(period).amount
    monthly_savings = snapshot.get_actual_monthly_savings_investments().amount
    surplus = snapshot.calculate_available_monthly_surplus(period).amount
    income_available, expenses_available = bool(incomes), bool(expenses)
    surplus_available = income_available and expenses_available
    goal_sips = _existing_goal_sips(request.planning_unit_id, assets_by_id)
    state = {
        "scope": request.scope, "planning_unit_id": request.planning_unit_id,
        "investor_id": request.investor_id or user_id, "as_of_date": as_of.isoformat(),
        "income_monthly": _metric(net_income, income_available, None if income_available else "MISSING_INPUT"),
        "income_annual": _metric(net_income * Decimal("12"), income_available, None if income_available else "MISSING_INPUT"),
        "income_breakdown": income_breakdown,
        "expenses_monthly": _metric(monthly_expenses, expenses_available, None if expenses_available else "MISSING_INPUT"),
        "expenses_annual": _metric(monthly_expenses * Decimal("12"), expenses_available, None if expenses_available else "MISSING_INPUT"),
        "expense_breakdown": expense_breakdown,
        "monthly_savings_investments": _metric(monthly_savings, True),
        "existing_sips_monthly": _metric(monthly_savings, True),
        "existing_goal_sips_by_goal": goal_sips,
        "investable_surplus_monthly": _metric(surplus, surplus_available, None if surplus_available else "MISSING_INPUT"),
        "investable_surplus_annual": _metric(surplus * Decimal("12"), surplus_available, None if surplus_available else "MISSING_INPUT"),
        "savings_investment_rate": _metric((monthly_savings / net_income * Decimal("100")) if net_income > 0 else Decimal("0"), income_available),
        "cash_flow_ratio": _metric((surplus / net_income * Decimal("100")) if net_income > 0 else Decimal("0"), surplus_available),
        "total_assets": _metric(snapshot.total_assets().amount, bool(assets)),
        "asset_breakdown": asset_breakdown,
        "total_liabilities": _metric(snapshot.total_liabilities().amount, bool(liabilities)),
        "liability_breakdown": liability_breakdown,
        "emi_burden_monthly": _metric(sum((item.monthly_payment.amount for item in liabilities), Decimal("0")), bool(liabilities)),
        "net_worth": _metric(snapshot.net_worth().amount, bool(assets) or bool(liabilities)),
        "safety_reserve_months": _metric(Decimal("0"), False, "NOT_CALCULATED"),
        "safety_reserve_required_amount": _metric(Decimal("0"), False, "NOT_CALCULATED"),
        "data_readiness": {
            "is_ready_for_goal_feasibility": readiness.is_ready_for_goal_feasibility and surplus_available,
            "missing_inputs": readiness.missing_inputs_for_goal_planning if surplus_available else (
                readiness.missing_inputs_for_goal_planning or ["Complete income and expense inputs."]
            ),
        },
    }
    return snapshot, state, readiness, surplus, goal_sips


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

    snapshot, state, readiness, surplus, goal_sips = _build_financial_state_snapshot(
        request, user_id, as_of, period
    )
    snapshot_id = _profile_repo.save_financial_state_snapshot(
        planning_unit_id=request.planning_unit_id,
        scope=request.scope,
        investor_id=request.investor_id if request.scope == "individual" else None,
        snapshot=state,
    )
    state["snapshot_id"] = snapshot_id

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
        available_monthly_surplus=surplus if readiness.is_ready_for_goal_feasibility else Decimal("0"),
        data_readiness={
            "is_ready_for_goal_feasibility": readiness.is_ready_for_goal_feasibility and state["investable_surplus_monthly"]["available"],
            "missing_inputs": state["data_readiness"]["missing_inputs"],
            "monthly_savings_investments": state["monthly_savings_investments"]["value"],
            "existing_goal_sips_by_goal": goal_sips,
        },
    )


@router.get("/latest/{planning_unit_id}")
@router.get("/api/financial-state/latest/{planning_unit_id}", include_in_schema=False)
def get_latest_financial_state(
    planning_unit_id: str,
    user_id: str = Depends(get_current_user_id),
    scope: str = Query(default="family"),
):
    """Retrieve the latest financial state for a planning unit."""
    saved = _profile_repo.get_latest_financial_state_snapshot(planning_unit_id, scope=scope)
    if saved and "financial_state" in saved:
        return saved["financial_state"]

    metric_zero = {"value": 0.0, "available": False, "reason": "MISSING_INPUT"}
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
