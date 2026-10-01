from datetime import datetime, timezone
import math

from models.moneywheel import MoneywheelInput, MoneywheelRatio, MoneywheelResult, MoneywheelRule
from rules.moneywheel import RULE_SET_VERSION, RULES, RULE_DEFINITIONS, classify


class MoneywheelEngine:
    """Calculates the final MoneyWheel ratios and separate coverage rules."""

    def build(self, data: MoneywheelInput) -> MoneywheelResult:
        ratios = [
            self._ratio(data, "savings_rate", data.monthly_surplus, data.gross_monthly_income),
            self._ratio(data, "liquid_asset_ratio", data.liquid_assets, data.total_assets),
            self._ratio(data, "debt_to_income_ratio", data.monthly_debt_payments, data.gross_monthly_income),
            self._ratio(data, "leverage_ratio", data.total_liabilities, data.total_assets),
            self._ratio(data, "financial_asset_ratio", data.financial_assets, data.total_assets),
            self._ratio(data, "insurance_coverage_ratio", data.existing_sum_assured, data.required_insurance_cover),
            self._ratio(data, "goal_funding_ratio", data.current_goal_funding, data.goal_target_amount),
            self._ratio(data, "future_funding_ratio", data.projected_goal_funding, data.future_goal_target),
            self._required_rate_of_return(data),
        ]
        rules = [
            self._coverage_rule(data, "expense_coverage", data.liquid_assets, data.monthly_expenses),
            self._coverage_rule(data, "emergency_coverage", data.liquid_assets, data.essential_monthly_expenses),
        ]
        return MoneywheelResult(
            planning_unit_id=data.planning_unit_id,
            overall_status="incomplete" if any(not r.available for r in ratios) else None,
            ratios=ratios,
            rules=rules,
            rule_set_version=RULE_SET_VERSION,
            calculated_at=datetime.now(timezone.utc).isoformat(),
            metadata={"overall_status": "not_defined"},
        )

    def _required_rate_of_return(self, data: MoneywheelInput) -> MoneywheelRatio:
        key = "required_rate_of_return"
        if data.future_goal_target is None or data.current_goal_funding is None or data.goal_duration_years is None:
            return self._unavailable(key, "Future goal target, current goal funding, and goal duration are required.")
        if data.current_goal_funding == 0:
            return self._unavailable(key, "Current goal funding is zero; required return is not defined.")
        value = ((data.future_goal_target / data.current_goal_funding) ** (1 / data.goal_duration_years) - 1) * 100
        return self._make_ratio(key, value)

    def _ratio(self, data: MoneywheelInput, key: str, numerator: float | None, denominator: float | None):
        if numerator is None or denominator is None:
            return self._unavailable(key, "Required input is missing.")
        if denominator == 0:
            return self._unavailable(key, "Ratio denominator is zero; ratio is not defined.")
        value = numerator / denominator
        if RULES[key]["unit"] == "%":
            value *= 100
        return self._make_ratio(key, value)

    @staticmethod
    def _coverage_rule(
        data: MoneywheelInput,
        key: str,
        numerator: float | None,
        denominator: float | None,
    ) -> MoneywheelRule:
        rule = RULE_DEFINITIONS[key]
        if numerator is None or denominator is None:
            return MoneywheelRule(
                key=key,
                name=rule["name"],
                value=None,
                unit=rule["unit"],
                formula=rule["formula"],
                explanation="Required input is missing.",
                available=False,
            )
        if denominator == 0:
            return MoneywheelRule(
                key=key,
                name=rule["name"],
                value=None,
                unit=rule["unit"],
                formula=rule["formula"],
                explanation="Coverage denominator is zero; coverage is not defined.",
                available=False,
            )
        value = numerator / denominator
        return MoneywheelRule(
            key=key,
            name=rule["name"],
            value=round(value, 4),
            unit=rule["unit"],
            formula=rule["formula"],
            explanation=f"{rule['name']} is {value:.2f} months.",
            available=True,
        )

    @staticmethod
    def _unavailable(key: str, reason: str) -> MoneywheelRatio:
        rule = RULES[key]
        return MoneywheelRatio(
            key=key, name=rule["name"], value=None, unit=rule["unit"],
            status="unavailable", formula=rule["formula"], explanation=reason, available=False,
        )

    @staticmethod
    def _make_ratio(key: str, value: float) -> MoneywheelRatio:
        if not math.isfinite(value):
            return MoneywheelEngine._unavailable(key, "Calculated ratio is not finite.")
        rule = RULES[key]
        status = classify(key, value)
        explanation = f"{rule['name']} is {status} at {value:.2f}{rule['unit']}."
        return MoneywheelRatio(
            key=key, name=rule["name"], value=round(value, 4), unit=rule["unit"],
            status=status, formula=rule["formula"], explanation=explanation,
        )
