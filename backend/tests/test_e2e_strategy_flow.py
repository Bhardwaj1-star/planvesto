"""
End-to-End Verification Test for Strategy Conversion Spec
==========================================================
Verifies the complete flow required by STRATEGY_CONVERSION_SPEC.md:
Goal Planner → Defined Goal → Strategy Builder → Strategy Architecture →
Recommendation → Strategy Selection → Retirement Report → PDF Export.
"""

from unittest.mock import MagicMock
from engines.rules.engine import RuleEngine
from engines.strategy.engine import StrategyEngine
from models.defined_goal import DefinedGoal
from models.strategy import InvestorPriorities, StrategyRun
from schemas.strategy import StrategySelectRequest
from services.strategy_service import StrategyService
from services.goal_report_service import GoalReportService


def _create_test_defined_goal(goal_type="Retirement"):
    return DefinedGoal(defined_goal_id="dg_retire_001", goal_id="goal_retire_001", planning_unit_id="pu_investor_001", version=1, is_latest=True, goal_type=goal_type, goal_name="Retirement Corpus Planning", today_cost=5000000.0, inflation_rate=0.06, target_month=12, target_year=2045, duration_years=20.0, future_target=16035677.0, priority="Critical", flexibility="Fixed", funding_gap=8000000.0, funding_status="Shortfall")


def test_end_to_end_strategy_conversion_engine_and_pdf():
    defined_goal = _create_test_defined_goal("Retirement")
    financial_context = {"monthly_cash_flow": 80000.0, "emergency_fund_months": 6.0, "existing_corpus": 2000000.0}
    rule_engine = RuleEngine()
    rule_assessment = rule_engine.assess(defined_goal, financial_context)
    assert rule_assessment.eligible is True
    priorities = InvestorPriorities(safety=0.2, liquidity=0.2, growth=0.4, flexibility=0.2)
    strategy_engine = StrategyEngine()
    result = strategy_engine.execute(defined_goal=defined_goal, priorities=priorities, financial_context=financial_context, rule_assessment=rule_assessment)
    assert result is not None
    assert len(result.applicable_strategies) > 0
    assert len(result.rankings) > 0
    assert len(result.architectures) > 0
    assert result.recommendation is not None
    assert result.recommendation.recommended_strategy_id != ""
    primary_arch = result.architectures[0]
    assert primary_arch.architecture_id != ""
    assert primary_arch.primary_strategy_id != ""
    assert isinstance(primary_arch.technique_ids, list)
    assert isinstance(primary_arch.trade_offs, list)
    assert isinstance(primary_arch.constraints, list)
    assert primary_arch.feasibility_status in ["feasible", "conditional", "infeasible"]
    recommended_ranking = next((r for r in result.rankings if r.strategy_id == result.recommendation.recommended_strategy_id), None)
    assert recommended_ranking is not None
    assert recommended_ranking.is_eligible is True
    assert "growth" in recommended_ranking.evidence_scores
    assert "funding_gap" in recommended_ranking.evidence_scores
    matched_strategy_def = next(s for s in result.applicable_strategies if s.strategy_id == recommended_ranking.strategy_id)
    assert matched_strategy_def.strategic_objective != ""
    assert matched_strategy_def.core_mechanism != ""
    recommended_scenario = next(s for s in result.scenarios if s.strategy_id == recommended_ranking.strategy_id)
    strategy_run = StrategyRun(strategy_run_id="run_retire_001", planning_unit_id="pu_investor_001", goal_id="goal_retire_001", defined_goal_id=defined_goal.defined_goal_id, defined_goal_version=defined_goal.version, run_version=1, is_latest=True, status="completed", applicable_strategies=result.applicable_strategies, scenarios=result.scenarios, investor_priorities=result.priorities, comparison_matrix=result.comparison_matrix, rankings=result.rankings, recommendation=result.recommendation, architectures=result.architectures, selected_strategy_id=recommended_ranking.strategy_id, selected_scenario_id=recommended_scenario.scenario_id, selected_architecture=primary_arch)
    assert strategy_run.selected_strategy_id == recommended_ranking.strategy_id
    assert strategy_run.selected_architecture is not None
    report_service = GoalReportService()
    report_service.strategy_repo.get_run_by_id = MagicMock(return_value=strategy_run)
    report_service.goal_repo.get_defined_goal_by_version = MagicMock(return_value=defined_goal)
    report_service.goal_repo.get_latest_defined_goal = MagicMock(return_value=defined_goal)
    report_service.financial_state_repo.get_latest = MagicMock(return_value=None)
    report = report_service.build_report("pu_investor_001", "run_retire_001")
    assert report is not None
    assert report["goal"]["type"] == "Retirement"
    assert "goal_calculation" in report
    pdf_bytes = report_service.generate_pdf("pu_investor_001", "run_retire_001")
    assert pdf_bytes is not None
    assert len(pdf_bytes) > 1000
    assert pdf_bytes.startswith(b"%PDF-"), "Exported bytes must be a valid PDF document"


def test_end_to_end_strategy_service_flow_with_mocks():
    service = StrategyService()
    mock_defined_goal = _create_test_defined_goal("Retirement")
    service.goal_repo.get_latest_defined_goal = MagicMock(return_value=mock_defined_goal)
    service.goal_repo.get_defined_goal_by_version = MagicMock(return_value=mock_defined_goal)
    service.strat_repo.get_latest_run = MagicMock(return_value=None)
    saved_runs = {}
    def mock_save_run(run):
        run.strategy_run_id = run.strategy_run_id or "run_mock_123"
        saved_runs[run.strategy_run_id] = run
        return run.strategy_run_id
    service.strat_repo.save_run = MagicMock(side_effect=mock_save_run)
    service.strat_repo.get_run_by_id = MagicMock(side_effect=lambda pu, rid: saved_runs.get(rid))
    service.strat_repo.update_selection = MagicMock()
    service.financial_state_repo.get_latest = MagicMock(return_value=None)
    mock_version = MagicMock(strategy_version_id="ver_mock_001", version=1, implementation_parameters={"equity_allocation": 0.7})
    service.strategy_version_service.create_version = MagicMock(return_value=mock_version)
    priorities = InvestorPriorities(safety=0.25, liquidity=0.25, growth=0.25, flexibility=0.25)
    run = service.build_strategy("pu_investor_001", "goal_retire_001", priorities)
    assert run.strategy_run_id == "run_mock_123"
    assert run.recommendation is not None
    assert len(run.rankings) > 0
    recommended_strat_id = run.recommendation.recommended_strategy_id
    recommended_scen_id = run.recommendation.recommended_scenario_id
    select_req = StrategySelectRequest(planning_unit_id="pu_investor_001", strategy_run_id="run_mock_123", selected_strategy_id=recommended_strat_id, selected_scenario_id=recommended_scen_id)
    selected_run = service.select_strategy(select_req)
    assert selected_run.selected_strategy_id == recommended_strat_id
    service.report_service.strategy_repo.get_run_by_id = MagicMock(return_value=selected_run)
    service.report_service.goal_repo.get_defined_goal_by_version = MagicMock(return_value=mock_defined_goal)
    service.report_service.goal_repo.get_latest_defined_goal = MagicMock(return_value=mock_defined_goal)
    service.report_service.financial_state_repo.get_latest = MagicMock(return_value=None)
    report_dict = service.get_retirement_report("pu_investor_001", "run_mock_123")
    assert report_dict is not None
    assert "goal_calculation" in report_dict or "goal_name" in report_dict
    pdf_bytes = service.report_service.generate_pdf("pu_investor_001", "run_mock_123")
    assert pdf_bytes.startswith(b"%PDF-")
