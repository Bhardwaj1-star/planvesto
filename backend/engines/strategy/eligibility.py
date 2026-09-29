"""Strategy eligibility rules.

Eligibility is distinct from strategy ranking. Every strategy that reaches the
recommendation layer must be classified against the approved eligibility fits.

Approved fit outcomes:
    PASS        -> strategy can be recommended directly.
    CONDITIONAL -> strategy can be considered only with explicit required changes.
    FAIL        -> strategy cannot be recommended.

The module intentionally does not invent financial-ratio thresholds. Numeric
requirements must come from the strategy/goal calculation layer or an explicit
fit assessment supplied in the financial context.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, List, Tuple

from models.strategy import StrategyDefinition
from models.defined_goal import DefinedGoal as GoalSnapshot
from engines.rules.engine import GOAL_TYPE_ALIASES


class EligibilityStatus(str, Enum):
    PASS = "pass"
    CONDITIONAL = "conditional"
    FAIL = "fail"


ELIGIBILITY_FITS: tuple[str, ...] = (
    "cashflow_fit",
    "liquidity_fit",
    "debt_fit",
    "asset_resource_fit",
    "risk_capacity_fit",
    "goal_constraint_fit",
    "multi_goal_conflict_fit",
    "implementation_fit",
)


@dataclass(frozen=True)
class EligibilityFitResult:
    fit: str
    status: EligibilityStatus
    reason: str = ""
    required_changes: tuple[str, ...] = ()
    data: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class EligibilityAssessment:
    """Complete eligibility assessment for one strategy."""

    results: tuple[EligibilityFitResult, ...]

    @property
    def status(self) -> EligibilityStatus:
        statuses = {result.status for result in self.results}
        if EligibilityStatus.FAIL in statuses:
            return EligibilityStatus.FAIL
        if EligibilityStatus.CONDITIONAL in statuses:
            return EligibilityStatus.CONDITIONAL
        return EligibilityStatus.PASS

    @property
    def failed_fits(self) -> tuple[EligibilityFitResult, ...]:
        return tuple(r for r in self.results if r.status == EligibilityStatus.FAIL)

    @property
    def conditional_fits(self) -> tuple[EligibilityFitResult, ...]:
        return tuple(r for r in self.results if r.status == EligibilityStatus.CONDITIONAL)

    @property
    def required_changes(self) -> tuple[str, ...]:
        return tuple(
            change
            for result in self.results
            for change in result.required_changes
        )

    @property
    def eligible_for_recommendation(self) -> bool:
        return self.status != EligibilityStatus.FAIL


def _fit_input(context: dict[str, Any], strategy_id: str, fit: str) -> dict[str, Any] | None:
    """Read an explicit calculated fit assessment without inventing thresholds."""
    root = context.get("eligibility_fits") or {}
    if not isinstance(root, dict):
        return None
    strategy_values = root.get(strategy_id)
    if not isinstance(strategy_values, dict):
        return None
    value = strategy_values.get(fit)
    if isinstance(value, dict):
        return value
    return None


def _build_fit_result(fit: str, value: dict[str, Any] | None) -> EligibilityFitResult:
    """Normalize an upstream fit calculation into the frozen Pass/Conditional/Fail contract."""
    if value is None:
        # Missing fit evidence is not silently treated as Pass. The strategy can
        # still be evaluated, but it must explicitly declare the missing evidence.
        return EligibilityFitResult(
            fit=fit,
            status=EligibilityStatus.CONDITIONAL,
            reason=f"{fit} assessment is unavailable",
            required_changes=(f"Provide {fit} assessment before implementation",),
        )

    raw_status = str(value.get("status", "")).strip().lower()
    try:
        status = EligibilityStatus(raw_status)
    except ValueError as exc:
        raise ValueError(f"Invalid {fit} status: {raw_status!r}") from exc

    changes = value.get("required_changes") or value.get("required_change") or ()
    if isinstance(changes, str):
        changes = (changes,)
    else:
        changes = tuple(str(change) for change in changes)

    return EligibilityFitResult(
        fit=fit,
        status=status,
        reason=str(value.get("reason", "")),
        required_changes=changes,
        data=dict(value.get("data") or {}),
    )


def evaluate_eligibility_fits(
    strategy: StrategyDefinition,
    *,
    financial_context: dict[str, Any] | None = None,
) -> EligibilityAssessment:
    """Evaluate all eight frozen eligibility fits for a strategy.

    The financial-state/goal calculation layer is responsible for producing the
    actual fit evidence. This function enforces the business contract and keeps
    the result deterministic: any failed fit fails the strategy; otherwise any
    conditional fit makes the strategy conditional; otherwise it passes.
    """
    context = dict(financial_context or {})
    results = tuple(
        _build_fit_result(fit, _fit_input(context, strategy.strategy_id, fit))
        for fit in ELIGIBILITY_FITS
    )
    return EligibilityAssessment(results=results)


def _metric_available(context: dict[str, Any], key: str) -> bool:
    raw = context.get(key)
    if isinstance(raw, dict):
        return bool(raw.get("available", True)) and raw.get("value") is not None
    return raw is not None


def _required_input_available(name: str, goal: GoalSnapshot, context: dict[str, Any]) -> bool:
    """Resolve library required_inputs against the defined goal/financial context."""
    goal_fields = {"future_target", "funding_gap", "duration_years", "funding_status", "goal_priority", "goal_priorities", "goal_amount", "income_need"}
    if name in goal_fields:
        if name == "goal_priority":
            return bool(getattr(goal, "priority", None))
        if name == "goal_priorities":
            return bool(context.get(name) or context.get("goals"))
        if name == "goal_amount":
            return getattr(goal, "future_target", None) is not None
        return getattr(goal, name, None) is not None

    if not context:
        return True

    aliases = {
        "financial_state": ("financial_state", "financial_context"),
        "surplus": ("investable_surplus_monthly", "investable_surplus_annual"),
        "liabilities": ("total_liabilities", "liability_breakdown"),
        "emi_burden": ("emi_burden_monthly",),
        "assets": ("total_assets", "asset_breakdown"),
        "income": ("income_monthly", "income_annual"),
    }
    candidates = aliases.get(name, (name,))
    return any(_metric_available(context, key) or bool(context.get(key)) for key in candidates)


def evaluate_eligibility(
    strategy: StrategyDefinition,
    goal: GoalSnapshot | None,
    state: Any | None = None,
    financial_context: dict[str, Any] | None = None,
    rule_assessment: Any | None = None,
) -> Tuple[bool, List[str]]:
    """Determine whether *strategy* is eligible for *goal* and current context."""
    reasons: List[str] = []
    eligible = True
    context = dict(financial_context or {})
    if goal is None:
        return True, []

    raw_type = (getattr(goal, "goal_type", getattr(goal, "type", "")) or "").strip().lower()
    canonical_type = GOAL_TYPE_ALIASES.get(raw_type, raw_type)
    duration_years = float(getattr(goal, "duration_years", getattr(goal, "horizon_years", 0)) or 0.0)

    strategy_types = [GOAL_TYPE_ALIASES.get(t.strip().lower(), t.strip().lower()) for t in getattr(strategy, "applicable_goal_types", [])]
    if strategy_types and canonical_type and canonical_type not in strategy_types and "other" not in strategy_types:
        eligible = False
        reasons.append(f"Goal type '{raw_type}' not allowed for strategy {strategy.strategy_id}")

    for c in getattr(strategy, "constraints", []) or []:
        if c.startswith("horizon<="):
            try:
                max_h = float(c.split("<=", 1)[1])
                if duration_years > max_h:
                    eligible = False
                    reasons.append(f"Goal horizon {duration_years:g} exceeds max {max_h:g} for strategy")
            except ValueError:
                pass
        elif c.startswith("horizon>="):
            try:
                min_h = float(c.split(">=", 1)[1])
                if duration_years < min_h:
                    eligible = False
                    reasons.append(f"Goal horizon {duration_years:g} below min {min_h:g} for strategy")
            except ValueError:
                pass
        elif c.startswith("funding_gap<="):
            try:
                max_gap = float(c.split("<=", 1)[1])
                if float(getattr(goal, "funding_gap", 0.0) or 0.0) > max_gap:
                    eligible = False
                    reasons.append(f"Funding gap {float(getattr(goal, 'funding_gap', 0.0) or 0.0):.2f} exceeds allowed {max_gap}")
            except ValueError:
                pass
        elif c.startswith("funding_gap>="):
            try:
                min_gap = float(c.split(">=", 1)[1])
                if float(getattr(goal, "funding_gap", 0.0) or 0.0) < min_gap:
                    eligible = False
                    reasons.append(f"Funding gap below required {min_gap}")
            except ValueError:
                pass

    missing_inputs = [name for name in getattr(strategy, "required_inputs", []) if not _required_input_available(name, goal, context)]
    if missing_inputs:
        eligible = False
        reasons.append("Missing required inputs: " + ", ".join(missing_inputs))

    if rule_assessment is not None:
        for result in getattr(rule_assessment, "hard_constraints", ()):
            if not result.passed:
                eligible = False
                reasons.append(result.message)

    if canonical_type == "retirement":
        chars = [c.strip().lower() for c in getattr(strategy, "applicable_goal_characteristics", [])]
        if "retirement" not in chars and "retirement" not in strategy_types:
            eligible = False
            reasons.append("Strategy not marked for retirement goals")

    return eligible, reasons
