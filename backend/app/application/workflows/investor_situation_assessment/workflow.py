"""
application/workflows/investor_situation_assessment/workflow.py
Chapter 07 — Investor Situation Assessment Workflow.

Coordinates the cross-feature sequence for assessing an investor's overall financial situation:
1. Verifies Financial State data readiness (Chapter 04).
2. Computes Moneywheel measurements and runs resilience diagnostics (Chapters 05 & 09).
3. Reconciles Risk Profile (Capacity vs Tolerance) if available.
4. Synthesizes a unified Situation Assessment bundle for planning decisions.

Non-negotiable invariants:
- Does not own calculation formulas or diagnostic rules (domain modules own them).
- Coordinates sequence and aggregates outputs.
"""

from dataclasses import dataclass
from datetime import date
from typing import List, Optional

from app.domain.shared.value_objects import CalendarMonth
from app.domain.features.investor_profile.financial_state import (
    FinancialStateSnapshot,
    DataReadinessReport,
    assess_data_readiness,
)
from app.domain.features.investor_profile.risk_profile import (
    RiskProfile,
    RiskAssessmentOutcome,
    assess_risk_profile,
)
from app.domain.features.investor_profile.behavioural_profile import (
    BehaviouralProfile,
    interpret_behavioural_guardrails,
)
from app.domain.features.investor_profile.investor_preferences_needs import (
    InvestorPreferences,
)
from app.domain.features.moneywheel import (
    MoneywheelMeasurements,
    MoneywheelAssessmentResult,
    assess_financial_health,
)


@dataclass(frozen=True)
class InvestorSituationAssessmentResult:
    """Consolidated situation assessment bundle."""
    investor_id: str
    assessment_date: date
    period: CalendarMonth
    readiness: DataReadinessReport
    moneywheel: MoneywheelAssessmentResult
    risk_assessment: Optional[RiskAssessmentOutcome] = None
    behavioural_guardrails: List[str] = None
    preferences: Optional[InvestorPreferences] = None
    executive_summary: str = ""


def execute_investor_situation_assessment(
    snapshot: FinancialStateSnapshot,
    period: CalendarMonth,
    risk_profile: Optional[RiskProfile] = None,
    behavioural_profile: Optional[BehaviouralProfile] = None,
    preferences: Optional[InvestorPreferences] = None,
) -> InvestorSituationAssessmentResult:
    """
    Coordinates the Chapter 07 situation assessment sequence.
    """
    # Step 1: Check Data Readiness
    readiness = assess_data_readiness(snapshot, period)

    # Step 2: Run Moneywheel Assessment & Resilience Diagnostics
    moneywheel_res = assess_financial_health(snapshot, period)

    # Step 3: Reconcile Risk Profile if available
    risk_res: Optional[RiskAssessmentOutcome] = None
    if risk_profile is not None:
        risk_res = assess_risk_profile(risk_profile)

    # Step 4: Extract Behavioural Guardrails if available
    guardrails: List[str] = []
    if behavioural_profile is not None:
        guardrails = interpret_behavioural_guardrails(behavioural_profile)

    # Step 5: Synthesize Executive Summary
    summary_parts = [
        f"Situation assessment evaluated as of {snapshot.as_of_date}.",
        f"Net worth: {moneywheel_res.measurements.net_worth.amount}.",
        f"Available monthly surplus: {moneywheel_res.measurements.available_monthly_surplus.amount}.",
        f"Identified {len(moneywheel_res.findings)} resilience diagnostic finding(s).",
    ]
    if risk_res:
        summary_parts.append(f"Reconciled risk posture: {risk_res.reconciled_risk_posture}.")
    if not readiness.is_ready_for_goal_feasibility:
        summary_parts.append(f"Notice: Missing inputs for goal planning: {', '.join(readiness.missing_inputs_for_goal_planning)}.")

    return InvestorSituationAssessmentResult(
        investor_id=snapshot.investor_id,
        assessment_date=snapshot.as_of_date,
        period=period,
        readiness=readiness,
        moneywheel=moneywheel_res,
        risk_assessment=risk_res,
        behavioural_guardrails=guardrails,
        preferences=preferences,
        executive_summary=" ".join(summary_parts),
    )
