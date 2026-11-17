"""
infrastructure/persistence/repositories/investor_profile.py
Concrete implementation of IInvestorProfileRepository using Supabase / PostgreSQL.
"""

from datetime import date
from typing import Any, Dict, List, Optional
import uuid

from app.application.ports.repositories.investor_profile import (
    IInvestorProfileRepository,
)
from app.core.logging import get_logger
from app.infrastructure.persistence.database import get_db_client

logger = get_logger(__name__)


class InvestorProfileRepository(IInvestorProfileRepository):
    """Handles persistence of raw financial facts and Financial State snapshots."""

    def __init__(self, client: Any = None):
        self._client = client
        self._memory_snapshots: Dict[str, Dict[str, Any]] = {}
        self._memory_facts: Dict[str, Dict[str, List[Dict[str, Any]]]] = {}

    @property
    def client(self):
        if self._client is None:
            self._client = get_db_client()
        return self._client

    def get_financial_facts(self, planning_unit_id: str) -> Dict[str, List[Dict[str, Any]]]:
        if self.client is None:
            return self._memory_facts.get(planning_unit_id, {
                "income": [], "expenses": [], "assets": [], "liabilities": []
            })

        try:
            investors = self.client.table("investors").select("*").eq("planning_unit_id", planning_unit_id).execute().data or []
            income = self.client.table("income").select("*").eq("planning_unit_id", planning_unit_id).execute().data or []
            expenses = self.client.table("expenses").select("*").eq("planning_unit_id", planning_unit_id).execute().data or []
            assets = self.client.table("assets").select("*").eq("planning_unit_id", planning_unit_id).execute().data or []
            liabilities = self.client.table("liabilities").select("*").eq("planning_unit_id", planning_unit_id).execute().data or []

            return {
                "investors": investors,
                "income": income,
                "expenses": expenses,
                "assets": assets,
                "liabilities": liabilities,
            }
        except Exception as exc:
            logger.warning(f"Failed to query Supabase for financial facts: {exc}. Using fallback.")
            return self._memory_facts.get(planning_unit_id, {
                "income": [], "expenses": [], "assets": [], "liabilities": []
            })

    def save_financial_state_snapshot(
        self,
        planning_unit_id: str,
        scope: str,
        investor_id: Optional[str],
        snapshot: Dict[str, Any],
        authority: Optional[Dict[str, Any]] = None,
    ) -> str:
        snapshot_id = snapshot.get("snapshot_id") or str(uuid.uuid4())
        stored_state = dict(snapshot)
        if authority is not None:
            stored_state["__snapshot_authority"] = authority

        payload = {
            "snapshot_id": snapshot_id,
            "planning_unit_id": planning_unit_id,
            "scope": scope,
            "investor_id": investor_id,
            "financial_state": stored_state,
        }

        # Store in local memory cache
        key = f"{planning_unit_id}:{snapshot_id}"
        self._memory_snapshots[key] = payload
        self._memory_snapshots[f"{planning_unit_id}:latest"] = payload

        if self.client is not None:
            try:
                res = self.client.table("financial_state_snapshots").insert(payload).execute()
                if res.data:
                    return res.data[0].get("snapshot_id", snapshot_id)
            except Exception as exc:
                logger.warning(f"Could not persist snapshot to Supabase: {exc}. Cached locally.")

        return snapshot_id

    def get_financial_state_snapshot(
        self, planning_unit_id: str, snapshot_id: str
    ) -> Optional[Dict[str, Any]]:
        key = f"{planning_unit_id}:{snapshot_id}"
        if self.client is None:
            return self._memory_snapshots.get(key)

        try:
            res = (
                self.client.table("financial_state_snapshots")
                .select("*")
                .eq("planning_unit_id", planning_unit_id)
                .eq("snapshot_id", snapshot_id)
                .limit(1)
                .execute()
            )
            if res.data:
                return res.data[0]
        except Exception as exc:
            logger.warning(f"Could not load snapshot from Supabase: {exc}.")

        return self._memory_snapshots.get(key)

    def get_latest_financial_state_snapshot(
        self, planning_unit_id: str, scope: str = "family"
    ) -> Optional[Dict[str, Any]]:
        if self.client is not None:
            try:
                res = (
                    self.client.table("financial_state_snapshots")
                    .select("*")
                    .eq("planning_unit_id", planning_unit_id)
                    .eq("scope", scope)
                    .order("created_at", desc=True)
                    .limit(1)
                    .execute()
                )
                if res.data:
                    return res.data[0]
            except Exception as exc:
                logger.warning(f"Could not load latest snapshot from Supabase: {exc}.")

        return self._memory_snapshots.get(f"{planning_unit_id}:latest")
