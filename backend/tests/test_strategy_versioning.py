import pytest

from backend.data.strategy_version_repository import StrategyVersionRepository
from backend.models.strategy import StrategyDefinition, StrategyImplementationParamDef
from backend.models.strategy_version import StrategyVersion
from backend.services.strategy_version_service import StrategyVersionService


class FakeRepository:
    def __init__(self):
        self.versions = []

    def get_latest_version(self, planning_unit_id, strategy_id):
        matches = [
            item for item in self.versions
            if item.planning_unit_id == planning_unit_id and item.strategy_id == strategy_id
        ]
        return max(matches, key=lambda item: item.version) if matches else None

    def get_version(self, planning_unit_id, strategy_id, version):
        return next(
            (
                item for item in self.versions
                if item.planning_unit_id == planning_unit_id
                and item.strategy_id == strategy_id
                and item.version == version
            ),
            None,
        )

    def save_version(self, version):
        self.versions.append(version)
        return version


def make_strategy():
    return StrategyDefinition(
        strategy_id="test-strategy",
        name="Test Strategy",
        tagline="Test",
        description="Test strategy",
        applicable_goal_types=["Other"],
        implementation_parameters=[
            StrategyImplementationParamDef(
                name="allocation_pct",
                label="Allocation",
                param_type="percentage",
                description="Allocation",
                default_value=60,
                min_value=30,
                max_value=80,
            ),
            StrategyImplementationParamDef(
                name="cadence",
                label="Cadence",
                param_type="choice",
                description="Cadence",
                default_value="Annual",
                choices=["Annual", "Semi-Annual"],
            ),
            StrategyImplementationParamDef(
                name="locked_value",
                label="Locked",
                param_type="integer",
                description="Locked value",
                default_value=2,
                min_value=1,
                max_value=5,
                editable=False,
            ),
        ],
    )


def test_first_version_is_one():
    repository = FakeRepository()
    service = StrategyVersionService(repository)
    version = service.create_version("pu-1", "strat-cap-preservation")
    assert version.version == 1
    assert version.parent_version is None
    assert version.source == "library"


def test_investor_edit_requires_parent_version():
    repository = FakeRepository()
    service = StrategyVersionService(repository)
    with pytest.raises(ValueError, match="parent_version"):
        service.create_version(
            "pu-1", "strat-cap-preservation", source="investor_edit"
        )


def test_missing_parameters_use_defaults_and_create_next_version():
    repository = FakeRepository()
    service = StrategyVersionService(repository)
    first = service.create_version("pu-1", "test-strategy")
    second = service.create_version(
        "pu-1",
        "test-strategy",
        parameters={"allocation_pct": 70},
        parent_version=first.version,
        source="investor_edit",
    )
    assert second.version == 2
    assert second.parent_version == 1
    assert second.implementation_parameters == {
        "allocation_pct": 70,
        "cadence": "Annual",
        "locked_value": 2,
    }


def test_unknown_parameter_rejected():
    service = StrategyVersionService(FakeRepository())
    with pytest.raises(ValueError, match="Unknown implementation parameters"):
        service.validate_parameters(make_strategy(), {"does_not_exist": 10})


def test_non_editable_parameter_rejected_when_changed():
    repository = FakeRepository()
    service = StrategyVersionService(repository)
    first = service.create_version("pu-1", "test-strategy")
    with pytest.raises(ValueError, match="not editable"):
        service.create_version(
            "pu-1",
            "test-strategy",
            parameters={"locked_value": 3},
            parent_version=first.version,
            source="investor_edit",
        )


def test_numeric_bounds_rejected():
    service = StrategyVersionService(FakeRepository())
    with pytest.raises(ValueError, match="below minimum"):
        service.validate_parameters(make_strategy(), {"allocation_pct": 20})
    with pytest.raises(ValueError, match="above maximum"):
        service.validate_parameters(make_strategy(), {"allocation_pct": 90})


def test_choice_rejected():
    service = StrategyVersionService(FakeRepository())
    with pytest.raises(ValueError, match="Invalid choice"):
        service.validate_parameters(make_strategy(), {"cadence": "Monthly"})


def test_valid_edit_is_accepted():
    repository = FakeRepository()
    service = StrategyVersionService(repository)
    first = service.create_version("pu-1", "test-strategy")
    second = service.create_version(
        "pu-1",
        "test-strategy",
        parameters={"allocation_pct": 70, "cadence": "Semi-Annual"},
        parent_version=first.version,
        source="investor_edit",
    )
    assert second.implementation_parameters["allocation_pct"] == 70
    assert second.implementation_parameters["cadence"] == "Semi-Annual"
    assert second.implementation_parameters["locked_value"] == 2


def test_strategy_version_domain_requires_parent_for_investor_edit():
    with pytest.raises(ValueError, match="parent_version"):
        StrategyVersion(
            planning_unit_id="pu-1",
            strategy_id="test-strategy",
            version=1,
            source="investor_edit",
            library_version="1.0",
            implementation_version="1.0",
        )


def test_repository_is_insert_read_only():
    public_methods = {
        name for name in dir(StrategyVersionRepository)
        if not name.startswith("_")
    }
    assert "save_version" in public_methods
    assert "get_version" in public_methods
    assert "get_latest_version" in public_methods
    assert "update_version" not in public_methods
    assert "delete_version" not in public_methods
