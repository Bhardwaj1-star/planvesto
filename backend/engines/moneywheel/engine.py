from datetime import datetime, timezone

from models.moneywheel import MoneywheelInput, MoneywheelRatio, MoneywheelResult
from rules.moneywheel import RULE_SET_VERSION, RULES, classify


class MoneywheelEngine:
    """Calculates the nine Moneywheel ratios without inventing missing data."""

    def build(self, data: MoneywheelInput) -> MoneywheelResult:
        ratios = [
            self._ratio(data, "savings_ratio", data.savings, data.gross_monthly_income, "savings / income * 100"),
            self._ratio(data, "expense_ratio", data.essential_monthly_expenses, data.gross_monthly_income, "essential expenses / income * 100"),
            self._ratio(data, "emergency_fund_coverage", data.liquid_assets, data.monthly_expenses, "liquid assets / monthly expenses"),
            self._ratio(data, "current_liquidity_ratio", data.liquid_assets, data.short_term_liabilities, "liquid assets / short-term liabilities"),
            self._ratio(data, "debt_to_income_ratio", data.monthly_debt_payments, data.gross_monthly_income, "monthly debt payments / income * 100"),
            self._ratio(data, "leverage_ratio", data.total_liabilities, data.total_assets, "total liabilities / total assets * 100"),
            self._ratio(data, "liquid_asset_to_total_asset", data.liquid_assets, data.total_assets, "liquid assets / total assets * 100"),
            self._solvency_ratio(data),
            self._ratio(data, "financial_asset_ratio", data.financial_assets, data.total_assets, "financial assets / total assets * 100"),
        ]
        available_statuses = [r.status for r in ratios if r.available]
        return MoneywheelResult(
            planning_unit_id=data.planning_unit_id,
            status="incomplete" if len(available_statuses) < 9 else "healthy",
            ratios=ratios,
            rule_set_version=RULE_SET_VERSION,
            calculated_at=datetime.now(timezone.utc).isoformat(),
            metadata={"overall_status": "not_defined"},
        )

    def _solvency_ratio(self, data: MoneywheelInput) -> MoneywheelRatio:
        if data.total_assets is None or data.total_assets == 0 or data.total_liabilities is None:
            return self._unavailable("solvency_ratio", "Total assets and liabilities are required; total assets cannot be zero.")
        value = (1 - (data.total_liabilities / data.total_assets)) * 100
        return self._make_ratio("solvency_ratio", value)

    def _ratio(self, data, key: str, numerator: float | None, denominator: float | None, expression: str):
        if numerator is None or denominator is None:
            return self._unavailable(key, "Required input is missing.")
        if denominator == 0:
            return self._unavailable(key, "Ratio denominator is zero; ratio is not defined.")
        value = numerator / denominator
        if RULES[key]["unit"] == "%":
            value *= 100
        return self._make_ratio(key, value, expression)

    @staticmethod
    def _unavailable(key: str, reason: str) -> MoneywheelRatio:
        rule = RULES[key]
        return MoneywheelRatio(
            key=key, name=rule["name"], value=None, unit=rule["unit"],
            status="unavailable", formula=rule["formula"], explanation=reason, available=False,
        )

    @staticmethod
    def _make_ratio(key: str, value: float, expression: str | None = None) -> MoneywheelRatio:
        rule = RULES[key]
        status = classify(key, value)
        explanation = f"{rule['name']} is {status} at {value:.2f}{rule['unit']}."
        return MoneywheelRatio(
            key=key, name=rule["name"], value=round(value, 4), unit=rule["unit"],
            status=status, formula=rule["formula"], explanation=explanation,
        )
