"""
Tests for Strategy Decision Authority Conversion
=================================================
Verifies that:
1. Changing dimension scores cannot change the selected strategy when all other decision evidence is unchanged.
2. Composite score is NOT used as decision authority.
3. Ineligible strategies cannot be recommended.
4. Recommendation comes strictly from the new decision output (DecisionResult).
5. Existing Goal -> Strategy Builder -> Strategy Result -> Retirement Report -> PDF flow remains intact.
"""

import pytest
from unittest.mock import MagicMock
from models.defined_goal import DefinedGoal
from models.strategy import (
    InvestorPriorities,
    Scenario,
    StrategyArchitecture,
    StrategyDefinition,
    StrategyRecommendation,
)
from engines.strategy.decision import evaluate_decision, DecisionResult
from engines.strategy.ranking import rank_scenarios
from engines.strategy.recommendation import generate_recommendation
from engines.strategy.engine import StrategyEngine
from services.strategy_service import StrategyService


def _sample_goal(goal_type="Child Education", duration=6.0, shortfall=500000.0, status="Shortfall"):
    return DefinedGoal(
        goal_id="g-test-decision",
        planning_unit_id="pu-test-decision",
        version=1,
        is_latest=True,
        goal_type=goal_type,
        goal_name="Test Decision Goal",
        today_cost=1000000.0,
        inflation_rate=0.06,
        target_month=6,
        target_year=2032,
        duration_years=duration,
        future_target=1418519.0,
        priority="Critical",
        flexibility="Fixed",
        funding_gap=shortfall,
        funding_status=status,
    )


def test_changing_dimension_scores_cannot_change_selected_strategy():
    """Changing dimension scores cannot change the selected strategy when decision evidence is unchanged."""
    engine = StrategyEngine()
    goal = _sample_goal()
    p_safety = InvestorPriorities(safety=0.9, liquidity=0.03, growth=0.04, flexibility=0.03)
    p_growth = InvestorPriorities(safety=0.03, liquidity=0.04, growth=0.9, flexibility=0.03)
    p_liquidity = InvestorPriorities(safety=0.04, liquidity=0.9, growth=0.03, flexibility=0.03)
    p_flexibility = InvestorPriorities(safety=0.03, liquidity=0.03, growth=0.04, flexibility=0.9)
    res_safety = engine.execute(goal, priorities=p_safety)
    res_growth = engine.execute(goal, priorities=p_growth)
    res_liquidity = engine.execute(goal, priorities=p_liquidity)
    res_flexibility = engine.execute(goal, priorities=p_flexibility)
    assert res_safety.recommendation.recommended_strategy_id == res_growth.recommendation.recommended_strategy_id
    assert res_growth.recommendation.recommended_strategy_id == res_liquidity.recommendation.recommended_strategy_id
    assert res_liquidity.recommendation.recommended_strategy_id == res_flexibility.recommendation.recommended_strategy_id
    assert res_safety.rankings[0].strategy_id == res_growth.rankings[0].strategy_id
    assert res_growth.rankings[0].strategy_id == res_liquidity.rankings[0].strategy_id


def test_composite_score_is_not_decision_authority():
    """Composite score is not used as decision authority."""
    engine = StrategyEngine()
    goal = _sample_goal()
    priorities = InvestorPriorities(safety=0.8, liquidity=0.1, growth=0.05, flexibility=0.05)
    res = engine.execute(goal, priorities=priorities)
    rec_strat = res.recommendation.recommended_strategy_id
    assert rec_strat == "strat-goal-funding"
    recommended_items = [r for r in res.rankings if r.is_recommended]
    assert len(recommended_items) == 1
    assert recommended_items[0].strategy_id == rec_strat


def test_ineligible_strategies_cannot_be_recommended():
    """Ineligible strategies cannot be recommended."""
    strat_ineligible = StrategyDefinition(
        strategy_id="strat-fake-ineligible",
        name="Fake Ineligible Strategy",
        tagline="Ineligible",
        description="Ineligible",
        strategy_family="Growth",
        strategic_objective="Ineligible",
        core_mechanism="Ineligible",
        applicable_goal_types=["NonExistentType"],
        applicable_goal_characteristics=[],
        constraints=["horizon<=1.0"],
        library_version="1.1",
        implementation_version="1.1",
        active=True,
    )
    arch_ineligible = StrategyArchitecture(
        architecture_id="arch-ineligible",
        primary_strategy_id="strat-fake-ineligible",
        supporting_strategy_ids=[],
        technique_ids=[],
        rationale=["Test"],
        trade_offs=["Test"],
        feasibility_status="infeasible",
        constraints=["Horizon constraint exceeded"],
    )
    scen_ineligible = Scenario(
        scenario_id="scen-ineligible-1",
        strategy_id="strat-fake-ineligible",
        scenario_type="baseline",
        scenario_name="Ineligible Scenario",
        assumptions={},
        funding_structure={},
        metrics={"safety_score": 10.0, "growth_score": 10.0, "liquidity_score": 10.0, "flexibility_score": 10.0},
        trade_off_notes="",
        is_investor_modified=False,
    )
    goal = _sample_goal(duration=6.0)
    decision = evaluate_decision(
        strategies=[strat_ineligible],
        scenarios=[scen_ineligible],
        architectures=[arch_ineligible],
        defined_goal=goal,
    )
    assert decision.recommended_strategy_id == ""
    assert decision.feasibility_status == "infeasible"
    rankings = rank_scenarios(
        strategies=[strat_ineligible],
        scenarios=[scen_ineligible],
        priorities=InvestorPriorities(),
        decision_result=decision,
        defined_goal=goal,
    )
    assert len(rankings) == 1
    assert rankings[0].is_eligible is False
    assert rankings[0].is_recommended is False


def test_recommendation_comes_from_new_decision_output():
    """Recommendation comes from the new decision output."""
    engine = StrategyEngine()
    goal = _sample_goal(goal_type="Retirement / Financial Freedom", duration=15.0, shortfall=2000000.0)
    priorities = InvestorPriorities(safety=0.25, liquidity=0.25, growth=0.25, flexibility=0.25)
    res = engine.execute(goal, priorities=priorities)
    rec = res.recommendation
    assert rec.recommended_strategy_id != ""
    assert rec.architecture is not None
    assert rec.architecture.primary_strategy_id == rec.recommended_strategy_id
    reasoning_text = " ".join(rec.short_reasons) + " " + rec.complete_reasoning
    assert "Strongly aligns with your priority for" not in reasoning_text
    assert "₹" in reasoning_text or "shortfall" in reasoning_text.lower() or "horizon" in reasoning_text.lower()


def test_end_to_end_goal_strategy_report_pdf_pipeline():
    """Existing Goal -> Strategy Builder -> Strategy Result -> Retirement Report -> PDF flow remains intact."""
    engine = StrategyEngine()
    goal = _sample_goal(goal_type="Retirement / Financial Freedom", duration=18.0, shortfall=3500000.0)
    res = engine.execute(goal, priorities=InvestorPriorities())
    assert res.recommendation.recommended_strategy_id != ""
    assert len(res.rankings) > 0
    service = StrategyService()
    service.goal_repo.get_latest_defined_goal = MagicMock(return_value=goal)
    service.goal_repo.get_defined_goal_by_version = MagicMock(return_value=goal)
    service.strat_repo.get_latest_run = MagicMock(return_value=None)
    saved_runs = {}

    def mock_save_run(run):
        run.strategy_run_id = run.strategy_run_id or "run-decision-e2e-123"
        saved_runs[run.strategy_run_id] = run
        return run.strategy_run_id

    service.strat_repo.save_run = MagicMock(side_effect=mock_save_run)
    service.strat_repo.get_run_by_id = MagicMock(side_effect=lambda pu, rid: saved_runs.get(rid))
    service.strat_repo.update_selection = MagicMock()
    service.financial_state_repo.get_latest = MagicMock(return_value=None)
    run = service.build_strategy(
        planning_unit_id="pu-decision-e2e",
        goal_id="g-test-decision",
        priorities=InvestorPriorities(),
    )
    assert run.strategy_run_id == "run-decision-e2e-123"
    service.report_service.strategy_repo.get_run_by_id = MagicMock(return_value=run)
    service.report_service.goal_repo.get_defined_goal_by_version = MagicMock(return_value=goal)
    service.report_service.goal_repo.get_latest_defined_goal = MagicMock(return_value=goal)
    service.report_service.financial_state_repo.get_latest = MagicMock(return_value=None)
    report_dict = service.get_retirement_report("pu-decision-e2e", "run-decision-e2e-123")
    assert report_dict is not None
    assert "goal_calculation" in report_dict or "goal_name" in report_dict
    pdf_bytes = service.report_service.generate_pdf("pu-decision-e2e", "run-decision-e2e-123")
    assert len(pdf_bytes) > 0
    assert pdf_bytes.startswith(b"%PDF-")


def test_technique_execution_is_decision_evidence():
    """Executed techniques contribute implementation-readiness evidence to the decision."""
    strat = StrategyDefinition(
        strategy_id="strat-tech-evidence",
        name="Technique Evidence Strategy",
        tagline="Test",
        description="Test",
        strategy_family="Funding",
        strategic_objective="Test",
        core_mechanism="Test",
        applicable_goal_types=["Child Education"],
        applicable_goal_characteristics=["shortfall", "fixed_timeline"],
        technique_ids=["tech-bucketing", "tech-laddering"],
        library_version="1.0",
        implementation_version="1.0",
        active=True,
    )
    arch = StrategyArchitecture(
        architecture_id="arch-tech-evidence",
        primary_strategy_id=strat.strategy_id,
        technique_ids=list(strat.technique_ids),
        rationale=["Test"],
        trade_offs=[],
    )
    scenario = Scenario(
        scenario_id="scen-tech-evidence",
        strategy_id=strat.strategy_id,
        scenario_type="baseline",
        scenario_name="Baseline",
        assumptions={},
        funding_structure={},
        metrics={},
    )
    goal = _sample_goal()
    decision = evaluate_decision(
        strategies=[strat],
        scenarios=[scenario],
        architectures=[arch],
        defined_goal=goal,
        technique_outputs=[
            {"technique_id": "tech-bucketing", "status": "calculated"},
            {"technique_id": "tech-laddering", "status": "calculated"},
        ],
    )
    evaluation = decision.evaluations[0]
    assert evaluation.evidence["technique_execution"]["execution_score"] == 2.0
    assert evaluation.total_decision_score > 0
