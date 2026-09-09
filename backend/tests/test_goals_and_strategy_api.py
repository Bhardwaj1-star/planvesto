import pytest
from fastapi.testclient import TestClient
from main import app

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
        assert "/api/strategy/scenarios/custom" in paths
        assert "/api/strategy/priorities" in paths
        assert "/api/strategy/select" in paths
        assert "/api/strategy/runs/{goal_id}/latest" in paths
        assert "/api/strategy/runs/{goal_id}/history" in paths
