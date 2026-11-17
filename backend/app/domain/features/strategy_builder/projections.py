"""
domain/features/strategy_builder/projections.py
Chapter 11 — Strategy Builder Step 4: Goal Funding Projection (§11.4, §11.5).

Projects year-by-year funding, compounding growth, and payouts for the Self Money path.
Fallback order (§11.5):
1. SIP / Contribution
2. Investment Growth
3. Goal Withdrawal
"""

from decimal import Decimal
from typing import List
from app.domain.shared.value_objects import Money, Rate
from app.domain.features.strategy_builder.funding_paths import (
    YearlyProjectionRow,
    SelfMoneyPathResult,
)


def build_self_money_path(
    goal_id: str,
    goal_target_amount: Money,
    horizon_years: int,
    start_calendar_year: int,
    initial_allocated_assets: Money,
    required_monthly_sip: Money,
    expected_annual_return: Rate,
) -> SelfMoneyPathResult:
    """
    Step 4: Goal Funding Projection for Self Money (§11.4).
    Projects year-by-year funding, compounding growth, and goal withdrawal.
    """
    projections: List[YearlyProjectionRow] = []
    current_balance = initial_allocated_assets
    annual_sip_amount = required_monthly_sip * 12
    r = float(expected_annual_return.as_decimal_ratio)
    years = max(1, horizon_years)

    for year_idx in range(1, years + 1):
        cal_year = start_calendar_year + year_idx - 1
        opening = current_balance

        # 1. Contributions during the year
        contributions = annual_sip_amount

        # 2. Investment Growth: opening compounds for full year, contributions compound on average mid-year
        growth_amount = (opening.amount * Decimal(str(r))) + (contributions.amount * Decimal(str(r / 2.0)))
        growth = Money(amount=growth_amount, currency=goal_target_amount.currency)

        balance_before_payout = opening + contributions + growth

        # 3. Withdrawal in target year
        if year_idx == years:
            withdrawal = goal_target_amount if balance_before_payout >= goal_target_amount else balance_before_payout
        else:
            withdrawal = Money.zero(currency=goal_target_amount.currency)

        closing = balance_before_payout - withdrawal
        current_balance = closing

        projections.append(
            YearlyProjectionRow(
                year_index=year_idx,
                calendar_year=cal_year,
                opening_balance=opening,
                annual_contributions=contributions,
                investment_growth=growth,
                financing_disbursement=Money.zero(currency=goal_target_amount.currency),
                annual_debt_repayment=Money.zero(currency=goal_target_amount.currency),
                goal_withdrawal=withdrawal,
                closing_balance=closing,
            )
        )

    target_year_row = projections[-1]
    funded_amount = target_year_row.goal_withdrawal
    corpus_at_goal = target_year_row.opening_balance + target_year_row.annual_contributions + target_year_row.investment_growth
    remaining_corpus = target_year_row.closing_balance

    total_contributions = initial_allocated_assets + (annual_sip_amount * years)
    is_fully_funded = funded_amount >= goal_target_amount

    explanation = (
        f"Self Money path accumulates {corpus_at_goal.amount} by year {target_year_row.calendar_year} "
        f"through {total_contributions.amount} in own contributions and disciplined investment compounding. "
        f"Post-goal remaining wealth: {remaining_corpus.amount}."
    )

    return SelfMoneyPathResult(
        goal_id=goal_id,
        total_own_money_contributed=total_contributions,
        projected_corpus_at_goal_date=corpus_at_goal,
        goal_target_amount=goal_target_amount,
        goal_amount_funded=funded_amount,
        remaining_corpus_after_goal=remaining_corpus,
        yearly_projections=projections,
        is_fully_funded=is_fully_funded,
        explanation=explanation,
    )
