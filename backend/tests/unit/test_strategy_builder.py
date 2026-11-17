"""
Unit tests for Chapter 11 Strategy Builder (Self Money vs Financing & Comparison).
"""

from decimal import Decimal
from app.domain.shared.value_objects import Money, Rate
from app.domain.features.strategy_builder import (
    FundingPathType,
    AssetDispositionChoice,
    AssetDecision,
    calculate_loan_emi,
    build_self_money_path,
    build_financing_path,
    compare_funding_paths,
)


def test_calculate_loan_emi():
    principal = Money.from_amount("1000000.00")  # 10 Lakh loan
    rate = Rate.from_percentage("8.5")            # 8.5% p.a.
    tenure_months = 60                            # 5 years

    monthly_emi, total_repayment, total_interest = calculate_loan_emi(
        principal=principal,
        annual_interest_rate=rate,
        tenure_months=tenure_months,
    )

    # Standard EMI for 10L @ 8.5% for 60 months is approx 20,517
    assert monthly_emi.amount > Decimal("20400.00")
    assert monthly_emi.amount < Decimal("20600.00")

    # Total repayment = EMI * 60 ≈ 12,31,000
    assert total_repayment.amount > Decimal("1220000.00")
    assert total_repayment.amount < Decimal("1240000.00")

    # Total interest = Total repayment - Principal ≈ 2,31,000
    assert total_interest.amount > Decimal("220000.00")
    assert total_interest.amount < Decimal("240000.00")


def test_build_self_money_path():
    target = Money.from_amount("1500000.00")  # 15 Lakh
    initial_assets = Money.from_amount("300000.00")  # 3 Lakh mapped
    monthly_sip = Money.from_amount("15000.00")      # 15k SIP
    exp_return = Rate.from_percentage("12.0")        # 12% return

    res = build_self_money_path(
        goal_id="goal-retire-1",
        goal_target_amount=target,
        horizon_years=5,
        start_calendar_year=2026,
        initial_allocated_assets=initial_assets,
        required_monthly_sip=monthly_sip,
        expected_annual_return=exp_return,
    )

    assert len(res.yearly_projections) == 5
    assert res.projected_corpus_at_goal_date.is_positive
    assert res.goal_amount_funded.is_positive
    assert "Self Money path accumulates" in res.explanation


def test_build_financing_path_and_comparison():
    target = Money.from_amount("2000000.00")  # 20 Lakh vehicle/home
    own_down_payment = Money.from_amount("500000.00")  # 5 Lakh own funds
    loan_rate = Rate.from_percentage("9.0")
    tenure_months = 60
    surplus = Money.from_amount("40000.00")  # 40,000 monthly surplus

    # 1. Build Financing Path
    fin_res = build_financing_path(
        goal_id="goal-vehicle-1",
        goal_target_amount=target,
        horizon_years=3,
        start_calendar_year=2026,
        own_down_payment=own_down_payment,
        loan_annual_interest_rate=loan_rate,
        loan_tenure_months=tenure_months,
        available_monthly_surplus=surplus,
    )

    # Loan principal = 20L - 5L = 15 Lakh
    assert fin_res.financing_amount.amount == Decimal("1500000.00")
    # EMI for 15L @ 9% for 5 years is approx 31,138
    assert fin_res.monthly_emi.amount < Decimal("32000.00")
    assert fin_res.monthly_emi.amount > Decimal("30000.00")
    # Since EMI ~31.1k <= Surplus 40k, it is affordable!
    assert fin_res.emi_affordable_within_surplus is True
    assert fin_res.is_fully_funded is True

    # 2. Build Self Money Path for comparison
    self_res = build_self_money_path(
        goal_id="goal-vehicle-1",
        goal_target_amount=target,
        horizon_years=3,
        start_calendar_year=2026,
        initial_allocated_assets=own_down_payment,
        required_monthly_sip=Money.from_amount("35000.00"),
        expected_annual_return=Rate.from_percentage("10.0"),
    )

    # 3. Compare Both Paths Side-by-Side (§11.7)
    comparison = compare_funding_paths(self_res, fin_res)

    assert comparison.goal_id == "goal-vehicle-1"
    assert comparison.financing_cost_drag == fin_res.total_interest_cost
    assert "Own Capital Outflow" in comparison.trade_off_summary
    assert "Compounding & Residual Wealth" in comparison.trade_off_summary
    assert "The investor retains full authority" in comparison.investor_decision_prompt
