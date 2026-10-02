from __future__ import annotations

from typing import Any
from rules.constraints import PRIORITY_RANKS
from engines.allocation.models import (
    ConsolidatedAllocationResult,
    GoalAllocationResult,
    GoalPriorityLevel,
)


class ResourceAllocationEngine:
    """Allocates shared financial resources across goals after single-goal strategies and constraints have been evaluated."""

    PRIORITY_RANKS = PRIORITY_RANKS

    @classmethod
    def priority_rank(cls, priority: str | None) -> int:
        return cls.PRIORITY_RANKS.get(str(priority or "").lower(), 4)

    def allocate(
        self,
        goals: list[dict[str, Any]],
        available_monthly_surplus: float | None,
    ) -> ConsolidatedAllocationResult:
        if not goals:
            return ConsolidatedAllocationResult(
                total_available_monthly_surplus=available_monthly_surplus,
                total_required_monthly_contribution=0.0,
                total_allocated_monthly_contribution=0.0,
                net_monthly_gap=0.0,
                overall_funding_status="within_surplus" if (available_monthly_surplus or 0) >= 0 else "surplus_shortfall",
                competition_detected=False,
                decision_log=["No goals submitted for resource allocation."],
            )

        total_required = round(sum(float(g.get("required_monthly_contribution") or 0.0) for g in goals), 2)
        surplus = float(available_monthly_surplus) if available_monthly_surplus is not None else None

        competition = False
        if surplus is not None and len(goals) > 1 and total_required > surplus:
            competition = True

        # Sort goals by resolved_priority, then target date
        sorted_goals = sorted(
            goals,
            key=lambda item: (
                self.priority_rank(item.get("resolved_priority") or item.get("client_priority")),
                item.get("target_date") or "9999-99",
            ),
        )

        remaining_surplus = surplus if surplus is not None else 0.0
        total_allocated = 0.0
        allocated_items: list[GoalAllocationResult] = []
        trade_offs: list[str] = []
        decision_log: list[str] = []

        if competition:
            decision_log.append(
                f"Resource competition detected: Total required ({total_required:.2f}/mo) exceeds available surplus ({surplus:.2f}/mo)."
            )

        for g in sorted_goals:
            goal_id = g.get("goal_id", "")
            goal_name = g.get("goal_name", goal_id)
            goal_type = g.get("goal_type", "general")
            client_p: GoalPriorityLevel = g.get("client_priority", "medium")
            resolved_p: GoalPriorityLevel = g.get("resolved_priority", client_p)
            req = float(g.get("required_monthly_contribution") or 0.0)
            target_dt = g.get("target_date")
            override_applied = bool(g.get("override_applied", False))
            override_reason = g.get("override_reason")

            allocated = 0.0
            trade_off_impact = None

            if surplus is not None:
                if remaining_surplus >= req:
                    allocated = req
                    remaining_surplus = round(remaining_surplus - req, 2)
                    funding_status = "fully_funded"
                    funding_pct = 100.0 if req > 0 else 100.0
                    feasibility = "feasible"
                    reasoning = f"Fully funded from investable monthly surplus (Priority: {resolved_p})."
                elif remaining_surplus > 0:
                    allocated = round(remaining_surplus, 2)
                    remaining_surplus = 0.0
                    funding_status = "partially_funded"
                    funding_pct = round((allocated / req) * 100.0, 1) if req > 0 else 0.0
                    feasibility = "constrained"
                    trade_off_impact = (
                        f"Goal '{goal_name}' receives {allocated:.2f} of {req:.2f}/mo ({funding_pct}% funded). "
                        f"Monthly shortfall is {req - allocated:.2f}."
                    )
                    trade_offs.append(trade_off_impact)
                    reasoning = f"Partially funded ({allocated:.2f} of {req:.2f}/mo). Remaining surplus was exhausted."
                else:
                    allocated = 0.0
                    funding_status = "unfunded"
                    funding_pct = 0.0
                    feasibility = "infeasible" if req > 0 else "feasible"
                    trade_off_impact = f"Goal '{goal_name}' is unfunded from current monthly surplus due to higher-priority allocations."
                    trade_offs.append(trade_off_impact)
                    reasoning = "Unfunded from current cash flow. Surplus was fully committed to higher-priority goals."
            else:
                funding_status = "requires_review"
                funding_pct = 0.0
                feasibility = "constrained"
                reasoning = "Available monthly surplus is unconfigured; funding allocation pending financial state verification."

            if override_applied and override_reason:
                reasoning += f" [System Override: Client selected '{client_p}', resolved to '{resolved_p}' — Reason: {override_reason}]"
                decision_log.append(f"Override applied to '{goal_name}': {override_reason}")

            shortfall = max(0.0, round(req - allocated, 2))
            total_allocated = round(total_allocated + allocated, 2)

            allocated_items.append(GoalAllocationResult(
                goal_id=goal_id,
                goal_name=goal_name,
                goal_type=goal_type,
                client_priority=client_p,
                resolved_priority=resolved_p,
                target_date=target_dt,
                required_monthly_contribution=req,
                allocated_monthly_contribution=allocated,
                monthly_shortfall=shortfall,
                funding_percentage=funding_pct,
                funding_status=funding_status,
                feasibility_status=feasibility,
                allocation_reasoning=reasoning,
                override_applied=override_applied,
                override_reason=override_reason,
                trade_off_impact=trade_off_impact,
            ))

        net_gap = round(total_required - surplus, 2) if surplus is not None else None
        if net_gap is None:
            overall_status = "requires_review"
        elif net_gap <= 0:
            overall_status = "within_surplus"
        else:
            overall_status = "surplus_shortfall"

        return ConsolidatedAllocationResult(
            total_available_monthly_surplus=surplus,
            total_required_monthly_contribution=total_required,
            total_allocated_monthly_contribution=total_allocated,
            net_monthly_gap=net_gap,
            overall_funding_status=overall_status,
            competition_detected=competition,
            allocations=allocated_items,
            trade_offs=trade_offs,
            decision_log=decision_log,
        )
