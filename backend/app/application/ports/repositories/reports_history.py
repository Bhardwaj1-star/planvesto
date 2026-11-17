"""
application/ports/repositories/reports_history.py
Repository port for Reports and History audit records.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class IReportsHistoryRepository(ABC):
    @abstractmethod
    def save_report_record(
        self, planning_unit_id: str, report_payload: Dict[str, Any]
    ) -> str:
        """Persist an assembled report record."""
        pass

    @abstractmethod
    def get_report_record(
        self, planning_unit_id: str, report_id: str
    ) -> Optional[Dict[str, Any]]:
        """Retrieve a specific report record by ID."""
        pass

    @abstractmethod
    def list_history_records(
        self, planning_unit_id: str, record_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """List historical audit records for a planning unit."""
        pass
