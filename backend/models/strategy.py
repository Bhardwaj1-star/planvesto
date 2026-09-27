from dataclasses import dataclass, field
from typing import Any
from pydantic import BaseModel, Field, model_validator


class StrategyImplementationParamDef(BaseModel):
    name: str
    label: str
    param_type: str
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
            if not self.choices or self.default_value not in self.choices:
                raise ValueError("choice parameters require a valid default")
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
        if not self.library_version.strip() or not self.implementation_version.strip():
            raise ValueError("version fields cannot be empty")
        names = [param.name for param in self.implementation_parameters]
        if len(names) != len(set(names)):
            raise ValueError("implementation parameter names must be unique")
        for score_name in ("baseline_safety_score", "baseline_liquidity_score", "baseline_growth_score", "baseline_flexibility_score"):
            score = getattr(self, score_name)
            if not 0 <= score <= 10:
                raise ValueError(f"{score_name} must be between 0 and 10")
        return self


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
