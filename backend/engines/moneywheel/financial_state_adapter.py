from typing import Any

from models.financial_state import FinancialState
from models.moneywheel import MoneywheelInput


class MoneywheelFinancialStateAdapter:
    """Maps authoritative FinancialState fields into Moneywheel inputs.

    Fields whose semantics are not yet represented by FinancialState remain
    explicit optional inputs rather than being inferred from unrelated data.
    """

    def build(
        self,
        financial_state: FinancialState,
        *,
        essential_monthly_expenses: float | None = None,
        liquid_assets: float | None = None,
        short_term_liabilities: float | None = None,
        financial_assets: float | None = None,
    ) -> MoneywheelInput:
        return MoneywheelInput(
            planning_unit_id=financial_state.planning_unit_id,
            gross_monthly_income=financial_state.income_monthly.value,
            savings=financial_state.investable_surplus_monthly.value,
            essential_monthly_expenses=essential_monthly_expenses,
            monthly_expenses=financial_state.expenses_monthly.value,
            liquid_assets=liquid_assets,
            short_term_liabilities=short_term_liabilities,
            monthly_debt_payments=financial_state.emi_burden_monthly.value,
            total_assets=financial_state.total_assets.value,
            total_liabilities=financial_state.total_liabilities.value,
            financial_assets=financial_assets,
        )

    @staticmethod
    def snapshot(financial_state: FinancialState) -> dict[str, Any]:
        return financial_state.model_dump(mode="json")
