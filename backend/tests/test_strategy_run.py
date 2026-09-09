import pytest
from unittest.mock import MagicMock, patch
from models.defined_goal import DefinedGoal
from models.strategy import (
    InvestorPriorities,
    Scenario,
    StrategyDefinition,
    StrategyRankingItem,
    StrategyRecommendation,
    StrategyRun,
)
from services.strategy_service import StrategyService
from schemas.strategy import StrategySelectRequest


def _dummy_defined_goal(version=1, target=1000000.0):
    return DefinedGoal(
        goal_id="g-test-run",
        planning_unit_id="pu-test-run",
        version=version,
        is_latest=True,
        goal_type="Child Education",
        goal_name="College Fund",
        today_cost=target,
        inflation_rate=0.06,
        target_month=6,
        target_year=2032,
        duration_years=6.0,
        future_target=target * 1.4,
        priority="Critical",
        flexibility="Fixed",
        funding_gap=target * 0.7,
        funding_status="Shortfall",
    )


class TestStrategyRunLifecycle:
    @patch("services.strategy_service.GoalRepository")
    @patch("services.strategy_service.StrategyRepository")
    def test_build_strategy_creates_run_snapshot(self, MockStratRepo, MockGoalRepo):
        goal_repo_mock = MockGoalRepo.return_value
        strat_repo_mock = MockStratRepo.return_value

        dg = _dummy_defined_goal(version=1)
        goal_repo_mock.get_latest_defined_goal.return_value = dg
        strat_repo_mock.get_latest_run.return_value = None
        strat_repo_mock.save_run.return_value = "run-uuid-1"

        svc = StrategyService()
        run = svc.build_strategy(planning_unit_id="pu-test-run", goal_id="g-test-run")

        assert run.strategy_run_id == "run-uuid-1"
        assert run.defined_goal_version == 1
        assert run.run_version == 1
        assert run.is_latest is True
        assert len(run.applicable_strategies) > 0
        assert len(run.scenarios) > 0
        assert len(run.rankings) > 0
        assert run.recommendation.recommended_strategy_id != ""

    @patch("services.strategy_service.StrategyRepository")
    def test_select_strategy_updates_selection(self, MockStratRepo):
        strat_repo_mock = MockStratRepo.return_value

        dummy_scen = Scenario(
            scenario_id="scen-test-1",
            strategy_id="strat-cap-preservation",
            scenario_name="Conservative Baseline",
        )
        existing_run = StrategyRun(
            strategy_run_id="run-1",
            planning_unit_id="pu-1",
            goal_id="g-1",
            defined_goal_id="dg-1",
            defined_goal_version=1,
            scenarios=[dummy_scen],
            recommendation=StrategyRecommendation(recommended_strategy_id="strat-cap-preservation", recommended_scenario_id="scen-test-1"),
        )
        strat_repo_mock.get_run_by_id.return_value = existing_run

        svc = StrategyService()
        req = StrategySelectRequest(
            planning_unit_id="pu-1",
            strategy_run_id="run-1",
            selected_strategy_id="strat-cap-preservation",
            selected_scenario_id="scen-test-1",
            selected_implementation_parameters={"debt_allocation_pct": 80.0},
        )
        updated = svc.select_strategy(req)

        strat_repo_mock.update_selection.assert_called_once()
        assert updated.selected_strategy_id == "strat-cap-preservation"
        assert updated.selected_scenario_id == "scen-test-1"
        assert updated.selected_implementation_parameters["debt_allocation_pct"] == 80.0

    @patch("services.strategy_service.StrategyRepository")
    def test_automatic_recalculation_on_defined_goal_updated(self, MockStratRepo):
        strat_repo_mock = MockStratRepo.return_value

        prev_run = StrategyRun(
            strategy_run_id="run-1",
            planning_unit_id="pu-1",
            goal_id="g-1",
            defined_goal_id="dg-1",
            defined_goal_version=1,
            run_version=1,
            investor_priorities=InvestorPriorities(safety=0.7, liquidity=0.1, growth=0.1, flexibility=0.1),
            selected_strategy_id="strat-cap-preservation",
            selected_scenario_id="scen-1",
            selected_implementation_parameters={"test": 123},
            recommendation=StrategyRecommendation(recommended_strategy_id="strat-cap-preservation", recommended_scenario_id="scen-1"),
        )
        strat_repo_mock.get_latest_run.return_value = prev_run

        new_dg = _dummy_defined_goal(version=2, target=1500000.0)

        svc = StrategyService()
        svc.on_defined_goal_updated(
            planning_unit_id="pu-1",
            goal_id="g-1",
            new_defined_goal=new_dg,
        )

        strat_repo_mock.save_run.assert_called_once()
        saved_run = strat_repo_mock.save_run.call_args[0][0]
        assert saved_run.run_version == 2
        assert saved_run.defined_goal_version == 2
        assert saved_run.status == "recalculated"
        assert saved_run.selected_strategy_id == "strat-cap-preservation"
