"""
Unit tests for Chapter 05 canonical financial calculations.
"""

from decimal import Decimal
from app.domain.shared.value_objects import Money, Rate
from app.domain.shared.calculations import (
    calculate_net_worth,
    calculate_monthly_surplus,
    calculate_savings_rate,
    calculate_monthly_spending_variance,
    DebtItem,
    calculate_debt_to_income_ratio,
    calculate_leverage_ratio,
    calculate_weighted_debt_rate,
    calculate_investment_debt_spread,
    calculate_liquid_asset_ratio,
    calculate_financial_asset_ratio,
    calculate_portfolio_concentration,
    calculate_future_goal_target,
    calculate_goal_funding_gap,
    calculate_goal_funding_ratio,
    calculate_required_monthly_contribution,
    calculate_monthly_sip_surplus_gap,
    calculate_required_surplus_increase,
    calculate_risk_required_return,
)


def test_net_worth():
    assets = Money.from_amount("1000000.00")
    liabilities = Money.from_amount("400000.00")
    nw = calculate_net_worth(assets, liabilities)
    assert nw.amount == Decimal("600000.00")


def test_cash_flow_surplus_and_savings_rate():
    income = Money.from_amount("100000.00")
    expenses = Money.from_amount("50000.00")
    savings = Money.from_amount("20000.00")

    surplus = calculate_monthly_surplus(income, expenses, savings)
    assert surplus.amount == Decimal("30000.00")

    savings_rate = calculate_savings_rate(savings, income)
    assert savings_rate is not None
    assert savings_rate.percentage == Decimal("20.00")

    # Variance: actual spending 55,000 against budget 50,000 -> +5,000 (over budget)
    variance = calculate_monthly_spending_variance(Money.from_amount("55000.00"), Money.from_amount("50000.00"))
    assert variance.amount == Decimal("5000.00")


def test_debt_ratios():
    gross_income = Money.from_amount("100000.00")
    debt_payments = Money.from_amount("30000.00")
    dti = calculate_debt_to_income_ratio(debt_payments, gross_income)
    assert dti is not None
    assert dti.percentage == Decimal("30.00")

    # Weighted debt rate
    debts = [
        DebtItem(outstanding_principal=Money.from_amount("500000.00"), annual_interest_rate=Rate.from_percentage("8.5")),
        DebtItem(outstanding_principal=Money.from_amount("100000.00"), annual_interest_rate=Rate.from_percentage("14.0")),
    ]
    # Total principal = 600,000. (500k * 8.5 + 100k * 14.0) / 600k = (4250k + 1400k) / 600k = 5650 / 600 ≈ 9.4166667%
    w_rate = calculate_weighted_debt_rate(debts)
    assert w_rate is not None
    assert round(w_rate.percentage, 2) == Decimal("9.42")


def test_goal_funding_calculations():
    # Today cost = 10,00,000, 6% inflation, 5 years
    current_cost = Money.from_amount("1000000.00")
    inflation = Rate.from_percentage("6.0")
    future_target = calculate_future_goal_target(current_cost, inflation, 5)
    # 10,00,000 * (1.06)^5 = 10,00,000 * 1.3382255776 = 13,38,225.58
    assert future_target.amount == Decimal("1338225.58")

    # Mapped projected assets = 3,38,225.58 -> Gap = 10,00,000.00
    projected_assets = Money.from_amount("338225.58")
    gap = calculate_goal_funding_gap(future_target, projected_assets)
    assert gap.amount == Decimal("1000000.00")

    # Required monthly contribution for 10 Lakh gap over 60 months at 12% annual return
    ret = Rate.from_percentage("12.0")
    req_sip = calculate_required_monthly_contribution(gap, 60, ret)
    assert req_sip is not None
    # Monthly contribution should be around ~12,400 to 12,600
    assert req_sip.amount > Decimal("12000.00")
    assert req_sip.amount < Decimal("13000.00")

    # Surplus gap: Required SIP is ~12,500, Available Surplus is 10,000 -> Gap is ~2,500
    surplus = Money.from_amount("10000.00")
    sip_gap = calculate_monthly_sip_surplus_gap(req_sip, surplus)
    assert sip_gap.is_positive
    surplus_increase = calculate_required_surplus_increase(sip_gap, surplus)
    assert surplus_increase is not None
    assert surplus_increase.percentage > Decimal("20.00")
