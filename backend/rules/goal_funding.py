from typing import Any
from models.goal_funding import FundingPathAssessment, FundingPath


# Chapter 11 requires daily dated cash-flow projection. Chapter 05 currently
# has no approved daily projection/day-count method for this workflow.
DAILY_GOAL_FUNDING_METHOD_APPROVED = False


def assess_path_evidence(path: FundingPathAssessment, mapped_asset_ids: set[str]) -> dict[str, Any]:
    issues: list[str] = []
    if path.path == FundingPath.SELF_MONEY_FINANCING:
        if path.financing is None:
            issues.append("Financing terms and evidence are missing.")
        else:
            issues.extend(
                f"Financing evidence is missing: {name}."
                for name in path.financing.missing_terms()
            )
            for index, row in enumerate(path.financing.repayment_schedule, start=1):
                if not row.get("payment_date") or row.get("amount") is None:
                    issues.append(f"Financing repayment schedule row {index} requires an actual payment date and amount.")

    supplied_asset_ids = {decision.asset_id for decision in path.asset_decisions}
    for missing_asset_id in sorted(mapped_asset_ids - supplied_asset_ids):
        issues.append(f"Mapped asset {missing_asset_id} has not been assessed in this funding path.")

    for decision in path.asset_decisions:
        if decision.asset_id not in mapped_asset_ids and not path.unmapped_asset_assessment_permitted:
            issues.append(f"Asset {decision.asset_id} is not mapped to this goal and has not been permitted for assessment.")
        if not decision.investor_approved:
            issues.append(f"Asset decision for {decision.asset_id} is not investor-approved and cannot be counted.")
        if decision.assessed_amount is None:
            issues.append(f"Assessed value is missing for asset {decision.asset_id}.")
        if decision.available_on is None:
            issues.append(f"Availability date is missing for asset {decision.asset_id}.")
        if not decision.liquidity_notes:
            issues.append(f"Liquidity assessment is missing for asset {decision.asset_id}.")
        if not decision.risk_suitability_assessment:
            issues.append(f"Risk suitability assessment is missing for asset {decision.asset_id}.")
        if not decision.competing_goal_notes:
            issues.append(f"Competing-goal commitment assessment is missing for asset {decision.asset_id}.")

    if not path.goal_linked_sips_assessed:
        issues.append("Existing goal-linked SIPs have not been assessed; confirm the list or explicitly confirm none.")
    for sip in path.goal_linked_sips:
        if not sip.confirmed_for_goal:
            issues.append(f"Goal-linked SIP {sip.sip_id} is not confirmed for this goal.")
        if not sip.source_reference:
            issues.append(f"Source evidence is missing for goal-linked SIP {sip.sip_id}.")

    if path.step_3_requirement_changed:
        issues.append("Approved asset decisions changed the self-money requirement; return to Chapter 10 to recalculate Funding Gap and Required SIP/Lump Sum before projection.")
    if path.path == FundingPath.SELF_MONEY and any(event.event_type.value in {"financing", "repayment"} for event in path.projection_events):
        issues.append("Self Money path cannot include financing drawdowns or repayments.")
    if not path.yearly_positions:
        issues.append("Year-by-year funding projection evidence is missing.")
    else:
        years = sorted(position.year for position in path.yearly_positions)
        if len(years) != len(set(years)):
            issues.append("Year-by-year projection contains duplicate calendar years.")
        for position in path.yearly_positions:
            required_values = ("opening_balance", "contributions", "investment_growth", "financing_drawdowns", "repayments", "goal_payments", "closing_balance", "shortfall", "surplus")
            if any(getattr(position, key) is None for key in required_values):
                issues.append(f"Year {position.year} is missing one or more explicit funding-position values; use zero only when evidenced as zero.")
            if not position.evidence_references:
                issues.append(f"Year {position.year} has no supporting evidence references.")
    if not path.projection_events:
        issues.append("Dated contribution, growth, financing/repayment and goal-payment events are missing.")
    for event in path.projection_events:
        if not event.source_reference:
            issues.append(f"Source evidence is missing for projection event on {event.event_date} ({event.event_type.value}).")
    if path.path == FundingPath.SELF_MONEY_FINANCING and path.financing and (path.financing.amount or 0) > 0:
        event_types = {event.event_type.value for event in path.projection_events}
        if "financing" not in event_types or "repayment" not in event_types:
            issues.append("Financing path requires dated financing drawdown and repayment events.")
    if not path.calculation_evidence.get("source_snapshot_id"):
        issues.append("Projection source snapshot is missing.")
    if not path.calculation_evidence.get("calculation_version"):
        issues.append("Projection calculation version is missing.")
    if not DAILY_GOAL_FUNDING_METHOD_APPROVED:
        issues.append("Daily dated cash-flow calculation method/day-count convention is not yet approved in Chapter 05; projection cannot be marked authoritative.")
    if path.investment_plan is None:
        issues.append("Investment planning evidence is missing.")
    elif not path.investment_plan.proposed_allocation or not path.investment_plan.assumptions or not path.investment_plan.risks or not path.investment_plan.costs or not path.investment_plan.trade_offs:
        issues.append("Investment allocation, assumptions, risks, costs and trade-offs must be explicitly assessed; use an explicit none/zero statement where applicable.")
    if not path.goal_payments:
        issues.append("Goal payment and withdrawal matching evidence is missing.")
    for payment in path.goal_payments:
        if payment.net_proceeds is None or payment.costs_and_taxes is None or payment.remaining_asset_value is None or not payment.expected_source or not payment.liquidity_notes or not payment.cross_goal_impact:
            issues.append(f"Payment source, net proceeds, costs/taxes, remaining asset value, liquidity and cross-goal impact are incomplete for payment on {payment.payment_date}.")
    if not path.monitoring_notes:
        issues.append("Monitoring evidence is missing.")
    if not path.contingency_options:
        issues.append("Contingency assessment is missing.")
    for option in path.contingency_options:
        if not option.revised_scenario:
            issues.append(f"Revised scenario evidence is missing for contingency trigger: {option.trigger}.")

    fallback_order = {
        "contribution": 0, "investment_growth": 1, "financing": 2,
        "repayment": 2, "goal_payment": 3,
    }
    ordered_events = sorted(
        path.projection_events,
        key=lambda event: (
            event.event_date,
            (0, event.event_timestamp) if event.event_timestamp is not None
            else (1, fallback_order[event.event_type.value]),
        ),
    )
    return {
        "status": "insufficient_evidence" if issues else "evidence_supplied",
        "issues": issues,
        "projection_event_order": [event.model_dump(mode="json") for event in ordered_events],
        "executable": False,
        "automatic_transactions_permitted": False,
    }


def _path_summary(path: FundingPathAssessment, evidence: dict[str, Any]) -> dict[str, Any]:
    contributions = sum(
        event.amount for event in path.projection_events
        if event.event_type.value == "contribution"
    )
    financing_amount = path.financing.amount if path.financing else 0.0
    repayment_total = sum(
        float(row.get("amount", 0) or 0)
        for row in (path.financing.repayment_schedule if path.financing else [])
    )
    financing_fees = (
        (path.financing.processing_fees or 0) + (path.financing.other_costs or 0)
        if path.financing else 0.0
    )
    last_year = max(path.yearly_positions, key=lambda row: row.year) if path.yearly_positions else None
    return {
        "evidence": evidence,
        "self_money_requirement": path.self_money_requirement,
        "own_money_contributions": round(contributions, 2),
        "approved_asset_amounts": round(sum(
            decision.assessed_amount or 0 for decision in path.asset_decisions
            if decision.disposition.value == "keep" and decision.investor_approved
        ), 2),
        "financing_amount": financing_amount,
        "financing_repayment_total": round(repayment_total, 2),
        "financing_fees_and_costs": round(financing_fees, 2),
        "financing_total_cost": round(max(0.0, repayment_total - financing_amount) + financing_fees, 2) if path.financing else 0.0,
        "emi": path.financing.emi if path.financing else None,
        "remaining_corpus": last_year.closing_balance if last_year else None,
        "yearly_shortfalls": [
            {"year": row.year, "shortfall": row.shortfall}
            for row in path.yearly_positions if row.shortfall and row.shortfall > 0
        ],
        "goal_payments": [item.model_dump(mode="json") for item in path.goal_payments],
        "liquidity_constraints": [item.liquidity_notes for item in path.asset_decisions if item.liquidity_notes],
        "risks": list(path.investment_plan.risks) if path.investment_plan else [],
        "trade_offs": list(path.investment_plan.trade_offs) if path.investment_plan else [],
        "other_goal_effects": [item.cross_goal_impact for item in path.goal_payments if item.cross_goal_impact],
    }


def compare_funding_paths(
    self_money_path: FundingPathAssessment,
    financed_path: FundingPathAssessment,
    self_money_evidence: dict[str, Any],
    financed_evidence: dict[str, Any],
) -> dict[str, Any]:
    return {
        "status": "comparable" if self_money_evidence["status"] == financed_evidence["status"] == "evidence_supplied" else "insufficient_evidence",
        "dimensions": [
            "own_money_used", "coverage_of_goal_funding_dates", "financing_amount_and_cost",
            "repayment_obligations", "remaining_corpus", "future_compounding",
            "liquidity", "risk", "constraints", "other_goal_impact",
        ],
        "self_money": _path_summary(self_money_path, self_money_evidence),
        "self_money_financing": _path_summary(financed_path, financed_evidence),
        "recommendation": None,
        "investor_decision_required": True,
        "automatic_path_selection": False,
    }
