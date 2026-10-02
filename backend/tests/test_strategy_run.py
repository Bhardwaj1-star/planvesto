import logging
import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from models.defined_goal import DefinedGoal
from models.strategy import (
    InvestorPriorities,
    Scenario,
    StrategyDefinition,
    StrategyRankingItem,
    StrategyRecommendation,
    StrategyRun,
)
from schemas.goals import GoalInput
from schemas.strategy import StrategySelectRequest
from services.goal_service import GoalService
from services.strategy_service import StrategyService


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
    # ── 1. Mandatory Priorities ──────────────────────────────────────────────
    @patch("services.strategy_service.GoalRepository")
    @patch("services.strategy_service.StrategyRepository")
    def test_first_strategy_build_without_priorities_rejected(self, MockStratRepo, MockGoalRepo):
        goal_repo_mock = MockGoalRepo.return_value
        strat_repo_mock = MockStratRepo.return_value
        dg = _dummy_defined_goal(version=1)
        goal_repo_mock.get_latest_defined_goal.return_value = dg
        strat_repo_mock.get_latest_run.return_value = None
        svc = StrategyService()
        with pytest.raises(HTTPException) as exc_info:
            svc.build_strategy(planning_unit_id="pu-test-run", goal_id="g-test-run", priorities=None)
        assert exc_info.value.status_code == 400
        assert "Investor priorities must be provided before strategy comparison" in exc_info.value.detail
        strat_repo_mock.save_run.assert_not_called()

    @patch("services.strategy_service.GoalRepository")
    @patch.object(StrategyService, "_financial_context", return_value={})
    @patch("services.strategy_service.StrategyRepository")
    def test_first_strategy_build_with_explicit_priorities_succeeds(self, MockStratRepo, mock_context, MockGoalRepo):
        goal_repo_mock = MockGoalRepo.return_value
        strat_repo_mock = MockStratRepo.return_value
        dg = _dummy_defined_goal(version=1)
        goal_repo_mock.get_latest_defined_goal.return_value = dg
        strat_repo_mock.get_latest_run.return_value = None
        strat_repo_mock.save_run.return_value = "run-uuid-1"
        svc = StrategyService()
        explicit_priorities = InvestorPriorities(safety=0.7, liquidity=0.1, growth=0.1, flexibility=0.1)
        run = svc.build_strategy(planning_unit_id="pu-test-run", goal_id="g-test-run", priorities=explicit_priorities)
        assert run.strategy_run_id == "run-uuid-1"
        assert run.defined_goal_version == 1
        assert run.run_version == 1
        assert run.is_latest is True
        assert len(run.applicable_strategies) > 0
        assert len(run.scenarios) > 0
        assert len(run.rankings) > 0
        assert run.recommendation.recommended_strategy_id != ""
        strat_repo_mock.save_run.assert_called_once()

    @patch("services.strategy_service.GoalRepository")
    @patch.object(StrategyService, "_financial_context", return_value={})
    @patch("services.strategy_service.StrategyRepository")
    def test_subsequent_strategy_build_reuses_previous_priorities(self, MockStratRepo, mock_context, MockGoalRepo):
        goal_repo_mock = MockGoalRepo.return_value
        strat_repo_mock = MockStratRepo.return_value
        dg = _dummy_defined_goal(version=1)
        goal_repo_mock.get_latest_defined_goal.return_value = dg
        prev_priorities = InvestorPriorities(safety=0.5, liquidity=0.2, growth=0.2, flexibility=0.1)
        prev_run = StrategyRun(
            strategy_run_id="run-0",
            planning_unit_id="pu-test-run",
            goal_id="g-test-run",
            defined_goal_id="dg-0",
            defined_goal_version=1,
            run_version=1,
            investor_priorities=prev_priorities,
            recommendation=StrategyRecommendation(recommended_strategy_id="strat-1", recommended_scenario_id="scen-1"),
        )
        strat_repo_mock.get_latest_run.return_value = prev_run
        strat_repo_mock.save_run.return_value = "run-uuid-2"
        svc = StrategyService()
        run = svc.build_strategy(planning_unit_id="pu-test-run", goal_id="g-test-run", priorities=None)
        assert run.strategy_run_id == "run-uuid-2"
        assert run.run_version == 2
        assert run.investor_priorities.safety == 0.5

    # ── 2. Strategy + Scenario Consistency Validation ────────────────────────
    @patch("services.strategy_service.StrategyRepository")
    def test_select_strategy_with_mismatched_scenario_rejected(self, MockStratRepo):
        strat_repo_mock = MockStratRepo.return_value
        strat_a = StrategyDefinition(strategy_id="strat-cap-preservation", name="Conservative", tagline="tag", description="desc")
        strat_b = StrategyDefinition(strategy_id="strat-calibrated-growth", name="Balanced", tagline="tag", description="desc")
        scen_a = Scenario(strategy_id="strat-cap-preservation", scenario_id="scen-strat-cap-preservation-baseline", scenario_name="Conservative Baseline")
        existing_run = StrategyRun(
            strategy_run_id="run-1", planning_unit_id="pu-1", goal_id="g-1", defined_goal_id="dg-1", defined_goal_version=1,
            applicable_strategies=[strat_a, strat_b], scenarios=[scen_a],
            recommendation=StrategyRecommendation(recommended_strategy_id="strat-cap-preservation", recommended_scenario_id="scen-strat-cap-preservation-baseline"),
        )
        strat_repo_mock.get_run_by_id.return_value = existing_run
        svc = StrategyService()
        req = StrategySelectRequest(
            planning_unit_id="pu-1", strategy_run_id="run-1", selected_strategy_id="strat-calibrated-growth",
            selected_scenario_id="scen-strat-cap-preservation-baseline", selected_implementation_parameters={},
        )
        with pytest.raises(HTTPException) as exc_info:
            svc.select_strategy(req)
        assert exc_info.value.status_code == 400
        assert "does not match selected strategy" in exc_info.value.detail
        strat_repo_mock.update_selection.assert_not_called()

    @patch("services.strategy_service.StrategyRepository")
    def test_select_strategy_with_nonexistent_strategy_rejected(self, MockStratRepo):
        strat_repo_mock = MockStratRepo.return_value
        scen_a = Scenario(strategy_id="strat-cap-preservation", scenario_id="scen-1", scenario_name="Conservative Baseline")
        existing_run = StrategyRun(
            strategy_run_id="run-1", planning_unit_id="pu-1", goal_id="g-1", defined_goal_id="dg-1", defined_goal_version=1,
            applicable_strategies=[], scenarios=[scen_a],
            recommendation=StrategyRecommendation(recommended_strategy_id="strat-cap-preservation", recommended_scenario_id="scen-1"),
        )
        strat_repo_mock.get_run_by_id.return_value = existing_run
        svc = StrategyService()
        req = StrategySelectRequest(planning_unit_id="pu-1", strategy_run_id="run-1", selected_strategy_id="strat-cap-preservation", selected_scenario_id="scen-1")
        with pytest.raises(HTTPException) as exc_info:
            svc.select_strategy(req)
        assert exc_info.value.status_code == 400
        assert "does not exist in this strategy run's applicable strategies" in exc_info.value.detail
        strat_repo_mock.update_selection.assert_not_called()

    @patch("services.strategy_service.StrategyRepository")
    def test_select_strategy_with_nonexistent_scenario_rejected(self, MockStratRepo):
        strat_repo_mock = MockStratRepo.return_value
        strat_a = StrategyDefinition(strategy_id="strat-cap-preservation", name="Conservative", tagline="tag", description="desc")
        existing_run = StrategyRun(
            strategy_run_id="run-1", planning_unit_id="pu-1", goal_id="g-1", defined_goal_id="dg-1", defined_goal_version=1,
            applicable_strategies=[strat_a], scenarios=[],
            recommendation=StrategyRecommendation(recommended_strategy_id="strat-cap-preservation", recommended_scenario_id="scen-1"),
        )
        strat_repo_mock.get_run_by_id.return_value = existing_run
        svc = StrategyService()
        req = StrategySelectRequest(planning_unit_id="pu-1", strategy_run_id="run-1", selected_strategy_id="strat-cap-preservation", selected_scenario_id="scen-nonexistent")
        with pytest.raises(HTTPException) as exc_info:
            svc.select_strategy(req)
        assert exc_info.value.status_code == 400
        assert "does not exist in this strategy run" in exc_info.value.detail
        strat_repo_mock.update_selection.assert_not_called()

    @patch("services.strategy_service.StrategyVersionService.create_version")
    @patch("services.strategy_service.StrategyRepository")
    def test_valid_strategy_and_scenario_selection_succeeds(self, MockStratRepo, mock_create_version):
        strat_repo_mock = MockStratRepo.return_value
        from models.strategy_version import StrategyVersion
        mock_create_version.return_value = StrategyVersion(
            strategy_version_id="sv-mock-1", planning_unit_id="pu-1", strategy_id="strat-cap-preservation",
            version=1, library_version="1.0", implementation_version="1.0", implementation_parameters={"debt_allocation_pct": 80.0},
        )
        strat_a = StrategyDefinition(strategy_id="strat-cap-preservation", name="Conservative", tagline="tag", description="desc")
        scen_a = Scenario(strategy_id="strat-cap-preservation", scenario_id="scen-test-1", scenario_name="Conservative Baseline")
        existing_run = StrategyRun(
            strategy_run_id="run-1", planning_unit_id="pu-1", goal_id="g-1", defined_goal_id="dg-1", defined_goal_version=1,
            applicable_strategies=[strat_a], scenarios=[scen_a],
            recommendation=StrategyRecommendation(recommended_strategy_id="strat-cap-preservation", recommended_scenario_id="scen-test-1"),
            architectures=[{"architecture_id": "arch-strat-cap-preservation", "primary_strategy_id": "strat-cap-preservation"}],
        )
        strat_repo_mock.get_run_by_id.return_value = existing_run
        svc = StrategyService()
        req = StrategySelectRequest(
            planning_unit_id="pu-1", strategy_run_id="run-1", selected_strategy_id="strat-cap-preservation", selected_scenario_id="scen-test-1",
            selected_implementation_parameters={"debt_allocation_pct": 80.0},
        )
        updated = svc.select_strategy(req)
        strat_repo_mock.update_selection.assert_called_once()
        assert updated.selected_strategy_id == "strat-cap-preservation"
        assert updated.selected_scenario_id == "scen-test-1"
        assert updated.selected_implementation_parameters["debt_allocation_pct"] == 80.0

    # ── 3. Selection Revalidation during Recalculation ────────────────────────
    @patch.object(StrategyService, "_financial_context", return_value={})
    @patch("services.strategy_service.StrategyRepository")
    def test_recalculation_preserves_still_valid_selection(self, MockStratRepo, mock_context):
        strat_repo_mock = MockStratRepo.return_value
        prev_run = StrategyRun(
            strategy_run_id="run-1", planning_unit_id="pu-1", goal_id="g-1", defined_goal_id="dg-1", defined_goal_version=1, run_version=1,
            investor_priorities=InvestorPriorities(safety=0.7, liquidity=0.1, growth=0.1, flexibility=0.1),
            selected_strategy_id="strat-goal-funding",
            selected_scenario_id="scen-strat-goal-funding-sip",
            selected_implementation_parameters={"existing_asset_utilisation_pct": 50},
            selection_timestamp="2026-09-09T10:00:00Z",
            recommendation=StrategyRecommendation(
                recommended_strategy_id="strat-goal-funding",
                recommended_scenario_id="scen-strat-goal-funding-sip",
            ),
        )
        strat_repo_mock.get_latest_run.return_value = prev_run
        new_dg = _dummy_defined_goal(version=2, target=1500000.0)
        svc = StrategyService()
        svc.on_defined_goal_updated(planning_unit_id="pu-1", goal_id="g-1", new_defined_goal=new_dg)
        strat_repo_mock.save_run.assert_called_once()
        saved_run = strat_repo_mock.save_run.call_args[0][0]
        assert saved_run.run_version == 2
        assert saved_run.defined_goal_version == 2
        assert saved_run.status == "recalculated"
        assert saved_run.selected_strategy_id == "strat-goal-funding"
        assert saved_run.selected_scenario_id == "scen-strat-goal-funding-sip"
        assert saved_run.selected_implementation_parameters == {"existing_asset_utilisation_pct": 50}
        assert saved_run.selection_timestamp == "2026-09-09T10:00:00Z"

    @patch.object(StrategyService, "_financial_context", return_value={})
    @patch("services.strategy_service.StrategyRepository")
    def test_recalculation_clears_invalid_selection(self, MockStratRepo, mock_context):
        strat_repo_mock = MockStratRepo.return_value
        prev_run = StrategyRun(
            strategy_run_id="run-1", planning_unit_id="pu-1", goal_id="g-1", defined_goal_id="dg-1", defined_goal_version=1, run_version=1,
            investor_priorities=InvestorPriorities(safety=0.7, liquidity=0.1, growth=0.1, flexibility=0.1),
            selected_strategy_id="strat-non-applicable-obsolete", selected_scenario_id="scen-old-obsolete",
            selected_implementation_parameters={"param": "value"}, selection_timestamp="2026-09-09T10:00:00Z",
            recommendation=StrategyRecommendation(recommended_strategy_id="strat-cap-preservation", recommended_scenario_id="scen-strat-cap-preservation-baseline"),
        )
        strat_repo_mock.get_latest_run.return_value = prev_run
        new_dg = _dummy_defined_goal(version=2, target=1500000.0)
        svc = StrategyService()
        svc.on_defined_goal_updated(planning_unit_id="pu-1", goal_id="g-1", new_defined_goal=new_dg)
        strat_repo_mock.save_run.assert_called_once()
        saved_run = strat_repo_mock.save_run.call_args[0][0]
        assert saved_run.run_version == 2
        assert saved_run.selected_strategy_id is None
        assert saved_run.selected_scenario_id is None
        assert saved_run.selected_implementation_parameters == {}
        assert saved_run.selection_timestamp is None
        assert saved_run.recommendation.recommended_strategy_id != ""
        assert saved_run.selected_strategy_id != saved_run.recommendation.recommended_strategy_id


class TestGoalServiceStrategyRecalculationErrorHandling:
    @patch("services.goal_service.GoalRepository")
    @patch("services.strategy_service.StrategyService.on_defined_goal_updated")
    def test_strategy_recalculation_exception_is_not_silently_swallowed(self, mock_on_updated, MockGoalRepo, caplog):
        goal_repo_mock = MockGoalRepo.return_value
        current_dg = _dummy_defined_goal(version=1, target=1000000.0)
        goal_repo_mock.ensure_goal_record.return_value = "g-test-run"
        goal_repo_mock.get_latest_defined_goal.return_value = current_dg
        goal_repo_mock.get_planning_unit_assets.return_value = []
        goal_repo_mock.has_material_change.return_value = True
        goal_repo_mock.save_defined_goal_snapshot.return_value = "dg-uuid-v2"
        mock_on_updated.side_effect = RuntimeError("Database connection timed out during recalculation")
        req = GoalInput(
            planning_unit_id="pu-test-run", goal_id="g-test-run", goal_name="College Fund", goal_type="Child Education",
            today_cost=1200000.0, target_month=6, target_year=2032,
        )
        svc = GoalService()
        with caplog.at_level(logging.ERROR):
            saved_goal = svc.save_and_define_goal(req)
        assert "Automatic strategy recalculation failed for goal g-test-run (version 2)" in caplog.text
        assert "Database connection timed out during recalculation" in caplog.text
