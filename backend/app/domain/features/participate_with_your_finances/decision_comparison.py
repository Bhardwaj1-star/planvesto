"""
domain/features/participate_with_your_finances/decision_comparison.py
Chapter 12 — Participate with Your Finances: Decision Comparison (§12.3).

Compares distinct hypothetical decision alternatives side-by-side.
Non-negotiable invariants:
- Does not force a single 'winner' or rank options by a hidden formula.
- Does not silently adopt or execute an alternative.
- Investor retains full authority to deliberate and decide.
"""

from dataclasses import dataclass
from typing import List
from app.domain.shared.value_objects import Money


@dataclass(frozen=True)
class DecisionAlternativeOption:
    """A distinct option under evaluation by the investor."""
    option_id: str
    option_name: str
    description: str
    monthly_outflow: Money
    total_lifetime_cost: Money
    pros: List[str]
    cons: List[str]
    key_trade_off: str


@dataclass(frozen=True)
class DecisionComparisonResult:
    """Structured side-by-side comparison of decision alternatives."""
    comparison_id: str
    investor_id: str
    title: str
    context_description: str
    options: List[DecisionAlternativeOption]
    unresolved_questions_for_investor: List[str]
