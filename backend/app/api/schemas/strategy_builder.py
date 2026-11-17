"""
api/schemas/strategy_builder.py
Transport schemas for Strategy Builder / Goal Funding endpoints.
"""

from decimal import Decimal
from typing import Any, Dict, List, Literal, Optional
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


# --- Frontend Strategy Journey Schemas ---

class InvestorPriorities(BaseModel):
    safety: float = 0.25
    liquidity: float = 0.25
    growth: float = 0.25
    flexibility: float = 0.25


class StrategyImplementationParamDef(BaseModel):
    name: str
    label: str
    param_type: Literal["currency", "percentage", "integer", "choice"]
    description: str
    default_value: Any
    editable: bool = True
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    choices: List[str] = Field(default_factory=list)


class StrategyDefinition(BaseModel):
    strategy_id: str
    name: str
    tagline: str
    description: str
    strategy_family: str = "General"
    strategic_objective: str = ""
    core_mechanism: str = ""
    principles: List[str] = Field(default_factory=list)
    constraints: List[str] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)
    required_inputs: List[str] = Field(default_factory=list)
    applicable_goal_characteristics: List[str] = Field(default_factory=list)
    applicable_goal_types: List[str] = Field(default_factory=list)
    technique_ids: List[str] = Field(default_factory=list)
    strategic_levers: List[str] = Field(default_factory=list)
    compatible_strategy_ids: List[str] = Field(default_factory=list)
    conflicting_strategy_ids: List[str] = Field(default_factory=list)
    library_version: str = "2.0"
    implementation_version: str = "2.0"
    active: bool = True
    implementation_parameters: List[StrategyImplementationParamDef] = Field(default_factory=list)
    good_outcomes: List[str] = Field(default_factory=list)
    bad_outcomes: List[str] = Field(default_factory=list)
    trade_offs: List[str] = Field(default_factory=list)
    baseline_safety_score: float = 7.0
    baseline_liquidity_score: float = 7.0
    baseline_growth_score: float = 7.0
    baseline_flexibility_score: float = 7.0


class StrategyArchitecture(BaseModel):
    architecture_id: str
    primary_strategy_id: str
    supporting_strategy_ids: List[str] = Field(default_factory=list)
    technique_ids: List[str] = Field(default_factory=list)
    rationale: List[str] = Field(default_factory=list)
    trade_offs: List[str] = Field(default_factory=list)
    feasibility_status: Literal["feasible", "conditional", "infeasible"] = "feasible"
    constraints: List[str] = Field(default_factory=list)


class Scenario(BaseModel):
    scenario_id: str
    strategy_id: str
    scenario_type: Literal["baseline", "modified", "custom"] = "baseline"
    scenario_name: str
    assumptions: Dict[str, Any] = Field(default_factory=dict)
    funding_structure: Dict[str, Any] = Field(default_factory=dict)
    metrics: Dict[str, Any] = Field(default_factory=dict)
    trade_off_notes: str = ""
    is_investor_modified: bool = False


class StrategyRankingItem(BaseModel):
    rank: int
    strategy_id: str
    scenario_id: str
    strategy_name: str
    scenario_name: str
    composite_score: float
    dimension_scores: Dict[str, float] = Field(default_factory=dict)
    is_recommended: bool = False
    evidence_scores: Optional[Dict[str, Any]] = None
    is_eligible: bool = True
    ineligible_reasons: List[str] = Field(default_factory=list)


class StrategyRecommendation(BaseModel):
    recommended_strategy_id: str
    recommended_scenario_id: str
    short_reasons: List[str] = Field(default_factory=list)
    complete_reasoning: str = ""
    architecture: Optional[StrategyArchitecture] = None
    alternative_architecture_ids: List[str] = Field(default_factory=list)
    feasibility_status: Literal["feasible", "conditional", "infeasible"] = "feasible"
    constraints: List[str] = Field(default_factory=list)


class StrategyRun(BaseModel):
    strategy_run_id: Optional[str] = None
    planning_unit_id: str
    goal_id: str
    defined_goal_id: str = "def_goal"
    defined_goal_version: int = 1
    run_version: int = 1
    is_latest: bool = True
    status: str = "completed"
    applicable_strategies: List[StrategyDefinition] = Field(default_factory=list)
    scenarios: List[Scenario] = Field(default_factory=list)
    investor_priorities: InvestorPriorities = Field(default_factory=InvestorPriorities)
    comparison_matrix: Dict[str, Any] = Field(default_factory=dict)
    rankings: List[StrategyRankingItem] = Field(default_factory=list)
    recommendation: StrategyRecommendation
    architectures: List[StrategyArchitecture] = Field(default_factory=list)
    selected_strategy_id: Optional[str] = None
    selected_scenario_id: Optional[str] = None
    selected_strategy_version_id: Optional[str] = None
    selected_strategy_version: Optional[int] = None
    selected_implementation_parameters: Dict[str, Any] = Field(default_factory=dict)
    selected_architecture: Optional[StrategyArchitecture] = None
    selection_timestamp: Optional[str] = None
    approval_status: Optional[str] = None
    run_metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: Optional[str] = None


class StrategyVersion(BaseModel):
    strategy_version_id: str
    planning_unit_id: str
    strategy_id: str
    version: int = 1
    parent_version: Optional[int] = None
    source: Literal["library", "investor_edit"] = "library"
    library_version: str = "2.0"
    implementation_version: str = "2.0"
    goal_id: Optional[str] = None
    defined_goal_id: Optional[str] = None
    defined_goal_version: Optional[int] = None
    architecture: Optional[StrategyArchitecture] = None
    decision_snapshot: Dict[str, Any] = Field(default_factory=dict)
    implementation_parameters: Dict[str, Any] = Field(default_factory=dict)
    status: str = "Active"
    source_strategy_run_id: Optional[str] = None
    created_at: str


class StrategyBuildRequest(BaseModel):
    planning_unit_id: str
    goal_id: str
    investor_priorities: Optional[InvestorPriorities] = None


class PriorityWeightsRequest(BaseModel):
    planning_unit_id: str
    strategy_run_id: str
    priorities: InvestorPriorities


class CustomScenarioRequest(BaseModel):
    planning_unit_id: str
    strategy_run_id: str
    strategy_id: str
    scenario_name: str
    assumptions: Dict[str, Any] = Field(default_factory=dict)
    funding_structure: Dict[str, Any] = Field(default_factory=dict)


class StrategySelectRequest(BaseModel):
    planning_unit_id: str
    strategy_run_id: str
    selected_strategy_id: str
    selected_scenario_id: str
    selected_implementation_parameters: Optional[Dict[str, Any]] = Field(default_factory=dict)
    selected_architecture_id: Optional[str] = None


class StrategyImplementationPreviewRequest(BaseModel):
    planning_unit_id: str
    strategy_run_id: str
    selected_strategy_id: str
    selected_scenario_id: str
    implementation_parameters: Dict[str, Any] = Field(default_factory=dict)
    assumptions: Dict[str, Any] = Field(default_factory=dict)
    funding_structure: Dict[str, Any] = Field(default_factory=dict)
    selected_architecture_id: Optional[str] = None


class StrategyImplementationFinalizeRequest(BaseModel):
    planning_unit_id: str
    strategy_run_id: str
    defined_goal_version: int = 1
    selected_strategy_id: str
    selected_scenario_id: str
    implementation_parameters: Dict[str, Any] = Field(default_factory=dict)
    assumptions: Dict[str, Any] = Field(default_factory=dict)
    funding_structure: Dict[str, Any] = Field(default_factory=dict)
    selected_architecture_id: Optional[str] = None


class StrategyEditRequest(BaseModel):
    planning_unit_id: str
    strategy_id: str
    parent_version: int
    implementation_parameters: Dict[str, Any] = Field(default_factory=dict)


class StrategyEditResult(BaseModel):
    strategy_id: str
    strategy_version_id: str
    strategy_version: int
    parent_version: int
    suitability_reassessment_required: bool = False
    approval_snapshot_required: bool = False
    primary_replacement_required: bool = False


class PrimaryStrategyResponse(BaseModel):
    planning_unit_id: str
    strategy_id: str
    strategy_version_id: str
    approval_snapshot_id: str = "snapshot_primary"
    status: str = "Active"
    previous_strategy_id: Optional[str] = None
    previous_strategy_version_id: Optional[str] = None
    pending_action_disposition: Optional[str] = None
    transition_metadata: Dict[str, Any] = Field(default_factory=dict)
    updated_at: str


class RetirementReportData(BaseModel):
    title: str = "Retirement Goal Funding Strategy Report"
    sections: List[Dict[str, Any]] = Field(default_factory=list)


class GoalStrategyReport(BaseModel):
    report_type: str = "goal_strategy_report"
    goal_id: Optional[str] = None
    goal_name: Optional[str] = None
    goal_type: Optional[str] = None
    goal: Optional[Dict[str, Any]] = None
    goal_details: Dict[str, Any] = Field(default_factory=dict)
    mapped_assets: List[Dict[str, Any]] = Field(default_factory=list)
    strategy_run_id: Optional[str] = None
    strategy_version_id: Optional[str] = None
    strategy: Dict[str, Any] = Field(default_factory=dict)
    recommendation: Dict[str, Any] = Field(default_factory=dict)
    selected_strategy_id: Optional[str] = None
    approval_status: Optional[str] = None
    goal_calculation: Dict[str, Any] = Field(default_factory=dict)
    financial_state: Dict[str, Any] = Field(default_factory=dict)
    cash_flow_trajectory: List[Dict[str, Any]] = Field(default_factory=list)
    product_architecture: List[Dict[str, Any]] = Field(default_factory=list)
    contribution_rules: List[Dict[str, Any]] = Field(default_factory=list)
    action_plan_timeline: List[Dict[str, Any]] = Field(default_factory=list)
    contingency_matrix: List[Dict[str, Any]] = Field(default_factory=list)


class ConsolidatedFinancialPlan(BaseModel):
    plan_id: Optional[str] = None
    planning_unit_id: str
    created_at: Optional[str] = None
    investor_priorities: Optional[InvestorPriorities] = None
    summary: Dict[str, Any] = Field(default_factory=dict)
    ratio_constraints: List[Dict[str, Any]] = Field(default_factory=list)
    resource_allocation: Dict[str, Any] = Field(default_factory=dict)
    goal_plans: List[Dict[str, Any]] = Field(default_factory=list)
    action_plan: Dict[str, Any] = Field(default_factory=dict)
    goals: List[Dict[str, Any]] = Field(default_factory=list)
    consolidated_funding: Optional[Dict[str, Any]] = None
    actions: List[Dict[str, Any]] = Field(default_factory=list)
    trade_offs: List[str] = Field(default_factory=list)
    audit_trail: List[Dict[str, Any]] = Field(default_factory=list)
    planning_notes: List[str] = Field(default_factory=list)


class FinancialPlanBuildRequest(BaseModel):
    planning_unit_id: str
    investor_priorities: Optional[InvestorPriorities] = None


class BasketReportRequest(BaseModel):
    planning_unit_id: str
    goal_ids: List[str] = Field(default_factory=list)
    basket_name: Optional[str] = None

