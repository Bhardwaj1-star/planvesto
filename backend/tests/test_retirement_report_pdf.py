from unittest.mock import MagicMock
from models.defined_goal import DefinedGoal
from models.strategy import (
    InvestorPriorities,
    StrategyArchitecture,
    StrategyDefinition,
    StrategyRecommendation,
    StrategyRun,
    Scenario,
)
from services.goal_report_service import GoalReportService


def _sample_retirement_run():
    strat = StrategyDefinition(
        strategy_id="strat-retirement-diversified",
        name="Diversified Retirement Strategy",
        tagline="Balanced growth with progressive risk management.",
        description="Core retirement accumulation strategy.",
        strategy_family="Retirement Accumulation",
        strategic_objective="Build corpus while mitigating sequence-of-returns risk.",
        core_mechanism="Multi-asset allocation shifting toward debt near retirement.",
        principles=["Accumulate equity early", "De-risk into retirement"],
    )
    scen = Scenario(
        scenario_id="scen-ret-base",
        strategy_id="strat-retirement-diversified",
        scenario_name="Base Case (7% real)",
        scenario_type="baseline",
        assumptions={"return_rate": 0.11, "inflation": 0.06},
        metrics={"target_corpus": 14379000.0, "projected_corpus": 15000000.0},
        is_selected=True,
    )
    arch = StrategyArchitecture(
        architecture_id="arch-ret-1",
        primary_strategy_id="strat-retirement-diversified",
        technique_ids=["tech-equity-growth", "tech-debt-ladder"],
        trade_offs=["Higher initial equity exposure requires tolerance for drawdowns"],
        constraints=["Emergency fund intact", "No high-cost debt"],
        feasibility_status="feasible",
    )
    return StrategyRun(
        strategy_run_id="run-ret-canonical-1",
        planning_unit_id="pu-ret-canonical-1",
        goal_id="goal-ret-1",
        defined_goal_id="dg-ret-1",
        defined_goal_version=1,
        run_version=1,
        is_latest=True,
        status="completed",
        applicable_strategies=[strat],
        scenarios=[scen],
        investor_priorities=InvestorPriorities(safety=0.3, liquidity=0.2, growth=0.4, flexibility=0.1),
        recommendation=StrategyRecommendation(
            recommended_strategy_id="strat-retirement-diversified",
            recommended_scenario_id="scen-ret-base",
            architecture=arch,
            short_reasons=["High corpus growth", "Fits investor horizon"],
            complete_reasoning="The diversified retirement strategy provides the required real returns while mitigating risk as retirement nears.",
        ),
        architectures=[arch],
        selected_strategy_id="strat-retirement-diversified",
        selected_scenario_id="scen-ret-base",
        selected_architecture=arch,
        run_metadata={"technique_outputs": []},
    )


def test_retirement_report_pdf_renders_via_canonical_goal_report_service():
    """Verify retirement goals generate canonical Goal Decision Report and valid PDF without legacy renderer/exporter."""
    goal = DefinedGoal(
        planning_unit_id="pu-ret-canonical-1",
        goal_id="goal-ret-1",
        goal_name="Retirement Corpus Planning",
        goal_type="Retirement",
        today_cost=5000000.0,
        target_month=12,
        target_year=2045,
        duration_years=20.0,
        inflation_rate=0.06,
        priority="Critical",
        flexibility="Fixed",
        future_target=16035677.0,
        funding_gap=8000000.0,
        funding_status="Shortfall",
        projected_mapped_asset_value=8035677.0,
        required_monthly_contribution=35000.0,
    )
    run = _sample_retirement_run()

    report_service = GoalReportService()
    report_service.strategy_repo.get_run_by_id = MagicMock(return_value=run)
    report_service.goal_repo.get_defined_goal_by_version = MagicMock(return_value=goal)
    report_service.goal_repo.get_latest_defined_goal = MagicMock(return_value=goal)
    report_service.financial_state_repo.get_latest = MagicMock(return_value=None)

    report = report_service.build_report("pu-ret-canonical-1", "run-ret-canonical-1")
    assert report["report_type"] == "goal_decision_report"
    assert report["goal"]["type"] == "Retirement"
    assert report["strategy"]["selected_strategy_id"] == "strat-retirement-diversified"

    pdf_bytes = report_service.generate_pdf("pu-ret-canonical-1", "run-ret-canonical-1")
    assert pdf_bytes.startswith(b"%PDF")
    assert len(pdf_bytes) > 1000


def test_canonical_goal_report_service_works_for_non_retirement_goal():
    """Canonical GoalReportService generates PDF seamlessly for non-retirement goals."""
    goal = DefinedGoal(
        planning_unit_id="pu-edu-1",
        goal_id="goal-edu-1",
        goal_name="Child College Education",
        goal_type="education",
        today_cost=2000000.0,
        target_month=6,
        target_year=2035,
        duration_years=10.0,
        inflation_rate=0.08,
        priority="Critical",
        flexibility="Fixed",
        future_target=4317850.0,
        funding_gap=2317850.0,
        funding_status="Shortfall",
        projected_mapped_asset_value=2000000.0,
        required_monthly_contribution=12000.0,
    )
    run = _sample_retirement_run()

    report_service = GoalReportService()
    report_service.strategy_repo.get_run_by_id = MagicMock(return_value=run)
    report_service.goal_repo.get_defined_goal_by_version = MagicMock(return_value=goal)
    report_service.goal_repo.get_latest_defined_goal = MagicMock(return_value=goal)
    report_service.financial_state_repo.get_latest = MagicMock(return_value=None)

    pdf_bytes = report_service.generate_pdf("pu-edu-1", "run-ret-canonical-1")
    assert pdf_bytes.startswith(b"%PDF")
    assert len(pdf_bytes) > 1000
