"""
tests/unit/test_repositories.py
Tests repository implementations and application port contracts.
"""

from app.infrastructure.persistence.repositories import (
    ActionPlanRepository,
    GoalPlannerRepository,
    InvestorProfileRepository,
    ReportsHistoryRepository,
    StrategyBuilderRepository,
)


def test_investor_profile_repository():
    repo = InvestorProfileRepository()
    snapshot_data = {
        "snapshot_id": "snap_101",
        "net_worth": "1500000.00",
        "total_assets": "2000000.00",
    }
    snap_id = repo.save_financial_state_snapshot("pu_test", "household", "inv_1", snapshot_data)
    assert snap_id == "snap_101"

    loaded = repo.get_financial_state_snapshot("pu_test", "snap_101")
    assert loaded is not None
    assert loaded["financial_state"]["net_worth"] == "1500000.00"

    latest = repo.get_latest_financial_state_snapshot("pu_test")
    assert latest is not None
    assert latest["snapshot_id"] == "snap_101"


def test_goal_planner_repository():
    repo = GoalPlannerRepository()
    gid = repo.ensure_goal_record(
        planning_unit_id="pu_test",
        goal_id=None,
        goal_name="Buy Electric Car",
        today_cost=1500000.0,
        target_month=6,
        target_year=2028,
    )
    assert gid is not None

    goals = repo.list_goals("pu_test")
    assert len(goals) == 1
    assert goals[0]["goal_name"] == "Buy Electric Car"

    def_id = repo.save_defined_goal(
        planning_unit_id="pu_test",
        defined_goal_payload={"goal_id": gid, "future_target": 1700000.0, "is_latest": True},
    )
    assert def_id is not None

    latest_def = repo.get_latest_defined_goal("pu_test", gid)
    assert latest_def is not None
    assert latest_def["future_target"] == 1700000.0


def test_strategy_builder_repository():
    repo = StrategyBuilderRepository()
    v_id = repo.save_strategy_version("pu_test", "goal_1", {"version": 1, "path": "self_money"})
    assert v_id is not None

    latest_v = repo.get_latest_strategy_version("pu_test", "goal_1")
    assert latest_v is not None
    assert latest_v["path"] == "self_money"


def test_action_plan_repository():
    repo = ActionPlanRepository()
    action = repo.save_action({
        "planning_unit_id": "pu_test",
        "title": "Setup recurring SIP",
        "status": "pending",
    })
    aid = action["action_id"]
    assert aid is not None

    actions = repo.list_actions("pu_test")
    assert len(actions) == 1

    updated = repo.update_action_status("pu_test", aid, "in_progress")
    assert updated["status"] == "in_progress"


def test_reports_history_repository():
    repo = ReportsHistoryRepository()
    rep_id = repo.save_report_record("pu_test", {"report_type": "individual_goal", "title": "Goal Plan"})
    assert rep_id is not None

    retrieved = repo.get_report_record("pu_test", rep_id)
    assert retrieved is not None
    assert retrieved["title"] == "Goal Plan"

    history = repo.list_history_records("pu_test")
    assert len(history) == 1
