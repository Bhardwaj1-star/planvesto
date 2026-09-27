from models.defined_goal import DefinedGoal
from models.strategy import StrategyDefinition
from library.strategies.registry import get_active_strategies
from engines.strategy.components.definitions import register_default_components


register_default_components()

GOAL_TYPE_ALIASES = {
    "retirement/financial freedom": "retirement",
    "education": "child education",
    "marriage": "child marriage",
    "dream home": "home purchase",
    "vacation": "travel",
    "others": "other",
    "passive income": "other",
    "debt repayment": "other",
    "philanthropy": "other",
}


def _canonical_goal_type(value: str | None) -> str:
    clean = (value or "").strip().lower()
    return GOAL_TYPE_ALIASES.get(clean, clean)


def filter_applicable_strategies(
    goal_type: str | None = None,
    defined_goal: DefinedGoal | None = None,
    financial_context: dict | None = None,
) -> list[StrategyDefinition]:
    """Return strategies eligible for the goal.

    Strategy eligibility is determined by library-level goal metadata. Component
    activation is deliberately evaluated later during architecture composition;
    a component being inactive must not make its parent strategy disappear from
    ranking or prevent an already-selected strategy from surviving a recalculation.
    """
    if defined_goal is not None:
        clean_goal_type = _canonical_goal_type(defined_goal.goal_type)
        goal = defined_goal
    else:
        clean_goal_type = _canonical_goal_type(goal_type)
        goal = None

    if not clean_goal_type:
        return []

    applicable: list[StrategyDefinition] = []
    for strategy in get_active_strategies():
        types_lower = [_canonical_goal_type(t) for t in strategy.applicable_goal_types]
        if clean_goal_type not in types_lower:
            continue

        characteristics = {c.strip().lower() for c in strategy.applicable_goal_characteristics}
        if goal is not None and characteristics:
            signals = {
                "shortfall": goal.funding_status.lower() == "shortfall",
                "on_track": goal.funding_status.lower() == "on track",
                "overfunded": goal.funding_status.lower() == "overfunded",
                "near_term": goal.duration_years <= 5,
                "long_term": goal.duration_years >= 7,
                "fixed_timeline": goal.flexibility.lower() == "fixed",
                "flexible_timeline": goal.flexibility.lower() != "fixed",
                "high_priority": goal.priority.lower() in {"critical", "high"},
            }
            if not any(signals.get(c, False) for c in characteristics):
                continue

        applicable.append(strategy)

    return applicable
