import pytest
from engines.constraints.evaluator import FinancialRatioConstraintEvaluator
from engines.orchestration.models import GoalEvaluationInput


@pytest.fixture
def evaluator():
    return FinancialRatioConstraintEvaluator()


def test_evaluate_ratios_standard_values(evaluator):
    financial_context = {
        "monthly_income": 100000.0,
        "monthly_expenses": 50000.0,
        "monthly_surplus": 50000.0,
        "liquid_assets": 350000.0,  # 7 months -> healthy
        "monthly_debt_payments": 25000.0,  # 25% -> healthy
        "total_assets": 1000000.0,
        "total_liabilities": 250000.0,  # 25% -> healthy
    }

    ratios = evaluator.evaluate_ratios(financial_context)
    ratio_dict = {r.ratio_key: r for r in ratios}

    assert "savings_ratio" in ratio_dict
    assert ratio_dict["savings_ratio"].value == 50.0
    assert ratio_dict["savings_ratio"].status == "excellent"

    assert "emergency_fund_coverage" in ratio_dict
    assert ratio_dict["emergency_fund_coverage"].value == 7.0
    assert ratio_dict["emergency_fund_coverage"].status == "healthy"

    assert "debt_to_income_ratio" in ratio_dict
    assert ratio_dict["debt_to_income_ratio"].value == 25.0
    assert ratio_dict["debt_to_income_ratio"].status == "healthy"

    assert "leverage_ratio" in ratio_dict
    assert ratio_dict["leverage_ratio"].value == 25.0
    assert ratio_dict["leverage_ratio"].status == "healthy"


def test_critical_emergency_fund_overrides_discretionary_goal(evaluator):
    # Liquid assets cover only 1 month of expenses (< 3 months is critical)
    financial_context = {
        "monthly_income": 80000.0,
        "monthly_expenses": 50000.0,
        "monthly_surplus": 30000.0,
        "liquid_assets": 50000.0,  # 1.0 month -> critical
        "total_assets": 200000.0,
        "total_liabilities": 50000.0,
    }

    goals = [
        GoalEvaluationInput(
            goal_id="g_vacation",
            goal_name="Europe Summer Vacation",
            goal_type="vacation",
            client_priority="critical",  # Client chose critical for luxury vacation
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

    # Hard constraint should be generated for the discretionary goal
    assert len(assessment.hard_constraints) == 1
    hc = assessment.hard_constraints[0]
    assert hc.goal_id == "g_vacation"
    assert hc.suggested_override_priority == "low"
    assert "Emergency fund coverage is critical" in hc.message
    assert "Discretionary allocation constrained" in hc.override_reason

    # Suggested overrides dictionary must be populated
    assert "g_vacation" in assessment.suggested_overrides
    assert assessment.suggested_overrides["g_vacation"]["resolved_priority"] == "low"


def test_critical_debt_to_income_constrains_discretionary_goal(evaluator):
    # Debt payments are 50% of income (> 40% is critical)
    financial_context = {
        "monthly_income": 100000.0,
        "monthly_expenses": 40000.0,
        "monthly_surplus": 10000.0,
        "liquid_assets": 400000.0,  # 10 months -> excellent
        "emi_burden_monthly": 50000.0,  # 50% DTI -> critical
        "total_assets": 1000000.0,
        "total_liabilities": 600000.0,
    }

    goals = [
        GoalEvaluationInput(
            goal_id="g_luxury_car",
            goal_name="Sports Car Purchase",
            goal_type="car",
            client_priority="high",
            required_monthly_contribution=10000.0,
        )
    ]

    assessment = evaluator.assess_constraints(goals, financial_context)

    assert len(assessment.hard_constraints) == 1
    hc = assessment.hard_constraints[0]
    assert hc.rule_id == "RULE_DEBT_BURDEN_EXCEEDED"
    assert hc.suggested_override_priority == "low"
    assert "Debt-to-Income ratio (50.0%) exceeds safe critical ceiling" in hc.message


def test_informational_warning_without_hard_override(evaluator):
    # Emergency fund is 4.5 months (attention range, not critical)
    financial_context = {
        "monthly_income": 80000.0,
        "monthly_expenses": 40000.0,
        "monthly_surplus": 40000.0,
        "liquid_assets": 180000.0,  # 4.5 months -> attention
        "monthly_debt_payments": 10000.0,  # 12.5% -> healthy
        "total_assets": 500000.0,
        "total_liabilities": 50000.0,
    }

    goals = [
        GoalEvaluationInput(
            goal_id="g_travel",
            goal_name="Annual Holiday",
            goal_type="travel",
            client_priority="medium",
            required_monthly_contribution=10000.0,
        )
    ]

    assessment = evaluator.assess_constraints(goals, financial_context)

    # No hard constraints or priority overrides
    assert len(assessment.hard_constraints) == 0
    assert len(assessment.suggested_overrides) == 0

    # Warning exists for attention-level buffer
    assert len(assessment.warnings) >= 1
    assert any("WARN_EMERGENCY_RESERVE_ATTENTION" == w.rule_id for w in assessment.warnings)
