"""
application/workflows/__init__.py
Application workflows exports across all chapters.
"""

from app.application.workflows.investor_situation_assessment import (
    InvestorSituationAssessmentResult,
    execute_investor_situation_assessment,
)
from app.application.workflows.budgeting_cash_flow_affordability import (
    CashFlowAffordabilityBundle,
    execute_budgeting_cash_flow_affordability,
)
from app.application.workflows.planning_lifecycle import (
    FinancingOptionsInput,
    PlanningLifecycleResult,
    execute_planning_lifecycle,
)
from app.application.workflows.plan_acceptance import (
    AcceptedPlanRecord,
    PlanAcceptanceResult,
    execute_plan_acceptance,
)
from app.application.workflows.report_preparation import (
    prepare_individual_goal_report,
)

__all__ = [
    "InvestorSituationAssessmentResult",
    "execute_investor_situation_assessment",
    "CashFlowAffordabilityBundle",
    "execute_budgeting_cash_flow_affordability",
    "FinancingOptionsInput",
    "PlanningLifecycleResult",
    "execute_planning_lifecycle",
    "AcceptedPlanRecord",
    "PlanAcceptanceResult",
    "execute_plan_acceptance",
    "prepare_individual_goal_report",
]
