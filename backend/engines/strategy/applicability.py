from models.defined_goal import DefinedGoal
from models.strategy import StrategyDefinition
from library.strategies.canonical import get_canonical_strategies
from engines.rules.engine import StrategyRuleEngine
from engines.strategy.components.definitions import register_default_components


register_default_components()
_rule_engine = StrategyRuleEngine()


def _canonical_goal_type(value: str | None) -> str:
    return _rule_engine.canonical_goal_type(value)


def filter_applicable_strategies(
    goal_type: str | None = None,
    defined_goal: DefinedGoal | None = None,
    financial_context: dict | None = None,
) -> list[StrategyDefinition]:
    """Return strategies eligible for the goal.

    Rule evaluation owns eligibility. Component activation remains a later
    architecture concern and cannot remove an otherwise eligible strategy.
    """
    if not (defined_goal is not None or _canonical_goal_type(goal_type)):
        return []

    applicable: list[StrategyDefinition] = []
    for strategy in get_canonical_strategies():
        evaluation = _rule_engine.evaluate(
            strategy=strategy,
            goal_type=goal_type,
            defined_goal=defined_goal,
            financial_context=financial_context,
        )
        if evaluation.eligible:
            applicable.append(strategy)

    return applicable
