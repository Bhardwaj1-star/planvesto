"""
Chapter 05 — Canonical Measurements & Formulas
Group D: Goal Funding & Feasibility Calculations (§2 Group D, §3 Group D)

1. metric_future_goal_target: Future Goal Target
   Formula: Today's Goal Cost × (1 + applicable Inflation Rate) ^ Duration in Years

2. metric_projected_asset_value: Projected Asset Value
   Formula: Current Allocated Amount × (1 + periodic return) ^ number of periods

3. metric_goal_funding_gap: Goal Funding Gap
   Formula: Future Goal Target − Projected Value of assets validly mapped to that goal

4. metric_goal_funding_ratio: Goal Funding Ratio (today's cost basis)
   Formula: (Current Eligible Goal Funding ÷ Current Goal Cost) × 100

5. metric_future_funding_ratio: Future Funding Ratio (future target basis)
   Formula: (Projected Goal Funding ÷ Future Goal Target) × 100

6. metric_required_monthly_contribution: Required Monthly Contribution
   Formula (Ordinary Annuity at month-end):
   Let G = remaining future funding gap at goal date
   Let n = whole monthly periods remaining
   Let r_m = (1 + r_a)^(1/12) − 1 (effective monthly return)
   If r_m > 0: Contribution = G × r_m ÷ ((1 + r_m)^n − 1)
   If r_m == 0: Contribution = G ÷ n

7. metric_monthly_sip_surplus_gap: Monthly SIP / Surplus Gap
   Formula: Additional Required SIP − Available Monthly Surplus

8. metric_required_surplus_increase: Required Surplus Increase (%)
   Formula: (Monthly SIP / Surplus Gap ÷ Available Monthly Surplus) × 100
   Valid only when Available Monthly Surplus > 0.

9. metric_risk_required_return: Risk Required Return (single-goal implied return)
   Formula: ((Future Goal Target ÷ Current Goal Funding) ^ (1 ÷ Duration in Years) − 1) × 100
"""

from decimal import Decimal
from typing import Optional
from app.domain.shared.value_objects import Money, Rate


def calculate_future_goal_target(
    current_cost: Money,
    annual_inflation_rate: Rate,
    duration_years: Decimal | int | float,
) -> Money:
    """
    Calculate Future Goal Target:
    Today's Goal Cost × (1 + inflation_rate) ^ duration_years
    """
    years = float(duration_years)
    inflation = float(annual_inflation_rate.as_decimal_ratio)
    multiplier = (1.0 + inflation) ** years
    future_amount = current_cost.amount * Decimal(str(multiplier))
    return Money(amount=future_amount, currency=current_cost.currency)


def calculate_projected_asset_value(
    current_allocated: Money,
    periodic_return: Rate,
    periods: int | float | Decimal,
) -> Money:
    """
    Calculate Projected Asset Value:
    Current Allocated Amount × (1 + periodic_return) ^ periods
    """
    r = float(periodic_return.as_decimal_ratio)
    p = float(periods)
    multiplier = (1.0 + r) ** p
    future_amount = current_allocated.amount * Decimal(str(multiplier))
    return Money(amount=future_amount, currency=current_allocated.currency)


def calculate_goal_funding_gap(
    future_goal_target: Money,
    projected_mapped_assets: Money,
) -> Money:
    """
    Calculate Goal Funding Gap:
    Future Goal Target − Projected Value of Mapped Assets
    """
    gap = future_goal_target - projected_mapped_assets
    if gap.is_negative:
        return Money.zero(currency=future_goal_target.currency)
    return gap


def calculate_goal_funding_ratio(
    current_funding: Money,
    current_cost: Money,
) -> Optional[Rate]:
    """
    Calculate Current Goal Funding Ratio (%):
    (Current Eligible Goal Funding ÷ Current Goal Cost) × 100
    """
    if current_cost.amount <= Decimal(0):
        return None
    ratio = (current_funding.amount / current_cost.amount) * Decimal(100)
    return Rate.from_percentage(ratio)


def calculate_future_funding_ratio(
    projected_funding: Money,
    future_target: Money,
) -> Optional[Rate]:
    """
    Calculate Future Funding Ratio (%):
    (Projected Goal Funding ÷ Future Goal Target) × 100
    """
    if future_target.amount <= Decimal(0):
        return None
    ratio = (projected_funding.amount / future_target.amount) * Decimal(100)
    return Rate.from_percentage(ratio)


def calculate_required_monthly_contribution(
    remaining_funding_gap: Money,
    months_remaining: int,
    effective_annual_return: Rate,
) -> Optional[Money]:
    """
    Calculate Required Monthly Contribution (Ordinary Annuity paid at month-end):
    G × r_m ÷ ((1 + r_m)^n − 1)
    where r_m = (1 + r_a)^(1/12) − 1
    """
    if months_remaining <= 0 or remaining_funding_gap.amount <= Decimal(0):
        return Money.zero(currency=remaining_funding_gap.currency)

    r_m = float(effective_annual_return.to_monthly_compounded_rate())
    n = months_remaining
    g = float(remaining_funding_gap.amount)

    if abs(r_m) < 1e-9:
        contribution = g / n
    else:
        denom = ((1.0 + r_m) ** n) - 1.0
        if abs(denom) < 1e-12:
            return None
        contribution = (g * r_m) / denom

    return Money(amount=Decimal(str(contribution)), currency=remaining_funding_gap.currency)


def calculate_required_sip(
    target_gap: Money,
    expected_annual_return: Rate,
    horizon_years: int,
) -> Money:
    """Convenience wrapper for required monthly SIP over years horizon."""
    months = horizon_years * 12
    res = calculate_required_monthly_contribution(target_gap, months, expected_annual_return)
    return res if res is not None else Money.zero(currency=target_gap.currency)


def calculate_monthly_sip_surplus_gap(
    additional_required_sip: Money,
    available_monthly_surplus: Money,
) -> Money:
    """
    Calculate Monthly SIP / Surplus Gap:
    Additional Required SIP − Available Monthly Surplus
    If non-positive, returns Money.zero (no shortfall).
    """
    gap = additional_required_sip - available_monthly_surplus
    if gap.is_negative:
        return Money.zero(currency=additional_required_sip.currency)
    return gap


def calculate_required_surplus_increase(
    monthly_sip_surplus_gap: Money,
    available_monthly_surplus: Money,
) -> Optional[Rate]:
    """
    Calculate Required Surplus Increase (%):
    (Monthly SIP / Surplus Gap ÷ Available Monthly Surplus) × 100
    Only valid when Available Monthly Surplus > 0.
    """
    if available_monthly_surplus.amount <= Decimal(0):
        return None
    if monthly_sip_surplus_gap.is_zero or monthly_sip_surplus_gap.is_negative:
        return Rate.from_percentage(0)

    ratio = (monthly_sip_surplus_gap.amount / available_monthly_surplus.amount) * Decimal(100)
    return Rate.from_percentage(ratio)


def calculate_risk_required_return(
    future_goal_target: Money,
    current_goal_funding: Money,
    duration_years: Decimal | int | float,
) -> Optional[Rate]:
    """
    Calculate Risk Required Return (annualised implied return):
    ((Future Target ÷ Current Funding) ^ (1 ÷ Years) − 1) × 100
    """
    years = float(duration_years)
    if years <= 0 or current_goal_funding.amount <= Decimal(0) or future_goal_target.amount <= Decimal(0):
        return None

    ratio = float(future_goal_target.amount / current_goal_funding.amount)
    implied_return = ((ratio ** (1.0 / years)) - 1.0) * 100.0
    return Rate.from_percentage(Decimal(str(implied_return)))
