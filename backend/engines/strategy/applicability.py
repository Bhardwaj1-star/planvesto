from models.defined_goal import DefinedGoal
from models.strategy import StrategyDefinition
from library.strategies.registry import get_active_strategies


def filter_applicable_strategies(
    goal_type: str | None = None,
    defined_goal: DefinedGoal | None = None,
    financial_context: dict | None = None,
) -> list[StrategyDefinition]:
    """Evaluate eligibility from the goal plus available financial-state context.

    Goal type remains a library index, not the final applicability decision.
    Missing financial-state data does not make a strategy ineligible; it makes the
    result less certain and is recorded by the engine as a conditional input.
    """
    if defined_goal is not None:
        clean_goal_type = (defined_goal.goal_type or "").strip().lower()
        goal = defined_goal
    else:
        clean_goal_type = (goal_type or "").strip().lower()
        goal = None

    if not clean_goal_type:
        return []

    context = financial_context or {}
    applicable: list[StrategyDefinition] = []
    for strategy in get_active_strategies():
        types_lower = [t.strip().lower() for t in strategy.applicable_goal_types]
        if clean_goal_type not in types_lower and "other" not in types_lower:
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

        # Investor circumstances can add eligibility signals without using risk-profile data.
        liabilities = _metric(context, "total_liabilities")
        surplus = _metric(context, "investable_surplus_monthly")
        if strategy.strategy_id == "strat-debt-reduction" and liabilities is not None and liabilities <= 0:
            continue
        if strategy.strategy_id == "strat-credit-utilisation" and surplus is not None and surplus <= 0:
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
