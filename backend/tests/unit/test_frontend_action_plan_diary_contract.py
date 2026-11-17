"""
tests/unit/test_frontend_action_plan_diary_contract.py
Verifies Action Plan and Investor Diary endpoints against frontend contracts.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_action_plan_lifecycle():
    """Verify action generation, creation, retrieval, and completion."""
    planning_unit_id = "test_pu_actions"
    strategy_version_id = "sv_test_123"

    # 1. Generate actions
    gen_resp = client.post(
        f"/api/action-plan/actions/generate?planning_unit_id={planning_unit_id}&strategy_version_id={strategy_version_id}"
    )
    assert gen_resp.status_code == 200, gen_resp.text
    actions = gen_resp.json()
    assert len(actions) >= 3
    action_id = actions[0]["action_id"]

    # 2. List actions
    list_resp = client.get(f"/api/action-plan/actions?planning_unit_id={planning_unit_id}")
    assert list_resp.status_code == 200
    assert len(list_resp.json()) >= 3

    # 3. Get action by id
    get_resp = client.get(f"/api/action-plan/actions/{action_id}?planning_unit_id={planning_unit_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["action_id"] == action_id

    # 4. Complete action
    comp_resp = client.post(
        f"/api/action-plan/actions/{action_id}/complete",
        json={
            "planning_unit_id": planning_unit_id,
            "action_id": action_id,
            "actual_state": {},
            "completion_preview": {"sip_configured": True},
        },
    )
    assert comp_resp.status_code == 200
    assert comp_resp.json()["status"] == "completed"

    # 5. Confirm decision
    dec_resp = client.post(
        "/api/action-plan/decisions",
        json={
            "planning_unit_id": planning_unit_id,
            "action_id": action_id,
            "decision": "complete",
            "impact_preview": {},
            "after_state": {},
        },
    )
    assert dec_resp.status_code == 200
    assert dec_resp.json()["decision"] == "complete"

    # 6. List decisions
    dec_list_resp = client.get(f"/api/action-plan/decisions?planning_unit_id={planning_unit_id}")
    assert dec_list_resp.status_code == 200
    assert len(dec_list_resp.json()) >= 1


def test_investor_diary_lifecycle():
    """Verify diary entry creation, retrieval, and deletion, plus decisions."""
    planning_unit_id = "test_pu_diary"

    # 1. Create entry
    create_resp = client.post(
        "/api/diary/entries",
        json={
            "planning_unit_id": planning_unit_id,
            "date": "2026-11-17",
            "title": "Strategy Reflection",
            "content": "Decided to follow Self Money path to avoid loan interest.",
            "tags": ["strategy", "retirement"],
            "prompts": [],
            "is_important": True,
        },
    )
    assert create_resp.status_code == 200, create_resp.text
    entry = create_resp.json()
    entry_id = entry["id"]

    # 2. List entries
    list_resp = client.get(f"/api/diary/entries?planning_unit_id={planning_unit_id}")
    assert list_resp.status_code == 200
    assert any(e["id"] == entry_id for e in list_resp.json())

    # 3. Create financial decision
    dec_resp = client.post(
        "/api/diary/decisions",
        json={
            "planning_unit_id": planning_unit_id,
            "date": "2026-11-17",
            "title": "SIP Mandate Started",
            "summary": "Started ₹25,000/mo SIP in index fund.",
            "category": "Investment",
            "source": "Investor",
        },
    )
    assert dec_resp.status_code == 200
    assert dec_resp.json()["category"] == "Investment"

    # 4. List decisions
    dec_list = client.get(f"/api/diary/decisions?planning_unit_id={planning_unit_id}")
    assert dec_list.status_code == 200
    assert len(dec_list.json()) >= 1

    # 5. Delete entry
    del_resp = client.delete(f"/api/diary/entries/{entry_id}?planning_unit_id={planning_unit_id}")
    assert del_resp.status_code == 200
    assert del_resp.json()["deleted"] is True
