"""
domain/features/goal_planner/feasibility.py
Chapter 10 — Goal Feasibility (§10.1, §10.3)

Single test: Fund Feasibility.
Evaluates supported funding methods (SIP, Lump Sum, Lump Sum + SIP) within that single test.
Reports Case 1 (Affordable) vs Case 2B (Capacity Shortfall: Surplus Gap & Required Surplus Increase %).
"""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from enum import Enum
from typing import List, Optional

from app.domain.canonical.goal_taxonomy import CanonicalGoalId
from app.domain.shared.value_objects import Money, Rate
from app.domain.shared.constraints import (
    ConstraintEvaluationResult,
    evaluate_sip_affordability_gate,
)
from app.domain.shared.calculations.goal_funding import (
    calculate_required_monthly_contribution,
    calculate_monthly_sip_surplus_gap,
    calculate_required_surplus_increase,
)
from app.domain.features.goal_planner.requirement import (
    GoalInstance,
    GoalRequirementOutput,
    plan_goal_requirement,
)


class GoalFundingMethod(str, Enum):
    """Funding methods evaluated within the single Fund Feasibility test (§10.3)."""
    SIP = "sip"
    LUMP_SUM = "lump_sum"
    COMBINED_LUMP_SUM_SIP = "combined_lump_sum_sip"


class FundFeasibilityCase(str, Enum):
    """Canonical Fund Feasibility cases (§10.3)."""
    CASE_1_AFFORDABLE = "case_1_affordable"
    CASE_2_SHORTFALL = "case_2_capacity_shortfall"


@dataclass(frozen=True)
class GoalFeasibilityResult:
    """Canonical Fund Feasibility result payload (§10.2, §10.3)."""
    goal_id: str
    goal_canonical_id: CanonicalGoalId
    funding_method: GoalFundingMethod
    fund_feasibility_case: FundFeasibilityCase

    # Requirement Planning Outputs (§10.2)
    future_goal_target: Money
    projected_existing_funding: Money
    remaining_funding_gap: Money
    required_return: Optional[Rate]

    # Feasibility Method Outputs (§10.3)
    required_monthly_sip: Optional[Money]
    required_lump_sum: Optional[Money]

    # Capacity & Surplus Gap Outputs (§10.3 Case 2B)
    available_monthly_surplus: Money
    surplus_gap: Optional[Money]
    required_surplus_increase_pct: Optional[Rate]

    is_feasible_under_current_conditions: bool
    constraint_evaluations: List[ConstraintEvaluationResult]
    explanation: str
    months_horizon: int


def evaluate_fund_feasibility(
    goal: GoalInstance,
    evaluation_date: date,
    available_monthly_surplus: Money,
    funding_method: GoalFundingMethod = GoalFundingMethod.SIP,
) -> GoalFeasibilityResult:
    """
    Executes the canonical Fund Feasibility test (§10.3) for a selected funding method.
    Consumes Chapter 10 Goal Requirement Planning.
    """
    req_output: GoalRequirementOutput = plan_goal_requirement(goal, evaluation_date)

    constraint_evaluations: List[ConstraintEvaluationResult] = list(req_output.asset_constraint_evaluations)
    required_sip: Optional[Money] = None
    required_lump_sum: Optional[Money] = None
    surplus_gap: Optional[Money] = None
    required_surplus_increase_pct: Optional[Rate] = None
    is_feasible: bool = True
    explanation_parts: List[str] = []

    if funding_method in (GoalFundingMethod.SIP, GoalFundingMethod.COMBINED_LUMP_SUM_SIP):
        calculated_sip = calculate_required_monthly_contribution(
            remaining_funding_gap=req_output.funding_gap,
            months_remaining=req_output.months_horizon,
            effective_annual_return=goal.expected_annual_return,
        )
        required_sip = calculated_sip or Money.zero(currency=goal.current_cost.currency)

        additional_required_sip = required_sip - goal.existing_goal_sip
        if additional_required_sip.is_negative:
            additional_required_sip = Money.zero(currency=goal.current_cost.currency)

        aff_gate = evaluate_sip_affordability_gate(
            additional_required_sip=additional_required_sip,
            available_monthly_surplus=available_monthly_surplus,
        )
        constraint_evaluations.append(aff_gate)

        if aff_gate.is_satisfied:
            feasibility_case = FundFeasibilityCase.CASE_1_AFFORDABLE
            is_feasible = True
            surplus_gap = Money.zero(currency=goal.current_cost.currency)
            required_surplus_increase_pct = Rate.from_percentage("0.0")
            explanation_parts.append(aff_gate.explanation)
        else:
            feasibility_case = FundFeasibilityCase.CASE_2_SHORTFALL
            is_feasible = False
            surplus_gap = calculate_monthly_sip_surplus_gap(additional_required_sip, available_monthly_surplus)
            required_surplus_increase_pct = calculate_required_surplus_increase(surplus_gap, available_monthly_surplus)
            explanation_parts.append(aff_gate.explanation)

    elif funding_method == GoalFundingMethod.LUMP_SUM:
        years_f = float(req_output.duration_years)
        r_f = float(goal.expected_annual_return.as_decimal_ratio)
        disc_factor = (1.0 + r_f) ** years_f if years_f > 0 else 1.0
        pv = req_output.future_goal_target.amount / Decimal(str(disc_factor))
        required_lump_sum = Money(amount=pv, currency=goal.current_cost.currency)

        total_current_mapped = sum((a.effective_value.amount for a in goal.mapped_assets if a.is_accessible and not a.is_committed), Decimal(0))
        total_curr_money = Money(amount=total_current_mapped, currency=goal.current_cost.currency)

        if total_curr_money < required_lump_sum:
            is_feasible = False
            feasibility_case = FundFeasibilityCase.CASE_2_SHORTFALL
            shortfall = required_lump_sum - total_curr_money
            explanation_parts.append(
                f"Lump-sum requirement of {required_lump_sum.amount} exceeds eligible available funding of {total_curr_money.amount} (Shortfall: {shortfall.amount})."
            )
        else:
            is_feasible = True
            feasibility_case = FundFeasibilityCase.CASE_1_AFFORDABLE
            explanation_parts.append(
                f"Lump-sum requirement of {required_lump_sum.amount} is fully covered by eligible assets ({total_curr_money.amount})."
            )

    full_explanation = " | ".join(explanation_parts)

    return GoalFeasibilityResult(
        goal_id=goal.id,
        goal_canonical_id=goal.canonical_id,
        funding_method=funding_method,
        fund_feasibility_case=feasibility_case,
        future_goal_target=req_output.future_goal_target,
        projected_existing_funding=req_output.projected_existing_funding,
        remaining_funding_gap=req_output.funding_gap,
        required_return=req_output.required_return,
        required_monthly_sip=required_sip,
        required_lump_sum=required_lump_sum,
        available_monthly_surplus=available_monthly_surplus,
        surplus_gap=surplus_gap,
        required_surplus_increase_pct=required_surplus_increase_pct,
        is_feasible_under_current_conditions=is_feasible,
        constraint_evaluations=constraint_evaluations,
        explanation=full_explanation,
        months_horizon=req_output.months_horizon,
    )
