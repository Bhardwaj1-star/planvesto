"""
domain/features/strategy_builder/monitoring.py
Chapter 11 — Strategy Builder Step 6: Monitoring & Gap Analysis (§11.4).

Ongoing comparison of actual accumulation against projected trajectory.
Identifies funding deviations, drift, or gaps and assesses contingency alternatives.
Non-negotiable invariants:
- Does not own Accepted Plan adoption or Action Plan lifecycle (Chapter 13).
- Presents diagnostic gaps and trade-offs without auto-executing corrective orders.
"""

from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import List, Optional
from app.domain.shared.value_objects import Money, Rate


class FundingStatus(str, Enum):
    ON_TRACK = "on_track"
    AHEAD_OF_TARGET = "ahead_of_target"
    SHORTFALL_IDENTIFIED = "shortfall_identified"
    CRITICAL_DEFICIT = "critical_deficit"


@dataclass(frozen=True)
class GoalMonitoringCheckpoint:
    """Checkpoint comparing actual progress to projected benchmark."""
    goal_id: str
    checkpoint_date: date
    projected_corpus_benchmark: Money
    actual_accumulated_corpus: Money
    deviation_amount: Money
    status: FundingStatus
    contingency_options: List[str]
