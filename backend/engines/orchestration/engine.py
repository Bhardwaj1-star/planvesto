from __future__ import annotations

from typing import Any, Callable
from engines.orchestration.models import (
    GoalEvaluationInput,
    GoalPriorityLevel,
    GoalResolution,
    MultiGoalPlanResult,
)


class MultiGoalOrchestrator:
    """Coordinates multiple goals competing for shared resources without replacing single-goal StrategyEngine."""

    PRIORITY_RANKS: dict[str, int] = {
        "critical": 0,
        "high": 1,
        "medium": 2,
        "low": 3,
    }

    @classmethod
    def priority_rank(cls, priority: str | None) -> int:
        return cls.PRIORITY_RANKS.get(str(priority or "").lower(), 4)

    def resolve_goal_priority(
        self,
        goal: GoalEvaluationInput,
        financial_context: dict[str, Any],
        rule_overrides: dict[str, dict[str, Any]] | None = None,
    ) -> tuple[GoalPriorityLevel, bool, str | None]:
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

        # Step 2: Resolve priorities & check competition
        resolutions_pre: list[dict[str, Any]] = []
        total_required = 0.0

        for g, s_info in evaluated_goals:
            req_contrib = float(g.required_monthly_contribution or s_info.get("required_monthly_contribution", 0.0))
            total_required += req_contrib

            resolved_p, override_applied, override_reason = self.resolve_goal_priority(
                g, context, rule_overrides
            )

            target_dt = g.target_date or (
                f"{g.target_year}-{g.target_month:02d}" if g.target_year and g.target_month else None
            )

            resolutions_pre.append({
                "input": g,
                "strat_info": s_info,
                "client_priority": g.client_priority,
                "resolved_priority": resolved_p,
                "override_applied": override_applied,
                "override_reason": override_reason,
                "required_monthly_contribution": req_contrib,
                "target_date": target_dt,
            })

        # Step 3: Sort by resolved priority, then target date
        resolutions_pre.sort(
            key=lambda item: (
                self.priority_rank(item["resolved_priority"]),
                item["target_date"] or "9999-99",
            )
        )

        competing_resources = False
        if available_surplus is not None and len(goals) > 1:
            if total_required > available_surplus:
                competing_resources = True

        # Step 4: Deterministic Resource Allocation across goals
        remaining_surplus = available_surplus if available_surplus is not None else 0.0
        total_allocated = 0.0
        goal_resolutions: list[GoalResolution] = []
        audit_trail: list[dict[str, Any]] = []
        trade_offs: list[str] = []

        for item in resolutions_pre:
            g = item["input"]
            s_info = item["strat_info"]
            req = item["required_monthly_contribution"]
            client_p = item["client_priority"]
            resolved_p = item["resolved_priority"]
            target_dt = item["target_date"]
            override_applied = item["override_applied"]
            override_reason = item["override_reason"]

            allocated = 0.0
            funding_status = "requires_review"
            feasibility = s_info.get("feasibility_status", "feasible")

            if available_surplus is not None:
                if remaining_surplus >= req:
                    allocated = req
                    remaining_surplus -= req
                    funding_status = "fully_funded"
                elif remaining_surplus > 0:
                    allocated = round(remaining_surplus, 2)
                    remaining_surplus = 0.0
                    funding_status = "partially_funded"
                    feasibility = "constrained"
                    trade_offs.append(
                        f"Goal '{g.goal_name}' is partially funded ({allocated:.2f} of {req:.2f}/month) due to limited investable surplus."
                    )
                else:
                    allocated = 0.0
                    funding_status = "unfunded"
                    feasibility = "infeasible" if req > 0 else "feasible"
                    trade_offs.append(
                        f"Goal '{g.goal_name}' cannot be funded from current monthly surplus."
                    )

            total_allocated += allocated
            shortfall = max(0.0, round(req - allocated, 2))

            reasons = list(s_info.get("reasons", []))
            if override_applied and override_reason:
                reasons.append(f"Priority Adjusted: {override_reason}")

            res = GoalResolution(
                goal_id=g.goal_id,
                goal_name=g.goal_name,
                goal_type=g.goal_type,
                client_priority=client_p,
                resolved_priority=resolved_p,
                target_date=target_dt,
                required_monthly_contribution=req,
                allocated_monthly_contribution=allocated,
                shortfall=shortfall,
                funding_status=funding_status,
                feasibility_status=feasibility,
                recommended_strategy_id=s_info.get("recommended_strategy_id"),
                recommended_strategy_name=s_info.get("recommended_strategy_name"),
                override_applied=override_applied,
                override_reason=override_reason,
                reasons=reasons,
                notes=s_info.get("notes", []),
            )
            goal_resolutions.append(res)

            audit_trail.append({
                "goal_id": g.goal_id,
                "goal_name": g.goal_name,
                "client_priority": client_p,
                "resolved_priority": resolved_p,
                "override_applied": override_applied,
                "override_reason": override_reason,
                "required_monthly_contribution": req,
                "allocated_monthly_contribution": allocated,
                "funding_status": funding_status,
            })

        # Step 5: Overall summary metrics
        monthly_gap = round(total_required - available_surplus, 2) if available_surplus is not None else None
        if monthly_gap is None:
            overall_status = "requires_review"
        elif monthly_gap <= 0:
            overall_status = "within_surplus"
        else:
            overall_status = "surplus_shortfall"

        # Step 6: Formulate Action Plan
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
        if competing_resources:
            planning_notes.append("Multiple goals are competing for the same investable surplus.")
        if any(r.override_applied for r in goal_resolutions):
            planning_notes.append("One or more goals have system-resolved priorities due to business/financial rules.")

        return MultiGoalPlanResult(
            planning_unit_id=context.get("planning_unit_id"),
            financial_state=context,
            total_available_surplus=available_surplus,
            total_required_contribution=round(total_required, 2),
            total_allocated_contribution=round(total_allocated, 2),
            monthly_gap=monthly_gap,
            overall_funding_status=overall_status,
            goals=goal_resolutions,
            competing_resources_detected=competing_resources,
            trade_offs=trade_offs,
            action_plan=actions,
            audit_trail=audit_trail,
            planning_notes=planning_notes,
        )
