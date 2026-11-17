"""
domain/features/strategy_builder/payment_withdrawal.py
Chapter 11 — Strategy Builder Step 5: Payment & Withdrawal Execution Planning (§11.4).

Matching goal payment dates/amounts to available funds.
Assesses net liquidation proceeds, exit loads, taxes where applicable, and remaining assets.
Non-negotiable invariants:
- No automatic sale, withdrawal, transfer or reallocation without explicit investor approval.
"""

from dataclasses import dataclass
from datetime import date
from typing import List, Optional
from app.domain.shared.value_objects import Money


@dataclass(frozen=True)
class WithdrawalSourceAssessment:
    """Assessment of candidate assets/funds earmarked for goal payout."""
    asset_id: str
    asset_name: str
    target_withdrawal_date: date
    gross_withdrawal_amount: Money
    estimated_tax_or_exit_charge: Money
    net_proceeds: Money
    remaining_asset_value: Money
    lock_in_satisfied: bool
    investor_approval_required: bool = True


@dataclass(frozen=True)
class GoalPaymentPlan:
    """Coordinated payment plan for settling the goal obligation on due date."""
    goal_id: str
    target_date: date
    required_payment_amount: Money
    planned_sources: List[WithdrawalSourceAssessment]
    total_net_proceeds: Money
    shortfall_if_any: Money
    is_fully_covered: bool
