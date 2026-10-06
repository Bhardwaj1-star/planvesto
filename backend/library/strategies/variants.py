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
    # Progressive De-risking Variants
    StrategyVariantDefinition(
        variant_id="goal_date_glide_path",
        name="Goal-Date Glide Path",
        strategy_id="strat-progressive-de-risking",
        variant_type="glide_path",
        description="Single fixed goal-date transition from growth to stabilisation to liquid as maturity approaches.",
        required_inputs=("duration_years", "future_target", "funding_status"),
    ),
    StrategyVariantDefinition(
        variant_id="payment_tranche_glide_path",
        name="Payment-Tranche Glide Path",
        strategy_id="strat-progressive-de-risking",
        variant_type="staged_glide_path",
        description="Protect the imminent payment tranche while later payment tranches retain growth exposure.",
        required_inputs=("duration_years", "future_target", "funding_status"),
    ),
    StrategyVariantDefinition(
        variant_id="recurring_cashflow_glide_path",
        name="Recurring-Cashflow Glide Path",
        strategy_id="strat-progressive-de-risking",
        variant_type="cyclical_glide_path",
        description="Protect next recurring cycle, execute withdrawal, and rebuild subsequent funding cycle.",
        required_inputs=("duration_years", "future_target", "funding_status"),
    ),
    StrategyVariantDefinition(
        variant_id="income_transition_glide_path",
        name="Income-Transition Glide Path",
        strategy_id="strat-progressive-de-risking",
        variant_type="income_transition",
        description="Staged transition architecture with near-term reserve, intermediate bucket, and long-term compounding bucket.",
        required_inputs=("duration_years", "future_target", "funding_status"),
    ),
    # Capital Preservation Variants
    StrategyVariantDefinition(
        variant_id="full_goal_preservation",
        name="Full-Goal Preservation",
        strategy_id="strat-capital-preservation",
        variant_type="full_preservation",
        description="Preserve the complete required target capital for a near-term or high-priority commitment.",
        required_inputs=("duration_years", "funding_status"),
    ),
    StrategyVariantDefinition(
        variant_id="first_payment_preservation",
        name="First-Payment Preservation",
        strategy_id="strat-capital-preservation",
        variant_type="imminent_preservation",
        description="Ring-fence only the imminent payment requirement while remaining capital maintains growth potential.",
        required_inputs=("duration_years", "funding_status"),
    ),
    StrategyVariantDefinition(
        variant_id="rolling_reserve_preservation",
        name="Rolling Reserve Preservation",
        strategy_id="strat-capital-preservation",
        variant_type="rolling_reserve",
        description="Maintain a protected next-cycle reserve, fund the withdrawal, and systematically rebuild the reserve.",
        required_inputs=("duration_years", "funding_status"),
    ),
    StrategyVariantDefinition(
        variant_id="protected_core_preservation",
        name="Protected-Core Preservation",
        strategy_id="strat-capital-preservation",
        variant_type="core_surplus_preservation",
        description="Protect the identifiable core requirement while deploying surplus resources toward growth opportunities.",
        required_inputs=("duration_years", "funding_status"),
    ),
    # Debt Reduction Variants
    StrategyVariantDefinition(
        variant_id="goal_gap_debt_reduction",
        name="Goal-Gap Debt Reduction",
        strategy_id="strat-debt-reduction",
        variant_type="goal_gap_debt_reduction",
        description="Allocate surplus between debt reduction and goal funding based on binding feasibility constraints.",
        required_inputs=("liabilities", "emi_burden", "surplus"),
    ),
    StrategyVariantDefinition(
        variant_id="emi_relief_debt_reduction",
        name="EMI-Relief Debt Reduction",
        strategy_id="strat-debt-reduction",
        variant_type="emi_relief",
        description="Target high-interest or high-EMI obligations first to free up monthly cash flow for goal commitments.",
        required_inputs=("liabilities", "emi_burden", "surplus"),
    ),
    StrategyVariantDefinition(
        variant_id="residual_gap_debt_reduction",
        name="Residual-Gap Debt Reduction",
        strategy_id="strat-debt-reduction",
        variant_type="residual_debt_reduction",
        description="Direct resources toward reducing debt that prevents reaching minimum goal contribution feasibility.",
        required_inputs=("liabilities", "emi_burden", "surplus"),
    ),
    StrategyVariantDefinition(
        variant_id="goal_linked_debt_reduction",
        name="Goal-Linked Debt Reduction",
        strategy_id="strat-debt-reduction",
        variant_type="goal_linked_debt_reduction",
        description="Accelerate repayment of debt specifically linked to the goal asset.",
        required_inputs=("liabilities", "emi_burden", "surplus"),
    ),
    # Credit Utilisation Variants
    StrategyVariantDefinition(
        variant_id="residual_gap_bridge",
        name="Residual-Gap Bridge",
        strategy_id="strat-credit-utilisation",
        variant_type="residual_bridge",
        description="Fund the remaining capital gap via credit after exhausting existing assets and sustainable surplus.",
        required_inputs=("surplus", "liabilities", "funding_gap"),
    ),
    StrategyVariantDefinition(
        variant_id="partial_goal_financing",
        name="Partial-Goal Financing",
        strategy_id="strat-credit-utilisation",
        variant_type="structured_financing",
        description="Finance a predetermined percentage of the goal via dedicated loans while investing surplus for the balance.",
        required_inputs=("surplus", "liabilities", "funding_gap"),
    ),
    StrategyVariantDefinition(
        variant_id="emi_cap_financing",
        name="EMI-Cap Financing",
        strategy_id="strat-credit-utilisation",
        variant_type="emi_capped_financing",
        description="Structure credit strictly within the investor's verified monthly surplus and safe EMI ceiling.",
        required_inputs=("surplus", "liabilities", "funding_gap"),
    ),
    StrategyVariantDefinition(
        variant_id="timing_bridge_financing",
        name="Timing-Bridge Financing",
        strategy_id="strat-credit-utilisation",
        variant_type="timing_bridge",
        description="Bridge a short-term liquidity mismatch ahead of a known future liquidity event or asset maturity.",
        required_inputs=("surplus", "liabilities", "funding_gap"),
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
