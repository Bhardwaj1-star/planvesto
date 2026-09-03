from supabase import create_client

from config.settings import (
    SUPABASE_URL,
    SUPABASE_SERVICE_ROLE_KEY,
)


supabase = create_client(
    SUPABASE_URL,
    SUPABASE_SERVICE_ROLE_KEY,
)


def get_dashboard(access_token: str):
    # ---------------------------------------------------------
    # 1. Verify the authenticated Supabase user
    # ---------------------------------------------------------

    user_response = supabase.auth.get_user(access_token)

    if not user_response or not user_response.user:
        raise ValueError("Invalid or expired authentication token.")

    user = user_response.user

    # ---------------------------------------------------------
    # 2. Find the Planvesto investor linked to this user
    # ---------------------------------------------------------

    investor_response = (
        supabase
        .table("investors")
        .select("*")
        .eq("user_id", user.id)
        .single()
        .execute()
    )

    investor = investor_response.data

    if not investor:
        raise ValueError("Investor profile not found.")

    investor_id = investor["id"]

    # ---------------------------------------------------------
    # 3. Fetch existing financial data
    # ---------------------------------------------------------

    financial_state = (
        supabase
        .table("financial_state")
        .select("*")
        .eq("investor_id", investor_id)
        .execute()
    )

    goals = (
        supabase
        .table("goals")
        .select("*")
        .eq("investor_id", investor_id)
        .execute()
    )

    assets = (
        supabase
        .table("assets")
        .select("*")
        .eq("investor_id", investor_id)
        .execute()
    )

    liabilities = (
        supabase
        .table("liabilities")
        .select("*")
        .eq("investor_id", investor_id)
        .execute()
    )

    income = (
        supabase
        .table("income")
        .select("*")
        .eq("investor_id", investor_id)
        .execute()
    )

    expenses = (
        supabase
        .table("expense")
        .select("*")
        .eq("investor_id", investor_id)
        .execute()
    )

    # ---------------------------------------------------------
    # 4. Return the source data
    #
    # Calculations will be added after we verify the exact
    # database columns during localhost testing.
    # ---------------------------------------------------------

    return {
        "success": True,
        "data": {
            "investor": investor,
            "financial_state": financial_state.data or [],
            "goals": goals.data or [],
            "assets": assets.data or [],
            "liabilities": liabilities.data or [],
            "income": income.data or [],
            "expenses": expenses.data or [],
        },
    }