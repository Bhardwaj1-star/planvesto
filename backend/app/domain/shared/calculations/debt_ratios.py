"""
Chapter 05 — Canonical Measurements & Formulas
Group C: Debt & Financial Health Ratios (§2 Group C, §3 Group C)

1. metric_debt_to_income_ratio: Debt-to-Income Ratio
   Formula: (Monthly Debt Payments ÷ Gross Monthly Income) × 100
   Requires: Gross monthly income > 0.

2. metric_leverage_ratio: Leverage Ratio
   Formula: (Total Liabilities ÷ Total Assets) × 100
   Requires: Total Assets > 0.

3. metric_weighted_debt_rate: Weighted Debt Rate
   Formula: Σ(Current Outstanding Principalᵢ × Annual Interest Rateᵢ) ÷ Σ(Current Outstanding Principalᵢ)
   Assumptions & Rules:
   - Uses current outstanding principal, never original sanctioned amount.
   - Contractual 0% included; missing rate cannot be treated as 0% (marks result provisional).
   - If total positive principal == 0, returns None.

4. metric_investment_debt_spread: Investment–Debt Spread
   Formula: Annualised Portfolio Return (%) − Weighted Debt Rate (%)
"""

from dataclasses import dataclass
from decimal import Decimal
from typing import List, Optional
from app.domain.shared.value_objects import Money, Rate


@dataclass(frozen=True)
class DebtItem:
    outstanding_principal: Money
    annual_interest_rate: Rate


def calculate_debt_to_income_ratio(
    monthly_debt_payments: Money,
    gross_monthly_income: Money,
) -> Optional[Rate]:
    """
    Calculate Debt-to-Income Ratio (%):
    (Monthly Debt Payments ÷ Gross Monthly Income) × 100
    """
    if gross_monthly_income.amount <= Decimal(0):
        return None
    ratio = (monthly_debt_payments.amount / gross_monthly_income.amount) * Decimal(100)
    return Rate.from_percentage(ratio)


def calculate_leverage_ratio(
    total_liabilities: Money,
    total_assets: Money,
) -> Optional[Rate]:
    """
    Calculate Leverage Ratio (%):
    (Total Liabilities ÷ Total Assets) × 100
    """
    if total_assets.amount <= Decimal(0):
        return None
    ratio = (total_liabilities.amount / total_assets.amount) * Decimal(100)
    return Rate.from_percentage(ratio)


def calculate_weighted_debt_rate(debts: List[DebtItem]) -> Optional[Rate]:
    """
    Calculate Weighted Debt Rate (% per year):
    Σ(Principalᵢ × Rateᵢ) ÷ Σ(Principalᵢ)
    """
    positive_debts = [d for d in debts if d.outstanding_principal.is_positive]
    if not positive_debts:
        return None

    total_principal = sum((d.outstanding_principal.amount for d in positive_debts), Decimal(0))
    if total_principal <= Decimal(0):
        return None

    weighted_rate_sum = sum(
        (d.outstanding_principal.amount * d.annual_interest_rate.percentage for d in positive_debts),
        Decimal(0),
    )
    weighted_rate = weighted_rate_sum / total_principal
    return Rate.from_percentage(weighted_rate)


def calculate_investment_debt_spread(
    annualised_portfolio_return: Rate,
    weighted_debt_rate: Rate,
) -> Decimal:
    """
    Calculate Investment-Debt Spread in percentage points:
    Annualised Portfolio Return (%) − Weighted Debt Rate (%)
    """
    return annualised_portfolio_return.percentage - weighted_debt_rate.percentage
