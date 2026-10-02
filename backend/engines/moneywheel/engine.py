from datetime import datetime, timezone
import math

from models.moneywheel import MoneywheelInput, MoneywheelRatio, MoneywheelResult, MoneywheelRule
from rules.moneywheel import RULE_SET_VERSION, RULES, RULE_DEFINITIONS, classify


from engines.calculation.canonical import (
    calculate_debt_to_income_ratio,
    calculate_emergency_coverage,
    calculate_expense_coverage,
    calculate_financial_asset_ratio,
    calculate_future_funding_ratio,
    calculate_goal_funding_ratio,
    calculate_insurance_coverage_ratio,
    calculate_leverage_ratio,
    calculate_liquid_asset_ratio,
    calculate_required_rate_of_return,
    calculate_savings_rate,
)


class MoneywheelEngine:
    """Calculates the final MoneyWheel ratios and separate coverage rules."""

    def build(self, data: MoneywheelInput) -> MoneywheelResult:
        ratios = [
            self._ratio(data, "savings_rate", calculate_savings_rate(data.monthly_surplus, data.gross_monthly_income), data.monthly_surplus, data.gross_monthly_income),
            self._ratio(data, "liquid_asset_ratio", calculate_liquid_asset_ratio(data.liquid_assets, data.total_assets), data.liquid_assets, data.total_assets),
            self._ratio(data, "debt_to_income_ratio", calculate_debt_to_income_ratio(data.monthly_debt_payments, data.gross_monthly_income), data.monthly_debt_payments, data.gross_monthly_income),
            self._ratio(data, "leverage_ratio", calculate_leverage_ratio(data.total_liabilities, data.total_assets), data.total_liabilities, data.total_assets),
            self._ratio(data, "financial_asset_ratio", calculate_financial_asset_ratio(data.financial_assets, data.total_assets), data.financial_assets, data.total_assets),
            self._ratio(data, "insurance_coverage_ratio", calculate_insurance_coverage_ratio(data.existing_sum_assured, data.required_insurance_cover), data.existing_sum_assured, data.required_insurance_cover),
            self._ratio(data, "goal_funding_ratio", calculate_goal_funding_ratio(data.current_goal_funding, data.goal_target_amount), data.current_goal_funding, data.goal_target_amount),
            self._ratio(data, "future_funding_ratio", calculate_future_funding_ratio(data.projected_goal_funding, data.future_goal_target), data.projected_goal_funding, data.future_goal_target),
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
        val = calculate_required_rate_of_return(data.future_goal_target, data.current_goal_funding, data.goal_duration_years)
        if val is None:
            return self._unavailable(key, "Unable to calculate required rate of return with given inputs.")
        return self._make_ratio(key, val)

    def _ratio(
        self,
        data: MoneywheelInput,
        key: str,
        calculated_value: float | None,
        numerator: float | None,
        denominator: float | None,
    ) -> MoneywheelRatio:
        if numerator is None or denominator is None:
            return self._unavailable(key, "Required input is missing.")
        if denominator == 0:
            return self._unavailable(key, "Ratio denominator is zero; ratio is not defined.")
        if calculated_value is None:
            return self._unavailable(key, "Ratio is not defined.")
        return self._make_ratio(key, calculated_value)

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
        if key == "emergency_coverage":
            val = calculate_emergency_coverage(numerator, denominator)
        else:
            val = calculate_expense_coverage(numerator, denominator)
        if val is None:
            return MoneywheelRule(
                key=key,
                name=rule["name"],
                value=None,
                unit=rule["unit"],
                formula=rule["formula"],
                explanation="Coverage is not defined.",
                available=False,
            )
        return MoneywheelRule(
            key=key,
            name=rule["name"],
            value=val,
            unit=rule["unit"],
            formula=rule["formula"],
            explanation=f"{rule['name']} is {val:.2f} months.",
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


# Backward-compatible public alias for legacy imports.
MoneyWheelEngine = MoneywheelEngine
