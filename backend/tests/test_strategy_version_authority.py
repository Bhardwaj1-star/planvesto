from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException
from data.strategy_repository import StrategyRepository
from models.defined_goal import DefinedGoal
from models.strategy import (
    InvestorPriorities,
    Scenario,
    StrategyArchitecture,
    StrategyRecommendation,
    StrategyRun,
)
from models.strategy_version import StrategyVersion
from schemas.strategy import StrategyImplementationFinalizeRequest
from services.strategy_service import StrategyService


class FakeQuery:
    def __init__(self, table_name, result, calls):
        self.table_name = table_name
        self.result = result
        self.calls = calls
        self.single = False

    def select(self, *_args):
        return self

    def eq(self, *_args):
        return self

    def maybe_single(self):
        self.single = True
        return self

    def upsert(self, payload, **kwargs):
        self.calls.append((self.table_name, payload, kwargs))
        return self

    def execute(self):
        data = self.result
        if self.single and isinstance(data, list):
            data = data[0] if data else None
        return SimpleNamespace(data=data)


class FakeDatabase:
    def __init__(self, results):
        self.results = results
        self.calls = []
        self.queried_tables = []

    def table(self, table_name):
        self.queried_tables.append(table_name)
        result = self.results.get(table_name)
        if callable(result):
            result = result()
        return FakeQuery(table_name, result, self.calls)


def version_row(**overrides):
    return {
        "strategy_version_id": "sv-1",
        "planning_unit_id": "pu-1",
        "strategy_id": "strat-1",
        "version": 1,
        "library_version": "1.0",
        "implementation_version": "1.0",
        "implementation_parameters": {},
        "goal_id": "goal-1",
        "defined_goal_id": "dg-2",
        "defined_goal_version": 2,
        "source_strategy_run_id": "run-source",
        "architecture": {
            "architecture_id": "arch-1",
            "primary_strategy_id": "strat-1",
            "supporting_strategy_ids": [],
            "technique_ids": [],
            "rationale": [],
            "trade_offs": [],
            "feasibility_status": "feasible",
            "constraints": [],
        },
        "decision_snapshot": {
            "selected_scenario_id": "scenario-1",
            "scenarios": [{"scenario_id": "scenario-1"}],
            "recommendation": {
                "recommended_strategy_id": "strat-1",
                "recommended_scenario_id": "scenario-1",
            },
        },
        **overrides,
    }


def test_selected_strategy_version_comes_from_explicit_pointer_not_run_history():
    database = FakeDatabase({
        "goal_strategy_selections": [{
            "defined_goal_id": "dg-2",
            "defined_goal_version": 2,
            "strategy_version_id": "sv-1",
        }],
        "defined_goals": [{
            "defined_goal_id": "dg-2",
            "version": 2,
        }],
        "strategy_versions": [version_row()],
    })
    repository = StrategyRepository.__new__(StrategyRepository)
    repository.db = database

    selected = repository.get_selected_strategy_version("pu-1", "goal-1")

    assert selected is not None
    assert selected.strategy_version_id == "sv-1"
    assert selected.defined_goal_id == "dg-2"
    assert "strategy_runs" not in database.queried_tables


def test_strategy_version_selection_is_not_current_after_defined_goal_revision():
    database = FakeDatabase({
        "goal_strategy_selections": [{
            "defined_goal_id": "dg-1",
            "defined_goal_version": 1,
            "strategy_version_id": "sv-old",
        }],
        "defined_goals": [{
            "defined_goal_id": "dg-2",
            "version": 2,
        }],
    })
    repository = StrategyRepository.__new__(StrategyRepository)
    repository.db = database

    assert repository.get_selected_strategy_version_id("pu-1", "goal-1") is None
    assert "strategy_versions" not in database.queried_tables
    assert "strategy_runs" not in database.queried_tables


def test_selected_pointer_rejects_version_with_different_goal_revision_binding():
    database = FakeDatabase({
        "goal_strategy_selections": {
            "defined_goal_id": "dg-2",
            "defined_goal_version": 2,
            "strategy_version_id": "sv-1",
        },
        "defined_goals": {
            "defined_goal_id": "dg-2",
            "version": 2,
        },
        "strategy_versions": version_row(defined_goal_id="dg-1"),
    })
    repository = StrategyRepository.__new__(StrategyRepository)
    repository.db = database

    assert repository.get_selected_strategy_version_id("pu-1", "goal-1") is None
    assert "strategy_runs" not in database.queried_tables


def test_selected_pointer_rejects_version_bound_to_another_goal():
    database = FakeDatabase({
        "goal_strategy_selections": {
            "defined_goal_id": "dg-2",
            "defined_goal_version": 2,
            "strategy_version_id": "sv-1",
        },
        "defined_goals": {
            "defined_goal_id": "dg-2",
            "version": 2,
        },
        "strategy_versions": version_row(goal_id="goal-other"),
    })
    repository = StrategyRepository.__new__(StrategyRepository)
    repository.db = database

    assert repository.get_selected_strategy_version_id("pu-1", "goal-1") is None
    assert "strategy_runs" not in database.queried_tables


def test_pointer_rejects_selection_for_stale_defined_goal_version():
    database = FakeDatabase({
        "defined_goals": [{
            "defined_goal_id": "dg-current",
            "version": 3,
        }],
    })
    repository = StrategyRepository.__new__(StrategyRepository)
    repository.db = database
    version = type("Version", (), {
        "strategy_version_id": "sv-old",
        "planning_unit_id": "pu-1",
        "goal_id": "goal-1",
        "defined_goal_id": "dg-old",
        "defined_goal_version": 2,
    })()

    try:
        repository.set_selected_strategy_version(version)
    except ValueError as error:
        assert "stale DefinedGoal" in str(error)
    else:
        raise AssertionError("Stale StrategyVersion selection should be rejected")
    assert "goal_strategy_selections" not in database.queried_tables


def test_pointer_persists_explicit_goal_and_strategy_version_binding():
    database = FakeDatabase({
        "defined_goals": {
            "defined_goal_id": "dg-2",
            "version": 2,
        },
    })
    repository = StrategyRepository.__new__(StrategyRepository)
    repository.db = database
    version = StrategyVersion.model_validate(version_row())

    repository.set_selected_strategy_version(version)

    assert database.calls == [(
        "goal_strategy_selections",
        {
            "planning_unit_id": "pu-1",
            "goal_id": "goal-1",
            "defined_goal_id": "dg-2",
            "defined_goal_version": 2,
            "strategy_version_id": "sv-1",
        },
        {"on_conflict": "planning_unit_id,goal_id"},
    )]


def test_finalization_persists_goal_bound_strategy_snapshot_and_selects_it(monkeypatch):
    service = StrategyService.__new__(StrategyService)
    service.goal_repo = MagicMock()
    service.strat_repo = MagicMock()
    service.strategy_version_service = MagicMock()
    defined_goal = DefinedGoal(
        defined_goal_id="dg-1",
        planning_unit_id="pu-1",
        goal_id="goal-1",
        version=2,
        is_latest=True,
        goal_type="Education",
        goal_name="Education",
        today_cost=1000,
        inflation_rate=0.05,
        target_month=6,
        target_year=2030,
        duration_years=4,
        future_target=1200,
        priority="high",
        flexibility="fixed",
        funding_gap=500,
        funding_status="Shortfall",
    )
    architecture = StrategyArchitecture(
        architecture_id="arch-final",
        primary_strategy_id="strat-goal-funding",
    )
    run = StrategyRun(
        strategy_run_id="run-source",
        planning_unit_id="pu-1",
        goal_id="goal-1",
        defined_goal_id="dg-1",
        defined_goal_version=2,
        scenarios=[Scenario(
            scenario_id="scenario-selected",
            strategy_id="strat-goal-funding",
            scenario_name="Selected",
        )],
        investor_priorities=InvestorPriorities(),
        recommendation=StrategyRecommendation(
            recommended_strategy_id="strat-goal-funding",
            recommended_scenario_id="scenario-selected",
        ),
        run_metadata={"technique_outputs": [{"technique_id": "tech-1"}]},
    )
    version = StrategyVersion(
        strategy_version_id="sv-1",
        planning_unit_id="pu-1",
        strategy_id="strat-goal-funding",
        version=1,
        library_version="1.0",
        implementation_version="1.0",
        goal_id="goal-1",
        defined_goal_id="dg-1",
        defined_goal_version=2,
        architecture=architecture,
        source_strategy_run_id="run-source",
        decision_snapshot={
            "recommendation": {
                "recommended_strategy_id": "strat-goal-funding",
                "recommended_scenario_id": "scenario-final",
            },
        },
    )
    service._validate_selection_context = MagicMock(
        return_value=(run, None, run.scenarios[0], architecture)
    )
    service.goal_repo.get_defined_goal_by_version.return_value = defined_goal
    service.goal_repo.get_latest_defined_goal.return_value = defined_goal
    service.strategy_version_service.create_version.return_value = version
    monkeypatch.setattr(
        "services.strategy_service.create_custom_scenario",
        lambda *_args, **_kwargs: Scenario(
            scenario_id="scenario-final",
            strategy_id="strat-goal-funding",
            scenario_name="Final Implementation",
        ),
    )

    result = service.finalize_implementation(StrategyImplementationFinalizeRequest(
        planning_unit_id="pu-1",
        strategy_run_id="run-source",
        defined_goal_version=2,
        selected_strategy_id="strat-goal-funding",
        selected_scenario_id="scenario-selected",
    ))

    create_args = service.strategy_version_service.create_version.call_args.kwargs
    assert create_args["goal_id"] == "goal-1"
    assert create_args["defined_goal_id"] == "dg-1"
    assert create_args["defined_goal_version"] == 2
    assert create_args["architecture"] == architecture
    assert create_args["source_strategy_run_id"] == "run-source"
    assert create_args["decision_snapshot"]["selected_scenario_id"] == "scenario-final"
    assert create_args["decision_snapshot"]["recommendation"]["recommended_strategy_id"] == "strat-goal-funding"
    service.strat_repo.set_selected_strategy_version.assert_called_once_with(version)
    service.strat_repo.update_selection.assert_not_called()
    assert result.strategy_version_id == "sv-1"


def test_finalization_rejects_strategy_run_for_revised_defined_goal(monkeypatch):
    service = StrategyService.__new__(StrategyService)
    service.goal_repo = MagicMock()
    service.strat_repo = MagicMock()
    service.strategy_version_service = MagicMock()
    old_goal = SimpleNamespace(
        planning_unit_id="pu-1",
        goal_id="goal-1",
        defined_goal_id="dg-1",
        version=1,
    )
    current_goal = SimpleNamespace(defined_goal_id="dg-2", version=2)
    run = SimpleNamespace(
        strategy_run_id="run-old",
        defined_goal_version=1,
        goal_id="goal-1",
        defined_goal_id="dg-1",
    )
    service._validate_selection_context = MagicMock(return_value=(run, None, None, None))
    service.goal_repo.get_defined_goal_by_version.return_value = old_goal
    service.goal_repo.get_latest_defined_goal.return_value = current_goal

    with pytest.raises(HTTPException) as error:
        service.finalize_implementation(StrategyImplementationFinalizeRequest(
            planning_unit_id="pu-1",
            strategy_run_id="run-old",
            defined_goal_version=1,
            selected_strategy_id="strat-goal-funding",
            selected_scenario_id="scenario-old",
        ))

    assert error.value.status_code == 409
    service.strategy_version_service.create_version.assert_not_called()
    service.strat_repo.set_selected_strategy_version.assert_not_called()
