"""
application/ports/repositories/action_plan.py
Repository port for Action Plan items and decision history.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class IActionPlanRepository(ABC):
    @abstractmethod
    def list_actions(self, planning_unit_id: str) -> List[Dict[str, Any]]:
        """List all active action plan items for a planning unit."""
        pass

    @abstractmethod
    def get_action(self, planning_unit_id: str, action_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a specific action plan item by ID."""
        pass

    @abstractmethod
    def save_action(self, action_payload: Dict[str, Any]) -> Dict[str, Any]:
        """Insert a newly authorized action plan item."""
        pass

    @abstractmethod
    def update_action_status(
        self,
        planning_unit_id: str,
        action_id: str,
        status: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Transition an action's lifecycle status and record decision history."""
        pass
