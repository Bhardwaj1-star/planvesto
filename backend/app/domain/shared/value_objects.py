"""
domain/shared/value_objects.py
Core financial and temporal value objects.

Non-negotiable invariants:
1. Exact monetary arithmetic using Decimal. Never use binary float for currency calculations.
2. Default currency is INR.
3. Provenance and Evidence status attached to values where required.
4. Value objects are immutable (frozen).
"""

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from enum import Enum
from typing import Optional


class Currency(str, Enum):
    INR = "INR"
    USD = "USD"


class EvidenceStatus(str, Enum):
    """Chapter 04 data readiness & provenance status."""
    ACTUAL_VERIFIED = "actual_verified"
    INVESTOR_REPORTED = "investor_reported"
    ESTIMATED = "estimated"
    UNVERIFIED = "unverified"
    PROVISIONAL = "provisional"


class FlowFrequency(str, Enum):
    MONTHLY = "monthly"
    ANNUAL = "annual"
    QUARTERLY = "quarterly"
    SEMI_ANNUAL = "semi_annual"
    ONE_OFF = "one_off"


@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: Currency = Currency.INR

    def __post_init__(self):
        if not isinstance(self.amount, Decimal):
            object.__setattr__(self, "amount", Decimal(str(self.amount)))
        # Quantize to 2 decimal places by default for standard INR representation
        quantized = self.amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        object.__setattr__(self, "amount", quantized)

    @classmethod
    def zero(cls, currency: Currency = Currency.INR) -> "Money":
        return cls(amount=Decimal("0.00"), currency=currency)

    @classmethod
    def from_amount(cls, value: int | float | str | Decimal, currency: Currency = Currency.INR) -> "Money":
        return cls(amount=Decimal(str(value)), currency=currency)

    def __add__(self, other: "Money") -> "Money":
        self._check_currency(other)
        return Money(amount=self.amount + other.amount, currency=self.currency)

    def __sub__(self, other: "Money") -> "Money":
        self._check_currency(other)
        return Money(amount=self.amount - other.amount, currency=self.currency)

    def __mul__(self, factor: Decimal | int | float) -> "Money":
        factor_dec = Decimal(str(factor))
        return Money(amount=self.amount * factor_dec, currency=self.currency)

    def __truediv__(self, divisor: Decimal | int | float) -> "Money":
        div_dec = Decimal(str(divisor))
        if div_dec == Decimal(0):
            raise ZeroDivisionError("Cannot divide Money by zero.")
        return Money(amount=self.amount / div_dec, currency=self.currency)

    def __lt__(self, other: "Money") -> bool:
        self._check_currency(other)
        return self.amount < other.amount

    def __le__(self, other: "Money") -> bool:
        self._check_currency(other)
        return self.amount <= other.amount

    def __gt__(self, other: "Money") -> bool:
        self._check_currency(other)
        return self.amount > other.amount

    def __ge__(self, other: "Money") -> bool:
        self._check_currency(other)
        return self.amount >= other.amount

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return False
        return self.currency == other.currency and self.amount == other.amount

    def _check_currency(self, other: "Money") -> None:
        if self.currency != other.currency:
            raise ValueError(f"Cannot operate between different currencies: {self.currency} and {other.currency}")

    @property
    def is_positive(self) -> bool:
        return self.amount > Decimal(0)

    @property
    def is_zero(self) -> bool:
        return self.amount == Decimal(0)

    @property
    def is_negative(self) -> bool:
        return self.amount < Decimal(0)


@dataclass(frozen=True)
class Rate:
    """Represents a percentage rate (e.g. 12% is entered as 12 or 12.0)."""
    percentage: Decimal

    def __post_init__(self):
        if not isinstance(self.percentage, Decimal):
            object.__setattr__(self, "percentage", Decimal(str(self.percentage)))

    @classmethod
    def from_percentage(cls, value: int | float | str | Decimal) -> "Rate":
        return cls(percentage=Decimal(str(value)))

    @classmethod
    def from_decimal_ratio(cls, ratio: int | float | str | Decimal) -> "Rate":
        """e.g. 0.12 ratio -> 12%"""
        return cls(percentage=Decimal(str(ratio)) * Decimal(100))

    @property
    def as_decimal_ratio(self) -> Decimal:
        """Returns 0.12 for 12%."""
        return self.percentage / Decimal(100)

    def to_monthly_compounded_rate(self) -> Decimal:
        """
        Chapter 05 canonical convention for converting annual effective rate r_a to monthly rate r_m:
        r_m = (1 + r_a)^(1/12) - 1
        """
        r_a = float(self.as_decimal_ratio)
        r_m = ((1.0 + r_a) ** (1.0 / 12.0)) - 1.0
        return Decimal(str(r_m))


@dataclass(frozen=True)
class CalendarMonth:
    """Represents a specific calendar month, e.g. 2026-11."""
    year: int
    month: int

    def __post_init__(self):
        if not (1 <= self.month <= 12):
            raise ValueError(f"Invalid month: {self.month}. Must be between 1 and 12.")
        if self.year < 1900 or self.year > 2200:
            raise ValueError(f"Invalid year: {self.year}.")

    def __str__(self) -> str:
        return f"{self.year:04d}-{self.month:02d}"
