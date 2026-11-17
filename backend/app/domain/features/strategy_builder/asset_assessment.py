"""
domain/features/strategy_builder/asset_assessment.py
Chapter 11 — Strategy Builder Step 2: Asset Assessment (§11.4).

Evaluates mapped assets: keep vs reallocate vs exclude.
Asset classification and actual records remain owned by Financial State.
No automatic sale, withdrawal or reallocation without explicit investor approval.
"""

from dataclasses import dataclass
from enum import Enum
from app.domain.shared.value_objects import Money, Rate


class AssetDispositionChoice(str, Enum):
    """Step 2: Asset Assessment decisions approved by investor (§11.4)."""
    KEEP = "keep"
    REALLOCATE = "reallocate"
    EXCLUDE = "exclude"


@dataclass(frozen=True)
class AssetDecision:
    """Investor-approved asset disposition decision (§11.4 Step 2)."""
    asset_id: str
    asset_name: str
    choice: AssetDispositionChoice
    current_value: Money
    expected_annual_return: Rate
