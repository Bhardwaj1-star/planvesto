from rules.constraints import (
    DEBT_TO_INCOME_CRITICAL_PERCENT,
    DEBT_TO_INCOME_EXCELLENT_PERCENT,
    DEBT_TO_INCOME_HEALTHY_PERCENT,
    EMERGENCY_RESERVE_CRITICAL_MONTHS,
    EMERGENCY_RESERVE_HEALTHY_MONTHS,
    SAVINGS_RATIO_HEALTHY_PERCENT,
)

from typing import Literal


RULE_SET_VERSION = "2.0"

Status = Literal["excellent", "healthy", "attention", "critical"]

CANONICAL_RATIO_KEYS = (
    "savings_rate",
    "liquid_asset_ratio",
    "debt_to_income_ratio",
    "leverage_ratio",
    "financial_asset_ratio",
    "insurance_coverage_ratio",
    "goal_funding_ratio",
    "future_funding_ratio",
    "required_rate_of_return",
)

CANONICAL_RULE_KEYS = ("expense_coverage", "emergency_coverage")

LEGACY_RATIO_ALIASES = {
    "savings_ratio": "savings_rate",
    "liquid_asset_to_total_asset": "liquid_asset_ratio",
    "insurance_gap_ratio": "insurance_coverage_ratio",
    "emergency_fund_coverage": "emergency_coverage",
}

# Compatibility-only definitions remain explicitly bounded and are never the current
# canonical contract. They are accepted at the boundary and normalized immediately.
COMPATIBILITY_RATIO_DEFINITIONS = {
    "emergency_fund_coverage": {
        "name": "Emergency Fund Coverage",
        "unit": "months",
        "formula": "Liquid Assets / Monthly Expenses",
        "excellent": (9.0, None),
        "healthy": (EMERGENCY_RESERVE_HEALTHY_MONTHS, 9.0),
        "attention": (EMERGENCY_RESERVE_CRITICAL_MONTHS, EMERGENCY_RESERVE_HEALTHY_MONTHS),
        "critical": (None, EMERGENCY_RESERVE_CRITICAL_MONTHS),
    },
    "current_liquidity_ratio": {
        "name": "Current Liquidity Ratio",
        "unit": "x",
        "formula": "Liquid Assets / Short-Term Liabilities",
        "excellent": (1.5, None),
        "healthy": (1.0, 1.5),
        "attention": (0.75, 1.0),
        "critical": (None, 0.75),
    },
    "expense_ratio": {
        "name": "Need Expense Ratio",
        "unit": "%",
        "formula": "Need Expenses / Gross Monthly Income × 100",
        "excellent": (None, 40.0),
        "healthy": (40.0, 50.0),
        "attention": (50.0, 60.0),
        "critical": (60.0, None),
    },
    "solvency_ratio": {
        "name": "Solvency Ratio",
        "unit": "%",
        "formula": "(1 - Leverage Ratio) × 100",
        "excellent": (80.0, None),
        "healthy": (70.0, 80.0),
        "attention": (50.0, 70.0),
        "critical": (None, 50.0),
    },
}

# Final MoneyWheel ratio set. Thresholds remain versioned planning baselines.
RULES = {
    "savings_rate": {"name": "Savings Rate", "unit": "%", "formula": "(Income - Expenses) / Income × 100", "excellent": (30.0, None), "healthy": (SAVINGS_RATIO_HEALTHY_PERCENT, 30.0), "attention": (10.0, SAVINGS_RATIO_HEALTHY_PERCENT), "critical": (None, 10.0)},
    "liquid_asset_ratio": {"name": "Liquid Asset Ratio", "unit": "%", "formula": "Liquid Assets / Total Assets × 100", "excellent": (25.0, None), "healthy": (15.0, 25.0), "attention": (10.0, 15.0), "critical": (None, 10.0)},
    "debt_to_income_ratio": {"name": "Debt-to-Income Ratio", "unit": "%", "formula": "Monthly Debt Payments / Gross Monthly Income × 100", "excellent": (None, DEBT_TO_INCOME_EXCELLENT_PERCENT), "healthy": (DEBT_TO_INCOME_EXCELLENT_PERCENT, DEBT_TO_INCOME_HEALTHY_PERCENT), "attention": (30.0, DEBT_TO_INCOME_CRITICAL_PERCENT), "critical": (DEBT_TO_INCOME_CRITICAL_PERCENT, None)},
    "leverage_ratio": {"name": "Leverage Ratio", "unit": "%", "formula": "Total Liabilities / Total Assets × 100", "excellent": (None, 20.0), "healthy": (20.0, 30.0), "attention": (30.0, 50.0), "critical": (50.0, None)},
    "financial_asset_ratio": {"name": "Financial Asset Ratio", "unit": "%", "formula": "Financial Assets / Total Assets × 100", "excellent": (70.0, None), "healthy": (50.0, 70.0), "attention": (30.0, 50.0), "critical": (None, 30.0)},
    "insurance_coverage_ratio": {"name": "Insurance Coverage Ratio", "unit": "%", "formula": "Existing Sum Assured / Required Insurance Cover × 100", "excellent": (80.0, None), "healthy": (60.0, 80.0), "attention": (40.0, 60.0), "critical": (None, 40.0)},
    "goal_funding_ratio": {"name": "Goal Funding Ratio", "unit": "%", "formula": "Current Goal Funding / Goal Target Amount × 100", "excellent": (100.0, None), "healthy": (80.0, 100.0), "attention": (50.0, 80.0), "critical": (None, 50.0)},
    "future_funding_ratio": {"name": "Future Funding Ratio", "unit": "%", "formula": "Projected Goal Funding / Future Goal Target × 100", "excellent": (100.0, None), "healthy": (80.0, 100.0), "attention": (50.0, 80.0), "critical": (None, 50.0)},
    "required_rate_of_return": {"name": "Required Rate of Return", "unit": "%", "formula": "(Future Goal Target / Current Goal Funding)^(1 / Goal Duration Years) - 1 × 100", "excellent": (None, 8.0), "healthy": (8.0, 12.0), "attention": (12.0, 15.0), "critical": (15.0, None)},
    "emergency_coverage": {"name": "Emergency Coverage", "unit": "months", "formula": "Liquid Assets / Essential Monthly Expenses", "excellent": (9.0, None), "healthy": (6.0, 9.0), "attention": (3.0, 6.0), "critical": (None, 3.0)},
    "expense_coverage": {"name": "Expense Coverage", "unit": "months", "formula": "Liquid Assets / Monthly Expenses", "excellent": (9.0, None), "healthy": (6.0, 9.0), "attention": (3.0, 6.0), "critical": (None, 3.0)},
}
RULES.update(COMPATIBILITY_RATIO_DEFINITIONS)

RULE_DEFINITIONS = {
    "expense_coverage": {
        "name": "Expense Coverage",
        "unit": "months",
        "formula": "Liquid Assets / Monthly Expenses",
    },
    "emergency_coverage": {
        "name": "Emergency Coverage",
        "unit": "months",
        "formula": "Liquid Assets / Essential Monthly Expenses",
    },
}


def canonicalize_metric_key(key: str | None) -> str:
    if key is None:
        raise KeyError("Metric key is required.")
    normalized = str(key).strip()
    if normalized in CANONICAL_RATIO_KEYS or normalized in CANONICAL_RULE_KEYS:
        return normalized
    mapped = LEGACY_RATIO_ALIASES.get(normalized)
    if mapped is not None:
        return mapped
    if normalized in RULES:
        return normalized
    return normalized


def classify(key: str, value: float) -> Status:
    canonical_key = canonicalize_metric_key(key)
    rule = RULES[canonical_key]
    for status in ("excellent", "healthy", "attention", "critical"):
        lower, upper = rule[status]
        if lower is not None and value < lower:
            continue
        if upper is not None and value >= upper:
            continue
        return status
    raise ValueError(f"Unable to classify Moneywheel ratio: {key}={value}")
