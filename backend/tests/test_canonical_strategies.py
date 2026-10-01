from library.strategies.canonical import (
    CANONICAL_STRATEGIES,
    get_canonical_strategy,
    get_canonical_strategies,
)
from library.strategies.catalog import STRATEGY_CATALOG
from library.strategies.registry import get_active_strategies, validate_strategy_library


def test_canonical_strategy_registry_has_unique_ids():
    ids = [strategy.strategy_id for strategy in CANONICAL_STRATEGIES]
    assert ids
    assert len(ids) == len(set(ids))


def test_canonical_registry_is_catalog_source_of_truth():
    assert STRATEGY_CATALOG is CANONICAL_STRATEGIES
    assert get_canonical_strategies() == CANONICAL_STRATEGIES


def test_canonical_strategy_lookup():
    strategy = get_canonical_strategy("strat-goal-funding")
    assert strategy is not None
    assert strategy.name == "Goal Funding"


def test_active_strategy_registry_consumes_canonical_registry():
    assert [s.strategy_id for s in get_active_strategies()] == [
        s.strategy_id for s in CANONICAL_STRATEGIES if s.active
    ]
    validate_strategy_library()
