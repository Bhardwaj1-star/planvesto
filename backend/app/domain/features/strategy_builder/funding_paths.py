"""
domain/features/strategy_builder/funding_paths.py
Chapter 11 — The Two Top-Level Goal Funding Strategy Paths (§11.1).

1. Self Money — use eligible own funds, assets and goal-linked SIPs.
2. Self Money + Financing — combine own resources with a financing option.
"""

from dataclasses import dataclass
from enum import Enum
from typing import List
from app.domain.shared.value_objects import Money, Rate


class FundingPathType(str, Enum):
    SELF_MONEY = "self_money"
    SELF_MONEY_PLUS_FINANCING = "self_money_plus_financing"


@dataclass(frozen=True)
class YearlyProjectionRow:
    """Year-by-year goal funding projection row (§11.4 Step 4, §11.5)."""
    year_index: int
    calendar_year: int
    opening_balance: Money
    annual_contributions: Money
    investment_growth: Money
    financing_disbursement: Money
    annual_debt_repayment: Money
    goal_withdrawal: Money
    closing_balance: Money


@dataclass(frozen=True)
class SelfMoneyPathResult:
    """Outcome of Self Money Funding Path evaluation (§11.1, §11.4)."""
    goal_id: str
    total_own_money_contributed: Money
    projected_corpus_at_goal_date: Money
    goal_target_amount: Money
    goal_amount_funded: Money
    remaining_corpus_after_goal: Money
    yearly_projections: List[YearlyProjectionRow]
    is_fully_funded: bool
    explanation: str


@dataclass(frozen=True)
class FinancingPathResult:
    """Outcome of Self Money + Financing Funding Path evaluation (§11.1, §11.6)."""
    goal_id: str
    own_down_payment: Money
    total_own_contributions: Money
    total_own_money_outflow: Money  # down payment + own contributions + total repayments
    financing_amount: Money         # loan principal
    loan_interest_rate: Rate
    loan_tenure_months: int
    monthly_emi: Money
    total_interest_cost: Money
    total_repayment_amount: Money   # principal + interest
    emi_affordable_within_surplus: bool
    projected_corpus_at_goal_date: Money
    goal_target_amount: Money
    goal_amount_funded: Money
    remaining_corpus_after_goal: Money
    yearly_projections: List[YearlyProjectionRow]
    is_fully_funded: bool
    explanation: str
