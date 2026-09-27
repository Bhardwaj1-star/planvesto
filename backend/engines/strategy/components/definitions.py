from .contracts import StrategyComponent
from .registry import get_active_components, register_component


COMPONENT_DEFINITIONS = (
    StrategyComponent("component-funding", "funding", "Coordinates resources and future surplus required to close a goal funding requirement.", activation_rules=(("funding_status", "eq", "Shortfall"),)),
    StrategyComponent("component-accumulation", "accumulation", "Builds the resource base over time through disciplined accumulation.", activation_rules=(("duration_years", "gte", 7),)),
    StrategyComponent("component-transition", "transition", "Changes strategic structure as a goal approaches its required date.", activation_rules=(("duration_years", "lte", 7),)),
    StrategyComponent("component-preservation", "preservation", "Protects resources whose loss would materially impair the goal."),
    StrategyComponent("component-liquidity", "liquidity", "Maintains accessible resources needed for near-term or uncertain cash-flow requirements."),
    StrategyComponent("component-debt", "debt", "Treats liabilities and debt service as a strategic resource-allocation constraint.", activation_rules=(("total_liabilities", "gt", 0), ("emi_burden_monthly", "gte", 0))),
    StrategyComponent("component-credit", "credit", "Evaluates credit as a funding lever alongside other available resources.", activation_rules=(("funding_gap", "gt", 0), ("investable_surplus_monthly", "gt", 0), ("emi_burden_monthly", "gte", 0))),
    StrategyComponent("component-orchestration", "orchestration", "Coordinates competing goals and prevents double-counting of resources.", activation_rules=(("funding_status", "in", ("On Track", "Overfunded")),)),
    StrategyComponent("component-income", "income", "Converts an accumulated resource base into goal-supporting cash flows.", activation_rules=(("duration_years", "lte", 5),)),
)


def register_default_components() -> None:
    existing = {component.component_id for component in get_active_components()}
    for component in COMPONENT_DEFINITIONS:
        if component.component_id not in existing:
            register_component(component)
