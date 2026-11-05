from __future__ import annotations


def round_money(value: float) -> float:
    return round(float(value), 2)


def percentage(part: float, total: float) -> float | None:
    if total == 0:
        return None
    return round_money(part / total * 100)
