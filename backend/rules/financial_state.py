MISSING_INPUT = "MISSING INPUT — requires a business rule or database field."


def cash_flow_ratio(expenses: float, income: float) -> float | None:
    """Compatibility wrapper around the canonical cash-flow calculation."""
    from engines.calculation.canonical import calculate_cash_flow_ratio
    return calculate_cash_flow_ratio(expenses, income)


def savings_investment_rate(investable_surplus: float, income: float) -> float | None:
    from engines.calculation.canonical import calculate_savings_rate
    return calculate_savings_rate(investable_surplus, income)


def required_safety_reserve_months(cash_flow_ratio_value: float) -> int:
    if cash_flow_ratio_value <= 50:
        return 3
    if cash_flow_ratio_value <= 70:
        return 6
    if cash_flow_ratio_value <= 85:
        return 9
    return 12
