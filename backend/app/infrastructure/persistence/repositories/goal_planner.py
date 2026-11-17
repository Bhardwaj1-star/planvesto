"""
infrastructure/persistence/repositories/goal_planner.py
Concrete implementation of IGoalPlannerRepository using Supabase / PostgreSQL.
"""

from typing import Any, Dict, List, Optional
import uuid

from app.application.ports.repositories.goal_planner import (
    IGoalPlannerRepository,
)
from app.core.logging import get_logger
from app.infrastructure.persistence.database import get_db_client

logger = get_logger(__name__)


class GoalPlannerRepository(IGoalPlannerRepository):
    """Handles persistence of Goals and Defined Goals."""

    def __init__(self, client: Any = None):
        self._client = client
        self._memory_goals: Dict[str, Dict[str, Any]] = {}
        self._memory_defined_goals: Dict[str, List[Dict[str, Any]]] = {}

    @property
    def client(self):
        if self._client is None:
            self._client = get_db_client()
        return self._client

    def list_goals(self, planning_unit_id: str) -> List[Dict[str, Any]]:
        if self.client is not None:
            try:
                res = (
                    self.client.table("goals")
                    .select("goal_id, planning_unit_id, goal_name, target_amount, target_date, priority, flexibility")
                    .eq("planning_unit_id", planning_unit_id)
                    .order("created_at")
                    .execute()
                )
                if res.data:
                    return res.data
            except Exception as exc:
                logger.warning(f"Error querying goals from Supabase: {exc}")

        return [
            g for g in self._memory_goals.values()
            if g.get("planning_unit_id") == planning_unit_id
        ]

    def get_goal(self, planning_unit_id: str, goal_id: str) -> Optional[Dict[str, Any]]:
        if self.client is not None:
            try:
                res = (
                    self.client.table("goals")
                    .select("*")
                    .eq("planning_unit_id", planning_unit_id)
                    .eq("goal_id", goal_id)
                    .limit(1)
                    .execute()
                )
                if res.data:
                    return res.data[0]
            except Exception as exc:
                logger.warning(f"Error querying goal {goal_id}: {exc}")

        return self._memory_goals.get(goal_id)

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
        gid = goal_id or str(uuid.uuid4())
        payload = {
            "goal_id": gid,
            "planning_unit_id": planning_unit_id,
            "goal_name": goal_name,
            "target_amount": today_cost,
            "target_date": f"{target_year:04d}-{target_month:02d}-01",
            "priority": priority or "Important",
            "flexibility": flexibility,
        }

        self._memory_goals[gid] = payload

        if self.client is not None:
            try:
                if goal_id and self.get_goal(planning_unit_id, goal_id):
                    self.client.table("goals").update(payload).eq("goal_id", goal_id).execute()
                    return goal_id
                res = self.client.table("goals").insert(payload).execute()
                if res.data:
                    return res.data[0].get("goal_id", gid)
            except Exception as exc:
                logger.warning(f"Error saving goal {gid} to Supabase: {exc}")

        return gid

    def get_latest_defined_goal(
        self, planning_unit_id: str, goal_id: str
    ) -> Optional[Dict[str, Any]]:
        if self.client is not None:
            try:
                res = (
                    self.client.table("defined_goals")
                    .select("*")
                    .eq("planning_unit_id", planning_unit_id)
                    .eq("goal_id", goal_id)
                    .eq("is_latest", True)
                    .limit(1)
                    .execute()
                )
                if res.data:
                    return res.data[0]
            except Exception as exc:
                logger.warning(f"Error querying defined_goal for {goal_id}: {exc}")

        versions = self._memory_defined_goals.get(goal_id, [])
        return versions[-1] if versions else None

    def save_defined_goal(
        self, planning_unit_id: str, defined_goal_payload: Dict[str, Any]
    ) -> str:
        d_id = defined_goal_payload.get("defined_goal_id") or str(uuid.uuid4())
        payload = dict(defined_goal_payload)
        payload["defined_goal_id"] = d_id
        payload["planning_unit_id"] = planning_unit_id

        goal_id = str(payload.get("goal_id", ""))
        if goal_id not in self._memory_defined_goals:
            self._memory_defined_goals[goal_id] = []
        self._memory_defined_goals[goal_id].append(payload)

        if self.client is not None:
            try:
                # Mark existing versions as not latest
                self.client.table("defined_goals").update({"is_latest": False}).eq(
                    "goal_id", goal_id
                ).execute()

                res = self.client.table("defined_goals").insert(payload).execute()
                if res.data:
                    return res.data[0].get("defined_goal_id", d_id)
            except Exception as exc:
                logger.warning(f"Error persisting defined_goal to Supabase: {exc}")

        return d_id
