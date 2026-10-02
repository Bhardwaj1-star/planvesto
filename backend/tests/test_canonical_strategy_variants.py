from library.strategies.variants import (
    CANONICAL_STRATEGY_VARIANTS,
    get_canonical_strategy_variant,
    get_canonical_strategy_variants,
    validate_strategy_variant_registry,
)


def test_canonical_strategy_variant_registry_has_unique_ids():
    ids = [v.variant_id for v in CANONICAL_STRATEGY_VARIANTS]
    assert ids
    assert len(ids) == len(set(ids))
    validate_strategy_variant_registry()


def test_goal_funding_variants_are_canonical():
    variants = get_canonical_strategy_variants("strat-goal-funding")
    assert [v.variant_id for v in variants] == [
        "existing_assets",
        "sip",
        "lumpsum",
        "lumpsum_plus_sip",
        "lumpsum_plus_step_up_sip",
        "step_up_sip",
    ]


def test_canonical_variant_lookup():
    variant = get_canonical_strategy_variant("step_up_sip")
    assert variant is not None
    assert variant.strategy_id == "strat-goal-funding"
    assert variant.name == "Step-up SIP"


def test_runtime_goal_funding_uses_canonical_variant_metadata():
    from engines.goal.funding_strategies import build_goal_funding_strategies

    variants = build_goal_funding_strategies(
        funding_gap=100000,
        annual_return=0.08,
        duration_years=10,
        available_monthly_surplus=5000,
    )
    canonical = {v.variant_id: v for v in CANONICAL_STRATEGY_VARIANTS}
    assert variants
    for variant in variants:
        definition = canonical[variant["strategy_id"]]
        assert variant["strategy_name"] == definition.name
        assert variant["strategy_type"] == definition.variant_type
