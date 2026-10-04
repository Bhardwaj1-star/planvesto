from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

from models.financial_state import Metric
from engines.financial_state.engine import FinancialStateEngine
from services.financial_state_service import FinancialStateService
from services.profile_service import ProfileService


class FakeDataRepository:
    def get_financial_state_inputs(self, planning_unit_id):
        return {
            "investors": self.get_investors(planning_unit_id),
            "income": self.get_income(planning_unit_id),
            "expenses": self.get_expenses(planning_unit_id),
            "assets": self.get_assets(planning_unit_id),
            "liabilities": self.get_liabilities(planning_unit_id),
            "asset_owners": self.get_asset_owners(planning_unit_id),
            "liability_responsibilities": self.get_liability_responsibilities(planning_unit_id),
            "expense_participants": self.get_expense_participants(planning_unit_id),
            "asset_type_master": [],
        }

    def get_investors(self, planning_unit_id):
        return [{"investor_id": "inv-1"}]

    def get_income(self, planning_unit_id):
        return []

    def get_expenses(self, planning_unit_id):
        return []

    def get_assets(self, planning_unit_id):
        return []

    def get_liabilities(self, planning_unit_id):
        return []

    def get_asset_owners(self, planning_unit_id):
        return []

    def get_liability_responsibilities(self, planning_unit_id):
        return []

    def get_expense_participants(self, planning_unit_id):
        return []


class FakeEngine:
    def build(self, **kwargs):
        return FinancialStateEngine().build(**kwargs)


class FakeSnapshotRepository:
    def __init__(self):
        self.saved = []
        self.lineage_valid = True

    def save_snapshot(self, **kwargs):
        stored_state = dict(kwargs["financial_state"])
        stored_state["__snapshot_authority"] = kwargs.get("authority")
        row = {
            "snapshot_id": f"snap-{len(self.saved) + 1}",
            **kwargs,
            "financial_state": stored_state,
        }
        self.saved.append(row)
        return row

    def get_latest(self, planning_unit_id, scope, investor_id=None):
        return self.saved[-1] if self.saved else None

    def has_completed_action_lineage(self, planning_unit_id, action_id, snapshot_id, strategy_version_id):
        return self.lineage_valid


def test_build_persists_immutable_snapshot(monkeypatch):
    monkeypatch.setattr(
        "services.financial_state_service.FinancialDataRepository", FakeDataRepository
    )
    monkeypatch.setattr(
        "services.financial_state_service.FinancialStateEngine", FakeEngine
    )
    snapshot_repository = FakeSnapshotRepository()
    monkeypatch.setattr(
        "services.financial_state_service.FinancialStateSnapshotRepository",
        lambda: snapshot_repository,
    )

    result = FinancialStateService().build("pu-1", "family")

    assert result.model_dump()["planning_unit_id"] == "pu-1"
    assert len(snapshot_repository.saved) == 1
    assert snapshot_repository.saved[0]["planning_unit_id"] == "pu-1"
    assert snapshot_repository.saved[0]["scope"] == "family"
    assert snapshot_repository.saved[0]["investor_id"] is None


def test_individual_build_requires_investor_id(monkeypatch):
    monkeypatch.setattr(
        "services.financial_state_service.FinancialDataRepository", FakeDataRepository
    )
    monkeypatch.setattr(
        "services.financial_state_service.FinancialStateEngine", FakeEngine
    )
    monkeypatch.setattr(
        "services.financial_state_service.FinancialStateSnapshotRepository",
        FakeSnapshotRepository,
    )

    with pytest.raises(Exception):
        FinancialStateService().build("pu-1", "individual")


def test_individual_build_persists_investor_scope(monkeypatch):
    monkeypatch.setattr(
        "services.financial_state_service.FinancialDataRepository", FakeDataRepository
    )
    monkeypatch.setattr(
        "services.financial_state_service.FinancialStateEngine", FakeEngine
    )
    snapshot_repository = FakeSnapshotRepository()
    monkeypatch.setattr(
        "services.financial_state_service.FinancialStateSnapshotRepository",
        lambda: snapshot_repository,
    )

    FinancialStateService().build("pu-1", "individual", "inv-1")

    assert snapshot_repository.saved[0]["scope"] == "individual"
    assert snapshot_repository.saved[0]["investor_id"] == "inv-1"


def test_current_snapshot_rebuilds_after_raw_input_revision_changes(monkeypatch):
    class MutableDataRepository(FakeDataRepository):
        income_amount = 10000

        def get_income(self, planning_unit_id):
            return [{"income_id": "income-1", "investor_id": "inv-1", "amount": self.income_amount, "frequency": "Monthly"}]

        def get_expenses(self, planning_unit_id):
            return [{"expense_id": "expense-1", "amount": 4000, "frequency": "Monthly"}]

    data = MutableDataRepository()
    snapshots = FakeSnapshotRepository()
    service = FinancialStateService(
        repository=data,
        snapshot_repository=snapshots,
    )

    first = service.current("pu-1")
    assert first.income_monthly.value == 10000
    assert len(snapshots.saved) == 1

    data.income_amount = 15000
    refreshed = service.current("pu-1")

    assert refreshed.income_monthly.value == 15000
    assert len(snapshots.saved) == 2
    assert snapshots.saved[-1]["authority"]["source"] == "backend_derived"


def test_action_completion_snapshot_remains_authoritative_until_raw_inputs_change():
    class MutableDataRepository(FakeDataRepository):
        income_amount = 10000

        def get_income(self, planning_unit_id):
            return [{"income_id": "income-1", "investor_id": "inv-1", "amount": self.income_amount, "frequency": "Monthly"}]

    data = MutableDataRepository()
    snapshots = FakeSnapshotRepository()
    service = FinancialStateService(repository=data, snapshot_repository=snapshots)
    source = service.get_current_snapshot("pu-1")
    actual = service._build_from_inputs(
        "pu-1",
        "family",
        None,
        data.get_financial_state_inputs("pu-1"),
    ).model_copy(update={"total_assets": Metric(value=123456, available=True)})
    service.save_actual_state(
        actual,
        "action-1",
        "strategy-version-1",
        source["snapshot_id"],
        source["authority"]["input_revision"],
    )

    current = service.current("pu-1")
    assert current.total_assets.value == 123456
    assert snapshots.saved[-1]["authority"]["action_id"] == "action-1"
    assert snapshots.saved[-1]["authority"]["strategy_version_id"] == "strategy-version-1"

    data.income_amount = 12000
    refreshed = service.current("pu-1")
    assert refreshed.income_monthly.value == 12000
    assert refreshed.total_assets.value == 0
    assert snapshots.saved[-1]["authority"]["source"] == "backend_derived"


def test_action_snapshot_without_completed_action_lineage_is_not_authoritative():
    data = FakeDataRepository()
    snapshots = FakeSnapshotRepository()
    service = FinancialStateService(repository=data, snapshot_repository=snapshots)
    actual = service._build_from_inputs(
        "pu-1", "family", None, data.get_financial_state_inputs("pu-1")
    )
    actual = actual.model_copy(update={"total_assets": Metric(value=123456, available=True)})
    source = service.get_current_snapshot("pu-1")
    service.save_actual_state(
        actual,
        "action-1",
        "strategy-version-1",
        source["snapshot_id"],
        source["authority"]["input_revision"],
    )
    snapshots.lineage_valid = False

    current = service.current("pu-1")

    assert current.total_assets.value == 0
    assert snapshots.saved[-1]["authority"]["source"] == "backend_derived"


def test_action_completion_rejects_snapshot_token_when_raw_inputs_changed():
    class MutableDataRepository(FakeDataRepository):
        income_amount = 10000

        def get_income(self, planning_unit_id):
            return [{"income_id": "income-1", "investor_id": "inv-1", "amount": self.income_amount, "frequency": "Monthly"}]

    data = MutableDataRepository()
    snapshots = FakeSnapshotRepository()
    service = FinancialStateService(repository=data, snapshot_repository=snapshots)
    source = service.get_current_snapshot("pu-1")
    actual = service._build_from_inputs(
        "pu-1", "family", None, data.get_financial_state_inputs("pu-1")
    )
    data.income_amount = 12000

    with pytest.raises(HTTPException) as error:
        service.save_actual_state(
            actual,
            "action-1",
            "strategy-version-1",
            source["snapshot_id"],
            source["authority"]["input_revision"],
        )

    assert error.value.status_code == 409
    assert len(snapshots.saved) == 2
    assert snapshots.saved[-1]["authority"]["source"] == "backend_derived"


def test_profile_uses_current_financial_state_and_excludes_internal_authority_metadata():
    service = ProfileService.__new__(ProfileService)
    service.repository = MagicMock()
    service.repository.next_version.return_value = 1
    service.repository.create_run.return_value = {"profile_run_id": "profile-1"}
    service.financial_state_service = MagicMock()
    service.financial_state_service.get_current_snapshot.return_value = {
        "snapshot_id": "snapshot-1",
        "financial_state": {
            "planning_unit_id": "pu-1",
            "scope": "individual",
            "investor_id": "investor-1",
            "__snapshot_authority": {"input_revision": "internal"},
        },
    }
    service.engine = MagicMock()
    service.engine.build.return_value = {
        "engine_version": "1",
        "constraints": [],
        "conflicts": [],
    }
    request = SimpleNamespace(
        financial_snapshot_id=None,
        planning_unit_id="pu-1",
        investor_id="investor-1",
        declared_constraints=[],
        observed_behavior=[],
        preferences=[],
        constraint_priorities=[],
        profile_version="1",
    )

    service.build(request)

    service.financial_state_service.get_current_snapshot.assert_called_once_with(
        "pu-1", "individual", "investor-1"
    )
    assert service.engine.build.call_args.kwargs["financial_state"] == {
        "planning_unit_id": "pu-1",
        "scope": "individual",
        "investor_id": "investor-1",
    }
    request.financial_snapshot_id = "stale-snapshot"
    with pytest.raises(ValueError, match="snapshot is stale"):
        service.build(request)
