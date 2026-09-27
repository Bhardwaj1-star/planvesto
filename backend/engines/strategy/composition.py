from models.defined_goal import DefinedGoal
from models.strategy import StrategyArchitecture, StrategyDefinition
from engines.strategy.components.adapters import components_for_strategy


def compose_architectures(
    strategies: list[StrategyDefinition],
    defined_goal: DefinedGoal,
    financial_context: dict | None = None,
) -> list[StrategyArchitecture]:
    """Compose architectures from strategy/component metadata only."""
    context = {
        "duration_years": defined_goal.duration_years,
        "funding_status": defined_goal.funding_status,
        **(financial_context or {}),
    }
    if not strategies:
        return []

    mapped = [(s, components_for_strategy(s)) for s in strategies]
    mapped = [(s, c) for s, c in mapped if c]
    if not mapped:
        return []
    by_id = {s.strategy_id: (s, c) for s, c in mapped}
    ordered = [s for s, _ in mapped]

    def can_support(primary, candidate):
        if candidate.strategy_id == primary.strategy_id:
            return False
        if candidate.strategy_id in primary.conflicting_strategy_ids or primary.strategy_id in candidate.conflicting_strategy_ids:
            return False
        return all(a.can_combine_with(b) for a in by_id[primary.strategy_id][1] for b in by_id[candidate.strategy_id][1])

    def make(primary, supporting, reason):
        support = [s for s in supporting if can_support(primary, s)]
        components = by_id[primary.strategy_id][1] + [c for s in support for c in by_id[s.strategy_id][1]]
        constraints = list(primary.constraints)
        missing = [x for x in primary.required_inputs if x not in context]
        if missing:
            constraints.append(f"Missing strategy inputs: {', '.join(missing)}")
        return StrategyArchitecture(
            architecture_id=f"arch-{defined_goal.goal_id}-{primary.strategy_id}-{'-'.join(s.strategy_id for s in support) or 'core'}",
            primary_strategy_id=primary.strategy_id,
            supporting_strategy_ids=[s.strategy_id for s in support],
            technique_ids=primary.technique_ids[:3],
            rationale=[reason, f"Primary components: {', '.join(c.role for c in by_id[primary.strategy_id][1])}."] + ([f"Supporting components: {', '.join(c.role for c in components[len(by_id[primary.strategy_id][1]):])}."] if support else []),
            trade_offs=primary.trade_offs[:2],
            feasibility_status="conditional" if missing else "feasible",
            constraints=constraints,
        )

    architectures = []
    for candidate in ordered:
        primary_components = by_id[candidate.strategy_id][1]
        preferred = [c for c in primary_components if c.is_preferred(context)]
        if not preferred:
            continue
        preferred_roles = {c.role for c in preferred}
        supports = [s for s in ordered if any(c.role not in preferred_roles for c in by_id[s.strategy_id][1])]
        reason = "Architecture activated by component metadata: " + ", ".join(c.role for c in preferred)
        architectures.append(make(candidate, supports, reason))

    if not architectures:
        primary = ordered[0]
        architectures.append(make(primary, [], "Fallback architecture using the first eligible strategy because no component activation rule matched."))

    unique, seen = [], set()
    for architecture in architectures:
        key = (architecture.primary_strategy_id, tuple(architecture.supporting_strategy_ids))
        if key not in seen:
            seen.add(key)
            unique.append(architecture)
    return unique
