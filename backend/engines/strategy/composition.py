from models.defined_goal import DefinedGoal
from models.strategy import StrategyArchitecture, StrategyDefinition
from engines.strategy.components.adapters import components_for_strategy
from library.strategies.components import get_canonical_component
from library.strategies.techniques_canonical import get_canonical_technique
from library.strategies.solution_matrix import get_strategy_solutions
from rules.goals import canonical_goal_priority


def compose_architectures(
    strategies: list[StrategyDefinition],
    defined_goal: DefinedGoal,
    financial_context: dict | None = None,
) -> list[StrategyArchitecture]:
    """Compose goal-specific architectures from canonical strategy solutions and components."""
    context = {
        "duration_years": defined_goal.duration_years,
        "funding_status": defined_goal.funding_status,
        "priority": canonical_goal_priority(defined_goal.priority).title(),
        **(financial_context or {}),
    }
    diagnostics = context.get("rule_diagnostics", [])
    diagnostic_constraints = [
        d.get("message", "")
        for d in diagnostics
        if not d.get("passed", True)
        and d.get("severity") in {"critical", "warning"}
        and d.get("message")
    ]
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
        return all(
            a.can_combine_with(b)
            for a in by_id[primary.strategy_id][1]
            for b in by_id[candidate.strategy_id][1]
        )

    def make(primary, supporting, reason):
        support = [s for s in supporting if can_support(primary, s)]
        components = by_id[primary.strategy_id][1] + [
            c for s in support for c in by_id[s.strategy_id][1]
        ]
        constraints = list(primary.constraints)

        solutions = get_strategy_solutions(
            strategy_id=primary.strategy_id,
            goal_type=defined_goal.goal_type,
        )
        missing_components = [
            cid for cid in primary.component_ids
            if get_canonical_component(cid) is None
        ]
        missing_techniques = [
            tid for tid in primary.technique_ids
            if get_canonical_technique(tid) is None
        ]

        if missing_components:
            constraints.append(
                "Unknown canonical components: " + ", ".join(missing_components)
            )
        if missing_techniques:
            constraints.append(
                "Unknown canonical techniques: " + ", ".join(missing_techniques)
            )
        if not solutions:
            constraints.append(
                f"No canonical solutions mapped for strategy {primary.strategy_id} and goal type {defined_goal.goal_type}."
            )

        missing = [x for x in primary.required_inputs if x not in context]
        if missing:
            constraints.append(f"Missing strategy inputs: {', '.join(missing)}")
        constraints.extend(diagnostic_constraints)

        rationale = [
            reason,
            f"Primary components: {', '.join(c.role for c in by_id[primary.strategy_id][1])}.",
            f"Applicable solutions: {', '.join(s.name for s in solutions)}."
            if solutions
            else "Applicable solutions: none.",
        ]
        if support:
            rationale.append(
                f"Supporting components: {', '.join(c.role for c in components[len(by_id[primary.strategy_id][1]):])}."
            )
        if diagnostic_constraints:
            rationale.append(
                "Financial-state constraints are carried into implementation without changing the priority-based ranking."
            )

        return StrategyArchitecture(
            architecture_id=f"arch-{defined_goal.goal_id}-{primary.strategy_id}-{'-'.join(s.strategy_id for s in support) or 'core'}",
            primary_strategy_id=primary.strategy_id,
            supporting_strategy_ids=[s.strategy_id for s in support],
            solution_ids=[s.solution_id for s in solutions],
            technique_ids=list(primary.technique_ids),
            rationale=rationale,
            trade_offs=primary.trade_offs[:2],
            feasibility_status="conditional" if missing or diagnostic_constraints or not solutions else "feasible",
            constraints=constraints,
        )

    architectures = []
    for candidate in ordered:
        primary_components = by_id[candidate.strategy_id][1]
        preferred = [c for c in primary_components if c.is_preferred(context)]
        if preferred:
            preferred_roles = {c.role for c in preferred}
            supports = [
                s for s in ordered
                if any(c.role not in preferred_roles for c in by_id[s.strategy_id][1])
            ]
            reason = "Architecture activated by component metadata: " + ", ".join(c.role for c in preferred)
            architectures.append(make(candidate, supports, reason))
        else:
            architectures.append(
                make(
                    candidate,
                    [],
                    "Architecture retained for the eligible strategy; no preferred component activation matched the current context.",
                )
            )

    unique, seen = [], set()
    for architecture in architectures:
        key = (architecture.primary_strategy_id, tuple(architecture.supporting_strategy_ids))
        if key not in seen:
            seen.add(key)
            unique.append(architecture)
    return unique
