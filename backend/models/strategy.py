from dataclasses import dataclass, field
from typing import Any, Literal
from pydantic import BaseModel, Field, model_validator


class StrategyImplementationParamDef(BaseModel):
    name: str
    label: str
    param_type: Literal["currency", "percentage", "integer", "choice"]
    description: str
    default_value: Any
    editable: bool = True
    min_value: float | None = None
    max_value: float | None = None
    choices: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_definition(self) -> "StrategyImplementationParamDef":
        if self.min_value is not None and self.max_value is not None and self.min_value > self.max_value:
            raise ValueError("min_value cannot be greater than max_value")
        if self.param_type == "choice":
            if not self.choices:
                raise ValueError("choice parameters must define at least one choice")
            if self.default_value not in self.choices:
                raise ValueError("choice default_value must be one of choices")
        elif self.choices:
            raise ValueError("choices are only valid for choice parameters")
        if self.param_type != "choice":
            if not isinstance(self.default_value, (int, float)) or isinstance(self.default_value, bool):
                raise ValueError("numeric parameters require a numeric default_value")
            if self.min_value is not None and self.default_value < self.min_value:
                raise ValueError("default_value cannot be below min_value")
            if self.max_value is not None and self.default_value > self.max_value:
                raise ValueError("default_value cannot exceed max_value")
        if self.param_type == "percentage":
            if self.min_value is not None and not 0 <= self.min_value <= 100:
                raise ValueError("percentage min_value must be between 0 and 100")
            if self.max_value is not None and not 0 <= self.max_value <= 100:
                raise ValueError("percentage max_value must be between 0 and 100")
        if self.param_type == "integer":
            for value in (self.default_value, self.min_value, self.max_value):
                if value is not None and float(value) != int(value):
                    raise ValueError("integer parameters require integer bounds and default")
        return self


class TechniqueDefinition(BaseModel):
    technique_id: str
    name: str
    description: str
    active: bool = True
    applicable_strategy_ids: list[str] = Field(default_factory=list)
    purpose: str = ""
    constraints: list[str] = Field(default_factory=list)


class StrategyDefinition(BaseModel):
    strategy_id: str
    name: str
    tagline: str
    description: str
    strategy_family: str = "General"
    strategic_objective: str = ""
    core_mechanism: str = ""
    principles: list[str] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)
    dependencies: list[str] = Field(default_factory=list)
    required_inputs: list[str] = Field(default_factory=list)
    applicable_goal_characteristics: list[str] = Field(default_factory=list)
    applicable_goal_types: list[str] = Field(default_factory=list)
    technique_ids: list[str] = Field(default_factory=list)
    strategic_levers: list[str] = Field(default_factory=list)
    compatible_strategy_ids: list[str] = Field(default_factory=list)
    conflicting_strategy_ids: list[str] = Field(default_factory=list)
    component_ids: list[str] = Field(default_factory=list)
    primary_component_ids: list[str] = Field(default_factory=list)
    supporting_component_ids: list[str] = Field(default_factory=list)
    activation_characteristics: list[str] = Field(default_factory=list)
    library_version: str = "1.0"
    implementation_version: str = "1.0"
    active: bool = True
    implementation_parameters: list[StrategyImplementationParamDef] = Field(default_factory=list)
    good_outcomes: list[str] = Field(default_factory=list)
    bad_outcomes: list[str] = Field(default_factory=list)
    trade_offs: list[str] = Field(default_factory=list)
    baseline_safety_score: float = 7.0
    baseline_liquidity_score: float = 7.0
    baseline_growth_score: float = 7.0
    baseline_flexibility_score: float = 7.0

    @model_validator(mode="after")
    def validate_definition(self) -> "StrategyDefinition":
        if not self.strategy_id.strip():
            raise ValueError("strategy_id cannot be empty")
        if not self.library_version.strip():
            raise ValueError("library_version cannot be empty")
        if not self.implementation_version.strip():
            raise ValueError("implementation_version cannot be empty")
        parameter_names = [param.name for param in self.implementation_parameters]
        if len(parameter_names) != len(set(parameter_names)):
            raise ValueError("implementation parameter names must be unique")
        for score_name in ("baseline_safety_score", "baseline_liquidity_score", "baseline_growth_score", "baseline_flexibility_score"):
            score = getattr(self, score_name)
            if not 0 <= score <= 10:
                raise ValueError(f"{score_name} must be between 0 and 10")
        return self


class StrategyArchitecture(BaseModel):
    architecture_id: str
    primary_strategy_id: str
    supporting_strategy_ids: list[str] = Field(default_factory=list)
    technique_ids: list[str] = Field(default_factory=list)
    rationale: list[str] = Field(default_factory=list)
    trade_offs: list[str] = Field(default_factory=list)
    feasibility_status: Literal["feasible", "conditional", "infeasible"] = "feasible"
    constraints: list[str] = Field(default_factory=list)


class Scenario(BaseModel):
    scenario_id: str
    strategy_id: str
    scenario_type: Literal["baseline", "modified", "custom"] = "baseline"
    scenario_name: str
    assumptions: dict[str, Any] = Field(default_factory=dict)
    funding_structure: dict[str, Any] = Field(default_factory=dict)
    metrics: dict[str, Any] = Field(default_factory=dict)
    trade_off_notes: str = ""
    is_investor_modified: bool = False


class InvestorPriorities(BaseModel):
    safety: float = 0.25
    liquidity: float = 0.25
    growth: float = 0.25
    flexibility: float = 0.25

    def normalized(self) -> "InvestorPriorities":
        total = self.safety + self.liquidity + self.growth + self.flexibility
        if total <= 0:
            return InvestorPriorities(safety=0.25, liquidity=0.25, growth=0.25, flexibility=0.25)
        return InvestorPriorities(
            safety=round(self.safety / total, 4),
            liquidity=round(self.liquidity / total, 4),
            growth=round(self.growth / total, 4),
            flexibility=round(self.flexibility / total, 4),
        )


class StrategyRankingItem(BaseModel):
    rank: int
    strategy_id: str
    scenario_id: str
    strategy_name: str
    scenario_name: str
    composite_score: float
    dimension_scores: dict[str, float] = Field(default_factory=dict)
    is_recommended: bool = False


class StrategyRecommendation(BaseModel):
    recommended_strategy_id: str
    recommended_scenario_id: str
    short_reasons: list[str] = Field(default_factory=list)
    complete_reasoning: str = ""
    architecture: StrategyArchitecture | None = None
    alternative_architecture_ids: list[str] = Field(default_factory=list)
    feasibility_status: Literal["feasible", "conditional", "infeasible"] = "feasible"
    constraints: list[str] = Field(default_factory=list)


class StrategyRun(BaseModel):
    strategy_run_id: str | None = None
    planning_unit_id: str
    goal_id: str
    defined_goal_id: str
    defined_goal_version: int
    run_version: int = 1
    is_latest: bool = True
    status: str = "completed"
    applicable_strategies: list[StrategyDefinition] = Field(default_factory=list)
    scenarios: list[Scenario] = Field(default_factory=list)
    investor_priorities: InvestorPriorities = Field(default_factory=InvestorPriorities)
    comparison_matrix: dict[str, Any] = Field(default_factory=dict)
    rankings: list[StrategyRankingItem] = Field(default_factory=list)
    recommendation: StrategyRecommendation
    architectures: list[StrategyArchitecture] = Field(default_factory=list)
    selected_strategy_id: str | None = None
    selected_scenario_id: str | None = None
    selected_strategy_version_id: str | None = None
    selected_strategy_version: int | None = None
    selected_implementation_parameters: dict[str, Any] = Field(default_factory=dict)
    selected_architecture: StrategyArchitecture | None = None
    selection_timestamp: str | None = None
    approval_status: Literal["not_selected", "selected", "approved", "rejected", "superseded"] = "not_selected"
    run_metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: str | None = None


@dataclass(frozen=True)
class StrategyComponent:
    component_id: str
    role: str
    description: str = ""
    required_inputs: tuple[str, ...] = ()
    output_keys: tuple[str, ...] = ()
    compatible_roles: tuple[str, ...] = ()
    conflicts_with_roles: tuple[str, ...] = ()
    implementation_parameters: tuple[str, ...] = ()

    def can_combine_with(self, other: "StrategyComponent") -> bool:
        return other.role not in self.conflicts_with_roles and self.role not in other.conflicts_with_roles


@dataclass
class StrategyPlan:
    goal_id: str
    primary_component_ids: list[str] = field(default_factory=list)
    supporting_component_ids: list[str] = field(default_factory=list)
    technique_ids: list[str] = field(default_factory=list)
    rationale: list[str] = field(default_factory=list)
    trade_offs: list[str] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)
    implementation: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
