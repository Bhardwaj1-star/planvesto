"""
api/schemas/goal_planner.py
Transport schemas for Goal Planner operations.
"""

from decimal import Decimal
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class AssetMappingInput(BaseModel):
    asset_id: str
    asset_name: Optional[str] = "Asset"
    current_value: Decimal = Decimal("0.0")
    allocation_type: Optional[str] = "percentage"
    allocation_value: Optional[Decimal] = Decimal("100.0")
    allocation_percentage: Optional[Decimal] = Decimal("100.0")
    expected_return: Optional[Decimal] = None
    expected_annual_return_pct: Optional[Decimal] = Decimal("10.0")
    return_frequency: Optional[str] = "annual"


class GoalCalculateRequest(BaseModel):
    planning_unit_id: str
    goal_id: Optional[str] = None
    investor_id: Optional[str] = None
    goal_name: str
    goal_type: Optional[str] = None
    canonical_id: Optional[str] = None
    today_cost: Decimal = Field(..., gt=0)
    target_year: int
    target_month: int = 1
    inflation_rate: Optional[Decimal] = None
    inflation_rate_pct: Optional[Decimal] = None
    expected_return_pct: Decimal = Decimal("10.0")
    priority: Optional[Any] = "high"
    flexibility: str = "Flexible"
    status: str = "Active"
    asset_mappings: List[AssetMappingInput] = Field(default_factory=list)
    dynamic_details: Optional[Dict[str, Any]] = Field(default_factory=dict)


class GoalCreateRequest(GoalCalculateRequest):
    pass


class GoalSummaryResponse(BaseModel):
    goal_id: str
    planning_unit_id: str
    goal_name: str
    target_amount: Decimal
    target_date: str
    priority: Any = 1
    flexibility: str = "Flexible"


class DefinedGoalResponse(BaseModel):
    goal_id: str
    defined_goal_id: Optional[str] = None
    planning_unit_id: Optional[str] = None
    goal_name: str
    goal_type: Optional[str] = "others"
    version: int = 1
    is_latest: bool = True
    today_cost: Decimal
    future_target: Decimal
    funding_gap: Decimal
    projected_mapped_asset_value: Decimal = Decimal("0.0")
    required_monthly_sip: Decimal = Decimal("0.0")
    required_monthly_contribution: Decimal = Decimal("0.0")
    available_monthly_surplus: Optional[Decimal] = None
    additional_required_monthly_sip: Decimal = Decimal("0.0")
    surplus_gap: Optional[Decimal] = None
    required_surplus_increase_pct: Optional[Decimal] = None
    fund_feasibility_case: Optional[str] = None
    feasibility_reason: Optional[str] = None
    feasibility_source: Optional[str] = None
    existing_goal_sip_monthly: Decimal = Decimal("0.0")
    is_feasible_under_current_conditions: bool = True
    feasibility_status: str = "feasible"
    funding_status: str = "Shortfall"
    duration_years: Decimal = Decimal("5.0")
    target_month: int = 1
    target_year: int = 2030
    inflation_rate: Decimal = Decimal("6.0")
    flexibility: str = "Flexible"
    status: str = "Active"
    priority: Any = "Important"
    explanation: str = "Goal requirement calculated successfully"
    version_metadata: Dict[str, Any] = Field(default_factory=dict)
    mapped_assets: List[Dict[str, Any]] = Field(default_factory=list)
