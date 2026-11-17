"""
Unit tests for Chapter 03 Canonical Taxonomy & Identity.

Acceptance criteria verified:
- C03-R01: Exactly 10 canonical goal types and IDs.
- C03-R02: Stable identity (distinct IDs from labels).
- C03-R04: Canonical categories across Income, Expense, Asset, Liability, Insurance.
"""

from app.domain.canonical.goal_taxonomy import (
    CanonicalGoalId,
    CANONICAL_GOAL_DEFINITIONS,
    get_canonical_goal_definition,
    is_valid_canonical_goal_id,
)
from app.domain.canonical.financial_categories import (
    FinancialGroup,
    CanonicalIncomeCategoryId,
    CanonicalExpenseCategoryId,
    CanonicalAssetCategoryId,
    CanonicalLiabilityCategoryId,
    CanonicalInsurancePolicyTypeId,
    CATEGORY_DEFINITIONS,
    get_category_definition,
)
from app.domain.canonical.measurements import (
    CanonicalMeasurementId,
    MEASUREMENT_CATALOGUE,
    get_measurement_metadata,
)


def test_canonical_goals_count_and_ids():
    """Verify exactly 10 canonical goal types exist and are registered."""
    assert len(CanonicalGoalId) == 10
    assert len(CANONICAL_GOAL_DEFINITIONS) == 10

    expected_ids = {
        "goal_retirement",
        "goal_marriage",
        "goal_vehicle",
        "goal_dream_home",
        "goal_education",
        "goal_vacation",
        "goal_debt_freedom",
        "goal_wealth_creation",
        "goal_fire_passive_income",
        "goal_others",
    }
    actual_ids = {g.value for g in CanonicalGoalId}
    assert actual_ids == expected_ids


def test_goal_definition_lookup():
    defn = get_canonical_goal_definition("goal_retirement")
    assert defn is not None
    assert defn.display_name == "Retirement"
    assert "post-retirement expenses" in defn.contextual_guidance

    # Invalid goal ID
    assert get_canonical_goal_definition("goal_unknown") is None
    assert not is_valid_canonical_goal_id("goal_child_education")  # Child education is not a separate ID


def test_canonical_financial_categories():
    assert len(CanonicalIncomeCategoryId) == 8
    assert len(CanonicalExpenseCategoryId) == 13
    assert len(CanonicalAssetCategoryId) == 12
    assert len(CanonicalLiabilityCategoryId) == 7
    assert len(CanonicalInsurancePolicyTypeId) == 9

    # Verify lookups
    salary_def = get_category_definition("income_salary")
    assert salary_def is not None
    assert salary_def.group == FinancialGroup.INCOME
    assert salary_def.display_name == "Salary"

    term_life_def = get_category_definition("insurance_term_life")
    assert term_life_def is not None
    assert term_life_def.group == FinancialGroup.INSURANCE


def test_canonical_measurements_registered():
    assert len(MEASUREMENT_CATALOGUE) == 20

    net_worth_meta = get_measurement_metadata("metric_net_worth")
    assert net_worth_meta is not None
    assert net_worth_meta.canonical_name == "Net Worth"

    surplus_meta = get_measurement_metadata("metric_monthly_surplus")
    assert surplus_meta is not None
    assert surplus_meta.canonical_name == "Available Monthly Surplus"
