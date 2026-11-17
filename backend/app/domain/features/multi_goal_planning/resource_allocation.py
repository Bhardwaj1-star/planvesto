"""
domain/features/multi_goal_planning/resource_allocation.py
Multi-Goal Planning: Resource Allocation.

Represents and assesses alternative allocations of evidenced available resources
and contribution capacity across selected goals.
Non-negotiable invariants:
- Does not invent an optimisation algorithm or silent allocation formula.
- Does not automatically reassign, sell, or withdraw assets without investor approval.
"""

from dataclasses import dataclass
from typing import Dict, List
from app.domain.shared.value_objects import Money


@dataclass(frozen=True)
class GoalResourceAllocation:
    """Evidenced resources apportioned to a specific goal."""
    goal_id: str
    allocated_monthly_sip: Money
    allocated_lump_sum_assets: Money
    fully_meets_individual_requirement: bool


@dataclass(frozen=True)
class MultiGoalAllocationPlan:
    """A candidate multi-goal resource allocation distribution."""
    allocation_plan_id: str
    investor_id: str
    allocations_by_goal: List[GoalResourceAllocation]
    unallocated_monthly_surplus: Money
    unallocated_assets: Money
