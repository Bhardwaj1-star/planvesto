from library.strategies.catalog import get_all_strategies
from models.strategy import StrategyDefinition


def filter_applicable_strategies(goal_type: str) -> list[StrategyDefinition]:
    """
    Evaluates applicability strictly by Goal Type.
    Funding status (Shortfall, On Track, Overfunded) is an analysis input,
    NOT an applicability filter.
    """
    clean_goal_type = (goal_type or "").strip().lower()
    if not clean_goal_type:
        return []

    applicable: list[StrategyDefinition] = []
    for strat in get_all_strategies():
        types_lower = [t.strip().lower() for t in strat.applicable_goal_types]
        if clean_goal_type in types_lower or "other" in types_lower:
            applicable.append(strat)

    return applicable
