"""
Unit tests for Chapter 13 Plan Acceptance Workflow and Action Plan Lifecycle.
"""

from datetime import date
import pytest
from app.domain.shared.value_objects import Money, Rate
from app.domain.features.strategy_builder.funding_paths import (
    FundingPathType,
    SelfMoneyPathResult,
    FinancingPathResult,
)
from app.domain.features.action_plan import (
    ActionType,
    ActionStatus,
    ActionItem,
    transition_action_status,
)
from app.application.workflows.plan_acceptance import execute_plan_acceptance


def test_plan_acceptance_self_money():
    self_path = SelfMoneyPathResult(
        goal_id="goal-child-edu",
        total_own_money_contributed=Money.from_amount("1500000.00"),
        projected_corpus_at_goal_date=Money.from_amount("2500000.00"),
        goal_target_amount=Money.from_amount("2500000.00"),
        goal_amount_funded=Money.from_amount("2500000.00"),
        remaining_corpus_after_goal=Money.zero(),
        yearly_projections=[],
        is_fully_funded=True,
        explanation="Fully funded through SIP.",
    )

    result = execute_plan_acceptance(
        investor_id="inv-101",
        goal_id="goal-child-edu",
        target_amount=Money.from_amount("2500000.00"),
        horizon_years=10,
        selected_path_type=FundingPathType.SELF_MONEY,
        self_money_path=self_path,
        acceptance_date=date(2026, 11, 16),
    )

    assert result.accepted_plan.goal_id == "goal-child-edu"
    assert result.accepted_plan.accepted_funding_path == FundingPathType.SELF_MONEY
    assert len(result.initial_actions) == 1
    assert result.initial_actions[0].action_type == ActionType.START_SIP
    assert result.initial_actions[0].status == ActionStatus.PENDING


def test_plan_acceptance_financing_path():
    fin_path = FinancingPathResult(
        goal_id="goal-home-buy",
        own_down_payment=Money.from_amount("2000000.00"),
        total_own_contributions=Money.from_amount("2000000.00"),
        total_own_money_outflow=Money.from_amount("7000000.00"),
        financing_amount=Money.from_amount("5000000.00"),
        loan_interest_rate=Rate.from_percentage("8.5"),
        loan_tenure_months=240,
        monthly_emi=Money.from_amount("43391.00"),
        total_interest_cost=Money.from_amount("5413840.00"),
        total_repayment_amount=Money.from_amount("10413840.00"),
        emi_affordable_within_surplus=True,
        projected_corpus_at_goal_date=Money.from_amount("7000000.00"),
        goal_target_amount=Money.from_amount("7000000.00"),
        goal_amount_funded=Money.from_amount("7000000.00"),
        remaining_corpus_after_goal=Money.zero(),
        yearly_projections=[],
        is_fully_funded=True,
        explanation="Funded via own down payment + home loan.",
    )

    result = execute_plan_acceptance(
        investor_id="inv-101",
        goal_id="goal-home-buy",
        target_amount=Money.from_amount("7000000.00"),
        horizon_years=5,
        selected_path_type=FundingPathType.SELF_MONEY_PLUS_FINANCING,
        financing_path=fin_path,
        acceptance_date=date(2026, 11, 16),
    )

    assert result.accepted_plan.accepted_funding_path == FundingPathType.SELF_MONEY_PLUS_FINANCING
    assert len(result.initial_actions) == 2
    types = [a.action_type for a in result.initial_actions]
    assert ActionType.LUMP_SUM_INVESTMENT in types
    assert ActionType.ACCOUNT_SEGREGATION in types


def test_action_item_lifecycle_transitions():
    action = ActionItem(
        action_id="act-001",
        investor_id="inv-101",
        plan_id="plan-001",
        action_type=ActionType.START_SIP,
        title="Start SIP",
        description="Set up mutual fund SIP mandate",
        target_amount=Money.from_amount("15000.00"),
        target_date=date(2026, 12, 1),
        status=ActionStatus.PENDING,
    )

    # Valid transition: PENDING -> IN_PROGRESS
    act_in_progress = transition_action_status(action, ActionStatus.IN_PROGRESS, as_of_date=date(2026, 11, 20))
    assert act_in_progress.status == ActionStatus.IN_PROGRESS

    # Valid transition: IN_PROGRESS -> COMPLETED
    act_completed = transition_action_status(act_in_progress, ActionStatus.COMPLETED, as_of_date=date(2026, 11, 25))
    assert act_completed.status == ActionStatus.COMPLETED

    # Invalid transition: COMPLETED is terminal
    with pytest.raises(ValueError, match="Invalid transition from completed"):
        transition_action_status(act_completed, ActionStatus.IN_PROGRESS, as_of_date=date(2026, 11, 26))
