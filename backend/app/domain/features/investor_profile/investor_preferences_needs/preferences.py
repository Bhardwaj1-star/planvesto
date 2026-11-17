"""
domain/features/investor_profile/investor_preferences_needs/preferences.py
Investor-stated preferences, needs and priorities used as planning context.

Non-negotiable invariants:
- A preference is not proof of suitability, feasibility or acceptance.
- Does not override hard mathematical or regulatory constraints.
"""

from dataclasses import dataclass, field
from typing import List, Optional
from app.domain.shared.value_objects import Money


@dataclass(frozen=True)
class InvestorPreferences:
    """Stated investor preferences, exclusions, and liquidity requirements."""
    investor_id: str
    tax_preference: str = "tax_efficient"
    minimum_emergency_reserve_target: Optional[Money] = None
    preferred_investment_modes: List[str] = field(default_factory=lambda: ["SIP", "LUMP_SUM"])
    ethical_or_esg_exclusions: List[str] = field(default_factory=list)
    liquidity_buffer_months: int = 6
    notes: Optional[str] = None
