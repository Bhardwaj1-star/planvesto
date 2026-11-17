"""
Unit tests for Chapter 12 Participate with Your Finances
(Scenarios, Sensitivity Analysis, and Decision Comparison).
"""

from decimal import Decimal
from datetime import date
from app.domain.shared.value_objects import Money, Rate
from app.domain.features.participate_with_your_finances import (
    HypotheticalParameterOverride,
    HypotheticalScenario,
    run_return_sensitivity_analysis,
    DecisionAlternativeOption,
    DecisionComparisonResult,
)


def test_hypothetical_scenario_invariants():
    scenario = HypotheticalScenario(
        scenario_id="scen-01",
        investor_id="inv-101",
        scenario_name="Early Retirement 50",
        created_at=date(2026, 11, 16),
        baseline_snapshot_id="snap-2026-11",
        parameter_overrides=[
            HypotheticalParameterOverride(
                parameter_name="target_retirement_age",
                baseline_value="55",
                hypothetical_value="50",
                rationale="Test feasibility of retiring 5 years earlier",
            )
        ],
    )
    assert scenario.is_hypothetical_only is True
    assert scenario.parameter_overrides[0].parameter_name == "target_retirement_age"


def test_return_sensitivity_analysis():
    target = Money.from_amount("1000000.00")  # 10 Lakhs
    horizon = 5  # 5 years
    base_rate = Rate.from_percentage("12.0")

    analysis = run_return_sensitivity_analysis(
        goal_id="goal-house-1",
        target_amount=target,
        horizon_years=horizon,
        baseline_return_rate=base_rate,
        rate_shifts_pct=[Decimal("-2.0"), Decimal("+2.0")],
    )

    assert analysis.goal_id == "goal-house-1"
    assert len(analysis.sensitivity_points) == 2

    # Point 1: 10% (-2%)
    p_down = analysis.sensitivity_points[0]
    assert p_down.varied_return_rate.percentage == Decimal("10.0")
    # Lower return requires MORE monthly SIP
    assert p_down.sip_difference_from_baseline.is_positive
    assert p_down.resulting_required_monthly_sip > analysis.baseline_monthly_sip

    # Point 2: 14% (+2%)
    p_up = analysis.sensitivity_points[1]
    assert p_up.varied_return_rate.percentage == Decimal("14.0")
    # Higher return requires LESS monthly SIP
    assert p_up.sip_difference_from_baseline.is_negative
    assert p_up.resulting_required_monthly_sip < analysis.baseline_monthly_sip


def test_decision_comparison():
    opt_rent = DecisionAlternativeOption(
        option_id="opt-rent",
        option_name="Continue Renting & Invest Surplus",
        description="Pay rent and invest remaining monthly surplus in equity funds.",
        monthly_outflow=Money.from_amount("45000.00"),
        total_lifetime_cost=Money.from_amount("5400000.00"),
        pros=["High liquidity", "No mortgage debt obligation"],
        cons=["No physical real estate ownership"],
        key_trade_off="Flexibility and higher investment corpus vs home ownership",
    )
    opt_buy = DecisionAlternativeOption(
        option_id="opt-buy",
        option_name="Buy House with Home Loan",
        description="Down payment from savings + 20-year home loan.",
        monthly_outflow=Money.from_amount("75000.00"),
        total_lifetime_cost=Money.from_amount("18000000.00"),
        pros=["Home ownership", "Stability"],
        cons=["High interest cost", "Fixed debt burden"],
        key_trade_off="Substantial debt commitment and reduced monthly surplus",
    )

    comparison = DecisionComparisonResult(
        comparison_id="comp-rent-vs-buy",
        investor_id="inv-101",
        title="Rent vs Buy Housing Decision",
        context_description="Evaluating buy vs rent over 10-year horizon",
        options=[opt_rent, opt_buy],
        unresolved_questions_for_investor=["Are you planning to relocate in the next 5 years?"],
    )

    assert len(comparison.options) == 2
    assert comparison.options[0].monthly_outflow < comparison.options[1].monthly_outflow
