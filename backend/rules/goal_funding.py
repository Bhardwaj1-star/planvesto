from typing import Any
from models.goal_funding import FundingPathAssessment, FundingPath


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

    if not path.yearly_positions:
        issues.append("Year-by-year funding projection evidence is missing.")
    if not path.projection_events:
        issues.append("Dated contribution, growth, financing/repayment and goal-payment events are missing.")
    if path.investment_plan is None:
        issues.append("Investment planning evidence is missing.")
    if not path.goal_payments:
        issues.append("Goal payment and withdrawal matching evidence is missing.")

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
