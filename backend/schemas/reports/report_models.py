"""Canonical Report Models.

All 4 report scopes share canonical summary models and schemas.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class VariantSummary(BaseModel):
    variant_id: str
    name: str
    description: str
    variant_type: str = "execution"
    strategy_id: Optional[str] = None


class GoalSummaryItem(BaseModel):
    id: str
    name: str
    goal_type: Optional[str] = None
    target_amount: float = 0.0
    currency: str = "INR"
    horizon_years: float = 0.0
    current_funding: float = 0.0
    funding_gap: float = 0.0
    feasibility: str = "feasible"
    required_contribution: Optional[float] = None
    allocated_contribution: Optional[float] = None
    shortfall: Optional[float] = None
    priority_rank: Optional[int] = None
    strategy_id: Optional[str] = None
    strategy_name: Optional[str] = None
    variant: Optional[VariantSummary] = None


class ConstraintReportSummary(BaseModel):
    rule_id: str
    rule_name: str
    category: str = "general"
    status: str = "pass"
    current_value: Optional[Any] = None
    target_threshold: Optional[Any] = None
    reason: Optional[str] = None
    corrective_action: Optional[str] = None


class CashFlowProjectionItem(BaseModel):
    year_index: int
    year: int
    opening_balance: float = 0.0
    annual_investment: float = 0.0
    growth: float = 0.0
    outflow: float = 0.0
    closing_balance: float = 0.0
    maturing_goals: Optional[str] = None


class ProductBucketReportItem(BaseModel):
    bucket: str
    instruments: str
    allocation: str
    strategic_rule: str


class ActionReportItem(BaseModel):
    timeline: str
    action: str
    owner: str = "Investor / Advisor"
    milestone: str


class ContingencyReportItem(BaseModel):
    risk_event: str
    immediate_action: str
    planning_change: str
    what_not_to_do: str


class GoalDecisionReportModel(BaseModel):
    report_type: str = "goal_decision_report"
    report_version: str = "1.0"
    goal: Dict[str, Any]
    financial_state: Dict[str, Any]
    goal_calculation: Dict[str, Any]
    feasibility: Dict[str, Any]
    strategy: Dict[str, Any]
    recommendation: Dict[str, Any]
    variant: Optional[VariantSummary] = None
    alternatives: List[Dict[str, Any]] = Field(default_factory=list)
    scenarios: List[Dict[str, Any]] = Field(default_factory=list)
    what_if_analysis: List[Dict[str, Any]] = Field(default_factory=list)
    trade_off_analysis: List[Dict[str, Any]] = Field(default_factory=list)
    technique_execution: List[Dict[str, Any]] = Field(default_factory=list)
    cash_flow_trajectory: List[Dict[str, Any]] = Field(default_factory=list)
    product_architecture: List[Dict[str, Any]] = Field(default_factory=list)
    contribution_rules: List[str] = Field(default_factory=list)
    action_plan_timeline: List[Dict[str, Any]] = Field(default_factory=list)
    contingency_matrix: List[Dict[str, Any]] = Field(default_factory=list)
    decision: Dict[str, Any]
    provenance: Dict[str, Any]


class BasketReportModel(BaseModel):
    report_type: str = "goal_basket_report"
    report_version: str = "1.0"
    basket: Dict[str, Any]
    summary: Dict[str, Any]
    goals: List[Dict[str, Any]]
    financial_state: Dict[str, Any]
    priority_ladder: List[Dict[str, Any]]
    shared_pool_allocation: Dict[str, Any]
    consolidated_cash_flow: List[Dict[str, Any]]
    bucket_architecture: List[Dict[str, Any]]
    action_plan_timeline: List[Dict[str, Any]]
    contingency_matrix: List[Dict[str, Any]]


class CompleteFinancialPlanReportModel(BaseModel):
    report_type: str = "complete_financial_plan"
    report_version: str = "1.0"
    planning_unit_id: str
    goals: List[Dict[str, Any]]
    financial_state: Dict[str, Any]
    consolidated_funding: Dict[str, Any]
    summary: Dict[str, Any]
    resource_allocation: Dict[str, Any]
    goal_plans: List[Dict[str, Any]]
    family_cash_flow_trajectory: List[Dict[str, Any]]
    moneywheel_health_scan: List[Dict[str, Any]]
    ratio_constraints: List[Dict[str, Any]]
    contingency_matrix: List[Dict[str, Any]]
    governance_protocol: List[Dict[str, Any]]


class SummaryReportModel(BaseModel):
    report_type: str = "summary_planning_report"
    report_version: str = "1.0"
    planning_unit_id: str
    financial_snapshot: Dict[str, Any]
    goals: List[GoalSummaryItem]
    observations: List[Dict[str, Any]]
    actions: List[Dict[str, Any]]
    investment_allocation: Optional[Dict[str, Any]] = None
    risk_profile: Optional[Dict[str, Any]] = None
    provenance: Optional[Dict[str, Any]] = None
