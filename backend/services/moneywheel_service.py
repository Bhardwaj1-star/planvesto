from typing import Any

from engines.moneywheel.engine import MoneywheelEngine
from engines.moneywheel.financial_state_adapter import MoneywheelFinancialStateAdapter
from models.financial_state import FinancialState
from models.moneywheel import MoneywheelInput, MoneywheelResult


class MoneywheelService:
    """Coordinates Moneywheel calculation and immutable snapshot persistence."""

    def __init__(self, repository):
        self.repository = repository
        self.engine = MoneywheelEngine()
        self.adapter = MoneywheelFinancialStateAdapter()

    def calculate(
        self,
        data: MoneywheelInput,
        financial_state_snapshot: dict[str, Any] | None = None,
    ) -> MoneywheelResult:
        result = self.engine.build(data)
        return self.repository.save_snapshot(result, financial_state_snapshot or {})

    def calculate_from_financial_state(
        self,
        financial_state: FinancialState,
        *,
        essential_monthly_expenses: float | None = None,
        liquid_assets: float | None = None,
        short_term_liabilities: float | None = None,
        financial_assets: float | None = None,
    ) -> MoneywheelResult:
        """Build Moneywheel from FinancialState plus explicit classified inputs.

        Classification-dependent fields remain explicit until their future
        authoritative source systems are implemented.
        """
        data = self.adapter.build(
            financial_state,
            essential_monthly_expenses=essential_monthly_expenses,
            liquid_assets=liquid_assets,
            short_term_liabilities=short_term_liabilities,
            financial_assets=financial_assets,
        )
        return self.calculate(data, financial_state.model_dump(mode="json"))
