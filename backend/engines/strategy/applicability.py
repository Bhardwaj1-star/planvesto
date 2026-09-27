from models.defined_goal import DefinedGoal
from models.strategy import StrategyDefinition
from library.strategies.registry import get_active_strategies
from engines.strategy.components.registry import get_component
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


def filter_applicable_strategies(goal_type: str | None = None, defined_goal: DefinedGoal | None = None, financial_context: dict | None = None) -> list[StrategyDefinition]:
    """Evaluate strategy eligibility from goal metadata and reusable components.

    Goal-type-only calls are discovery calls and therefore do not have enough
    financial context to activate/deactivate components. Full goal evaluation
    applies component activation rules using the supplied financial state.
    """
    if defined_goal is not None:
        clean_goal_type = _canonical_goal_type(defined_goal.goal_type)
        goal = defined_goal
    else:
        clean_goal_type = _canonical_goal_type(goal_type)
        goal = None
    if not clean_goal_type:
        return []

    context = dict(financial_context or {})
    if goal is not None:
        context.update({
            "funding_status": goal.funding_status,
            "duration_years": goal.duration_years,
            "flexibility": goal.flexibility,
            "priority": goal.priority,
            "funding_gap": goal.funding_gap,
        })

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

        # Only a fully defined goal should activate component-level financial
        # rules. A goal-type discovery call must remain useful without state.
        if strategy.component_ids and goal is not None:
            if not all(_component_is_active(component_id, context) for component_id in strategy.component_ids):
                continue
        applicable.append(strategy)
    return applicable


def _component_is_active(component_id: str, context: dict) -> bool:
    component = get_component(component_id)
    return component is not None and component.is_preferred(context)
