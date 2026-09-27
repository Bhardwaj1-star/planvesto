import pytest

from engines.strategy.engine import StrategyEngine
from models.defined_goal import DefinedGoal
from models.strategy import InvestorPriorities
from .goal_matrix import GOAL_CASES


def make_defined_goal(case):
    return DefinedGoal(
        goal_id=f"goal-{case.name}",
        planning_unit_id="test-planning-unit",
        investor_id="test-investor",
        goal_type=case.goal_type,
        goal_name=case.name.title(),
        today_cost=1_000_000,
        inflation_rate=0.06,
        target_month=3,
        target_year=2026 + case.duration_years,
        duration_years=case.duration_years,
        future_target=1_000_000,
        priority=case.priority,
        flexibility=case.flexibility,
        funding_gap=500_000,
        funding_status=case.funding_status,
    )


@pytest.mark.parametrize("case", GOAL_CASES, ids=lambda case: case.name)
def test_strategy_engine_executes_cross_goal(case):
    result = StrategyEngine().execute(
        defined_goal=make_defined_goal(case),
        priorities=InvestorPriorities(safety=0.3, liquidity=0.25, growth=0.25, flexibility=0.2),
        financial_context={},
    )

    assert result is not None
    assert result.priorities is not None
    assert isinstance(result.applicable_strategies, list)
    assert isinstance(result.scenarios, list)
    assert isinstance(result.architectures, list)
    assert result.recommendation is not None

    # If strategies are eligible, the full downstream pipeline must produce
    # scenarios and architectures rather than stopping at applicability.
    if result.applicable_strategies:
        assert result.scenarios
        assert result.architectures
        assert result.recommendation.recommended_strategy_id
