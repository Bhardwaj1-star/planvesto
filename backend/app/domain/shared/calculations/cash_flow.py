"""
Chapter 05 — Canonical Measurements & Formulas
Group B: Monthly Cash Flow (§2 Group B, §3 Group B)

1. metric_monthly_surplus: Available Monthly Surplus
   Formula: Actual Net Monthly Income − Actual Monthly Expenses − Actual Monthly Savings and Investments
   Assumptions & Rules:
   - Same calendar month.
   - Negative result indicates a cash-flow shortfall.
   - EMI included exactly once under Expenses.
   - Own-account transfers excluded.

2. metric_savings_rate: Savings Ratio
   Formula: (Actual Monthly Savings and Investments ÷ Actual Net Monthly Income) × 100
   Assumptions & Rules:
   - Requires positive net monthly income. Returns None (N/A) if income <= 0.

3. metric_monthly_variance: Monthly Spending Variance
   Formula: Actual Monthly Spending − Budgeted Monthly Spending Limit
   Assumptions & Rules:
   - Positive = over budget, negative = under budget.
   - Zero budget is valid: variance equals actual spending.
"""

from decimal import Decimal
from typing import Optional
from app.domain.shared.value_objects import Money, Rate


def calculate_monthly_surplus(
    net_monthly_income: Money,
    monthly_expenses: Money,
    monthly_savings_investments: Money,
) -> Money:
    """
    Calculate Available Monthly Surplus:
    Actual Net Monthly Income − Actual Monthly Expenses − Actual Monthly Savings and Investments
    """
    return net_monthly_income - monthly_expenses - monthly_savings_investments


def calculate_savings_rate(
    monthly_savings_investments: Money,
    net_monthly_income: Money,
) -> Optional[Rate]:
    """
    Calculate Savings Ratio (%):
    (Actual Monthly Savings and Investments ÷ Actual Net Monthly Income) × 100
    Returns None if net_monthly_income is zero or negative.
    """
    if net_monthly_income.amount <= Decimal(0):
        return None

    savings_ratio = (monthly_savings_investments.amount / net_monthly_income.amount) * Decimal(100)
    return Rate.from_percentage(savings_ratio)


def calculate_monthly_spending_variance(
    actual_spending: Money,
    budgeted_limit: Money,
) -> Money:
    """
    Calculate Monthly Spending Variance:
    Actual Monthly Spending − Budgeted Monthly Spending Limit
    Positive means over budget, negative means under budget.
    """
    return actual_spending - budgeted_limit
