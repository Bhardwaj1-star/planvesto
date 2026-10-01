from engines.strategy.applicability import filter_applicable_strategies
from engines.strategy.components.adapters import components_for_strategy
from library.strategies.canonical import CANONICAL_STRATEGIES
from library.strategies.components import CANONICAL_COMPONENTS
from library.strategies.techniques_canonical import get_canonical_technique


def test_strategy_applicability_consumes_canonical_strategy_registry():
    canonical_ids = {s.strategy_id for s in CANONICAL_STRATEGIES}
    strategies = filter_applicable_strategies(goal_type="Retirement / Financial Freedom")
    assert strategies
    assert {s.strategy_id for s in strategies} <= canonical_ids


def test_component_adapter_resolves_canonical_components():
    goal_funding = next(s for s in CANONICAL_STRATEGIES if s.strategy_id == "strat-goal-funding")
    components = components_for_strategy(goal_funding)
    assert components
    canonical_ids = {c.component_id for c in CANONICAL_COMPONENTS}
    assert {c.component_id for c in components} <= canonical_ids


def test_strategy_technique_references_resolve_canonically():
    for strategy in CANONICAL_STRATEGIES:
        for technique_id in strategy.technique_ids:
            assert get_canonical_technique(technique_id) is not None
