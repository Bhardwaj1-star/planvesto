from typing import Any

from models.financial_state import FinancialState
from models.moneywheel import MoneywheelInput, MoneywheelResult
from engines.moneywheel.engine import MoneywheelEngine
from engines.moneywheel.financial_state_adapter import MoneywheelFinancialStateAdapter
from data.financial_data import FinancialDataRepository

LIQUID_ASSET_TYPES = {"Bank / Cash", "Mutual Funds", "Stocks / Equity"}
FINANCIAL_ASSET_TYPES = {"Bank / Cash", "Fixed Deposits", "Mutual Funds", "Stocks / Equity", "Bonds / Debt", "EPF / PPF", "NPS"}
SHORT_TERM_LIABILITY_TYPES = {"Credit Card", "Personal Loan", "Consumer Loan", "Other"}
ESSENTIAL_EXPENSE_TYPES = {"Housing", "Utilities", "Groceries", "Healthcare", "Insurance", "Education", "Debt Payments"}


class MoneywheelService:
    """Calculates Moneywheel from authoritative financial state and source classifications."""

    def __init__(self, repository):
        self.repository = repository
        self.data_repository = FinancialDataRepository()
        self.engine = MoneywheelEngine()
        self.adapter = MoneywheelFinancialStateAdapter()

    def calculate(self, data: MoneywheelInput, financial_state_snapshot: dict[str, Any] | None = None, protection_metadata: dict[str, Any] | None = None) -> MoneywheelResult:
        result = self.engine.build(data)
        if protection_metadata:
            result.metadata["protection"] = protection_metadata
        return self.repository.save_snapshot(result, financial_state_snapshot or {})

    def calculate_from_financial_state(self, financial_state: FinancialState, *, essential_monthly_expenses: float | None = None, liquid_assets: float | None = None, short_term_liabilities: float | None = None, financial_assets: float | None = None) -> MoneywheelResult:
        planning_unit_id = financial_state.planning_unit_id
        expenses = self.data_repository.get_expenses(planning_unit_id)
        assets = self.data_repository.get_assets(planning_unit_id)
        liabilities = self.data_repository.get_liabilities(planning_unit_id)
        policies = self.data_repository.get_insurance_policies(planning_unit_id)

        if essential_monthly_expenses is None:
            essential_monthly_expenses = self._sum_expenses(expenses)
        if liquid_assets is None:
            liquid_assets = self._sum_assets(assets, LIQUID_ASSET_TYPES)
        if financial_assets is None:
            financial_assets = self._sum_assets(assets, FINANCIAL_ASSET_TYPES)
        if short_term_liabilities is None:
            short_term_liabilities = self._sum_liabilities(liabilities, SHORT_TERM_LIABILITY_TYPES)

        # Map sum assured to protection signals without duplicate counting in assets/net worth
        total_sum_assured = sum(float(p.get("sum_assured") or 0) for p in policies)
        total_life_cover = sum(
            float(p.get("sum_assured") or 0) for p in policies
            if str(p.get("policy_type") or "").strip().lower() in {
                "term insurance", "term", "endowment", "whole life", "ulip", "money back"
            }
        )
        total_health_cover = sum(
            float(p.get("sum_assured") or 0) for p in policies
            if str(p.get("policy_type") or "").strip().lower() in {"health insurance", "health"}
        )
        protection_metadata = {
            "total_sum_assured": total_sum_assured,
            "life_cover": total_life_cover,
            "health_cover": total_health_cover,
            "policy_count": len(policies),
        }

        data = self.adapter.build(
            financial_state,
            essential_monthly_expenses=essential_monthly_expenses,
            liquid_assets=liquid_assets,
            short_term_liabilities=short_term_liabilities,
            financial_assets=financial_assets,
        )
        return self.calculate(data, financial_state.model_dump(mode="json"), protection_metadata=protection_metadata)


    @staticmethod
    def _sum_assets(rows, allowed_types):
        return sum(float(row.get("current_value") or 0) for row in rows if str(row.get("asset_type") or "Other") in allowed_types)

    @staticmethod
    def _sum_liabilities(rows, allowed_types):
        return sum(float(row.get("outstanding_amount") or 0) for row in rows if str(row.get("liability_type") or "Other") in allowed_types)

    @staticmethod
    def _sum_expenses(rows):
        from engines.calculation.engine import monthly_amount
        return sum(
            monthly_amount(float(row.get("amount") or 0), str(row.get("frequency") or "")) or 0
            for row in rows
            if str(row.get("expense_type") or "Other") in ESSENTIAL_EXPENSE_TYPES
        )
