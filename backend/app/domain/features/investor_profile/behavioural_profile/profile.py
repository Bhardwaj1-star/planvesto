"""
domain/features/investor_profile/behavioural_profile/profile.py
Domain representation of approved behavioral context relevant to financial decisions.

Captures evidenced behavioural tendencies:
- Past market drop reaction (panic selling vs buying vs doing nothing)
- Decision-making style (analytical, intuitive, advisor-reliant)
- Financial discipline / consistency
Non-negotiable: No unsupported personality types or medicalized diagnoses.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class MarketDownturnReaction(str, Enum):
    PANIC_SOLD = "panic_sold"
    HELD_STEADY = "held_steady"
    INVESTED_MORE = "invested_more"
    NO_PRIOR_EXPERIENCE = "no_prior_experience"


class FinancialDecisionStyle(str, Enum):
    DATA_DRIVEN_DELIBERATE = "data_driven_deliberate"
    INTUITIVE_QUICK = "intuitive_quick"
    DELEGATIVE_COLLABORATIVE = "delegative_collaborative"


@dataclass(frozen=True)
class BehaviouralProfile:
    """Investor behavioral traits evidenced from past actions and stated habits."""
    investor_id: str
    past_downturn_reaction: MarketDownturnReaction
    decision_style: FinancialDecisionStyle
    has_history_of_early_withdrawal: bool = False
    context_notes: Optional[str] = None
