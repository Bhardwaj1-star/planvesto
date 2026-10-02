import pytest
from unittest.mock import patch
from fastapi import HTTPException
from fastapi.testclient import TestClient
from main import app
from models.orchestration import ModuleAvailability, PlanningContext, PlanningOrchestrationContext
from models.orchestration import WorkflowNextAction, WorkflowPrerequisite
from services.planning_orchestration_service import PlanningOrchestrationService

client = TestClient(app)


class TestGoalsAndStrategyAPIRoutes:
    def test_goals_calculate_unauthenticated_returns_401(self):
        payload = {
            "planning_unit_id": "test-pu-123",
            "goal_name": "Vacation",
            "goal_type": "Travel",
            "today_cost": 200000.0,
            "target_month": 12,
            "target_year": 2027,
        }
        r = client.post("/api/goals/calculate", json=payload)
        assert r.status_code == 401
        assert "Authorization token required" in r.json()["detail"]

    def test_strategy_build_unauthenticated_returns_401(self):
        payload = {
            "planning_unit_id": "test-pu-123",
            "goal_id": "test-goal-123",
        }
        r = client.post("/api/strategy/build", json=payload)
        assert r.status_code == 401
        assert "Authorization token required" in r.json()["detail"]

    def test_goals_calculate_invalid_body_returns_422(self):
        # Missing required fields like today_cost, target_month
        r = client.post("/api/goals/calculate", json={"planning_unit_id": "pu-1"})
        assert r.status_code == 422

    def test_strategy_build_invalid_body_returns_422(self):
        # Missing goal_id
        r = client.post("/api/strategy/build", json={"planning_unit_id": "pu-1"})
        assert r.status_code == 422

    def test_routes_are_registered_on_fastapi_app(self):
        paths = app.openapi()["paths"]
        assert "/api/goals/calculate" in paths
        assert "/api/goals" in paths
        assert "/api/goals/{goal_id}/defined/latest" in paths
        assert "/api/goals/{goal_id}/defined/versions" in paths
        assert "/api/goals/{goal_id}/defined/versions/{version}" in paths
        assert "/api/strategy/build" in paths
        assert "/api/strategy/primary" in paths
        assert "/api/strategy/scenarios/custom" in paths
        assert "/api/strategy/priorities" in paths
        assert "/api/strategy/select" in paths
        assert "/api/strategy/runs/{goal_id}/latest" in paths
        assert "/api/strategy/runs/{goal_id}/history" in paths

    @patch("api.strategy_version.PrimaryStrategyRepository.get_current")
    @patch("api.strategy_version.verify_planning_unit_ownership")
    @patch("api.strategy_version.authenticate_user")
    def test_get_primary_strategy_returns_data_or_null(self, mock_auth, mock_pu, mock_get_current):
        mock_auth.return_value = "user-1"
        mock_pu.return_value = None
        mock_get_current.return_value = None
        r = client.get("/api/strategy/primary?planning_unit_id=pu-1", headers={"Authorization": "Bearer fake"})
        assert r.status_code == 200
        assert r.json() is None

    @patch("api.strategy.verify_goal_ownership")
    @patch("api.strategy.authenticate_user")
    @patch("api.strategy.StrategyService.build_strategy")
    def test_strategy_build_missing_priorities_returns_400(self, mock_build, mock_auth, mock_goal):
        mock_auth.return_value = "user-1"
        mock_goal.return_value = None
        mock_build.side_effect = HTTPException(
            status_code=400,
            detail="Investor priorities must be provided before strategy comparison and ranking.",
        )
        r = client.post(
            "/api/strategy/build",
            json={"planning_unit_id": "pu-1", "goal_id": "g-1"},
            headers={"Authorization": "Bearer fake"},
        )
        assert r.status_code == 400
        assert "Investor priorities must be provided" in r.json()["detail"]

    @patch("api.strategy.verify_strategy_run_ownership")
    @patch("api.strategy.authenticate_user")
    @patch("api.strategy.StrategyService.select_strategy")
    def test_strategy_select_inconsistent_returns_400(self, mock_select, mock_auth, mock_run):
        mock_auth.return_value = "user-1"
        mock_run.return_value = None
        mock_select.side_effect = HTTPException(
            status_code=400,
            detail="Selected scenario does not match selected strategy.",
        )
        r = client.post(
            "/api/strategy/select",
            json={
                "planning_unit_id": "pu-1",
                "strategy_run_id": "run-1",
                "selected_strategy_id": "strat-a",
                "selected_scenario_id": "scen-b",
            },
            headers={"Authorization": "Bearer fake"},
        )
        assert r.status_code == 400
        assert "Selected scenario does not match" in r.json()["detail"]


    @patch("api.strategy.verify_goal_ownership")
    @patch("api.strategy.authenticate_user")
    @patch("api.strategy.StrategyService.build_strategy")
    def test_strategy_build_checks_goal_ownership(self, mock_build, mock_auth, mock_goal):
        mock_auth.return_value = "user-1"
        mock_goal.return_value = None
        mock_build.return_value = {"strategy_run_id": "run-1", "planning_unit_id": "pu-1", "goal_id": "g-1", "defined_goal_id": "dg-1", "defined_goal_version": 1, "recommendation": {"recommended_strategy_id": "strat-1", "recommended_scenario_id": "scen-1"}}
        client.post("/api/strategy/build", json={"planning_unit_id": "pu-1", "goal_id": "g-1", "investor_priorities": {}}, headers={"Authorization": "Bearer fake"})
        mock_goal.assert_called_once_with("pu-1", "g-1", "user-1")

    @patch("api.strategy.verify_strategy_run_ownership")
    @patch("api.strategy.authenticate_user")
    @patch("api.strategy.StrategyService.select_strategy")
    def test_strategy_select_checks_run_ownership(self, mock_select, mock_auth, mock_run):
        mock_auth.return_value = "user-1"
        mock_run.return_value = None
        mock_select.return_value = {"strategy_run_id": "run-1", "planning_unit_id": "pu-1", "goal_id": "g-1", "defined_goal_id": "dg-1", "defined_goal_version": 1, "recommendation": {"recommended_strategy_id": "strat-1", "recommended_scenario_id": "scen-1"}}
        client.post("/api/strategy/select", json={"planning_unit_id": "pu-1", "strategy_run_id": "run-1", "selected_strategy_id": "strat-a", "selected_scenario_id": "scen-a"}, headers={"Authorization": "Bearer fake"})
        mock_run.assert_called_once_with("pu-1", "run-1", "user-1")


class TestDashboardAuthorization:
    @patch("api.dashboard.verify_investor_ownership")
    @patch("api.dashboard.verify_planning_unit_ownership")
    @patch("api.dashboard.authenticate_user")
    @patch("api.dashboard.DashboardService.build")
    def test_dashboard_individual_scope_checks_investor_ownership(
        self, mock_build, mock_auth, mock_pu, mock_investor
    ):
        mock_auth.return_value = "user-1"
        mock_build.return_value = PlanningOrchestrationContext(
            planning_context=PlanningContext(planning_unit_id="pu-1", scope="individual", investor_id="investor-1", goal_version_ids=["defined-goal-1", "defined-goal-2"], strategy_version_id="strategy-version-1"),
            financial_state=ModuleAvailability(available=False),
            goals=ModuleAvailability(available=True),
            strategy=ModuleAvailability(available=True),
            moneywheel=ModuleAvailability(available=False),
            action_plan=ModuleAvailability(available=True),
        )
        r = client.get(
            "/api/dashboard",
            params={
                "planning_unit_id": "pu-1",
                "scope": "individual",
                "investor_id": "investor-1",
            },
            headers={"Authorization": "Bearer fake"},
        )
        assert r.status_code == 200
        mock_pu.assert_called_once_with("pu-1", "user-1")
        mock_investor.assert_called_once_with("pu-1", "investor-1", "user-1")

    @patch("api.dashboard.verify_planning_unit_ownership")
    @patch("api.dashboard.authenticate_user")
    def test_dashboard_rejects_investor_id_for_family_scope(self, mock_auth, mock_pu):
        mock_auth.return_value = "user-1"
        r = client.get(
            "/api/dashboard",
            params={
                "planning_unit_id": "pu-1",
                "scope": "family",
                "investor_id": "investor-1",
            },
            headers={"Authorization": "Bearer fake"},
        )
        assert r.status_code == 400
        assert "only valid for individual scope" in r.json()["detail"]


class TestOrchestrationAuthorization:
    @patch("api.orchestration.verify_defined_goal_ownership")
    @patch("api.orchestration.verify_strategy_version_ownership")
    @patch("api.orchestration.verify_investor_ownership")
    @patch("api.orchestration.verify_planning_unit_ownership")
    @patch("api.orchestration.authenticate_user")
    @patch("api.orchestration.PlanningOrchestrationService.build_context")
    def test_orchestration_checks_all_referenced_resources(
        self, mock_build, mock_auth, mock_pu, mock_investor, mock_strategy_version, mock_goal_version
    ):
        mock_auth.return_value = "user-1"
        mock_build.return_value = {}
        r = client.post(
            "/api/orchestration/context",
            json={
                "planning_unit_id": "pu-1",
                "scope": "individual",
                "investor_id": "investor-1",
                "goal_version_ids": ["defined-goal-1", "defined-goal-2"],
                "strategy_version_id": "strategy-version-1",
            },
            headers={"Authorization": "Bearer fake"},
        )
        assert r.status_code == 200
        mock_pu.assert_called_once_with("pu-1", "user-1")
        mock_investor.assert_called_once_with("pu-1", "investor-1", "user-1")
        assert mock_goal_version.call_count == 2
        mock_strategy_version.assert_called_once_with("pu-1", "strategy-version-1", "user-1")

    @patch("api.orchestration.verify_planning_unit_ownership")
    @patch("api.orchestration.authenticate_user")
    @patch("api.orchestration.MultiGoalPlanningService.build_multi_goal_plan")
    def test_orchestration_plan_endpoint(self, mock_build, mock_auth, mock_pu):
        mock_auth.return_value = "user-1"
        mock_pu.return_value = None
        from engines.orchestration.models import MultiGoalPlanResult
        mock_build.return_value = MultiGoalPlanResult(planning_unit_id="pu-1")
        r = client.post(
            "/api/orchestration/plan",
            json={"planning_unit_id": "pu-1"},
            headers={"Authorization": "Bearer fake"},
        )
        assert r.status_code == 200
        mock_pu.assert_called_once_with("pu-1", "user-1")
        assert r.json()["planning_unit_id"] == "pu-1"


class TestWorkflowReadiness:
    def test_ready_workflow_has_no_blockers_and_returns_to_process(self):
        readiness = PlanningOrchestrationService.build_workflow_readiness(
            process_route="/investor/goal-planner?goalId=goal-1",
            prerequisites=[
                WorkflowPrerequisite(
                    key="financial_state",
                    availability=ModuleAvailability(available=True),
                )
            ],
        )

        assert readiness.status == "ready"
        assert readiness.blockers == []
        assert readiness.next_action is None
        assert readiness.return_to == "/investor/goal-planner?goalId=goal-1"

    def test_blocked_workflow_exposes_reason_action_and_return_route(self):
        readiness = PlanningOrchestrationService.build_workflow_readiness(
            process_route="/investor/goal-planner?goalId=goal-1",
            prerequisites=[
                WorkflowPrerequisite(
                    key="financial_state",
                    availability=ModuleAvailability(
                        available=False,
                        reason="No Financial State snapshot exists for this planning context",
                    ),
                    next_action=WorkflowNextAction(
                        label="Review Financial State",
                        route="/investor/financial-state",
                    ),
                )
            ],
        )

        assert readiness.status == "blocked"
        assert len(readiness.blockers) == 1
        assert readiness.blockers[0].reason == "No Financial State snapshot exists for this planning context"
        assert readiness.next_action.route == "/investor/financial-state"
        assert readiness.return_to == "/investor/goal-planner?goalId=goal-1"

    def test_workflow_routes_must_be_local_paths(self):
        with pytest.raises(ValueError):
            WorkflowNextAction(label="External", route="https://example.com")
