"""
domain/features/multi_goal_planning/goal_coordination.py
Multi-Goal Planning: Goal Coordination.

Coordinates selected goals in one planning context and assesses combined multi-goal feasibility.
Non-negotiable invariants:
- Does not recalculate individual goal requirements or feasibility (Goal Planner owns that).
- Consumes approved goal requirements and feasibility outputs.
"""

from dataclasses import dataclass
from typing import List
from app.domain.shared.value_objects import Money
from app.domain.features.goal_planner.requirement import GoalRequirement
from app.domain.features.goal_planner.feasibility import GoalFeasibilityResult


@dataclass(frozen=True)
class GoalBasketItem:
    """An individual goal participating in the multi-goal coordination context."""
    goal_requirement: GoalRequirement
    individual_feasibility: GoalFeasibilityResult
    investor_priority_rank: int


@dataclass(frozen=True)
class CombinedMultiGoalFeasibility:
    """Combined feasibility evaluation across all selected basket goals."""
    total_required_monthly_sip: Money
    available_monthly_surplus: Money
    combined_surplus_gap: Money
    is_combined_feasible: bool
    participating_goal_count: int
