"""
domain/features/investor_profile/financial_state/readiness.py
Chapter 04 §4 Financial State Data Readiness.

Decision-specific readiness assessment:
Checks whether sufficient dated evidence exists for downstream features
(Budgeting, Goal Planning, Strategy Builder) without inventing arbitrary readiness scores.
"""

from dataclasses import dataclass
from typing import List
from app.domain.shared.value_objects import CalendarMonth
from app.domain.features.investor_profile.financial_state.models import FinancialStateSnapshot


@dataclass(frozen=True)
class DataReadinessReport:
    """Decision-specific readiness findings."""
    has_verified_income: bool
    has_verified_expenses: bool
    has_debt_evidence: bool
    missing_inputs_for_goal_planning: List[str]
    missing_inputs_for_strategy_builder: List[str]
    is_ready_for_goal_feasibility: bool


def assess_data_readiness(
    snapshot: FinancialStateSnapshot,
    target_period: CalendarMonth,
) -> DataReadinessReport:
    """Evaluates readiness for planning decisions based on available evidence."""
    has_inc = any(inc.period == target_period for inc in snapshot.incomes)
    has_exp = any(exp.period == target_period for exp in snapshot.expenses)
    has_debts = len(snapshot.liabilities) > 0

    missing_goal_inputs: List[str] = []
    if not has_inc:
        missing_goal_inputs.append("Missing verified income for period.")
    if not has_exp:
        missing_goal_inputs.append("Missing expense records for period.")

    missing_strategy_inputs: List[str] = list(missing_goal_inputs)
    if not snapshot.assets:
        missing_strategy_inputs.append("No asset holdings recorded for asset allocation or funding.")

    ready = (has_inc and has_exp)

    return DataReadinessReport(
        has_verified_income=has_inc,
        has_verified_expenses=has_exp,
        has_debt_evidence=has_debts,
        missing_inputs_for_goal_planning=missing_goal_inputs,
        missing_inputs_for_strategy_builder=missing_strategy_inputs,
        is_ready_for_goal_feasibility=ready,
    )
