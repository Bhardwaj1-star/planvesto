"""
domain/shared/constraints/evaluator.py
Canonical evaluation gates implementing Chapter 06 rules.
"""

from decimal import Decimal
from typing import Any, Dict, List, Optional
from app.domain.shared.value_objects import Money, Rate
from app.domain.shared.calculations.goal_funding import calculate_monthly_sip_surplus_gap
from app.domain.shared.constraints.catalog import ConstraintRuleId
from app.domain.shared.constraints.result import (
    ConstraintEffect,
    ConstraintEvaluationResult,
)


def evaluate_dti_gate(dti_rate: Optional[Rate]) -> ConstraintEvaluationResult:
    """
    CTR-DTI-001: Debt-to-Income planning assessment (§2.1).
    Rule: Informs cash-flow / surplus assessment. DTI alone must NEVER block a goal,
    investment, or strategy. No numeric pass/fail threshold is approved.
    """
    if dti_rate is None:
        return ConstraintEvaluationResult(
            rule_id=ConstraintRuleId.CTR_DTI_001.value,
            effect=ConstraintEffect.INSUFFICIENT_EVIDENCE,
            is_satisfied=True,  # Does not block
            explanation="Gross monthly income or debt payment evidence is missing or non-positive. DTI cannot be calculated.",
            details={"dti_percentage": None},
        )

    return ConstraintEvaluationResult(
        rule_id=ConstraintRuleId.CTR_DTI_001.value,
        effect=ConstraintEffect.INFORMATIONAL,
        is_satisfied=True,  # Informational only; never blocks
        explanation=f"Debt-to-Income ratio is {dti_rate.percentage:.2f}%. Informs Available Monthly Surplus context without blocking.",
        details={"dti_percentage": float(dti_rate.percentage)},
    )


def evaluate_asset_availability_gate(
    asset_id: str,
    asset_name: str,
    asset_value: Money,
    is_accessible: bool,
    access_restrictions: Optional[List[str]] = None,
    is_already_committed: bool = False,
    committed_goal_id: Optional[str] = None,
) -> ConstraintEvaluationResult:
    """
    CTR-LIQ-001: Goal/strategy asset-availability rule (§2.2).
    Rule: Exclude assets that are not verified as accessible, unencumbered, and uncommitted.
    Ownership or portfolio inclusion alone does not prove availability.
    """
    restrictions = access_restrictions or []

    if not is_accessible or restrictions:
        reasons = ", ".join(restrictions) if restrictions else "Asset marked as not practically accessible"
        return ConstraintEvaluationResult(
            rule_id=ConstraintRuleId.CTR_LIQ_001.value,
            effect=ConstraintEffect.SHORTFALL_UNDER_CURRENT_CONDITIONS,
            is_satisfied=False,
            explanation=f"Asset '{asset_name}' ({asset_id}) cannot be allocated: {reasons}.",
            details={"asset_id": asset_id, "restrictions": restrictions, "is_accessible": is_accessible},
        )

    if is_already_committed:
        return ConstraintEvaluationResult(
            rule_id=ConstraintRuleId.CTR_LIQ_001.value,
            effect=ConstraintEffect.SHORTFALL_UNDER_CURRENT_CONDITIONS,
            is_satisfied=False,
            explanation=f"Asset '{asset_name}' is already committed to goal '{committed_goal_id}'. No double counting permitted.",
            details={"asset_id": asset_id, "committed_goal_id": committed_goal_id},
        )

    return ConstraintEvaluationResult(
        rule_id=ConstraintRuleId.CTR_LIQ_001.value,
        effect=ConstraintEffect.SATISFIED,
        is_satisfied=True,
        explanation=f"Asset '{asset_name}' is unencumbered and available for allocation.",
        details={"asset_id": asset_id, "value": str(asset_value.amount)},
    )


def evaluate_high_interest_liability_gate(
    liability_id: str,
    liability_name: str,
    outstanding_balance: Money,
    annual_interest_rate: Rate,
    alternative_investment_return: Optional[Rate] = None,
) -> ConstraintEvaluationResult:
    """
    CTR-HIR-001: High-interest liability assessment (§2.3).
    Trigger: Interest rate strictly > 14.0% p.a. (14.0% exactly does NOT trigger).
    Effect: Mandatory trade-off assessment and disclosure. Does NOT automatically block investment.
    """
    is_high_interest = annual_interest_rate.percentage > Decimal("14.0")

    if not is_high_interest:
        return ConstraintEvaluationResult(
            rule_id=ConstraintRuleId.CTR_HIR_001.value,
            effect=ConstraintEffect.SATISFIED,
            is_satisfied=True,
            explanation=f"Liability '{liability_name}' interest rate ({annual_interest_rate.percentage:.2f}%) does not exceed the 14% high-interest trigger.",
            details={"liability_id": liability_id, "interest_rate": float(annual_interest_rate.percentage)},
        )

    details: Dict[str, Any] = {
        "liability_id": liability_id,
        "outstanding_balance": str(outstanding_balance.amount),
        "interest_rate": float(annual_interest_rate.percentage),
    }

    if alternative_investment_return is not None:
        expected_ret = alternative_investment_return.percentage
        spread = annual_interest_rate.percentage - expected_ret
        details["expected_investment_return"] = float(expected_ret)
        details["interest_drag_spread"] = float(spread)
        comparison_text = (
            f"Guaranteed loan interest saved by prepayment is {annual_interest_rate.percentage:.2f}%, "
            f"compared to estimated alternative investment return of {expected_ret:.2f}%."
        )
    else:
        comparison_text = f"Debt bears high contractual interest of {annual_interest_rate.percentage:.2f}%."

    return ConstraintEvaluationResult(
        rule_id=ConstraintRuleId.CTR_HIR_001.value,
        effect=ConstraintEffect.MANDATORY_DISCLOSURE,
        is_satisfied=True,  # Does not block; requires explicit investor review
        explanation=(
            f"High-interest debt detected on '{liability_name}' (>14% p.a.). {comparison_text} "
            "Investor must be presented with this debt-repayment vs investment comparison."
        ),
        details=details,
    )


def evaluate_sip_affordability_gate(
    additional_required_sip: Money,
    available_monthly_surplus: Money,
) -> ConstraintEvaluationResult:
    """
    CTR-AFF-001: Goal-funding affordability rule (§2.6).
    Rule: Compare additional Required SIP with Available Monthly Surplus for same period.
    Passes when additional Required SIP <= Available Monthly Surplus.
    If it exceeds, reports monthly shortfall gap. Does NOT mean goal is impossible.
    """
    if available_monthly_surplus.is_negative:
        gap = additional_required_sip + Money.from_amount(abs(available_monthly_surplus.amount))
        return ConstraintEvaluationResult(
            rule_id=ConstraintRuleId.CTR_AFF_001.value,
            effect=ConstraintEffect.SHORTFALL_UNDER_CURRENT_CONDITIONS,
            is_satisfied=False,
            gap_amount=gap,
            explanation=(
                f"Investor has an existing monthly deficit of {abs(available_monthly_surplus.amount)}. "
                f"Total monthly capacity shortfall for required SIP of {additional_required_sip.amount} is {gap.amount}."
            ),
            details={
                "required_sip": str(additional_required_sip.amount),
                "monthly_surplus": str(available_monthly_surplus.amount),
                "gap": str(gap.amount),
            },
        )

    if additional_required_sip <= available_monthly_surplus:
        margin = available_monthly_surplus - additional_required_sip
        return ConstraintEvaluationResult(
            rule_id=ConstraintRuleId.CTR_AFF_001.value,
            effect=ConstraintEffect.SATISFIED,
            is_satisfied=True,
            gap_amount=Money.zero(currency=additional_required_sip.currency),
            explanation=(
                f"Required monthly SIP of {additional_required_sip.amount} is fully affordable "
                f"within Available Monthly Surplus of {available_monthly_surplus.amount} (Uncommitted buffer: {margin.amount})."
            ),
            details={
                "required_sip": str(additional_required_sip.amount),
                "monthly_surplus": str(available_monthly_surplus.amount),
                "uncommitted_margin": str(margin.amount),
            },
        )

    gap = calculate_monthly_sip_surplus_gap(additional_required_sip, available_monthly_surplus)
    return ConstraintEvaluationResult(
        rule_id=ConstraintRuleId.CTR_AFF_001.value,
        effect=ConstraintEffect.SHORTFALL_UNDER_CURRENT_CONDITIONS,
        is_satisfied=False,
        gap_amount=gap,
        explanation=(
            f"Required SIP of {additional_required_sip.amount} exceeds Available Monthly Surplus of "
            f"{available_monthly_surplus.amount} by a monthly shortfall of {gap.amount} under current conditions."
        ),
        details={
            "required_sip": str(additional_required_sip.amount),
            "monthly_surplus": str(available_monthly_surplus.amount),
            "gap": str(gap.amount),
        },
    )
