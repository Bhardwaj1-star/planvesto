from __future__ import annotations

from typing import Any, Literal
from pydantic import BaseModel, Field
from engines.orchestration.models import GoalPriorityLevel

ConstraintSeverity = Literal["hard", "warning", "info"]
RatioStatus = Literal["excellent", "healthy", "attention", "critical"]


class FinancialRatioResult(BaseModel):
    ratio_key: str
    name: str
    value: float | None = None
    unit: str
    status: RatioStatus | None = None
    benchmark: str = ""
    evidence: dict[str, Any] = Field(default_factory=dict)


class ConstraintCheckResult(BaseModel):
    rule_id: str
    goal_id: str | None = None
    severity: ConstraintSeverity
    passed: bool
    message: str
    suggested_override_priority: GoalPriorityLevel | None = None
    override_reason: str | None = None
    ratio_evidence: dict[str, Any] = Field(default_factory=dict)


class RatioConstraintAssessment(BaseModel):
    ratios: list[FinancialRatioResult] = Field(default_factory=list)
    constraints: list[ConstraintCheckResult] = Field(default_factory=list)
    hard_constraints: list[ConstraintCheckResult] = Field(default_factory=list)
    warnings: list[ConstraintCheckResult] = Field(default_factory=list)
    suggested_overrides: dict[str, dict[str, Any]] = Field(default_factory=dict)

    @property
    def has_overrides(self) -> bool:
        return bool(self.suggested_overrides)


# ---------------------------------------------------------------------------
# Canonical Constraints Layer
# ---------------------------------------------------------------------------

ConstraintDomain = Literal[
    "financial_ratio",      # MoneyWheel / ratio evaluator
    "risk_capacity",        # Risk Profiler capacity constraints
    "risk_tolerance",       # Risk Profiler behavioral constraints
    "risk_required",        # Risk Profiler canonical risk required
    "goal_diagnostic",      # RuleEngine goal-level diagnostics
    "goal_eligibility",     # RuleEngine hard constraints on goals
    "strategy",             # Strategy-level constraints from library
    "investment",           # Investment engine constraints
    "declared",             # Investor-declared constraints
]

ConstraintRole = Literal[
    "hard_constraint",        # Blocks downstream processing
    "eligibility",            # Determines strategy eligibility
    "ranking_input",          # Influences strategy ranking
    "recommendation_only",    # Advisory, shown in recommendation
    "architecture_constraint", # Constrains strategy architecture
    "explanatory_evidence",   # Diagnostic / informational
]


class CanonicalConstraint(BaseModel):
    """Unified constraint representation across all domain engines.

    Every constraint in the system can be expressed in this form, regardless
    of which engine produced it.  The canonical model preserves:
      - identity (constraint_id, rule_id)
      - provenance (domain, source, source_engine)
      - semantics (severity, role, kind)
      - value (value, unit)
      - evidence chain
      - validity window
      - pass/fail status
      - goal binding (optional)
      - override suggestions (optional)
    """
    constraint_id: str
    rule_id: str
    domain: ConstraintDomain
    source: str                  # e.g. "financial_state", "observed_behavior", "canonical_calculation"
    source_engine: str           # e.g. "RiskProfilerEngine", "RuleEngine", "FinancialRatioConstraintEvaluator"
    severity: ConstraintSeverity
    role: ConstraintRole = "explanatory_evidence"
    kind: Literal["hard", "soft", "diagnostic"] = "soft"
    passed: bool = True
    message: str = ""
    value: float | None = None
    unit: str | None = None
    goal_id: str | None = None
    evidence: dict[str, Any] = Field(default_factory=dict)
    confidence: float = 1.0
    validity: dict[str, Any] = Field(default_factory=lambda: {"status": "valid", "valid_from": None, "valid_until": None})
    suggested_override_priority: GoalPriorityLevel | None = None
    override_reason: str | None = None


class ConstraintConflict(BaseModel):
    """Records when two or more constraints disagree on the same key."""
    key: str
    status: str = "unresolved"
    reason: str = ""
    sources: list[str] = Field(default_factory=list)
    constraint_ids: list[str] = Field(default_factory=list)
    hard_constraint_present: bool = False


class ConstraintSet(BaseModel):
    """Centralized container aggregating canonical constraints from all domains.

    This is the single interface consumed by the Strategy Engine and
    downstream planning layers.  It preserves every constraint from
    every source, detects conflicts, and provides typed accessors.
    """
    constraints: list[CanonicalConstraint] = Field(default_factory=list)
    conflicts: list[ConstraintConflict] = Field(default_factory=list)
    provenance: dict[str, Any] = Field(default_factory=dict)

    # ---- typed accessors ----
    @property
    def hard_constraints(self) -> list[CanonicalConstraint]:
        return [c for c in self.constraints if c.severity == "hard" and not c.passed]

    @property
    def warnings(self) -> list[CanonicalConstraint]:
        return [c for c in self.constraints if c.severity == "warning"]

    @property
    def info(self) -> list[CanonicalConstraint]:
        return [c for c in self.constraints if c.severity == "info"]

    @property
    def failed(self) -> list[CanonicalConstraint]:
        return [c for c in self.constraints if not c.passed]

    @property
    def has_hard_failures(self) -> bool:
        return any(c.severity == "hard" and not c.passed for c in self.constraints)

    def by_domain(self, domain: str) -> list[CanonicalConstraint]:
        return [c for c in self.constraints if c.domain == domain]

    def by_goal(self, goal_id: str) -> list[CanonicalConstraint]:
        return [c for c in self.constraints if c.goal_id == goal_id]

    def by_role(self, role: str) -> list[CanonicalConstraint]:
        return [c for c in self.constraints if c.role == role]

    def suggested_overrides(self) -> dict[str, dict[str, Any]]:
        overrides: dict[str, dict[str, Any]] = {}
        for c in self.constraints:
            if c.suggested_override_priority and c.goal_id:
                overrides[c.goal_id] = {
                    "resolved_priority": c.suggested_override_priority,
                    "reason": c.override_reason or c.message,
                }
        return overrides

