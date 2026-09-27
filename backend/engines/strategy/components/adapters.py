from models.strategy import StrategyDefinition
from .definitions import register_default_components
from .registry import get_component


# Explicit library migration map. Component composition is now driven by the
# strategy record identity rather than by strategy_family semantics.
STRATEGY_TO_COMPONENTS = {
    "strat-calibrated-growth": ("component-funding",),
    "strat-dynamic-accumulation": ("component-accumulation",),
    "strat-high-liquidity-flex": ("component-transition", "component-liquidity"),
    "strat-cap-preservation": ("component-preservation", "component-liquidity"),
    "strat-debt-reduction": ("component-debt",),
    "strat-credit-utilisation": ("component-credit",),
    "strat-goal-reprioritisation": ("component-orchestration",),
    "strat-income-transition": ("component-income", "component-transition"),
}


def component_ids_for_strategy(strategy: StrategyDefinition) -> tuple[str, ...]:
    return STRATEGY_TO_COMPONENTS.get(strategy.strategy_id, ())


def components_for_strategy(strategy: StrategyDefinition):
    register_default_components()
    return [
        component
        for component_id in component_ids_for_strategy(strategy)
        if (component := get_component(component_id)) is not None
    ]


def components_for_strategies(strategies: list[StrategyDefinition]):
    return [(strategy, components_for_strategy(strategy)) for strategy in strategies]
