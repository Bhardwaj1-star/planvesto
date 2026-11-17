"""
Unit tests for Chapter 06 Constraints and Decision Gates.
"""

from decimal import Decimal
from app.domain.shared.value_objects import Money, Rate
from app.domain.shared.constraints import (
    ConstraintRuleId,
    ConstraintEffect,
    evaluate_dti_gate,
    evaluate_asset_availability_gate,
    evaluate_high_interest_liability_gate,
    evaluate_sip_affordability_gate,
)


def test_ctr_dti_001_informational_never_blocks():
    # High DTI (e.g. 60%) must remain informational and NOT block
    high_dti = Rate.from_percentage("60.0")
    res = evaluate_dti_gate(high_dti)
    assert res.rule_id == ConstraintRuleId.CTR_DTI_001
    assert res.effect == ConstraintEffect.INFORMATIONAL
    assert res.is_satisfied is True
    assert "Informs Available Monthly Surplus context without blocking" in res.explanation

    # Missing evidence
    missing_res = evaluate_dti_gate(None)
    assert missing_res.effect == ConstraintEffect.INSUFFICIENT_EVIDENCE
    assert missing_res.is_satisfied is True


def test_ctr_liq_001_asset_availability():
    val = Money.from_amount("500000.00")

    # Clean unencumbered asset
    clean_res = evaluate_asset_availability_gate("ast-1", "Mutual Fund", val, is_accessible=True)
    assert clean_res.is_satisfied is True
    assert clean_res.effect == ConstraintEffect.SATISFIED

    # Restricted asset (e.g. 3-year ELSS lock-in)
    locked_res = evaluate_asset_availability_gate(
        "ast-2", "ELSS Fund", val, is_accessible=False, access_restrictions=["ELSS 3-year statutory lock-in"]
    )
    assert locked_res.is_satisfied is False
    assert locked_res.effect == ConstraintEffect.SHORTFALL_UNDER_CURRENT_CONDITIONS
    assert "lock-in" in locked_res.explanation

    # Already committed asset
    committed_res = evaluate_asset_availability_gate(
        "ast-3", "FD", val, is_accessible=True, is_already_committed=True, committed_goal_id="goal-retire-1"
    )
    assert committed_res.is_satisfied is False
    assert "already committed" in committed_res.explanation


def test_ctr_hir_001_high_interest_liability_threshold():
    balance = Money.from_amount("200000.00")

    # Boundary test: exactly 14.00% does NOT trigger
    rate_14 = Rate.from_percentage("14.0")
    res_14 = evaluate_high_interest_liability_gate("l-1", "Personal Loan", balance, rate_14)
    assert res_14.effect == ConstraintEffect.SATISFIED
    assert "does not exceed the 14% high-interest trigger" in res_14.explanation

    # Strictly greater: 14.01% triggers mandatory trade-off disclosure
    rate_high = Rate.from_percentage("14.01")
    expected_inv_return = Rate.from_percentage("12.0")
    res_high = evaluate_high_interest_liability_gate("l-2", "Credit Card Debt", balance, rate_high, expected_inv_return)
    assert res_high.effect == ConstraintEffect.MANDATORY_DISCLOSURE
    assert res_high.is_satisfied is True  # Mandatory disclosure, does not block
    assert "High-interest debt detected" in res_high.explanation
    assert res_high.details["interest_drag_spread"] == 2.01


def test_ctr_aff_001_sip_affordability():
    # Fully affordable: Required SIP 15,000 <= Surplus 25,000
    res_pass = evaluate_sip_affordability_gate(Money.from_amount("15000.00"), Money.from_amount("25000.00"))
    assert res_pass.is_satisfied is True
    assert res_pass.effect == ConstraintEffect.SATISFIED
    assert res_pass.gap_amount.amount == Decimal("0.00")

    # Shortfall: Required SIP 30,000 > Surplus 20,000 -> Gap is 10,000
    res_fail = evaluate_sip_affordability_gate(Money.from_amount("30000.00"), Money.from_amount("20000.00"))
    assert res_fail.is_satisfied is False
    assert res_fail.effect == ConstraintEffect.SHORTFALL_UNDER_CURRENT_CONDITIONS
    assert res_fail.gap_amount.amount == Decimal("10000.00")

    # Deficit case: Investor currently has -5,000 deficit and needs 10,000 SIP -> Gap is 15,000
    res_deficit = evaluate_sip_affordability_gate(Money.from_amount("10000.00"), Money.from_amount("-5000.00"))
    assert res_deficit.is_satisfied is False
    assert res_deficit.gap_amount.amount == Decimal("15000.00")
