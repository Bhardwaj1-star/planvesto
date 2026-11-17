"""
domain/features/investor_profile/risk_profile/profile.py
Approved investor risk-profile dimensions.

Maintains distinct:
1. Risk Capacity (objective financial ability to absorb loss)
2. Risk Tolerance (psychological willingness to endure volatility)
3. Risk Need (rate of return needed to achieve goals)
Non-negotiable: Does not collapse capacity, tolerance and willingness into a single invented score.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional
from app.domain.shared.value_objects import Rate


class RiskToleranceBand(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"


class RiskCapacityBand(str, Enum):
    LIMITED = "limited"
    ADEQUATE = "adequate"
    SUBSTANTIAL = "substantial"


@dataclass(frozen=True)
class RiskProfile:
    """Investor risk profile dimensions recorded with dated context."""
    investor_id: str
    risk_capacity: RiskCapacityBand
    risk_tolerance: RiskToleranceBand
    stated_time_horizon_years: int
    maximum_drawdown_tolerance_pct: Optional[Rate] = None
    capacity_notes: Optional[str] = None
    tolerance_notes: Optional[str] = None
