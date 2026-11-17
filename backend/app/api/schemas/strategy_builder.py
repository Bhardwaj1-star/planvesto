"""
api/schemas/strategy_builder.py
Transport schemas for Strategy Builder / Goal Funding endpoints.
"""

from decimal import Decimal
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class FinancingOptionInput(BaseModel):
    down_payment: Decimal = Decimal("0.0")
    loan_annual_interest_rate_pct: Decimal = Decimal("9.0")
    loan_tenure_months: int = 60


class GoalFundingAssessmentRequest(BaseModel):
    planning_unit_id: str
    goal_id: str
    target_amount: Decimal = Field(..., gt=0)
    horizon_years: int = Field(..., gt=0)
    start_calendar_year: int = 2026
    initial_allocated_assets: Decimal = Decimal("0.0")
    required_monthly_sip: Decimal = Decimal("0.0")
    expected_annual_return_pct: Decimal = Decimal("10.0")
    available_monthly_surplus: Decimal = Decimal("0.0")
    financing_option: Optional[FinancingOptionInput] = None


class PathProjectionRowResponse(BaseModel):
    year_index: int
    calendar_year: int
    opening_balance: Decimal
    annual_contributions: Decimal
    investment_growth: Decimal
    financing_disbursement: Decimal
    annual_debt_repayment: Decimal
    goal_withdrawal: Decimal
    closing_balance: Decimal


class SelfMoneyPathResponse(BaseModel):
    goal_id: str
    total_own_contributions: Decimal
    projected_corpus_at_goal: Decimal
    goal_amount_funded: Decimal
    remaining_corpus: Decimal
    is_fully_funded: bool
    explanation: str
    yearly_projections: List[PathProjectionRowResponse]


class FinancingPathResponse(BaseModel):
    goal_id: str
    down_payment: Decimal
    financing_amount: Decimal
    loan_interest_rate_pct: Decimal
    loan_tenure_months: int
    monthly_emi: Decimal
    total_interest_cost: Decimal
    total_repayment: Decimal
    emi_affordable: bool
    is_fully_funded: bool
    explanation: str
    yearly_projections: List[PathProjectionRowResponse]


class ComparisonMatrixResponse(BaseModel):
    goal_id: str
    own_money_outflow_difference: Decimal
    financing_cost_drag: Decimal
    remaining_corpus_difference: Decimal
    trade_off_summary: str
    investor_decision_prompt: str


class GoalFundingAssessmentResponse(BaseModel):
    planning_unit_id: str
    goal_id: str
    self_money_path: SelfMoneyPathResponse
    financing_path: Optional[FinancingPathResponse] = None
    comparison_matrix: Optional[ComparisonMatrixResponse] = None
