from models.defined_goal import DefinedGoal
from models.strategy import InvestorPriorities, Scenario, StrategyDefinition, StrategyRankingItem, StrategyRecommendation, StrategyArchitecture
from engines.strategy.applicability import filter_applicable_strategies
from engines.strategy.comparison import build_comparison_matrix
from engines.strategy.ranking import rank_scenarios
from engines.strategy.recommendation import generate_recommendation
from engines.strategy.scenario import generate_baseline_scenarios
from engines.strategy.composition import compose_architectures


class StrategyEngineResult:
    def __init__(self, applicable_strategies, scenarios, priorities, comparison_matrix, rankings, recommendation, architectures):
        self.applicable_strategies = applicable_strategies
        self.scenarios = scenarios
        self.priorities = priorities
        self.comparison_matrix = comparison_matrix
        self.rankings = rankings
        self.recommendation = recommendation
        self.architectures = architectures


class StrategyEngine:
    @staticmethod
    def _decision_context(financial_context: dict | None, rule_assessment=None) -> dict:
        context = dict(financial_context or {})
        if rule_assessment is None:
            context["rule_diagnostics"] = []
            context["decision_roles"] = {"eligibility": [], "ranking": [], "recommendation": []}
            return context

        diagnostics = list(rule_assessment.diagnostics)
        # Current rule set: hard constraints govern eligibility; financial-health
        # diagnostics are recommendation evidence. Ranking remains driven by the
        # explicit investor priority weights until a documented scoring policy exists.
        roles = {
            "eligibility": [r.rule_id for r in rule_assessment.hard_constraints],
            "ranking": [],
            "recommendation": [r.rule_id for r in diagnostics],
        }
        context["rule_diagnostics"] = [
            {
                "rule_id": r.rule_id,
                "passed": r.passed,
                "severity": r.severity,
                "message": r.message,
                "evidence": r.evidence,
            }
            for r in diagnostics
        ]
        context["decision_roles"] = roles
        return context

    def execute(
        self,
        defined_goal: DefinedGoal,
        priorities: InvestorPriorities | None = None,
        custom_scenarios: list[Scenario] | None = None,
        financial_context: dict | None = None,
        rule_assessment=None,
    ) -> StrategyEngineResult:
        if priorities is None:
            raise ValueError("Investor priorities must be provided before strategy comparison and ranking.")

        strategies = filter_applicable_strategies(
            defined_goal=defined_goal,
            financial_context=financial_context,
        )

        if not strategies:
            empty_rec = StrategyRecommendation(
                recommended_strategy_id="",
                recommended_scenario_id="",
                short_reasons=["No Strategy Available"],
                complete_reasoning="No strategy in the library is eligible for the current goal and available constraints.",
                feasibility_status="infeasible",
            )
            return StrategyEngineResult([], [], priorities, {"dimensions": [], "items": []}, [], empty_rec, [])

        all_scenarios: list[Scenario] = []
        for strategy in strategies:
            all_scenarios.extend(generate_baseline_scenarios(strategy, defined_goal))
        if custom_scenarios:
            all_scenarios.extend(custom_scenarios)

        strategy_context = self._decision_context(financial_context, rule_assessment)
        comp_matrix = build_comparison_matrix(strategies, all_scenarios)
        rankings = rank_scenarios(strategies, all_scenarios, priorities)
        architectures = compose_architectures(strategies, defined_goal, strategy_context)

        recommendation = generate_recommendation(
            ranked_items=rankings,
            strategies=strategies,
            scenarios=all_scenarios,
            defined_goal=defined_goal,
            priorities=priorities,
            architectures=architectures,
        )

        return StrategyEngineResult(
            strategies, all_scenarios, priorities, comp_matrix, rankings, recommendation, architectures
        )
