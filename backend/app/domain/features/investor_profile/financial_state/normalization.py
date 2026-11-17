"""Chapter 04 frequency normalization for Financial State domain facts."""
from decimal import Decimal

from app.domain.shared.value_objects import Money, FlowFrequency
from app.domain.features.investor_profile.financial_state.models import IncomeRecord


def normalize_income_to_monthly(income: IncomeRecord) -> Money:
    """Return the monthly cash equivalent while excluding one-off income."""
    divisors = {
        FlowFrequency.ANNUAL: Decimal("12"),
        FlowFrequency.QUARTERLY: Decimal("3"),
        FlowFrequency.SEMI_ANNUAL: Decimal("6"),
    }
    if income.frequency == FlowFrequency.ONE_OFF:
        return Money.zero(currency=income.amount.currency)
    divisor = divisors.get(income.frequency)
    if divisor is None:
        return income.amount
    return Money(amount=income.amount.amount / divisor, currency=income.amount.currency)
