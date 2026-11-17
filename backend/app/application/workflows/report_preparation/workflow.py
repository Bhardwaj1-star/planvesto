"""
application/workflows/report_preparation/workflow.py
Report Preparation Workflow.

Coordinates report preparation by assembling authoritative outputs from owning features
into the approved report view contracts (Chapter 14).
Non-negotiable invariants:
- Does not recalculate, alter, or optimize financial or strategy decisions.
- Rendering (PDF / HTML) implementation belongs exclusively in infrastructure/reporting.
"""

from datetime import date
import uuid

from app.domain.features.reports.report_scope import (
    ReportType,
    IndividualGoalReportScope,
)
from app.application.workflows.planning_lifecycle import PlanningLifecycleResult


def prepare_individual_goal_report(
    investor_id: str,
    planning_result: PlanningLifecycleResult,
    as_of_date: date = None,
) -> IndividualGoalReportScope:
    """
    Assembles authoritative Goal Planner and Strategy Builder outputs into IndividualGoalReportScope.
    """
    report_id = f"rpt_{uuid.uuid4().hex[:12]}"
    gen_date = as_of_date or date.today()

    return IndividualGoalReportScope(
        report_id=report_id,
        investor_id=investor_id,
        generated_at=gen_date,
        goal_requirement=planning_result.goal_requirement,
        feasibility_result=planning_result.feasibility,
        self_money_path=planning_result.self_money_path,
        financing_path=planning_result.financing_path,
        comparison_matrix=planning_result.comparison_matrix,
    )
