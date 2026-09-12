from fastapi import HTTPException

from data.financial_data import FinancialDataRepository
from data.financial_state_repository import FinancialStateSnapshotRepository
from engines.financial_state.engine import FinancialStateEngine


class FinancialStateService:
    def __init__(self):
        self.repository = FinancialDataRepository()
        self.snapshot_repository = FinancialStateSnapshotRepository()
        self.engine = FinancialStateEngine()

    def build(self, planning_unit_id: str, scope: str = "family", investor_id: str | None = None):
        if scope == "individual" and not investor_id:
            raise HTTPException(status_code=400, detail="investor_id is required for individual scope")
        investors = self.repository.get_investors(planning_unit_id)
        if scope == "individual" and not any(r.get("investor_id") == investor_id for r in investors):
            raise HTTPException(status_code=404, detail="Investor not found in planning unit")
        financial_state = self.engine.build(
            planning_unit_id=planning_unit_id,
            investors=investors,
            income_rows=self.repository.get_income(planning_unit_id),
            expense_rows=self.repository.get_expenses(planning_unit_id),
            asset_rows=self.repository.get_assets(planning_unit_id),
            liability_rows=self.repository.get_liabilities(planning_unit_id),
            asset_owner_rows=self.repository.get_asset_owners(planning_unit_id),
            liability_responsibility_rows=self.repository.get_liability_responsibilities(planning_unit_id),
            expense_participant_rows=self.repository.get_expense_participants(planning_unit_id),
            scope=scope,
            investor_id=investor_id,
        )
        self.snapshot_repository.save_snapshot(
            planning_unit_id=planning_unit_id,
            scope=scope,
            investor_id=investor_id,
            financial_state=financial_state.model_dump(mode="json"),
        )
        return financial_state
