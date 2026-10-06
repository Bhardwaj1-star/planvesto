from __future__ import annotations

from typing import Any
from fastapi import HTTPException

from data.goal_repository import GoalRepository
from data.strategy_repository import StrategyRepository
from engines.constraints.aggregator import ConstraintAggregator
from engines.constraints.models import ConstraintSet
from engines.orchestration.engine import MultiGoalOrchestrator
from engines.orchestration.models import GoalEvaluationInput, MultiGoalPlanResult
from models.strategy import InvestorPriorities
from services.goal_report_service import GoalReportService
from services.strategy_service import StrategyService
from services.financial_state_service import FinancialStateService


class MultiGoalPlanningService:
    """Service layer coordinating multi-goal planning workflows using MultiGoalOrchestrator."""

    def __init__(
        self,
        goal_repo: GoalRepository | None = None,
        strategy_repo: StrategyRepository | None = None,
        strategy_service: StrategyService | None = None,
        goal_report_service: GoalReportService | None = None,
        orchestrator: MultiGoalOrchestrator | None = None,
        financial_state_service: FinancialStateService | None = None,
    ):
        self.goal_repo = goal_repo or GoalRepository()
        self.strategy_repo = strategy_repo or StrategyRepository()
        self.strategy_service = strategy_service or StrategyService()
        self.goal_report_service = goal_report_service or GoalReportService()
        self.orchestrator = orchestrator or MultiGoalOrchestrator()
        self.constraint_aggregator = ConstraintAggregator()
        self.financial_state_service = financial_state_service or FinancialStateService()

    def build_multi_goal_plan(
        self,
        planning_unit_id: str,
        priorities: InvestorPriorities | None = None,
        rule_overrides: dict[str, dict[str, Any]] | None = None,
        priority_ranks: dict[str, int] | None = None,
        goal_order: list[str] | None = None,
    ) -> MultiGoalPlanResult:
        goals = self.goal_repo.list_goals(planning_unit_id)
        if not goals:
            raise HTTPException(status_code=404, detail="No goals found for this planning unit")

        inputs: list[GoalEvaluationInput] = []
        strategy_eval_map: dict[str, dict[str, Any]] = {}

        for idx, goal in enumerate(goals):
            goal_id = goal["goal_id"]
            strategy_version_id = self.strategy_repo.get_selected_strategy_version_id(planning_unit_id, goal_id)
            if not strategy_version_id:
                raise HTTPException(
                    status_code=404,
                    detail=f"No current StrategyVersion selected for goal '{goal_id}'. Finalize a strategy version before building the current multi-goal plan.",
                )

            report = self.goal_report_service.build_report(
                planning_unit_id,
                strategy_version_id=strategy_version_id,
            )
            calc = report.get("goal_calculation", {})
            rec = report.get("recommendation", {})

            if goal_order and goal_id in goal_order:
                rank = goal_order.index(goal_id) + 1
            elif priority_ranks and goal_id in priority_ranks:
                rank = int(priority_ranks[goal_id])
            elif goal.get("priority_rank"):
                rank = int(goal["priority_rank"])
            else:
                rank = idx + 1

            client_p = goal.get("priority") or calc.get("priority") or "medium"
            today_cost = float(calc.get("today_cost") or 0.0)
            future_target = float(calc.get("future_target") or 0.0)
            funding_gap = float(calc.get("funding_gap") or 0.0)
            req_monthly = float(calc.get("required_monthly_contribution") or 0.0)

            t_year = calc.get("target_year")
            t_month = calc.get("target_month")
            target_date = f"{t_year}-{t_month:02d}" if t_year and t_month else None

            eval_input = GoalEvaluationInput(
                goal_id=goal_id,
                goal_name=report.get("goal_name") or goal.get("goal_name") or goal_id,
                goal_type=report.get("goal_type") or goal.get("goal_type") or "general",
                priority_rank=rank,
                client_priority=client_p,
                target_date=target_date,
                target_year=t_year,
                target_month=t_month,
                today_cost=today_cost,
                future_target=future_target,
                funding_gap=funding_gap,
                required_monthly_contribution=req_monthly,
                flexibility=goal.get("flexibility"),
            )
            inputs.append(eval_input)

            strategy_eval_map[goal_id] = {
                "recommended_strategy_id": report.get("selected_strategy_id") or rec.get("recommended_strategy_id"),
                "recommended_strategy_name": report.get("strategy", {}).get("name"),
                "strategy_version_id": strategy_version_id,
                "feasibility_status": {"feasible": "pass", "constrained": "conditional"}.get(
                    rec.get("feasibility_status"), rec.get("feasibility_status") or "pass"
                ),
                "required_monthly_contribution": req_monthly,
                "today_cost": calc.get("today_cost"),
                "future_target": calc.get("future_target"),
                "funding_gap": calc.get("funding_gap"),
                "projected_mapped_asset_value": calc.get("projected_mapped_asset_value"),
                "funding_return_assumption": calc.get("funding_return_assumption"),
                "available_monthly_surplus": report.get("feasibility", {}).get(
                    "available_monthly_surplus"
                ),
                "funding_strategies": report.get("funding_solutions", []),
                "reasons": rec.get("short_reasons", []),
            }

        # Consume the canonical current FinancialState directly.
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

        # Single canonical constraint path: all ratio/rule-derived controls are
        # evaluated and normalized by ConstraintAggregator into ConstraintSet.
        canonical_constraint_set = self.constraint_aggregator.aggregate(
            goals=inputs,
            financial_context=financial_context,
            planning_unit_id=planning_unit_id,
        )
        effective_overrides = canonical_constraint_set.suggested_overrides()
        if rule_overrides:
            effective_overrides.update(rule_overrides)

        def eval_lookup(goal_input: GoalEvaluationInput, context: dict[str, Any]) -> dict[str, Any]:
            return strategy_eval_map.get(goal_input.goal_id, {})

        plan = self.orchestrator.orchestrate(
            goals=inputs,
            financial_context=financial_context,
            strategy_evaluator=eval_lookup,
            rule_overrides=effective_overrides,
        )

        # Surface the canonical constraint output; no second evaluator path.
        for warning in canonical_constraint_set.warnings:
            plan.planning_notes.append(f"Constraint Warning: {warning.message}")
        for hard in canonical_constraint_set.hard_constraints:
            plan.trade_offs.append(f"Constraint: {hard.message}")

        # Attach the canonical constraint set to the plan's audit trail
        plan.audit_trail.append({
            "source": "ConstraintAggregator",
            "canonical_constraint_set": canonical_constraint_set.model_dump(),
            "constraint_count": len(canonical_constraint_set.constraints),
            "conflict_count": len(canonical_constraint_set.conflicts),
            "hard_failure_count": len(canonical_constraint_set.hard_constraints),
        })

        return plan
