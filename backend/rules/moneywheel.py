from typing import Literal


RULE_SET_VERSION = "2.0"

Status = Literal["excellent", "healthy", "attention", "critical"]


# Final MoneyWheel ratio set. Thresholds remain versioned planning baselines.
RULES = {
    "savings_rate": {"name": "Savings Rate", "unit": "%", "formula": "(Income - Expenses) / Income × 100", "excellent": (30.0, None), "healthy": (20.0, 30.0), "attention": (10.0, 20.0), "critical": (None, 10.0)},
    "liquid_asset_ratio": {"name": "Liquid Asset Ratio", "unit": "%", "formula": "Liquid Assets / Total Assets × 100", "excellent": (25.0, None), "healthy": (15.0, 25.0), "attention": (10.0, 15.0), "critical": (None, 10.0)},
    "debt_to_income_ratio": {"name": "Debt-to-Income Ratio", "unit": "%", "formula": "Monthly Debt Payments / Gross Monthly Income × 100", "excellent": (None, 20.0), "healthy": (20.0, 30.0), "attention": (30.0, 40.0), "critical": (40.0, None)},
    "leverage_ratio": {"name": "Leverage Ratio", "unit": "%", "formula": "Total Liabilities / Total Assets × 100", "excellent": (None, 20.0), "healthy": (20.0, 30.0), "attention": (30.0, 50.0), "critical": (50.0, None)},
    "financial_asset_ratio": {"name": "Financial Asset Ratio", "unit": "%", "formula": "Financial Assets / Total Assets × 100", "excellent": (70.0, None), "healthy": (50.0, 70.0), "attention": (30.0, 50.0), "critical": (None, 30.0)},
    "insurance_coverage_ratio": {"name": "Insurance Coverage Ratio", "unit": "%", "formula": "Existing Sum Assured / Required Insurance Cover × 100", "excellent": (80.0, None), "healthy": (60.0, 80.0), "attention": (40.0, 60.0), "critical": (None, 40.0)},
    "goal_funding_ratio": {"name": "Goal Funding Ratio", "unit": "%", "formula": "Current Goal Funding / Goal Target Amount × 100", "excellent": (100.0, None), "healthy": (80.0, 100.0), "attention": (50.0, 80.0), "critical": (None, 50.0)},
    "future_funding_ratio": {"name": "Future Funding Ratio", "unit": "%", "formula": "Projected Goal Funding / Future Goal Target × 100", "excellent": (100.0, None), "healthy": (80.0, 100.0), "attention": (50.0, 80.0), "critical": (None, 50.0)},
    "required_rate_of_return": {"name": "Required Rate of Return", "unit": "%", "formula": "(Future Goal Target / Current Goal Funding)^(1 / Goal Duration Years) - 1 × 100", "excellent": (None, 8.0), "healthy": (8.0, 12.0), "attention": (12.0, 15.0), "critical": (15.0, None)},
}

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


def classify(key: str, value: float) -> Status:
    rule = RULES[key]
    for status in ("excellent", "healthy", "attention", "critical"):
        lower, upper = rule[status]
        if lower is not None and value < lower:
            continue
        if upper is not None and value >= upper:
            continue
        return status
    raise ValueError(f"Unable to classify Moneywheel ratio: {key}={value}")
