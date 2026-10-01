import logging
from datetime import date, datetime
from typing import Any
from fastapi import HTTPException
from data.goal_repository import GoalRepository
from data.financial_state_repository import FinancialStateSnapshotRepository
from data.supabase import get_supabase
from engines.goal.engine import GoalEngine
from models.defined_goal import DefinedGoal, DefinedGoalVersionSummary
from schemas.goals import GoalInput, GoalCalculateRequest

logger = logging.getLogger(__name__)


class GoalService:
    def __init__(self):
        self.repository = GoalRepository()
        self.financial_state_repository = FinancialStateSnapshotRepository()
        self.engine = GoalEngine()

    def _get_assets_lookup(self, planning_unit_id: str) -> dict[str, dict[str, Any]]:
        rows = self.repository.get_planning_unit_assets(planning_unit_id)
        return {r["asset_id"]: r for r in rows}

    def _enrich_retirement_context(self, request: GoalInput | GoalCalculateRequest) -> None:
        if request.goal_type != "Retirement / Financial Freedom":
            return
        details = dict(request.dynamic_details or {})
        if details.get("currentAge") is not None or details.get("current_age") is not None:
            return

        query = get_supabase().table("investors").select("date_of_birth").eq("planning_unit_id", request.planning_unit_id).limit(1).execute()
        row = (query.data or [None])[0]
        dob_value = row.get("date_of_birth") if row else None
        if not dob_value:
            raise ValueError("Retirement planning requires the investor date of birth in Personal Information")

        try:
            dob = datetime.fromisoformat(str(dob_value)).date()
        except ValueError:
            dob = date.fromisoformat(str(dob_value))

        today = date.today()
        current_age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        details["currentAge"] = current_age
        request.dynamic_details = details

    @staticmethod
    def _metric_value(state: dict[str, Any], key: str):
        value = state.get(key)
        if isinstance(value, dict):
            return value.get("value")
        if hasattr(value, "value"):
            return value.value
        return value

    def _apply_feasibility(self, defined_goal: DefinedGoal) -> DefinedGoal:
        """Assess whether the goal's required contribution fits current surplus.

        This is a planning feasibility check, not a strategy or product decision.
        The financial-state snapshot is the source of the available surplus.
        """
        row = self.financial_state_repository.get_latest(defined_goal.planning_unit_id, "family")
        state = row.get("financial_state") if row else None
        if hasattr(state, "model_dump"):
            state = state.model_dump()
        if not isinstance(state, dict):
            defined_goal.feasibility_status = "unknown"
            defined_goal.feasibility_reason = "Current financial surplus is unavailable."
            defined_goal.version_metadata["goal_feasibility"] = {
                "status": "unknown",
                "reason": defined_goal.feasibility_reason,
            }
            return defined_goal

        surplus = self._metric_value(state, "investable_surplus_monthly")
        if surplus is None:
            defined_goal.feasibility_status = "unknown"
            defined_goal.feasibility_reason = "Monthly investable surplus is unavailable."
            defined_goal.version_metadata["goal_feasibility"] = {
                "status": "unknown",
                "reason": defined_goal.feasibility_reason,
            }
            return defined_goal

        surplus = max(0.0, float(surplus))
        required = max(0.0, float(defined_goal.required_monthly_contribution))
        contribution_gap = round(required - surplus, 2)
        defined_goal.available_monthly_surplus = surplus
        defined_goal.monthly_contribution_surplus_gap = contribution_gap

        if defined_goal.funding_gap <= 0:
            status = "feasible"
            reason = "The mapped assets already cover the target-date requirement."
        elif required <= surplus:
            status = "feasible"
            reason = "The required monthly contribution fits within the current investable surplus."
        elif surplus > 0:
            status = "constrained"
            reason = "The goal requires a higher monthly contribution than the current investable surplus."
        else:
            status = "infeasible"
            reason = "There is currently no investable monthly surplus available for the funding gap."

        defined_goal.feasibility_status = status
        defined_goal.feasibility_reason = reason
        defined_goal.version_metadata["goal_feasibility"] = {
            "status": status,
            "available_monthly_surplus": surplus,
            "required_monthly_contribution": required,
            "monthly_contribution_surplus_gap": contribution_gap,
            "reason": reason,
        }
        return defined_goal

    def calculate_preview(self, request: GoalCalculateRequest) -> DefinedGoal:
        self._enrich_retirement_context(request)
        assets_lookup = self._get_assets_lookup(request.planning_unit_id)
        defined_goal = self.engine.calculate_defined_goal(goal_input=request, assets_lookup=assets_lookup, version=1, is_latest=True)
        return self._apply_feasibility(defined_goal)

    def save_and_define_goal(self, request: GoalInput) -> DefinedGoal:
        self._enrich_retirement_context(request)
        goal_id = self.repository.ensure_goal_record(
            planning_unit_id=request.planning_unit_id,
            goal_id=request.goal_id,
            goal_name=request.goal_name,
            today_cost=request.today_cost,
            target_month=request.target_month,
            target_year=request.target_year,
            priority=request.priority,
            flexibility=request.flexibility,
        )
        request.goal_id = goal_id

        current_latest = self.repository.get_latest_defined_goal(planning_unit_id=request.planning_unit_id, goal_id=goal_id)
        assets_lookup = self._get_assets_lookup(request.planning_unit_id)

        if current_latest is None:
            new_version, is_material = 1, True
        else:
            is_material = self.repository.has_material_change(current_latest, request)
            if not is_material and current_latest.status == request.status and current_latest.priority == request.priority and current_latest.flexibility == request.flexibility:
                return self._apply_feasibility(current_latest)
            new_version = current_latest.version + 1

        defined_goal = self.engine.calculate_defined_goal(
            goal_input=request,
            assets_lookup=assets_lookup,
            version=new_version,
            is_latest=True,
        )
        defined_goal = self._apply_feasibility(defined_goal)
        def_id = self.repository.save_defined_goal_snapshot(defined_goal)
        defined_goal.defined_goal_id = def_id

        if is_material and new_version > 1:
            try:
                from services.strategy_service import StrategyService
                StrategyService().on_defined_goal_updated(
                    planning_unit_id=request.planning_unit_id,
                    goal_id=goal_id,
                    new_defined_goal=defined_goal,
                )
                defined_goal.version_metadata["strategy_recalculation"] = "succeeded"
                self.repository.update_defined_goal_metadata(def_id, defined_goal.version_metadata)
            except Exception as exc:
                logger.error("Automatic strategy recalculation failed for goal %s (version %d): %s", goal_id, new_version, exc, exc_info=True)
                defined_goal.version_metadata["strategy_recalculation"] = "failed"
                defined_goal.version_metadata["strategy_recalculation_error"] = str(exc)
                self.repository.update_defined_goal_metadata(def_id, defined_goal.version_metadata)
        return defined_goal

    def get_latest_defined_goal(self, planning_unit_id: str, goal_id: str) -> DefinedGoal:
        goal = self.repository.get_latest_defined_goal(planning_unit_id, goal_id)
        if not goal:
            raise HTTPException(status_code=404, detail="DefinedGoal not found for this goal")
        return goal

    def get_defined_goal_version(self, planning_unit_id: str, goal_id: str, version: int) -> DefinedGoal:
        goal = self.repository.get_defined_goal_by_version(planning_unit_id, goal_id, version)
        if not goal:
            raise HTTPException(status_code=404, detail=f"DefinedGoal version {version} not found")
        return goal

    def get_version_history(self, planning_unit_id: str, goal_id: str) -> list[DefinedGoalVersionSummary]:
        rows = self.repository.get_all_defined_goal_versions(planning_unit_id, goal_id)
        return [
            DefinedGoalVersionSummary(
                defined_goal_id=r["defined_goal_id"], goal_id=r["goal_id"], version=r["version"], is_latest=r["is_latest"],
                today_cost=float(r["today_cost"]), future_target=float(r["future_target"]),
                projected_mapped_asset_value=float(r.get("projected_mapped_asset_value", 0.0)), funding_gap=float(r["funding_gap"]),
                funding_status=r["funding_status"], feasibility_status=(r.get("version_metadata") or {}).get("goal_feasibility", {}).get("status", "unknown"), feasibility_reason=(r.get("version_metadata") or {}).get("goal_feasibility", {}).get("reason"), created_at=r["created_at"],
            ) for r in rows
        ]
