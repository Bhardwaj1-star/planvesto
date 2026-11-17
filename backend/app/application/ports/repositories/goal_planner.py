"""
application/ports/repositories/goal_planner.py
Repository port for Goal Planner & Defined Goals operations.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class IGoalPlannerRepository(ABC):
    @abstractmethod
    def list_goals(self, planning_unit_id: str) -> List[Dict[str, Any]]:
        """List all goals for a planning unit."""
        pass

    @abstractmethod
    def get_goal(self, planning_unit_id: str, goal_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a specific goal by ID."""
        pass

    @abstractmethod
    def ensure_goal_record(
        self,
        planning_unit_id: str,
        goal_id: Optional[str],
        goal_name: str,
        today_cost: float,
        target_month: int,
        target_year: int,
        priority: Optional[str] = None,
        flexibility: str = "Flexible",
    ) -> str:
        """Create or update a goal record and return the goal_id."""
        pass

    @abstractmethod
    def get_latest_defined_goal(
        self, planning_unit_id: str, goal_id: str
    ) -> Optional[Dict[str, Any]]:
        """Retrieve the latest defined goal version."""
        pass

    @abstractmethod
    def save_defined_goal(
        self, planning_unit_id: str, defined_goal_payload: Dict[str, Any]
    ) -> str:
        """Persist a new version of a defined goal and return the defined_goal_id."""
        pass
