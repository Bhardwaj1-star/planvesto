import pytest

from models.action_plan import ActionImpactPreview, ActionPlanItem
from models.financial_state import FinancialState, Metric
from services.action_plan_service import ActionPlanService


class FakeRepository:
    def __init__(self):
        self.actions = {}
        self.decisions = []

    def save_action(self, action):
        action.action_id = action.action_id or "action-1"
        self.actions[action.action_id] = action
        return action

    def update_action(self, planning_unit_id, action_id, updates):
        action = self.actions[action_id]
        self.actions[action_id] = action.model_copy(update=updates)
        return self.actions[action_id]

    def delete_action(self, planning_unit_id, action_id):
        del self.actions[action_id]

    def record_decision(self, record):
        self.decisions.append(record)
        return record


def _preview():
    return ActionImpactPreview(action={"type": "test"})


def _action(status="planned"):
    state = _financial_state()
    return ActionPlanItem(
        action_id="action-1",
        planning_unit_id="pu-1",
        strategy_version_id="strategy-1",
        title="Build emergency reserve",
        status=status,
        planned_impact={"financial_state": state.model_dump(mode="json")},
    )


def _financial_state(planning_unit_id="pu-1"):
    metric = Metric(value=1000, available=True)
    return FinancialState(
        scope="family",
        planning_unit_id=planning_unit_id,
        investor_id=None,
        income_monthly=metric,
        income_annual=metric,
        expenses_monthly=metric,
        expenses_annual=metric,
        investable_surplus_monthly=metric,
        investable_surplus_annual=metric,
        total_assets=metric,
        total_liabilities=metric,
        emi_burden_monthly=metric,
    )


def test_add_confirms_planned_action_and_records_history():
    repo = FakeRepository()
    repo.actions["action-1"] = _action()
    record = ActionPlanService(repo).confirm_decision(repo.actions["action-1"], "add", _preview())
    assert repo.actions["action-1"].status == "confirmed"
    assert record.decision == "add"
    assert record.before_state["status"] == "planned"
    assert record.after_state["status"] == "confirmed"


def test_modify_only_updates_allowed_fields():
    repo = FakeRepository()
    repo.actions["action-1"] = _action("confirmed")
    record = ActionPlanService(repo).confirm_decision(
        repo.actions["action-1"],
        "modify",
        _preview(),
        {"title": "Increase emergency reserve", "status": "completed", "strategy_version_id": "other"},
    )
    assert repo.actions["action-1"].title == "Increase emergency reserve"
    assert repo.actions["action-1"].status == "confirmed"
    assert repo.actions["action-1"].strategy_version_id == "strategy-1"
    assert record.after_state["title"] == "Increase emergency reserve"


def test_complete_changes_status():
    repo = FakeRepository()
    repo.actions["action-1"] = _action("confirmed")
    record = ActionPlanService(repo).confirm_decision(repo.actions["action-1"], "complete", _preview())
    assert repo.actions["action-1"].status == "completed"
    assert record.after_state["status"] == "completed"


def test_cancel_changes_status():
    repo = FakeRepository()
    repo.actions["action-1"] = _action("confirmed")
    record = ActionPlanService(repo).confirm_decision(repo.actions["action-1"], "cancel", _preview())
    assert repo.actions["action-1"].status == "cancelled"
    assert record.after_state["status"] == "cancelled"


def test_delete_removes_current_action_but_preserves_history():
    repo = FakeRepository()
    repo.actions["action-1"] = _action("confirmed")
    record = ActionPlanService(repo).confirm_decision(repo.actions["action-1"], "delete", _preview())
    assert "action-1" not in repo.actions
    assert record.after_state == {"action_id": "action-1", "deleted": True}
    assert len(repo.decisions) == 1


def test_terminal_actions_cannot_be_modified_or_cancelled():
    repo = FakeRepository()
    for status in ("completed", "cancelled"):
        repo.actions["action-1"] = _action(status)
        with pytest.raises(ValueError):
            ActionPlanService(repo).confirm_decision(repo.actions["action-1"], "modify", _preview(), {"title": "x"})
        with pytest.raises(ValueError):
            ActionPlanService(repo).confirm_decision(repo.actions["action-1"], "cancel", _preview())


def test_action_completion_persists_authoritative_state_with_lineage():
    class SnapshotRepo:
        pass

    class FinancialStateAuthority:
        def save_actual_state(self, state, action_id, strategy_version_id, source_snapshot_id, expected_input_revision):
            return {"snapshot_id": "snapshot-1"}

    repo = FakeRepository()
    action = _action("confirmed")
    repo.actions[action.action_id] = action
    actual = _financial_state()
    service = ActionPlanService(repo, SnapshotRepo(), FinancialStateAuthority())

    updated, record, _ = service.complete_action_with_actual_state(
        action,
        actual.model_dump(mode="json"),
        _preview(),
        "source-snapshot-1",
        "input-revision-1",
    )

    assert updated.status == "completed"
    assert updated.actual_impact["financial_state_snapshot_id"] == "snapshot-1"
    assert updated.actual_impact["strategy_version_id"] == "strategy-1"
    assert record.after_state["financial_state_snapshot_id"] == "snapshot-1"


def test_action_completion_rejects_cross_planning_unit_state():
    repo = FakeRepository()
    action = _action("confirmed")
    repo.actions[action.action_id] = action
    service = ActionPlanService(
        repo,
        object(),
        type("StateAuthority", (), {"save_actual_state": lambda *args: {}})(),
    )

    with pytest.raises(ValueError, match="context does not match"):
        service.complete_action_with_actual_state(
            action,
            _financial_state("other-pu").model_dump(mode="json"),
            _preview(),
            "source-snapshot-1",
            "input-revision-1",
        )


def test_action_completion_rejects_incomplete_financial_state():
    repo = FakeRepository()
    action = _action("confirmed")
    repo.actions[action.action_id] = action
    service = ActionPlanService(
        repo,
        object(),
        type("StateAuthority", (), {"save_actual_state": lambda *args: {}})(),
    )

    with pytest.raises(ValueError):
        service.complete_action_with_actual_state(
            action,
            {"planning_unit_id": "pu-1"},
            _preview(),
            "source-snapshot-1",
            "input-revision-1",
        )
