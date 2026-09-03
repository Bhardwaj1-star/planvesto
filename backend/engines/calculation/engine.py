def calculate_future_value(
    current_corpus: float,
    monthly_investment: float,
    annual_return: float,
    years: int,
) -> float:
    months = years * 12
    monthly_rate = annual_return / 100 / 12

    if monthly_rate == 0:
        return current_corpus + (monthly_investment * months)

    future_corpus = (
        current_corpus * ((1 + monthly_rate) ** months)
        + monthly_investment
        * (((1 + monthly_rate) ** months - 1) / monthly_rate)
    )

    return round(future_corpus, 2)


def calculate_required_monthly_investment(
    target_amount: float,
    current_corpus: float,
    annual_return: float,
    years: int,
) -> float:
    months = years * 12
    monthly_rate = annual_return / 100 / 12

    future_current_corpus = (
        current_corpus * ((1 + monthly_rate) ** months)
        if monthly_rate != 0
        else current_corpus
    )

    remaining_target = max(target_amount - future_current_corpus, 0)

    if remaining_target == 0:
        return 0.0

    if monthly_rate == 0:
        return round(remaining_target / months, 2)

    required = remaining_target * monthly_rate / (
        (1 + monthly_rate) ** months - 1
    )

    return round(required, 2)