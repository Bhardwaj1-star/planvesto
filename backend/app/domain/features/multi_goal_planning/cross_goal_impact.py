"""
domain/features/multi_goal_planning/cross_goal_impact.py
Multi-Goal Planning: Cross-Goal Impact Analysis.

Assesses cross-goal effects of proposed adjustments to a goal's target amount,
timeline, or resource allocation (e.g., extending timeline on Goal A frees up surplus for Goal B).
Non-negotiable invariants:
- Does not recalculate individual requirements (Goal Planner does that).
- Does not mutate actual Financial State.
"""

from dataclasses import dataclass
from typing import List
from app.domain.shared.value_objects import Money


@dataclass(frozen=True)
class CrossGoalImpactFinding:
    """Documented effect of an adjustment on sibling goals in the basket."""
    adjusted_goal_id: str
    impacted_goal_id: str
    impact_description: str
    freed_up_monthly_surplus: Money
    resulting_feasibility_change: str
