from typing import Any

from models.financial_state import FinancialState
from models.moneywheel import MoneywheelInput


class MoneywheelFinancialStateAdapter:
    """Maps authoritative FinancialState fields into Moneywheel inputs."""

    def build(
        self,
        financial_state: FinancialState,
    ) -> MoneywheelInput:
        return MoneywheelInput(
            planning_unit_id=financial_state.planning_unit_id,
            gross_monthly_income=financial_state.income_monthly.value,
            monthly_surplus=financial_state.investable_surplus_monthly.value,
            monthly_expenses=financial_state.expenses_monthly.value,
            essential_monthly_expenses=financial_state.essential_monthly_expenses.value,
            liquid_assets=financial_state.liquid_assets.value,
            monthly_debt_payments=financial_state.emi_burden_monthly.value,
            total_assets=financial_state.total_assets.value,
            total_liabilities=financial_state.total_liabilities.value,
            financial_assets=financial_state.financial_assets.value,
        )

    @staticmethod
    def snapshot(financial_state: FinancialState) -> dict[str, Any]:
        return financial_state.model_dump(mode="json")
