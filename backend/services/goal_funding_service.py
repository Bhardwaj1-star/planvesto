from fastapi import HTTPException
from data.goal_repository import GoalRepository
from data.goal_funding_repository import GoalFundingRepository
from models.goal_funding import GoalFundingAssessment, GoalFundingAssessmentRequest
from rules.goal_funding import assess_path_evidence, compare_funding_paths


class GoalFundingService:
    def __init__(self):
        self.goals = GoalRepository()
        self.repository = GoalFundingRepository()

    def assess(self, request: GoalFundingAssessmentRequest) -> GoalFundingAssessment:
        goal = self.goals.get_defined_goal_by_version(
            request.planning_unit_id, request.goal_id, request.defined_goal_version
        )
        if goal is None:
            raise HTTPException(status_code=404, detail="Defined Goal version not found")
        if not goal.defined_goal_id:
            raise HTTPException(status_code=409, detail="Defined Goal handoff is missing its identity")

        mapped_ids = {asset.asset_id for asset in goal.mapped_assets}
        entry_route = "steps_1_to_3_then_step_4" if mapped_ids else "step_4_direct"
        handoff = {
            "defined_goal_id": goal.defined_goal_id,
            "defined_goal_version": goal.version,
            "goal_name": goal.goal_name,
            "goal_type": goal.goal_type,
            "future_target": goal.future_target,
            "target_month": goal.target_month,
            "target_year": goal.target_year,
            "duration_years": goal.duration_years,
            "funding_gap": goal.funding_gap,
            "funding_status": goal.funding_status,
            "feasibility_status": goal.feasibility_status,
            "required_monthly_contribution": goal.required_monthly_contribution,
            "funding_return_assumption": goal.funding_return_assumption,
            "mapped_assets": [item.model_dump(mode="json") for item in goal.mapped_assets],
            "version_metadata": goal.version_metadata,
        }
        self_evidence = assess_path_evidence(request.self_money, mapped_ids)
        finance_evidence = assess_path_evidence(request.self_money_financing, mapped_ids)
        comparison = compare_funding_paths(self_evidence, finance_evidence)

        # Step 3 is deliberately a hand-back to Goal Planner. Strategy does not
        # calculate a replacement Required SIP or Required Lump Sum.
        for label, path in (
            ("Self Money", request.self_money),
            ("Self Money + Financing", request.self_money_financing),
        ):
            unapproved = [
                decision.asset_id for decision in path.asset_decisions
                if decision.disposition == "reallocate" and not decision.investor_approved
            ]
            if unapproved:
                comparison.setdefault("blocking_items", []).append(
                    f"{label}: asset reallocation awaits investor approval ({', '.join(unapproved)})."
                )

        status = "insufficient_evidence" if comparison["status"] != "comparable" else "ready_for_investor_review"
        assessment = GoalFundingAssessment(
            planning_unit_id=request.planning_unit_id,
            goal_id=request.goal_id,
            defined_goal_id=goal.defined_goal_id,
            defined_goal_version=goal.version,
            status=status,
            entry_route=entry_route,
            goal_handoff=handoff,
            self_money=request.self_money,
            self_money_financing=request.self_money_financing,
            comparison=comparison,
            investor_decision=request.investor_decision,
            investor_decision_confirmed=request.investor_decision_confirmed,
            decision_notes=request.decision_notes,
        )
        return self.repository.save(assessment)

    def latest(self, planning_unit_id: str, goal_id: str):
        return self.repository.get_latest(planning_unit_id, goal_id)

    def history(self, planning_unit_id: str, goal_id: str):
        return self.repository.list_history(planning_unit_id, goal_id)
