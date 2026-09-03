from supabase import create_client

from config.settings import (
    SUPABASE_URL,
    SUPABASE_SERVICE_ROLE_KEY,
)

from engines.strategy.engine import build_strategies


supabase = create_client(
    SUPABASE_URL,
    SUPABASE_SERVICE_ROLE_KEY,
)


def save_strategy(
    user_id: str,
    name: str,
    email: str,
    goal_amount: float,
    time_horizon_years: int,
    current_corpus: float,
    monthly_investment: float,
    existing_investments: float,
    expected_annual_return: float,
):
    investor_response = (
        supabase
        .table("investors")
        .upsert(
            {
                "user_id": user_id,
                "name": name,
                "email": email,
            },
            on_conflict="user_id",
        )
        .execute()
    )

    investor = investor_response.data[0]

    input_response = (
        supabase
        .table("strategy_inputs")
        .insert(
            {
                "investor_id": investor["id"],
                "goal_amount": goal_amount,
                "time_horizon_years": time_horizon_years,
                "current_corpus": current_corpus,
                "monthly_investment": monthly_investment,
                "existing_investments": existing_investments,
                "expected_annual_return": expected_annual_return,
            }
        )
        .execute()
    )

    strategy_input = input_response.data[0]

    results = build_strategies(
        goal_amount=goal_amount,
        time_horizon_years=time_horizon_years,
        current_corpus=current_corpus,
        monthly_investment=monthly_investment,
        expected_annual_return=expected_annual_return,
    )

    saved_results = []

    for result in results:
        response = (
            supabase
            .table("strategy_results")
            .insert(
                {
                    "investor_id": investor["id"],
                    "strategy_input_id": strategy_input["id"],
                    "strategy_id": result["strategy_id"],
                    "strategy_name": result["strategy_name"],
                    "annual_return": result["annual_return"],
                    "monthly_investment": result["monthly_investment"],
                    "time_horizon_years": result["time_horizon_years"],
                    "initial_capital": result["initial_capital"],
                    "projected_corpus": result["projected_corpus"],
                    "funding_gap": result["funding_gap"],
                    "total_contribution": result["total_contribution"],
                }
            )
            .execute()
        )

        saved_results.extend(response.data)

    return {
        "investor": investor,
        "strategy_input": strategy_input,
        "results": saved_results,
    }