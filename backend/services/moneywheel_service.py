from typing import Any

from engines.moneywheel.engine import MoneywheelEngine
from models.financial_state import FinancialState
from models.moneywheel import MoneywheelInput, MoneywheelResult


class MoneywheelService:
    def __init__(self, repository):
        self.repository = repository
        self.engine = MoneywheelEngine()

    def calculate(self, data: MoneywheelInput, financial_state_snapshot: dict[str, Any] | None = None) -> MoneywheelResult:
        result = self.engine.build(data)
        snapshot = financial_state_snapshot or {}
        return self.repository.save_snapshot(result, snapshot)

    def calculate_from_financial_state(
        self,
        financial_state: FinancialState,
        *,
        essential_monthly_expenses: float | None = None,
        liquid_assets: float | None = None,
        short_term_liabilities: float | None = None,
        financial_assets: float | None = None,
    ) -> MoneywheelResult:
        """Build from the existing FinancialState where semantics are explicit.

        Classification-dependent fields are supplied separately until the
        Financial State model stores those classifications natively.
        """
        data = MoneywheelInput(
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
        return self.calculate(data, financial_state.model_dump(mode="json"))
