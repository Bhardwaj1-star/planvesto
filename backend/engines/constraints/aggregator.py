"""Centralized Constraint Aggregator.

This module provides the single entry point for assembling a ConstraintSet
from all domain engines.  It is the canonical interface that downstream
consumers (Strategy Engine, Multi-Goal Orchestrator) should use.

Flow:
    Domain Engines -> Constraint Adapters -> Canonical Constraints -> ConstraintSet
"""
from __future__ import annotations

from typing import Any
from engines.constraints.adapters import (
    adapt_ratio_assessment,
    adapt_risk_profile_constraints,
    adapt_rule_assessment,
    adapt_strategy_constraints,
    build_constraint_set,
)
from engines.constraints.evaluator import FinancialRatioConstraintEvaluator
from engines.constraints.models import ConstraintSet
from engines.orchestration.models import GoalEvaluationInput


class ConstraintAggregator:
    """Assembles a ConstraintSet from all available domain engine outputs.

    Usage:
        aggregator = ConstraintAggregator()
        constraint_set = aggregator.aggregate(
            rule_assessment=rule_assessment,           # from RuleEngine
            goals=goal_inputs,                         # for ratio evaluation
            financial_context=financial_context,        # shared context
            risk_profile_constraints=risk_constraints,  # from RiskProfilerEngine
            strategy_constraints=arch_constraints,      # from strategy library
        )
    """

    def __init__(
        self,
        ratio_evaluator: FinancialRatioConstraintEvaluator | None = None,
    ):
        self.ratio_evaluator = ratio_evaluator or FinancialRatioConstraintEvaluator()

    def aggregate(
        self,
        *,
        rule_assessment: Any | None = None,
        goals: list[GoalEvaluationInput] | None = None,
        financial_context: dict[str, Any] | None = None,
        risk_profile_constraints: list[dict[str, Any]] | None = None,
        strategy_constraints: list[str] | None = None,
        strategy_id: str = "",
        planning_unit_id: str | None = None,
    ) -> ConstraintSet:
        """Build a unified ConstraintSet from all available domain outputs.

        Each parameter is optional — only the constraint sources that are
        available will be included.  This allows incremental adoption:
        callers can pass whatever they have.
        """
        layers: list = []

        # 1. RuleEngine assessment (goal diagnostics, hard/soft constraints)
        if rule_assessment is not None:
            layers.append(adapt_rule_assessment(rule_assessment))

        # 2. Financial ratio constraints (MoneyWheel-derived)
        if goals is not None and financial_context is not None:
            ratio_assessment = self.ratio_evaluator.assess_constraints(
                goals, financial_context
            )
            layers.append(adapt_ratio_assessment(ratio_assessment))

        # 3. Risk Profiler constraints
        if risk_profile_constraints is not None:
            layers.append(adapt_risk_profile_constraints(risk_profile_constraints))

        # 4. Strategy-level constraints
        if strategy_constraints is not None:
            layers.append(adapt_strategy_constraints(
                strategy_constraints, strategy_id=strategy_id
            ))

        provenance = {"planning_unit_id": planning_unit_id} if planning_unit_id else {}

        return build_constraint_set(*layers, provenance=provenance)
