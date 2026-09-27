from models.strategy import StrategyDefinition
from .definitions import register_default_components
from .registry import get_component


def component_ids_for_strategy(strategy: StrategyDefinition) -> tuple[str, ...]:
    """Return component IDs declared by the Strategy Library record."""
    return tuple(strategy.component_ids)


def components_for_strategy(strategy: StrategyDefinition):
    register_default_components()
    return [
        component
        for component_id in component_ids_for_strategy(strategy)
        if (component := get_component(component_id)) is not None
    ]


def components_for_strategies(strategies: list[StrategyDefinition]):
    return [(strategy, components_for_strategy(strategy)) for strategy in strategies]
