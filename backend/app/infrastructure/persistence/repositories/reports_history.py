"""
infrastructure/persistence/repositories/reports_history.py
Concrete implementation of IReportsHistoryRepository using Supabase / PostgreSQL.
"""

from typing import Any, Dict, List, Optional
import uuid

from app.application.ports.repositories.reports_history import (
    IReportsHistoryRepository,
)
from app.core.logging import get_logger
from app.infrastructure.persistence.database import get_db_client

logger = get_logger(__name__)


class ReportsHistoryRepository(IReportsHistoryRepository):
    """Handles persistence of Reports and History audit trails."""

    def __init__(self, client: Any = None):
        self._client = client
        self._memory_reports: Dict[str, Dict[str, Any]] = {}
        self._memory_history: List[Dict[str, Any]] = []

    @property
    def client(self):
        if self._client is None:
            self._client = get_db_client()
        return self._client

    def save_report_record(
        self, planning_unit_id: str, report_payload: Dict[str, Any]
    ) -> str:
        report_id = report_payload.get("report_id") or str(uuid.uuid4())
        payload = dict(report_payload)
        payload["report_id"] = report_id
        payload["planning_unit_id"] = planning_unit_id

        self._memory_reports[report_id] = payload
        self._memory_history.append({
            "record_id": report_id,
            "planning_unit_id": planning_unit_id,
            "record_type": "report",
            "content": payload,
        })

        if self.client is not None:
            try:
                res = self.client.table("reports").insert(payload).execute()
                if res.data:
                    return res.data[0].get("report_id", report_id)
            except Exception as exc:
                logger.warning(f"Error saving report {report_id} to Supabase: {exc}")

        return report_id

    def get_report_record(
        self, planning_unit_id: str, report_id: str
    ) -> Optional[Dict[str, Any]]:
        if self.client is not None:
            try:
                res = (
                    self.client.table("reports")
                    .select("*")
                    .eq("planning_unit_id", planning_unit_id)
                    .eq("report_id", report_id)
                    .limit(1)
                    .execute()
                )
                if res.data:
                    return res.data[0]
            except Exception as exc:
                logger.warning(f"Error retrieving report {report_id}: {exc}")

        return self._memory_reports.get(report_id)

    def list_history_records(
        self, planning_unit_id: str, record_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        if self.client is not None:
            try:
                query = self.client.table("history_records").select("*").eq(
                    "planning_unit_id", planning_unit_id
                )
                if record_type:
                    query = query.eq("record_type", record_type)
                res = query.order("created_at", desc=True).execute()
                if res.data:
                    return res.data
            except Exception as exc:
                logger.warning(f"Error querying history from Supabase: {exc}")

        return [
            h for h in self._memory_history
            if h.get("planning_unit_id") == planning_unit_id
            and (not record_type or h.get("record_type") == record_type)
        ]
