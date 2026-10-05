"""Backward-compatible facade for canonical constraint policy.

Constraint normalization/conflict policy is owned by engines.constraints.policy.
"""
from engines.constraints.policy import (
    ConstraintKind,
    ConstraintSource,
    SOURCE_PRIORITY,
    ConstraintRules,
)

__all__ = ["ConstraintKind", "ConstraintSource", "SOURCE_PRIORITY", "ConstraintRules"]
