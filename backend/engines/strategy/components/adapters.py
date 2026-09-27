from models.strategy import StrategyDefinition
from .definitions import register_default_components
from .registry import get_component


# Transitional adapter: existing strategy-library records already carry a
# semantic strategy_family. This lets the new component layer work before every
# library record is explicitly migrated to component metadata.
FAMILY_TO_COMPONENT = {
    "Goal Funding": "component-funding",
    "Growth": "component-accumulation",
    "Transition": "component-transition",
    "Capital Protection": "component-preservation",
    "Credit": "component-debt",
    "Orchestration": "component-orchestration",
    "Income": "component-income",
}


def component_for_strategy(strategy: StrategyDefinition):
    register_default_components()
    component_id = FAMILY_TO_COMPONENT.get(strategy.strategy_family)
    return get_component(component_id) if component_id else None


def components_for_strategies(strategies: list[StrategyDefinition]):
    return [(strategy, component_for_strategy(strategy)) for strategy in strategies]
