"""
domain/features/multi_goal_planning/consolidated_plan.py
Multi-Goal Planning: Consolidated Multi-Goal Plan Assembly.

Assembles the coordinated multi-goal planning result:
- Combined feasibility outcome
- Goal-wise funding positions
- Shared-resource overlaps / conflicts
- Priorities, cross-goal impacts, and shortfalls
Non-negotiable invariants:
- Does not create an Accepted Plan or authorize transactions (Chapter 13).
- Report rendering belongs to infrastructure.
"""

from dataclasses import dataclass, field
from datetime import date
from typing import List, Optional
from app.domain.shared.value_objects import Money
from app.domain.features.multi_goal_planning.goal_coordination import (
    GoalBasketItem,
    CombinedMultiGoalFeasibility,
)
from app.domain.features.multi_goal_planning.shared_resources import SharedResourceConflict
from app.domain.features.multi_goal_planning.resource_allocation import MultiGoalAllocationPlan
from app.domain.features.multi_goal_planning.cross_goal_impact import CrossGoalImpactFinding


@dataclass(frozen=True)
class ConsolidatedMultiGoalPlan:
    """Consolidated assessment of multiple goals evaluated as an integrated basket."""
    basket_id: str
    investor_id: str
    assessment_date: date
    basket_goals: List[GoalBasketItem]
    combined_feasibility: CombinedMultiGoalFeasibility
    allocation_plan: Optional[MultiGoalAllocationPlan]
    detected_conflicts: List[SharedResourceConflict] = field(default_factory=list)
    cross_goal_impacts: List[CrossGoalImpactFinding] = field(default_factory=list)
    consolidated_summary: str = ""
