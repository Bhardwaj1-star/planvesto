from engines.calculation.engine import (
    calculate_future_value,
    calculate_required_monthly_investment,
)


def build_strategies(
    goal_amount: float,
    time_horizon_years: int,
    current_corpus: float,
    monthly_investment: float,
    expected_annual_return: float,
):
    scenarios = [
        {
            "strategy_id": "conservative",
            "strategy_name": "Conservative Strategy",
            "annual_return": max(expected_annual_return - 3, 0),
        },
        {
            "strategy_id": "balanced",
            "strategy_name": "Balanced Strategy",
            "annual_return": expected_annual_return,
        },
        {
            "strategy_id": "growth",
            "strategy_name": "Growth Strategy",
            "annual_return": expected_annual_return + 3,
        },
    ]

    results = []

    for scenario in scenarios:
        annual_return = scenario["annual_return"]

        projected_corpus = calculate_future_value(
            current_corpus=current_corpus,
            monthly_investment=monthly_investment,
            annual_return=annual_return,
            years=time_horizon_years,
        )

        required_monthly = calculate_required_monthly_investment(
            target_amount=goal_amount,
            current_corpus=current_corpus,
            annual_return=annual_return,
            years=time_horizon_years,
        )

        total_contribution = (
            current_corpus
            + monthly_investment * time_horizon_years * 12
        )

        results.append(
            {
                "strategy_id": scenario["strategy_id"],
                "strategy_name": scenario["strategy_name"],
                "annual_return": annual_return,
                "monthly_investment": monthly_investment,
                "required_monthly_investment": required_monthly,
                "time_horizon_years": time_horizon_years,
                "initial_capital": current_corpus,
                "projected_corpus": projected_corpus,
                "funding_gap": round(
                    max(goal_amount - projected_corpus, 0), 2
                ),
                "total_contribution": round(total_contribution, 2),
            }
        )

    return results