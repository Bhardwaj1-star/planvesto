import pytest
from engines.orchestration.engine import MultiGoalOrchestrator
from engines.orchestration.models import GoalEvaluationInput


@pytest.fixture
def orchestrator():
    return MultiGoalOrchestrator()


def test_one_goal_within_surplus(orchestrator):
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
    assert result.monthly_gap == -35000.0
    assert len(result.goals) == 1
    assert result.goals[0].funding_status == "fully_funded"
    assert result.goals[0].allocated_monthly_contribution == 15000.0
    assert result.goals[0].override_applied is False
    assert result.competing_resources_detected is False


def test_multiple_independent_goals_within_surplus(orchestrator):
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
    assert result.competing_resources_detected is False
    assert all(g.funding_status == "fully_funded" for g in result.goals)


def test_competing_goals_sharing_limited_surplus(orchestrator):
    goals = [
        GoalEvaluationInput(
            goal_id="g1",
            goal_name="Child Education",
            goal_type="child education",
            client_priority="high",
            target_date="2035-05",
            required_monthly_contribution=30000.0,
        ),
        GoalEvaluationInput(
            goal_id="g2",
            goal_name="Vacation Home",
            goal_type="home",
            client_priority="medium",
            target_date="2038-10",
            required_monthly_contribution=25000.0,
        ),
    ]
    financial_state = {"monthly_surplus": 40000.0}

    result = orchestrator.orchestrate(goals, financial_state)

    assert result.competing_resources_detected is True
    assert result.overall_funding_status == "surplus_shortfall"
    assert result.monthly_gap == 15000.0  # 55000 - 40000

    # Higher priority (Child Education) should be fully funded first
    assert result.goals[0].goal_id == "g1"
    assert result.goals[0].allocated_monthly_contribution == 30000.0
    assert result.goals[0].funding_status == "fully_funded"

    # Lower priority (Vacation Home) should get remainder (10,000)
    assert result.goals[1].goal_id == "g2"
    assert result.goals[1].allocated_monthly_contribution == 10000.0
    assert result.goals[1].shortfall == 15000.0
    assert result.goals[1].funding_status == "partially_funded"
    assert result.goals[1].feasibility_status == "constrained"
    assert len(result.trade_offs) >= 1


def test_client_priority_preserved_when_no_conflict(orchestrator):
    goals = [
        GoalEvaluationInput(
            goal_id="g1",
            goal_name="Dream Car",
            goal_type="vehicle",
            client_priority="low",
            target_date="2028-01",
            required_monthly_contribution=10000.0,
        ),
        GoalEvaluationInput(
            goal_id="g2",
            goal_name="Retirement",
            goal_type="retirement",
            client_priority="critical",
            target_date="2040-01",
            required_monthly_contribution=20000.0,
        ),
    ]
    financial_state = {"monthly_surplus": 35000.0}

    result = orchestrator.orchestrate(goals, financial_state)

    # First in list should be critical priority goal
    assert result.goals[0].goal_id == "g2"
    assert result.goals[0].client_priority == "critical"
    assert result.goals[0].resolved_priority == "critical"
    assert result.goals[0].override_applied is False

    assert result.goals[1].goal_id == "g1"
    assert result.goals[1].client_priority == "low"
    assert result.goals[1].resolved_priority == "low"
    assert result.goals[1].override_applied is False


def test_rule_driven_allocation_override_and_traceability(orchestrator):
    goals = [
        GoalEvaluationInput(
            goal_id="luxury_trip",
            goal_name="Luxury World Tour",
            goal_type="travel",
            client_priority="critical",
            target_date="2026-12",
            required_monthly_contribution=25000.0,
        ),
        GoalEvaluationInput(
            goal_id="retirement",
            goal_name="Retirement Corpus",
            goal_type="retirement",
            client_priority="medium",
            target_date="2045-01",
            required_monthly_contribution=20000.0,
        ),
    ]
    financial_state = {"monthly_surplus": 30000.0}

    # Simulate an approved system rule override: retirement must precede luxury travel
    rule_overrides = {
        "luxury_trip": {
            "resolved_priority": "low",
            "reason": "Discretionary luxury goal deprioritized due to insufficient retirement coverage.",
        }
    }

    result = orchestrator.orchestrate(goals, financial_state, rule_overrides=rule_overrides)

    # Retirement (medium) should now be evaluated before luxury trip (demoted to low)
    assert result.goals[0].goal_id == "retirement"
    assert result.goals[0].allocated_monthly_contribution == 20000.0
    assert result.goals[0].funding_status == "fully_funded"

    # Luxury trip has override recorded
    luxury_res = result.goals[1]
    assert luxury_res.goal_id == "luxury_trip"
    assert luxury_res.client_priority == "critical"  # Preserved!
    assert luxury_res.resolved_priority == "low"      # System resolved!
    assert luxury_res.override_applied is True
    assert "Discretionary luxury goal deprioritized" in luxury_res.override_reason
    assert luxury_res.allocated_monthly_contribution == 10000.0
    assert luxury_res.funding_status == "partially_funded"

    # Check audit trail traceability
    audit_item = next(a for a in result.audit_trail if a["goal_id"] == "luxury_trip")
    assert audit_item["client_priority"] == "critical"
    assert audit_item["resolved_priority"] == "low"
    assert audit_item["override_applied"] is True


def test_insufficient_resources_and_infeasible_goal(orchestrator):
    goals = [
        GoalEvaluationInput(
            goal_id="g1",
            goal_name="Home Purchase",
            goal_type="home purchase",
            client_priority="high",
            target_date="2030-01",
            required_monthly_contribution=30000.0,
        ),
        GoalEvaluationInput(
            goal_id="g2",
            goal_name="New Car",
            goal_type="vehicle",
            client_priority="low",
            target_date="2031-01",
            required_monthly_contribution=15000.0,
        ),
    ]
    financial_state = {"monthly_surplus": 20000.0}

    result = orchestrator.orchestrate(goals, financial_state)

    assert result.overall_funding_status == "surplus_shortfall"
    assert result.total_required_contribution == 45000.0
    assert result.total_allocated_contribution == 20000.0

    # g1 partially funded
    assert result.goals[0].goal_id == "g1"
    assert result.goals[0].allocated_monthly_contribution == 20000.0
    assert result.goals[0].funding_status == "partially_funded"

    # g2 completely unfunded and infeasible from monthly surplus
    assert result.goals[1].goal_id == "g2"
    assert result.goals[1].allocated_monthly_contribution == 0.0
    assert result.goals[1].shortfall == 15000.0
    assert result.goals[1].funding_status == "unfunded"
    assert result.goals[1].feasibility_status == "infeasible"


def test_custom_strategy_evaluator_integration(orchestrator):
    def dummy_strategy_evaluator(goal_input, context):
        return {
            "recommended_strategy_id": "growth_equity",
            "recommended_strategy_name": "Aggressive Growth Strategy",
            "required_monthly_contribution": 12000.0,
            "feasibility_status": "feasible",
            "reasons": ["Long-term compounder"],
        }

    goals = [
        GoalEvaluationInput(
            goal_id="g1",
            goal_name="Retirement Corpus",
            goal_type="retirement",
            client_priority="high",
            required_monthly_contribution=0.0,  # Will be provided by evaluator
        )
    ]
    financial_state = {"monthly_surplus": 25000.0}

    result = orchestrator.orchestrate(goals, financial_state, strategy_evaluator=dummy_strategy_evaluator)

    assert result.goals[0].recommended_strategy_id == "growth_equity"
    assert result.goals[0].recommended_strategy_name == "Aggressive Growth Strategy"
    assert result.goals[0].required_monthly_contribution == 12000.0
    assert result.goals[0].allocated_monthly_contribution == 12000.0
    assert result.goals[0].funding_status == "fully_funded"
