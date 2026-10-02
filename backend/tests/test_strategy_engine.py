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
        assert "strat-capital-preservation" in ids
        assert "strat-goal-funding" in ids

    def test_financial_freedom_passive_income_goal_maps_to_goal_funding(self):
        goal = _make_goal(goal_type="Financial Freedom / Passive Income")
        strats = filter_applicable_strategies(defined_goal=goal)
        ids = {s.strategy_id for s in strats}
        assert "strat-goal-funding" in ids

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
        engine.execute(goal, priorities=priorities)
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


class TestEvidenceBasedDecision:
    def test_changing_dimension_scores_does_not_change_selected_strategy(self):
        """Changing dimension weights cannot change the selected strategy when decision evidence is unchanged."""
        engine = StrategyEngine()
        goal = _make_goal()
        res_safety = engine.execute(goal, priorities=InvestorPriorities(safety=0.9, liquidity=0.03, growth=0.04, flexibility=0.03))
        res_growth = engine.execute(goal, priorities=InvestorPriorities(safety=0.03, liquidity=0.04, growth=0.9, flexibility=0.03))
        assert res_safety.recommendation.recommended_strategy_id == res_growth.recommendation.recommended_strategy_id
        assert res_safety.rankings[0].strategy_id == res_growth.rankings[0].strategy_id
        assert res_safety.recommendation.recommended_strategy_id == "strat-goal-funding"

    def test_composite_score_is_not_decision_authority(self):
        """Strategy recommendation is NOT driven by composite_score."""
        engine = StrategyEngine()
        goal = _make_goal()
        priorities = InvestorPriorities(safety=0.8, liquidity=0.1, growth=0.05, flexibility=0.05)
        res = engine.execute(goal, priorities=priorities)
        top_rec = res.recommendation.recommended_strategy_id
        recommended_item = next(r for r in res.rankings if r.strategy_id == top_rec)
        assert recommended_item.is_recommended is True
        assert top_rec == "strat-goal-funding"
        assert res.recommendation.architecture is not None
        assert res.recommendation.architecture.primary_strategy_id == top_rec

    def test_ineligible_strategies_cannot_be_recommended(self):
        engine = StrategyEngine()
        goal = _make_goal()
        res = engine.execute(goal, priorities=InvestorPriorities())
        for r in res.rankings:
            if not r.is_eligible:
                assert r.is_recommended is False
                assert r.strategy_id != res.recommendation.recommended_strategy_id

    def test_recommendation_comes_from_new_decision_output(self):
        engine = StrategyEngine()
        goal = _make_goal()
        res = engine.execute(goal, priorities=InvestorPriorities())
        rec = res.recommendation
        assert rec.recommended_strategy_id != ""
        assert rec.architecture is not None
        assert "conditional" in rec.complete_reasoning.lower() or "goal" in rec.complete_reasoning.lower()
        assert not any("Strongly aligns with your priority for" in r for r in rec.short_reasons)

    def test_near_term_liquidity_goal_selects_liquidity_architecture(self):
        """A near-term corpus goal should select a protection/liquidity architecture."""
        engine = StrategyEngine()
        goal = _make_goal(goal_type="Vacation")
        goal.duration_years = 1.0
        priorities = InvestorPriorities(safety=0.25, liquidity=0.25, growth=0.25, flexibility=0.25)
        res = engine.execute(goal, priorities=priorities)
        assert res.recommendation.recommended_strategy_id in {"strat-progressive-de-risking", "strat-capital-preservation", "strat-goal-funding"}


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


class TestGenericMultiGoalArchitecture:
    """Verifies that StrategyEngine is generic across different goal types."""

    @pytest.mark.parametrize("goal_type,duration,target_amount", [
        ("Child Education", 8.0, 3000000.0),
        ("Home Purchase", 5.0, 5000000.0),
        ("Wealth Creation", 12.0, 10000000.0),
        ("Car", 3.0, 1500000.0),
    ])
    def test_generic_goal_strategy_generation(self, goal_type, duration, target_amount):
        engine = StrategyEngine()
        goal = DefinedGoal(
            goal_id=f"g-{goal_type.lower().replace(' ', '-')}",
            planning_unit_id="pu-generic-01",
            version=1,
            is_latest=True,
            goal_type=goal_type,
            goal_name=f"My {goal_type} Goal",
            today_cost=target_amount * 0.7,
            inflation_rate=0.06,
            target_month=12,
            target_year=2030,
            duration_years=duration,
            future_target=target_amount,
            priority="High",
            flexibility="Negotiable",
            funding_gap=target_amount * 0.5,
            funding_status="Shortfall",
        )
        res = engine.execute(goal, priorities=InvestorPriorities())
        assert len(res.applicable_strategies) > 0
        assert len(res.architectures) > 0
        assert len(res.rankings) > 0
        assert res.recommendation is not None
        assert res.recommendation.recommended_strategy_id != ""
        arch_ids = [a.architecture_id for a in res.architectures]
        assert res.recommendation.architecture.architecture_id in arch_ids
        assert not hasattr(res, "retirement_report")
