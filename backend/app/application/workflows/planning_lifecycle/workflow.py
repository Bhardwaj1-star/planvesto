"""
application/workflows/planning_lifecycle/workflow.py
Planning Lifecycle Workflow (Goal Planner -> Strategy Builder Handoff).

Coordinates the end-to-end planning journey:
1. Coordinates Goal Requirement Planning in Goal Planner (Chapter 10 §10.2).
2. Coordinates Fund Feasibility evaluation in Goal Planner (Chapter 10 §10.3).
3. Passes approved Goal Planner outputs to Strategy Builder (Chapter 11).
4. Invokes Strategy Builder to construct Self Money path, optional Financing path, and side-by-side comparison matrix.

Non-negotiable invariants:
- Feature domains (Goal Planner and Strategy Builder) DO NOT call one another directly.
- The workflow coordinates the handoff without duplicating financial calculations or rules.
"""

from dataclasses import dataclass
from datetime import date
from typing import Optional

from app.domain.shared.value_objects import Money, Rate
from app.domain.features.goal_planner.requirement import (
    GoalInstance,
    GoalRequirementOutput,
    plan_goal_requirement,
)
from app.domain.features.goal_planner.feasibility import (
    GoalFeasibilityResult,
    evaluate_fund_feasibility,
)
from app.domain.features.strategy_builder import (
    SelfMoneyPathResult,
    FinancingPathResult,
    StrategyComparisonMatrix,
    build_self_money_path,
    build_financing_path,
    compare_funding_paths,
)


@dataclass(frozen=True)
class FinancingOptionsInput:
    """Optional borrowing terms for evaluating the financing path."""
    down_payment: Money
    loan_annual_interest_rate: Rate
    loan_tenure_months: int


@dataclass(frozen=True)
class PlanningLifecycleResult:
    """Consolidated outcome of the planning lifecycle run."""
    goal_requirement: GoalRequirementOutput
    feasibility: GoalFeasibilityResult
    self_money_path: SelfMoneyPathResult
    financing_path: Optional[FinancingPathResult]
    comparison_matrix: Optional[StrategyComparisonMatrix]


def execute_planning_lifecycle(
    goal: GoalInstance,
    available_monthly_surplus: Money,
    current_calendar_year: int,
    financing_input: Optional[FinancingOptionsInput] = None,
    evaluation_date: Optional[date] = None,
) -> PlanningLifecycleResult:
    """
    Coordinates the handoff between Goal Planner and Strategy Builder.
    """
    eval_date = evaluation_date or goal.created_at

    # Step 1 & 2: Goal Feasibility Evaluation (Goal Planner Domain)
    feasibility = evaluate_fund_feasibility(
        goal=goal,
        evaluation_date=eval_date,
        available_monthly_surplus=available_monthly_surplus,
    )
    requirement = plan_goal_requirement(goal, eval_date)

    # Step 3: Strategy Builder Handoff (Strategy Builder Domain)
    initial_assets = sum((a.effective_value.amount for a in goal.mapped_assets), Money.zero().amount)
    initial_allocated = Money(amount=initial_assets, currency=goal.current_cost.currency)

    horizon_years = max(1, (requirement.months_horizon + 11) // 12)

    self_money_res = build_self_money_path(
        goal_id=goal.id,
        goal_target_amount=requirement.future_goal_target,
        horizon_years=horizon_years,
        start_calendar_year=current_calendar_year,
        initial_allocated_assets=initial_allocated,
        required_monthly_sip=feasibility.required_monthly_sip,
        expected_annual_return=goal.expected_annual_return,
    )

    financing_res: Optional[FinancingPathResult] = None
    comparison: Optional[StrategyComparisonMatrix] = None

    if financing_input is not None:
        financing_res = build_financing_path(
            goal_id=goal.id,
            goal_target_amount=requirement.future_goal_target,
            horizon_years=horizon_years,
            start_calendar_year=current_calendar_year,
            own_down_payment=financing_input.down_payment,
            loan_annual_interest_rate=financing_input.loan_annual_interest_rate,
            loan_tenure_months=financing_input.loan_tenure_months,
            available_monthly_surplus=available_monthly_surplus,
            initial_allocated_assets=initial_allocated,
            expected_annual_return=goal.expected_annual_return,
        )

        comparison = compare_funding_paths(
            self_money_path=self_money_res,
            financing_path=financing_res,
        )

    return PlanningLifecycleResult(
        goal_requirement=requirement,
        feasibility=feasibility,
        self_money_path=self_money_res,
        financing_path=financing_res,
        comparison_matrix=comparison,
    )
