from typing import Any
from data.supabase import get_supabase
from models.strategy import InvestorPriorities, Scenario, StrategyDefinition, StrategyRankingItem, StrategyRecommendation, StrategyRun, StrategyArchitecture
from models.strategy_version import StrategyVersion


class StrategyRepository:
    def __init__(self):
        self.db = get_supabase()

    def get_selected_strategy_version(self, planning_unit_id: str, goal_id: str) -> StrategyVersion | None:
        """Resolve the explicit, current goal selection and reject stale goal bindings."""
        res = (
            self.db.table("goal_strategy_selections")
            .select("defined_goal_id, defined_goal_version, strategy_version_id")
            .eq("planning_unit_id", planning_unit_id)
            .eq("goal_id", goal_id)
            .maybe_single()
            .execute()
        )
        selection = res.data if res else None
        if not selection:
            return None

        latest_goal = (
            self.db.table("defined_goals")
            .select("defined_goal_id, version")
            .eq("planning_unit_id", planning_unit_id)
            .eq("goal_id", goal_id)
            .eq("is_latest", True)
            .maybe_single()
            .execute()
        )
        current_goal = latest_goal.data if latest_goal else None
        if (
            not current_goal
            or current_goal.get("defined_goal_id") != selection.get("defined_goal_id")
            or current_goal.get("version") != selection.get("defined_goal_version")
        ):
            return None

        version_result = (
            self.db.table("strategy_versions")
            .select("*")
            .eq("planning_unit_id", planning_unit_id)
            .eq("strategy_version_id", selection["strategy_version_id"])
            .maybe_single()
            .execute()
        )
        version_row = version_result.data if version_result else None
        decision_snapshot = (version_row or {}).get("decision_snapshot") or {}
        recommendation = decision_snapshot.get("recommendation") or {}
        if (
            not version_row
            or version_row.get("goal_id") != goal_id
            or version_row.get("defined_goal_id") != selection.get("defined_goal_id")
            or version_row.get("defined_goal_version") != selection.get("defined_goal_version")
            or not version_row.get("source_strategy_run_id")
            or not version_row.get("architecture")
            or recommendation.get("recommended_strategy_id") != version_row.get("strategy_id")
            or recommendation.get("recommended_scenario_id")
            != decision_snapshot.get("selected_scenario_id")
            or not any(
                row.get("scenario_id") == decision_snapshot.get("selected_scenario_id")
                for row in decision_snapshot.get("scenarios", [])
                if isinstance(row, dict)
            )
        ):
            return None
        return StrategyVersion.model_validate(version_row)

    def get_selected_strategy_version_id(self, planning_unit_id: str, goal_id: str) -> str | None:
        version = self.get_selected_strategy_version(planning_unit_id, goal_id)
        return version.strategy_version_id if version else None

    def set_selected_strategy_version(self, version: StrategyVersion) -> None:
        if not version.strategy_version_id or not version.goal_id or not version.defined_goal_id or not version.defined_goal_version:
            raise ValueError("A selected StrategyVersion must be bound to its Goal and DefinedGoal version")
        current_goal = (
            self.db.table("defined_goals")
            .select("defined_goal_id, version")
            .eq("planning_unit_id", version.planning_unit_id)
            .eq("goal_id", version.goal_id)
            .eq("is_latest", True)
            .maybe_single()
            .execute()
        )
        row = current_goal.data if current_goal else None
        if (
            not row
            or row.get("defined_goal_id") != version.defined_goal_id
            or row.get("version") != version.defined_goal_version
        ):
            raise ValueError("Cannot select a StrategyVersion for a stale DefinedGoal version")
        snapshot = version.decision_snapshot
        recommendation = snapshot.get("recommendation", {})
        if (
            version.architecture is None
            or not version.source_strategy_run_id
            or recommendation.get("recommended_strategy_id") != version.strategy_id
            or recommendation.get("recommended_scenario_id")
            != snapshot.get("selected_scenario_id")
            or not any(
                row.get("scenario_id") == snapshot.get("selected_scenario_id")
                for row in snapshot.get("scenarios", [])
                if isinstance(row, dict)
            )
        ):
            raise ValueError("A selected StrategyVersion must include its finalized strategy and architecture snapshot")
        self.db.table("goal_strategy_selections").upsert({
            "planning_unit_id": version.planning_unit_id,
            "goal_id": version.goal_id,
            "defined_goal_id": version.defined_goal_id,
            "defined_goal_version": version.defined_goal_version,
            "strategy_version_id": version.strategy_version_id,
        }, on_conflict="planning_unit_id,goal_id").execute()

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
        metadata = {**run.run_metadata, "architectures": [a.model_dump() for a in run.architectures], "selected_architecture": run.selected_architecture.model_dump() if run.selected_architecture else None, "what_if_scenarios": [s.model_dump() for s in run.what_if_scenarios]}
        payload = {
            "planning_unit_id": run.planning_unit_id, "goal_id": run.goal_id, "defined_goal_id": run.defined_goal_id, "defined_goal_version": run.defined_goal_version,
            "run_version": run.run_version, "is_latest": True, "status": run.status, "investor_priorities": run.investor_priorities.model_dump(),
            "applicable_strategies": [s.model_dump() for s in run.applicable_strategies], "scenarios": [sc.model_dump() for sc in run.scenarios],
            "comparison_snapshot": run.comparison_matrix, "ranking_snapshot": [r.model_dump() for r in run.rankings], "recommendation": run.recommendation.model_dump(),
            "selected_strategy_id": run.selected_strategy_id, "selected_scenario_id": run.selected_scenario_id,
            "selected_strategy_version_id": run.selected_strategy_version_id, "selected_strategy_version": run.selected_strategy_version,
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

    def update_architectures(self, planning_unit_id: str, strategy_run_id: str, architectures: list[StrategyArchitecture], selected_architecture: StrategyArchitecture | None = None) -> None:
        existing = self.db.table("strategy_runs").select("run_metadata").eq(
            "planning_unit_id", planning_unit_id
        ).eq("strategy_run_id", strategy_run_id).maybe_single().execute()
        metadata = dict((existing.data or {}).get("run_metadata") or {}) if existing and existing.data else {}
        metadata["architectures"] = [architecture.model_dump() for architecture in architectures]
        if selected_architecture is not None:
            metadata["selected_architecture"] = selected_architecture.model_dump()
        self.db.table("strategy_runs").update({"run_metadata": metadata}).eq(
            "planning_unit_id", planning_unit_id
        ).eq("strategy_run_id", strategy_run_id).execute()

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
            selected_strategy_version_id=row.get("selected_strategy_version_id") or metadata.get("selected_strategy_version_id"),
            selected_strategy_version=row.get("selected_strategy_version") if row.get("selected_strategy_version") is not None else metadata.get("selected_strategy_version"),
            what_if_scenarios=[Scenario(**sc) for sc in metadata.get("what_if_scenarios", [])], selected_implementation_parameters=row.get("selected_implementation_parameters") or {}, selected_architecture=StrategyArchitecture(**selected_architecture) if selected_architecture else None,
            selection_timestamp=row.get("selection_timestamp"), run_metadata=metadata, created_at=row.get("created_at"),
        )
