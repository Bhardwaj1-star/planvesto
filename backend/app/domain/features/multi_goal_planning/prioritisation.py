"""
domain/features/multi_goal_planning/prioritisation.py
Multi-Goal Planning: Goal Prioritisation & Sequencing.

Assesses alternative goal priorities and sequencing using investor-stated preferences,
timelines, approved feasibility outputs and constraints.
Non-negotiable invariants:
- Does not invent priority weights, scoring bands, or a universal ranking formula.
- Does not silently change investor-stated priorities.
"""

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class GoalPriorityRank:
    """Investor-stated or candidate priority rank for a goal."""
    goal_id: str
    goal_title: str
    rank: int
    rationale: str


@dataclass(frozen=True)
class MultiGoalSequencingAssessment:
    """Sequential assessment of goals in order of investor priority."""
    prioritized_goals: List[GoalPriorityRank]
    advisory_trade_off_notes: List[str]
