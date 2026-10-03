"""Canonical Strategy Registry.

The Strategy Library definitions live here as the single source of truth.
Compatibility consumers should import through this module or the catalog shim.
"""

from models.strategy import StrategyDefinition, StrategyImplementationParamDef


def _pct(name: str, label: str, default: float, minimum: float = 0, maximum: float = 100):
    return StrategyImplementationParamDef(name=name, label=label, param_type="percentage", description=label, default_value=default, min_value=minimum, max_value=maximum)


def _years(name: str, label: str, default: int, minimum: int = 1, maximum: int = 30):
    return StrategyImplementationParamDef(name=name, label=label, param_type="integer", description=label, default_value=default, min_value=minimum, max_value=maximum)


# Strategy library contains goal-level strategy architectures only.
# Multi-goal orchestration is intentionally handled outside this catalog.
BASE = dict(library_version="2.0", implementation_version="2.0")

GOAL_TYPES = [
    "emergency_fund",
    "debt_freedom",
    "education",
    "marriage",
    "home",
    "home_improvement",
    "vehicle",
    "travel",
    "retirement",
    "financial_independence",
    "family_care",
    "healthcare",
    "business",
    "lifestyle",
    "wealth_creation",
    "legacy_giving",
    "other",
]

CORPUS_GOAL_TYPES = [g for g in GOAL_TYPES if g not in {"emergency_fund", "debt_freedom"}]

CANONICAL_STRATEGIES: list[StrategyDefinition] = [
    StrategyDefinition(
        strategy_id="strat-goal-funding",
        name="Goal Funding",
        tagline="Fund a defined goal using the appropriate mix of existing resources, future surplus and time.",
        description="The unified goal-funding architecture. It covers immediate, medium-term and long-term funding requirements. Long-term accumulation and income-transition approaches are variants within this architecture rather than separate strategies.",
        strategy_family="Goal Funding",
        strategic_objective="Achieve the defined goal funding requirement.",
        core_mechanism="Match the future funding requirement with existing assets, future surplus, time, goal amount and appropriate funding sources.",
        principles=["Start from the defined goal and funding gap.", "Use existing resources before assuming new contributions where appropriate.", "Adapt contribution, timing or target when the original funding path is infeasible.", "Long-term accumulation is a funding variant, not a separate strategy.", "Income transition is a funding variant when the goal requires future cash-flow generation."],
        required_inputs=["future_target", "funding_gap", "duration_years", "financial_state"],
        applicable_goal_characteristics=["shortfall", "on_track", "overfunded", "near_term", "long_term", "fixed_timeline", "flexible_timeline", "high_priority"],
        applicable_goal_types=GOAL_TYPES,
        technique_ids=["tech-asset-earmarking", "tech-contribution-escalation", "tech-cashflow-matching", "tech-bucketing", "tech-tax-efficient-sequencing"],
        strategic_levers=["existing_assets", "future_surplus", "time", "goal_amount", "funding_source"],
        component_ids=["component-funding"],
        primary_component_ids=["component-funding"],
        activation_characteristics=["shortfall", "on_track", "overfunded"],
        implementation_parameters=[_pct("existing_asset_utilisation_pct", "Existing Asset Utilisation (%)", 50)],
        trade_offs=["Funding certainty versus contribution burden.", "Goal certainty versus flexibility in timing or target.", "Growth opportunity versus funding reliability."],
        baseline_safety_score=7.5,
        baseline_liquidity_score=7.0,
        baseline_growth_score=7.5,
        baseline_flexibility_score=8.0,
        **BASE,
    ),
    StrategyDefinition(
        strategy_id="strat-progressive-de-risking",
        name="Progressive De-risking",
        tagline="Reduce goal-funding uncertainty as the target date approaches.",
        description="A time-dependent transition architecture that progressively reduces exposure to adverse late-horizon outcomes as a funded goal approaches.",
        strategy_family="Goal Protection",
        strategic_objective="Protect achieved goal funding while preserving appropriate growth opportunity earlier in the horizon.",
        core_mechanism="Progressively change the strategic exposure as time-to-goal falls.",
        principles=["Risk reduction is progressive, not an immediate switch to preservation.", "The de-risking window is driven by time-to-goal and funding sensitivity.", "This strategy protects an already-funded or partially-funded goal; it does not replace the funding strategy itself."],
        required_inputs=["duration_years", "future_target", "funding_status"],
        applicable_goal_characteristics=["near_term", "fixed_timeline", "on_track", "shortfall"],
        applicable_goal_types=CORPUS_GOAL_TYPES,
        technique_ids=["tech-glide-path", "tech-bucketing", "tech-cashflow-matching"],
        strategic_levers=["time", "resource_allocation"],
        component_ids=["component-transition", "component-liquidity"],
        primary_component_ids=["component-transition"],
        supporting_component_ids=["component-liquidity"],
        activation_characteristics=["near_term", "fixed_timeline", "on_track", "shortfall"],
        implementation_parameters=[_years("derisking_window_years", "De-risking Window (Years)", 5, 1, 15)],
        trade_offs=["Funding certainty versus remaining growth opportunity."],
        baseline_safety_score=8.8,
        baseline_liquidity_score=9.6,
        baseline_growth_score=6.2,
        baseline_flexibility_score=8.5,
        **BASE,
    ),
    StrategyDefinition(
        strategy_id="strat-capital-preservation",
        name="Capital Preservation",
        tagline="Preserve resources where loss would materially threaten the goal.",
        description="A defensive architecture used when capital certainty and predictability take precedence over additional growth opportunity.",
        strategy_family="Goal Protection",
        strategic_objective="Prioritise preservation and predictability of required capital.",
        core_mechanism="Reduce exposure to outcomes that could materially impair required capital.",
        principles=["Use when the goal is sensitive to capital loss.", "Prioritise preservation where recovery time is insufficient.", "Do not treat preservation as a default investment strategy for every goal."],
        required_inputs=["duration_years", "funding_status", "goal_priority"],
        applicable_goal_characteristics=["near_term", "fixed_timeline", "high_priority", "shortfall", "on_track"],
        applicable_goal_types=CORPUS_GOAL_TYPES,
        technique_ids=["tech-bucketing", "tech-laddering", "tech-cashflow-matching"],
        strategic_levers=["existing_assets", "resource_allocation", "time"],
        component_ids=["component-preservation", "component-liquidity"],
        primary_component_ids=["component-preservation"],
        supporting_component_ids=["component-liquidity"],
        activation_characteristics=["near_term", "fixed_timeline", "high_priority"],
        implementation_parameters=[_pct("preservation_allocation_pct", "Preservation Allocation (%)", 75, 25)],
        trade_offs=["Capital certainty versus growth and opportunity cost."],
        baseline_safety_score=9.3,
        baseline_liquidity_score=8.2,
        baseline_growth_score=5.0,
        baseline_flexibility_score=8.5,
        **BASE,
    ),
    StrategyDefinition(
        strategy_id="strat-debt-reduction",
        name="Debt Reduction",
        tagline="Reduce debt pressure when liabilities materially constrain the goal plan.",
        description="A liability-management architecture that redirects available resources toward reducing material debt burden when doing so improves overall goal feasibility.",
        strategy_family="Liability Management",
        strategic_objective="Reduce liability burden where it materially constrains goal funding or financial resilience.",
        core_mechanism="Compare debt cost and burden with alternative uses of surplus, then allocate appropriate resources toward liability reduction.",
        principles=["Debt reduction is a resource-allocation decision, not an automatic recommendation.", "The strategy can support a Debt Repayment goal or act as a supporting strategy for another goal.", "Debt cost, liquidity and goal priority must be evaluated together."],
        required_inputs=["liabilities", "emi_burden", "surplus", "goal_priority"],
        applicable_goal_characteristics=["shortfall", "high_priority"],
        applicable_goal_types=GOAL_TYPES,
        technique_ids=["tech-goal-segmentation", "tech-cashflow-matching"],
        strategic_levers=["debt_structure", "future_surplus", "resource_allocation"],
        component_ids=["component-debt"],
        primary_component_ids=["component-debt"],
        activation_characteristics=["shortfall", "high_priority"],
        implementation_parameters=[_pct("surplus_to_debt_pct", "Surplus Directed to Debt (%)", 30)],
        trade_offs=["Debt cost reduction versus immediate deployment of resources toward the goal."],
        baseline_safety_score=8.3,
        baseline_liquidity_score=6.5,
        baseline_growth_score=6.0,
        baseline_flexibility_score=7.0,
        **BASE,
    ),
    StrategyDefinition(
        strategy_id="strat-credit-utilisation",
        name="Credit Utilisation",
        tagline="Evaluate credit deliberately when it can improve goal feasibility.",
        description="A financing architecture that evaluates credit as one possible funding lever rather than assuming borrowing is appropriate.",
        strategy_family="Financing",
        strategic_objective="Determine whether credit can responsibly bridge a funding or timing mismatch.",
        core_mechanism="Compare credit cost, repayment burden, liquidity impact and alternatives before using credit.",
        principles=["Credit is a funding lever, not a default solution.", "Borrowing must be assessed against repayment capacity and alternative funding paths.", "The strategy can be selected only when the financing trade-off improves overall goal feasibility."],
        required_inputs=["surplus", "liabilities", "emi_burden", "funding_gap"],
        applicable_goal_characteristics=["shortfall", "near_term", "fixed_timeline"],
        applicable_goal_types=["education", "marriage", "home", "vehicle", "other"],
        technique_ids=["tech-cashflow-matching", "tech-goal-segmentation"],
        strategic_levers=["credit", "time", "existing_assets", "future_surplus"],
        component_ids=["component-credit"],
        primary_component_ids=["component-credit"],
        activation_characteristics=["shortfall", "near_term", "fixed_timeline"],
        implementation_parameters=[_pct("credit_share_of_gap_pct", "Credit Share of Funding Gap (%)", 25)],
        trade_offs=["Liquidity preservation and timing versus financing cost and future obligation."],
        baseline_safety_score=5.8,
        baseline_liquidity_score=8.0,
        baseline_growth_score=6.0,
        baseline_flexibility_score=7.5,
        **BASE,
    ),
]


def get_canonical_strategies() -> list[StrategyDefinition]:
    return list(CANONICAL_STRATEGIES)


def get_canonical_strategy(strategy_id: str) -> StrategyDefinition | None:
    return next((strategy for strategy in CANONICAL_STRATEGIES if strategy.strategy_id == strategy_id), None)
