"""
tests/unit/test_persistence_mappers.py
Tests bi-directional mapping between database records and domain entities.
"""

from datetime import date
from decimal import Decimal
from app.domain.canonical.financial_categories import (
    CanonicalAssetCategoryId,
    CanonicalExpenseCategoryId,
    CanonicalIncomeCategoryId,
    CanonicalLiabilityCategoryId,
)
from app.domain.canonical.goal_taxonomy import CanonicalGoalId
from app.domain.features.goal_planner.requirement import (
    GoalInstance,
    plan_goal_requirement,
)
from app.domain.features.action_plan.actions import ActionItem, ActionStatus, ActionType
from app.domain.shared.value_objects import CalendarMonth, Money, Rate
from app.infrastructure.persistence.mappers import (
    map_action_item_to_dict,
    map_db_row_to_action_item,
    map_db_row_to_goal_instance,
    map_financial_facts_to_snapshot,
    map_goal_instance_to_persistence_dict,
    map_requirement_to_defined_goal_dict,
    map_row_to_asset_record,
    map_row_to_expense_record,
    map_row_to_income_record,
    map_row_to_liability_record,
    snapshot_to_persistence_dict,
)


def test_financial_state_mappers():
    period = CalendarMonth(2026, 11)
    
    # Income mapping
    income_row = {"income_id": "inc_1", "category": "salary", "amount": 150000, "is_net": True}
    inc_record = map_row_to_income_record(income_row, period)
    assert inc_record.category == CanonicalIncomeCategoryId.SALARY
    assert inc_record.amount.amount == Decimal("150000")

    # Expense mapping
    expense_row = {"expense_id": "exp_1", "category": "housing", "amount": 35000}
    exp_record = map_row_to_expense_record(expense_row, period)
    assert exp_record.category == CanonicalExpenseCategoryId.HOUSING
    assert exp_record.amount.amount == Decimal("35000")

    # Asset mapping
    asset_row = {"asset_id": "ast_1", "category": "mutual_funds", "current_value": 500000}
    ast_record = map_row_to_asset_record(asset_row)
    assert ast_record.category == CanonicalAssetCategoryId.MUTUAL_FUNDS
    assert ast_record.current_value.amount == Decimal("500000")

    # Liability mapping
    liab_row = {"liability_id": "lia_1", "category": "car_loan", "outstanding_balance": 400000, "annual_interest_rate": 8.5, "monthly_payment": 12000}
    lia_record = map_row_to_liability_record(liab_row)
    assert lia_record.category == CanonicalLiabilityCategoryId.CAR_LOAN
    assert lia_record.outstanding_balance.amount == Decimal("400000")

    # Financial facts to snapshot
    facts = {
        "income": [income_row],
        "expenses": [expense_row],
        "assets": [asset_row],
        "liabilities": [liab_row],
    }
    snapshot = map_financial_facts_to_snapshot("inv_1", date(2026, 11, 1), facts)
    assert snapshot.investor_id == "inv_1"
    assert snapshot.total_assets().amount == Decimal("500000")
    assert snapshot.total_liabilities().amount == Decimal("400000")
    assert snapshot.net_worth().amount == Decimal("100000")

    # Snapshot to dict
    serialized = snapshot_to_persistence_dict(snapshot)
    assert serialized["investor_id"] == "inv_1"
    assert serialized["total_assets"] == "500000.00"
    assert serialized["net_worth"] == "100000.00"


def test_goal_planner_mappers():
    goal_row = {
        "goal_id": "g_123",
        "planning_unit_id": "pu_1",
        "goal_name": "Dream Vacation to Europe",
        "target_amount": 500000.0,
        "target_date": "2028-11-01",
        "priority": "1",
    }
    goal_inst = map_db_row_to_goal_instance(goal_row)
    assert goal_inst.id == "g_123"
    assert goal_inst.canonical_id == CanonicalGoalId.VACATION
    assert goal_inst.current_cost.amount == Decimal("500000.0")

    persisted_dict = map_goal_instance_to_persistence_dict(goal_inst)
    assert persisted_dict["goal_name"] == "Dream Vacation to Europe"
    assert persisted_dict["target_amount"] == 500000.0

    req = plan_goal_requirement(goal_inst, evaluation_date=date(2026, 11, 1))
    defined_dict = map_requirement_to_defined_goal_dict(goal_inst, req, version=1)
    assert defined_dict["goal_id"] == "g_123"
    assert defined_dict["funding_status"] == "gap"
    assert defined_dict["future_target"] > 500000.0


def test_action_plan_mappers():
    row = {
        "action_id": "act_99",
        "planning_unit_id": "pu_1",
        "plan_id": "plan_1",
        "action_type": "start_sip",
        "title": "Start Index Fund SIP",
        "target_amount": 15000.0,
        "status": "pending",
    }
    item = map_db_row_to_action_item(row)
    assert item.action_id == "act_99"
    assert item.action_type == ActionType.START_SIP
    assert item.status == ActionStatus.PENDING
    assert item.target_amount.amount == Decimal("15000.0")

    out_dict = map_action_item_to_dict(item)
    assert out_dict["action_id"] == "act_99"
    assert out_dict["action_type"] == "start_sip"
    assert out_dict["status"] == "pending"
