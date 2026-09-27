import pytest
from models.defined_goal import DefinedGoal
from models.strategy import InvestorPriorities
from engines.strategy.applicability import filter_applicable_strategies
from engines.strategy.engine import StrategyEngine
from engines.strategy.scenario import create_custom_scenario


def _make_goal(goal_type="Child Education", funding_gap=500000.0, funding_status="Shortfall"):
    return DefinedGoal(
        goal_id="g-100",
        planning_unit_id="pu-100",
        version=1,
        is_latest=True,
        goal_type=goal_type,
        goal_name="Test Goal",
        today_cost=1000000.0,
        inflation_rate=0.06,
        target_month=6,
        target_year=2032,
        duration_years=6.0,
        future_target=1418519.0,
        priority="Critical",
        flexibility="Fixed",
        funding_gap=funding_gap,
        funding_status=funding_status,
    )


class TestStrategyApplicability:
    def test_applicability_by_goal_type(self):
        strats = filter_applicable_strategies("Child Education")
        assert len(strats) >= 2
        ids = [s.strategy_id for s in strats]
        assert "strat-cap-preservation" in ids
        assert "strat-calibrated-growth" in ids

    def test_no_applicable_strategy_for_empty_type(self):
        strats = filter_applicable_strategies("")
        assert len(strats) == 0

    def test_debt_strategy_eligibility_is_separate_from_component_activation(self):
        goal = _make_goal()
        without_emi = filter_applicable_strategies(
            defined_goal=goal,
            financial_context={"total_liabilities": 500000, "investable_surplus_monthly": 30000},
        )
        with_emi = filter_applicable_strategies(
            defined_goal=goal,
            financial_context={
                "total_liabilities": 500000,
                "investable_surplus_monthly": 30000,
                "emi_burden_monthly": {"value": 12000, "available": True},
            },
        )
        assert "strat-debt-reduction" in {s.strategy_id for s in without_emi}
        assert "strat-debt-reduction" in {s.strategy_id for s in with_emi}

    def test_credit_strategy_eligibility_is_separate_from_component_activation(self):
        goal = _make_goal(goal_type="Home Purchase")
        without_emi = filter_applicable_strategies(
            defined_goal=goal,
            financial_context={"investable_surplus_monthly": 30000},
        )
        with_emi = filter_applicable_strategies(
            defined_goal=goal,
            financial_context={
                "investable_surplus_monthly": 30000,
                "emi_burden_monthly": {"value": 12000, "available": True},
            },
        )
        assert "strat-credit-utilisation" in {s.strategy_id for s in without_emi}
        assert "strat-credit-utilisation" in {s.strategy_id for s in with_emi}

    def test_engine_raises_error_if_priorities_missing(self):
        engine = StrategyEngine()
        goal = _make_goal()
        with pytest.raises(ValueError, match="Investor priorities must be provided"):
            engine.execute(goal, priorities=None)

    def test_strategy_engine_returns_no_strategy_available(self):
        engine = StrategyEngine()
        priorities = InvestorPriorities()
        goal = _make_goal(goal_type="CompletelyUnmatchedNonExistentType999")
        result = engine.execute(goal, priorities=priorities)
        goal_empty = _make_goal(goal_type="")
        result_empty = engine.execute(goal_empty, priorities=priorities)
        assert len(result_empty.applicable_strategies) == 0
        assert "No Strategy Available" in result_empty.recommendation.short_reasons

    def test_strategies_generated_for_shortfall(self):
        engine = StrategyEngine()
        goal = _make_goal(funding_gap=600000.0, funding_status="Shortfall")
        res = engine.execute(goal, priorities=InvestorPriorities())
        assert len(res.applicable_strategies) > 0
        assert len(res.rankings) > 0

    def test_strategies_generated_for_on_track(self):
        engine = StrategyEngine()
        goal = _make_goal(funding_gap=0.0, funding_status="On Track")
        res = engine.execute(goal, priorities=InvestorPriorities())
        assert len(res.applicable_strategies) > 0
        assert len(res.rankings) > 0

    def test_strategies_generated_for_overfunded(self):
        engine = StrategyEngine()
        goal = _make_goal(funding_gap=-200000.0, funding_status="Overfunded")
        res = engine.execute(goal, priorities=InvestorPriorities())
        assert len(res.applicable_strategies) > 0
        assert len(res.rankings) > 0


class TestPriorityBasedRanking:
    def test_safety_prioritized_ranks_safety_highest(self):
        engine = StrategyEngine()
        goal = _make_goal()
        priorities = InvestorPriorities(safety=0.8, liquidity=0.1, growth=0.05, flexibility=0.05)
        res = engine.execute(goal, priorities=priorities)
        top = res.rankings[0]
        assert top.strategy_id == "strat-cap-preservation"
        assert res.recommendation.recommended_strategy_id == "strat-cap-preservation"

    def test_growth_prioritized_ranks_growth_highest(self):
        engine = StrategyEngine()
        goal = _make_goal()
        priorities = InvestorPriorities(safety=0.05, liquidity=0.05, growth=0.85, flexibility=0.05)
        res = engine.execute(goal, priorities=priorities)
        top = res.rankings[0]
        assert top.strategy_id in {"strat-calibrated-growth", "strat-dynamic-accumulation"}

    def test_liquidity_prioritized_ranks_liquidity_highest(self):
        engine = StrategyEngine()
        goal = _make_goal(goal_type="Emergency Fund")
        priorities = InvestorPriorities(safety=0.1, liquidity=0.8, growth=0.05, flexibility=0.05)
        res = engine.execute(goal, priorities=priorities)
        top = res.rankings[0]
        assert top.strategy_id == "strat-high-liquidity-flex"


class TestCustomScenarios:
    def test_custom_scenario_participates_in_ranking(self):
        engine = StrategyEngine()
        goal = _make_goal()
        applicable = filter_applicable_strategies(goal.goal_type)
        strat = applicable[0]

        custom = create_custom_scenario(
            strategy=strat,
            defined_goal=goal,
            custom_name="My Custom Aggressive Run",
            custom_assumptions={"inflation_rate": 0.05},
            custom_funding={"equity_allocation_pct": 80.0},
        )
        assert custom.is_investor_modified is True

        res = engine.execute(goal, priorities=InvestorPriorities(), custom_scenarios=[custom])
        scenario_ids = [r.scenario_id for r in res.rankings]
        assert custom.scenario_id in scenario_ids
