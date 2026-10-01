"""Canonical Financial Calculations and Derived Facts Layer.

This module is the single authoritative owner of shared financial calculations
in the Planvesto backend architecture.

Consumers:
  - MoneyWheel Engine (diagnostics)
  - Risk Profiler (risk capacity, exposure, required risk)
  - Goal Engine (funding gap, target calculation, required monthly contribution)
  - Constraint Evaluator (financial ratio constraints)
  - Strategy Builder (eligibility, baseline trade-offs)

Core Principles:
  - One definition per financial fact
  - One canonical implementation/owner
  - One canonical output format (DerivedFact or pure calculation)
  - Many domain consumers
  - Missing data is NEVER silently defaulted to zero
  - Calculation ownership is centralized; decision authority remains in domain engines
"""

from __future__ import annotations

from dataclasses import dataclass, field
import math
from typing import Any

from engines.calculation.engine import round_money

CANONICAL_CALCULATION_VERSION = "1.0.0"


@dataclass(frozen=True)
class DerivedFact:
    """Canonical representation of a derived financial fact.

    Attributes:
        fact_id: Unique identifier of the financial fact.
        value: Numeric result of the calculation, or None if unavailable.
        unit: Unit of measurement (e.g. "%", "months", "INR", "ratio").
        formula: Canonical mathematical definition used.
        inputs_used: Dictionary of input values and their availability.
        available: True if all required inputs were present and valid.
        data_quality: "authoritative", "estimated", or "unavailable".
        calculation_version: Semantic version of the canonical calculation logic.
        source: Provenance source ("canonical_calculation").
        explanation: Human-readable explanation of the calculated result or failure reason.
    """

    fact_id: str
    value: float | None
    unit: str
    formula: str
    inputs_used: dict[str, Any] = field(default_factory=dict)
    available: bool = True
    data_quality: str = "authoritative"
    calculation_version: str = CANONICAL_CALCULATION_VERSION
    source: str = "canonical_calculation"
    explanation: str = ""


# ==============================================================================
# Pure Canonical Calculations (Shared Math)
# ==============================================================================


def calculate_savings_rate(monthly_surplus: float | None, monthly_income: float | None) -> float | None:
    """Savings Rate = (Monthly Surplus / Monthly Income) * 100.

    Returns None if any input is None, income <= 0, or result is not finite.
    """
    if monthly_surplus is None or monthly_income is None:
        return None
    try:
        surplus = float(monthly_surplus)
        income = float(monthly_income)
    except (TypeError, ValueError):
        return None
    if income <= 0:
        return None
    res = (surplus / income) * 100.0
    return round(res, 4) if math.isfinite(res) else None


def calculate_liquid_asset_ratio(liquid_assets: float | None, total_assets: float | None) -> float | None:
    """Liquid Asset Ratio = (Liquid Assets / Total Assets) * 100.

    Returns None if any input is None, total_assets <= 0, or result is not finite.
    """
    if liquid_assets is None or total_assets is None:
        return None
    try:
        liquid = float(liquid_assets)
        total = float(total_assets)
    except (TypeError, ValueError):
        return None
    if total <= 0:
        return None
    res = (liquid / total) * 100.0
    return round(res, 4) if math.isfinite(res) else None


def calculate_expense_coverage(liquid_assets: float | None, monthly_expenses: float | None) -> float | None:
    """Expense Coverage = Liquid Assets / Monthly Expenses (in months).

    Returns None if any input is None, monthly_expenses <= 0, or result is not finite.
    """
    if liquid_assets is None or monthly_expenses is None:
        return None
    try:
        liquid = float(liquid_assets)
        expenses = float(monthly_expenses)
    except (TypeError, ValueError):
        return None
    if expenses <= 0:
        return None
    res = liquid / expenses
    return round(res, 4) if math.isfinite(res) else None


def calculate_emergency_coverage(liquid_assets: float | None, essential_monthly_expenses: float | None) -> float | None:
    """Emergency Coverage = Liquid Assets / Essential Monthly Expenses (in months).

    Returns None if any input is None, essential_monthly_expenses <= 0, or result is not finite.
    """
    if liquid_assets is None or essential_monthly_expenses is None:
        return None
    try:
        liquid = float(liquid_assets)
        essential = float(essential_monthly_expenses)
    except (TypeError, ValueError):
        return None
    if essential <= 0:
        return None
    res = liquid / essential
    return round(res, 4) if math.isfinite(res) else None


def calculate_debt_to_income_ratio(
    monthly_debt_payments: float | None,
    gross_monthly_income: float | None,
    *,
    as_percentage: bool = True,
) -> float | None:
    """Debt-to-Income (DTI) = Monthly Debt Payments / Gross Monthly Income (* 100 if as_percentage).

    Returns None if any input is None, gross_monthly_income <= 0, or result is not finite.
    """
    if monthly_debt_payments is None or gross_monthly_income is None:
        return None
    try:
        debt = float(monthly_debt_payments)
        income = float(gross_monthly_income)
    except (TypeError, ValueError):
        return None
    if income <= 0:
        return None
    factor = 100.0 if as_percentage else 1.0
    res = (debt / income) * factor
    return round(res, 4) if math.isfinite(res) else None


def calculate_leverage_ratio(total_liabilities: float | None, total_assets: float | None) -> float | None:
    """Leverage Ratio = (Total Liabilities / Total Assets) * 100.

    Returns None if any input is None, total_assets <= 0, or result is not finite.
    """
    if total_liabilities is None or total_assets is None:
        return None
    try:
        liabilities = float(total_liabilities)
        assets = float(total_assets)
    except (TypeError, ValueError):
        return None
    if assets <= 0:
        return None
    res = (liabilities / assets) * 100.0
    return round(res, 4) if math.isfinite(res) else None


def calculate_financial_asset_ratio(financial_assets: float | None, total_assets: float | None) -> float | None:
    """Financial Asset Ratio = (Financial Assets / Total Assets) * 100.

    Returns None if any input is None, total_assets <= 0, or result is not finite.
    """
    if financial_assets is None or total_assets is None:
        return None
    try:
        fin = float(financial_assets)
        assets = float(total_assets)
    except (TypeError, ValueError):
        return None
    if assets <= 0:
        return None
    res = (fin / assets) * 100.0
    return round(res, 4) if math.isfinite(res) else None


def calculate_insurance_coverage_ratio(existing_sum_assured: float | None, required_insurance_cover: float | None) -> float | None:
    """Insurance Coverage Ratio = (Existing Sum Assured / Required Insurance Cover) * 100.

    Returns None if any input is None, required_insurance_cover <= 0, or result is not finite.
    """
    if existing_sum_assured is None or required_insurance_cover is None:
        return None
    try:
        existing = float(existing_sum_assured)
        required = float(required_insurance_cover)
    except (TypeError, ValueError):
        return None
    if required <= 0:
        return None
    res = (existing / required) * 100.0
    return round(res, 4) if math.isfinite(res) else None


def calculate_goal_funding_ratio(current_goal_funding: float | None, goal_target_amount: float | None) -> float | None:
    """Goal Funding Ratio = (Current Goal Funding / Goal Target Amount) * 100.

    Returns None if any input is None, goal_target_amount <= 0, or result is not finite.
    """
    if current_goal_funding is None or goal_target_amount is None:
        return None
    try:
        funding = float(current_goal_funding)
        target = float(goal_target_amount)
    except (TypeError, ValueError):
        return None
    if target <= 0:
        return None
    res = (funding / target) * 100.0
    return round(res, 4) if math.isfinite(res) else None


def calculate_future_funding_ratio(projected_goal_funding: float | None, future_goal_target: float | None) -> float | None:
    """Future Funding Ratio = (Projected Goal Funding / Future Goal Target) * 100.

    Returns None if any input is None, future_goal_target <= 0, or result is not finite.
    """
    if projected_goal_funding is None or future_goal_target is None:
        return None
    try:
        projected = float(projected_goal_funding)
        future = float(future_goal_target)
    except (TypeError, ValueError):
        return None
    if future <= 0:
        return None
    res = (projected / future) * 100.0
    return round(res, 4) if math.isfinite(res) else None


def calculate_required_rate_of_return(
    future_goal_target: float | None,
    current_goal_funding: float | None,
    goal_duration_years: float | None,
) -> float | None:
    """Required Rate of Return (Risk Required) = ((Future Target / Current Funding) ^ (1 / Duration) - 1) * 100.

    Shared canonical implementation consumed by MoneyWheel and Risk Profiler.
    Returns None if any input is None, current_goal_funding <= 0, goal_duration_years <= 0, or not finite.
    """
    if future_goal_target is None or current_goal_funding is None or goal_duration_years is None:
        return None
    try:
        target = float(future_goal_target)
        funding = float(current_goal_funding)
        years = float(goal_duration_years)
    except (TypeError, ValueError):
        return None
    if funding <= 0 or years <= 0 or target <= 0:
        return None
    try:
        res = ((target / funding) ** (1.0 / years) - 1.0) * 100.0
        return round(res, 4) if math.isfinite(res) else None
    except (OverflowError, ZeroDivisionError):
        return None


# Canonical alias: Risk Required is the Required Rate of Return for funding goals
calculate_risk_required = calculate_required_rate_of_return


def calculate_portfolio_concentration(
    largest_asset_value: float | None,
    total_assets: float | None,
    *,
    as_percentage: bool = False,
) -> float | None:
    """Portfolio Concentration = Largest Asset Value / Total Assets.

    Returns None if any input is None, total_assets <= 0, or result is not finite.
    """
    if largest_asset_value is None or total_assets is None:
        return None
    try:
        largest = float(largest_asset_value)
        total = float(total_assets)
    except (TypeError, ValueError):
        return None
    if total <= 0:
        return None
    factor = 100.0 if as_percentage else 1.0
    res = (largest / total) * factor
    return round(res, 6 if not as_percentage else 4) if math.isfinite(res) else None


def calculate_goal_future_target(
    today_cost: float | None,
    inflation_rate: float | None,
    duration_years: float | None,
) -> float | None:
    """Future Target = Today Cost * ((1 + inflation_rate) ^ duration_years).

    Returns None if any input is None or duration_years < 0.
    """
    if today_cost is None or inflation_rate is None or duration_years is None:
        return None
    try:
        cost = float(today_cost)
        inflation = float(inflation_rate)
        years = float(duration_years)
    except (TypeError, ValueError):
        return None
    if cost <= 0:
        return 0.0
    if years < 0:
        return None
    val = cost * ((1.0 + inflation) ** years)
    return round_money(val) if math.isfinite(val) else None


def calculate_goal_funding_gap(
    future_target: float | None,
    projected_mapped_asset_value: float | None,
) -> float | None:
    """Goal Funding Gap = Future Target - Projected Mapped Asset Value.

    Returns None if any input is None.
    """
    if future_target is None or projected_mapped_asset_value is None:
        return None
    try:
        target = float(future_target)
        projected = float(projected_mapped_asset_value)
    except (TypeError, ValueError):
        return None
    return round_money(target - projected)


def calculate_required_monthly_contribution(
    funding_gap: float | None,
    annual_return: float | None,
    duration_years: float | None,
) -> float | None:
    """End-of-month contribution required to fund a target-date gap.

    A non-positive gap requires 0.0 additional contribution.
    If duration <= 0, returns 0.0 (caller must handle immediate shortfall).
    """
    if funding_gap is None or annual_return is None or duration_years is None:
        return None
    try:
        gap = max(0.0, float(funding_gap))
        years = max(0.0, float(duration_years))
        annual = float(annual_return)
    except (TypeError, ValueError):
        return None

    if gap <= 0.0 or years <= 0.0:
        return 0.0
    if annual <= -1.0:
        return None

    months = max(1, round(years * 12))
    monthly_rate = annual / 12.0

    if abs(monthly_rate) < 1e-12:
        return round_money(gap / months)

    denominator = ((1.0 + monthly_rate) ** months) - 1.0
    if denominator <= 0.0:
        return None

    required = gap * monthly_rate / denominator
    return round_money(max(0.0, required))


# ==============================================================================
# Canonical Fact Builders (DerivedFact Contracts)
# ==============================================================================


def fact_savings_rate(monthly_surplus: float | None, monthly_income: float | None) -> DerivedFact:
    val = calculate_savings_rate(monthly_surplus, monthly_income)
    available = val is not None
    return DerivedFact(
        fact_id="savings_rate",
        value=val,
        unit="%",
        formula="(Monthly Surplus / Monthly Income) * 100",
        inputs_used={"monthly_surplus": monthly_surplus, "monthly_income": monthly_income},
        available=available,
        data_quality="authoritative" if available else "unavailable",
        explanation=f"Savings rate is {val:.2f}%." if available else "Monthly surplus or income is missing or non-positive.",
    )


def fact_liquid_asset_ratio(liquid_assets: float | None, total_assets: float | None) -> DerivedFact:
    val = calculate_liquid_asset_ratio(liquid_assets, total_assets)
    available = val is not None
    return DerivedFact(
        fact_id="liquid_asset_ratio",
        value=val,
        unit="%",
        formula="(Liquid Assets / Total Assets) * 100",
        inputs_used={"liquid_assets": liquid_assets, "total_assets": total_assets},
        available=available,
        data_quality="authoritative" if available else "unavailable",
        explanation=f"Liquid asset ratio is {val:.2f}%." if available else "Liquid assets or total assets are missing or non-positive.",
    )


def fact_expense_coverage(liquid_assets: float | None, monthly_expenses: float | None) -> DerivedFact:
    val = calculate_expense_coverage(liquid_assets, monthly_expenses)
    available = val is not None
    return DerivedFact(
        fact_id="expense_coverage",
        value=val,
        unit="months",
        formula="Liquid Assets / Monthly Expenses",
        inputs_used={"liquid_assets": liquid_assets, "monthly_expenses": monthly_expenses},
        available=available,
        data_quality="authoritative" if available else "unavailable",
        explanation=f"Expense coverage is {val:.2f} months." if available else "Liquid assets or monthly expenses are missing or non-positive.",
    )


def fact_emergency_coverage(liquid_assets: float | None, essential_monthly_expenses: float | None) -> DerivedFact:
    val = calculate_emergency_coverage(liquid_assets, essential_monthly_expenses)
    available = val is not None
    return DerivedFact(
        fact_id="emergency_coverage",
        value=val,
        unit="months",
        formula="Liquid Assets / Essential Monthly Expenses",
        inputs_used={"liquid_assets": liquid_assets, "essential_monthly_expenses": essential_monthly_expenses},
        available=available,
        data_quality="authoritative" if available else "unavailable",
        explanation=f"Emergency coverage is {val:.2f} months." if available else "Liquid assets or essential monthly expenses are missing or non-positive.",
    )


def fact_debt_to_income_ratio(
    monthly_debt_payments: float | None,
    gross_monthly_income: float | None,
    *,
    as_percentage: bool = True,
) -> DerivedFact:
    val = calculate_debt_to_income_ratio(monthly_debt_payments, gross_monthly_income, as_percentage=as_percentage)
    available = val is not None
    unit = "%" if as_percentage else "ratio"
    return DerivedFact(
        fact_id="debt_to_income_ratio",
        value=val,
        unit=unit,
        formula="Monthly Debt Payments / Gross Monthly Income" + (" * 100" if as_percentage else ""),
        inputs_used={"monthly_debt_payments": monthly_debt_payments, "gross_monthly_income": gross_monthly_income},
        available=available,
        data_quality="authoritative" if available else "unavailable",
        explanation=f"Debt-to-income is {val:.2f}{unit}." if available else "Debt payments or monthly income are missing or non-positive.",
    )


def fact_leverage_ratio(total_liabilities: float | None, total_assets: float | None) -> DerivedFact:
    val = calculate_leverage_ratio(total_liabilities, total_assets)
    available = val is not None
    return DerivedFact(
        fact_id="leverage_ratio",
        value=val,
        unit="%",
        formula="(Total Liabilities / Total Assets) * 100",
        inputs_used={"total_liabilities": total_liabilities, "total_assets": total_assets},
        available=available,
        data_quality="authoritative" if available else "unavailable",
        explanation=f"Leverage ratio is {val:.2f}%." if available else "Total liabilities or total assets are missing or non-positive.",
    )


def fact_financial_asset_ratio(financial_assets: float | None, total_assets: float | None) -> DerivedFact:
    val = calculate_financial_asset_ratio(financial_assets, total_assets)
    available = val is not None
    return DerivedFact(
        fact_id="financial_asset_ratio",
        value=val,
        unit="%",
        formula="(Financial Assets / Total Assets) * 100",
        inputs_used={"financial_assets": financial_assets, "total_assets": total_assets},
        available=available,
        data_quality="authoritative" if available else "unavailable",
        explanation=f"Financial asset ratio is {val:.2f}%." if available else "Financial assets or total assets are missing or non-positive.",
    )


def fact_insurance_coverage_ratio(existing_sum_assured: float | None, required_insurance_cover: float | None) -> DerivedFact:
    val = calculate_insurance_coverage_ratio(existing_sum_assured, required_insurance_cover)
    available = val is not None
    return DerivedFact(
        fact_id="insurance_coverage_ratio",
        value=val,
        unit="%",
        formula="(Existing Sum Assured / Required Insurance Cover) * 100",
        inputs_used={"existing_sum_assured": existing_sum_assured, "required_insurance_cover": required_insurance_cover},
        available=available,
        data_quality="authoritative" if available else "unavailable",
        explanation=f"Insurance coverage ratio is {val:.2f}%." if available else "Existing cover or required cover is missing or non-positive.",
    )


def fact_goal_funding_ratio(current_goal_funding: float | None, goal_target_amount: float | None) -> DerivedFact:
    val = calculate_goal_funding_ratio(current_goal_funding, goal_target_amount)
    available = val is not None
    return DerivedFact(
        fact_id="goal_funding_ratio",
        value=val,
        unit="%",
        formula="(Current Goal Funding / Goal Target Amount) * 100",
        inputs_used={"current_goal_funding": current_goal_funding, "goal_target_amount": goal_target_amount},
        available=available,
        data_quality="authoritative" if available else "unavailable",
        explanation=f"Goal funding ratio is {val:.2f}%." if available else "Goal funding or target amount is missing or non-positive.",
    )


def fact_future_funding_ratio(projected_goal_funding: float | None, future_goal_target: float | None) -> DerivedFact:
    val = calculate_future_funding_ratio(projected_goal_funding, future_goal_target)
    available = val is not None
    return DerivedFact(
        fact_id="future_funding_ratio",
        value=val,
        unit="%",
        formula="(Projected Goal Funding / Future Goal Target) * 100",
        inputs_used={"projected_goal_funding": projected_goal_funding, "future_goal_target": future_goal_target},
        available=available,
        data_quality="authoritative" if available else "unavailable",
        explanation=f"Future funding ratio is {val:.2f}%." if available else "Projected funding or future target is missing or non-positive.",
    )


def fact_required_rate_of_return(
    future_goal_target: float | None,
    current_goal_funding: float | None,
    goal_duration_years: float | None,
) -> DerivedFact:
    val = calculate_required_rate_of_return(future_goal_target, current_goal_funding, goal_duration_years)
    available = val is not None
    return DerivedFact(
        fact_id="required_rate_of_return",
        value=val,
        unit="%",
        formula="((Future Goal Target / Current Goal Funding) ^ (1 / Goal Duration Years) - 1) * 100",
        inputs_used={
            "future_goal_target": future_goal_target,
            "current_goal_funding": current_goal_funding,
            "goal_duration_years": goal_duration_years,
        },
        available=available,
        data_quality="authoritative" if available else "unavailable",
        explanation=f"Required rate of return is {val:.2f}%." if available else "Target, funding, or duration is missing or non-positive.",
    )


def fact_risk_required(
    future_goal_target: float | None,
    current_goal_funding: float | None,
    goal_duration_years: float | None,
) -> DerivedFact:
    fact = fact_required_rate_of_return(future_goal_target, current_goal_funding, goal_duration_years)
    return DerivedFact(
        fact_id="risk_required",
        value=fact.value,
        unit=fact.unit,
        formula=fact.formula,
        inputs_used=fact.inputs_used,
        available=fact.available,
        data_quality=fact.data_quality,
        explanation=fact.explanation,
    )


def fact_portfolio_concentration(
    largest_asset_value: float | None,
    total_assets: float | None,
    *,
    as_percentage: bool = False,
) -> DerivedFact:
    val = calculate_portfolio_concentration(largest_asset_value, total_assets, as_percentage=as_percentage)
    available = val is not None
    unit = "%" if as_percentage else "ratio"
    return DerivedFact(
        fact_id="portfolio_concentration",
        value=val,
        unit=unit,
        formula="Largest Asset Value / Total Assets" + (" * 100" if as_percentage else ""),
        inputs_used={"largest_asset_value": largest_asset_value, "total_assets": total_assets},
        available=available,
        data_quality="authoritative" if available else "unavailable",
        explanation=f"Portfolio concentration is {val:.4f}{unit}." if available else "Largest asset value or total assets missing or non-positive.",
    )


def fact_goal_funding_gap(future_target: float | None, projected_mapped_asset_value: float | None) -> DerivedFact:
    val = calculate_goal_funding_gap(future_target, projected_mapped_asset_value)
    available = val is not None
    return DerivedFact(
        fact_id="goal_funding_gap",
        value=val,
        unit="INR",
        formula="Future Target - Projected Mapped Asset Value",
        inputs_used={"future_target": future_target, "projected_mapped_asset_value": projected_mapped_asset_value},
        available=available,
        data_quality="authoritative" if available else "unavailable",
        explanation=f"Funding gap is {val:,.2f} INR." if available else "Future target or projected asset value missing.",
    )


def fact_required_monthly_contribution(
    funding_gap: float | None,
    annual_return: float | None,
    duration_years: float | None,
) -> DerivedFact:
    val = calculate_required_monthly_contribution(funding_gap, annual_return, duration_years)
    available = val is not None
    return DerivedFact(
        fact_id="required_monthly_contribution",
        value=val,
        unit="INR/month",
        formula="Goal Funding Gap amortized over duration at assumed monthly return",
        inputs_used={"funding_gap": funding_gap, "annual_return": annual_return, "duration_years": duration_years},
        available=available,
        data_quality="authoritative" if available else "unavailable",
        explanation=f"Required monthly contribution is {val:,.2f} INR/month." if available else "Inputs missing or invalid return assumption.",
    )
