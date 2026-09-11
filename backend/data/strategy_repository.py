from typing import Any
from datetime import datetime, timezone
from data.supabase import get_supabase
from models.strategy import InvestorPriorities, Scenario, StrategyDefinition, StrategyRankingItem, StrategyRecommendation, StrategyRun, StrategyArchitecture


class StrategyRepository:
    def __init__(self):
        self.db = get_supabase()

    def get_latest_run(self, planning_unit_id: str, goal_id: str) -> StrategyRun | None:
        res = self.db.table("strategy_runs").select("*").eq("planning_unit_id", planning_unit_id).eq("goal_id", goal_id).eq("is_latest", True).maybe_single().execute()
        return self._hydrate_run(res.data) if res and res.data else None

    def get_run_by_id(self, planning_unit_id: str, strategy_run_id: str) -> StrategyRun | None:
        res = self.db.table("strategy_runs").select("*").eq("planning_unit_id", planning_unit_id).eq("strategy_run_id", strategy_run_id).maybe_single().execute()
        return self._hydrate_run(res.data) if res and res.data else None

    def get_run_history(self, planning_unit_id: str, goal_id: str) -> list[dict[str, Any]]:
        res = self.db.table("strategy_runs").select("strategy_run_id, goal_id, defined_goal_version, run_version, is_latest, status, selected_strategy_id, selected_scenario_id, selected_strategy_version_id, selected_strategy_version, created_at").eq("planning_unit_id", planning_unit_id).eq("goal_id", goal_id).order("run_version", desc=True).execute()
        return res.data or []

    def save_run(self, run: StrategyRun) -> str:
        self.db.table("strategy_runs").update({"is_latest": False}).eq("planning_unit_id", run.planning_unit_id).eq("goal_id", run.goal_id).eq("is_latest", True).execute()
        metadata = {**run.run_metadata, "architectures": [a.model_dump() for a in run.architectures], "selected_architecture": run.selected_architecture.model_dump() if run.selected_architecture else None, "approval_status": run.approval_status}
        payload = {
            "planning_unit_id": run.planning_unit_id, "goal_id": run.goal_id, "defined_goal_id": run.defined_goal_id, "defined_goal_version": run.defined_goal_version,
            "run_version": run.run_version, "is_latest": True, "status": run.status, "investor_priorities": run.investor_priorities.model_dump(),
            "applicable_strategies": [s.model_dump() for s in run.applicable_strategies], "scenarios": [sc.model_dump() for sc in run.scenarios],
            "comparison_snapshot": run.comparison_matrix, "ranking_snapshot": [r.model_dump() for r in run.rankings], "recommendation": run.recommendation.model_dump(),
            "selected_strategy_id": run.selected_strategy_id, "selected_scenario_id": run.selected_scenario_id,
            "selected_strategy_version_id": run.run_metadata.get("selected_strategy_version_id"), "selected_strategy_version": run.run_metadata.get("selected_strategy_version"),
            "selected_implementation_parameters": run.selected_implementation_parameters, "selection_timestamp": run.selection_timestamp,
            "run_metadata": metadata,
        }
        res = self.db.table("strategy_runs").insert(payload).select("strategy_run_id").execute()
        if not res.data:
            raise RuntimeError("Failed to insert strategy run")
        record = res.data[0] if isinstance(res.data, list) else res.data
        custom_rows = [{"strategy_run_id": record["strategy_run_id"], "strategy_id": sc.strategy_id, "scenario_type": sc.scenario_type, "scenario_name": sc.scenario_name, "assumptions": sc.assumptions, "funding_structure": sc.funding_structure, "metrics": sc.metrics, "is_investor_modified": sc.is_investor_modified} for sc in run.scenarios if sc.is_investor_modified or sc.scenario_type == "custom"]
        if custom_rows:
            self.db.table("strategy_scenarios").insert(custom_rows).execute()
        return record["strategy_run_id"]

    def update_selection(self, planning_unit_id: str, strategy_run_id: str, selected_strategy_id: str, selected_scenario_id: str, selected_params: dict[str, Any], selected_architecture: StrategyArchitecture | None = None, approval_status: str = "selected", selected_strategy_version_id: str | None = None, selected_strategy_version: int | None = None) -> None:
        metadata = {"selected_architecture": selected_architecture.model_dump() if selected_architecture else None, "approval_status": approval_status}
        if selected_strategy_version_id is not None:
            metadata["selected_strategy_version_id"] = selected_strategy_version_id
        if selected_strategy_version is not None:
            metadata["selected_strategy_version"] = selected_strategy_version
        payload = {
            "selected_strategy_id": selected_strategy_id, "selected_scenario_id": selected_scenario_id,
            "selected_strategy_version_id": selected_strategy_version_id, "selected_strategy_version": selected_strategy_version,
            "selected_implementation_parameters": selected_params,
            "selection_timestamp": datetime.now(timezone.utc).isoformat(), "run_metadata": metadata,
        }
        self.db.table("strategy_runs").update(payload).eq("planning_unit_id", planning_unit_id).eq("strategy_run_id", strategy_run_id).execute()

    def update_approval(self, planning_unit_id: str, strategy_run_id: str, decision: str) -> None:
        run = self.get_run_by_id(planning_unit_id, strategy_run_id)
        if not run:
            raise ValueError("Strategy run not found")
        status = "approved" if decision == "approve" else "rejected"
        metadata = dict(run.run_metadata)
        metadata["approval_status"] = status
        self.db.table("strategy_runs").update({"status": "active" if status == "approved" else "completed", "run_metadata": metadata}).eq("planning_unit_id", planning_unit_id).eq("strategy_run_id", strategy_run_id).execute()

    def _hydrate_run(self, row: dict[str, Any]) -> StrategyRun:
        priorities = InvestorPriorities(**(row.get("investor_priorities") or {}))
        applicable = [StrategyDefinition(**s) for s in (row.get("applicable_strategies") or [])]
        scenarios = [Scenario(**sc) for sc in (row.get("scenarios") or [])]
        rankings = [StrategyRankingItem(**r) for r in (row.get("ranking_snapshot") or [])]
        rec = StrategyRecommendation(**(row.get("recommendation") or {}))
        metadata = row.get("run_metadata") or {}
        architectures = [StrategyArchitecture(**a) for a in metadata.get("architectures", [])]
        selected_architecture = metadata.get("selected_architecture")
        return StrategyRun(
            strategy_run_id=row["strategy_run_id"], planning_unit_id=row["planning_unit_id"], goal_id=row["goal_id"], defined_goal_id=row["defined_goal_id"],
            defined_goal_version=row["defined_goal_version"], run_version=row["run_version"], is_latest=row["is_latest"], status=row.get("status", "completed"),
            applicable_strategies=applicable, scenarios=scenarios, investor_priorities=priorities, comparison_matrix=row.get("comparison_snapshot") or {},
            rankings=rankings, recommendation=rec, architectures=architectures, selected_strategy_id=row.get("selected_strategy_id"), selected_scenario_id=row.get("selected_scenario_id"),
            selected_implementation_parameters=row.get("selected_implementation_parameters") or {}, selected_architecture=StrategyArchitecture(**selected_architecture) if selected_architecture else None,
            approval_status=metadata.get("approval_status", "not_selected"), selection_timestamp=row.get("selection_timestamp"), run_metadata=metadata, created_at=row.get("created_at"),
        )
