"""
application/workflows/plan_acceptance.py
Chapter 13 — Explicit Investor Plan Acceptance Workflow (§13.1, §13.2).

Non-negotiable invariants:
1. A proposed strategy or recommendation is NOT acceptance.
2. Acceptance requires an explicit, dated decision by the authenticated investor.
3. Once accepted, creates the Accepted Plan record and derives initial Action Items.
"""

from dataclasses import dataclass
from datetime import date
from typing import List, Optional
import uuid

from app.domain.shared.value_objects import Money
from app.domain.features.strategy_builder.funding_paths import (
    FundingPathType,
    SelfMoneyPathResult,
    FinancingPathResult,
)
from app.domain.features.action_plan.actions import (
    ActionItem,
    ActionType,
    ActionStatus,
)


@dataclass(frozen=True)
class AcceptedPlanRecord:
    """Explicitly accepted financial plan record."""
    plan_id: str
    investor_id: str
    goal_id: str
    accepted_funding_path: FundingPathType
    accepted_at: date
    target_amount: Money
    horizon_years: int
    derived_action_ids: List[str]
    notes: Optional[str] = None


@dataclass(frozen=True)
class PlanAcceptanceResult:
    """Outcome of the explicit acceptance workflow."""
    accepted_plan: AcceptedPlanRecord
    initial_actions: List[ActionItem]
    confirmation_message: str


def execute_plan_acceptance(
    investor_id: str,
    goal_id: str,
    target_amount: Money,
    horizon_years: int,
    selected_path_type: FundingPathType,
    self_money_path: Optional[SelfMoneyPathResult] = None,
    financing_path: Optional[FinancingPathResult] = None,
    acceptance_date: Optional[date] = None,
    investor_notes: Optional[str] = None,
) -> PlanAcceptanceResult:
    """
    Coordinates the explicit acceptance gate.
    Creates an immutable AcceptedPlanRecord and derives approved ActionItems.
    """
    plan_id = f"plan_{uuid.uuid4().hex[:12]}"
    as_of = acceptance_date or date.today()
    action_items: List[ActionItem] = []

    if selected_path_type == FundingPathType.SELF_MONEY:
        if self_money_path is None:
            raise ValueError("SelfMoneyPathResult is required when selecting SELF_MONEY path.")

        # Action: Set up SIP mandate
        action_items.append(
            ActionItem(
                action_id=f"act_{uuid.uuid4().hex[:8]}",
                investor_id=investor_id,
                plan_id=plan_id,
                action_type=ActionType.START_SIP,
                title=f"Set up Goal SIP Mandate",
                description=f"Automate monthly contributions towards goal {goal_id}.",
                target_amount=self_money_path.total_own_money_contributed,
                target_date=as_of,
                status=ActionStatus.PENDING,
            )
        )
    elif selected_path_type == FundingPathType.SELF_MONEY_PLUS_FINANCING:
        if financing_path is None:
            raise ValueError("FinancingPathResult is required when selecting SELF_MONEY_PLUS_FINANCING path.")

        # Action 1: Down payment arrangement
        action_items.append(
            ActionItem(
                action_id=f"act_{uuid.uuid4().hex[:8]}",
                investor_id=investor_id,
                plan_id=plan_id,
                action_type=ActionType.LUMP_SUM_INVESTMENT,
                title=f"Earmark Own Down Payment",
                description=f"Arrange down payment of {financing_path.own_down_payment.amount}.",
                target_amount=financing_path.own_down_payment,
                target_date=as_of,
                status=ActionStatus.PENDING,
            )
        )
        # Action 2: Financing application setup
        action_items.append(
            ActionItem(
                action_id=f"act_{uuid.uuid4().hex[:8]}",
                investor_id=investor_id,
                plan_id=plan_id,
                action_type=ActionType.ACCOUNT_SEGREGATION,
                title=f"Loan EMI Cash-flow Segregation",
                description=f"Ensure surplus covers monthly EMI of {financing_path.monthly_emi.amount}.",
                target_amount=financing_path.monthly_emi,
                target_date=as_of,
                status=ActionStatus.PENDING,
            )
        )

    accepted_plan = AcceptedPlanRecord(
        plan_id=plan_id,
        investor_id=investor_id,
        goal_id=goal_id,
        accepted_funding_path=selected_path_type,
        accepted_at=as_of,
        target_amount=target_amount,
        horizon_years=horizon_years,
        derived_action_ids=[a.action_id for a in action_items],
        notes=investor_notes,
    )

    confirmation = (
        f"Plan {plan_id} successfully accepted for goal {goal_id} under {selected_path_type.value}. "
        f"Generated {len(action_items)} approved action items."
    )

    return PlanAcceptanceResult(
        accepted_plan=accepted_plan,
        initial_actions=action_items,
        confirmation_message=confirmation,
    )
