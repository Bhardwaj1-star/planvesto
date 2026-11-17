"""
domain/features/participate_with_your_finances/sensitivity.py
Chapter 12 — Participate with Your Finances: Sensitivity Analysis (§12.2).

Tests sensitivity of goal funding and required contributions to variations in key assumptions:
- Return variations (e.g. -2%, -1%, +1%, +2%)
- Inflation variations
- Timeline adjustments (e.g. delaying goal by 1 or 2 years)
- Contribution changes (increasing / decreasing monthly SIP)
"""

from dataclasses import dataclass
from decimal import Decimal
from typing import List
from app.domain.shared.value_objects import Money, Rate
from app.domain.shared.calculations.goal_funding import calculate_required_sip


@dataclass(frozen=True)
class SensitivityPoint:
    """Outcome for a specific parameter variation."""
    parameter_variation_label: str
    varied_return_rate: Rate
    resulting_required_monthly_sip: Money
    sip_difference_from_baseline: Money
    feasibility_impact: str


@dataclass(frozen=True)
class ReturnSensitivityAnalysis:
    """Sensitivity analysis across alternative return rates for a goal."""
    goal_id: str
    target_amount: Money
    horizon_years: int
    baseline_return_rate: Rate
    baseline_monthly_sip: Money
    sensitivity_points: List[SensitivityPoint]


def run_return_sensitivity_analysis(
    goal_id: str,
    target_amount: Money,
    horizon_years: int,
    baseline_return_rate: Rate,
    rate_shifts_pct: List[Decimal] = None,
) -> ReturnSensitivityAnalysis:
    """
    Evaluates required SIP across a range of return assumptions.
    Demonstrates sensitivity to market returns without promising outcomes.
    """
    if rate_shifts_pct is None:
        rate_shifts_pct = [Decimal("-2.0"), Decimal("-1.0"), Decimal("1.0"), Decimal("2.0")]

    baseline_sip = calculate_required_sip(target_amount, baseline_return_rate, horizon_years)
    points: List[SensitivityPoint] = []

    for shift in rate_shifts_pct:
        shifted_rate_val = baseline_return_rate.percentage + shift
        if shifted_rate_val < Decimal("0.0"):
            shifted_rate_val = Decimal("0.0")

        shifted_rate = Rate.from_percentage(shifted_rate_val)
        shifted_sip = calculate_required_sip(target_amount, shifted_rate, horizon_years)
        diff = shifted_sip - baseline_sip

        if diff.is_positive:
            impact = f"Requires additional {diff.amount}/month due to lower return assumption."
        elif diff.is_negative:
            impact = f"Requires {abs(diff.amount)}/month less due to higher return assumption."
        else:
            impact = "No change."

        points.append(
            SensitivityPoint(
                parameter_variation_label=f"{shift:+}% p.a. ({shifted_rate.percentage:.1f}%)",
                varied_return_rate=shifted_rate,
                resulting_required_monthly_sip=shifted_sip,
                sip_difference_from_baseline=diff,
                feasibility_impact=impact,
            )
        )

    return ReturnSensitivityAnalysis(
        goal_id=goal_id,
        target_amount=target_amount,
        horizon_years=horizon_years,
        baseline_return_rate=baseline_return_rate,
        baseline_monthly_sip=baseline_sip,
        sensitivity_points=points,
    )
