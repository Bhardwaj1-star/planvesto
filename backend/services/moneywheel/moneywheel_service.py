from typing import Any
import logging

from models.financial_state import FinancialState
from models.moneywheel import MoneywheelInput, MoneywheelResult
from engines.moneywheel.engine import MoneywheelEngine
from engines.moneywheel.financial_state_adapter import MoneywheelFinancialStateAdapter
from data.goal_repository import GoalRepository
from rules.protection import (
    calculate_required_insurance_cover,
    is_health_insurance,
    is_life_insurance,
)

logger = logging.getLogger(__name__)


class MoneywheelService:
    """Calculates Moneywheel from authoritative financial state and source classifications."""

    def __init__(
        self,
        repository=None,
        data_repository=None,
        goal_repository: GoalRepository | None = None,
        engine: MoneywheelEngine | None = None,
        adapter: MoneywheelFinancialStateAdapter | None = None,
    ):
        self.repository = repository
        self.data_repository = data_repository
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
        if self.repository is None:
            raise RuntimeError("MoneywheelRepository is required to persist a calculation.")
        return self.repository.save_snapshot(result, financial_state_snapshot or {})

    def build_from_financial_state(
        self,
        financial_state: FinancialState,
    ) -> MoneywheelResult:
        """Build a Moneywheel assessment without persisting a history snapshot.

        Use this for embedded report sections that need the same canonical
        measurements without creating a second calculation-history record.
        Insurance facts and breakdown are sourced from FinancialState.
        Goal funding remains sourced from GoalRepository.
        """
        planning_unit_id = financial_state.planning_unit_id
        policies = financial_state.insurance_breakdown or []

        total_sum_assured = float(financial_state.total_insurance_sum_assured.value or 0)
        total_life_cover = sum(
            float(p.get("sum_assured") or 0) for p in policies
            if is_life_insurance(p.get("policy_type"))
        )
        total_health_cover = sum(
            float(p.get("sum_assured") or 0) for p in policies
            if is_health_insurance(p.get("policy_type"))
        )

        annual_income = float(financial_state.income_monthly.value or 0) * 12
        total_liabilities = float(financial_state.total_liabilities.value or 0)
        required_insurance_cover = calculate_required_insurance_cover(annual_income, total_liabilities)

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

        data = self.adapter.build(financial_state)
        data.current_goal_funding = current_goal_funding
        data.goal_target_amount = goal_target_amount
        data.projected_goal_funding = projected_goal_funding
        data.future_goal_target = future_goal_target
        data.existing_sum_assured = total_sum_assured
        data.required_insurance_cover = required_insurance_cover

        result = self.engine.build(data)
        result.metadata["protection"] = protection_metadata
        result.metadata["goals"] = goal_metadata
        return result

    def calculate_from_financial_state(
        self,
        financial_state: FinancialState,
    ) -> MoneywheelResult:
        """Build the canonical assessment and persist its history snapshot."""
        result = self.build_from_financial_state(financial_state)
        if self.repository is None:
            raise RuntimeError("MoneywheelRepository is required to persist a calculation.")
        return self.repository.save_snapshot(result, financial_state.model_dump(mode="json"))

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
