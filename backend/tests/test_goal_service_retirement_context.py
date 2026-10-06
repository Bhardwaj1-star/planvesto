from unittest.mock import MagicMock, patch

from schemas.goals import GoalInput
from services.goal_service import GoalService


def _request(goal_type="retirement", dynamic_details=None):
    return GoalInput(
        planning_unit_id="pu-1",
        goal_name="Retirement",
        goal_type=goal_type,
        today_cost=1200000,
        target_month=12,
        target_year=2045,
        inflation_rate=0.06,
        priority="Important",
        flexibility="Flexible",
        status="Active",
        dynamic_details=dynamic_details or {},
    )


def test_retirement_context_derives_current_age_and_default_life_expectancy():
    query = MagicMock()
    query.eq.return_value = query
    query.order.return_value = query
    query.limit.return_value = query
    query.maybe_single.return_value = query
    query.execute.return_value = MagicMock(data={"date_of_birth": "1990-10-07"})

    supabase = MagicMock()
    supabase.table.return_value.select.return_value = query

    service = GoalService.__new__(GoalService)
    request = _request()

    with patch("services.goal_service.get_supabase", return_value=supabase), patch(
        "services.goal_service.date",
    ) as mocked_date:
        mocked_date.today.return_value = __import__("datetime").date(2026, 10, 6)
        service._enrich_retirement_context(request)

    assert request.dynamic_details["currentAge"] == 35
    assert request.dynamic_details["lifeExpectancy"] == 85


def test_retirement_context_preserves_explicit_values():
    service = GoalService.__new__(GoalService)
    request = _request(dynamic_details={"currentAge": 42, "lifeExpectancy": 90})

    with patch("services.goal_service.get_supabase") as get_supabase:
        service._enrich_retirement_context(request)

    get_supabase.assert_not_called()
    assert request.dynamic_details == {"currentAge": 42, "lifeExpectancy": 90}


def test_non_retirement_goal_does_not_query_investor_context():
    service = GoalService.__new__(GoalService)
    request = _request(goal_type="vacation")

    with patch("services.goal_service.get_supabase") as get_supabase:
        service._enrich_retirement_context(request)

    get_supabase.assert_not_called()
    assert request.dynamic_details == {}
