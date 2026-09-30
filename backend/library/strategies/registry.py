from models.strategy import StrategyDefinition
from library.strategies.catalog import STRATEGY_CATALOG


LIBRARY_VERSION = "2.0"


def validate_strategy_library(strategies: list[StrategyDefinition] | None = None) -> None:
    """Validate the complete Strategy Library at load time."""
    catalog = strategies if strategies is not None else STRATEGY_CATALOG
    ids = [strategy.strategy_id for strategy in catalog]
    if len(ids) != len(set(ids)):
        raise ValueError("Strategy Library contains duplicate strategy_id values")

    for strategy in catalog:
        if strategy.library_version != LIBRARY_VERSION:
            raise ValueError(
                f"Strategy {strategy.strategy_id} uses library_version "
                f"{strategy.library_version}; expected {LIBRARY_VERSION}"
            )


def get_active_strategies() -> list[StrategyDefinition]:
    return [strategy for strategy in STRATEGY_CATALOG if strategy.active]


LEGACY_ALIASES: dict[str, str] = {
    "strat-cap-preservation": "strat-capital-preservation",
}


def get_strategy_by_id(strategy_id: str) -> StrategyDefinition | None:
    resolved_id = LEGACY_ALIASES.get(strategy_id, strategy_id)
    return next(
        (strategy for strategy in get_active_strategies() if strategy.strategy_id == resolved_id),
        None,
    )


validate_strategy_library()
