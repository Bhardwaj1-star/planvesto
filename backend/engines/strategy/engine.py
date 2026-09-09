from models.defined_goal import DefinedGoal
from models.strategy import (
    InvestorPriorities,
    Scenario,
    StrategyDefinition,
    StrategyRankingItem,
    StrategyRecommendation,
)
from engines.strategy.applicability import filter_applicable_strategies
from engines.strategy.comparison import build_comparison_matrix
from engines.strategy.ranking import rank_scenarios
from engines.strategy.recommendation import generate_recommendation
from engines.strategy.scenario import generate_baseline_scenarios


class StrategyEngineResult:
    def __init__(
        self,
        applicable_strategies: list[StrategyDefinition],
        scenarios: list[Scenario],
        priorities: InvestorPriorities,
        comparison_matrix: dict,
        rankings: list[StrategyRankingItem],
        recommendation: StrategyRecommendation,
    ):
        self.applicable_strategies = applicable_strategies
        self.scenarios = scenarios
        self.priorities = priorities
        self.comparison_matrix = comparison_matrix
        self.rankings = rankings
        self.recommendation = recommendation


class StrategyEngine:
    def execute(
        self,
        defined_goal: DefinedGoal,
        priorities: InvestorPriorities | None = None,
        custom_scenarios: list[Scenario] | None = None,
    ) -> StrategyEngineResult:
        if priorities is None:
            priorities = InvestorPriorities()

        # 1. Applicability (strictly by Goal Type)
        strategies = filter_applicable_strategies(defined_goal.goal_type)

        if not strategies:
            # "No Strategy Available"
            empty_rec = StrategyRecommendation(
                recommended_strategy_id="",
                recommended_scenario_id="",
                short_reasons=["No Strategy Available"],
                complete_reasoning="No strategies in the library match this goal type.",
            )
            return StrategyEngineResult(
                applicable_strategies=[],
                scenarios=[],
                priorities=priorities,
                comparison_matrix={"dimensions": [], "items": []},
                rankings=[],
                recommendation=empty_rec,
            )

        # 2. Scenarios: Baseline + Custom
        all_scenarios: list[Scenario] = []
        for s in strategies:
            baselines = generate_baseline_scenarios(s, defined_goal)
            all_scenarios.extend(baselines)

        if custom_scenarios:
            all_scenarios.extend(custom_scenarios)

        # 3. Comparison Matrix
        comp_matrix = build_comparison_matrix(strategies, all_scenarios)

        # 4. Ranking
        rankings = rank_scenarios(strategies, all_scenarios, priorities)

        # 5. Recommendation
        recommendation = generate_recommendation(
            ranked_items=rankings,
            strategies=strategies,
            scenarios=all_scenarios,
            defined_goal=defined_goal,
            priorities=priorities,
        )

        return StrategyEngineResult(
            applicable_strategies=strategies,
            scenarios=all_scenarios,
            priorities=priorities,
            comparison_matrix=comp_matrix,
            rankings=rankings,
            recommendation=recommendation,
        )
