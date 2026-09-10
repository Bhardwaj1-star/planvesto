from typing import Any

from models.action_plan import ActionDecisionRecord, ActionImpactPreview, ActionPlanItem


class ActionPlanService:
    """Builds planned actions and requires an impact preview before decisions.

    Financial calculations are intentionally delegated to downstream engines;
    this layer preserves the decision contract and never invents numbers.
    """

    def __init__(self, repository):
        self.repository = repository

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
        if decision not in {"add", "modify", "delete", "complete", "cancel"}:
            raise ValueError(f"Invalid action decision: {decision}")
        return self.repository.record_decision(ActionDecisionRecord(
            planning_unit_id=action.planning_unit_id,
            action_id=action.action_id or "",
            decision=decision,  # type: ignore[arg-type]
            before_state=action.model_dump(mode="json"),
            after_state=after_state or action.model_dump(mode="json"),
            impact_preview=preview,
        ))
