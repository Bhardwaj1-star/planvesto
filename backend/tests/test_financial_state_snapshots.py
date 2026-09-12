from types import SimpleNamespace

import pytest

from services.financial_state_service import FinancialStateService


class FakeDataRepository:
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
        return SimpleNamespace(
            model_dump=lambda mode=None: {
                "planning_unit_id": kwargs["planning_unit_id"],
                "scope": kwargs["scope"],
                "investor_id": kwargs["investor_id"],
                "net_worth": {"value": 100000, "available": True, "reason": None},
            }
        )


class FakeSnapshotRepository:
    def __init__(self):
        self.saved = []

    def save_snapshot(self, **kwargs):
        self.saved.append(kwargs)
        return {"snapshot_id": "snap-1", **kwargs}


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
