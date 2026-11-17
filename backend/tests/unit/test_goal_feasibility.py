"""
Unit tests for Chapter 10 Goal Planner & Fund Feasibility Engine.
"""

from datetime import date
from decimal import Decimal
from app.domain.canonical.goal_taxonomy import CanonicalGoalId
from app.domain.canonical.financial_categories import CanonicalAssetCategoryId
from app.domain.shared.value_objects import Money, Rate
from app.domain.features.financial_state.models import AssetRecord
from app.domain.features.goal_planner import (
    GoalInstance,
    GoalFundingMethod,
    FundFeasibilityCase,
    evaluate_fund_feasibility,
)


def test_goal_feasibility_sip_path_case_1_affordable():
    eval_date = date(2026, 11, 16)
    target_date = date(2031, 11, 16)  # 5 years horizon

    # Vehicle Goal: Today cost 10 Lakh, 6% inflation, 12% expected return
    goal = GoalInstance(
        id="goal-vehicle-1",
        investor_id="inv-123",
        canonical_id=CanonicalGoalId.VEHICLE,
        name="Family SUV",
        target_date=target_date,
        current_cost=Money.from_amount("1000000.00"),
        applicable_inflation_rate=Rate.from_percentage("6.0"),
        expected_annual_return=Rate.from_percentage("12.0"),
        created_at=eval_date,
    )

    # Investor has 25,000 monthly surplus
    surplus = Money.from_amount("25000.00")

    result = evaluate_fund_feasibility(
        goal=goal,
        evaluation_date=eval_date,
        available_monthly_surplus=surplus,
        funding_method=GoalFundingMethod.SIP,
    )

    # 10 Lakh @ 6% for 5 years -> Future Target ≈ 13,38,225
    assert result.future_goal_target.amount > Decimal("1300000.00")
    assert result.future_goal_target.amount < Decimal("1350000.00")

    # Required SIP for ~13.38 Lakh gap over 60 months @ 12% return is ~16,500 - 17,000
    assert result.required_monthly_sip is not None
    assert result.required_monthly_sip.amount < Decimal("20000.00")

    # Case 1: Affordable!
    assert result.fund_feasibility_case == FundFeasibilityCase.CASE_1_AFFORDABLE
    assert result.is_feasible_under_current_conditions is True
    assert result.surplus_gap.amount == Decimal("0.00")
    assert "is fully affordable" in result.explanation


def test_goal_feasibility_sip_path_case_2_shortfall():
    eval_date = date(2026, 11, 16)
    target_date = date(2029, 11, 16)  # 3 years horizon

    # Dream Home Down-payment: 25 Lakh in 3 years
    goal = GoalInstance(
        id="goal-home-1",
        investor_id="inv-123",
        canonical_id=CanonicalGoalId.DREAM_HOME,
        name="Dream Home Down Payment",
        target_date=target_date,
        current_cost=Money.from_amount("2500000.00"),
        applicable_inflation_rate=Rate.from_percentage("7.0"),
        expected_annual_return=Rate.from_percentage("10.0"),
        created_at=eval_date,
    )

    # Investor only has 15,000 monthly surplus (insufficient for 25+ Lakh in 3 years)
    surplus = Money.from_amount("15000.00")

    result = evaluate_fund_feasibility(
        goal=goal,
        evaluation_date=eval_date,
        available_monthly_surplus=surplus,
        funding_method=GoalFundingMethod.SIP,
    )

    # Required SIP will be around ~65,000 - 75,000
    assert result.required_monthly_sip is not None
    assert result.required_monthly_sip.amount > Decimal("50000.00")

    # Case 2: Shortfall with explicit Surplus Gap and Required Surplus Increase % (§10.3 Case 2B)
    assert result.fund_feasibility_case == FundFeasibilityCase.CASE_2_SHORTFALL
    assert result.is_feasible_under_current_conditions is False
    assert result.surplus_gap is not None
    assert result.surplus_gap.is_positive
    assert result.required_surplus_increase_pct is not None
    assert result.required_surplus_increase_pct.percentage > Decimal("100.0")  # Needs >100% surplus increase
    assert "exceeds Available Monthly Surplus" in result.explanation


def test_goal_feasibility_with_mapped_assets_and_required_return():
    eval_date = date(2026, 11, 16)
    target_date = date(2031, 11, 16)  # 5 years horizon

    # Mapped Asset: 5 Lakh Mutual fund, fully accessible
    mapped_mf = AssetRecord(
        id="ast-mf-1",
        category=CanonicalAssetCategoryId.MUTUAL_FUNDS,
        name="Equity Corpus",
        value=Money.from_amount("500000.00"),
        as_of_date=eval_date,
        is_accessible=True,
    )

    # Goal: 15 Lakh current cost
    goal = GoalInstance(
        id="goal-wealth-1",
        investor_id="inv-123",
        canonical_id=CanonicalGoalId.WEALTH_CREATION,
        name="Child Higher Education",
        target_date=target_date,
        current_cost=Money.from_amount("1500000.00"),
        applicable_inflation_rate=Rate.from_percentage("8.0"),
        expected_annual_return=Rate.from_percentage("12.0"),
        created_at=eval_date,
        mapped_assets=[mapped_mf],
    )

    surplus = Money.from_amount("30000.00")

    result = evaluate_fund_feasibility(
        goal=goal,
        evaluation_date=eval_date,
        available_monthly_surplus=surplus,
        funding_method=GoalFundingMethod.SIP,
    )

    # Mapped 5 Lakh asset compounds at 12% over 5 years to ~8.8 Lakh
    assert result.projected_existing_funding.amount > Decimal("800000.00")

    # Remaining funding gap = Future Target (≈ 22 Lakh) - Projected Funding (≈ 8.8 Lakh) ≈ 13.2 Lakh
    assert result.remaining_funding_gap.amount < result.future_goal_target.amount

    # Required Return output (§10.2: only when assets are mapped)
    assert result.required_return is not None
    assert result.required_return.percentage > Decimal("0.0")

    assert result.fund_feasibility_case == FundFeasibilityCase.CASE_1_AFFORDABLE
    assert result.is_feasible_under_current_conditions is True
