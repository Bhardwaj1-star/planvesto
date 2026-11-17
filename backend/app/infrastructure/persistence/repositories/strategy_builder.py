"""
infrastructure/persistence/repositories/strategy_builder.py
Concrete implementation of IStrategyBuilderRepository using Supabase / PostgreSQL.
"""

from typing import Any, Dict, Optional
import uuid

from app.application.ports.repositories.strategy_builder import (
    IStrategyBuilderRepository,
)
from app.core.logging import get_logger
from app.infrastructure.persistence.database import get_db_client

logger = get_logger(__name__)


class StrategyBuilderRepository(IStrategyBuilderRepository):
    """Handles persistence of Strategy Versions and Funding Assessments."""

    def __init__(self, client: Any = None):
        self._client = client
        self._memory_strategies: Dict[str, Dict[str, Any]] = {}
        self._memory_assessments: Dict[str, Dict[str, Any]] = {}

    @property
    def client(self):
        if self._client is None:
            self._client = get_db_client()
        return self._client

    def save_strategy_version(
        self, planning_unit_id: str, goal_id: str, strategy_payload: Dict[str, Any]
    ) -> str:
        version_id = strategy_payload.get("strategy_version_id") or str(uuid.uuid4())
        payload = dict(strategy_payload)
        payload["strategy_version_id"] = version_id
        payload["planning_unit_id"] = planning_unit_id
        payload["goal_id"] = goal_id

        key = f"{planning_unit_id}:{goal_id}"
        self._memory_strategies[key] = payload

        if self.client is not None:
            try:
                res = self.client.table("strategy_versions").insert(payload).execute()
                if res.data:
                    return res.data[0].get("strategy_version_id", version_id)
            except Exception as exc:
                logger.warning(f"Error persisting strategy version to Supabase: {exc}")

        return version_id

    def get_latest_strategy_version(
        self, planning_unit_id: str, goal_id: str
    ) -> Optional[Dict[str, Any]]:
        if self.client is not None:
            try:
                res = (
                    self.client.table("strategy_versions")
                    .select("*")
                    .eq("planning_unit_id", planning_unit_id)
                    .eq("goal_id", goal_id)
                    .order("version", desc=True)
                    .limit(1)
                    .execute()
                )
                if res.data:
                    return res.data[0]
            except Exception as exc:
                logger.warning(f"Error loading strategy version from Supabase: {exc}")

        return self._memory_strategies.get(f"{planning_unit_id}:{goal_id}")

    def save_funding_assessment(
        self, planning_unit_id: str, goal_id: str, assessment_payload: Dict[str, Any]
    ) -> str:
        assessment_id = assessment_payload.get("assessment_id") or str(uuid.uuid4())
        payload = dict(assessment_payload)
        payload["assessment_id"] = assessment_id
        payload["planning_unit_id"] = planning_unit_id
        payload["goal_id"] = goal_id

        key = f"{planning_unit_id}:{goal_id}"
        self._memory_assessments[key] = payload

        if self.client is not None:
            try:
                res = self.client.table("goal_funding_assessments").insert(payload).execute()
                if res.data:
                    return res.data[0].get("assessment_id", assessment_id)
            except Exception as exc:
                logger.warning(f"Error persisting funding assessment to Supabase: {exc}")

        return assessment_id
