"""
domain/features/strategy_builder/financing.py
Chapter 11 — Self Money + Financing Funding Path (§11.6).

Evaluates evidenced borrowing terms, reducing-balance EMI, borrowing cost, and repayment capacity.
Does not assume financing is available or suitable without evidence.
"""

from decimal import Decimal
from typing import List, Tuple
from app.domain.shared.value_objects import Money, Rate
from app.domain.features.strategy_builder.funding_paths import (
    FinancingPathResult,
    YearlyProjectionRow,
)


def calculate_loan_emi(
    principal: Money,
    annual_interest_rate: Rate,
    tenure_months: int,
) -> Tuple[Money, Money, Money]:
    """
    Standard reducing-balance EMI calculation:
    EMI = P × r × (1 + r)^n ÷ ((1 + r)^n − 1)
    where r = annual_rate / 12 / 100.
    Returns: (monthly_emi, total_repayment, total_interest_cost)
    """
    if tenure_months <= 0 or principal.amount <= Decimal(0):
        zero = Money.zero(currency=principal.currency)
        return zero, zero, zero

    p = float(principal.amount)
    r = float(annual_interest_rate.as_decimal_ratio) / 12.0
    n = tenure_months

    if r <= 0:
        emi_val = p / n
    else:
        compound = (1.0 + r) ** n
        denom = compound - 1.0
        if denom <= 0:
            emi_val = p / n
        else:
            emi_val = (p * r * compound) / denom

    monthly_emi = Money(amount=Decimal(str(emi_val)), currency=principal.currency)
    total_repayment = monthly_emi * n
    total_interest = total_repayment - principal

    if total_interest.is_negative:
        total_interest = Money.zero(currency=principal.currency)

    return monthly_emi, total_repayment, total_interest


def build_financing_path(
    goal_id: str,
    goal_target_amount: Money,
    horizon_years: int,
    start_calendar_year: int,
    own_down_payment: Money,
    loan_annual_interest_rate: Rate,
    loan_tenure_months: int,
    available_monthly_surplus: Money,
    initial_allocated_assets: Money = Money.zero(),
    expected_annual_return: Rate = Rate.from_percentage("0.0"),
) -> FinancingPathResult:
    """
    Self Money + Financing Funding Path evaluation (§11.6).
    Assesses borrowing terms, EMI, repayment capacity, and year-by-year cash flows.
    """
    financing_amount = goal_target_amount - own_down_payment
    if financing_amount.is_negative:
        financing_amount = Money.zero(currency=goal_target_amount.currency)

    monthly_emi, total_repayment, total_interest = calculate_loan_emi(
        principal=financing_amount,
        annual_interest_rate=loan_annual_interest_rate,
        tenure_months=loan_tenure_months,
    )

    emi_affordable = monthly_emi <= available_monthly_surplus

    loan_tenure_years = max(1, (loan_tenure_months + 11) // 12)
    total_projection_years = max(horizon_years, horizon_years + loan_tenure_years)
    projections: List[YearlyProjectionRow] = []
    current_balance = initial_allocated_assets
    annual_emi_outflow = monthly_emi * 12
    years = max(1, horizon_years)

    for year_idx in range(1, total_projection_years + 1):
        cal_year = start_calendar_year + year_idx - 1
        opening = current_balance

        disbursement = financing_amount if year_idx == years else Money.zero(currency=goal_target_amount.currency)
        is_repayment_period = (year_idx > years) and (year_idx <= years + loan_tenure_years)
        repayment = annual_emi_outflow if is_repayment_period else Money.zero(currency=goal_target_amount.currency)
        withdrawal = goal_target_amount if year_idx == years else Money.zero(currency=goal_target_amount.currency)

        growth = Money.zero(currency=goal_target_amount.currency)
        closing = opening + disbursement - repayment - withdrawal if year_idx == years else opening - repayment
        if closing.is_negative:
            closing = Money.zero(currency=goal_target_amount.currency)

        current_balance = closing

        projections.append(
            YearlyProjectionRow(
                year_index=year_idx,
                calendar_year=cal_year,
                opening_balance=opening,
                annual_contributions=Money.zero(currency=goal_target_amount.currency),
                investment_growth=growth,
                financing_disbursement=disbursement,
                annual_debt_repayment=repayment,
                goal_withdrawal=withdrawal,
                closing_balance=closing,
            )
        )

    total_own_outflow = own_down_payment + total_repayment

    affordability_msg = (
        f"Monthly EMI of {monthly_emi.amount} is within surplus ({available_monthly_surplus.amount})."
        if emi_affordable
        else f"Monthly EMI of {monthly_emi.amount} exceeds surplus ({available_monthly_surplus.amount}) by {monthly_emi.amount - available_monthly_surplus.amount}."
    )

    explanation = (
        f"Self Money + Financing requires {own_down_payment.amount} upfront down payment and borrows "
        f"{financing_amount.amount} at {loan_annual_interest_rate.percentage:.2f}% p.a. over {loan_tenure_months} months. "
        f"Total borrowing interest cost: {total_interest.amount}. {affordability_msg}"
    )

    return FinancingPathResult(
        goal_id=goal_id,
        own_down_payment=own_down_payment,
        total_own_contributions=own_down_payment,
        total_own_money_outflow=total_own_outflow,
        financing_amount=financing_amount,
        loan_interest_rate=loan_annual_interest_rate,
        loan_tenure_months=loan_tenure_months,
        monthly_emi=monthly_emi,
        total_interest_cost=total_interest,
        total_repayment_amount=total_repayment,
        emi_affordable_within_surplus=emi_affordable,
        projected_corpus_at_goal_date=goal_target_amount,
        goal_target_amount=goal_target_amount,
        goal_amount_funded=goal_target_amount if (own_down_payment + financing_amount >= goal_target_amount) else (own_down_payment + financing_amount),
        remaining_corpus_after_goal=Money.zero(currency=goal_target_amount.currency),
        yearly_projections=projections,
        is_fully_funded=(own_down_payment + financing_amount >= goal_target_amount),
        explanation=explanation,
    )
