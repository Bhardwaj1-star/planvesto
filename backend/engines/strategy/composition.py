from models.defined_goal import DefinedGoal
from models.strategy import StrategyArchitecture, StrategyDefinition
from engines.strategy.components.adapters import components_for_strategy


def compose_architectures(
    strategies: list[StrategyDefinition],
    defined_goal: DefinedGoal,
    financial_context: dict | None = None,
) -> list[StrategyArchitecture]:
    """Compose goal-level architectures from reusable strategy components.

    Strategy records are translated into one or more reusable components.
    Composition uses component roles and compatibility rules; it does not use
    strategy names as architectural logic.
    """
    context = financial_context or {}
    if not strategies:
        return []

    mapped = [(strategy, components_for_strategy(strategy)) for strategy in strategies]
    mapped = [(strategy, components) for strategy, components in mapped if components]
    if not mapped:
        return []

    by_id = {strategy.strategy_id: (strategy, components) for strategy, components in mapped}
    ordered = [strategy for strategy, _ in mapped]

    def can_support(primary, candidate) -> bool:
        if candidate.strategy_id == primary.strategy_id:
            return False
        if candidate.strategy_id in primary.conflicting_strategy_ids:
            return False
        if primary.strategy_id in candidate.conflicting_strategy_ids:
            return False
        primary_components = by_id[primary.strategy_id][1]
        candidate_components = by_id[candidate.strategy_id][1]
        return all(
            left.can_combine_with(right)
            for left in primary_components
            for right in candidate_components
        )

    def make(primary: StrategyDefinition, supporting: list[StrategyDefinition], reason: str):
        support = [s for s in supporting if can_support(primary, s)]
        primary_components = by_id[primary.strategy_id][1]
        support_components = [component for s in support for component in by_id[s.strategy_id][1]]
        constraints = list(primary.constraints)
        missing_inputs = [name for name in primary.required_inputs if name not in context]
        if missing_inputs:
            constraints.append(f"Missing strategy inputs: {', '.join(missing_inputs)}")
        component_roles = [c.role for c in primary_components + support_components]
        return StrategyArchitecture(
            architecture_id=f"arch-{defined_goal.goal_id}-{primary.strategy_id}-{'-'.join(s.strategy_id for s in support) or 'core'}",
            primary_strategy_id=primary.strategy_id,
            supporting_strategy_ids=[s.strategy_id for s in support],
            technique_ids=primary.technique_ids[:3],
            rationale=[reason, f"Primary components: {', '.join(c.role for c in primary_components)}."]
            + ([f"Supporting components: {', '.join(c.role for c in support_components)}."] if support_components else []),
            trade_offs=primary.trade_offs[:2],
            feasibility_status="conditional" if missing_inputs else "feasible",
            constraints=constraints,
        )

    architectures: list[StrategyArchitecture] = []

    for candidate in ordered:
        roles = {component.role for component in by_id[candidate.strategy_id][1]}
        if "funding" in roles and defined_goal.funding_status == "Shortfall":
            supports = [s for s in ordered if {c.role for c in by_id[s.strategy_id][1]} & {"preservation", "debt", "orchestration"}]
            architectures.append(make(candidate, supports, "The goal has a funding shortfall, so funding is the primary strategic role."))
        elif "accumulation" in roles and defined_goal.duration_years >= 7:
            supports = [s for s in ordered if {c.role for c in by_id[s.strategy_id][1]} & {"transition", "preservation"}]
            architectures.append(make(candidate, supports, "The goal has a sufficiently long horizon for an accumulation-led architecture."))
        elif "transition" in roles and defined_goal.duration_years <= 7:
            supports = [s for s in ordered if {c.role for c in by_id[s.strategy_id][1]} & {"preservation", "liquidity"}]
            architectures.append(make(candidate, supports, "The goal is approaching maturity, so transition becomes strategically relevant."))
        elif "income" in roles and defined_goal.duration_years <= 5:
            supports = [s for s in ordered if {c.role for c in by_id[s.strategy_id][1]} & {"preservation", "liquidity"}]
            architectures.append(make(candidate, supports, "The goal is close enough that dependable cash-flow support becomes strategically relevant."))
        elif "debt" in roles and _metric(context, "total_liabilities") not in (None, 0):
            supports = [s for s in ordered if {c.role for c in by_id[s.strategy_id][1]} & {"funding", "orchestration"}]
            architectures.append(make(candidate, supports, "Liability pressure is part of the available financial context and can affect goal feasibility."))
        elif "orchestration" in roles and defined_goal.funding_status in {"Overfunded", "On Track"}:
            supports = [s for s in ordered if {c.role for c in by_id[s.strategy_id][1]} & {"preservation", "funding"}]
            architectures.append(make(candidate, supports, "The goal is funded or on track, so resource allocation can be coordinated explicitly."))

    if not architectures:
        primary = ordered[0]
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
