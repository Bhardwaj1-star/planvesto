"""
tests/unit/test_frontend_strategy_contract.py
Verifies Strategy Builder endpoints against the Chapter 11 Funding Path contract.
"""

from decimal import Decimal
import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_strategy_build_generates_funding_paths():
    """Verify POST /api/strategy/build returns the 2 canonical Chapter 11 funding paths."""
    payload = {
        "planning_unit_id": "test_pu_strategy_1",
        "goal_id": "goal_child_edu_1",
        "investor_priorities": {
            "safety": 0.3,
            "liquidity": 0.2,
            "growth": 0.4,
            "flexibility": 0.1,
        },
    }
    resp = client.post("/api/strategy/build", json=payload)
    assert resp.status_code == 200, resp.text
    data = resp.json()

    assert data["strategy_run_id"] is not None
    assert data["planning_unit_id"] == "test_pu_strategy_1"
    assert data["goal_id"] == "goal_child_edu_1"

    # Must contain both Chapter 11 Funding Paths
    strat_ids = [s["strategy_id"] for s in data["applicable_strategies"]]
    assert "path_self_money" in strat_ids
    assert "path_self_money_financing" in strat_ids

    # Rankings must have composite scores and ranks
    assert len(data["rankings"]) == 2
    assert data["rankings"][0]["rank"] == 1
    assert data["rankings"][1]["rank"] == 2

    # Recommendation
    assert data["recommendation"]["recommended_strategy_id"] in ("path_self_money", "path_self_money_financing")
    assert len(data["recommendation"]["short_reasons"]) > 0

    # Architectures
    arch_ids = [a["primary_strategy_id"] for a in data["architectures"]]
    assert "path_self_money" in arch_ids
    assert "path_self_money_financing" in arch_ids


def test_strategy_run_lifecycle_and_history():
    """Verify run retrieval by ID, history, and priority re-scoring."""
    # 1. Build
    build_payload = {
        "planning_unit_id": "test_pu_lifecycle",
        "goal_id": "goal_retirement_1",
    }
    run = client.post("/api/strategy/build", json=build_payload).json()
    run_id = run["strategy_run_id"]

    # 2. Get by ID
    get_resp = client.get(f"/api/strategy/runs/by-id/{run_id}?planning_unit_id=test_pu_lifecycle")
    assert get_resp.status_code == 200
    assert get_resp.json()["strategy_run_id"] == run_id

    # 3. Get history
    hist_resp = client.get("/api/strategy/runs/goal_retirement_1/history?planning_unit_id=test_pu_lifecycle")
    assert hist_resp.status_code == 200
    assert len(hist_resp.json()) >= 1

    # 4. Update priorities
    prio_payload = {
        "planning_unit_id": "test_pu_lifecycle",
        "strategy_run_id": run_id,
        "priorities": {"safety": 0.7, "liquidity": 0.1, "growth": 0.1, "flexibility": 0.1},
    }
    prio_resp = client.post("/api/strategy/priorities", json=prio_payload)
    assert prio_resp.status_code == 200
    assert prio_resp.json()["investor_priorities"]["safety"] == 0.7

    # 5. Select strategy
    select_payload = {
        "planning_unit_id": "test_pu_lifecycle",
        "strategy_run_id": run_id,
        "selected_strategy_id": "path_self_money",
        "selected_scenario_id": "scen_self_money_baseline",
    }
    select_resp = client.post("/api/strategy/select", json=select_payload)
    assert select_resp.status_code == 200
    assert select_resp.json()["selected_strategy_id"] == "path_self_money"

    # 6. Finalize implementation
    finalize_payload = {
        "planning_unit_id": "test_pu_lifecycle",
        "strategy_run_id": run_id,
        "defined_goal_version": 1,
        "selected_strategy_id": "path_self_money",
        "selected_scenario_id": "scen_self_money_baseline",
        "implementation_parameters": {"sip_amount": 25000},
    }
    finalize_resp = client.post("/api/strategy/implementation/finalize", json=finalize_payload)
    assert finalize_resp.status_code == 200
    ver = finalize_resp.json()
    assert ver["strategy_version_id"] is not None
    assert ver["strategy_id"] == "path_self_money"

    # 7. Verify selected version endpoint
    selected_ver_resp = client.get("/api/strategy/goals/goal_retirement_1/selected-version?planning_unit_id=test_pu_lifecycle")
    assert selected_ver_resp.status_code == 200
    assert selected_ver_resp.json()["strategy_id"] == "path_self_money"
