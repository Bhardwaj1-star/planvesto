from typing import Literal


RULE_SET_VERSION = "1.2"

Status = Literal["excellent", "healthy", "attention", "critical"]


# Provisional planning baselines. These are intentionally versioned so they can
# be replaced by a later Planvesto rule set without changing historical data.
RULES = {
    "savings_ratio": {"name": "Savings Ratio", "unit": "%", "formula": "Savings / Gross Monthly Income × 100", "excellent": (30.0, None), "healthy": (20.0, 30.0), "attention": (10.0, 20.0), "critical": (None, 10.0)},
    "expense_ratio": {"name": "Expense Ratio", "unit": "%", "formula": "Essential Expenses / Gross Monthly Income × 100", "excellent": (None, 40.0), "healthy": (40.0, 50.0), "attention": (50.0, 60.0), "critical": (60.0, None)},
    "emergency_fund_coverage": {"name": "Emergency Fund Coverage", "unit": "months", "formula": "Liquid Assets / Monthly Expenses", "excellent": (9.0, None), "healthy": (6.0, 9.0), "attention": (3.0, 6.0), "critical": (None, 3.0)},
    "current_liquidity_ratio": {"name": "Current Liquidity Ratio", "unit": "x", "formula": "Liquid Assets / Short-Term Liabilities", "excellent": (1.5, None), "healthy": (1.0, 1.5), "attention": (0.75, 1.0), "critical": (None, 0.75)},
    "debt_to_income_ratio": {"name": "Debt-to-Income Ratio", "unit": "%", "formula": "Total Monthly Debt Payments / Gross Monthly Income × 100", "excellent": (None, 20.0), "healthy": (20.0, 30.0), "attention": (30.0, 40.0), "critical": (40.0, None)},
    "leverage_ratio": {"name": "Leverage Ratio", "unit": "%", "formula": "Total Liabilities / Total Assets × 100", "excellent": (None, 20.0), "healthy": (20.0, 30.0), "attention": (30.0, 50.0), "critical": (50.0, None)},
    "liquid_asset_to_total_asset": {"name": "Liquid Asset-to-Total Asset", "unit": "%", "formula": "Liquid Assets / Total Assets × 100", "excellent": (25.0, None), "healthy": (15.0, 25.0), "attention": (10.0, 15.0), "critical": (None, 10.0)},
    "solvency_ratio": {"name": "Solvency Ratio", "unit": "%", "formula": "(1 - Leverage Ratio) × 100", "excellent": (80.0, None), "healthy": (70.0, 80.0), "attention": (50.0, 70.0), "critical": (None, 50.0)},
    "financial_asset_ratio": {"name": "Financial Asset Ratio", "unit": "%", "formula": "Financial Assets / Total Assets × 100", "excellent": (70.0, None), "healthy": (50.0, 70.0), "attention": (30.0, 50.0), "critical": (None, 30.0)},
    "insurance_gap_ratio": {"name": "Insurance Coverage Ratio", "unit": "%", "formula": "Existing Sum Assured / Required Insurance Cover × 100", "excellent": (80.0, None), "healthy": (60.0, 80.0), "attention": (40.0, 60.0), "critical": (None, 40.0)},
    "goal_funding_ratio": {"name": "Goal Funding Ratio", "unit": "%", "formula": "Current Goal Funding / Goal Target Amount × 100", "excellent": (100.0, None), "healthy": (80.0, 100.0), "attention": (50.0, 80.0), "critical": (None, 50.0)},
    "future_funding_ratio": {"name": "Future Funding Ratio", "unit": "%", "formula": "Projected Goal Funding / Future Goal Target × 100", "excellent": (100.0, None), "healthy": (80.0, 100.0), "attention": (50.0, 80.0), "critical": (None, 50.0)},
}


def classify(key: str, value: float) -> Status:
    rule = RULES[key]
    for status in ("excellent", "healthy", "attention", "critical"):
        lower, upper = rule[status]
        if lower is not None and value < lower:
            continue
        if upper is not None and value >= upper:
            continue
        return status  # type: ignore[return-value]
    raise ValueError(f"Unable to classify Moneywheel ratio: {key}={value}")
