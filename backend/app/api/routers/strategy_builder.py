"""
api/routers/strategy_builder.py
FastAPI router for Strategy Builder / Goal Funding endpoints.
"""

from decimal import Decimal
from typing import List, Optional
from fastapi import APIRouter, Depends

from app.api.dependencies import get_current_user_id
from app.api.schemas.strategy_builder import (
    GoalFundingAssessmentRequest,
    GoalFundingAssessmentResponse,
    SelfMoneyPathResponse,
    FinancingPathResponse,
    ComparisonMatrixResponse,
    PathProjectionRowResponse,
)
from app.domain.shared.value_objects import Money, Rate
from app.domain.features.strategy_builder import (
    build_self_money_path,
    build_financing_path,
    compare_funding_paths,
)

router = APIRouter(tags=["Strategy Builder & Goal Funding"])


@router.post("/assess", response_model=GoalFundingAssessmentResponse)
@router.post("/api/goal-funding/assess", response_model=GoalFundingAssessmentResponse, include_in_schema=False)
def assess_goal_funding(
    request: GoalFundingAssessmentRequest,
    user_id: str = Depends(get_current_user_id),
):
    """Evaluates Self Money and optional Financing paths with side-by-side comparison."""
    target_amount = Money.from_amount(request.target_amount)
    initial_assets = Money.from_amount(request.initial_allocated_assets)
    sip = Money.from_amount(request.required_monthly_sip)
    exp_return = Rate.from_percentage(request.expected_annual_return_pct)
    surplus = Money.from_amount(request.available_monthly_surplus)

    # 1. Build Self Money Path
    self_res = build_self_money_path(
        goal_id=request.goal_id,
        goal_target_amount=target_amount,
        horizon_years=request.horizon_years,
        start_calendar_year=request.start_calendar_year,
        initial_allocated_assets=initial_assets,
        required_monthly_sip=sip,
        expected_annual_return=exp_return,
    )

    self_projections: List[PathProjectionRowResponse] = [
        PathProjectionRowResponse(
            year_index=r.year_index,
            calendar_year=r.calendar_year,
            opening_balance=r.opening_balance.amount,
            annual_contributions=r.annual_contributions.amount,
            investment_growth=r.investment_growth.amount,
            financing_disbursement=r.financing_disbursement.amount,
            annual_debt_repayment=r.annual_debt_repayment.amount,
            goal_withdrawal=r.goal_withdrawal.amount,
            closing_balance=r.closing_balance.amount,
        )
        for r in self_res.yearly_projections
    ]

    self_resp = SelfMoneyPathResponse(
        goal_id=request.goal_id,
        total_own_contributions=self_res.total_own_money_contributed.amount,
        projected_corpus_at_goal=self_res.projected_corpus_at_goal_date.amount,
        goal_amount_funded=self_res.goal_amount_funded.amount,
        remaining_corpus=self_res.remaining_corpus_after_goal.amount,
        is_fully_funded=self_res.is_fully_funded,
        explanation=self_res.explanation,
        yearly_projections=self_projections,
    )

    fin_resp: Optional[FinancingPathResponse] = None
    comp_resp: Optional[ComparisonMatrixResponse] = None

    if request.financing_option is not None:
        down_payment = Money.from_amount(request.financing_option.down_payment)
        loan_rate = Rate.from_percentage(request.financing_option.loan_annual_interest_rate_pct)

        fin_res = build_financing_path(
            goal_id=request.goal_id,
            goal_target_amount=target_amount,
            horizon_years=request.horizon_years,
            start_calendar_year=request.start_calendar_year,
            own_down_payment=down_payment,
            loan_annual_interest_rate=loan_rate,
            loan_tenure_months=request.financing_option.loan_tenure_months,
            available_monthly_surplus=surplus,
            initial_allocated_assets=initial_assets,
            expected_annual_return=exp_return,
        )

        fin_projections: List[PathProjectionRowResponse] = [
            PathProjectionRowResponse(
                year_index=r.year_index,
                calendar_year=r.calendar_year,
                opening_balance=r.opening_balance.amount,
                annual_contributions=r.annual_contributions.amount,
                investment_growth=r.investment_growth.amount,
                financing_disbursement=r.financing_disbursement.amount,
                annual_debt_repayment=r.annual_debt_repayment.amount,
                goal_withdrawal=r.goal_withdrawal.amount,
                closing_balance=r.closing_balance.amount,
            )
            for r in fin_res.yearly_projections
        ]

        fin_resp = FinancingPathResponse(
            goal_id=request.goal_id,
            down_payment=fin_res.own_down_payment.amount,
            financing_amount=fin_res.financing_amount.amount,
            loan_interest_rate_pct=fin_res.loan_interest_rate.percentage,
            loan_tenure_months=fin_res.loan_tenure_months,
            monthly_emi=fin_res.monthly_emi.amount,
            total_interest_cost=fin_res.total_interest_cost.amount,
            total_repayment=fin_res.total_repayment_amount.amount,
            emi_affordable=fin_res.emi_affordable_within_surplus,
            is_fully_funded=fin_res.is_fully_funded,
            explanation=fin_res.explanation,
            yearly_projections=fin_projections,
        )

        comp_res = compare_funding_paths(self_res, fin_res)
        comp_resp = ComparisonMatrixResponse(
            goal_id=request.goal_id,
            own_money_outflow_difference=comp_res.own_money_outflow_difference.amount,
            financing_cost_drag=comp_res.financing_cost_drag.amount,
            remaining_corpus_difference=comp_res.remaining_corpus_difference.amount,
            trade_off_summary=comp_res.trade_off_summary,
            investor_decision_prompt=comp_res.investor_decision_prompt,
        )

    return GoalFundingAssessmentResponse(
        planning_unit_id=request.planning_unit_id,
        goal_id=request.goal_id,
        self_money_path=self_resp,
        financing_path=fin_resp,
        comparison_matrix=comp_resp,
    )
