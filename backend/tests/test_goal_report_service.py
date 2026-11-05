from unittest.mock import MagicMock

from models.strategy import (
    InvestorPriorities,
    Scenario,
    StrategyArchitecture,
    StrategyDefinition,
    StrategyRecommendation,
    StrategyRun,
)
from services.goal_report_service import GoalReportService
from models.strategy_version import StrategyVersion
import pytest


@pytest.fixture(autouse=True)
def _financial_state_without_external_data(monkeypatch):
    monkeypatch.setattr(
        "services.goal_report_service.FinancialStateService.current",
        lambda *args, **kwargs: None,
    )


class Goal:
    planning_unit_id = "p1"
    goal_id = "g1"
    defined_goal_id = "dg1"
    goal_name = "Dream Home"
    goal_type = "dream_home"
    priority = "High"
    flexibility = "Flexible"
    status = "Active"
    version = 1
    target_month = 6
    target_year = 2035
    duration_years = 9
    today_cost = 10000000
    inflation_rate = 0.06
    future_target = 17000000
    funding_gap = 10000000
    required_monthly_contribution = 50000
    projected_mapped_asset_value = 7000000
    funding_return_assumption = 0.10
    funding_status = "Shortfall"
    feasibility_status = "constrained"
    feasibility_reason = "Required contribution exceeds current surplus."
    available_monthly_surplus = 30000
    monthly_contribution_surplus_gap = 20000
    funding_strategies = [] 
    mapped_assets = []


def make_run():
    strategy = StrategyDefinition(
        strategy_id="strat-goal-funding",
        name="Goal Funding",
        tagline="Fund the goal",
        description="Fund a defined goal.",
        strategic_objective="Match future funding requirements with resources.",
        applicable_goal_types=["dream_home"],
        technique_ids=["tech-asset-earmarking"],
        component_ids=["component-funding"],
    )
    scenario = Scenario(
        scenario_id="scen-sip",
        strategy_id="strat-goal-funding",
        funding_strategy_id="sip",
        scenario_name="Goal Funding — SIP",
        funding_structure={"required_monthly_contribution": 50000},
        metrics={"funding_status": "constrained"},
        trade_off_notes="Higher monthly burden.",
    )
    architecture = StrategyArchitecture(
        architecture_id="arch-g1",
        primary_strategy_id="strat-goal-funding",
        solution_ids=["solution-strat-goal-funding-sip"],
        technique_ids=["tech-asset-earmarking"],
    )
    recommendation = StrategyRecommendation(
        recommended_strategy_id="strat-goal-funding",
        recommended_scenario_id="scen-sip",
        short_reasons=["Funding gap requires additional contribution."],
        complete_reasoning="The engine compared applicable funding paths.",
        architecture=architecture,
    )
    return StrategyRun(
        what_if_scenarios=[Scenario(
            scenario_id="whatif-1",
            strategy_id="strat-goal-funding",
            scenario_type="custom",
            scenario_name="What-if: Monthly contribution +10%",
            funding_structure={"additional_monthly_contribution": 5000},
            metrics={"remaining_gap": 1000},
            trade_off_notes="Higher monthly burden.",
        )],
        planning_unit_id="p1",
        goal_id="g1",
        defined_goal_id="dg1",
        defined_goal_version=1,
        applicable_strategies=[strategy],
        scenarios=[scenario],
        investor_priorities=InvestorPriorities(),
        rankings=[],
        recommendation=recommendation,
        architectures=[architecture],
        selected_strategy_id="strat-goal-funding",
        selected_scenario_id="scen-sip",
        selected_architecture=architecture,
        run_metadata={},
    )


def test_report_contains_decision_sections(monkeypatch):
    service = GoalReportService()
    run = make_run()

    monkeypatch.setattr(service, "_load", lambda p, s: (run, Goal(), {
        "annual_income": 1200000,
        "annual_expenses": 840000,
        "monthly_surplus": 30000,
        "assets": 7000000,
        "liabilities": 0,
        "net_worth": 7000000,
    }))

    report = service.build_report("p1", "run1")

    assert report["report_type"] == "goal_decision_report"
    assert "what_if_analysis" in report
    assert "trade_off_analysis" in report
    assert report["strategy"]["architecture"]["solution_ids"] == [
        "solution-strat-goal-funding-sip"
    ]
    assert report["decision"]["status"] == "investor_decision_required"


def test_report_exposes_scenario_outputs(monkeypatch):
    service = GoalReportService()
    run = make_run()
    monkeypatch.setattr(service, "_load", lambda p, s: (run, Goal(), {}))

    report = service.build_report("p1", "run1")

    assert len(report["what_if_analysis"]) == 1
    assert report["what_if_analysis"][0]["trade_off"] == "Higher monthly burden."


def test_report_source_is_selected_strategy_version(monkeypatch):
    service = GoalReportService()
    service.strategy_version_repo.get_by_id = lambda planning_unit_id, strategy_version_id: StrategyVersion(
        strategy_version_id=strategy_version_id,
        planning_unit_id=planning_unit_id,
        strategy_id="strat-goal-funding",
        version=1,
        library_version="1.0.0",
        implementation_version="1.0.0",
        implementation_parameters={},
        goal_id="g1",
        defined_goal_id="dg1",
        defined_goal_version=1,
        architecture=make_run().selected_architecture,
        decision_snapshot={
            "selected_scenario_id": "scen-sip",
            "applicable_strategies": [
                item.model_dump(mode="json") for item in make_run().applicable_strategies
            ],
            "scenarios": [
                item.model_dump(mode="json") for item in make_run().scenarios
            ],
            "what_if_scenarios": [
                item.model_dump(mode="json") for item in make_run().what_if_scenarios
            ],
            "investor_priorities": make_run().investor_priorities.model_dump(mode="json"),
            "rankings": [],
            "recommendation": {
                **make_run().recommendation.model_dump(mode="json"),
                "recommended_strategy_id": "strat-goal-funding",
                "architecture": None,
            },
        },
        source_strategy_run_id="run-source",
    )
    service.goal_repo.get_defined_goal_by_version = lambda *args: Goal()
    service.strategy_repo.get_run_by_id = MagicMock(
        side_effect=AssertionError("Version report must not read StrategyRun")
    )
    service.financial_state_service.current = lambda *args: None

    loaded_run, _, _ = service._load_by_strategy_version("p1", "sv-selected")

    assert loaded_run["strategy_run_id"] == "run-source"
    assert loaded_run["selected_strategy_id"] == "strat-goal-funding"
    assert loaded_run["selected_architecture"]["architecture_id"] == "arch-g1"
    service.strategy_repo.get_run_by_id.assert_not_called()
