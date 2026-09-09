from typing import Any, Literal
from pydantic import BaseModel, Field


class StrategyImplementationParamDef(BaseModel):
    name: str
    label: str
    param_type: Literal["currency", "percentage", "integer", "choice"]
    description: str
    default_value: Any
    min_value: float | None = None
    max_value: float | None = None
    choices: list[str] = Field(default_factory=list)


class StrategyDefinition(BaseModel):
    strategy_id: str
    name: str
    tagline: str
    description: str
    applicable_goal_types: list[str] = Field(default_factory=list)
    implementation_parameters: list[StrategyImplementationParamDef] = Field(default_factory=list)
    good_outcomes: list[str] = Field(default_factory=list)
    bad_outcomes: list[str] = Field(default_factory=list)
    trade_offs: list[str] = Field(default_factory=list)
    baseline_safety_score: float = 7.0
    baseline_liquidity_score: float = 7.0
    baseline_growth_score: float = 7.0
    baseline_flexibility_score: float = 7.0


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
    selected_strategy_id: str | None = None
    selected_scenario_id: str | None = None
    selected_implementation_parameters: dict[str, Any] = Field(default_factory=dict)
    selection_timestamp: str | None = None
    run_metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: str | None = None
