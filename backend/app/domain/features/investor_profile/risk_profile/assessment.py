"""
domain/features/investor_profile/risk_profile/assessment.py
Risk profile assessment behavior using only approved inputs.

Provides clear reconciliation when Risk Capacity and Risk Tolerance diverge
(e.g., High Tolerance but Low Capacity requires prudent exposure limits).
"""

from dataclasses import dataclass
from typing import List
from app.domain.features.investor_profile.risk_profile.profile import (
    RiskProfile,
    RiskCapacityBand,
    RiskToleranceBand,
)


@dataclass(frozen=True)
class RiskAssessmentOutcome:
    """Reconciled risk posture and advisory guidance."""
    investor_id: str
    reconciled_risk_posture: str
    divergence_notes: List[str]
    max_equity_exposure_guideline_pct: int


def assess_risk_profile(profile: RiskProfile) -> RiskAssessmentOutcome:
    """
    Evaluates capacity vs tolerance.
    Principle: Risk Capacity acts as the hard ceiling on risk-taking.
    """
    notes: List[str] = []

    if profile.risk_capacity == RiskCapacityBand.LIMITED:
        max_equity = 30
        if profile.risk_tolerance == RiskToleranceBand.HIGH:
            notes.append(
                "Divergence detected: High psychological tolerance but limited financial capacity. "
                "Capacity constrains max loss absorption; conservative asset allocation recommended."
            )
        posture = "conservative_constrained"
    elif profile.risk_capacity == RiskCapacityBand.ADEQUATE:
        if profile.risk_tolerance == RiskToleranceBand.LOW:
            max_equity = 40
            posture = "moderately_conservative"
        elif profile.risk_tolerance == RiskToleranceBand.HIGH:
            max_equity = 70
            posture = "growth_oriented"
        else:
            max_equity = 55
            posture = "balanced"
    else:  # SUBSTANTIAL
        if profile.risk_tolerance == RiskToleranceBand.HIGH:
            max_equity = 85
            posture = "aggressive_growth"
        elif profile.risk_tolerance == RiskToleranceBand.LOW:
            max_equity = 40
            notes.append("Substantial capacity present, but conservative allocation chosen due to low psychological tolerance.")
            posture = "conservative_capital_preservation"
        else:
            max_equity = 65
            posture = "moderate_growth"

    return RiskAssessmentOutcome(
        investor_id=profile.investor_id,
        reconciled_risk_posture=posture,
        divergence_notes=notes,
        max_equity_exposure_guideline_pct=max_equity,
    )
