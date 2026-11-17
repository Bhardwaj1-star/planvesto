"""
domain/shared/constraints/result.py
Chapter 06 — Constraint Evaluation Result Contracts (§1, §2).

Output contract:
- Status, evidence, missing-input, explanation, gap amount, and version references.
- Non-negotiable: Never treats missing evidence as Pass.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional
from app.domain.shared.value_objects import Money


class ConstraintEffect(str, Enum):
    INFORMATIONAL = "informational"
    MANDATORY_DISCLOSURE = "mandatory_disclosure"
    SATISFIED = "satisfied"
    SHORTFALL_UNDER_CURRENT_CONDITIONS = "shortfall_under_current_conditions"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"


@dataclass(frozen=True)
class ConstraintEvaluationResult:
    rule_id: str
    effect: ConstraintEffect
    is_satisfied: bool
    explanation: str
    gap_amount: Optional[Money] = None
    details: Dict[str, Any] = field(default_factory=dict)
