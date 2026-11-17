"""
Unit tests for domain/shared/value_objects.py
"""

from decimal import Decimal
import pytest
from app.domain.shared.value_objects import Money, Rate, Currency, CalendarMonth


def test_money_arithmetic_and_quantization():
    m1 = Money.from_amount("100.50")
    m2 = Money.from_amount("50.25")

    m3 = m1 + m2
    assert m3.amount == Decimal("150.75")
    assert m3.currency == Currency.INR

    m4 = m1 - m2
    assert m4.amount == Decimal("50.25")

    m_mult = m1 * 2
    assert m_mult.amount == Decimal("201.00")

    m_div = m1 / 2
    assert m_div.amount == Decimal("50.25")


def test_money_comparisons():
    m1 = Money.from_amount("100.00")
    m2 = Money.from_amount("200.00")

    assert m1 < m2
    assert m1 <= m2
    assert m2 > m1
    assert m2 >= m1
    assert m1 != m2
    assert m1 == Money.from_amount("100.00")


def test_money_currency_mismatch_raises():
    m_inr = Money.from_amount("100.00", Currency.INR)
    m_usd = Money.from_amount("100.00", Currency.USD)

    with pytest.raises(ValueError):
        _ = m_inr + m_usd


def test_rate_conversion_and_compounding():
    rate = Rate.from_percentage("12.0")
    assert rate.as_decimal_ratio == Decimal("0.12")

    # Monthly compounded rate for 12% effective annual return:
    # r_m = (1.12)^(1/12) - 1 ≈ 0.009488792934583046
    r_m = rate.to_monthly_compounded_rate()
    assert float(r_m) > 0.0094
    assert float(r_m) < 0.0095


def test_calendar_month():
    cm = CalendarMonth(year=2026, month=11)
    assert str(cm) == "2026-11"

    with pytest.raises(ValueError):
        CalendarMonth(year=2026, month=13)
