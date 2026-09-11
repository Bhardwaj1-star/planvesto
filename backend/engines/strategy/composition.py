from models.defined_goal import DefinedGoal
from models.strategy import StrategyArchitecture, StrategyDefinition


def compose_architectures(
    strategies: list[StrategyDefinition],
    defined_goal: DefinedGoal,
    financial_context: dict | None = None,
) -> list[StrategyArchitecture]:
    """Build coherent goal-level architectures from eligible strategies.

    Composition is strategic only: no investment products or risk-profile inputs are used.
    """
    context = financial_context or {}
    by_id = {s.strategy_id: s for s in strategies}
    ordered = list(strategies)
    if not ordered:
        return []

    surplus = _metric(context, "investable_surplus_monthly")
    liabilities = _metric(context, "total_liabilities")
    safety_months = _metric(context, "safety_reserve_months")

    def make(primary: StrategyDefinition, supporting: list[str], rationale: list[str], techniques: list[str], constraints: list[str] | None = None):
        support = [sid for sid in supporting if sid in by_id and sid != primary.strategy_id]
        # Never compose an explicit conflict.
        support = [sid for sid in support if sid not in primary.conflicting_strategy_ids]
        return StrategyArchitecture(
            architecture_id=f"arch-{defined_goal.goal_id}-{primary.strategy_id}-{'-'.join(support) or 'core'}",
            primary_strategy_id=primary.strategy_id,
            supporting_strategy_ids=support,
            technique_ids=techniques,
            rationale=rationale,
            trade_offs=primary.trade_offs[:2],
            feasibility_status="conditional" if constraints else "feasible",
            constraints=constraints or [],
        )

    architectures: list[StrategyArchitecture] = []
    primary = ordered[0]

    # Funding gaps favour a funding strategy; supporting strategies can protect liquidity,
    # reduce debt pressure, or allocate existing resources.
    funding = next((s for s in ordered if "fund" in s.name.lower() or s.strategy_id == "strat-calibrated-growth"), None)
    preservation = next((s for s in ordered if s.strategy_id == "strat-cap-preservation"), None)
    debt = next((s for s in ordered if "debt" in s.name.lower()), None)
    allocation = next((s for s in ordered if "allocation" in s.name.lower() or "repriorit" in s.name.lower()), None)
    accumulation = next((s for s in ordered if "accumulation" in s.name.lower()), None)
    derisk = next((s for s in ordered if "de-risk" in s.name.lower()), None)
    income = next((s for s in ordered if "income transition" in s.name.lower()), None)

    if defined_goal.funding_status == "Shortfall" and funding:
        supporting = []
        if preservation and defined_goal.duration_years <= 5:
            supporting.append(preservation.strategy_id)
        if debt and liabilities is not None and liabilities > 0:
            supporting.append(debt.strategy_id)
        if allocation and len(strategies) > 2:
            supporting.append(allocation.strategy_id)
        architectures.append(make(funding, supporting, ["The goal has a funding shortfall, so the architecture prioritises closing the gap."], ["tech-contribution-escalation", "tech-asset-earmarking"]))

    if accumulation and defined_goal.duration_years >= 7:
        supporting = [derisk.strategy_id] if derisk else []
        architectures.append(make(accumulation, supporting, ["The long horizon creates room for an accumulation-led architecture.", "De-risking is treated as a supporting strategy when the goal approaches maturity."], ["tech-glide-path", "tech-asset-earmarking"]))

    if derisk and defined_goal.duration_years <= 7:
        supporting = [preservation.strategy_id] if preservation else []
        architectures.append(make(derisk, supporting, ["As the goal approaches, the architecture prioritises reducing late-horizon funding risk."], ["tech-glide-path", "tech-cashflow-matching"]))

    if income and defined_goal.duration_years <= 5:
        architectures.append(make(income, [preservation.strategy_id] if preservation else [], ["The goal is close enough that converting accumulated resources into dependable cash flows becomes strategically relevant."], ["tech-cashflow-matching", "tech-bucketing"]))

    if debt and liabilities is not None and liabilities > 0:
        architectures.append(make(debt, [funding.strategy_id] if funding else [], ["Liability pressure is material enough to make debt structure part of the goal strategy."], ["tech-goal-segmentation"]))

    if allocation and defined_goal.funding_status in {"Overfunded", "On Track"}:
        architectures.append(make(allocation, [preservation.strategy_id] if preservation else [], ["The goal is already funded or ahead, so resources should be deliberately allocated rather than automatically accumulated further."], ["tech-asset-earmarking", "tech-goal-segmentation"]))

    # Always retain the best eligible strategy as a fallback architecture.
    if not architectures:
        architectures.append(make(primary, [], ["This is the strongest eligible architecture under the currently available goal information."], primary.technique_ids[:3]))

    # De-duplicate architectures while preserving order.
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
