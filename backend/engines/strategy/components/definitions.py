from .contracts import StrategyComponent
from .registry import register_component


COMPONENT_DEFINITIONS = (
    StrategyComponent("component-funding", "funding", "Coordinates the resources and future surplus required to close a goal funding requirement."),
    StrategyComponent("component-accumulation", "accumulation", "Builds the resource base over time through disciplined accumulation."),
    StrategyComponent("component-transition", "transition", "Changes the strategic structure as a goal approaches its required date."),
    StrategyComponent("component-preservation", "preservation", "Protects resources whose loss would materially impair the goal."),
    StrategyComponent("component-debt", "debt", "Treats liabilities and debt service as a strategic resource-allocation constraint."),
    StrategyComponent("component-credit", "credit", "Evaluates credit as a funding lever alongside other available resources."),
    StrategyComponent("component-orchestration", "orchestration", "Coordinates competing goals and prevents double-counting of resources."),
    StrategyComponent("component-income", "income", "Converts an accumulated resource base into goal-supporting cash flows."),
)


def register_default_components() -> None:
    for component in COMPONENT_DEFINITIONS:
        if component.component_id not in {c.component_id for c in __import__("engines.strategy.components.registry", fromlist=["get_active_components"]).get_active_components()}:
            register_component(component)
