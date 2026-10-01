from engines.constraints.models import (
    CanonicalConstraint,
    ConstraintCheckResult,
    ConstraintConflict,
    ConstraintDomain,
    ConstraintRole,
    ConstraintSet,
    ConstraintSeverity,
    FinancialRatioResult,
    RatioConstraintAssessment,
    RatioStatus,
)
from engines.constraints.evaluator import FinancialRatioConstraintEvaluator
from engines.constraints.adapters import (
    adapt_constraint_check,
    adapt_ratio_assessment,
    adapt_ratio_result,
    adapt_risk_constraint,
    adapt_risk_profile_constraints,
    adapt_rule_assessment,
    adapt_rule_result,
    adapt_strategy_constraints,
    build_constraint_set,
)
from engines.constraints.aggregator import ConstraintAggregator

__all__ = [
    # Legacy (backward compatible)
    "ConstraintCheckResult",
    "FinancialRatioResult",
    "RatioConstraintAssessment",
    "ConstraintSeverity",
    "RatioStatus",
    "FinancialRatioConstraintEvaluator",
    # Canonical layer
    "CanonicalConstraint",
    "ConstraintConflict",
    "ConstraintDomain",
    "ConstraintRole",
    "ConstraintSet",
    # Adapters
    "adapt_constraint_check",
    "adapt_ratio_assessment",
    "adapt_ratio_result",
    "adapt_risk_constraint",
    "adapt_risk_profile_constraints",
    "adapt_rule_assessment",
    "adapt_rule_result",
    "adapt_strategy_constraints",
    "build_constraint_set",
    # Aggregator
    "ConstraintAggregator",
]
