from models.defined_goal import DefinedGoal
from models.strategy import StrategyDefinition
from library.strategies.registry import get_active_strategies


# Goal Planner uses user-facing goal names while the strategy catalog keeps
# canonical goal types. Keep this mapping in the applicability layer so the
# catalog and persisted goal records do not need to be rewritten.
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
    """Evaluate eligibility from the goal plus available financial-state context."""
    if defined_goal is not None:
        clean_goal_type = _canonical_goal_type(defined_goal.goal_type)
        goal = defined_goal
    else:
        clean_goal_type = _canonical_goal_type(goal_type)
        goal = None
    if not clean_goal_type:
        return []

    context = financial_context or {}
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

        liabilities = _metric(context, "total_liabilities")
        surplus = _metric(context, "investable_surplus_monthly")
        emi = _metric(context, "emi_burden_monthly")
        if strategy.strategy_id == "strat-debt-reduction":
            # Debt reduction is only a financially grounded strategy when the
            # household actually has debt and its servicing burden is known.
            if liabilities is not None and liabilities <= 0:
                continue
            if liabilities is not None and emi is None:
                continue
        if strategy.strategy_id == "strat-credit-utilisation":
            # Credit is only considered when there is positive surplus and the
            # existing debt-service burden is known. Unknown cash-flow capacity
            # must not be treated as affordability.
            if surplus is not None and surplus <= 0:
                continue
            if surplus is not None and emi is None:
                continue
        applicable.append(strategy)
    return applicable


def _metric(context: dict, name: str) -> float | None:
    raw = context.get(name)
    if isinstance(raw, dict):
        raw = raw.get("value") if raw.get("available", True) else None
    try:
        return float(raw) if raw is not None else None
    except (TypeError, ValueError):
        return None
