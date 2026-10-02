from models.defined_goal import DefinedGoal
from services.goal_service import GoalService


def _defined_goal() -> DefinedGoal:
    return DefinedGoal(
        goal_id="goal-1",
        planning_unit_id="planning-unit-1",
        goal_type="Education",
        goal_name="Education",
        today_cost=100000,
        inflation_rate=0.06,
        target_month=12,
        target_year=2030,
        duration_years=4,
        future_target=120000,
        priority="Important",
        flexibility="Flexible",
        funding_gap=50000,
        funding_status="Shortfall",
        required_monthly_contribution=500,
    )


class _SnapshotRepository:
    def __init__(self, row):
        self.row = row

    def get_latest(self, planning_unit_id, scope):
        return self.row


class _FinancialStateService:
    def __init__(self, state=None):
        self.state = state
        self.calls = []

    def build(self, planning_unit_id, scope):
        self.calls.append((planning_unit_id, scope))
        if self.state is None:
            raise RuntimeError("Financial inputs are unavailable")
        return self.state


def _service(snapshot, financial_state=None):
    service = GoalService.__new__(GoalService)
    service.financial_state_repository = _SnapshotRepository(snapshot)
    service.financial_state_service = _FinancialStateService(financial_state)
    return service


def test_missing_financial_state_keeps_feasibility_unknown_and_exposes_action():
    goal = _service(None)._apply_feasibility(_defined_goal())

    assert goal.feasibility_status == "unknown"
    assert goal.feasibility_reason == "Current financial surplus is unavailable."
    assert goal.workflow_readiness.status == "blocked"
    assert goal.workflow_readiness.blockers[0].reason == goal.feasibility_reason
    assert goal.workflow_readiness.blockers[0].missing_data[0].label == "Latest Financial State snapshot"
    assert goal.workflow_readiness.blockers[0].missing_data[0].route is None
    assert goal.workflow_readiness.next_action.label == "Complete Financial State"
    assert goal.workflow_readiness.next_action.route == "/investor/financial-state"
    assert goal.version_metadata["goal_feasibility"]["missing_prerequisite"]["key"] == "financial_state"
    assert goal.version_metadata["goal_feasibility"]["next_action"]["route"] == "/investor/financial-state"
    assert goal.workflow_readiness.return_to == "/investor/goal-planner"
    assert goal.funding_status == "Shortfall"
    assert goal.funding_gap == 50000


def test_unavailable_surplus_metric_remains_unknown_even_if_value_is_zero():
    goal = _service({
        "financial_state": {
            "income_monthly": {"value": None, "available": False},
            "expenses_monthly": {"value": 20000, "available": True},
            "investable_surplus_monthly": {"value": 0, "available": False},
        }
    })._apply_feasibility(_defined_goal())

    assert goal.feasibility_status == "unknown"
    assert goal.workflow_readiness.status == "blocked"
    missing = goal.workflow_readiness.blockers[0].missing_data
    assert [item.label for item in missing] == ["Income frequency"]
    assert missing[0].route == "/investor/onboarding/income"


def test_unavailable_income_and_expenses_are_both_reported():
    goal = _service({
        "financial_state": {
            "income_monthly": {"value": None, "available": False},
            "expenses_monthly": {"value": None, "available": False},
            "investable_surplus_monthly": {"value": None, "available": False},
        }
    })._apply_feasibility(_defined_goal())

    assert goal.feasibility_status == "unknown"
    missing = goal.workflow_readiness.blockers[0].missing_data
    assert [item.label for item in missing] == ["Income frequency", "Expense frequency"]
    assert [item.route for item in missing] == [
        "/investor/onboarding/income",
        "/investor/onboarding/expenses",
    ]


def test_available_surplus_keeps_existing_feasibility_calculation():
    goal = _service({
        "financial_state": {
            "investable_surplus_monthly": {"value": 1000, "available": True},
        }
    })._apply_feasibility(_defined_goal())

    assert goal.feasibility_status == "feasible"
    assert goal.workflow_readiness.status == "ready"
    assert goal.workflow_readiness.next_action is None
    assert goal.funding_status == "Shortfall"
    assert goal.funding_gap == 50000


def test_missing_snapshot_builds_canonical_financial_state_before_assessing_goal():
    service = _service(None, {
        "scope": "family",
        "planning_unit_id": "planning-unit-1",
        "investable_surplus_monthly": {"value": 1000, "available": True},
    })

    goal = service._apply_feasibility(_defined_goal())

    assert service.financial_state_service.calls == [("planning-unit-1", "family")]
    assert goal.feasibility_status == "feasible"
    assert goal.available_monthly_surplus == 1000


def test_insufficient_positive_surplus_is_constrained():
    goal = _service({
        "financial_state": {
            "investable_surplus_monthly": {"value": 100, "available": True},
        }
    })._apply_feasibility(_defined_goal())

    assert goal.feasibility_status == "constrained"


def test_zero_surplus_is_infeasible_when_goal_has_a_funding_gap():
    goal = _service({
        "financial_state": {
            "investable_surplus_monthly": {"value": 0, "available": True},
        }
    })._apply_feasibility(_defined_goal())

    assert goal.feasibility_status == "infeasible"


def test_workflow_readiness_hydrates_from_existing_goal_metadata():
    goal = _defined_goal()
    goal.version_metadata["workflow_readiness"] = {
        "status": "blocked",
        "process_route": "/investor/goal-planner",
        "blockers": [],
        "next_action": {
            "label": "Complete Financial State",
            "route": "/investor/financial-state",
        },
        "return_to": "/investor/goal-planner",
    }

    restored = DefinedGoal.model_validate(goal.model_dump(exclude={"workflow_readiness"}))

    assert restored.workflow_readiness.next_action.route == "/investor/financial-state"


def test_latest_goal_rechecks_feasibility_against_latest_financial_state():
    goal = _defined_goal()
    goal.feasibility_status = "unknown"
    service = _service({
        "financial_state": {
            "investable_surplus_monthly": {"value": 1000, "available": True},
        }
    })
    service.repository = type("GoalRepositoryStub", (), {
        "get_latest_defined_goal": lambda self, planning_unit_id, goal_id: goal,
    })()

    latest = service.get_latest_defined_goal("planning-unit-1", "goal-1")

    assert latest.feasibility_status == "feasible"
    assert latest.workflow_readiness.status == "ready"