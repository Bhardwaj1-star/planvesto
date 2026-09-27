from models.defined_goal import DefinedGoal
from models.strategy import InvestorPriorities
from engines.rules.engine import RuleAssessment, RuleResult
from engines.strategy.engine import StrategyEngine


def _goal():
    return DefinedGoal(
        goal_id="goal-contract",
        planning_unit_id="pu-contract",
        version=1,
        is_latest=True,
        goal_type="Child Education",
        goal_name="Education Contract Test",
        today_cost=1_000_000.0,
        inflation_rate=0.06,
        target_month=6,
        target_year=2032,
        duration_years=6.0,
        future_target=1_418_519.0,
        priority="Critical",
        flexibility="Fixed",
        funding_gap=500_000.0,
        funding_status="Shortfall",
    )


def _assessment():
    diagnostic = RuleResult(
        rule_id="emergency-reserve-health",
        passed=True,
        severity="diagnostic",
        message="Emergency reserve coverage is healthy.",
        evidence={"value": 7.0, "status": "healthy", "source_metric": "emergency_fund_coverage"},
    )
    return RuleAssessment(
        diagnostics=(diagnostic,),
        hard_constraints=(),
        soft_constraints=(),
    )


def test_strategy_builder_contract_carries_rules_into_recommendation():
    result = StrategyEngine().execute(
        defined_goal=_goal(),
        priorities=InvestorPriorities(safety=0.7, liquidity=0.1, growth=0.1, flexibility=0.1),
        financial_context={"emergency_fund_coverage": 7.0},
        rule_assessment=_assessment(),
    )

    assert result.applicable_strategies
    assert result.scenarios
    assert result.rankings
    assert result.recommendation.recommended_strategy_id == result.rankings[0].strategy_id
    assert any("Emergency reserve coverage is healthy." in reason for reason in result.recommendation.short_reasons)
    assert result.recommendation.architecture is not None
    assert result.recommendation.architecture.primary_strategy_id == result.recommendation.recommended_strategy_id


def test_strategy_builder_contract_keeps_rule_diagnostics_out_of_ranking_score():
    priorities = InvestorPriorities(safety=0.7, liquidity=0.1, growth=0.1, flexibility=0.1)
    baseline = StrategyEngine().execute(_goal(), priorities=priorities)
    assessed = StrategyEngine().execute(
        _goal(),
        priorities=priorities,
        financial_context={"emergency_fund_coverage": 2.0},
        rule_assessment=RuleAssessment(
            diagnostics=(RuleResult(
                "emergency-reserve-health",
                False,
                "diagnostic",
                "Emergency reserve coverage is critical.",
                {"value": 2.0, "status": "critical", "source_metric": "emergency_fund_coverage"},
            ),),
            hard_constraints=(),
            soft_constraints=(),
        ),
    )

    assert [(x.strategy_id, x.scenario_id, x.composite_score) for x in baseline.rankings] == [
        (x.strategy_id, x.scenario_id, x.composite_score) for x in assessed.rankings
    ]
    assert any("Emergency reserve coverage is critical." in reason for reason in assessed.recommendation.short_reasons)
