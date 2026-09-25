from typing import Any
import time

from data.supabase import get_supabase


class FinancialDataRepository:
    """Read-only access to the existing planning-unit database model."""

    def __init__(self):
        self.db = get_supabase()

    @staticmethod
    def _execute(query: Any, retries: int = 3) -> Any:
        """Retry transient HTTP disconnects from Supabase without changing business logic."""
        for attempt in range(retries):
            try:
                return query.execute()
            except Exception as exc:
                transient = exc.__class__.__name__ in {
                    "RemoteProtocolError",
                    "ConnectError",
                    "ReadTimeout",
                    "WriteTimeout",
                }
                if not transient or attempt == retries - 1:
                    raise
                time.sleep(0.5 * (2**attempt))
        raise RuntimeError("Supabase request failed after retries")

    def _rows(self, table: str, planning_unit_id: str) -> list[dict[str, Any]]:
        result = self._execute(
            self.db.table(table)
            .select("*")
            .eq("planning_unit_id", planning_unit_id)
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
        return self._execute(
            self.db.table("asset_owners").select("*").in_("asset_id", ids)
        ).data or []

    def get_liability_responsibilities(self, planning_unit_id: str):
        liabilities = self.get_liabilities(planning_unit_id)
        ids = [row["liability_id"] for row in liabilities]
        if not ids:
            return []
        return self._execute(
            self.db.table("liability_responsibilities").select("*").in_("liability_id", ids)
        ).data or []

    def get_expense_participants(self, planning_unit_id: str):
        expenses = self.get_expenses(planning_unit_id)
        ids = [row["expense_id"] for row in expenses]
        if not ids:
            return []
        return self._execute(
            self.db.table("expense_participants").select("*").in_("expense_id", ids)
        ).data or []

    def get_insurance_policies(self, planning_unit_id: str) -> list[dict[str, Any]]:
        return self._rows("insurance_policies", planning_unit_id)

    def get_active_asset_types(self) -> list[dict[str, Any]]:
        result = self._execute(
            self.db.table("asset_type_master")
            .select("*")
            .eq("is_active", True)
        )
        return result.data or []

    def get_asset_type_master(self, active_only: bool = True) -> list[dict[str, Any]]:
        query = self.db.table("asset_type_master").select("*")
        if active_only:
            query = query.eq("is_active", True)
        result = self._execute(query)
        return result.data or []
