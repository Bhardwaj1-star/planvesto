from dataclasses import dataclass
from typing import Any

from models.defined_goal import DefinedGoal
from models.strategy import StrategyDefinition


GOAL_TYPE_ALIASES = {
    "retirement/financial freedom": "retirement",
    "education": "child education",
    "marriage": "child marriage",
    "dream home": "home purchase",
    "vacation": "travel",
    "others": "other",
    "passive income": "other",
    "debt repayment": "other",
    "philanthropy": "other",
}


@dataclass(frozen=True)
class RuleEvaluation:
    strategy_id: str
    eligible: bool
    goal_type_match: bool
    matched_characteristics: tuple[str, ...] = ()
    unmet_characteristics: tuple[str, ...] = ()
    reasons: tuple[str, ...] = ()
    missing_inputs: tuple[str, ...] = ()


@dataclass(frozen=True)
class RuleResult:
    rule_id: str
    passed: bool
    severity: str
    message: str
    evidence: dict[str, Any]


@dataclass(frozen=True)
class RuleAssessment:
    diagnostics: tuple[RuleResult, ...]
    hard_constraints: tuple[RuleResult, ...]
    soft_constraints: tuple[RuleResult, ...]

    @property
    def eligible(self) -> bool:
        return not any(not result.passed for result in self.hard_constraints)


class StrategyRuleEngine:
    """Evaluates library-level strategy rules without ranking or architecture decisions."""

    @staticmethod
    def canonical_goal_type(value: str | None) -> str:
        clean = (value or "").strip().lower()
        return GOAL_TYPE_ALIASES.get(clean, clean)

    def evaluate(
        self,
        strategy: StrategyDefinition,
        goal_type: str | None = None,
        defined_goal: DefinedGoal | None = None,
        financial_context: dict | None = None,
    ) -> RuleEvaluation:
        clean_goal_type = self.canonical_goal_type(
            defined_goal.goal_type if defined_goal is not None else goal_type
        )
        applicable_types = {
            self.canonical_goal_type(value) for value in strategy.applicable_goal_types
        }
        goal_type_match = bool(clean_goal_type and clean_goal_type in applicable_types)
        if not goal_type_match:
            return RuleEvaluation(
                strategy_id=strategy.strategy_id,
                eligible=False,
                goal_type_match=False,
                reasons=("Goal type is not applicable to this strategy.",),
            )

        if defined_goal is None or not strategy.applicable_goal_characteristics:
            return RuleEvaluation(
                strategy_id=strategy.strategy_id,
                eligible=True,
                goal_type_match=True,
                reasons=("Goal type is applicable.",),
            )

        signals = {
            "shortfall": defined_goal.funding_status.lower() == "shortfall",
            "on_track": defined_goal.funding_status.lower() == "on track",
            "overfunded": defined_goal.funding_status.lower() == "overfunded",
            "near_term": defined_goal.duration_years <= 5,
            "long_term": defined_goal.duration_years >= 7,
            "fixed_timeline": defined_goal.flexibility.lower() == "fixed",
            "flexible_timeline": defined_goal.flexibility.lower() != "fixed",
            "high_priority": defined_goal.priority.lower() in {"critical", "high"},
        }
        characteristics = tuple(c.strip().lower() for c in strategy.applicable_goal_characteristics)
        matched = tuple(c for c in characteristics if signals.get(c, False))
        unmet = tuple(c for c in characteristics if not signals.get(c, False))

        return RuleEvaluation(
            strategy_id=strategy.strategy_id,
            eligible=bool(matched),
            goal_type_match=True,
            matched_characteristics=matched,
            unmet_characteristics=unmet,
            reasons=(
                "At least one applicable goal characteristic matched."
                if matched
                else "No applicable goal characteristic matched.",
            ),
        )


class RuleEngine:
    """Goal diagnostics and constraint evaluation consumed by downstream engines."""

    @staticmethod
    def _metric_value(context: dict[str, Any], key: str) -> float | None:
        raw = context.get(key)
        if isinstance(raw, dict):
            if not raw.get("available", True):
                return None
            raw = raw.get("value")
        if raw is None:
            return None
        try:
            return float(raw)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _status(value: float, excellent_floor: float | None, healthy_floor: float | None, inverse: bool = False) -> str:
        """Return only stable three-state diagnostics: excellent, healthy, critical."""
        if inverse:
            if excellent_floor is not None and value < excellent_floor:
                return "excellent"
            if healthy_floor is not None and value < healthy_floor:
                return "healthy"
            return "critical"
        if excellent_floor is not None and value >= excellent_floor:
            return "excellent"
        if healthy_floor is not None and value >= healthy_floor:
            return "healthy"
        return "critical"

    @staticmethod
    def _health_diagnostic(
        context: dict[str, Any],
        diagnostics: list[RuleResult],
        key: str,
        rule_id: str,
        label: str,
        excellent_floor: float | None,
        healthy_floor: float | None,
        inverse: bool = False,
    ) -> None:
        value = RuleEngine._metric_value(context, key)
        if value is None:
            diagnostics.append(RuleResult(rule_id, True, "diagnostic", f"{label} is unavailable; no health conclusion was made.", {"available": False}))
            return
        status = RuleEngine._status(value, excellent_floor, healthy_floor, inverse)
        diagnostics.append(RuleResult(rule_id, status != "critical", "diagnostic", f"{label} is {status}.", {"value": value, "status": status, "source_metric": key}))

    def assess(
        self,
        goal: DefinedGoal,
        financial_context: dict[str, Any] | None = None,
    ) -> RuleAssessment:
        context = financial_context or {}
        diagnostics: list[RuleResult] = []
        hard: list[RuleResult] = []
        soft: list[RuleResult] = []

        if goal.duration_years <= 0:
            hard.append(RuleResult("goal-positive-horizon", False, "hard", "Goal horizon must be positive.", {"duration_years": goal.duration_years}))
        else:
            diagnostics.append(RuleResult("goal-positive-horizon", True, "diagnostic", "Goal horizon is valid.", {"duration_years": goal.duration_years}))

        if goal.future_target <= 0:
            hard.append(RuleResult("goal-positive-target", False, "hard", "Goal target must be positive.", {"future_target": goal.future_target}))
        else:
            diagnostics.append(RuleResult("goal-positive-target", True, "diagnostic", "Goal target is valid.", {"future_target": goal.future_target}))

        if goal.priority.strip().lower() in {"critical", "high"}:
            soft.append(RuleResult("priority-sensitive", True, "soft", "Goal priority requires explicit trade-off consideration.", {"priority": goal.priority}))

        if goal.flexibility.strip().lower() == "fixed":
            soft.append(RuleResult("fixed-timeline", True, "soft", "Fixed timeline limits timing flexibility.", {"flexibility": goal.flexibility}))

        monthly_surplus = self._metric_value(context, "investable_surplus_monthly")
        if monthly_surplus is not None:
            passed = monthly_surplus >= 0
            soft.append(RuleResult("surplus-health", passed, "soft", "Current monthly surplus is non-negative." if passed else "Current monthly surplus is negative.", {"investable_surplus_monthly": monthly_surplus}))
        else:
            diagnostics.append(RuleResult("surplus-health", True, "diagnostic", "Monthly surplus is unavailable; no surplus constraint was evaluated.", {"available": False}))

        self._health_diagnostic(context, diagnostics, "emergency_fund_coverage", "emergency-reserve-health", "Emergency reserve coverage", 9.0, 6.0)
        self._health_diagnostic(context, diagnostics, "current_liquidity_ratio", "liquidity-health", "Current liquidity", 1.5, 1.0)
        self._health_diagnostic(context, diagnostics, "debt_to_income_ratio", "debt-pressure-health", "Debt-to-income", 20.0, 30.0, True)
        self._health_diagnostic(context, diagnostics, "leverage_ratio", "leverage-health", "Leverage", 20.0, 30.0, True)

        return RuleAssessment(tuple(diagnostics), tuple(hard), tuple(soft))
