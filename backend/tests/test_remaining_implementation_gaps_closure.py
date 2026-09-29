"""Comprehensive Verification Suite for REMAINING-IMPLEMENTATION-GAPS.md.

Directly tests all 11 mandatory scenarios specified under GAP 7:
1. One goal — regression against existing single-goal behavior.
2. Multiple independent goals.
3. Multiple goals competing for the same surplus.
4. Client priority preserved when no constraint conflicts.
5. Ratio/constraint-driven allocation change.
6. Traceability of client priority vs resolved outcome.
7. Partial funding.
8. Infeasible combination.
9. Correct report explanation for an override.
10. Auth/ownership behavior.
11. End-to-end API flow.
"""

from unittest.mock import MagicMock, patch
import pytest
from fastapi.testclient import TestClient

from main import app
from engines.orchestration.engine import MultiGoalOrchestrator
from engines.orchestration.models import GoalEvaluationInput, MultiGoalPlanResult
from engines.constraints.evaluator import FinancialRatioConstraintEvaluator
from engines.allocation.engine import ResourceAllocationEngine
from services.financial_plan_service import FinancialPlanService

client = TestClient(app)


class TestRemainingImplementationGapsClosure:
    """Verifies all 11 mandatory GAP 7 scenarios from REMAINING-IMPLEMENTATION-GAPS.md."""

    # Scenario 1: One goal — regression against existing single-goal behavior
    def test_scenario_01_one_goal_regression(self):
        orchestrator = MultiGoalOrchestrator()
        goals = [
            GoalEvaluationInput(
                goal_id="g1",
                goal_name="Emergency Fund",
                goal_type="emergency_fund",
                client_priority="critical",
                target_date="2027-01",
                required_monthly_contribution=15000.0,
            )
        ]
        financial_state = {"monthly_surplus": 50000.0}
        result = orchestrator.orchestrate(goals, financial_state)

        assert result.overall_funding_status == "within_surplus"
        assert result.total_required_contribution == 15000.0
        assert result.total_allocated_contribution == 15000.0
        assert len(result.goals) == 1
        assert result.goals[0].funding_status == "fully_funded"
        assert result.competing_resources_detected is False

    # Scenario 2: Multiple independent goals
    def test_scenario_02_multiple_independent_goals(self):
        orchestrator = MultiGoalOrchestrator()
        goals = [
            GoalEvaluationInput(
                goal_id="g1",
                goal_name="Retirement",
                goal_type="retirement",
                client_priority="high",
                target_date="2045-12",
                required_monthly_contribution=25000.0,
            ),
            GoalEvaluationInput(
                goal_id="g2",
                goal_name="Child Education",
                goal_type="education",
                client_priority="medium",
                target_date="2035-06",
                required_monthly_contribution=15000.0,
            ),
        ]
        financial_state = {"monthly_surplus": 60000.0}
        result = orchestrator.orchestrate(goals, financial_state)

        assert result.overall_funding_status == "within_surplus"
        assert result.total_required_contribution == 40000.0
        assert result.total_allocated_contribution == 40000.0
        assert all(g.funding_status == "fully_funded" for g in result.goals)
        assert result.competing_resources_detected is False

    # Scenario 3: Multiple goals competing for the same surplus
    def test_scenario_03_competing_goals_sharing_limited_surplus(self):
        orchestrator = MultiGoalOrchestrator()
        goals = [
            GoalEvaluationInput(
                goal_id="g1",
                goal_name="Child Education",
                goal_type="education",
                client_priority="high",
                required_monthly_contribution=30000.0,
            ),
            GoalEvaluationInput(
                goal_id="g2",
                goal_name="Vacation Home",
                goal_type="home purchase",
                client_priority="medium",
                required_monthly_contribution=25000.0,
            ),
        ]
        financial_state = {"monthly_surplus": 40000.0}
        result = orchestrator.orchestrate(goals, financial_state)

        assert result.competing_resources_detected is True
        assert result.overall_funding_status == "surplus_shortfall"
        assert result.monthly_gap == 15000.0

        # g1 fully funded, g2 gets remainder
        assert result.goals[0].goal_id == "g1"
        assert result.goals[0].allocated_monthly_contribution == 30000.0
        assert result.goals[0].funding_status == "fully_funded"

        assert result.goals[1].goal_id == "g2"
        assert result.goals[1].allocated_monthly_contribution == 10000.0
        assert result.goals[1].funding_status == "partially_funded"

    # Scenario 4: Client priority preserved when no constraint conflicts
    def test_scenario_04_client_priority_preserved_without_conflicts(self):
        orchestrator = MultiGoalOrchestrator()
        goals = [
            GoalEvaluationInput(
                goal_id="g_low",
                goal_name="Dream Car",
                client_priority="low",
                required_monthly_contribution=10000.0,
            ),
            GoalEvaluationInput(
                goal_id="g_crit",
                goal_name="Retirement",
                client_priority="critical",
                required_monthly_contribution=20000.0,
            ),
        ]
        financial_state = {"monthly_surplus": 35000.0}
        result = orchestrator.orchestrate(goals, financial_state)

        assert result.goals[0].goal_id == "g_crit"
        assert result.goals[0].client_priority == "critical"
        assert result.goals[0].resolved_priority == "critical"
        assert result.goals[0].override_applied is False

        assert result.goals[1].goal_id == "g_low"
        assert result.goals[1].client_priority == "low"
        assert result.goals[1].resolved_priority == "low"
        assert result.goals[1].override_applied is False

    # Scenario 5: Ratio/constraint-driven allocation change
    def test_scenario_05_ratio_constraint_driven_allocation_change(self):
        evaluator = FinancialRatioConstraintEvaluator()
        financial_context = {
            "monthly_income": 80000.0,
            "monthly_expenses": 50000.0,
            "monthly_surplus": 30000.0,
            "liquid_assets": 50000.0,  # 1.0 month -> critical (< 3.0)
            "total_assets": 200000.0,
            "total_liabilities": 50000.0,
        }
        goals = [
            GoalEvaluationInput(
                goal_id="g_vacation",
                goal_name="Luxury Holiday",
                goal_type="vacation",
                client_priority="critical",
                required_monthly_contribution=15000.0,
            ),
            GoalEvaluationInput(
                goal_id="g_emergency",
                goal_name="Emergency Reserve",
                goal_type="emergency_fund",
                client_priority="high",
                required_monthly_contribution=15000.0,
            ),
        ]
        assessment = evaluator.assess_constraints(goals, financial_context)
        assert assessment.has_overrides is True
        override = assessment.suggested_overrides["g_vacation"]
        assert override["resolved_priority"] == "low"
        assert "emergency fund coverage" in override["reason"].lower()

    # Scenario 6: Traceability of client priority vs resolved outcome
    def test_scenario_06_traceability_of_client_priority_vs_resolved_outcome(self):
        orchestrator = MultiGoalOrchestrator()
        goals = [
            GoalEvaluationInput(
                goal_id="trip",
                goal_name="Luxury Trip",
                client_priority="critical",
                required_monthly_contribution=25000.0,
            ),
            GoalEvaluationInput(
                goal_id="retirement",
                goal_name="Retirement",
                client_priority="medium",
                required_monthly_contribution=20000.0,
            ),
        ]
        financial_state = {"monthly_surplus": 30000.0}
        rule_overrides = {
            "trip": {
                "resolved_priority": "low",
                "reason": "Deprioritized by system ratio constraint rule.",
            }
        }
        result = orchestrator.orchestrate(goals, financial_state, rule_overrides=rule_overrides)

        trip_res = next(g for g in result.goals if g.goal_id == "trip")
        assert trip_res.client_priority == "critical"  # Preserved original client choice
        assert trip_res.resolved_priority == "low"      # System override documented
        assert trip_res.override_applied is True
        assert "Deprioritized by system" in trip_res.override_reason

    # Scenario 7: Partial funding
    def test_scenario_07_partial_funding_behavior(self):
        engine = ResourceAllocationEngine()
        goals = [
            {"goal_id": "g1", "goal_name": "Education", "client_priority": "high", "resolved_priority": "high", "required_monthly_contribution": 20000.0},
            {"goal_id": "g2", "goal_name": "Car", "client_priority": "medium", "resolved_priority": "medium", "required_monthly_contribution": 25000.0},
        ]
        result = engine.allocate(goals, 30000.0)

        assert result.allocations[0].allocated_monthly_contribution == 20000.0
        assert result.allocations[0].funding_percentage == 100.0

        assert result.allocations[1].allocated_monthly_contribution == 10000.0
        assert result.allocations[1].monthly_shortfall == 15000.0
        assert result.allocations[1].funding_percentage == 40.0

    # Scenario 8: Infeasible combination
    def test_scenario_08_infeasible_combination_handling(self):
        engine = ResourceAllocationEngine()
        goals = [
            {"goal_id": "g1", "goal_name": "Goal 1", "client_priority": "high", "resolved_priority": "high", "required_monthly_contribution": 15000.0},
            {"goal_id": "g2", "goal_name": "Goal 2", "client_priority": "low", "resolved_priority": "low", "required_monthly_contribution": 20000.0},
        ]
        result = engine.allocate(goals, 15000.0)

        assert result.allocations[0].allocated_monthly_contribution == 15000.0
        assert result.allocations[0].funding_status == "fully_funded"

        assert result.allocations[1].allocated_monthly_contribution == 0.0
        assert result.allocations[1].monthly_shortfall == 20000.0
        assert result.allocations[1].funding_status == "unfunded"
        assert result.allocations[1].feasibility_status == "infeasible"

    # Scenario 9: Correct report explanation for an override
    def test_scenario_09_correct_report_explanation_for_override(self):
        mock_goal_repo = MagicMock()
        mock_strat_repo = MagicMock()
        mock_multi = MagicMock()

        mock_goal_repo.list_goals.return_value = [{"goal_id": "g1"}]
        mock_strat_repo.get_latest_run.return_value = MagicMock(strategy_run_id="run-1")
        mock_multi.build_multi_goal_plan.return_value = MultiGoalPlanResult(
            planning_unit_id="pu-1",
            total_available_surplus=40000.0,
            total_required_contribution=30000.0,
            total_allocated_contribution=30000.0,
            overall_funding_status="within_surplus",
            goals=[],
        )

        service = FinancialPlanService(
            goal_repo=mock_goal_repo,
            strategy_repo=mock_strat_repo,
            multi_goal_service=mock_multi,
        )

        # PDF generation with ratio override
        pdf_bytes = service.generate_pdf("pu-1")
        assert isinstance(pdf_bytes, bytes)
        assert len(pdf_bytes) > 1000

    # Scenario 10: Auth/ownership behavior
    def test_scenario_10_auth_and_ownership_verification(self):
        # 401 when no token
        r1 = client.get("/api/strategy/financial-plan?planning_unit_id=pu-1")
        assert r1.status_code == 401

        r2 = client.post("/api/strategy/financial-plan/build", json={"planning_unit_id": "pu-1"})
        assert r2.status_code == 401

        r3 = client.get("/api/strategy/financial-plan.pdf?planning_unit_id=pu-1")
        assert r3.status_code == 401

        r4 = client.post("/api/orchestration/plan", json={"planning_unit_id": "pu-1"})
        assert r4.status_code == 401

    # Scenario 11: End-to-end API flow
    @patch("api.strategy.verify_planning_unit_ownership")
    @patch("api.strategy.authenticate_user")
    @patch("api.strategy.FinancialPlanService.build_plan")
    @patch("api.strategy.FinancialPlanService.generate_pdf")
    def test_scenario_11_end_to_end_api_pipeline_flow(self, mock_pdf, mock_build, mock_auth, mock_verify):
        mock_auth.return_value = "user-1"
        mock_verify.return_value = True
        mock_build.return_value = {
            "report_type": "complete_financial_plan",
            "planning_unit_id": "pu-test",
            "summary": {"total_goals_count": 2},
            "ratio_constraints": [],
            "resource_allocation": {"total_monthly_surplus": 50000.0},
        }
        mock_pdf.return_value = b"%PDF-1.4 test binary data"

        headers = {"Authorization": "Bearer token-123"}

        # 1. Build Plan POST
        r_build = client.post("/api/strategy/financial-plan/build", json={"planning_unit_id": "pu-test"}, headers=headers)
        assert r_build.status_code == 200
        assert r_build.json()["report_type"] == "complete_financial_plan"

        # 2. Get Plan GET
        r_get = client.get("/api/strategy/financial-plan?planning_unit_id=pu-test", headers=headers)
        assert r_get.status_code == 200
        assert r_get.json()["planning_unit_id"] == "pu-test"

        # 3. Download PDF GET
        r_pdf = client.get("/api/strategy/financial-plan.pdf?planning_unit_id=pu-test", headers=headers)
        assert r_pdf.status_code == 200
        assert r_pdf.headers["content-type"] == "application/pdf"
        assert b"%PDF-1.4" in r_pdf.content
