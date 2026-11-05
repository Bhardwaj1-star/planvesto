import pytest

from services.shared.normalisation.amounts import (
    annual_amount,
    monthly_amount,
    normalise_frequency,
    normalise_recurring_amount,
)


@pytest.mark.parametrize(
    ("amount", "frequency", "monthly", "annual"),
    [
        (12000, "Monthly", 12000.0, 144000.0),
        (30000, "Quarterly", 10000.0, 120000.0),
        (60000, "Half-yearly", 10000.0, 120000.0),
        (120000, "Yearly", 10000.0, 120000.0),
    ],
)
def test_recurring_amount_normalises_to_monthly_and_annual(amount, frequency, monthly, annual):
    result = normalise_recurring_amount(amount, frequency)
    assert result is not None
    assert result.monthly_amount == monthly
    assert result.annual_amount == annual
    assert result.original_amount == float(amount)
    assert result.original_frequency == frequency


def test_insurance_premium_uses_same_shared_frequency_normalisation():
    assert monthly_amount(15000, "Quarterly") == 5000.0
    assert annual_amount(15000, "Quarterly") == 60000.0


def test_unknown_or_missing_frequency_is_not_guessed():
    assert normalise_frequency("Weekly") is None
    assert normalise_recurring_amount(10000, "Weekly") is None
    assert normalise_recurring_amount(10000, None) is None
    assert monthly_amount(10000, "") is None


def test_invalid_or_non_finite_amount_is_unavailable():
    assert normalise_recurring_amount(None, "Monthly") is None
    assert normalise_recurring_amount(float("nan"), "Monthly") is None
    assert normalise_recurring_amount(float("inf"), "Monthly") is None
    assert normalise_recurring_amount(True, "Monthly") is None
