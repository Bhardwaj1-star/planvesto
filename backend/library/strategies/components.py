"""Canonical Strategy Component Registry.

Components are reusable strategic building blocks. Their activation metadata is
centralized here; orchestration and calculation remain engine responsibilities.
"""

from engines.strategy.components.contracts import StrategyComponent


CANONICAL_COMPONENT_SET_VERSION = "1.0"

CANONICAL_COMPONENTS: tuple[StrategyComponent, ...] = (
    StrategyComponent("component-funding", "funding", "Coordinates resources and future surplus required to close a goal funding requirement.", activation_rules=(("funding_status", "eq", "Shortfall"),)),
    StrategyComponent("component-accumulation", "accumulation", "Builds the resource base over time through disciplined accumulation.", activation_rules=(("duration_years", "gte", 7),)),
    StrategyComponent("component-transition", "transition", "Changes strategic structure as a goal approaches its required date.", activation_rules=(("duration_years", "lte", 7),)),
    StrategyComponent("component-preservation", "preservation", "Protects resources whose loss would materially impair the goal.", activation_rules=(("priority", "eq", "High"),)),
    StrategyComponent("component-liquidity", "liquidity", "Maintains accessible resources needed for near-term or uncertain cash-flow requirements.", activation_rules=(("duration_years", "lte", 5),)),
    StrategyComponent("component-debt", "debt", "Treats liabilities and debt service as a strategic resource-allocation constraint.", activation_rules=(("total_liabilities", "gt", 0), ("emi_burden_monthly", "gte", 0))),
    StrategyComponent("component-credit", "credit", "Evaluates credit as a funding lever alongside other available resources.", activation_rules=(("funding_gap", "gt", 0), ("investable_surplus_monthly", "gt", 0), ("emi_burden_monthly", "gte", 0))),
    StrategyComponent("component-orchestration", "orchestration", "Coordinates competing goals and prevents double-counting of resources.", activation_rules=(("funding_status", "in", ("On Track", "Overfunded")),)),
    StrategyComponent("component-income", "income", "Converts an accumulated resource base into goal-supporting cash flows.", activation_rules=(("duration_years", "lte", 5),)),
)


def get_canonical_components() -> list[StrategyComponent]:
    return list(CANONICAL_COMPONENTS)


def get_canonical_component(component_id: str) -> StrategyComponent | None:
    return next((c for c in CANONICAL_COMPONENTS if c.component_id == component_id), None)


def validate_component_registry(components: list[StrategyComponent] | tuple[StrategyComponent, ...] | None = None) -> None:
    registry = components if components is not None else CANONICAL_COMPONENTS
    ids = [c.component_id for c in registry]
    if len(ids) != len(set(ids)):
        raise ValueError("Canonical Component Registry contains duplicate component_id values")
    for component in registry:
        if not component.component_id.strip():
            raise ValueError("Canonical Component Registry contains an empty component_id")
        if not component.role.strip():
            raise ValueError(f"Component {component.component_id} has an empty role")


validate_component_registry()
