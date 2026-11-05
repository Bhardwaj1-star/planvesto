from __future__ import annotations


def round_money(value: float) -> float:
    return round(float(value), 2)


def monthly_amount(amount: float, frequency: str) -> float | None:
    """Convert supported frequencies (monthly, quarterly, half-yearly, yearly) to a monthly amount."""
    key = frequency.strip().lower()
    if key == "monthly":
        return round_money(amount)
    if key in {"quarterly", "quarter", "every quarter"}:
        return round_money(amount / 3)
    if key in {"half-yearly", "half yearly", "semi-annual", "semiannual", "semi-annually", "semi annually"}:
        return round_money(amount / 6)
    if key in {"annual", "annually", "yearly"}:
        return round_money(amount / 12)
    return None


def annual_amount(amount: float, frequency: str) -> float | None:
    """Convert supported frequencies (monthly, quarterly, half-yearly, yearly) to an annual amount."""
    key = frequency.strip().lower()
    if key == "monthly":
        return round_money(amount * 12)
    if key in {"quarterly", "quarter", "every quarter"}:
        return round_money(amount * 4)
    if key in {"half-yearly", "half yearly", "semi-annual", "semiannual", "semi-annually", "semi annually"}:
        return round_money(amount * 2)
    if key in {"annual", "annually", "yearly"}:
        return round_money(amount)
    return None


def percentage(part: float, total: float) -> float | None:
    if total == 0:
        return None
    return round_money(part / total * 100)
