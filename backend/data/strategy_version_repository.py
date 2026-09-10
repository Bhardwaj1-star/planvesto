from typing import Any

from models.strategy_version import StrategyVersion


class StrategyVersionRepository:
    """Persistence boundary for immutable StrategyVersion records.

    The repository intentionally exposes insert/read operations only. Database
    enforcement is added by the strategy_versions migration.
    """

    def __init__(self, supabase_client: Any):
        self.client = supabase_client
        self.table_name = "strategy_versions"

    def get_latest_version(self, planning_unit_id: str, strategy_id: str) -> StrategyVersion | None:
        response = (
            self.client.table(self.table_name)
            .select("*")
            .eq("planning_unit_id", planning_unit_id)
            .eq("strategy_id", strategy_id)
            .order("version", desc=True)
            .limit(1)
            .execute()
        )
        rows = response.data or []
        return StrategyVersion.model_validate(rows[0]) if rows else None

    def get_version(self, planning_unit_id: str, strategy_id: str, version: int) -> StrategyVersion | None:
        response = (
            self.client.table(self.table_name)
            .select("*")
            .eq("planning_unit_id", planning_unit_id)
            .eq("strategy_id", strategy_id)
            .eq("version", version)
            .limit(1)
            .execute()
        )
        rows = response.data or []
        return StrategyVersion.model_validate(rows[0]) if rows else None

    def get_history(self, planning_unit_id: str, strategy_id: str) -> list[StrategyVersion]:
        response = (
            self.client.table(self.table_name)
            .select("*")
            .eq("planning_unit_id", planning_unit_id)
            .eq("strategy_id", strategy_id)
            .order("version", desc=False)
            .execute()
        )
        return [StrategyVersion.model_validate(row) for row in (response.data or [])]

    def save_version(self, version: StrategyVersion) -> StrategyVersion:
        payload = version.model_dump(mode="json", exclude_none=True)
        response = self.client.table(self.table_name).insert(payload).execute()
        rows = response.data or []
        if not rows:
            raise RuntimeError("Strategy Version insert returned no data")
        return StrategyVersion.model_validate(rows[0])
