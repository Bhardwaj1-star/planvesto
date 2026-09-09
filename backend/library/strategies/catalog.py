from models.strategy import StrategyDefinition, StrategyImplementationParamDef

STRATEGY_CATALOG: list[StrategyDefinition] = [
    StrategyDefinition(
        strategy_id="strat-cap-preservation",
        name="Capital Preservation & Guaranteed Yield Strategy",
        tagline="Maximum principal protection with predictable, inflation-hedged yields.",
        description=(
            "Designed for critical capital milestones where downside preservation is paramount. "
            "Focuses on fixed-income security, debt stability, and defensive capital allocation."
        ),
        applicable_goal_types=[
            "Emergency Fund",
            "Child Education",
            "Child Marriage",
            "Home Purchase",
            "Vehicle",
            "Retirement",
            "Travel",
            "Business",
            "Wealth Creation",
            "Other",
        ],
        implementation_parameters=[
            StrategyImplementationParamDef(
                name="debt_allocation_pct",
                label="Debt / Fixed-Income Allocation (%)",
                param_type="percentage",
                description="Percentage of corpus deployed into capital-protected debt avenues.",
                default_value=75.0,
                min_value=50.0,
                max_value=100.0,
            ),
            StrategyImplementationParamDef(
                name="lockin_period_years",
                label="Lock-in Commitment (Years)",
                param_type="integer",
                description="Selected fixed-term lock-in period for sovereign/guaranteed yields.",
                default_value=3,
                min_value=1,
                max_value=10,
            ),
            StrategyImplementationParamDef(
                name="emergency_liquidity_buffer",
                label="Emergency Liquidity Buffer (₹)",
                param_type="currency",
                description="Unencumbered liquidity carve-out retained in liquid avenues.",
                default_value=100000.0,
                min_value=0.0,
            ),
        ],
        good_outcomes=[
            "Zero principal loss risk during turbulent market cycles.",
            "High milestone predictability with guaranteed accumulation curve.",
            "Complete emotional insulation from equity market volatility.",
        ],
        bad_outcomes=[
            "Substantial opportunity cost during broader equity bull markets.",
            "Corpus may fall slightly behind unexpected structural inflation surges.",
        ],
        trade_offs=[
            "Trades away upside growth potential in exchange for guaranteed milestone certainty.",
            "Requires higher periodic or initial capital compared to equity-heavy avenues.",
        ],
        baseline_safety_score=9.2,
        baseline_liquidity_score=7.8,
        baseline_growth_score=5.8,
        baseline_flexibility_score=8.0,
    ),
    StrategyDefinition(
        strategy_id="strat-calibrated-growth",
        name="Calibrated Core Growth & Dynamic Hedging Strategy",
        tagline="Balanced compounding engine combining calibrated equity upside with defensive hedging.",
        description=(
            "Optimizes capital growth while keeping maximum drawdown strictly bounded. "
            "Blends diversified core index equities with defensive fixed-income buffers."
        ),
        applicable_goal_types=[
            "Child Education",
            "Child Marriage",
            "Home Purchase",
            "Retirement",
            "Wealth Creation",
            "Business",
            "Vehicle",
            "Other",
        ],
        implementation_parameters=[
            StrategyImplementationParamDef(
                name="equity_allocation_pct",
                label="Core Equity Allocation (%)",
                param_type="percentage",
                description="Target percentage dedicated to diversified equity compounding.",
                default_value=60.0,
                min_value=30.0,
                max_value=80.0,
            ),
            StrategyImplementationParamDef(
                name="rebalancing_cadence",
                label="Portfolio Rebalancing Cadence",
                param_type="choice",
                description="Rule-based trigger to rebalance back to target weights.",
                default_value="Annual",
                choices=["Semi-Annual", "Annual", "Threshold-Based (5%)"],
            ),
            StrategyImplementationParamDef(
                name="down_payment_quantum",
                label="Initial Down Payment / Upfront Reallocation (₹)",
                param_type="currency",
                description="Initial lump-sum commitment deployed at strategy inception.",
                default_value=250000.0,
                min_value=0.0,
            ),
        ],
        good_outcomes=[
            "Substantially outpaces baseline inflation over 4+ year horizons.",
            "Reduces periodic capital requirement compared to conservative models.",
            "Dynamic hedging insulates milestone readiness from sharp market corrections.",
        ],
        bad_outcomes=[
            "Short-term portfolio drawdown during macro market downswings.",
            "Requires investor discipline to maintain allocation during volatility.",
        ],
        trade_offs=[
            "Accepts moderate short-term fluctuations in exchange for higher terminal corpus.",
            "Requires periodic rebalancing maintenance.",
        ],
        baseline_safety_score=7.6,
        baseline_liquidity_score=7.8,
        baseline_growth_score=8.2,
        baseline_flexibility_score=7.4,
    ),
    StrategyDefinition(
        strategy_id="strat-dynamic-accumulation",
        name="Aggressive Long-Term Wealth Accumulation Strategy",
        tagline="Maximum compounding power through active equity premium and glide-path de-risking.",
        description=(
            "A growth-first wealth creation pathway for long-term horizons. "
            "Harnesses full market upside during accumulation, then transitions into debt as target nears."
        ),
        applicable_goal_types=[
            "Retirement",
            "Wealth Creation",
            "Child Education",
            "Business",
            "Other",
        ],
        implementation_parameters=[
            StrategyImplementationParamDef(
                name="growth_allocation_pct",
                label="Aggressive Growth Allocation (%)",
                param_type="percentage",
                description="Initial equity-heavy growth allocation.",
                default_value=85.0,
                min_value=70.0,
                max_value=100.0,
            ),
            StrategyImplementationParamDef(
                name="derisking_lead_years",
                label="Glide-Path De-risking Window (Years before goal)",
                param_type="integer",
                description="Years before maturity when automated de-risking into debt begins.",
                default_value=3,
                min_value=1,
                max_value=5,
            ),
            StrategyImplementationParamDef(
                name="upfront_seed_capital",
                label="Upfront Seed Capital (₹)",
                param_type="currency",
                description="Initial capital allocation committed at strategy inception.",
                default_value=500000.0,
                min_value=0.0,
            ),
        ],
        good_outcomes=[
            "Superior compounding multiplier over 7+ year investment cycles.",
            "Significantly minimizes required ongoing capital outlay due to compounding leverage.",
            "Automated glide-path locks in accumulated corpus before goal horizon.",
        ],
        bad_outcomes=[
            "High portfolio volatility during mid-tenure market corrections.",
            "Severe sequence-of-returns risk if market crashes before de-risking phase.",
        ],
        trade_offs=[
            "Sacrifices short-to-medium term liquidity and capital stability for long-term corpus expansion.",
            "Demands high emotional fortitude during bear markets.",
        ],
        baseline_safety_score=5.8,
        baseline_liquidity_score=6.8,
        baseline_growth_score=9.5,
        baseline_flexibility_score=6.2,
    ),
    StrategyDefinition(
        strategy_id="strat-high-liquidity-flex",
        name="Adaptive Liquid Buffer & Milestone Flexibility Strategy",
        tagline="Unmatched capital accessibility and dynamic timeline responsiveness.",
        description=(
            "Engineered for milestones requiring flexible execution dates and immediate liquidity. "
            "Eliminates exit loads and lock-in penalties."
        ),
        applicable_goal_types=[
            "Emergency Fund",
            "Travel",
            "Vehicle",
            "Business",
            "Other",
        ],
        implementation_parameters=[
            StrategyImplementationParamDef(
                name="instant_liquidity_pct",
                label="Instant Liquid Reserve (%)",
                param_type="percentage",
                description="Percentage held in instant-redemption avenues.",
                default_value=40.0,
                min_value=20.0,
                max_value=100.0,
            ),
            StrategyImplementationParamDef(
                name="short_term_debt_pct",
                label="Short-Duration Yield Buffer (%)",
                param_type="percentage",
                description="Balance deployed into short-duration debt for incremental yield.",
                default_value=60.0,
                min_value=0.0,
                max_value=80.0,
            ),
        ],
        good_outcomes=[
            "T+0 / T+1 liquidity availability with zero penalty or exit load.",
            "Zero lock-in restrictions allow early goal execution or reallocation.",
            "High capital safety with nominal credit risk.",
        ],
        bad_outcomes=[
            "Yield lags long-term wealth compounding avenues.",
            "Tax drag on short-term debt gains if applicable.",
        ],
        trade_offs=[
            "Trades compound return velocity for near-cash liquidity and flexibility.",
        ],
        baseline_safety_score=8.8,
        baseline_liquidity_score=9.6,
        baseline_growth_score=5.2,
        baseline_flexibility_score=9.6,
    ),
]


def get_all_strategies() -> list[StrategyDefinition]:
    return list(STRATEGY_CATALOG)
