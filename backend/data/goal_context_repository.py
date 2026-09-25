from typing import Any
from data.supabase import get_supabase


class GoalContextRepository:
    """Read-only context used to derive specialized goal inputs from existing financial data."""

    def __init__(self):
        self.db = get_supabase()

    def get_dependent(self, planning_unit_id: str, dependent_id: str) -> dict[str, Any] | None:
        res = self.db.table("dependents").select("dependent_id, name, date_of_birth, relationship").eq("planning_unit_id", planning_unit_id).eq("dependent_id", dependent_id).maybe_single().execute()
        return res.data if res and res.data else None

    def get_primary_investor(self, planning_unit_id: str) -> dict[str, Any] | None:
        res = self.db.table("investors").select("investor_id, date_of_birth").eq("planning_unit_id", planning_unit_id).order("created_at").limit(1).maybe_single().execute()
        return res.data if res and res.data else None

    def get_monthly_expenses(self, planning_unit_id: str) -> float:
        res = self.db.table("expenses").select("amount, frequency").eq("planning_unit_id", planning_unit_id).execute()
        total = 0.0
        for row in (res.data or []):
            amount = float(row.get("amount") or 0)
            frequency = str(row.get("frequency") or "monthly").lower()
            multiplier = {
                "monthly": 1.0,
                "quarterly": 1 / 3,
                "half-yearly": 1 / 6,
                "semi-annual": 1 / 6,
                "annual": 1 / 12,
                "yearly": 1 / 12,
                "weekly": 52 / 12,
                "daily": 365 / 12,
            }.get(frequency, 1.0)
            total += amount * multiplier
        return total
