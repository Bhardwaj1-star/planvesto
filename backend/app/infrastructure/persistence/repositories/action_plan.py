"""
infrastructure/persistence/repositories/action_plan.py
Concrete implementation of IActionPlanRepository using Supabase / PostgreSQL.
"""

from datetime import date
from typing import Any, Dict, List, Optional
import uuid

from app.application.ports.repositories.action_plan import (
    IActionPlanRepository,
)
from app.core.logging import get_logger
from app.infrastructure.persistence.database import get_db_client

logger = get_logger(__name__)


class ActionPlanRepository(IActionPlanRepository):
    """Handles persistence of Action Plan items and status updates."""

    def __init__(self, client: Any = None):
        self._client = client
        self._memory_actions: Dict[str, Dict[str, Any]] = {}
        self._decision_history: List[Dict[str, Any]] = []

    @property
    def client(self):
        if self._client is None:
            self._client = get_db_client()
        return self._client

    def list_actions(self, planning_unit_id: str) -> List[Dict[str, Any]]:
        if self.client is not None:
            try:
                res = (
                    self.client.table("action_plan_items")
                    .select("*")
                    .eq("planning_unit_id", planning_unit_id)
                    .order("created_at", desc=True)
                    .execute()
                )
                if res.data:
                    return res.data
            except Exception as exc:
                logger.warning(f"Error loading actions from Supabase: {exc}")

        return [
            a for a in self._memory_actions.values()
            if a.get("planning_unit_id") == planning_unit_id
        ]

    def get_action(self, planning_unit_id: str, action_id: str) -> Optional[Dict[str, Any]]:
        if self.client is not None:
            try:
                res = (
                    self.client.table("action_plan_items")
                    .select("*")
                    .eq("planning_unit_id", planning_unit_id)
                    .eq("action_id", action_id)
                    .limit(1)
                    .execute()
                )
                if res.data:
                    return res.data[0]
            except Exception as exc:
                logger.warning(f"Error loading action {action_id} from Supabase: {exc}")

        return self._memory_actions.get(action_id)

    def save_action(self, action_payload: Dict[str, Any]) -> Dict[str, Any]:
        aid = action_payload.get("action_id") or str(uuid.uuid4())
        payload = dict(action_payload)
        payload["action_id"] = aid
        self._memory_actions[aid] = payload

        if self.client is not None:
            try:
                res = self.client.table("action_plan_items").insert(payload).execute()
                if res.data:
                    return res.data[0]
            except Exception as exc:
                logger.warning(f"Error saving action {aid} to Supabase: {exc}")

        return payload

    def update_action_status(
        self,
        planning_unit_id: str,
        action_id: str,
        status: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        update_data = {
            "status": status,
            "status_updated_at": date.today().isoformat(),
        }
        if metadata:
            update_data.update(metadata)

        if action_id in self._memory_actions:
            self._memory_actions[action_id].update(update_data)

        # Log history
        self._decision_history.append({
            "action_id": action_id,
            "planning_unit_id": planning_unit_id,
            "new_status": status,
            "timestamp": date.today().isoformat(),
            "metadata": metadata or {},
        })

        if self.client is not None:
            try:
                self.client.table("action_plan_items").update(update_data).eq(
                    "planning_unit_id", planning_unit_id
                ).eq("action_id", action_id).execute()

                # Also insert decision history record if table exists
                self.client.table("action_decision_history").insert({
                    "action_id": action_id,
                    "planning_unit_id": planning_unit_id,
                    "action_type": "status_transition",
                    "new_status": status,
                }).execute()
            except Exception as exc:
                logger.warning(f"Error updating action {action_id} in Supabase: {exc}")

        return self._memory_actions.get(action_id, update_data)
