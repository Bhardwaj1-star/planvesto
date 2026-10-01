"""Adapters that convert domain-specific constraint representations into
CanonicalConstraint instances.

Each adapter is a pure function: it receives domain objects and returns
a list of CanonicalConstraint.  No business rules are invented here;
the adapters only re-shape existing data.
"""
from __future__ import annotations

from typing import Any
from engines.constraints.models import (
    CanonicalConstraint,
    ConstraintCheckResult,
    ConstraintConflict,
    ConstraintRole,
    ConstraintSet,
    ConstraintSeverity,
    FinancialRatioResult,
    RatioConstraintAssessment,
)


# ---------------------------------------------------------------------------
# 1. RuleEngine (engines/rules/engine.py) -> CanonicalConstraint
# ---------------------------------------------------------------------------

_ROLE_MAP = {
    "HARD_CONSTRAINT": "hard_constraint",
    "ELIGIBILITY": "eligibility",
    "RANKING_INPUT": "ranking_input",
    "RECOMMENDATION_ONLY": "recommendation_only",
    "ARCHITECTURE_CONSTRAINT": "architecture_constraint",
    "EXPLANATORY_EVIDENCE": "explanatory_evidence",
}

_SEVERITY_MAP = {
    "hard": "hard",
    "soft": "warning",
    "diagnostic": "info",
}


def adapt_rule_result(result, *, index: int = 0) -> CanonicalConstraint:
    """Convert a single RuleResult (from engines.rules.engine) to CanonicalConstraint."""
    role_value = getattr(result.role, "value", None) if result.role else None
    canonical_role: ConstraintRole = _ROLE_MAP.get(role_value, "explanatory_evidence")
    severity: ConstraintSeverity = _SEVERITY_MAP.get(result.severity, "info")
    domain = "goal_eligibility" if severity == "hard" else "goal_diagnostic"
    kind = "hard" if result.severity == "hard" else ("soft" if result.severity == "soft" else "diagnostic")

    return CanonicalConstraint(
        constraint_id=f"rule-{result.rule_id}-{index}",
        rule_id=result.rule_id,
        domain=domain,
        source="rule_engine",
        source_engine="RuleEngine",
        severity=severity,
        role=canonical_role,
        kind=kind,
        passed=result.passed,
        message=result.message,
        evidence=dict(result.evidence) if result.evidence else {},
    )


def adapt_rule_assessment(assessment) -> list[CanonicalConstraint]:
    """Convert a full RuleAssessment into a list of CanonicalConstraint."""
    constraints: list[CanonicalConstraint] = []
    idx = 0
    for r in assessment.hard_constraints:
        constraints.append(adapt_rule_result(r, index=idx))
        idx += 1
    for r in assessment.soft_constraints:
        constraints.append(adapt_rule_result(r, index=idx))
        idx += 1
    for r in assessment.diagnostics:
        constraints.append(adapt_rule_result(r, index=idx))
        idx += 1
    return constraints


# ---------------------------------------------------------------------------
# 2. FinancialRatioConstraintEvaluator -> CanonicalConstraint
# ---------------------------------------------------------------------------

def adapt_ratio_result(ratio: FinancialRatioResult) -> CanonicalConstraint:
    """Convert a FinancialRatioResult into an info-level CanonicalConstraint."""
    severity: ConstraintSeverity = "info"
    if ratio.status == "critical":
        severity = "hard"
    elif ratio.status == "attention":
        severity = "warning"

    return CanonicalConstraint(
        constraint_id=f"ratio-{ratio.ratio_key}",
        rule_id=f"RATIO_{ratio.ratio_key.upper()}",
        domain="financial_ratio",
        source="moneywheel",
        source_engine="FinancialRatioConstraintEvaluator",
        severity=severity,
        role="explanatory_evidence",
        kind="diagnostic",
        passed=ratio.status not in ("critical",),
        message=f"{ratio.name}: {ratio.value} {ratio.unit} ({ratio.status or 'unknown'})",
        value=ratio.value,
        unit=ratio.unit,
        evidence=dict(ratio.evidence) if ratio.evidence else {},
    )


def adapt_constraint_check(check: ConstraintCheckResult) -> CanonicalConstraint:
    """Convert a ConstraintCheckResult into a CanonicalConstraint."""
    severity: ConstraintSeverity = check.severity
    role: ConstraintRole = "hard_constraint" if severity == "hard" else (
        "recommendation_only" if severity == "warning" else "explanatory_evidence"
    )
    kind = "hard" if severity == "hard" else "soft"

    return CanonicalConstraint(
        constraint_id=f"check-{check.rule_id}-{check.goal_id or 'global'}",
        rule_id=check.rule_id,
        domain="financial_ratio",
        source="ratio_constraint_evaluator",
        source_engine="FinancialRatioConstraintEvaluator",
        severity=severity,
        role=role,
        kind=kind,
        passed=check.passed,
        message=check.message,
        goal_id=check.goal_id,
        evidence=dict(check.ratio_evidence) if check.ratio_evidence else {},
        suggested_override_priority=check.suggested_override_priority,
        override_reason=check.override_reason,
    )


def adapt_ratio_assessment(assessment: RatioConstraintAssessment) -> list[CanonicalConstraint]:
    """Convert a full RatioConstraintAssessment into canonical constraints."""
    constraints: list[CanonicalConstraint] = []
    for ratio in assessment.ratios:
        constraints.append(adapt_ratio_result(ratio))
    for check in assessment.constraints:
        constraints.append(adapt_constraint_check(check))
    for warning in assessment.warnings:
        constraints.append(adapt_constraint_check(warning))
    return constraints


# ---------------------------------------------------------------------------
# 3. RiskProfilerEngine constraints (dict-based) -> CanonicalConstraint
# ---------------------------------------------------------------------------

_RISK_DOMAIN_MAP = {
    "risk_need_": "risk_required",
    "risk_capacity_": "risk_capacity",
    "risk_exposure_": "risk_capacity",
    "risk_tolerance_": "risk_tolerance",
}


def _infer_risk_domain(key: str) -> str:
    for prefix, domain in _RISK_DOMAIN_MAP.items():
        if key.startswith(prefix):
            return domain
    return "risk_capacity"


def _normalize_evidence(evidence: Any) -> dict[str, Any]:
    """Convert evidence to dict form. Risk Profiler stores evidence as list[dict]."""
    if isinstance(evidence, dict):
        return evidence
    if isinstance(evidence, list):
        result: dict[str, Any] = {"items": evidence}
        # Also flatten single-item lists for convenience
        for i, item in enumerate(evidence):
            if isinstance(item, dict):
                for k, v in item.items():
                    result[k] = v
        return result
    return {}


def adapt_risk_constraint(item: dict[str, Any], *, index: int = 0) -> CanonicalConstraint:
    """Convert a single risk profiler constraint dict into a CanonicalConstraint."""
    kind_raw = item.get("kind", "soft")
    severity: ConstraintSeverity = "hard" if kind_raw == "hard" else "warning"
    role: ConstraintRole = "hard_constraint" if kind_raw == "hard" else "recommendation_only"
    domain = _infer_risk_domain(item.get("key", ""))

    validity = item.get("validity", {})
    if not isinstance(validity, dict):
        validity = {"status": "valid", "valid_from": None, "valid_until": None}

    return CanonicalConstraint(
        constraint_id=f"risk-{item.get('key', 'unknown')}-{index}",
        rule_id=item.get("key", f"risk_constraint_{index}"),
        domain=domain,
        source=item.get("source", "financial_state"),
        source_engine="RiskProfilerEngine",
        severity=severity,
        role=role,
        kind=kind_raw,
        passed=True,  # Risk constraints are factual observations, not pass/fail
        message=f"{item.get('key', 'constraint')}: {item.get('value')} {item.get('unit', '')}",
        value=float(item["value"]) if item.get("value") is not None else None,
        unit=item.get("unit"),
        evidence=_normalize_evidence(item.get("evidence", {})),
        confidence=float(item.get("confidence", 1.0)),
        validity=validity,
    )


def adapt_risk_profile_constraints(risk_profile_constraints: list[dict[str, Any]]) -> list[CanonicalConstraint]:
    """Convert all constraints from a RiskProfile into canonical form."""
    return [
        adapt_risk_constraint(item, index=i)
        for i, item in enumerate(risk_profile_constraints)
    ]


# ---------------------------------------------------------------------------
# 4. Strategy-level constraints (list[str]) -> CanonicalConstraint
# ---------------------------------------------------------------------------

def adapt_strategy_constraints(constraints: list[str], *, strategy_id: str = "") -> list[CanonicalConstraint]:
    """Convert strategy architecture string constraints into canonical form."""
    return [
        CanonicalConstraint(
            constraint_id=f"strategy-{strategy_id}-{i}",
            rule_id=f"STRATEGY_CONSTRAINT_{i}",
            domain="strategy",
            source="strategy_library",
            source_engine="StrategyEngine",
            severity="warning",
            role="architecture_constraint",
            kind="soft",
            passed=True,
            message=msg,
        )
        for i, msg in enumerate(constraints)
    ]


# ---------------------------------------------------------------------------
# 5. ConstraintSet assembly
# ---------------------------------------------------------------------------

def build_constraint_set(
    *constraint_lists: list[CanonicalConstraint],
    provenance: dict[str, Any] | None = None,
) -> ConstraintSet:
    """Merge multiple lists of CanonicalConstraint into a single ConstraintSet.

    Detects conflicts: if two constraints share the same rule_id but have
    different values, a ConstraintConflict is recorded.  Neither constraint
    is removed — both are preserved.
    """
    all_constraints: list[CanonicalConstraint] = []
    for clist in constraint_lists:
        all_constraints.extend(clist)

    # Detect conflicts (same rule_id, different values)
    groups: dict[str, list[CanonicalConstraint]] = {}
    for c in all_constraints:
        groups.setdefault(c.rule_id, []).append(c)

    conflicts: list[ConstraintConflict] = []
    for rule_id, group in groups.items():
        unique_values = {repr(c.value) for c in group}
        if len(unique_values) > 1:
            conflicts.append(ConstraintConflict(
                key=rule_id,
                status="unresolved",
                reason="Multiple sources provide different values for the same constraint.",
                sources=[c.source for c in group],
                constraint_ids=[c.constraint_id for c in group],
                hard_constraint_present=any(c.severity == "hard" for c in group),
            ))

    return ConstraintSet(
        constraints=all_constraints,
        conflicts=conflicts,
        provenance=provenance or {},
    )
