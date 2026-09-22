from typing import Any

from models.action_plan import ActionDecisionRecord, ActionImpactPreview, ActionPlanItem
from models.financial_state import FinancialState
from engines.action_plan.impact_engine import ActionImpactEngine


class ActionPlanService:
    """Builds actions, executes decisions, preserves history, and compares impact."""

    _EDITABLE_FIELDS = {"title", "description", "priority", "deadline", "planned_impact"}

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
        if not self.repository.is_strategy_version_approved(planning_unit_id, strategy_version_id):
            raise ValueError("Implementation actions can only be created for an approved Strategy Version")
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

        if decision == "add":
            if action.status != "planned":
                raise ValueError("Only planned actions can be added/confirmed")
            updated = self.repository.update_action(
                action.planning_unit_id, action.action_id, {"status": "confirmed"}
            )
            resulting_state = updated.model_dump(mode="json")

        elif decision == "modify":
            if action.status not in {"planned", "confirmed"}:
                raise ValueError("Only planned or confirmed actions can be modified")
            requested = after_state or {}
            updates = {key: requested[key] for key in self._EDITABLE_FIELDS if key in requested}
            if not updates:
                raise ValueError("Modify decision contains no editable action fields")
            updated = self.repository.update_action(
                action.planning_unit_id, action.action_id, updates
            )
            resulting_state = updated.model_dump(mode="json")

        elif decision == "complete":
            if action.status not in {"planned", "confirmed"}:
                raise ValueError("Only planned or confirmed actions can be completed")
            updated = self.repository.update_action(
                action.planning_unit_id, action.action_id, {"status": "completed"}
            )
            resulting_state = updated.model_dump(mode="json")

        elif decision == "cancel":
            if action.status not in {"planned", "confirmed"}:
                raise ValueError("Only planned or confirmed actions can be cancelled")
            updated = self.repository.update_action(
                action.planning_unit_id, action.action_id, {"status": "cancelled"}
            )
            resulting_state = updated.model_dump(mode="json")

        else:  # delete
            if action.status in {"completed", "cancelled"}:
                raise ValueError("Completed or cancelled actions cannot be deleted")
            resulting_state = {"action_id": action.action_id, "deleted": True}
            self.repository.delete_action(action.planning_unit_id, action.action_id)

        return self.repository.record_decision(ActionDecisionRecord(
            planning_unit_id=action.planning_unit_id,
            action_id=action.action_id,
            decision=decision,  # type: ignore[arg-type]
            before_state=action.model_dump(mode="json"),
            after_state=resulting_state,
            impact_preview=preview,
        ))

    def complete_action(
        self,
        action: ActionPlanItem,
        projected_state: FinancialState,
        actual_state: FinancialState,
        completion_preview: ActionImpactPreview,
    ) -> tuple[ActionPlanItem, ActionDecisionRecord, dict[str, Any]]:
        """Complete an action after the actual Financial State has been confirmed."""
        if not action.action_id:
            raise ValueError("Action must have an action_id before completion")
        if action.status not in {"planned", "confirmed"}:
            raise ValueError("Only planned or confirmed actions can be completed")

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
