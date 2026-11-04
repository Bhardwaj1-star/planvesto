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

    for decision in path.asset_decisions:
        if decision.asset_id not in mapped_asset_ids and not path.unmapped_asset_assessment_permitted:
            issues.append(f"Asset {decision.asset_id} is not mapped to this goal and has not been permitted for assessment.")
        if decision.disposition == "reallocate" and not decision.investor_approved:
            issues.append(f"Asset {decision.asset_id} reallocation is proposed but not investor-approved.")

    for sip in path.goal_linked_sips:
        if not sip.confirmed_for_goal:
            issues.append(f"Goal-linked SIP {sip.sip_id} is not confirmed for this goal.")

    if path.step_3_requirement_changed:
        issues.append("Approved asset decisions changed the self-money requirement; return to Chapter 10 to recalculate Funding Gap and Required SIP/Lump Sum before projection.")

    if not path.yearly_positions:
        issues.append("Year-by-year funding projection evidence is missing.")
    if not path.projection_events:
        issues.append("Dated contribution, growth, financing/repayment and goal-payment events are missing.")
    if any(event.event_timestamp is None for event in path.projection_events):
        issues.append("Some projection events lack timestamps; the documented fallback event ordering must be applied.")
    if not path.calculation_evidence.get("source_snapshot_id"):
        issues.append("Projection source snapshot is missing.")
    if not path.calculation_evidence.get("calculation_version"):
        issues.append("Projection calculation version is missing.")
    if not DAILY_GOAL_FUNDING_METHOD_APPROVED:
        issues.append("Daily dated cash-flow calculation method/day-count convention is not yet approved in Chapter 05; projection cannot be marked authoritative.")

    if path.investment_plan is None:
        issues.append("Investment planning evidence is missing.")
    if not path.goal_payments:
        issues.append("Goal payment and withdrawal matching evidence is missing.")
    if not path.monitoring_notes:
        issues.append("Monitoring evidence is missing.")
    if not path.contingency_options:
        issues.append("Contingency assessment is missing.")

    return {
        "status": "insufficient_evidence" if issues else "evidence_supplied",
        "issues": issues,
        "executable": False,
        "automatic_transactions_permitted": False,
    }


def compare_funding_paths(self_money: dict[str, Any], financed: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": "comparable" if self_money["status"] == financed["status"] == "evidence_supplied" else "insufficient_evidence",
        "dimensions": [
            "own_money_used", "goal_date_coverage", "financing_amount_and_cost",
            "repayment_obligations", "remaining_corpus", "future_compounding",
            "liquidity", "risk", "constraints", "other_goal_impact",
        ],
        "self_money": self_money,
        "self_money_financing": financed,
        "recommendation": None,
        "investor_decision_required": True,
    }
