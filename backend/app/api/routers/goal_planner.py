"""
api/routers/goal_planner.py
FastAPI router for Goal Planner endpoints.
"""

from datetime import date
from decimal import Decimal
from typing import List, Optional
import uuid
from fastapi import APIRouter, Depends, Header, HTTPException, Query

from app.api.dependencies import get_current_user_id
from app.api.schemas.goal_planner import (
    GoalCalculateRequest,
    GoalCreateRequest,
    GoalSummaryResponse,
    DefinedGoalResponse,
)
from app.domain.canonical.goal_taxonomy import CanonicalGoalId
from app.domain.shared.value_objects import Money, Rate
from app.domain.features.goal_planner.requirement import (
    GoalInstance,
    plan_goal_requirement,
)
from app.domain.features.goal_planner.feasibility import (
    evaluate_fund_feasibility,
)
from app.domain.features.investor_profile.financial_state import AssetRecord

router = APIRouter(tags=["Goal Planner"])


def _build_goal_instance(req: GoalCalculateRequest, goal_id: str, investor_id: str) -> GoalInstance:
    # Resolve canonical goal ID safely
    cid = CanonicalGoalId.OTHERS
    for c in CanonicalGoalId:
        if c.value == req.canonical_id:
            cid = c
            break

    target_date = date(req.target_year, req.target_month, 1)
    as_of = date.today()

    mapped_assets: List[AssetRecord] = []
    for m in req.asset_mappings:
        mapped_assets.append(
            AssetRecord(
                id=m.asset_id,
                name=m.asset_name,
                category=None,
                current_value=Money.from_amount(m.current_value),
                as_of_date=as_of,
                ownership_percentage=Rate.from_percentage(m.allocation_percentage),
                expected_annual_return=Rate.from_percentage(m.expected_annual_return_pct),
            )
        )

    return GoalInstance(
        id=goal_id,
        investor_id=investor_id,
        canonical_id=cid,
        name=req.goal_name,
        target_date=target_date,
        current_cost=Money.from_amount(req.today_cost),
        applicable_inflation_rate=Rate.from_percentage(req.inflation_rate_pct),
        expected_annual_return=Rate.from_percentage(req.expected_return_pct),
        created_at=as_of,
        mapped_assets=mapped_assets,
    )


@router.post("/calculate", response_model=DefinedGoalResponse)
@router.post("/api/goals/calculate", response_model=DefinedGoalResponse, include_in_schema=False)
def calculate_goal_preview(
    request: GoalCalculateRequest,
    user_id: str = Depends(get_current_user_id),
):
    """Calculates goal requirement and fund feasibility preview using Chapter 10 domain logic."""
    temp_id = f"goal_{uuid.uuid4().hex[:8]}"
    goal = _build_goal_instance(request, temp_id, user_id)
    as_of = date.today()

    surplus = Money.from_amount(request.available_monthly_surplus)
    feasibility = evaluate_fund_feasibility(goal, as_of, surplus)

    return DefinedGoalResponse(
        goal_id=temp_id,
        goal_name=request.goal_name,
        today_cost=request.today_cost,
        future_target=feasibility.future_goal_target.amount,
        funding_gap=feasibility.remaining_funding_gap.amount,
        projected_mapped_asset_value=feasibility.projected_existing_funding.amount,
        required_monthly_sip=feasibility.required_monthly_sip.amount if feasibility.required_monthly_sip else Decimal(0),
        available_monthly_surplus=feasibility.available_monthly_surplus.amount,
        surplus_gap=feasibility.surplus_gap.amount if feasibility.surplus_gap else Decimal(0),
        required_surplus_increase_pct=feasibility.required_surplus_increase_pct.percentage if feasibility.required_surplus_increase_pct else None,
        is_feasible_under_current_conditions=feasibility.is_feasible_under_current_conditions,
        explanation=feasibility.explanation,
    )


@router.post("", response_model=DefinedGoalResponse)
@router.post("/api/goals", response_model=DefinedGoalResponse, include_in_schema=False)
def save_goal(
    request: GoalCreateRequest,
    user_id: str = Depends(get_current_user_id),
):
    """Saves and defines a goal using Chapter 10 domain evaluation."""
    goal_id = request.goal_id or f"goal_{uuid.uuid4().hex[:8]}"
    goal = _build_goal_instance(request, goal_id, user_id)
    as_of = date.today()

    surplus = Money.from_amount(request.available_monthly_surplus)
    feasibility = evaluate_fund_feasibility(goal, as_of, surplus)

    return DefinedGoalResponse(
        goal_id=goal_id,
        goal_name=request.goal_name,
        today_cost=request.today_cost,
        future_target=feasibility.future_goal_target.amount,
        funding_gap=feasibility.remaining_funding_gap.amount,
        projected_mapped_asset_value=feasibility.projected_existing_funding.amount,
        required_monthly_sip=feasibility.required_monthly_sip.amount if feasibility.required_monthly_sip else Decimal(0),
        available_monthly_surplus=feasibility.available_monthly_surplus.amount,
        surplus_gap=feasibility.surplus_gap.amount if feasibility.surplus_gap else Decimal(0),
        required_surplus_increase_pct=feasibility.required_surplus_increase_pct.percentage if feasibility.required_surplus_increase_pct else None,
        is_feasible_under_current_conditions=feasibility.is_feasible_under_current_conditions,
        explanation=feasibility.explanation,
    )
