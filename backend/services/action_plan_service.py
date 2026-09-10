from typing import Any

from models.action_plan import ActionDecisionRecord, ActionImpactPreview, ActionPlanItem
from models.financial_state import FinancialState
from engines.action_plan.impact_engine import ActionImpactEngine


class ActionPlanService:
    """Builds actions, preserves decisions, and compares completed-action impact."""

    def __init__(self, repository):
        self.repository = repository
        self.impact_engine = ActionImpactEngine()

    def build_action(
        self,
        planning_unit_id: str,
        strategy_version_id: str,
        title: str,
        description: str | None = None,
        priority: str = "medium",
        deadline: str | None = None,
        planned_impact: dict[str, Any] | None = None,
    ) -> ActionPlanItem:
        return self.repository.save_action(ActionPlanItem(
            planning_unit_id=planning_unit_id,
            strategy_version_id=strategy_version_id,
            title=title,
            description=description,
            priority=priority,  # type: ignore[arg-type]
            deadline=deadline,
            planned_impact=planned_impact or {},
        ))

    def confirm_decision(
        self,
        action: ActionPlanItem,
        decision: str,
        preview: ActionImpactPreview,
        after_state: dict[str, Any] | None = None,
    ) -> ActionDecisionRecord:
        if not action.action_id:
            raise ValueError("Action must have an action_id before recording a decision")
        if decision not in {"add", "modify", "delete", "complete", "cancel"}:
            raise ValueError(f"Invalid action decision: {decision}")
        return self.repository.record_decision(ActionDecisionRecord(
            planning_unit_id=action.planning_unit_id,
            action_id=action.action_id,
            decision=decision,  # type: ignore[arg-type]
            before_state=action.model_dump(mode="json"),
            after_state=after_state or action.model_dump(mode="json"),
            impact_preview=preview,
        ))

    def complete_action(
        self,
        action: ActionPlanItem,
        projected_state: FinancialState,
        actual_state: FinancialState,
        completion_preview: ActionImpactPreview,
    ) -> tuple[ActionPlanItem, ActionDecisionRecord, dict[str, Any]]:
        """Complete an action after the actual Financial State has been confirmed.

        This method does not mutate source financial records. The actual state must
        already reflect the investor-confirmed data update. It only computes and
        preserves the Actual-vs-Projected comparison.
        """
        if not action.action_id:
            raise ValueError("Action must have an action_id before completion")

        comparison = self.impact_engine.compare(projected_state, actual_state)
        actual_impact = {
            "financial_state": actual_state.model_dump(mode="json"),
            "variance_analysis": comparison,
        }
        updated = self.repository.update_action(
            action.planning_unit_id,
            action.action_id,
            {"status": "completed", "actual_impact": actual_impact},
        )
        record = self.repository.record_decision(ActionDecisionRecord(
            planning_unit_id=action.planning_unit_id,
            action_id=action.action_id,
            decision="complete",
            before_state=action.model_dump(mode="json"),
            after_state=updated.model_dump(mode="json"),
            impact_preview=completion_preview,
        ))
        return updated, record, comparison
