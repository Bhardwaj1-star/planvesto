"""Deterministic eligibility gate for strategy conversion.

Eligibility is deliberately narrower than ranking/recommendation.  A strategy is
rejected only by an explicit hard constraint, goal applicability, horizon/funding
constraint, or missing data that the strategy explicitly declares as required.
Financial-health metrics such as cash-flow, liquidity and debt pressure remain
explanatory/conditional evidence unless the rule engine marks them as hard
constraints; this prevents the builder from silently rejecting a goal that needs
a remediation strategy.
"""

from typing import Any, List, Tuple

from models.strategy import StrategyDefinition
from models.defined_goal import DefinedGoal as GoalSnapshot
from engines.rules.engine import GOAL_TYPE_ALIASES


def _metric_available(context: dict[str, Any], key: str) -> bool:
    raw = context.get(key)
    if isinstance(raw, dict):
        return bool(raw.get("available", True)) and raw.get("value") is not None
    return raw is not None


def _required_input_available(name: str, goal: GoalSnapshot, context: dict[str, Any]) -> bool:
    """Resolve library required_inputs against the defined goal/financial context."""
    goal_fields = {
        "future_target", "funding_gap", "duration_years", "funding_status",
        "goal_priority", "goal_priorities", "goal_amount", "income_need",
    }
    if name in goal_fields:
        if name == "goal_priority":
            return bool(getattr(goal, "priority", None))
        if name == "goal_priorities":
            return bool(context.get(name) or context.get("goals"))
        if name == "goal_amount":
            return getattr(goal, "future_target", None) is not None
        return getattr(goal, name, None) is not None

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

    strategy_types = [
        GOAL_TYPE_ALIASES.get(t.strip().lower(), t.strip().lower())
        for t in getattr(strategy, "applicable_goal_types", [])
    ]
    if strategy_types and canonical_type and canonical_type not in strategy_types and "other" not in strategy_types:
        eligible = False
        reasons.append(f"Goal type '{raw_type}' not allowed for strategy {strategy.strategy_id}")

    constraints = getattr(strategy, "constraints", []) or []
    for c in constraints:
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

    funding_gap = float(
        getattr(goal, "funding_gap", getattr(goal, "target_amount", 0)) or 0.0
    )
    for c in constraints:
        if c.startswith("funding_gap<="):
            try:
                max_gap = float(c.split("<=", 1)[1])
                if funding_gap > max_gap:
                    eligible = False
                    reasons.append(f"Funding gap {funding_gap:.2f} exceeds allowed {max_gap}")
            except ValueError:
                pass
        elif c.startswith("funding_gap>="):
            try:
                min_gap = float(c.split(">=", 1)[1])
                if funding_gap < min_gap:
                    eligible = False
                    reasons.append(f"Funding gap {funding_gap:.2f} below required {min_gap}")
            except ValueError:
                pass

    # A strategy may explicitly declare required inputs. Missing inputs make that
    # strategy ineligible; they are not inferred from strategy names.
    missing_inputs = [
        name for name in getattr(strategy, "required_inputs", [])
        if not _required_input_available(name, goal, context)
    ]
    if missing_inputs:
        eligible = False
        reasons.append("Missing required inputs: " + ", ".join(missing_inputs))

    # Consume only hard constraints from the authoritative rule engine. Soft and
    # diagnostic health findings must not silently disqualify a remediation strategy.
    if rule_assessment is not None:
        for result in getattr(rule_assessment, "hard_constraints", ()):
            if not result.passed:
                eligible = False
                reasons.append(result.message)

    if canonical_type == "retirement":
        chars = getattr(strategy, "applicable_goal_characteristics", [])
        if "retirement" not in [c.strip().lower() for c in chars] and "retirement" not in strategy_types:
            eligible = False
            reasons.append("Strategy not marked for retirement goals")

    return eligible, reasons
