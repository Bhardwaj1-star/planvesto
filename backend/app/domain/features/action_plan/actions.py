"""
domain/features/action_plan/actions.py
Chapter 13 — Action Plan: Action Item Contracts (§13.2).

Action items derived strictly from an explicitly Accepted Plan.
Non-negotiable invariants:
- An action list is NOT plan acceptance or transaction authorization.
- Actions cannot be created without an explicit investor-approved plan.
- Does not invent speculative execution dates or mandatory third-party accounts.
"""

from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Optional
from app.domain.shared.value_objects import Money


class ActionType(str, Enum):
    START_SIP = "start_sip"
    LUMP_SUM_INVESTMENT = "lump_sum_investment"
    DEBT_PREPAYMENT = "debt_prepayment"
    INSURANCE_COVERAGE_SETUP = "insurance_coverage_setup"
    EMERGENCY_RESERVE_DEPOSIT = "emergency_reserve_deposit"
    ACCOUNT_SEGREGATION = "account_segregation"


class ActionStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    DEFERRED = "deferred"
    CANCELLED = "cancelled"


@dataclass(frozen=True)
class ActionItem:
    """A concrete, tangible step the investor has approved to execute."""
    action_id: str
    investor_id: str
    plan_id: str  # References explicitly Accepted Plan
    action_type: ActionType
    title: str
    description: str
    target_amount: Optional[Money]
    target_date: Optional[date]
    status: ActionStatus = ActionStatus.PENDING
    status_updated_at: Optional[date] = None
    completion_notes: Optional[str] = None
