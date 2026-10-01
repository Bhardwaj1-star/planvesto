from models.defined_goal import DefinedGoal
from models.strategy import InvestorPriorities, Scenario, StrategyRecommendation
from engines.strategy.applicability import filter_applicable_strategies
from engines.strategy.comparison import build_comparison_matrix
from engines.strategy.ranking import rank_scenarios
from engines.strategy.recommendation import generate_recommendation
from engines.strategy.scenario import generate_baseline_scenarios
from engines.strategy.composition import compose_architectures
from engines.strategy.decision import evaluate_decision
from engines.rules.engine import RuleEngine
from engines.constraints.aggregator import ConstraintAggregator
from engines.constraints.models import ConstraintSet


class StrategyEngineResult:
    def __init__(self, applicable_strategies, scenarios, priorities, comparison_matrix, rankings, recommendation, architectures):
        self.applicable_strategies = applicable_strategies
        self.scenarios = scenarios
        self.priorities = priorities
        self.comparison_matrix = comparison_matrix
        self.rankings = rankings
        self.recommendation = recommendation
        self.architectures = architectures
        self.what_if_scenarios = what_if_scenarios or []


class StrategyEngine:
    @staticmethod
    def _decision_context(financial_context: dict | None, constraint_set: ConstraintSet | None = None, rule_assessment=None) -> dict:
        context = dict(financial_context or {})
        if constraint_set is not None:
            constraints = constraint_set.constraints
            context["canonical_constraints"] = [c.model_dump() for c in constraints]
            context["constraint_conflicts"] = [c.model_dump() for c in constraint_set.conflicts]
            context["rule_diagnostics"] = [
                {
                    "rule_id": c.rule_id,
                    "passed": c.passed,
                    "severity": c.severity,
                    "message": c.message,
                    "evidence": c.evidence,
                    "role": c.role,
                }
                for c in constraints
                if c.role in {"recommendation_only", "explanatory_evidence"}
            ]
            context["decision_roles"] = {
                "eligibility": [c.rule_id for c in constraint_set.hard_constraints],
                "ranking": [c.rule_id for c in constraints if c.role == "ranking_input"],
                "recommendation": [c.rule_id for c in constraints if c.role in {"recommendation_only", "explanatory_evidence"}],
            }
            return context
        if rule_assessment is None:
            context["rule_diagnostics"] = []
            context["decision_roles"] = {"eligibility": [], "ranking": [], "recommendation": []}
            return context
        diagnostics = list(rule_assessment.diagnostics)
        context["rule_diagnostics"] = [
            {
                "rule_id": r.rule_id,
                "passed": r.passed,
                "severity": r.severity,
                "message": r.message,
                "evidence": r.evidence,
                "role": (r.role.value if getattr(r, "role", None) is not None else None),
            }
            for r in diagnostics
        ]
        roles = rule_assessment.decision_roles
        context["decision_roles"] = {
            "eligibility": [r.rule_id for r in rule_assessment.hard_constraints],
            "ranking": roles.get("RANKING_INPUT", []),
            "recommendation": roles.get("RECOMMENDATION_ONLY", []) + roles.get("EXPLANATORY_EVIDENCE", []),
        }
        return context

    def execute(
        self,
        defined_goal: DefinedGoal,
        priorities: InvestorPriorities | None = None,
        custom_scenarios: list[Scenario] | None = None,
        financial_context: dict | None = None,
        rule_assessment=None,
        constraint_set: ConstraintSet | None = None,
    ) -> StrategyEngineResult:
        if priorities is None:
            raise ValueError("Investor priorities must be provided before strategy comparison and ranking.")

        # Direct callers remain backward-compatible. Service-layer flows
        # provide the centralized ConstraintSet explicitly.
        if constraint_set is None:
            if rule_assessment is None:
                rule_assessment = RuleEngine().assess(defined_goal, financial_context or {})
            constraint_set = ConstraintAggregator().aggregate(
                rule_assessment=rule_assessment,
                financial_context=financial_context or {},
            )

        strategies = filter_applicable_strategies(defined_goal=defined_goal, financial_context=financial_context)
        if not strategies:
            empty_rec = StrategyRecommendation(
                recommended_strategy_id="", recommended_scenario_id="", short_reasons=["No Strategy Available"],
                complete_reasoning="No strategy in the library is eligible for the current goal and available constraints.", feasibility_status="infeasible",
            )
            return StrategyEngineResult([], [], priorities, {"dimensions": [], "items": []}, [], empty_rec, [])

        all_scenarios: list[Scenario] = []
        for strategy in strategies:
            all_scenarios.extend(generate_baseline_scenarios(strategy, defined_goal))
        if custom_scenarios:
            all_scenarios.extend(custom_scenarios)

        what_if_scenarios: list[Scenario] = []
        for strategy in strategies:
            what_if_scenarios.extend(generate_what_if_scenarios(strategy, defined_goal))

        strategy_context = self._decision_context(financial_context, constraint_set, rule_assessment)
        comp_matrix = build_comparison_matrix(strategies, all_scenarios)
        architectures = compose_architectures(strategies, defined_goal, strategy_context)

        decision_result = evaluate_decision(
            strategies=strategies,
            scenarios=all_scenarios,
            architectures=architectures,
            defined_goal=defined_goal,
            financial_context=financial_context,
            rule_assessment=rule_assessment,
            priorities=priorities,
            constraint_set=constraint_set,
        )

        rankings = rank_scenarios(
            strategies=strategies,
            scenarios=all_scenarios,
            priorities=priorities,
            decision_result=decision_result,
            defined_goal=defined_goal,
            financial_context=financial_context,
            architectures=architectures,
            constraint_set=constraint_set,
        )

        recommendation = generate_recommendation(
            decision_result=decision_result,
            ranked_items=rankings,
            strategies=strategies,
            scenarios=all_scenarios,
            defined_goal=defined_goal,
            priorities=priorities,
            architectures=architectures,
            rule_diagnostics=strategy_context["rule_diagnostics"],
        )

        return StrategyEngineResult(strategies, all_scenarios, priorities, comp_matrix, rankings, recommendation, architectures)
