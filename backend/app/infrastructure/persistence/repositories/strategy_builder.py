"""
infrastructure/persistence/repositories/strategy_builder.py
Concrete implementation of IStrategyBuilderRepository using Supabase / PostgreSQL.
"""

from typing import Any, Dict, List, Optional
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
        self._memory_versions_by_id: Dict[str, Dict[str, Any]] = {}
        self._memory_assessments: Dict[str, Dict[str, Any]] = {}
        self._memory_runs: Dict[str, Dict[str, Any]] = {}

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
        self._memory_versions_by_id[version_id] = payload

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

    def get_strategy_version_by_id(
        self, planning_unit_id: str, strategy_version_id: str
    ) -> Optional[Dict[str, Any]]:
        if self.client is not None:
            try:
                res = (
                    self.client.table("strategy_versions")
                    .select("*")
                    .eq("planning_unit_id", planning_unit_id)
                    .eq("strategy_version_id", strategy_version_id)
                    .limit(1)
                    .execute()
                )
                if res.data:
                    return res.data[0]
            except Exception as exc:
                logger.warning(f"Error loading version {strategy_version_id}: {exc}")
        return self._memory_versions_by_id.get(strategy_version_id)

    def list_strategy_versions_for_strategy(
        self, planning_unit_id: str, strategy_id: str
    ) -> List[Dict[str, Any]]:
        if self.client is not None:
            try:
                res = (
                    self.client.table("strategy_versions")
                    .select("*")
                    .eq("planning_unit_id", planning_unit_id)
                    .eq("strategy_id", strategy_id)
                    .order("version", desc=True)
                    .execute()
                )
                if res.data:
                    return res.data
            except Exception as exc:
                logger.warning(f"Error listing versions for {strategy_id}: {exc}")
        return [
            v for v in self._memory_versions_by_id.values()
            if v.get("planning_unit_id") == planning_unit_id and v.get("strategy_id") == strategy_id
        ]

    def save_strategy_run(
        self, planning_unit_id: str, goal_id: str, run_payload: Dict[str, Any]
    ) -> str:
        run_id = run_payload.get("strategy_run_id") or str(uuid.uuid4())
        payload = dict(run_payload)
        payload["strategy_run_id"] = run_id
        payload["planning_unit_id"] = planning_unit_id
        payload["goal_id"] = goal_id
        self._memory_runs[run_id] = payload
        return run_id

    def get_strategy_run(
        self, planning_unit_id: str, run_id: str
    ) -> Optional[Dict[str, Any]]:
        return self._memory_runs.get(run_id)

    def list_strategy_runs_for_goal(
        self, planning_unit_id: str, goal_id: str
    ) -> List[Dict[str, Any]]:
        runs = [
            r for r in self._memory_runs.values()
            if r.get("planning_unit_id") == planning_unit_id and r.get("goal_id") == goal_id
        ]
        runs.sort(key=lambda x: x.get("run_version", 1), reverse=True)
        return runs

