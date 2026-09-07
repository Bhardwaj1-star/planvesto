from __future__ import annotations


def round_money(value: float) -> float:
    return round(float(value), 2)


def monthly_amount(amount: float, frequency: str) -> float | None:
    """Match the current frontend model: Monthly is monthly; otherwise Annual is expected."""
    key = frequency.strip().lower()
    if key == "monthly":
        return round_money(amount)
    if key in {"annual", "annually", "yearly"}:
        return round_money(amount / 12)
    return None


def annual_amount(amount: float, frequency: str) -> float | None:
    key = frequency.strip().lower()
    if key == "monthly":
        return round_money(amount * 12)
    if key in {"annual", "annually", "yearly"}:
        return round_money(amount)
    return None


def percentage(part: float, total: float) -> float | None:
    if total == 0:
        return None
    return round_money(part / total * 100)
