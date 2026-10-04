from models.defined_goal import DefinedGoal
from models.strategy import StrategyDefinition
from engines.rules.engine import StrategyRuleEngine
from rules.goals import canonical_goal_name, canonical_goal_type


def _goal(**overrides):
    values = dict(
        goal_id="g-rule",
        planning_unit_id="pu-rule",
        version=1,
        is_latest=True,
        goal_type="retirement",
        goal_name="Retirement",
        today_cost=1000000.0,
        inflation_rate=0.06,
        target_month=6,
        target_year=2041,
        duration_years=15.0,
        future_target=2400000.0,
        priority="High",
        flexibility="Fixed",
        funding_gap=500000.0,
        funding_status="Shortfall",
    )
    values.update(overrides)
    return DefinedGoal(**values)


def _strategy(**overrides):
    values = dict(
        strategy_id="strat-rule-test",
        name="Rule Test Strategy",
        tagline="Test",
        description="Test strategy",
        applicable_goal_types=["retirement"],
        applicable_goal_characteristics=["shortfall"],
    )
    values.update(overrides)
    return StrategyDefinition(**values)


def test_rule_engine_matches_goal_type_without_component_evaluation():
    result = StrategyRuleEngine().evaluate(
        _strategy(applicable_goal_characteristics=[]),
        defined_goal=_goal(),
    )
    assert result.eligible is True
    assert result.goal_type_match is True


def test_rule_engine_reports_unmatched_characteristic_without_mutating_strategy():
    result = StrategyRuleEngine().evaluate(
        _strategy(applicable_goal_characteristics=["near_term"]),
        defined_goal=_goal(duration_years=15.0),
    )
    assert result.eligible is False
    assert result.unmet_characteristics == ("near_term",)


def test_rule_engine_does_not_use_financial_context_as_component_activation():
    result = StrategyRuleEngine().evaluate(
        _strategy(),
        defined_goal=_goal(),
        financial_context={"total_liabilities": 500000, "emi_burden_monthly": None},
    )
    assert result.eligible is True
    assert result.missing_inputs == ()


def test_canonical_goal_taxonomy_accepts_only_the_onboarding_ids():
    expected = {
        "retirement": "Retirement",
        "marriage": "Marriage",
        "vehicle": "Vehicle",
        "dream_home": "Dream Home",
        "education": "Education",
        "vacation": "Vacation",
        "debt_freedom": "Debt Freedom",
        "wealth_creation": "Wealth Creation",
        "fire_passive_income": "FIRE / Passive Income",
        "others": "Others",
    }
    for goal_type, label in expected.items():
        assert canonical_goal_type(goal_type) == goal_type
        assert canonical_goal_name(goal_type) == label

    assert canonical_goal_type("Financial Independence") == ""
    assert canonical_goal_type("Passive Income") == ""
    assert canonical_goal_type("Child Education") == ""
    assert canonical_goal_type("philanthropy") == ""
