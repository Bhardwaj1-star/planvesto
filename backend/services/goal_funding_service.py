from fastapi import HTTPException
from data.goal_repository import GoalRepository
from data.goal_funding_repository import GoalFundingRepository
from data.financial_state_repository import FinancialStateSnapshotRepository
from services.financial_state_service import FinancialStateService
from models.goal_funding import GoalFundingAssessment, GoalFundingAssessmentRequest
from rules.goal_funding import assess_path_evidence, compare_funding_paths


class GoalFundingService:
    def __init__(self):
        self.goals = GoalRepository()
        self.repository = GoalFundingRepository()
        self.financial_state_service = FinancialStateService(
            snapshot_repository=FinancialStateSnapshotRepository()
        )

    @staticmethod
    def _metric_value(state, key):
        value = state.get(key) if isinstance(state, dict) else None
        if isinstance(value, dict):
            return value.get("value")
        return getattr(value, "value", value)

    def assess(self, request: GoalFundingAssessmentRequest) -> GoalFundingAssessment:
        goal = self.goals.get_defined_goal_by_version(
            request.planning_unit_id, request.goal_id, request.defined_goal_version
        )
        if goal is None:
            raise HTTPException(status_code=404, detail="Defined Goal version not found")
        if not goal.defined_goal_id:
            raise HTTPException(status_code=409, detail="Defined Goal handoff is missing its identity")

        financial_snapshot = self.financial_state_service.get_current_snapshot(request.planning_unit_id, "family")
        financial_state = financial_snapshot.get("financial_state") or {}
        if hasattr(financial_state, "model_dump"):
            financial_state = financial_state.model_dump(mode="json")
        available_monthly_surplus = self._metric_value(financial_state, "investable_surplus_monthly")
        monthly_debt_payments = self._metric_value(financial_state, "emi_burden_monthly")

        mapped_ids = {asset.asset_id for asset in goal.mapped_assets}
        mapped_assets = {asset.asset_id: asset for asset in goal.mapped_assets}
        for path in (request.self_money, request.self_money_financing):
            for decision in path.asset_decisions:
                mapped_asset = mapped_assets.get(decision.asset_id)
                if mapped_asset and decision.assessed_amount is not None and decision.assessed_amount > mapped_asset.allocated_amount + 0.01:
                    raise HTTPException(status_code=422, detail=f"Assessed amount for asset {decision.asset_id} exceeds the amount mapped to this goal.")
                if mapped_asset and (decision.disposition.value == "reallocate" or (decision.assessed_amount is not None and decision.assessed_amount < mapped_asset.allocated_amount - 0.01)):
                    path.step_3_requirement_changed = True
                if decision.asset_id in mapped_ids and decision.available_on and (decision.available_on.year, decision.available_on.month) > (goal.target_year, goal.target_month):
                    raise HTTPException(status_code=422, detail=f"Asset {decision.asset_id} is not available in the goal funding month.")
                if not decision.risk_suitability_assessment:
                    raise HTTPException(status_code=422, detail=f"Risk suitability assessment is required for asset {decision.asset_id}.")

        entry_route = "steps_1_to_3_then_step_4" if mapped_ids else "step_4_direct"
        for path in (request.self_money, request.self_money_financing):
            if path.self_money_requirement is None and not path.step_3_requirement_changed:
                path.self_money_requirement = goal.funding_gap
            elif path.self_money_requirement is not None and not path.step_3_requirement_changed and abs(path.self_money_requirement - goal.funding_gap) > 0.01:
                raise HTTPException(status_code=409, detail="Self-money requirement differs from Chapter 10; submit approved asset decisions for Goal Planner recalculation first.")
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
            "funding_options": goal.funding_options,
            "funding_return_assumption": goal.funding_return_assumption,
            "mapped_assets": [item.model_dump(mode="json") for item in goal.mapped_assets],
            "available_monthly_surplus": available_monthly_surplus,
            "financial_state_snapshot_id": financial_snapshot.get("snapshot_id"),
            "monthly_debt_payments": monthly_debt_payments,
            "version_metadata": goal.version_metadata,
        }

        self_evidence = assess_path_evidence(request.self_money, mapped_ids)
        finance_evidence = assess_path_evidence(request.self_money_financing, mapped_ids)
        financing = request.self_money_financing.financing
        if financing and available_monthly_surplus is None:
            finance_evidence["issues"].append("Current Available Monthly Surplus is unavailable; financing repayment capacity cannot be assessed.")
            finance_evidence["status"] = "insufficient_evidence"
        elif financing and available_monthly_surplus is not None and float(available_monthly_surplus) <= 0:
            finance_evidence["issues"].append("Current Available Monthly Surplus is zero or negative; financing repayment capacity is not established.")
            finance_evidence["status"] = "insufficient_evidence"
        elif financing and financing.emi is not None and available_monthly_surplus is not None and financing.emi > float(available_monthly_surplus):
            finance_evidence["issues"].append("Proposed EMI exceeds current Available Monthly Surplus; repayment capacity is not established.")
            finance_evidence["status"] = "insufficient_evidence"

        comparison = compare_funding_paths(
            request.self_money, request.self_money_financing, self_evidence, finance_evidence
        )
        comparison["repayment_capacity_context"] = {
            "available_monthly_surplus": available_monthly_surplus,
            "existing_monthly_debt_payments": monthly_debt_payments,
            "proposed_monthly_emi": financing.emi if financing else None,
        }
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
        if request.investor_decision is not None and status != "ready_for_investor_review":
            raise HTTPException(status_code=409, detail="A funding path decision cannot be recorded until both paths have sufficient comparable evidence.")
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
