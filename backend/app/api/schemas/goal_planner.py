"""
api/schemas/goal_planner.py
Transport schemas for Goal Planner operations.
"""

from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, Field


class AssetMappingInput(BaseModel):
    asset_id: str
    asset_name: str
    current_value: Decimal
    allocation_percentage: Decimal = Decimal("100.0")
    expected_annual_return_pct: Decimal = Decimal("10.0")


class GoalCalculateRequest(BaseModel):
    planning_unit_id: str
    goal_name: str
    canonical_id: str = "goal_education"
    today_cost: Decimal = Field(..., gt=0)
    target_year: int
    target_month: int = 1
    inflation_rate_pct: Decimal = Decimal("6.0")
    expected_return_pct: Decimal = Decimal("10.0")
    available_monthly_surplus: Decimal = Decimal("0.0")
    asset_mappings: List[AssetMappingInput] = Field(default_factory=list)


class GoalCreateRequest(GoalCalculateRequest):
    goal_id: Optional[str] = None
    priority: int = 1
    flexibility: str = "Flexible"


class GoalSummaryResponse(BaseModel):
    goal_id: str
    planning_unit_id: str
    goal_name: str
    target_amount: Decimal
    target_date: str
    priority: int = 1
    flexibility: str = "Flexible"


class DefinedGoalResponse(BaseModel):
    goal_id: str
    goal_name: str
    today_cost: Decimal
    future_target: Decimal
    funding_gap: Decimal
    projected_mapped_asset_value: Decimal
    required_monthly_sip: Decimal
    available_monthly_surplus: Decimal
    surplus_gap: Decimal
    required_surplus_increase_pct: Optional[Decimal] = None
    is_feasible_under_current_conditions: bool
    explanation: str
