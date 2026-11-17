"""
domain/features/investor_profile/behavioural_profile/interpretation.py
Interpretation of recorded behavioral context for downstream planning decisions.

Does not diagnose the investor or create unsupported scores.
Provides practical advisory guardrails (e.g. recommend automated SIPs or systematic withdrawal plans
if early withdrawal history exists).
"""

from typing import List
from app.domain.features.investor_profile.behavioural_profile.profile import (
    BehaviouralProfile,
    MarketDownturnReaction,
)


def interpret_behavioural_guardrails(profile: BehaviouralProfile) -> List[str]:
    """Generates planning guardrails based on evidenced behavioural tendencies."""
    guardrails: List[str] = []

    if profile.past_downturn_reaction == MarketDownturnReaction.PANIC_SOLD:
        guardrails.append(
            "Investor has a recorded history of selling during drawdowns. "
            "Recommend building higher liquid emergency reserves and establishing pre-committed rebalancing rules to reduce panic triggers."
        )

    if profile.has_history_of_early_withdrawal:
        guardrails.append(
            "History of tapping goal-earmarked funds prematurely. "
            "Recommend hard goal account segregation and automated SIP mandates."
        )

    return guardrails
