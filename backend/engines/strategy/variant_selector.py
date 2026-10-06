"""Automated Strategy Variant Selector.

Variant is 100% automated system-selected based on goal pattern, strategy, and
financial context. The investor selects between system-generated candidate strategies;
variants are not exposed as an interactive selection choice in the UI.

Selected variant is preserved in decision snapshots and run metadata for report
generation and downstream scheduling.
"""
from __future__ import annotations

from typing import Any
from library.strategies.variants import (
    StrategyVariantDefinition,
    get_canonical_strategy_variant,
    get_canonical_strategy_variants,
)
from rules.goals import canonical_goal_type


class VariantSelector:
    """Deterministically resolves the canonical strategy variant for any goal + strategy."""

    @classmethod
    def select_variant(
        cls,
        strategy_id: str,
        goal: Any,
        financial_context: dict[str, Any] | None = None,
        baseline_scenario: Any | None = None,
    ) -> StrategyVariantDefinition:
        context = financial_context or {}
        goal_type = canonical_goal_type(getattr(goal, "goal_type", None) or getattr(goal, "type", "") or "")
        dynamic_details = getattr(goal, "dynamic_details", {}) or {}
        if not isinstance(dynamic_details, dict):
            dynamic_details = {}

        if strategy_id == "strat-goal-funding":
            variant_id = cls._select_goal_funding_variant(goal, context, baseline_scenario)
        elif strategy_id == "strat-progressive-de-risking":
            variant_id = cls._select_de_risking_variant(goal_type, goal, dynamic_details)
        elif strategy_id == "strat-capital-preservation":
            variant_id = cls._select_preservation_variant(goal_type, goal, dynamic_details, context)
        elif strategy_id == "strat-debt-reduction":
            variant_id = cls._select_debt_reduction_variant(goal_type, dynamic_details, context)
        elif strategy_id == "strat-credit-utilisation":
            variant_id = cls._select_credit_variant(goal_type, goal, dynamic_details, context)
        else:
            variants = get_canonical_strategy_variants(strategy_id)
            variant_id = variants[0].variant_id if variants else "default"

        variant = get_canonical_strategy_variant(variant_id)
        if variant is None:
            # Fallback to the first available variant for the strategy
            available = get_canonical_strategy_variants(strategy_id)
            if available:
                return available[0]
            raise ValueError(f"No canonical variant found for strategy {strategy_id}")
        return variant

    @classmethod
    def _select_goal_funding_variant(
        cls,
        goal: Any,
        context: dict[str, Any],
        baseline_scenario: Any | None,
    ) -> str:
        if baseline_scenario is not None:
            f_id = getattr(baseline_scenario, "funding_strategy_id", None)
            if not f_id and isinstance(baseline_scenario, dict):
                f_id = baseline_scenario.get("funding_strategy_id")
            if f_id and get_canonical_strategy_variant(f_id):
                return str(f_id)

        mapped = float(getattr(goal, "projected_mapped_asset_value", 0) or 0)
        future_target = float(getattr(goal, "future_target", 0) or 0)
        gap = float(getattr(goal, "funding_gap", 0) or 0)
        if future_target > 0 and mapped >= future_target:
            return "existing_assets"

        surplus = float(context.get("investable_surplus_monthly") or context.get("monthly_surplus") or 0)
        if surplus <= 0 and gap > 0:
            return "lumpsum"
        return "step_up_sip"

    @classmethod
    def _select_de_risking_variant(
        cls,
        goal_type: str,
        goal: Any,
        dynamic_details: dict[str, Any],
    ) -> str:
        if goal_type in ("retirement", "fire_passive_income"):
            return "income_transition_glide_path"
        if goal_type == "education" or bool(dynamic_details.get("has_tranches") or dynamic_details.get("number_of_years")):
            return "payment_tranche_glide_path"
        if goal_type == "vacation" or int(dynamic_details.get("number_of_trips", 1) or 1) > 1:
            return "recurring_cashflow_glide_path"
        return "goal_date_glide_path"

    @classmethod
    def _select_preservation_variant(
        cls,
        goal_type: str,
        goal: Any,
        dynamic_details: dict[str, Any],
        context: dict[str, Any],
    ) -> str:
        if goal_type == "vacation" or bool(dynamic_details.get("repeat_every_years")):
            return "rolling_reserve_preservation"
        if goal_type == "education" or bool(dynamic_details.get("number_of_years")):
            return "first_payment_preservation"
        surplus = float(context.get("investable_surplus_monthly") or context.get("monthly_surplus") or 0)
        if surplus > 0 and float(getattr(goal, "future_target", 0) or 0) > 0:
            return "protected_core_preservation"
        return "full_goal_preservation"

    @classmethod
    def _select_debt_reduction_variant(
        cls,
        goal_type: str,
        dynamic_details: dict[str, Any],
        context: dict[str, Any],
    ) -> str:
        if goal_type == "debt_freedom" or bool(dynamic_details.get("linked_liability_id")):
            return "goal_linked_debt_reduction"
        emi = float(context.get("emi_burden_monthly") or context.get("monthly_debt_payments") or 0)
        income = float(context.get("monthly_income") or context.get("income") or 1)
        if income > 0 and (emi / income) >= 0.40:
            return "emi_relief_debt_reduction"
        surplus = float(context.get("investable_surplus_monthly") or context.get("monthly_surplus") or 0)
        if surplus <= 0:
            return "residual_gap_debt_reduction"
        return "goal_gap_debt_reduction"

    @classmethod
    def _select_credit_variant(
        cls,
        goal_type: str,
        goal: Any,
        dynamic_details: dict[str, Any],
        context: dict[str, Any],
    ) -> str:
        duration = float(getattr(goal, "duration_years", 0) or 0)
        if bool(dynamic_details.get("timing_bridge")) or duration <= 1:
            return "timing_bridge_financing"
        emi = float(context.get("emi_burden_monthly") or context.get("monthly_debt_payments") or 0)
        income = float(context.get("monthly_income") or context.get("income") or 1)
        if income > 0 and (emi / income) >= 0.30:
            return "emi_cap_financing"
        if goal_type in ("education", "dream_home"):
            return "partial_goal_financing"
        return "residual_gap_bridge"
