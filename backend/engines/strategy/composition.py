from models.defined_goal import DefinedGoal
from models.strategy import StrategyArchitecture, StrategyDefinition
from engines.strategy.components.adapters import component_for_strategy


def compose_architectures(
    strategies: list[StrategyDefinition],
    defined_goal: DefinedGoal,
    financial_context: dict | None = None,
) -> list[StrategyArchitecture]:
    """Compose goal-level architectures from reusable strategy components.

    The composer deliberately does not inspect strategy names or strategy IDs.
    Existing library families are translated through the component adapter, and
    component compatibility/conflict rules govern composition.
    """
    context = financial_context or {}
    if not strategies:
        return []

    mapped = [(strategy, component_for_strategy(strategy)) for strategy in strategies]
    mapped = [(strategy, component) for strategy, component in mapped if component is not None]
    if not mapped:
        return []

    by_id = {strategy.strategy_id: (strategy, component) for strategy, component in mapped}
    ordered = [strategy for strategy, _ in mapped]

    def can_support(primary, candidate) -> bool:
        if candidate.strategy_id == primary.strategy_id:
            return False
        if candidate.strategy_id in primary.conflicting_strategy_ids:
            return False
        if primary.strategy_id in candidate.conflicting_strategy_ids:
            return False
        primary_component = by_id[primary.strategy_id][1]
        candidate_component = by_id[candidate.strategy_id][1]
        return primary_component.can_combine_with(candidate_component)

    def make(primary: StrategyDefinition, supporting: list[StrategyDefinition], reason: str):
        support = [s for s in supporting if can_support(primary, s)]
        primary_component = by_id[primary.strategy_id][1]
        support_components = [by_id[s.strategy_id][1] for s in support]
        constraints = list(primary.constraints)
        missing_inputs = [name for name in primary.required_inputs if name not in context]
        if missing_inputs:
            constraints.append(f"Missing strategy inputs: {', '.join(missing_inputs)}")
        return StrategyArchitecture(
            architecture_id=f"arch-{defined_goal.goal_id}-{primary.strategy_id}-{'-'.join(s.strategy_id for s in support) or 'core'}",
            primary_strategy_id=primary.strategy_id,
            supporting_strategy_ids=[s.strategy_id for s in support],
            technique_ids=primary.technique_ids[:3],
            rationale=[reason, f"Primary component: {primary_component.role}."] + [f"Supporting component: {c.role}." for c in support_components],
            trade_offs=primary.trade_offs[:2],
            feasibility_status="conditional" if missing_inputs else "feasible",
            constraints=constraints,
        )

    architectures: list[StrategyArchitecture] = []
    primary = ordered[0]

    # Build candidate architectures from the available component roles and the
    # goal state. No goal-specific engine or strategy-name heuristic is used.
    for candidate in ordered:
        role = by_id[candidate.strategy_id][1].role
        if role == "funding" and defined_goal.funding_status == "Shortfall":
            supports = [s for s in ordered if by_id[s.strategy_id][1].role in {"preservation", "debt", "orchestration"}]
            architectures.append(make(candidate, supports, "The goal has a funding shortfall, so funding is the primary strategic role."))
        elif role == "accumulation" and defined_goal.duration_years >= 7:
            supports = [s for s in ordered if by_id[s.strategy_id][1].role in {"transition", "preservation"}]
            architectures.append(make(candidate, supports, "The goal has a sufficiently long horizon for an accumulation-led architecture."))
        elif role == "transition" and defined_goal.duration_years <= 7:
            supports = [s for s in ordered if by_id[s.strategy_id][1].role == "preservation"]
            architectures.append(make(candidate, supports, "The goal is approaching maturity, so transition becomes strategically relevant."))
        elif role == "income" and defined_goal.duration_years <= 5:
            supports = [s for s in ordered if by_id[s.strategy_id][1].role == "preservation"]
            architectures.append(make(candidate, supports, "The goal is close enough that dependable cash-flow support becomes strategically relevant."))
        elif role == "debt" and _metric(context, "total_liabilities") not in (None, 0):
            supports = [s for s in ordered if by_id[s.strategy_id][1].role in {"funding", "orchestration"}]
            architectures.append(make(candidate, supports, "Liability pressure is part of the available financial context and can affect goal feasibility."))
        elif role == "orchestration" and defined_goal.funding_status in {"Overfunded", "On Track"}:
            supports = [s for s in ordered if by_id[s.strategy_id][1].role in {"preservation", "funding"}]
            architectures.append(make(candidate, supports, "The goal is funded or on track, so resource allocation can be coordinated explicitly."))

    if not architectures:
        architectures.append(make(primary, [], "This is the strongest eligible architecture under the currently available goal information."))

    unique: list[StrategyArchitecture] = []
    seen: set[tuple[str, tuple[str, ...]]] = set()
    for architecture in architectures:
        key = (architecture.primary_strategy_id, tuple(architecture.supporting_strategy_ids))
        if key not in seen:
            seen.add(key)
            unique.append(architecture)
    return unique


def _metric(context: dict, name: str) -> float | None:
    raw = context.get(name)
    if isinstance(raw, dict):
        raw = raw.get("value") if raw.get("available", True) else None
    try:
        return float(raw) if raw is not None else None
    except (TypeError, ValueError):
        return None
