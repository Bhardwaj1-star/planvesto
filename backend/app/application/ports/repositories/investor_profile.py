"""
application/ports/repositories/investor_profile.py
Repository port for Investor Profile & Financial State operations.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class IInvestorProfileRepository(ABC):
    @abstractmethod
    def get_financial_facts(self, planning_unit_id: str) -> Dict[str, List[Dict[str, Any]]]:
        """Load raw evidenced financial facts (investors, income, expenses, assets, liabilities)."""
        pass

    @abstractmethod
    def save_financial_state_snapshot(
        self,
        planning_unit_id: str,
        scope: str,
        investor_id: Optional[str],
        snapshot: Dict[str, Any],
        authority: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Persist an immutable Financial State snapshot and return the snapshot_id."""
        pass

    @abstractmethod
    def get_financial_state_snapshot(
        self, planning_unit_id: str, snapshot_id: str
    ) -> Optional[Dict[str, Any]]:
        """Retrieve a specific Financial State snapshot by ID."""
        pass

    @abstractmethod
    def get_latest_financial_state_snapshot(
        self, planning_unit_id: str, scope: str = "household"
    ) -> Optional[Dict[str, Any]]:
        """Retrieve the latest Financial State snapshot for a planning unit."""
        pass
