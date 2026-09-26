from typing import Any
import time
from data.supabase import get_supabase
from models.defined_goal import DefinedGoal, DefinedGoalAssetMapping
from schemas.goals import GoalInput


class GoalRepository:
    def __init__(self):
        self.db = get_supabase()

    @staticmethod
    def _execute(query: Any, retries: int = 3) -> Any:
        for attempt in range(retries):
            try:
                return query.execute()
            except Exception as exc:
                transient = exc.__class__.__name__ in {"RemoteProtocolError", "ConnectError", "ReadTimeout", "WriteTimeout"}
                if not transient or attempt == retries - 1:
                    raise
                time.sleep(0.5 * (2**attempt))
        raise RuntimeError("Supabase request failed after retries")

    def list_goals(self, planning_unit_id: str) -> list[dict[str, Any]]:
        res = self._execute(self.db.table("goals").select("goal_id, planning_unit_id, goal_name, target_amount, target_date, priority, flexibility").eq("planning_unit_id", planning_unit_id).order("created_at"))
        return res.data or []

    def get_planning_unit_assets(self, planning_unit_id: str) -> list[dict[str, Any]]:
        res = self._execute(self.db.table("assets").select("*").eq("planning_unit_id", planning_unit_id))
        return res.data or []

    def get_goal(self, planning_unit_id: str, goal_id: str) -> dict[str, Any] | None:
        res = self._execute(self.db.table("goals").select("*").eq("planning_unit_id", planning_unit_id).eq("goal_id", goal_id).maybe_single())
        return res.data if res else None

    def ensure_goal_record(self, planning_unit_id: str, goal_id: str | None, goal_name: str, today_cost: float, target_month: int, target_year: int, priority: str, flexibility: str) -> str:
        payload = {"planning_unit_id": planning_unit_id, "goal_name": goal_name, "target_amount": today_cost, "target_date": f"{target_year:04d}-{target_month:02d}-01", "priority": priority, "flexibility": flexibility}
        if goal_id:
            existing = self.get_goal(planning_unit_id, goal_id)
            if existing:
                self._execute(self.db.table("goals").update(payload).eq("goal_id", goal_id))
                return goal_id
        res = self._execute(self.db.table("goals").insert(payload).select("goal_id"))
        if not res.data:
            raise RuntimeError(f"Failed to insert goal record for planning unit {planning_unit_id}")
        record = res.data[0] if isinstance(res.data, list) else res.data
        return record["goal_id"]

    def get_latest_defined_goal(self, planning_unit_id: str, goal_id: str) -> DefinedGoal | None:
        res = self._execute(self.db.table("defined_goals").select("*").eq("planning_unit_id", planning_unit_id).eq("goal_id", goal_id).eq("is_latest", True).maybe_single())
        return self._hydrate_defined_goal(res.data) if res and res.data else None

    def get_defined_goal_by_version(self, planning_unit_id: str, goal_id: str, version: int) -> DefinedGoal | None:
        res = self._execute(self.db.table("defined_goals").select("*").eq("planning_unit_id", planning_unit_id).eq("goal_id", goal_id).eq("version", version).maybe_single())
        return self._hydrate_defined_goal(res.data) if res and res.data else None

    def get_all_defined_goal_versions(self, planning_unit_id: str, goal_id: str) -> list[dict[str, Any]]:
        res = self._execute(self.db.table("defined_goals").select("defined_goal_id, goal_id, version, is_latest, today_cost, future_target, projected_mapped_asset_value, funding_gap, funding_status, created_at").eq("planning_unit_id", planning_unit_id).eq("goal_id", goal_id).order("version", desc=True))
        return res.data or []

    def _hydrate_defined_goal(self, row: dict[str, Any]) -> DefinedGoal:
        maps_res = self._execute(self.db.table("defined_goal_asset_mappings").select("*").eq("defined_goal_id", row["defined_goal_id"]))
        mappings = [DefinedGoalAssetMapping(mapping_id=m.get("mapping_id"), defined_goal_id=m.get("defined_goal_id"), asset_id=m["asset_id"], asset_name=m.get("asset_name"), allocation_type=m["allocation_type"], allocation_value=float(m["allocation_value"]), allocated_amount=float(m["allocated_amount"]), allocated_percentage=float(m["allocated_percentage"]), expected_return=float(m["expected_return"]), return_frequency=m.get("return_frequency", "annual"), projected_value=float(m["projected_value"]), created_at=m.get("created_at")) for m in (maps_res.data or [])]
        metadata = row.get("version_metadata") or {}
        return DefinedGoal(defined_goal_id=row["defined_goal_id"], goal_id=row["goal_id"], planning_unit_id=row["planning_unit_id"], investor_id=row.get("investor_id"), version=row["version"], is_latest=row["is_latest"], goal_type=row["goal_type"], goal_name=row["goal_name"], today_cost=float(row["today_cost"]), inflation_rate=float(row["inflation_rate"]), inflation_source=row.get("inflation_source", "default"), target_month=int(row["target_month"]), target_year=int(row["target_year"]), duration_years=float(row["duration_years"]), future_target=float(row["future_target"]), priority=row["priority"], flexibility=row["flexibility"], status=row.get("status", "Active"), mapped_assets=mappings, projected_mapped_asset_value=float(row.get("projected_mapped_asset_value", 0.0)), funding_gap=float(row["funding_gap"]), funding_status=row["funding_status"], required_monthly_contribution=float(metadata.get("required_monthly_contribution", 0.0)), funding_return_assumption=float(metadata.get("funding_return_assumption", 0.08)), version_metadata=metadata, created_at=row.get("created_at"))

    def save_defined_goal_snapshot(self, defined_goal: DefinedGoal) -> str:
        self._execute(self.db.table("defined_goals").update({"is_latest": False}).eq("goal_id", defined_goal.goal_id).eq("planning_unit_id", defined_goal.planning_unit_id).eq("is_latest", True))
        payload = {"goal_id": defined_goal.goal_id, "planning_unit_id": defined_goal.planning_unit_id, "investor_id": defined_goal.investor_id, "version": defined_goal.version, "is_latest": True, "goal_type": defined_goal.goal_type, "goal_name": defined_goal.goal_name, "today_cost": defined_goal.today_cost, "inflation_rate": defined_goal.inflation_rate, "inflation_source": defined_goal.inflation_source, "target_month": defined_goal.target_month, "target_year": defined_goal.target_year, "duration_years": defined_goal.duration_years, "future_target": defined_goal.future_target, "priority": defined_goal.priority, "flexibility": defined_goal.flexibility, "status": defined_goal.status, "projected_mapped_asset_value": defined_goal.projected_mapped_asset_value, "funding_gap": defined_goal.funding_gap, "funding_status": defined_goal.funding_status, "version_metadata": defined_goal.version_metadata}
        res = self._execute(self.db.table("defined_goals").insert(payload).select("defined_goal_id"))
        if not res.data:
            raise RuntimeError("Failed to insert defined goal snapshot")
        def_id = (res.data[0] if isinstance(res.data, list) else res.data)["defined_goal_id"]
        if defined_goal.mapped_assets:
            self._execute(self.db.table("defined_goal_asset_mappings").insert([{"defined_goal_id": def_id, "asset_id": m.asset_id, "allocation_type": m.allocation_type, "allocation_value": m.allocation_value, "allocated_amount": m.allocated_amount, "allocated_percentage": m.allocated_percentage, "expected_return": m.expected_return, "return_frequency": m.return_frequency, "projected_value": m.projected_value} for m in defined_goal.mapped_assets]))
        return def_id

    def update_defined_goal_metadata(self, defined_goal_id: str, metadata: dict[str, Any]) -> None:
        self._execute(self.db.table("defined_goals").update({"version_metadata": metadata}).eq("defined_goal_id", defined_goal_id))

    def has_material_change(self, current: DefinedGoal, new_input: GoalInput) -> bool:
        if abs(current.today_cost - new_input.today_cost) > 0.01 or current.target_month != new_input.target_month or current.target_year != new_input.target_year:
            return True
        curr_map = {m.asset_id: (m.allocation_type, m.allocation_value) for m in current.mapped_assets}
        new_map = {m.asset_id: (m.allocation_type, m.allocation_value) for m in new_input.asset_mappings}
        if curr_map != new_map:
            return True
        return (current.version_metadata or {}).get("dynamic_details", {}) != new_input.dynamic_details
