"""Canonical business-rule registry.

This module is the single metadata authority for rule identity, scope, role,
and version. Existing rule modules remain compatibility/implementation surfaces;
new engines should reference canonical rule IDs from this registry rather than
inventing local rule identifiers.

No financial thresholds or business behavior are changed here.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final


CANONICAL_RULE_SET_VERSION: Final[str] = "1.0"


class RuleScope(str, Enum):
    GLOBAL = "global"
    FINANCIAL_STATE = "financial_state"
    GOAL = "goal"
    CONSTRAINT = "constraint"
    STRATEGY = "strategy"
    ACTION = "action"
    DECISION = "decision"
    PROTECTION = "protection"


class RuleRole(str, Enum):
    HARD_CONSTRAINT = "hard_constraint"
    ELIGIBILITY = "eligibility"
    RANKING_INPUT = "ranking_input"
    RECOMMENDATION_ONLY = "recommendation_only"
    ARCHITECTURE_CONSTRAINT = "architecture_constraint"
    EXPLANATORY_EVIDENCE = "explanatory_evidence"
    CLASSIFICATION = "classification"
    TRANSFORMATION = "transformation"


@dataclass(frozen=True)
class CanonicalRule:
    rule_id: str
    name: str
    scope: RuleScope
    role: RuleRole
    source_module: str
    description: str
    version: str = CANONICAL_RULE_SET_VERSION


def _rule(
    rule_id: str,
    name: str,
    scope: RuleScope,
    role: RuleRole,
    source_module: str,
    description: str,
) -> CanonicalRule:
    return CanonicalRule(
        rule_id=rule_id,
        name=name,
        scope=scope,
        role=role,
        source_module=source_module,
        description=description,
    )


CANONICAL_RULES: Final[dict[str, CanonicalRule]] = {
    # Goal validity
    "goal-positive-horizon": _rule(
        "goal-positive-horizon",
        "Goal Positive Horizon",
        RuleScope.GOAL,
        RuleRole.HARD_CONSTRAINT,
        "engines.rules.engine",
        "Goal duration must be positive.",
    ),
    "goal-positive-target": _rule(
        "goal-positive-target",
        "Goal Positive Target",
        RuleScope.GOAL,
        RuleRole.HARD_CONSTRAINT,
        "engines.rules.engine",
        "Goal future target must be positive.",
    ),

    # Goal classification / normalization
    "goal-type-normalization": _rule(
        "goal-type-normalization",
        "Goal Type Normalization",
        RuleScope.GOAL,
        RuleRole.CLASSIFICATION,
        "rules.goals",
        "Normalize goal-type labels and aliases to canonical goal types.",
    ),
    "goal-priority-classification": _rule(
        "goal-priority-classification",
        "Goal Priority Classification",
        RuleScope.GOAL,
        RuleRole.CLASSIFICATION,
        "rules.goals",
        "Classify goal priority into the canonical priority vocabulary.",
    ),

    # MoneyWheel / financial diagnostics
    "moneywheel-savings-rate": _rule(
        "moneywheel-savings-rate",
        "Savings Rate",
        RuleScope.FINANCIAL_STATE,
        RuleRole.EXPLANATORY_EVIDENCE,
        "rules.moneywheel",
        "Classify savings rate against the MoneyWheel benchmark bands.",
    ),
    "moneywheel-liquid-asset-ratio": _rule(
        "moneywheel-liquid-asset-ratio",
        "Liquid Asset Ratio",
        RuleScope.FINANCIAL_STATE,
        RuleRole.EXPLANATORY_EVIDENCE,
        "rules.moneywheel",
        "Classify liquid assets relative to total assets.",
    ),
    "moneywheel-debt-to-income": _rule(
        "moneywheel-debt-to-income",
        "Debt-to-Income Ratio",
        RuleScope.FINANCIAL_STATE,
        RuleRole.EXPLANATORY_EVIDENCE,
        "rules.moneywheel",
        "Classify mandatory debt payments relative to gross income.",
    ),
    "moneywheel-leverage": _rule(
        "moneywheel-leverage",
        "Leverage Ratio",
        RuleScope.FINANCIAL_STATE,
        RuleRole.EXPLANATORY_EVIDENCE,
        "rules.moneywheel",
        "Classify liabilities relative to total assets.",
    ),
    "moneywheel-financial-asset-ratio": _rule(
        "moneywheel-financial-asset-ratio",
        "Financial Asset Ratio",
        RuleScope.FINANCIAL_STATE,
        RuleRole.EXPLANATORY_EVIDENCE,
        "rules.moneywheel",
        "Classify financial assets relative to total assets.",
    ),
    "moneywheel-insurance-coverage": _rule(
        "moneywheel-insurance-coverage",
        "Insurance Coverage Ratio",
        RuleScope.PROTECTION,
        RuleRole.EXPLANATORY_EVIDENCE,
        "rules.moneywheel",
        "Classify existing insurance cover relative to required cover.",
    ),
    "moneywheel-goal-funding": _rule(
        "moneywheel-goal-funding",
        "Goal Funding Ratio",
        RuleScope.GOAL,
        RuleRole.EXPLANATORY_EVIDENCE,
        "rules.moneywheel",
        "Classify current goal funding relative to target.",
    ),
    "moneywheel-future-funding": _rule(
        "moneywheel-future-funding",
        "Future Funding Ratio",
        RuleScope.GOAL,
        RuleRole.EXPLANATORY_EVIDENCE,
        "rules.moneywheel",
        "Classify projected goal funding relative to the future target.",
    ),
    "moneywheel-required-return": _rule(
        "moneywheel-required-return",
        "Required Rate of Return",
        RuleScope.GOAL,
        RuleRole.EXPLANATORY_EVIDENCE,
        "rules.moneywheel",
        "Classify the return implied by current funding, target, and horizon.",
    ),
    "moneywheel-expense-coverage": _rule(
        "moneywheel-expense-coverage",
        "Expense Coverage",
        RuleScope.FINANCIAL_STATE,
        RuleRole.EXPLANATORY_EVIDENCE,
        "rules.moneywheel",
        "Measure liquid assets in months of total expenses.",
    ),
    "moneywheel-emergency-coverage": _rule(
        "moneywheel-emergency-coverage",
        "Emergency Coverage",
        RuleScope.FINANCIAL_STATE,
        RuleRole.EXPLANATORY_EVIDENCE,
        "rules.moneywheel",
        "Measure liquid assets in months of essential expenses.",
    ),

    # Strategy eligibility
    "strategy-cashflow-fit": _rule(
        "strategy-cashflow-fit",
        "Strategy Cash-flow Fit",
        RuleScope.STRATEGY,
        RuleRole.ELIGIBILITY,
        "engines.strategy.eligibility",
        "Check whether required contribution fits available cash-flow capacity.",
    ),
    "strategy-liquidity-fit": _rule(
        "strategy-liquidity-fit",
        "Strategy Liquidity Fit",
        RuleScope.STRATEGY,
        RuleRole.ELIGIBILITY,
        "engines.strategy.eligibility",
        "Check required liquidity against available liquid resources.",
    ),
    "strategy-debt-fit": _rule(
        "strategy-debt-fit",
        "Strategy Debt Fit",
        RuleScope.STRATEGY,
        RuleRole.ELIGIBILITY,
        "engines.strategy.eligibility",
        "Check whether mandatory debt obligations remain serviceable.",
    ),
    "strategy-asset-resource-fit": _rule(
        "strategy-asset-resource-fit",
        "Strategy Asset Resource Fit",
        RuleScope.STRATEGY,
        RuleRole.ELIGIBILITY,
        "engines.strategy.eligibility",
        "Check required strategy resources against available resources.",
    ),
    "strategy-risk-capacity-fit": _rule(
        "strategy-risk-capacity-fit",
        "Strategy Risk Capacity Fit",
        RuleScope.STRATEGY,
        RuleRole.ELIGIBILITY,
        "engines.strategy.eligibility",
        "Check strategy risk requirement against investor risk capacity.",
    ),
    "strategy-goal-constraint-fit": _rule(
        "strategy-goal-constraint-fit",
        "Strategy Goal Constraint Fit",
        RuleScope.STRATEGY,
        RuleRole.ELIGIBILITY,
        "engines.strategy.eligibility",
        "Check goal type, horizon, and mandatory strategy constraints.",
    ),
    "strategy-multi-goal-conflict-fit": _rule(
        "strategy-multi-goal-conflict-fit",
        "Strategy Multi-goal Conflict Fit",
        RuleScope.STRATEGY,
        RuleRole.ELIGIBILITY,
        "engines.strategy.eligibility",
        "Check whether a strategy materially compromises a higher-priority goal.",
    ),
    "strategy-implementation-fit": _rule(
        "strategy-implementation-fit",
        "Strategy Implementation Fit",
        RuleScope.STRATEGY,
        RuleRole.ELIGIBILITY,
        "engines.strategy.eligibility",
        "Check whether required implementation evidence is available and feasible.",
    ),

    # Multi-goal policy
    "goal-priority-order": _rule(
        "goal-priority-order",
        "Goal Priority Order",
        RuleScope.GOAL,
        RuleRole.ARCHITECTURE_CONSTRAINT,
        "rules.multi_goal",
        "Map goal priority to canonical precedence ranks.",
    ),
    "discretionary-cannot-preempt-essential": _rule(
        "discretionary-cannot-preempt-essential",
        "Discretionary Cannot Preempt Essential",
        RuleScope.CONSTRAINT,
        RuleRole.HARD_CONSTRAINT,
        "rules.multi_goal",
        "Discretionary commitments must not preempt essential or safety-reserve funding.",
    ),

    # Protection
    "required-insurance-cover": _rule(
        "required-insurance-cover",
        "Required Insurance Cover",
        RuleScope.PROTECTION,
        RuleRole.TRANSFORMATION,
        "rules.protection",
        "Baseline required cover is ten years of gross annual income plus outstanding liabilities.",
    ),
}


def get_rule(rule_id: str) -> CanonicalRule:
    """Return one canonical rule definition."""
    try:
        return CANONICAL_RULES[rule_id]
    except KeyError as exc:
        raise KeyError(f"Unknown canonical rule: {rule_id}") from exc


def get_rules(
    *,
    scope: RuleScope | None = None,
    role: RuleRole | None = None,
) -> tuple[CanonicalRule, ...]:
    """Return canonical rules filtered by scope and/or decision role."""
    rules = CANONICAL_RULES.values()
    if scope is not None:
        rules = (rule for rule in rules if rule.scope == scope)
    if role is not None:
        rules = (rule for rule in rules if rule.role == role)
    return tuple(rules)


def validate_rule_registry() -> None:
    """Fail fast on duplicate IDs or malformed canonical definitions."""
    if len(CANONICAL_RULES) != len(set(CANONICAL_RULES)):
        raise ValueError("Canonical rule IDs must be unique.")
    for rule_id, rule in CANONICAL_RULES.items():
        if rule_id != rule.rule_id:
            raise ValueError(f"Canonical rule key mismatch: {rule_id}")
