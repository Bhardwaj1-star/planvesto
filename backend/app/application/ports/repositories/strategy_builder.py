"""
application/ports/repositories/strategy_builder.py
Repository port for Strategy Builder and Goal Funding evaluations.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class IStrategyBuilderRepository(ABC):
    @abstractmethod
    def save_strategy_version(
        self, planning_unit_id: str, goal_id: str, strategy_payload: Dict[str, Any]
    ) -> str:
        """Persist a new strategy version and return its ID."""
        pass

    @abstractmethod
    def get_latest_strategy_version(
        self, planning_unit_id: str, goal_id: str
    ) -> Optional[Dict[str, Any]]:
        """Retrieve the latest strategy version for a goal."""
        pass

    @abstractmethod
    def save_funding_assessment(
        self, planning_unit_id: str, goal_id: str, assessment_payload: Dict[str, Any]
    ) -> str:
        """Persist a goal funding strategy assessment result."""
        pass
