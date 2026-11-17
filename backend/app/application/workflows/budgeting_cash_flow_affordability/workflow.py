"""
application/workflows/budgeting_cash_flow_affordability/workflow.py
Chapter 08 — Budgeting, Cash-Flow and Affordability Workflow.

Coordinates the verification of period-matched income, expense, and savings evidence:
1. Validates period-matching between flows.
2. Computes canonical Available Monthly Surplus (Chapter 05).
3. Evaluates DTI gate (CTR-DTI-001) for cash-flow context.
4. Identifies high-interest liabilities (CTR-HIR-001) impacting surplus.
5. Produces validated cash-flow bundle to pass to Goal Planner & Strategy Builder.

Non-negotiable invariants:
- Consumes Chapter 05 canonical surplus calculation; never invents a separate formula.
- DTI is informational only and never blocks.
"""

from dataclasses import dataclass
from datetime import date
from typing import List, Optional

from app.domain.shared.value_objects import Money, Rate, CalendarMonth
from app.domain.shared.calculations.debt_ratios import calculate_debt_to_income_ratio
from app.domain.shared.constraints import (
    ConstraintEvaluationResult,
    evaluate_dti_gate,
    evaluate_high_interest_liability_gate,
)
from app.domain.features.investor_profile.financial_state import FinancialStateSnapshot


@dataclass(frozen=True)
class CashFlowAffordabilityBundle:
    """Verified cash flow and affordability context for downstream planning."""
    investor_id: str
    period: CalendarMonth
    net_monthly_income: Money
    monthly_expenses: Money
    monthly_savings: Money
    available_monthly_surplus: Money
    debt_payments_total: Money
    dti_evaluation: ConstraintEvaluationResult
    high_interest_debt_evaluations: List[ConstraintEvaluationResult]
    is_cash_flow_positive: bool
    summary_notes: str


def execute_budgeting_cash_flow_affordability(
    snapshot: FinancialStateSnapshot,
    period: CalendarMonth,
) -> CashFlowAffordabilityBundle:
    """
    Coordinates the Chapter 08 cash flow & affordability verification.
    """
    net_income = snapshot.get_actual_net_monthly_income(period)
    expenses = snapshot.get_actual_monthly_expenses(period)
    savings = snapshot.get_actual_monthly_savings_investments()
    surplus = snapshot.calculate_available_monthly_surplus(period)

    # Debt payments
    debt_payments = sum((l.monthly_payment.amount for l in snapshot.liabilities), Money.zero().amount)
    total_debt_payments = Money(amount=debt_payments)

    # Evaluate DTI
    dti_rate = calculate_debt_to_income_ratio(total_debt_payments, net_income)
    dti_eval = evaluate_dti_gate(dti_rate)

    # Evaluate High Interest Debts
    hir_evals: List[ConstraintEvaluationResult] = []
    for liab in snapshot.liabilities:
        hir_eval = evaluate_high_interest_liability_gate(
            liability_id=liab.id,
            liability_name=liab.name,
            outstanding_balance=liab.outstanding_balance,
            annual_interest_rate=liab.annual_interest_rate,
        )
        hir_evals.append(hir_eval)

    is_positive = surplus.is_positive or surplus.is_zero

    summary = (
        f"Period {period.year}-{period.month:02d}: Net Income {net_income.amount}, "
        f"Expenses {expenses.amount}, Surplus {surplus.amount}. "
        f"Cash flow is {'positive' if is_positive else 'in deficit'}."
    )

    return CashFlowAffordabilityBundle(
        investor_id=snapshot.investor_id,
        period=period,
        net_monthly_income=net_income,
        monthly_expenses=expenses,
        monthly_savings=savings,
        available_monthly_surplus=surplus,
        debt_payments_total=total_debt_payments,
        dti_evaluation=dti_eval,
        high_interest_debt_evaluations=hir_evals,
        is_cash_flow_positive=is_positive,
        summary_notes=summary,
    )
