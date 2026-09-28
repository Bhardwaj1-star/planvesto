# Eligibility Engine for Strategy Conversion
"""
Implements deterministic rule evaluation as described in STRATEGY_CONVERSION_SPEC.md
Section 3.4 – Rule / Eligibility Engine.
The engine returns a tuple (is_eligible: bool, reasons: list[str]).
"""

from typing import List, Tuple

from models.strategy import StrategyDefinition
from models.defined_goal import DefinedGoal as GoalSnapshot
from models.financial_state import FinancialState
from engines.rules.engine import GOAL_TYPE_ALIASES


def evaluate_eligibility(
    strategy: StrategyDefinition,
    goal: GoalSnapshot | None,
    state: FinancialState | None,
) -> Tuple[bool, List[str]]:
    """Determine whether *strategy* is applicable for *goal* and *state*.

    The rules are deterministic and explainable. Each rule that fails adds a
    human-readable reason to the *reasons* list.
    """
    reasons: List[str] = []
    eligible = True

    # If no goal is provided, assume no goal-level constraints
    if goal is None:
        return True, []

    raw_type = (getattr(goal, "goal_type", getattr(goal, "type", "")) or "").strip().lower()
    canonical_type = GOAL_TYPE_ALIASES.get(raw_type, raw_type)
    duration_years = float(getattr(goal, "duration_years", getattr(goal, "horizon_years", 0)) or 0.0)

    # Goal type applicability
    strategy_types = [
        GOAL_TYPE_ALIASES.get(t.strip().lower(), t.strip().lower())
        for t in getattr(strategy, "applicable_goal_types", [])
    ]
    if strategy_types and canonical_type and canonical_type not in strategy_types and "other" not in strategy_types:
        eligible = False
        reasons.append(f"Goal type '{raw_type}' not allowed for strategy {strategy.strategy_id}")

    # Horizon constraints
    if hasattr(strategy, "constraints") and strategy.constraints:
        for c in strategy.constraints:
            if c.startswith("horizon<="):
                try:
                    max_h = float(c.split("<=")[1])
                    if duration_years > max_h:
                        eligible = False
                        reasons.append(
                            f"Goal horizon {duration_years:g} exceeds max {max_h:g} for strategy"
                        )
                except ValueError:
                    pass
            elif c.startswith("horizon>="):
                try:
                    min_h = float(c.split(">=")[1])
                    if duration_years < min_h:
                        eligible = False
                        reasons.append(
                            f"Goal horizon {duration_years:g} below min {min_h:g} for strategy"
                        )
                except ValueError:
                    pass

    # Financial state constraints (if state is present)
    if state is not None:
        funding_gap = getattr(goal, "funding_gap", getattr(goal, "target_amount", 0) - getattr(state, "liquidity", 0))
        for c in getattr(strategy, "constraints", []):
            if c.startswith("funding_gap<="):
                try:
                    max_gap = float(c.split("<=")[1])
                    if funding_gap > max_gap:
                        eligible = False
                        reasons.append(f"Funding gap {funding_gap:.2f} exceeds allowed {max_gap}")
                except ValueError:
                    pass
            elif c.startswith("funding_gap>="):
                try:
                    min_gap = float(c.split(">=")[1])
                    if funding_gap < min_gap:
                        eligible = False
                        reasons.append(f"Funding gap {funding_gap:.2f} below required {min_gap}")
                except ValueError:
                    pass

    # Retirement-specific rule
    if canonical_type == "retirement":
        chars = getattr(strategy, "applicable_goal_characteristics", [])
        types = [t.strip().lower() for t in getattr(strategy, "applicable_goal_types", [])]
        if "retirement" not in chars and "retirement" not in types:
            eligible = False
            reasons.append("Strategy not marked for retirement goals")

    return eligible, reasons
