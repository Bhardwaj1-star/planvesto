from typing import Any

from data.supabase import get_supabase


class FinancialDataRepository:
    """Read-only access to the existing planning-unit database model."""

    def __init__(self):
        self.db = get_supabase()

    def _rows(self, table: str, planning_unit_id: str) -> list[dict[str, Any]]:
        result = (
            self.db.table(table)
            .select("*")
            .eq("planning_unit_id", planning_unit_id)
            .execute()
        )
        return result.data or []

    def get_investors(self, planning_unit_id: str):
        return self._rows("investors", planning_unit_id)

    def get_income(self, planning_unit_id: str):
        return self._rows("income", planning_unit_id)

    def get_expenses(self, planning_unit_id: str):
        return self._rows("expenses", planning_unit_id)

    def get_assets(self, planning_unit_id: str):
        return self._rows("assets", planning_unit_id)

    def get_liabilities(self, planning_unit_id: str):
        return self._rows("liabilities", planning_unit_id)

    def get_asset_owners(self, planning_unit_id: str):
        assets = self.get_assets(planning_unit_id)
        ids = [row["asset_id"] for row in assets]
        if not ids:
            return []
        return self.db.table("asset_owners").select("*").in_("asset_id", ids).execute().data or []

    def get_liability_responsibilities(self, planning_unit_id: str):
        liabilities = self.get_liabilities(planning_unit_id)
        ids = [row["liability_id"] for row in liabilities]
        if not ids:
            return []
        return self.db.table("liability_responsibilities").select("*").in_("liability_id", ids).execute().data or []

    def get_expense_participants(self, planning_unit_id: str):
        expenses = self.get_expenses(planning_unit_id)
        ids = [row["expense_id"] for row in expenses]
        if not ids:
            return []
        return self.db.table("expense_participants").select("*").in_("expense_id", ids).execute().data or []

    def get_insurance_policies(self, planning_unit_id: str) -> list[dict[str, Any]]:
        return self._rows("insurance_policies", planning_unit_id)

