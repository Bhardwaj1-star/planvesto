from datetime import date, datetime
from enum import Enum
from typing import Any
from pydantic import BaseModel, Field, model_validator


class FundingPath(str, Enum):
    SELF_MONEY = "self_money"
    SELF_MONEY_FINANCING = "self_money_financing"


class AssetDisposition(str, Enum):
    KEEP = "keep"
    REALLOCATE = "reallocate"


class GoalLinkedSIP(BaseModel):
    sip_id: str = Field(min_length=1)
    monthly_amount: float = Field(ge=0)
    next_contribution_date: date | None = None
    end_date: date | None = None
    source_reference: str | None = None
    confirmed_for_goal: bool = False


class ProjectionEventType(str, Enum):
    CONTRIBUTION = "contribution"
    INVESTMENT_GROWTH = "investment_growth"
    FINANCING = "financing"
    REPAYMENT = "repayment"
    GOAL_PAYMENT = "goal_payment"


class AssetDecision(BaseModel):
    asset_id: str = Field(min_length=1)
    disposition: AssetDisposition
    assessed_amount: float | None = Field(default=None, ge=0)
    investor_approved: bool = False
    available_on: date | None = None
    liquidity_notes: str | None = None
    risk_suitability_assessment: str | None = None
    restrictions: list[str] = Field(default_factory=list)
    competing_goal_notes: str | None = None


class FinancingEvidence(BaseModel):
    lender_or_source: str | None = None
    amount: float | None = Field(default=None, gt=0)
    drawdown_date: date | None = None
    annual_interest_rate: float | None = Field(default=None, ge=0, le=100, description="Annual interest rate in percent, e.g. 8.5")
    tenure_months: int | None = Field(default=None, ge=1)
    emi: float | None = Field(default=None, gt=0)
    processing_fees: float | None = Field(default=None, ge=0)
    other_costs: float | None = Field(default=None, ge=0)
    total_financing_cost: float | None = Field(default=None, ge=0, description="Total evidenced financing cost over the full repayment term, including applicable fees and charges.")
    repayment_schedule: list[dict[str, Any]] = Field(default_factory=list)
    evidence_reference: str | None = None

    def missing_terms(self) -> list[str]:
        required = {
            "lender_or_source": self.lender_or_source,
            "amount": self.amount,
            "drawdown_date": self.drawdown_date,
            "annual_interest_rate": self.annual_interest_rate,
            "tenure_months": self.tenure_months,
            "emi": self.emi,
            "processing_fees": self.processing_fees,
            "other_costs": self.other_costs,
            "total_financing_cost": self.total_financing_cost,
            "repayment_schedule": self.repayment_schedule or None,
            "evidence_reference": self.evidence_reference,
        }
        return [key for key, value in required.items() if value is None]


class ProjectionEvent(BaseModel):
    event_date: date
    event_timestamp: datetime | None = None
    event_type: ProjectionEventType
    amount: float = Field(ge=0)
    source_reference: str | None = None
    asset_id: str | None = None
    notes: str | None = None


class YearlyFundingPosition(BaseModel):
    year: int = Field(ge=1900, le=2200)
    opening_balance: float | None = None
    contributions: float | None = None
    investment_growth: float | None = None
    financing_drawdowns: float | None = None
    repayments: float | None = None
    goal_payments: float | None = None
    closing_balance: float | None = None
    shortfall: float | None = None
    surplus: float | None = None
    evidence_references: list[str] = Field(default_factory=list)


class InvestmentPlanEvidence(BaseModel):
    proposed_allocation: dict[str, Any] = Field(default_factory=dict)
    techniques_considered: list[str] = Field(default_factory=list)
    product_options: list[dict[str, Any]] = Field(default_factory=list)
    alternatives: list[dict[str, Any]] = Field(default_factory=list)
    assumptions: dict[str, Any] = Field(default_factory=dict)
    risks: list[str] = Field(default_factory=list)
    costs: list[dict[str, Any]] = Field(default_factory=list)
    trade_offs: list[str] = Field(default_factory=list)
    investor_approved: bool = False


class GoalPayment(BaseModel):
    payment_date: date
    amount: float = Field(ge=0)
    expected_source: str | None = None
    net_proceeds: float | None = None
    costs_and_taxes: float | None = None
    remaining_asset_value: float | None = None
    liquidity_notes: str | None = None
    cross_goal_impact: str | None = None


class ContingencyOption(BaseModel):
    trigger: str
    proposed_response: str
    expected_funding_effect: str | None = None
    cost_risk_liquidity_effect: dict[str, Any] = Field(default_factory=dict)
    revised_scenario: dict[str, Any] = Field(default_factory=dict)
    investor_approved: bool = False


class FundingPathAssessment(BaseModel):
    path: FundingPath
    asset_decisions: list[AssetDecision] = Field(default_factory=list)
    goal_linked_sips: list[GoalLinkedSIP] = Field(default_factory=list)
    goal_linked_sips_assessed: bool = False
    unmapped_asset_assessment_permitted: bool = False
    self_money_requirement: float | None = Field(default=None, ge=0)
    financing: FinancingEvidence | None = None
    projection_events: list[ProjectionEvent] = Field(default_factory=list)
    yearly_positions: list[YearlyFundingPosition] = Field(default_factory=list)
    investment_plan: InvestmentPlanEvidence | None = None
    goal_payments: list[GoalPayment] = Field(default_factory=list)
    monitoring_notes: list[str] = Field(default_factory=list)
    contingency_options: list[ContingencyOption] = Field(default_factory=list)
    assumptions: dict[str, Any] = Field(default_factory=dict)
    constraints: list[str] = Field(default_factory=list)
    calculation_evidence: dict[str, Any] = Field(default_factory=dict)
    step_3_requirement_changed: bool = False

    @model_validator(mode="after")
    def financing_only_on_financing_path(self):
        if self.path == FundingPath.SELF_MONEY and self.financing is not None:
            raise ValueError("Self Money path cannot contain financing terms")
        return self


class GoalFundingAssessmentRequest(BaseModel):
    planning_unit_id: str = Field(min_length=1, max_length=100)
    goal_id: str = Field(min_length=1, max_length=100)
    defined_goal_version: int = Field(ge=1)
    self_money: FundingPathAssessment
    self_money_financing: FundingPathAssessment
    investor_decision: FundingPath | None = None
    investor_decision_confirmed: bool = False
    decision_notes: str | None = None

    @model_validator(mode="after")
    def require_both_paths(self):
        if self.self_money.path != FundingPath.SELF_MONEY:
            raise ValueError("self_money must use the self_money funding path")
        if self.self_money_financing.path != FundingPath.SELF_MONEY_FINANCING:
            raise ValueError("self_money_financing must use the self_money_financing funding path")
        if self.investor_decision is not None and not self.investor_decision_confirmed:
            raise ValueError("Investor decision requires explicit confirmation")
        if self.investor_decision is None and self.investor_decision_confirmed:
            raise ValueError("Decision confirmation cannot be true without a selected funding path")
        return self


class GoalFundingAssessment(BaseModel):
    assessment_id: str | None = None
    planning_unit_id: str
    goal_id: str
    defined_goal_id: str
    defined_goal_version: int
    version: int = 1
    status: str
    entry_route: str
    goal_handoff: dict[str, Any]
    self_money: FundingPathAssessment
    self_money_financing: FundingPathAssessment
    comparison: dict[str, Any] = Field(default_factory=dict)
    investor_decision: FundingPath | None = None
    investor_decision_confirmed: bool = False
    decision_notes: str | None = None
    created_at: str | None = None
