from datetime import datetime, timezone
from typing import Any
from data.supabase import get_supabase
from models.strategy import (
    InvestorPriorities,
    Scenario,
    StrategyDefinition,
    StrategyRankingItem,
    StrategyRecommendation,
    StrategyRun,
)


class StrategyRepository:
    def __init__(self):
        self.db = get_supabase()

    def get_latest_run(self, planning_unit_id: str, goal_id: str) -> StrategyRun | None:
        res = (
            self.db.table("strategy_runs")
            .select("*")
            .eq("planning_unit_id", planning_unit_id)
            .eq("goal_id", goal_id)
            .eq("is_latest", True)
            .maybe_single()
            .execute()
        )
        if not res or not res.data:
            return None
        return self._hydrate_run(res.data)

    def get_run_by_id(self, planning_unit_id: str, strategy_run_id: str) -> StrategyRun | None:
        res = (
            self.db.table("strategy_runs")
            .select("*")
            .eq("planning_unit_id", planning_unit_id)
            .eq("strategy_run_id", strategy_run_id)
            .maybe_single()
            .execute()
        )
        if not res or not res.data:
            return None
        return self._hydrate_run(res.data)

    def get_run_history(self, planning_unit_id: str, goal_id: str) -> list[dict[str, Any]]:
        res = (
            self.db.table("strategy_runs")
            .select("strategy_run_id, goal_id, defined_goal_version, run_version, is_latest, status, selected_strategy_id, selected_scenario_id, created_at")
            .eq("planning_unit_id", planning_unit_id)
            .eq("goal_id", goal_id)
            .order("run_version", desc=True)
            .execute()
        )
        return res.data or []

    def save_run(self, run: StrategyRun) -> str:
        # Clear previous latest
        (
            self.db.table("strategy_runs")
            .update({"is_latest": False})
            .eq("planning_unit_id", run.planning_unit_id)
            .eq("goal_id", run.goal_id)
            .eq("is_latest", True)
            .execute()
        )

        payload = {
            "planning_unit_id": run.planning_unit_id,
            "goal_id": run.goal_id,
            "defined_goal_id": run.defined_goal_id,
            "defined_goal_version": run.defined_goal_version,
            "run_version": run.run_version,
            "is_latest": True,
            "status": run.status,
            "investor_priorities": run.investor_priorities.model_dump(),
            "applicable_strategies": [s.model_dump() for s in run.applicable_strategies],
            "scenarios": [sc.model_dump() for sc in run.scenarios],
            "comparison_snapshot": run.comparison_matrix,
            "ranking_snapshot": [r.model_dump() for r in run.rankings],
            "recommendation": run.recommendation.model_dump(),
            "selected_strategy_id": run.selected_strategy_id,
            "selected_scenario_id": run.selected_scenario_id,
            "selected_implementation_parameters": run.selected_implementation_parameters,
            "selection_timestamp": run.selection_timestamp,
            "run_metadata": run.run_metadata,
        }

        res = self.db.table("strategy_runs").insert(payload).select("strategy_run_id").execute()
        if not res.data:
            raise RuntimeError("Failed to insert strategy run")
        record = res.data[0] if isinstance(res.data, list) else res.data
        run_id = record["strategy_run_id"]

        # Persist custom/modified scenarios separately
        custom_rows = [
            {
                "strategy_run_id": run_id,
                "strategy_id": sc.strategy_id,
                "scenario_type": sc.scenario_type,
                "scenario_name": sc.scenario_name,
                "assumptions": sc.assumptions,
                "funding_structure": sc.funding_structure,
                "metrics": sc.metrics,
                "is_investor_modified": sc.is_investor_modified,
            }
            for sc in run.scenarios
            if sc.is_investor_modified or sc.scenario_type == "custom"
        ]
        if custom_rows:
            self.db.table("strategy_scenarios").insert(custom_rows).execute()

        return run_id

    def update_selection(
        self,
        planning_unit_id: str,
        strategy_run_id: str,
        selected_strategy_id: str,
        selected_scenario_id: str,
        selected_params: dict[str, Any],
    ) -> None:
        now_iso = datetime.now(timezone.utc).isoformat()
        payload = {
            "selected_strategy_id": selected_strategy_id,
            "selected_scenario_id": selected_scenario_id,
            "selected_implementation_parameters": selected_params,
            "selection_timestamp": now_iso,
        }
        self.db.table("strategy_runs").update(payload).eq("planning_unit_id", planning_unit_id).eq("strategy_run_id", strategy_run_id).execute()

    def _hydrate_run(self, row: dict[str, Any]) -> StrategyRun:
        priorities_raw = row.get("investor_priorities") or {}
        priorities = InvestorPriorities(**priorities_raw) if priorities_raw else InvestorPriorities()

        applicable_strats = [StrategyDefinition(**s) for s in (row.get("applicable_strategies") or [])]
        scenarios = [Scenario(**sc) for sc in (row.get("scenarios") or [])]
        rankings = [StrategyRankingItem(**r) for r in (row.get("ranking_snapshot") or [])]
        rec = StrategyRecommendation(**(row.get("recommendation") or {}))

        return StrategyRun(
            strategy_run_id=row["strategy_run_id"],
            planning_unit_id=row["planning_unit_id"],
            goal_id=row["goal_id"],
            defined_goal_id=row["defined_goal_id"],
            defined_goal_version=row["defined_goal_version"],
            run_version=row["run_version"],
            is_latest=row["is_latest"],
            status=row.get("status", "completed"),
            applicable_strategies=applicable_strats,
            scenarios=scenarios,
            investor_priorities=priorities,
            comparison_matrix=row.get("comparison_snapshot") or {},
            rankings=rankings,
            recommendation=rec,
            selected_strategy_id=row.get("selected_strategy_id"),
            selected_scenario_id=row.get("selected_scenario_id"),
            selected_implementation_parameters=row.get("selected_implementation_parameters") or {},
            selection_timestamp=row.get("selection_timestamp"),
            run_metadata=row.get("run_metadata") or {},
            created_at=row.get("created_at"),
        )
