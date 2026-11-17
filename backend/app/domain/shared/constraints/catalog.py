"""
domain/shared/constraints/catalog.py
Chapter 06 — Constraint Catalogue Representation (§1, §2).

The authoritative registry of approved rules:
- CTR-DTI-001: Debt-to-Income planning assessment (informational)
- CTR-LIQ-001: Asset availability / accessibility check
- CTR-HIR-001: High interest rate trigger (>14.0% p.a.)
- CTR-AFF-001: SIP surplus affordability check
- CTR-RATIO-001: Ratio limit boundary
- CTR-INS-001: Insurance protection coverage boundary
- CTR-GATE-001: Overall planning prerequisite gate
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional


class ConstraintRuleId(str, Enum):
    CTR_DTI_001 = "CTR-DTI-001"
    CTR_LIQ_001 = "CTR-LIQ-001"
    CTR_HIR_001 = "CTR-HIR-001"
    CTR_AFF_001 = "CTR-AFF-001"
    CTR_RATIO_001 = "CTR-RATIO-001"
    CTR_INS_001 = "CTR-INS-001"
    CTR_GATE_001 = "CTR-GATE-001"


@dataclass(frozen=True)
class ConstraintRuleDefinition:
    rule_id: ConstraintRuleId
    name: str
    description: str
    chapter_reference: str
    is_blocking: bool


CONSTRAINT_CATALOG: Dict[ConstraintRuleId, ConstraintRuleDefinition] = {
    ConstraintRuleId.CTR_DTI_001: ConstraintRuleDefinition(
        rule_id=ConstraintRuleId.CTR_DTI_001,
        name="Debt-to-Income Planning Assessment",
        description="Informs Available Monthly Surplus context without blocking.",
        chapter_reference="Chapter 06 §2.1",
        is_blocking=False,
    ),
    ConstraintRuleId.CTR_LIQ_001: ConstraintRuleDefinition(
        rule_id=ConstraintRuleId.CTR_LIQ_001,
        name="Asset Availability & Accessibility Gate",
        description="Excludes assets not verified as accessible, unencumbered, and uncommitted.",
        chapter_reference="Chapter 06 §2.2",
        is_blocking=True,
    ),
    ConstraintRuleId.CTR_HIR_001: ConstraintRuleDefinition(
        rule_id=ConstraintRuleId.CTR_HIR_001,
        name="High-Interest Debt Evaluation Gate",
        description="Debts with rate > 14.0% p.a. trigger mandatory disclosure and prepayment comparison.",
        chapter_reference="Chapter 06 §2.3",
        is_blocking=False,
    ),
    ConstraintRuleId.CTR_AFF_001: ConstraintRuleDefinition(
        rule_id=ConstraintRuleId.CTR_AFF_001,
        name="SIP Surplus Affordability Gate",
        description="Tests whether required monthly SIP exceeds Available Monthly Surplus.",
        chapter_reference="Chapter 06 §2.4",
        is_blocking=False,
    ),
}
