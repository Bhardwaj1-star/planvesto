"""Canonical Strategy Variant Registry.

Variants are reusable implementation paths under a canonical strategy. They do
not replace strategies and do not contain investor-specific calculated values.
Runtime calculations remain in the Strategy/Goal engines.
"""

from dataclasses import dataclass


CANONICAL_VARIANT_SET_VERSION = "1.0"


@dataclass(frozen=True)
class StrategyVariantDefinition:
    variant_id: str
    name: str
    strategy_id: str
    variant_type: str
    description: str
    required_inputs: tuple[str, ...] = ()
    version: str = CANONICAL_VARIANT_SET_VERSION
    active: bool = True


CANONICAL_STRATEGY_VARIANTS: tuple[StrategyVariantDefinition, ...] = (
    StrategyVariantDefinition(
        variant_id="existing_assets",
        name="Existing Assets",
        strategy_id="strat-goal-funding",
        variant_type="existing_asset_funding",
        description="Fund the defined goal from already mapped assets when they cover the requirement.",
        required_inputs=("funding_gap", "mapped_assets"),
    ),
    StrategyVariantDefinition(
        variant_id="sip",
        name="SIP",
        strategy_id="strat-goal-funding",
        variant_type="sip",
        description="Fund the remaining goal requirement through a level recurring contribution.",
        required_inputs=("funding_gap", "annual_return", "duration_years", "available_monthly_surplus"),
    ),
    StrategyVariantDefinition(
        variant_id="lumpsum",
        name="Lumpsum",
        strategy_id="strat-goal-funding",
        variant_type="lumpsum",
        description="Fund the remaining goal requirement through upfront capital.",
        required_inputs=("funding_gap", "annual_return", "duration_years"),
    ),
    StrategyVariantDefinition(
        variant_id="lumpsum_plus_sip",
        name="Lumpsum + SIP",
        strategy_id="strat-goal-funding",
        variant_type="hybrid_funding",
        description="Combine available recurring surplus with an upfront amount for the residual requirement.",
        required_inputs=("funding_gap", "annual_return", "duration_years", "available_monthly_surplus"),
    ),
    StrategyVariantDefinition(
        variant_id="lumpsum_plus_step_up_sip",
        name="Lumpsum + Step-up SIP",
        strategy_id="strat-goal-funding",
        variant_type="hybrid_step_up_funding",
        description="Combine a recurring contribution that escalates annually with upfront capital when required.",
        required_inputs=("funding_gap", "annual_return", "duration_years", "available_monthly_surplus"),
    ),
    StrategyVariantDefinition(
        variant_id="step_up_sip",
        name="Step-up SIP",
        strategy_id="strat-goal-funding",
        variant_type="step_up_sip",
        description="Fund the remaining requirement through a recurring contribution that increases annually.",
        required_inputs=("funding_gap", "annual_return", "duration_years", "available_monthly_surplus"),
    ),
)


def get_canonical_strategy_variants(
    strategy_id: str | None = None,
) -> list[StrategyVariantDefinition]:
    variants = [v for v in CANONICAL_STRATEGY_VARIANTS if v.active]
    if strategy_id is not None:
        variants = [v for v in variants if v.strategy_id == strategy_id]
    return variants


def get_canonical_strategy_variant(variant_id: str) -> StrategyVariantDefinition | None:
    return next(
        (v for v in CANONICAL_STRATEGY_VARIANTS if v.active and v.variant_id == variant_id),
        None,
    )


def validate_strategy_variant_registry(
    variants: list[StrategyVariantDefinition] | tuple[StrategyVariantDefinition, ...] | None = None,
) -> None:
    registry = variants if variants is not None else CANONICAL_STRATEGY_VARIANTS
    ids = [v.variant_id for v in registry]
    if len(ids) != len(set(ids)):
        raise ValueError("Canonical Strategy Variant Registry contains duplicate variant_id values")
    for variant in registry:
        if not variant.variant_id.strip():
            raise ValueError("Canonical Strategy Variant Registry contains an empty variant_id")
        if not variant.strategy_id.strip():
            raise ValueError(f"Variant {variant.variant_id} has an empty parent strategy_id")
        if not variant.name.strip():
            raise ValueError(f"Variant {variant.variant_id} has an empty name")


validate_strategy_variant_registry()
