"""
domain/features/reports/report_scope.py
Chapter 14 — Reports Domain Scope & Content Assembly.

Defines scope and approved payload structure for:
1. Individual Goal Report: derived from Goal Planner & Strategy Builder outputs
2. Goal Basket Report: derived from Multi-Goal consolidated outputs

Non-negotiable invariants:
- Does not calculate or recalculate numbers.
- Does not change investor decisions or adopt plans.
- Rendering (PDF / HTML) belongs exclusively to infrastructure/reporting.
"""

from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import List, Optional
from app.domain.shared.value_objects import Money
from app.domain.features.goal_planner.requirement import GoalRequirement
from app.domain.features.goal_planner.feasibility import GoalFeasibilityResult
from app.domain.features.strategy_builder.funding_paths import (
    SelfMoneyPathResult,
    FinancingPathResult,
)
from app.domain.features.strategy_builder.comparison import StrategyComparisonMatrix


class ReportType(str, Enum):
    INDIVIDUAL_GOAL_REPORT = "individual_goal_report"
    GOAL_BASKET_REPORT = "goal_basket_report"


@dataclass(frozen=True)
class IndividualGoalReportScope:
    """Approved content scope for an Individual Goal Report."""
    report_id: str
    investor_id: str
    generated_at: date
    goal_requirement: GoalRequirement
    feasibility_result: GoalFeasibilityResult
    self_money_path: Optional[SelfMoneyPathResult]
    financing_path: Optional[FinancingPathResult]
    comparison_matrix: Optional[StrategyComparisonMatrix]
    disclaimer: str = (
        "This report reflects evaluated projections and trade-offs based on investor inputs "
        "and is provided solely for financial planning purposes."
    )
