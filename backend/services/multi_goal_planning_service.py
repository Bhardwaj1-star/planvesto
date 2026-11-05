from __future__ import annotations

from typing import Any
from fastapi import HTTPException

from data.goal_repository import GoalRepository
from engines.constraints.aggregator import ConstraintAggregator
from engines.orchestration.engine import MultiGoalOrchestrator
from engines.orchestration.models import GoalEvaluationInput, MultiGoalPlanResult
from services.financial_state_service import FinancialStateService


class MultiGoalPlanningService:
    """Coordinates competing goals using Goal Planner outputs only."""

    def __init__(
        self,
        goal_repo: GoalRepository | None = None,
        orchestrator: MultiGoalOrchestrator | None = None,
        financial_state_service: FinancialStateService | None = None,
    ):
        self.goal_repo = goal_repo or GoalRepository()
        self.orchestrator = orchestrator or MultiGoalOrchestrator()
        self.constraint_aggregator = ConstraintAggregator()
        self.financial_state_service = financial_state_service or FinancialStateService()

    def build_multi_goal_plan(
        self,
        planning_unit_id: str,
        priorities: dict[str, Any] | None = None,
        rule_overrides: dict[str, dict[str, Any]] | None = None,
        priority_ranks: dict[str, int] | None = None,
        goal_order: list[str] | None = None,
    ) -> MultiGoalPlanResult:
        goals = self.goal_repo.list_goals(planning_unit_id)
        if not goals:
            raise HTTPException(status_code=404, detail="No goals found for this planning unit")

        inputs: list[GoalEvaluationInput] = []
        for idx, goal_row in enumerate(goals):
            goal_id = goal_row["goal_id"]
            defined_goal = self.goal_repo.get_latest_defined_goal(planning_unit_id, goal_id)
            if defined_goal is None:
                raise HTTPException(
                    status_code=409,
                    detail=f"Goal '{goal_id}' has no current DefinedGoal snapshot from Chapter 10.",
                )
            if goal_order and goal_id in goal_order:
                rank = goal_order.index(goal_id) + 1
            elif priority_ranks and goal_id in priority_ranks:
                rank = int(priority_ranks[goal_id])
            elif goal_row.get("priority_rank"):
                rank = int(goal_row["priority_rank"])
            else:
                rank = idx + 1

            target_date = f"{defined_goal.target_year}-{defined_goal.target_month:02d}"
            inputs.append(GoalEvaluationInput(
                goal_id=goal_id,
                goal_name=defined_goal.goal_name,
                goal_type=defined_goal.goal_type,
                priority_rank=rank,
                client_priority=defined_goal.priority,
                target_date=target_date,
                target_year=defined_goal.target_year,
                target_month=defined_goal.target_month,
                today_cost=defined_goal.today_cost,
                future_target=defined_goal.future_target,
                funding_gap=defined_goal.funding_gap,
                required_monthly_contribution=defined_goal.required_monthly_contribution,
                flexibility=defined_goal.flexibility,
                defined_goal=defined_goal,
                metadata={
                    "defined_goal_id": defined_goal.defined_goal_id,
                    "defined_goal_version": defined_goal.version,
                    "funding_options": defined_goal.funding_options,
                    "projected_mapped_asset_value": defined_goal.projected_mapped_asset_value,
                    "funding_return_assumption": defined_goal.funding_return_assumption,
                    "available_monthly_surplus": defined_goal.available_monthly_surplus,
                    "feasibility_status": {"feasible": "pass", "constrained": "conditional", "infeasible": "infeasible", "unknown": "conditional"}.get(defined_goal.feasibility_status, "conditional"),
                    "notes": [defined_goal.feasibility_reason] if defined_goal.feasibility_reason else [],
                },
            ))

        state = self.financial_state_service.current(planning_unit_id, "family")
        if hasattr(state, "model_dump"):
            state = state.model_dump(mode="json")
        financial_context = dict(state) if isinstance(state, dict) else {}
        financial_context["planning_unit_id"] = planning_unit_id

        def metric_value(key: str):
            value = financial_context.get(key)
            return value.get("value") if isinstance(value, dict) else getattr(value, "value", value)

        financial_context.update({
            "annual_income": metric_value("income_annual"),
            "income": metric_value("income_annual"),
            "annual_expenses": metric_value("expenses_annual"),
            "expenses": metric_value("expenses_annual"),
            "monthly_surplus": metric_value("investable_surplus_monthly"),
            "surplus": metric_value("investable_surplus_monthly"),
            "assets": metric_value("total_assets"),
            "liabilities": metric_value("total_liabilities"),
            "total_liabilities": metric_value("total_liabilities"),
            "net_worth": metric_value("net_worth"),
            "financial_assets": metric_value("financial_assets"),
            "liquid_assets": metric_value("liquid_assets"),
            "essential_monthly_expenses": metric_value("essential_monthly_expenses"),
            "monthly_debt_payments": metric_value("emi_burden_monthly"),
            "emi_burden_monthly": metric_value("emi_burden_monthly"),
        })

        canonical_constraint_set = self.constraint_aggregator.aggregate(
            goals=inputs,
            financial_context=financial_context,
            planning_unit_id=planning_unit_id,
        )
        effective_overrides = canonical_constraint_set.suggested_overrides()
        if rule_overrides:
            effective_overrides.update(rule_overrides)

        plan = self.orchestrator.orchestrate(
            goals=inputs,
            financial_context=financial_context,
            rule_overrides=effective_overrides,
        )
        for warning in canonical_constraint_set.warnings:
            plan.planning_notes.append(f"Constraint Warning: {warning.message}")
        for hard in canonical_constraint_set.hard_constraints:
            plan.trade_offs.append(f"Constraint: {hard.message}")
        plan.audit_trail.append({
            "source": "ConstraintAggregator",
            "canonical_constraint_set": canonical_constraint_set.model_dump(),
            "constraint_count": len(canonical_constraint_set.constraints),
            "conflict_count": len(canonical_constraint_set.conflicts),
            "hard_failure_count": len(canonical_constraint_set.hard_constraints),
        })
        return plan
