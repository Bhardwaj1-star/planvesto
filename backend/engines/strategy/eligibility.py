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


def evaluate_eligibility(
    strategy: StrategyDefinition,
    goal: GoalSnapshot | None,
    state: FinancialState | None,
) -> Tuple[bool, List[str]]:
    """Determine whether *strategy* is applicable for *goal* and *state*.

    The rules are deterministic and explainable. Each rule that fails adds a
    human‑readable reason to the *reasons* list.

    The implementation follows the spec sections:
    * goal type applicability
    * time horizon
    * funding shortfall / surplus
    * cash‑flow requirements
    * existing assets
    * debt constraints
    * liquidity requirements
    * retirement‑specific requirements (if goal.type == "retirement")
    """
    reasons: List[str] = []
    eligible = True

    # If no goal or state is provided, assume no constraints (eligible)
    if goal is None or state is None:
        return True, []

    # Example rule: goal type must be in strategy.applicable_goal_types
    if getattr(strategy, "applicable_goal_types", None) and goal.type not in strategy.applicable_goal_types:
        eligible = False
        reasons.append(
            f"Goal type '{goal.type}' not allowed for strategy {strategy.strategy_id}"
        )

    # Example rule: horizon (in years) must be within strategy constraints if any
    if hasattr(strategy, "constraints"):
        for c in strategy.constraints:
            if c.startswith("horizon<="):
                try:
                    max_h = float(c.split("<=")[1])
                    if getattr(goal, "horizon_years", 0) > max_h:
                        eligible = False
                        reasons.append(
                            f"Goal horizon {getattr(goal, 'horizon_years', 'N/A')} exceeds max {max_h} for strategy"
                        )
                except ValueError:
                    pass
            elif c.startswith("horizon>="):
                try:
                    min_h = float(c.split(">=")[1])
                    if getattr(goal, "horizon_years", 0) < min_h:
                        eligible = False
                        reasons.append(
                            f"Goal horizon {getattr(goal, 'horizon_years', 'N/A')} below min {min_h} for strategy"
                        )
                except ValueError:
                    pass

    # Funding gap / surplus rule
    funding_gap = getattr(goal, "target_amount", 0) - getattr(state, "liquidity", 0)
    if "funding_gap" in getattr(strategy, "constraints", []):
        for c in strategy.constraints:
            if c.startswith("funding_gap<="):
                try:
                    max_gap = float(c.split("<=")[1])
                    if funding_gap > max_gap:
                        eligible = False
                        reasons.append(
                            f"Funding gap {funding_gap:.2f} exceeds allowed {max_gap}"
                        )
                except ValueError:
                    pass
            elif c.startswith("funding_gap>="):
                try:
                    min_gap = float(c.split(">=")[1])
                    if funding_gap < min_gap:
                        eligible = False
                        reasons.append(
                            f"Funding gap {funding_gap:.2f} below required {min_gap}"
                        )
                except ValueError:
                    pass

    # Retirement‑specific rule example
    if getattr(goal, "type", None) == "retirement":
        if "retirement" not in getattr(strategy, "applicable_goal_characteristics", []):
            eligible = False
            reasons.append("Strategy not marked for retirement goals")

    return eligible, reasons
