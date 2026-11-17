"""
domain/features/moneywheel/protection.py
Chapter 09 §4.1 Protection Coverage Assessment.

Guideline life cover evaluation:
Required Life Cover = (max(0, Gross Annual Income) * 10) + max(0, Total Liabilities)
Health insurance coverage verification.
"""

from decimal import Decimal
from typing import List, Optional, Tuple

from app.domain.canonical.financial_categories import CanonicalInsurancePolicyTypeId
from app.domain.shared.value_objects import Money, Rate
from app.domain.features.financial_state.models import InsuranceRecord


def calculate_required_life_cover(
    gross_annual_income: Money,
    total_liabilities: Money,
) -> Money:
    """
    Chapter 09 §4.1:
    Required Life Cover = (Gross Annual Income × 10) + Total Liabilities.
    """
    income_component = max(Decimal(0), gross_annual_income.amount) * Decimal(10)
    liability_component = max(Decimal(0), total_liabilities.amount)
    return Money(amount=income_component + liability_component, currency=gross_annual_income.currency)


def evaluate_existing_life_insurance(
    insurances: List[InsuranceRecord],
) -> Money:
    """Sums sum assured of active life policies (term, whole life, ULIP)."""
    life_policy_types = {
        CanonicalInsurancePolicyTypeId.TERM_LIFE,
        CanonicalInsurancePolicyTypeId.WHOLE_LIFE_ENDOWMENT,
        CanonicalInsurancePolicyTypeId.ULIP,
    }
    life_sum = sum(
        (i.sum_insured.amount for i in insurances if i.policy_type in life_policy_types and i.policy_status == "active"),
        Decimal(0),
    )
    return Money(amount=life_sum)


def evaluate_life_coverage_ratio(
    existing_cover: Money,
    required_cover: Money,
) -> Optional[Rate]:
    """Calculates coverage ratio = (existing / required) * 100."""
    if required_cover.amount <= Decimal(0):
        return None
    ratio_pct = (existing_cover.amount / required_cover.amount) * Decimal(100)
    return Rate.from_percentage(ratio_pct)


def evaluate_health_insurance(
    insurances: List[InsuranceRecord],
) -> Tuple[bool, Money]:
    """Returns (has_active_health, total_sum_insured) across active health/critical illness policies."""
    health_policies = [
        i for i in insurances
        if i.policy_type in (CanonicalInsurancePolicyTypeId.HEALTH, CanonicalInsurancePolicyTypeId.CRITICAL_ILLNESS_ACCIDENT_DISABILITY)
        and i.policy_status == "active"
    ]
    has_active = len(health_policies) > 0
    total_cover = Money(amount=sum((i.sum_insured.amount for i in health_policies), Decimal(0)))
    return has_active, total_cover
