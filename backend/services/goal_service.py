from typing import Any
from fastapi import HTTPException
from data.goal_repository import GoalRepository
from engines.goal.engine import GoalEngine
from models.defined_goal import DefinedGoal, DefinedGoalVersionSummary
from schemas.goals import GoalInput, GoalCalculateRequest


class GoalService:
    def __init__(self):
        self.repository = GoalRepository()
        self.engine = GoalEngine()

    def _get_assets_lookup(self, planning_unit_id: str) -> dict[str, dict[str, Any]]:
        rows = self.repository.get_planning_unit_assets(planning_unit_id)
        return {r["asset_id"]: r for r in rows}

    def calculate_preview(self, request: GoalCalculateRequest) -> DefinedGoal:
        assets_lookup = self._get_assets_lookup(request.planning_unit_id)
        return self.engine.calculate_defined_goal(
            goal_input=request,
            assets_lookup=assets_lookup,
            version=1,
            is_latest=True,
        )

    def save_and_define_goal(self, request: GoalInput) -> DefinedGoal:
        # 1. Ensure primary goal entity
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

        # 2. Check existing latest DefinedGoal
        current_latest = self.repository.get_latest_defined_goal(
            planning_unit_id=request.planning_unit_id,
            goal_id=goal_id,
        )

        assets_lookup = self._get_assets_lookup(request.planning_unit_id)

        if current_latest is None:
            new_version = 1
            is_material = True
        else:
            is_material = self.repository.has_material_change(current_latest, request)
            if not is_material and current_latest.status == request.status and current_latest.priority == request.priority and current_latest.flexibility == request.flexibility:
                return current_latest
            new_version = current_latest.version + 1

        # 3. Calculate new DefinedGoal
        defined_goal = self.engine.calculate_defined_goal(
            goal_input=request,
            assets_lookup=assets_lookup,
            version=new_version,
            is_latest=True,
        )

        # 4. Persist snapshot
        def_id = self.repository.save_defined_goal_snapshot(defined_goal)
        defined_goal.defined_goal_id = def_id

        # 5. Trigger Strategy recalculation if material change occurred
        if is_material and new_version > 1:
            try:
                from services.strategy_service import StrategyService
                StrategyService().on_defined_goal_updated(
                    planning_unit_id=request.planning_unit_id,
                    goal_id=goal_id,
                    new_defined_goal=defined_goal,
                )
            except Exception:
                # Logging / graceful fallback so goal save succeeds
                pass

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
                defined_goal_id=r["defined_goal_id"],
                goal_id=r["goal_id"],
                version=r["version"],
                is_latest=r["is_latest"],
                today_cost=float(r["today_cost"]),
                future_target=float(r["future_target"]),
                projected_mapped_asset_value=float(r.get("projected_mapped_asset_value", 0.0)),
                funding_gap=float(r["funding_gap"]),
                funding_status=r["funding_status"],
                created_at=r["created_at"],
            )
            for r in rows
        ]
