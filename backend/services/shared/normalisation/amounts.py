"""Frequency-aware normalisation for recurring monetary amounts.

Keep the source amount and frequency at the caller. This module only derives
comparable monthly and annual representations; it does not persist or overwrite
raw financial records.
"""

from __future__ import annotations

from dataclasses import dataclass
import math


_FREQUENCY_ALIASES = {
    "monthly": "monthly",
    "quarter": "quarterly",
    "quarterly": "quarterly",
    "every quarter": "quarterly",
    "half yearly": "half_yearly",
    "half-yearly": "half_yearly",
    "semi annual": "half_yearly",
    "semi-annual": "half_yearly",
    "semiannual": "half_yearly",
    "semi annually": "half_yearly",
    "semi-annually": "half_yearly",
    "annual": "annual",
    "annually": "annual",
    "yearly": "annual",
}
_PERIODS_PER_YEAR = {
    "monthly": 12,
    "quarterly": 4,
    "half_yearly": 2,
    "annual": 1,
}


@dataclass(frozen=True)
class NormalisedRecurringAmount:
    """Derived recurring values with the original input retained for traceability."""

    original_amount: float
    original_frequency: str | None
    canonical_frequency: str
    monthly_amount: float
    annual_amount: float


def normalise_frequency(frequency: str | None) -> str | None:
    """Return a canonical supported frequency, or None for missing/unknown input."""
    if not isinstance(frequency, str):
        return None
    key = " ".join(frequency.strip().lower().replace("_", " ").split())
    return _FREQUENCY_ALIASES.get(key)


def normalise_recurring_amount(
    amount: float | int | None,
    frequency: str | None,
) -> NormalisedRecurringAmount | None:
    """Derive monthly and annual values without guessing unsupported frequencies.

    Unsupported frequencies (including one-time/irregular payments) return None.
    The caller remains responsible for preserving the raw amount, frequency,
    currency, source and period alongside these derived values.
    """
    canonical_frequency = normalise_frequency(frequency)
    if amount is None or canonical_frequency is None or isinstance(amount, bool):
        return None
    try:
        original_amount = float(amount)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(original_amount):
        return None

    annual = round(original_amount * _PERIODS_PER_YEAR[canonical_frequency], 2)
    monthly = round(annual / 12, 2)
    return NormalisedRecurringAmount(
        original_amount=original_amount,
        original_frequency=frequency,
        canonical_frequency=canonical_frequency,
        monthly_amount=monthly,
        annual_amount=annual,
    )


def monthly_amount(amount: float | int | None, frequency: str | None) -> float | None:
    """Return a monthly equivalent through the shared normalisation contract."""
    result = normalise_recurring_amount(amount, frequency)
    return result.monthly_amount if result is not None else None


def annual_amount(amount: float | int | None, frequency: str | None) -> float | None:
    """Return an annual equivalent through the shared normalisation contract."""
    result = normalise_recurring_amount(amount, frequency)
    return result.annual_amount if result is not None else None
