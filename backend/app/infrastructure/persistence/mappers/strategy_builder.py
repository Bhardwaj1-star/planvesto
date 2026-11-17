"""
infrastructure/persistence/mappers/strategy_builder.py
Bi-directional translation for Strategy Builder results and database records.
"""

from decimal import Decimal
from typing import Any, Dict, List, Optional
from app.domain.features.strategy_builder.funding_paths import (
    FinancingPathResult,
    SelfMoneyPathResult,
    YearlyProjectionRow,
)
from app.domain.features.strategy_builder.comparison import StrategyComparisonMatrix
from app.domain.shared.value_objects import Money, Rate


def map_yearly_row_to_dict(row: YearlyProjectionRow) -> Dict[str, Any]:
    return {
        "year_index": row.year_index,
        "calendar_year": row.calendar_year,
        "opening_balance": str(row.opening_balance.amount),
        "annual_contributions": str(row.annual_contributions.amount),
        "investment_growth": str(row.investment_growth.amount),
        "financing_disbursement": str(row.financing_disbursement.amount),
        "annual_debt_repayment": str(row.annual_debt_repayment.amount),
        "goal_withdrawal": str(row.goal_withdrawal.amount),
        "closing_balance": str(row.closing_balance.amount),
    }


def map_self_money_path_to_dict(result: SelfMoneyPathResult) -> Dict[str, Any]:
    return {
        "path_type": "self_money",
        "goal_id": result.goal_id,
        "total_own_money_contributed": str(result.total_own_money_contributed.amount),
        "projected_corpus_at_goal_date": str(result.projected_corpus_at_goal_date.amount),
        "goal_target_amount": str(result.goal_target_amount.amount),
        "goal_amount_funded": str(result.goal_amount_funded.amount),
        "remaining_corpus_after_goal": str(result.remaining_corpus_after_goal.amount),
        "is_fully_funded": result.is_fully_funded,
        "explanation": result.explanation,
        "yearly_projections": [map_yearly_row_to_dict(r) for r in result.yearly_projections],
    }


def map_financing_path_to_dict(result: FinancingPathResult) -> Dict[str, Any]:
    return {
        "path_type": "self_money_plus_financing",
        "goal_id": result.goal_id,
        "own_money_portion": str(result.own_money_portion.amount),
        "loan_principal_borrowed": str(result.loan_principal_borrowed.amount),
        "annual_interest_rate": str(result.annual_interest_rate.percentage),
        "loan_tenure_months": result.loan_tenure_months,
        "monthly_emi": str(result.monthly_emi.amount),
        "total_interest_payable": str(result.total_interest_payable.amount),
        "total_loan_repayment": str(result.total_loan_repayment.amount),
        "is_viable": result.is_viable,
        "explanation": result.explanation,
        "yearly_projections": [map_yearly_row_to_dict(r) for r in result.yearly_projections],
    }


def map_funding_comparison_to_dict(result: StrategyComparisonMatrix) -> Dict[str, Any]:
    return {
        "goal_id": result.goal_id,
        "self_money_path": map_self_money_path_to_dict(result.self_money_path),
        "financing_path": map_financing_path_to_dict(result.financing_path),
        "financing_cost_drag": str(result.financing_cost_drag.amount),
        "trade_off_summary": result.trade_off_summary,
        "investor_decision_prompt": result.investor_decision_prompt,
    }
