from typing import Any
from data.supabase import get_supabase
from models.goal_funding import GoalFundingAssessment


class GoalFundingRepository:
    def __init__(self):
        self.db = get_supabase()

    def save(self, assessment: GoalFundingAssessment) -> GoalFundingAssessment:
        latest = (
            self.db.table("goal_funding_assessments")
            .select("version")
            .eq("planning_unit_id", assessment.planning_unit_id)
            .eq("goal_id", assessment.goal_id)
            .order("version", desc=True)
            .limit(1)
            .execute()
        )
        rows = latest.data or []
        assessment.version = int(rows[0]["version"]) + 1 if rows else 1
        payload = assessment.model_dump(mode="json", exclude_none=True)
        payload.pop("assessment_id", None)
        payload.pop("created_at", None)
        response = self.db.table("goal_funding_assessments").insert(payload).select("*").execute()
        if not response.data:
            raise RuntimeError("Goal Funding assessment could not be saved")
        row = response.data[0] if isinstance(response.data, list) else response.data
        return GoalFundingAssessment.model_validate(row)

    def get_latest(self, planning_unit_id: str, goal_id: str) -> GoalFundingAssessment | None:
        response = (
            self.db.table("goal_funding_assessments")
            .select("*")
            .eq("planning_unit_id", planning_unit_id)
            .eq("goal_id", goal_id)
            .order("version", desc=True)
            .limit(1)
            .execute()
        )
        rows = response.data or []
        return GoalFundingAssessment.model_validate(rows[0]) if rows else None

    def list_history(self, planning_unit_id: str, goal_id: str) -> list[dict[str, Any]]:
        response = (
            self.db.table("goal_funding_assessments")
            .select("assessment_id, goal_id, defined_goal_version, version, status, investor_decision, investor_decision_confirmed, created_at")
            .eq("planning_unit_id", planning_unit_id)
            .eq("goal_id", goal_id)
            .order("version", desc=True)
            .execute()
        )
        return response.data or []
