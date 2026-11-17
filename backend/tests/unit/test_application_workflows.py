"""
Unit tests for Application Layer Workflows.
- Chapter 07 Investor Situation Assessment
- Chapter 08 Budgeting, Cash Flow & Affordability
- Planning Lifecycle (Goal Planner -> Strategy Builder handoff)
- Report Preparation
"""

from datetime import date
from decimal import Decimal
from app.domain.canonical.goal_taxonomy import CanonicalGoalId
from app.domain.canonical.financial_categories import (
    CanonicalIncomeCategoryId,
    CanonicalExpenseCategoryId,
    CanonicalAssetCategoryId,
    CanonicalLiabilityCategoryId,
)
from app.domain.shared.value_objects import (
    Money,
    Rate,
    CalendarMonth,
    FlowFrequency,
)
from app.domain.features.investor_profile.financial_state import (
    IncomeRecord,
    ExpenseRecord,
    AssetRecord,
    LiabilityRecord,
    FinancialStateSnapshot,
)
from app.domain.features.investor_profile.risk_profile import (
    RiskProfile,
    RiskCapacityBand,
    RiskToleranceBand,
)
from app.domain.features.goal_planner import GoalInstance
from app.application.workflows import (
    execute_investor_situation_assessment,
    execute_budgeting_cash_flow_affordability,
    execute_planning_lifecycle,
    prepare_individual_goal_report,
    FinancingOptionsInput,
)


def _build_sample_snapshot() -> tuple[FinancialStateSnapshot, CalendarMonth]:
    nov_2026 = CalendarMonth(year=2026, month=11)
    as_of = date(2026, 11, 16)

    incomes = [
        IncomeRecord(
            id="inc-1",
            category=CanonicalIncomeCategoryId.SALARY,
            amount=Money.from_amount("150000.00"),
            is_net=True,
            frequency=FlowFrequency.MONTHLY,
            period=nov_2026,
        )
    ]
    expenses = [
        ExpenseRecord(
            id="exp-1",
            category=CanonicalExpenseCategoryId.HOUSING,
            amount=Money.from_amount("40000.00"),
            period=nov_2026,
        ),
        ExpenseRecord(
            id="exp-2",
            category=CanonicalExpenseCategoryId.FOOD_GROCERIES,
            amount=Money.from_amount("25000.00"),
            period=nov_2026,
        ),
    ]
    assets = [
        AssetRecord(
            id="ast-1",
            name="Bank Savings",
            category=CanonicalAssetCategoryId.BANK_CASH,
            value=Money.from_amount("500000.00"),
            as_of_date=as_of,
        ),
        AssetRecord(
            id="ast-2",
            name="Equity Mutual Funds",
            category=CanonicalAssetCategoryId.MUTUAL_FUNDS,
            value=Money.from_amount("1000000.00"),
            as_of_date=as_of,
            expected_annual_return=Rate.from_percentage("12.0"),
        ),
    ]
    liabilities = [
        LiabilityRecord(
            id="liab-1",
            name="Car Loan",
            category=CanonicalLiabilityCategoryId.CAR_LOAN,
            outstanding_balance=Money.from_amount("300000.00"),
            annual_interest_rate=Rate.from_percentage("9.5"),
            monthly_payment=Money.from_amount("12000.00"),
            as_of_date=as_of,
            remaining_tenure_months=28,
        )
    ]

    snapshot = FinancialStateSnapshot(
        investor_id="inv-workflow-1",
        as_of_date=as_of,
        incomes=incomes,
        expenses=expenses,
        assets=assets,
        liabilities=liabilities,
    )
    return snapshot, nov_2026


def test_investor_situation_assessment_workflow():
    snapshot, period = _build_sample_snapshot()
    risk = RiskProfile(
        investor_id="inv-workflow-1",
        risk_capacity=RiskCapacityBand.ADEQUATE,
        risk_tolerance=RiskToleranceBand.HIGH,
        stated_time_horizon_years=10,
    )

    result = execute_investor_situation_assessment(
        snapshot=snapshot,
        period=period,
        risk_profile=risk,
    )

    assert result.investor_id == "inv-workflow-1"
    assert result.readiness.is_ready_for_goal_feasibility is True
    assert result.moneywheel.measurements.net_worth.amount == Decimal("1200000.00")
    assert result.risk_assessment.reconciled_risk_posture == "growth_oriented"
    assert "Situation assessment evaluated" in result.executive_summary


def test_budgeting_cash_flow_affordability_workflow():
    snapshot, period = _build_sample_snapshot()

    bundle = execute_budgeting_cash_flow_affordability(snapshot, period)

    assert bundle.investor_id == "inv-workflow-1"
    # Income 1,50,000 - Expenses (40,000 + 25,000) = 85,000 surplus
    assert bundle.available_monthly_surplus.amount == Decimal("85000.00")
    assert bundle.is_cash_flow_positive is True
    assert bundle.dti_evaluation.is_satisfied is True
    assert len(bundle.high_interest_debt_evaluations) == 1
    # 9.5% p.a. <= 14% -> SATISFIED
    assert bundle.high_interest_debt_evaluations[0].is_satisfied is True


def test_planning_lifecycle_and_report_preparation_workflow():
    as_of = date(2026, 11, 16)
    target_date = date(2031, 11, 16)  # 5 years

    goal = GoalInstance(
        id="goal-child-higher-edu",
        investor_id="inv-workflow-1",
        canonical_id=CanonicalGoalId.EDUCATION,
        name="Child Higher Education",
        target_date=target_date,
        current_cost=Money.from_amount("1500000.00"),  # 15 Lakhs
        applicable_inflation_rate=Rate.from_percentage("8.0"),
        expected_annual_return=Rate.from_percentage("12.0"),
        created_at=as_of,
    )

    available_surplus = Money.from_amount("85000.00")

    lifecycle_res = execute_planning_lifecycle(
        goal=goal,
        available_monthly_surplus=available_surplus,
        current_calendar_year=2026,
        financing_input=FinancingOptionsInput(
            down_payment=Money.from_amount("500000.00"),
            loan_annual_interest_rate=Rate.from_percentage("10.0"),
            loan_tenure_months=60,
        ),
    )

    # 1. Goal Requirement output
    assert lifecycle_res.goal_requirement.future_goal_target.amount > Decimal("2000000.00")

    # 2. Feasibility
    assert lifecycle_res.feasibility.is_feasible_under_current_conditions is True
    assert lifecycle_res.feasibility.required_monthly_sip < available_surplus

    # 3. Strategy Builder Self Money & Financing
    assert lifecycle_res.self_money_path.is_fully_funded is True
    assert lifecycle_res.financing_path is not None
    assert lifecycle_res.comparison_matrix is not None
    assert "Trade-off Decision" in lifecycle_res.comparison_matrix.investor_decision_prompt

    # 4. Report Preparation Workflow
    report = prepare_individual_goal_report(
        investor_id="inv-workflow-1",
        planning_result=lifecycle_res,
        as_of_date=as_of,
    )

    assert report.investor_id == "inv-workflow-1"
    assert report.goal_requirement == lifecycle_res.goal_requirement
    assert report.self_money_path == lifecycle_res.self_money_path
    assert report.comparison_matrix == lifecycle_res.comparison_matrix
