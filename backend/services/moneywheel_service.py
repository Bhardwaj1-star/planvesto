import logging
from typing import Any

from models.financial_state import FinancialState
from models.moneywheel import MoneywheelInput, MoneywheelResult
from engines.moneywheel.engine import MoneywheelEngine
from engines.moneywheel.financial_state_adapter import MoneywheelFinancialStateAdapter
from data.financial_data import FinancialDataRepository
from data.goal_repository import GoalRepository

logger = logging.getLogger(__name__)

SHORT_TERM_LIABILITY_TYPES = {"Credit Card", "Personal Loan", "Consumer Loan", "Other"}
ESSENTIAL_EXPENSE_TYPES = {"Housing", "Utilities", "Groceries", "Healthcare", "Insurance", "Education", "Debt Payments"}


class MoneywheelService:
    """Calculates Moneywheel from authoritative financial state and source classifications."""

    def __init__(
        self,
        repository,
        data_repository: FinancialDataRepository | None = None,
        goal_repository: GoalRepository | None = None,
        engine: MoneywheelEngine | None = None,
        adapter: MoneywheelFinancialStateAdapter | None = None,
    ):
        self.repository = repository
        self.data_repository = data_repository or FinancialDataRepository()
        self.goal_repository = goal_repository or GoalRepository()
        self.engine = engine or MoneywheelEngine()
        self.adapter = adapter or MoneywheelFinancialStateAdapter()

    def calculate(
        self,
        data: MoneywheelInput,
        financial_state_snapshot: dict[str, Any] | None = None,
        protection_metadata: dict[str, Any] | None = None,
        debug_metadata: dict[str, Any] | None = None,
    ) -> MoneywheelResult:
        result = self.engine.build(data)
        if protection_metadata:
            result.metadata["protection"] = protection_metadata
        if debug_metadata:
            result.metadata.update(debug_metadata)
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
        planning_unit_id = financial_state.planning_unit_id
        expenses = self.data_repository.get_expenses(planning_unit_id)
        assets = self.data_repository.get_assets(planning_unit_id)
        liabilities = self.data_repository.get_liabilities(planning_unit_id)
        policies = self.data_repository.get_insurance_policies(planning_unit_id)

        active_asset_types = self.data_repository.get_active_asset_types()
        unmapped_asset_types: set[str] = set()

        if essential_monthly_expenses is None:
            essential_monthly_expenses = self._sum_expenses(expenses)
        if liquid_assets is None:
            liquid_assets = self._sum_assets(
                assets, "is_liquid", classifications=active_asset_types, unmapped_accumulator=unmapped_asset_types
            )
        if financial_assets is None:
            financial_assets = self._sum_assets(
                assets, "is_financial", classifications=active_asset_types, unmapped_accumulator=unmapped_asset_types
            )
        if short_term_liabilities is None:
            short_term_liabilities = self._sum_liabilities(liabilities, SHORT_TERM_LIABILITY_TYPES)

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

        # Required cover baseline: 10 years of gross income plus outstanding liabilities.
        # Existing assets are intentionally not netted off so insurance remains a pure protection signal.
        annual_income = float(financial_state.income_monthly.value or 0) * 12
        total_liabilities = float(financial_state.total_liabilities.value or 0)
        required_insurance_cover = (annual_income * 10) + total_liabilities

        goal_target_amount, current_goal_funding, future_goal_target, projected_goal_funding = self._goal_funding(planning_unit_id)

        protection_metadata = {
            "total_sum_assured": total_sum_assured,
            "life_cover": total_life_cover,
            "health_cover": total_health_cover,
            "required_insurance_cover": required_insurance_cover,
            "policy_count": len(policies),
        }
        goal_metadata = {
            "goal_target_amount": goal_target_amount,
            "current_goal_funding": current_goal_funding,
            "future_goal_target": future_goal_target,
            "projected_goal_funding": projected_goal_funding,
        }

        data = self.adapter.build(
            financial_state,
            essential_monthly_expenses=essential_monthly_expenses,
            liquid_assets=liquid_assets,
            short_term_liabilities=short_term_liabilities,
            financial_assets=financial_assets,
            existing_sum_assured=total_sum_assured,
            required_insurance_cover=required_insurance_cover,
        )
        data.current_goal_funding = current_goal_funding
        data.goal_target_amount = goal_target_amount
        data.projected_goal_funding = projected_goal_funding
        data.future_goal_target = future_goal_target

        debug_metadata = {
            "unmapped_asset_types": sorted(list(unmapped_asset_types)),
        }

        result = self.calculate(
            data,
            financial_state.model_dump(mode="json"),
            protection_metadata=protection_metadata,
            debug_metadata=debug_metadata,
        )
        result.metadata["goals"] = goal_metadata
        if "unmapped_asset_types" not in result.metadata:
            result.metadata["unmapped_asset_types"] = sorted(list(unmapped_asset_types))
        return result

    def _goal_funding(self, planning_unit_id: str):
        goals = self.goal_repository.list_goals(planning_unit_id)
        if not goals:
            return None, None, None, None

        current_target = 0.0
        current_funding = 0.0
        future_target = 0.0
        projected_funding = 0.0
        found = False

        for goal in goals:
            defined = self.goal_repository.get_latest_defined_goal(planning_unit_id, goal["goal_id"])
            if not defined:
                continue
            found = True
            current_target += max(float(defined.today_cost or 0), 0.0)
            current_funding += sum(max(float(m.allocated_amount or 0), 0.0) for m in defined.mapped_assets)
            future_target += max(float(defined.future_target or 0), 0.0)
            projected_funding += max(float(defined.projected_mapped_asset_value or 0), 0.0)

        if not found:
            return None, None, None, None
        return current_target, current_funding, future_target, projected_funding

    @staticmethod
    def _build_master_lookup(classifications: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
        lookup: dict[str, dict[str, Any]] = {}
        for item in classifications:
            if not item.get("is_active", True):
                continue
            name = str(item.get("name") or "").strip().lower()
            if name:
                lookup[name] = item
            code = str(item.get("code") or "").strip().lower()
            if code:
                lookup[code] = item
        return lookup

    @classmethod
    def _resolve_asset_classification(
        cls,
        row: dict[str, Any],
        lookup: dict[str, dict[str, Any]],
    ) -> tuple[dict[str, Any] | None, str | None]:
        """Resolves an asset row to its corresponding asset_type_master record.

        Returns (master_record, raw_identifier).
        - If resolved: (master_record, raw_identifier)
        - If unmapped: (None, raw_identifier)
        - If row has neither asset type nor asset name: (None, None)
        """
        raw_type = row.get("asset_type")
        if raw_type is not None:
            trimmed = str(raw_type).strip()
            if not trimmed:
                return None, None
            lowered = trimmed.lower()
            if lowered in lookup:
                return lookup[lowered], trimmed
            return None, trimmed

        raw_name = row.get("asset_name")
        if raw_name is not None:
            trimmed_name = str(raw_name).strip()
            if not trimmed_name:
                return None, None
            lowered_name = trimmed_name.lower()
            if lowered_name in lookup:
                return lookup[lowered_name], trimmed_name
            if " - " in trimmed_name:
                prefix = trimmed_name.split(" - ", 1)[0].strip()
                lowered_prefix = prefix.lower()
                if lowered_prefix in lookup:
                    return lookup[lowered_prefix], prefix
                return None, prefix
            return None, trimmed_name

        return None, None

    @classmethod
    def _sum_assets(
        cls,
        rows: list[dict[str, Any]],
        flag: str,
        classifications: list[dict[str, Any]] | None = None,
        unmapped_accumulator: set[str] | list[str] | None = None,
    ) -> float:
        if classifications is None:
            classifications = FinancialDataRepository().get_active_asset_types()

        lookup = cls._build_master_lookup(classifications)
        total = 0.0
        for row in rows:
            master, raw_identifier = cls._resolve_asset_classification(row, lookup)
            if master is None:
                if raw_identifier is not None:
                    logger.warning("Unmapped or unknown asset type encountered: %s", raw_identifier)
                    if unmapped_accumulator is not None:
                        if isinstance(unmapped_accumulator, set):
                            unmapped_accumulator.add(raw_identifier)
                        elif isinstance(unmapped_accumulator, list) and raw_identifier not in unmapped_accumulator:
                            unmapped_accumulator.append(raw_identifier)
                continue
            if master.get(flag) is True:
                total += float(row.get("current_value") or 0)
        return total

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
