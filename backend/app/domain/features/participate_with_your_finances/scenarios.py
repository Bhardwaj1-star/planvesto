"""
domain/features/participate_with_your_finances/scenarios.py
Chapter 12 — Participate with Your Finances: Hypothetical Scenarios (§12.1).

Non-negotiable invariants:
1. A scenario is hypothetical: it NEVER mutates actual Financial State or Accepted Plan.
2. A scenario is not an investor decision, advice, or plan acceptance.
3. Every scenario explicitly references its baseline data snapshot.
"""

from dataclasses import dataclass, field
from datetime import date
from typing import Dict, List, Optional
from app.domain.shared.value_objects import Money, Rate


@dataclass(frozen=True)
class HypotheticalParameterOverride:
    """Hypothetical modification of an input parameter for what-if testing."""
    parameter_name: str
    baseline_value: str
    hypothetical_value: str
    rationale: str


@dataclass(frozen=True)
class HypotheticalScenario:
    """Hypothetical scenario entity capturing an investor's what-if investigation."""
    scenario_id: str
    investor_id: str
    scenario_name: str
    created_at: date
    baseline_snapshot_id: str
    parameter_overrides: List[HypotheticalParameterOverride]
    notes: Optional[str] = None
    is_hypothetical_only: bool = True
