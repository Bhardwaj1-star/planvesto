import pytest
from engines.allocation.engine import ResourceAllocationEngine


@pytest.fixture
def allocation_engine():
    return ResourceAllocationEngine()


def test_sufficient_resources_all_goals_funded(allocation_engine):
    goals = [
        {
            "goal_id": "g1",
            "goal_name": "Emergency Fund",
            "client_priority": "critical",
            "resolved_priority": "critical",
            "required_monthly_contribution": 10000.0,
            "target_date": "2027-01",
        },
        {
            "goal_id": "g2",
            "goal_name": "Retirement",
            "client_priority": "high",
            "resolved_priority": "high",
            "required_monthly_contribution": 20000.0,
            "target_date": "2045-12",
        },
    ]
    surplus = 40000.0

    result = allocation_engine.allocate(goals, surplus)

    assert result.competition_detected is False
    assert result.overall_funding_status == "within_surplus"
    assert result.total_required_monthly_contribution == 30000.0
    assert result.total_allocated_monthly_contribution == 30000.0
    assert result.net_monthly_gap == -10000.0
    assert len(result.trade_offs) == 0

    assert all(a.funding_status == "fully_funded" for a in result.allocations)
    assert all(a.funding_percentage == 100.0 for a in result.allocations)


def test_competing_goals_with_partial_funding(allocation_engine):
    goals = [
        {
            "goal_id": "g1",
            "goal_name": "Child Education",
            "client_priority": "high",
            "resolved_priority": "high",
            "required_monthly_contribution": 25000.0,
            "target_date": "2035-06",
        },
        {
            "goal_id": "g2",
            "goal_name": "Home Downpayment",
            "client_priority": "medium",
            "resolved_priority": "medium",
            "required_monthly_contribution": 20000.0,
            "target_date": "2032-12",
        },
    ]
    surplus = 35000.0  # Total required is 45000. Shortfall of 10000.

    result = allocation_engine.allocate(goals, surplus)

    assert result.competition_detected is True
    assert result.overall_funding_status == "surplus_shortfall"
    assert result.total_required_monthly_contribution == 45000.0
    assert result.total_allocated_monthly_contribution == 35000.0
    assert result.net_monthly_gap == 10000.0

    # g1 is fully funded (25000)
    assert result.allocations[0].goal_id == "g1"
    assert result.allocations[0].allocated_monthly_contribution == 25000.0
    assert result.allocations[0].funding_status == "fully_funded"

    # g2 gets remainder (10000 of 20000) -> 50%
    assert result.allocations[1].goal_id == "g2"
    assert result.allocations[1].allocated_monthly_contribution == 10000.0
    assert result.allocations[1].monthly_shortfall == 10000.0
    assert result.allocations[1].funding_percentage == 50.0
    assert result.allocations[1].funding_status == "partially_funded"
    assert result.allocations[1].feasibility_status == "constrained"
    assert "receives 10000.00 of 20000.00/mo (50.0% funded)" in result.trade_offs[0]


def test_infeasible_goal_due_to_zero_remaining_surplus(allocation_engine):
    goals = [
        {
            "goal_id": "g1",
            "goal_name": "Priority Goal",
            "client_priority": "critical",
            "resolved_priority": "critical",
            "required_monthly_contribution": 30000.0,
        },
        {
            "goal_id": "g2",
            "goal_name": "Secondary Goal",
            "client_priority": "low",
            "resolved_priority": "low",
            "required_monthly_contribution": 15000.0,
        },
    ]
    surplus = 25000.0

    result = allocation_engine.allocate(goals, surplus)

    # g1 partially funded
    assert result.allocations[0].goal_id == "g1"
    assert result.allocations[0].allocated_monthly_contribution == 25000.0
    assert result.allocations[0].funding_status == "partially_funded"

    # g2 completely unfunded
    assert result.allocations[1].goal_id == "g2"
    assert result.allocations[1].allocated_monthly_contribution == 0.0
    assert result.allocations[1].monthly_shortfall == 15000.0
    assert result.allocations[1].funding_status == "unfunded"
    assert result.allocations[1].feasibility_status == "infeasible"
    assert "unfunded from current monthly surplus" in result.trade_offs[1]


def test_ratio_driven_allocation_override_preserved(allocation_engine):
    goals = [
        {
            "goal_id": "luxury",
            "goal_name": "Luxury Sports Car",
            "client_priority": "critical",
            "resolved_priority": "low",  # Override by ratio rule
            "override_applied": True,
            "override_reason": "Discretionary goal deprioritized due to high debt-to-income ratio (45%).",
            "required_monthly_contribution": 20000.0,
            "target_date": "2027-01",
        },
        {
            "goal_id": "retirement",
            "goal_name": "Retirement",
            "client_priority": "medium",
            "resolved_priority": "medium",
            "override_applied": False,
            "required_monthly_contribution": 20000.0,
            "target_date": "2045-01",
        },
    ]
    surplus = 25000.0

    result = allocation_engine.allocate(goals, surplus)

    # Retirement should be allocated first because its resolved priority (medium) is higher than luxury's (low)
    assert result.allocations[0].goal_id == "retirement"
    assert result.allocations[0].allocated_monthly_contribution == 20000.0
    assert result.allocations[0].funding_status == "fully_funded"

    # Luxury car gets remaining (5000)
    luxury_alloc = result.allocations[1]
    assert luxury_alloc.goal_id == "luxury"
    assert luxury_alloc.allocated_monthly_contribution == 5000.0
    assert luxury_alloc.funding_status == "partially_funded"
    assert luxury_alloc.client_priority == "critical"
    assert luxury_alloc.resolved_priority == "low"
    assert luxury_alloc.override_applied is True
    assert "System Override: Client selected 'critical', resolved to 'low'" in luxury_alloc.allocation_reasoning
    assert any("Override applied to 'Luxury Sports Car'" in log for log in result.decision_log)
