import pytest

from engines.strategy.engine import StrategyEngine
from models.defined_goal import DefinedGoal
from models.strategy import InvestorPriorities
from .goal_matrix import GOAL_CASES
from engines.strategy.components.adapters import components_for_strategy


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

    if result.applicable_strategies:
        assert result.scenarios
        assert result.architectures
        assert result.recommendation.recommended_strategy_id

        applicable_ids = {strategy.strategy_id for strategy in result.applicable_strategies}
        for architecture in result.architectures:
            assert architecture.primary_strategy_id in applicable_ids
            for supporting_id in architecture.supporting_strategy_ids:
                assert supporting_id in applicable_ids

            primary = next(
                strategy for strategy in result.applicable_strategies
                if strategy.strategy_id == architecture.primary_strategy_id
            )
            expected_components = components_for_strategy(primary)
            assert expected_components, f"No reusable components mapped for {primary.strategy_id}"
            rationale = " ".join(architecture.rationale)
            assert any(
                component.role in rationale for component in expected_components
            ), f"Architecture does not expose primary component roles for {primary.strategy_id}"

        assert result.recommendation.recommended_strategy_id in applicable_ids
        assert result.recommendation.architecture is not None
        assert result.recommendation.architecture.primary_strategy_id in applicable_ids
