from __future__ import annotations

from typing import Any, Callable
from engines.allocation.engine import ResourceAllocationEngine
from rules.multi_goal import get_priority_rank
from rules.goals import GoalPriority
from engines.orchestration.models import (
    GoalEvaluationInput,
    GoalResolution,
    MultiGoalPlanResult,
)


class MultiGoalOrchestrator:
    """Coordinates multiple goals competing for shared resources without replacing single-goal StrategyEngine."""

    def __init__(self, allocation_engine: ResourceAllocationEngine | None = None):
        self.allocation_engine = allocation_engine or ResourceAllocationEngine()

    @classmethod
    def priority_rank(cls, priority: str | None) -> int:
        return get_priority_rank(priority)

    def resolve_goal_priority(
        self,
        goal: GoalEvaluationInput,
        financial_context: dict[str, Any],
        rule_overrides: dict[str, dict[str, Any]] | None = None,
    ) -> tuple[GoalPriority, bool, str | None]:
        """Determines resolved priority while preserving client_priority for auditability.

        If explicit rule_overrides specifies an override for goal_id, or if an approved rule applies,
        resolves priority accordingly.
        """
        client_p = goal.client_priority
        if rule_overrides and goal.goal_id in rule_overrides:
            override_info = rule_overrides[goal.goal_id]
            new_priority = override_info.get("resolved_priority", client_p)
            reason = override_info.get("reason", "System rule constraint applied.")
            if new_priority != client_p:
                return new_priority, True, reason

        return client_p, False, None

    def orchestrate(
        self,
        goals: list[GoalEvaluationInput],
        financial_context: dict[str, Any] | None = None,
        strategy_evaluator: Callable[[GoalEvaluationInput, dict[str, Any]], dict[str, Any]] | None = None,
        rule_overrides: dict[str, dict[str, Any]] | None = None,
    ) -> MultiGoalPlanResult:
        """Executes multi-goal orchestration across competing goals and resources."""
        if not goals:
            return MultiGoalPlanResult(
                financial_state=financial_context or {},
                overall_funding_status="requires_review",
                planning_notes=["No goals provided for orchestration."],
            )

        context = dict(financial_context or {})
        surplus_val = context.get("monthly_surplus")
        available_surplus = float(surplus_val) if surplus_val is not None else None

        # Step 1: Evaluate each goal independently (reuse StrategyEngine or evaluator)
        evaluated_goals: list[tuple[GoalEvaluationInput, dict[str, Any]]] = []
        for g in goals:
            strat_info = {}
            if strategy_evaluator:
                strat_info = strategy_evaluator(g, context)
            evaluated_goals.append((g, strat_info))

        # Step 2: Resolve priorities & prepare allocation payload
        allocation_items: list[dict[str, Any]] = []
        strat_map: dict[str, dict[str, Any]] = {}

        for g, s_info in evaluated_goals:
            req_contrib = float(g.required_monthly_contribution or s_info.get("required_monthly_contribution", 0.0))
            strat_map[g.goal_id] = s_info

            resolved_p, override_applied, override_reason = self.resolve_goal_priority(
                g, context, rule_overrides
            )

            target_dt = g.target_date or (
                f"{g.target_year}-{g.target_month:02d}" if g.target_year and g.target_month else None
            )

            allocation_items.append({
                "goal_id": g.goal_id,
                "goal_name": g.goal_name,
                "goal_type": g.goal_type,
                "client_priority": g.client_priority,
                "resolved_priority": resolved_p,
                "required_monthly_contribution": req_contrib,
                "target_date": target_dt,
                "override_applied": override_applied,
                "override_reason": override_reason,
            })

        # Step 3: Execute Resource Allocation Engine (Step 04)
        alloc_result = self.allocation_engine.allocate(
            goals=allocation_items,
            available_monthly_surplus=available_surplus,
        )

        # Step 4: Assemble GoalResolutions, Audit Trail, and Action Plan
        goal_resolutions: list[GoalResolution] = []
        audit_trail: list[dict[str, Any]] = []

        for item in alloc_result.allocations:
            s_info = strat_map.get(item.goal_id, {})
            reasons = list(s_info.get("reasons", []))
            if item.override_applied and item.override_reason:
                reasons.append(f"Priority Adjusted: {item.override_reason}")

            res = GoalResolution(
                goal_id=item.goal_id,
                goal_name=item.goal_name,
                goal_type=item.goal_type,
                client_priority=item.client_priority,
                resolved_priority=item.resolved_priority,
                target_date=item.target_date,
                required_monthly_contribution=item.required_monthly_contribution,
                allocated_monthly_contribution=item.allocated_monthly_contribution,
                shortfall=item.monthly_shortfall,
                funding_status=item.funding_status,
                feasibility_status=item.feasibility_status,
                recommended_strategy_id=s_info.get("recommended_strategy_id"),
                recommended_strategy_name=s_info.get("recommended_strategy_name"),
                override_applied=item.override_applied,
                override_reason=item.override_reason,
                reasons=reasons,
                notes=s_info.get("notes", []) + ([item.allocation_reasoning] if item.allocation_reasoning else []),
            )
            goal_resolutions.append(res)

            audit_trail.append({
                "goal_id": item.goal_id,
                "goal_name": item.goal_name,
                "client_priority": item.client_priority,
                "resolved_priority": item.resolved_priority,
                "override_applied": item.override_applied,
                "override_reason": item.override_reason,
                "required_monthly_contribution": item.required_monthly_contribution,
                "allocated_monthly_contribution": item.allocated_monthly_contribution,
                "funding_status": item.funding_status,
                "allocation_reasoning": item.allocation_reasoning,
            })

        # Step 5: Action Plan formulation
        actions = []
        for index, res in enumerate(goal_resolutions, start=1):
            actions.append({
                "sequence": index,
                "goal_id": res.goal_id,
                "goal_name": res.goal_name,
                "action": f"Allocate {res.allocated_monthly_contribution:.2f}/month to {res.goal_name} (Priority: {res.resolved_priority}).",
                "monthly_contribution": res.allocated_monthly_contribution,
                "required_contribution": res.required_monthly_contribution,
                "target_date": res.target_date,
                "funding_status": res.funding_status,
            })

        planning_notes = [
            "Goals are prioritized by resolved priority and target date.",
            "Client-selected priorities are preserved for full traceability.",
        ]
        if alloc_result.competition_detected:
            planning_notes.append("Multiple goals are competing for the same investable surplus.")
        if any(r.override_applied for r in goal_resolutions):
            planning_notes.append("One or more goals have system-resolved priorities due to business/financial rules.")

        planning_notes.extend(alloc_result.decision_log)

        return MultiGoalPlanResult(
            planning_unit_id=context.get("planning_unit_id"),
            financial_state=context,
            total_available_surplus=alloc_result.total_available_monthly_surplus,
            total_required_contribution=alloc_result.total_required_monthly_contribution,
            total_allocated_contribution=alloc_result.total_allocated_monthly_contribution,
            monthly_gap=alloc_result.net_monthly_gap,
            overall_funding_status=alloc_result.overall_funding_status,
            goals=goal_resolutions,
            competing_resources_detected=alloc_result.competition_detected,
            trade_offs=alloc_result.trade_offs,
            action_plan=actions,
            audit_trail=audit_trail,
            planning_notes=planning_notes,
        )
