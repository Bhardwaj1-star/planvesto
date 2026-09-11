from models.strategy import StrategyDefinition, StrategyImplementationParamDef


def _pct(name: str, label: str, default: float, minimum: float = 0, maximum: float = 100):
    return StrategyImplementationParamDef(name=name, label=label, param_type="percentage", description=label, default_value=default, min_value=minimum, max_value=maximum)


def _years(name: str, label: str, default: int, minimum: int = 1, maximum: int = 30):
    return StrategyImplementationParamDef(name=name, label=label, param_type="integer", description=label, default_value=default, min_value=minimum, max_value=maximum)


STRATEGY_CATALOG: list[StrategyDefinition] = [
    StrategyDefinition(
        strategy_id="strat-calibrated-growth", name="Goal Funding", tagline="Close a defined goal-funding gap with the right mix of resources and future surplus.",
        description="A goal-specific funding architecture that decides how the target should be funded rather than selecting products.", strategy_family="Goal Funding",
        strategic_objective="Fund a defined goal by coordinating existing resources, future surplus, time and other permitted levers.", core_mechanism="Match the funding requirement with available and future resources.",
        principles=["Goal first", "Use existing resources deliberately", "Make funding trade-offs explicit"], constraints=["Cannot invent unavailable surplus or resources"],
        dependencies=["Defined Goal", "Financial State"], required_inputs=["future_target", "funding_gap", "duration_years", "financial_state"],
        applicable_goal_characteristics=["shortfall", "on_track"], applicable_goal_types=["Child Education", "Child Marriage", "Home Purchase", "Vehicle", "Travel", "Business", "Retirement", "Wealth Creation", "Other"],
        technique_ids=["tech-asset-earmarking", "tech-contribution-escalation", "tech-cashflow-matching"], strategic_levers=["existing_assets", "future_surplus", "time", "goal_amount", "funding_source"],
        good_outcomes=["Explicitly closes or measures the remaining funding gap."], bad_outcomes=["May require higher contributions, a longer horizon, or a modified goal."], trade_offs=["Funding certainty versus contribution burden."],
        implementation_parameters=[_pct("existing_asset_utilisation_pct", "Existing Asset Utilisation (%)", 50)], baseline_safety_score=7.5, baseline_liquidity_score=7.0, baseline_growth_score=7.5, baseline_flexibility_score=8.0,
    ),
    StrategyDefinition(
        strategy_id="strat-dynamic-accumulation", name="Long-Term Accumulation", tagline="Build resources over a long horizon through disciplined accumulation.",
        description="A growth-oriented strategic architecture for goals with sufficient time to accumulate resources.", strategy_family="Growth",
        strategic_objective="Build the required resource base over a long horizon.", core_mechanism="Sustained contributions plus long-horizon compounding.", principles=["Time is a strategic resource", "Consistency matters", "Avoid premature goal-risk concentration"],
        constraints=["Requires sufficient horizon and sustainable surplus"], dependencies=["Defined Goal", "Financial State"], required_inputs=["duration_years", "future_target", "surplus"],
        applicable_goal_characteristics=["long_term", "shortfall"], applicable_goal_types=["Retirement", "Wealth Creation", "Child Education", "Child Marriage", "Business", "Other"],
        technique_ids=["tech-contribution-escalation", "tech-goal-segmentation"], strategic_levers=["future_surplus", "time", "goal_amount"],
        good_outcomes=["Uses a long horizon to reduce the required funding intensity."], bad_outcomes=["The architecture can be disrupted by a short remaining horizon or weak surplus."], trade_offs=["Long-term growth potential versus patience and contribution discipline."],
        implementation_parameters=[_years("accumulation_horizon_years", "Accumulation Horizon (Years)", 10, 1, 40)], baseline_safety_score=5.8, baseline_liquidity_score=6.8, baseline_growth_score=9.3, baseline_flexibility_score=7.0,
    ),
    StrategyDefinition(
        strategy_id="strat-high-liquidity-flex", name="Progressive De-risking", tagline="Reduce goal-funding uncertainty as the target date approaches.",
        description="A strategic transition from growth-oriented resources toward greater certainty as a goal becomes imminent.", strategy_family="Transition",
        strategic_objective="Protect achieved goal funding from late-horizon shocks.", core_mechanism="Progressively change the strategic exposure as time-to-goal falls.", principles=["De-risk with purpose", "Protect funded capital near the goal", "Do not de-risk prematurely without reason"],
        constraints=["Requires a measurable goal horizon"], dependencies=["Defined Goal"], required_inputs=["duration_years", "future_target", "funding_status"],
        applicable_goal_characteristics=["near_term", "fixed_timeline", "on_track", "shortfall"], applicable_goal_types=["Child Education", "Child Marriage", "Home Purchase", "Vehicle", "Retirement", "Business", "Other"],
        technique_ids=["tech-glide-path", "tech-bucketing", "tech-cashflow-matching"], strategic_levers=["time", "resource_allocation"],
        good_outcomes=["Reduces the probability that a late market shock derails an approaching goal."], bad_outcomes=["Earlier de-risking can reduce growth potential."], trade_offs=["Funding certainty versus remaining growth opportunity."],
        implementation_parameters=[_years("derisking_window_years", "De-risking Window (Years)", 5, 1, 15)], baseline_safety_score=8.2, baseline_liquidity_score=8.0, baseline_growth_score=6.2, baseline_flexibility_score=8.0,
    ),
    StrategyDefinition(
        strategy_id="strat-cap-preservation", name="Capital Preservation", tagline="Preserve resources where loss of capital would materially threaten the goal.",
        description="A defensive strategic architecture for critical or near-term funding requirements.", strategy_family="Capital Protection",
        strategic_objective="Prioritise preservation and predictability of resources required for the goal.", core_mechanism="Reduce exposure to outcomes that could materially impair required capital.", principles=["Preserve what the goal needs", "Liquidity matters", "Avoid false certainty"],
        constraints=["May reduce long-term growth potential"], dependencies=["Defined Goal", "Financial State"], required_inputs=["duration_years", "funding_status", "goal_priority"],
        applicable_goal_characteristics=["near_term", "fixed_timeline", "high_priority"], applicable_goal_types=["Emergency Fund", "Child Education", "Child Marriage", "Home Purchase", "Vehicle", "Retirement", "Travel", "Business", "Other"],
        technique_ids=["tech-bucketing", "tech-laddering", "tech-cashflow-matching"], strategic_levers=["existing_assets", "resource_allocation", "time"],
        good_outcomes=["Improves predictability of required goal resources."], bad_outcomes=["Can sacrifice growth if used too early or too broadly."], trade_offs=["Capital certainty versus growth and opportunity cost."],
        implementation_parameters=[_pct("preservation_allocation_pct", "Preservation Allocation (%)", 75, 25)], baseline_safety_score=9.3, baseline_liquidity_score=8.2, baseline_growth_score=5.0, baseline_flexibility_score=8.5,
    ),
    StrategyDefinition(
        strategy_id="strat-debt-reduction", name="Debt Reduction", tagline="Reduce debt pressure when liabilities constrain the goal strategy.",
        description="Treat debt as a resource-allocation constraint and determine when reducing it improves goal feasibility.", strategy_family="Credit",
        strategic_objective="Reduce liability burden where it is materially constraining cash flow or goal funding.", core_mechanism="Redirect resources toward liability reduction when the trade-off is favourable.", principles=["Debt is neither inherently good nor bad", "Evaluate cost and cash-flow impact", "Protect essential liquidity"],
        constraints=["Debt reduction must not create an unsafe liquidity position"], dependencies=["Financial State"], required_inputs=["liabilities", "emi_burden", "surplus", "goal_priority"],
        applicable_goal_characteristics=["shortfall", "high_priority"], applicable_goal_types=["Retirement", "Home Purchase", "Child Education", "Business", "Vehicle", "Other"],
        technique_ids=["tech-goal-segmentation", "tech-cashflow-matching"], strategic_levers=["debt_structure", "future_surplus", "resource_allocation"],
        good_outcomes=["Can release future cash flow and reduce a binding financial constraint."], bad_outcomes=["Aggressive repayment can reduce liquidity available for other needs."], trade_offs=["Debt cost and flexibility versus immediate resource deployment."],
        implementation_parameters=[_pct("surplus_to_debt_pct", "Surplus Directed to Debt (%)", 30)], baseline_safety_score=8.3, baseline_liquidity_score=6.5, baseline_growth_score=6.0, baseline_flexibility_score=7.0,
    ),
    StrategyDefinition(
        strategy_id="strat-credit-utilisation", name="Credit Utilisation", tagline="Use credit deliberately when it improves goal feasibility without creating an unacceptable burden.",
        description="Evaluate credit as one funding lever alongside assets, surplus and time; it does not imply automatically taking more debt.", strategy_family="Credit",
        strategic_objective="Determine whether credit can efficiently bridge a timing or funding mismatch.", core_mechanism="Compare credit cost, cash-flow burden, liquidity preservation and alternatives.", principles=["Credit is a tool", "Assess affordability", "Compare against non-credit alternatives"],
        constraints=["Requires sustainable cash flow and acceptable obligations"], dependencies=["Financial State"], required_inputs=["surplus", "liabilities", "emi_burden", "funding_gap"],
        applicable_goal_characteristics=["shortfall", "near_term"], applicable_goal_types=["Home Purchase", "Vehicle", "Business", "Child Education", "Other"],
        technique_ids=["tech-cashflow-matching", "tech-goal-segmentation"], strategic_levers=["credit", "time", "existing_assets", "future_surplus"],
        good_outcomes=["Can preserve liquidity or bridge a timing mismatch when affordable."], bad_outcomes=["Interest cost and repayment obligations can weaken future flexibility."], trade_offs=["Liquidity preservation and timing versus financing cost and obligation."],
        implementation_parameters=[_pct("credit_share_of_gap_pct", "Credit Share of Funding Gap (%)", 25)], baseline_safety_score=5.8, baseline_liquidity_score=8.0, baseline_growth_score=6.0, baseline_flexibility_score=7.5,
    ),
    StrategyDefinition(
        strategy_id="strat-goal-reprioritisation", name="Goal Reprioritisation & Resource Allocation", tagline="Coordinate competing goals when one resource base cannot fully satisfy all objectives.",
        description="An investor-level orchestration strategy that makes competing goal priorities and resource allocation explicit.", strategy_family="Orchestration",
        strategic_objective="Allocate finite resources across competing goals without double-counting them.", core_mechanism="Rank goals, earmark resources, identify conflicts and make trade-offs explicit.", principles=["Resources are finite", "One asset cannot be fully promised twice", "Investor decides trade-offs"],
        constraints=["Requires a multi-goal view of resources and priorities"], dependencies=["Defined Goals", "Financial State"], required_inputs=["goal_priorities", "assets", "surplus", "liabilities"],
        applicable_goal_characteristics=["shortfall", "on_track", "overfunded"], applicable_goal_types=["Retirement", "Home Purchase", "Child Education", "Child Marriage", "Business", "Vehicle", "Travel", "Wealth Creation", "Other"],
        technique_ids=["tech-asset-earmarking", "tech-goal-segmentation"], strategic_levers=["goal_priority", "resource_allocation", "existing_assets", "future_surplus", "time"],
        good_outcomes=["Makes competing-goal trade-offs visible and prevents resource double counting."], bad_outcomes=["A lower-priority goal may receive fewer resources or a later target."], trade_offs=["One goal's certainty can require another goal's deferral or reduced funding."],
        implementation_parameters=[], baseline_safety_score=8.0, baseline_liquidity_score=7.5, baseline_growth_score=7.0, baseline_flexibility_score=9.0,
    ),
    StrategyDefinition(
        strategy_id="strat-income-transition", name="Income Transition", tagline="Convert an accumulated resource base into dependable goal-supporting cash flows.",
        description="A transition architecture for goals where the question shifts from accumulation to dependable cash-flow support.", strategy_family="Income",
        strategic_objective="Create a sustainable transition from accumulation into required income or withdrawals.", core_mechanism="Align resources, timing and expected cash flows with the post-transition need.", principles=["Cash flow is the objective", "Sequence matters", "Preserve flexibility where possible"],
        constraints=["Requires clarity on expected income need and available resources"], dependencies=["Defined Goal", "Financial State"], required_inputs=["future_target", "duration_years", "income_need"],
        applicable_goal_characteristics=["near_term", "on_track", "high_priority"], applicable_goal_types=["Retirement", "Business", "Other"],
        technique_ids=["tech-cashflow-matching", "tech-bucketing", "tech-tax-efficient-sequencing"], strategic_levers=["existing_assets", "resource_allocation", "time"],
        good_outcomes=["Aligns accumulated resources with future cash-flow requirements."], bad_outcomes=["Poor sequencing can create liquidity or longevity pressure."], trade_offs=["Current income certainty versus flexibility and remaining growth."],
        implementation_parameters=[_years("transition_window_years", "Income Transition Window (Years)", 3, 1, 15)], baseline_safety_score=8.5, baseline_liquidity_score=8.5, baseline_growth_score=5.5, baseline_flexibility_score=8.2,
    ),
]


def get_all_strategies() -> list[StrategyDefinition]:
    return list(STRATEGY_CATALOG)
