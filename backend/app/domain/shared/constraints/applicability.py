"""
domain/shared/constraints/applicability.py
Chapter 06 — Constraint Applicability Selection (§1, §2).

Selects approved rules for a specific decision context:
- Goal Feasibility requires CTR-AFF-001 and CTR-LIQ-001
- Financing path requires CTR-DTI-001 and CTR-HIR-001
- Diagnostics/Moneywheel evaluates all applicable position rules
"""

from enum import Enum
from typing import List
from app.domain.shared.constraints.catalog import ConstraintRuleId


class DecisionContext(str, Enum):
    GOAL_FEASIBILITY = "goal_feasibility"
    STRATEGY_BUILDER_FINANCING = "strategy_builder_financing"
    STRATEGY_BUILDER_ASSET_ALLOCATION = "strategy_builder_asset_allocation"
    MONEYWHEEL_DIAGNOSTICS = "moneywheel_diagnostics"


def get_applicable_rules(context: DecisionContext) -> List[ConstraintRuleId]:
    """Returns the list of constraint rules that must be evaluated for the context."""
    if context == DecisionContext.GOAL_FEASIBILITY:
        return [ConstraintRuleId.CTR_AFF_001, ConstraintRuleId.CTR_LIQ_001]
    elif context == DecisionContext.STRATEGY_BUILDER_FINANCING:
        return [ConstraintRuleId.CTR_DTI_001, ConstraintRuleId.CTR_HIR_001]
    elif context == DecisionContext.STRATEGY_BUILDER_ASSET_ALLOCATION:
        return [ConstraintRuleId.CTR_LIQ_001]
    elif context == DecisionContext.MONEYWHEEL_DIAGNOSTICS:
        return [
            ConstraintRuleId.CTR_DTI_001,
            ConstraintRuleId.CTR_LIQ_001,
            ConstraintRuleId.CTR_HIR_001,
        ]
    return []
