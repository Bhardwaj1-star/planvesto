import pytest

from models.strategy_edit import StrategyEditRequest
from services.strategy_edit_service import StrategyEditService


class FakeVersionRepo:
    def __init__(self):
        self.saved = []
        self.client = None

    def get_version(self, planning_unit_id, strategy_id, version):
        if version == 1:
            from models.strategy_version import StrategyVersion
            return StrategyVersion(
                strategy_version_id="v1",
                planning_unit_id=planning_unit_id,
                strategy_id=strategy_id,
                version=1,
                library_version="1.0",
                implementation_version="1.0",
                implementation_parameters={},
                status="primary",
            )
        return None

    def get_latest_version(self, planning_unit_id, strategy_id):
        return self.get_version(planning_unit_id, strategy_id, 1)

    def save_version(self, version):
        self.saved.append(version)
        return version.model_copy(update={"strategy_version_id": "v2"})


class FakePrimaryRepo:
    def get_current(self, planning_unit_id):
        return None


def test_edit_requires_existing_parent(monkeypatch):
    repo = FakeVersionRepo()
    service = StrategyEditService(repo)
    monkeypatch.setattr(service, "primary_repository", FakePrimaryRepo())
    request = StrategyEditRequest(
        planning_unit_id="pu-1",
        strategy_id="strat-cap-preservation",
        parent_version=99,
        implementation_parameters={},
    )
    with pytest.raises(Exception):
        service.edit_strategy(request)
