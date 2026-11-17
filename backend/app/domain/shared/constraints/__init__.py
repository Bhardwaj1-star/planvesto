"""
domain/shared/constraints/__init__.py
Chapter 06 Constraints module exports.
"""

from app.domain.shared.constraints.catalog import (
    ConstraintRuleId,
    ConstraintRuleDefinition,
    CONSTRAINT_CATALOG,
)
from app.domain.shared.constraints.result import (
    ConstraintEffect,
    ConstraintEvaluationResult,
)
from app.domain.shared.constraints.applicability import (
    DecisionContext,
    get_applicable_rules,
)
from app.domain.shared.constraints.evaluator import (
    evaluate_dti_gate,
    evaluate_asset_availability_gate,
    evaluate_high_interest_liability_gate,
    evaluate_sip_affordability_gate,
)

__all__ = [
    "ConstraintRuleId",
    "ConstraintRuleDefinition",
    "CONSTRAINT_CATALOG",
    "ConstraintEffect",
    "ConstraintEvaluationResult",
    "DecisionContext",
    "get_applicable_rules",
    "evaluate_dti_gate",
    "evaluate_asset_availability_gate",
    "evaluate_high_interest_liability_gate",
    "evaluate_sip_affordability_gate",
]
