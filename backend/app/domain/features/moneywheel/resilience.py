"""
domain/features/moneywheel/resilience.py
Chapter 09 — Financial Health Assessment & Resilience Diagnostics (§2, §3).

Evaluates the 5 resilience dimensions without inventing arbitrary scores or pass/fail flags:
1. Access to Money
2. Cash-flow Continuity
3. Debt Pressure
4. Protection Gaps
5. Concentration & Dependency
"""

from decimal import Decimal
from typing import List

from app.domain.shared.value_objects import CalendarMonth
from app.domain.features.investor_profile.financial_state.models import FinancialStateSnapshot
from app.domain.features.moneywheel.findings import (
    ResilienceDimension,
    AssessmentFinding,
)
from app.domain.features.moneywheel.assessment import (
    MoneywheelAssessmentResult,
    compute_moneywheel_measurements,
)
from app.domain.features.moneywheel.explanation import (
    explain_liquidity_status,
    explain_cash_flow_status,
)


def assess_financial_health(
    snapshot: FinancialStateSnapshot,
    period: CalendarMonth,
) -> MoneywheelAssessmentResult:
    """
    Sub-feature 2: Financial Health Assessment (§2, §3).
    Produces explainable resilience diagnostics across the 5 dimensions without invented scores.
    """
    m = compute_moneywheel_measurements(snapshot, period)
    findings: List[AssessmentFinding] = []

    # Dimension 1: Access to Money
    if m.liquid_assets.is_zero or (m.liquid_asset_ratio and m.liquid_asset_ratio.percentage < Decimal("10.0")):
        findings.append(
            AssessmentFinding(
                dimension=ResilienceDimension.ACCESS_TO_MONEY,
                finding="Low immediate liquid reserves relative to overall assets.",
                evidence=explain_liquidity_status(m.liquid_assets, m.liquid_asset_ratio),
                impact="Sudden disruptions or emergencies may force high-cost borrowing or premature asset liquidation.",
                uncertainty="Practical conversion time of fixed deposits or mutual funds depends on terms.",
                investor_consideration="Consider maintaining an accessible emergency reserve before locking funds into long-term illiquid goals.",
            )
        )
    else:
        findings.append(
            AssessmentFinding(
                dimension=ResilienceDimension.ACCESS_TO_MONEY,
                finding="Adequate liquid assets buffer available.",
                evidence=explain_liquidity_status(m.liquid_assets, m.liquid_asset_ratio),
                impact="Supports short-term liquidity without disrupting ongoing investments.",
                uncertainty="Verify withdrawal terms and bank access permissions.",
                investor_consideration="Maintain liquid funds in accessible accounts for planned short-term commitments.",
            )
        )

    # Dimension 2: Cash-flow Continuity
    if m.available_monthly_surplus.is_negative:
        findings.append(
            AssessmentFinding(
                dimension=ResilienceDimension.CASH_FLOW_CONTINUITY,
                finding="Monthly cash-flow deficit detected.",
                evidence=explain_cash_flow_status(
                    m.net_monthly_income,
                    m.monthly_expenses,
                    m.monthly_savings_investments,
                    m.available_monthly_surplus,
                ),
                impact="Deficit drains cash reserves or increases revolving debt.",
                uncertainty="Distinguish recurring outflows from one-off payments.",
                investor_consideration="Review discretionary expenses or adjust ongoing investment amounts to balance cash flow.",
            )
        )
    else:
        findings.append(
            AssessmentFinding(
                dimension=ResilienceDimension.CASH_FLOW_CONTINUITY,
                finding="Positive available monthly surplus.",
                evidence=explain_cash_flow_status(
                    m.net_monthly_income,
                    m.monthly_expenses,
                    m.monthly_savings_investments,
                    m.available_monthly_surplus,
                ),
                impact="Provides ongoing funding capacity for future goal planning.",
                uncertainty="Excludes irregular annual expenses unless budgeted.",
                investor_consideration="Deploy uncommitted surplus towards prioritized goal SIPs or debt reduction.",
            )
        )

    # Dimension 3: Debt Pressure
    high_rate_debts = [l for l in snapshot.liabilities if l.annual_interest_rate.percentage > Decimal("14.0")]
    if high_rate_debts:
        debts_desc = ", ".join([f"{l.name} ({l.annual_interest_rate.percentage:.1f}%)" for l in high_rate_debts])
        findings.append(
            AssessmentFinding(
                dimension=ResilienceDimension.DEBT_PRESSURE,
                finding="High-interest debt obligations present (>14% p.a.).",
                evidence=f"Debts triggering high-interest assessment: {debts_desc}.",
                impact="Interest drag significantly erodes household wealth and reduces monthly surplus.",
                uncertainty="Prepayment charges and foreclosure terms need verification.",
                investor_consideration="Evaluate trade-off between aggressive debt prepayment vs continuing new investments (CTR-HIR-001).",
            )
        )

    # Dimension 4: Protection Gaps
    if not m.has_active_health_insurance:
        findings.append(
            AssessmentFinding(
                dimension=ResilienceDimension.PROTECTION_GAPS,
                finding="No active health insurance coverage evidenced.",
                evidence="No individual or family floater health policy recorded in Financial State.",
                impact="Major hospitalization or medical emergency could cause direct depletion of savings.",
                uncertainty="Employer group health cover may exist but is unverified in records.",
                investor_consideration="Prioritize basic indemnity health insurance coverage for household members.",
            )
        )
    elif m.life_insurance_coverage_ratio and m.life_insurance_coverage_ratio.percentage < Decimal("50.0"):
        findings.append(
            AssessmentFinding(
                dimension=ResilienceDimension.PROTECTION_GAPS,
                finding="Life insurance cover appears below 10x income + liabilities guideline.",
                evidence=f"Existing sum assured is {m.existing_life_sum_assured.amount} vs guideline required cover of {m.required_life_cover.amount} ({m.life_insurance_coverage_ratio.percentage:.1f}% coverage).",
                impact="Dependents may face financial strain in case of untimely breadwinner loss.",
                uncertainty="Individual policy exclusions, riders and employer group life cover unverified.",
                investor_consideration="Assess pure term life insurance to bridge the protection gap.",
            )
        )

    # Dimension 5: Concentration & Dependency
    if m.portfolio_concentration and m.portfolio_concentration.percentage > Decimal("50.0"):
        findings.append(
            AssessmentFinding(
                dimension=ResilienceDimension.CONCENTRATION_DEPENDENCY,
                finding="High asset concentration in a single holding.",
                evidence=f"Largest asset accounts for {m.portfolio_concentration.percentage:.1f}% of total portfolio value ({m.largest_single_asset.amount}).",
                impact="Portfolio performance is heavily vulnerable to adverse movements in this single holding.",
                uncertainty="Asset liquidity and lock-in period affect diversification options.",
                investor_consideration="Consider progressive diversification across asset classes for long-term resilience.",
            )
        )

    return MoneywheelAssessmentResult(
        investor_id=snapshot.investor_id,
        evaluation_date=snapshot.as_of_date,
        measurements=m,
        findings=findings,
    )
