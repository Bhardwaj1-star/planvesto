from __future__ import annotations

from typing import Any, Literal

ConstraintKind = Literal["hard", "soft"]
ConstraintSource = Literal[
    "financial_state", "observed_behavior", "declared_constraint", "preference"
]

# Higher priority wins only when the evidence is otherwise comparable.
SOURCE_PRIORITY: dict[str, int] = {
    "financial_state": 4,
    "observed_behavior": 3,
    "declared_constraint": 2,
    "preference": 1,
}


class ConstraintRules:
    """Business rules for constraint normalization and conflict detection."""

    @staticmethod
    def normalize(item: dict[str, Any], source: ConstraintSource) -> dict[str, Any]:
        key = item["key"]
        kind: ConstraintKind = item.get("kind", "soft")
        return {
            "key": key,
            "value": item["value"],
            "unit": item.get("unit"),
            "kind": kind,
            "source": source,
            "evidence": item.get("evidence", []),
            "valid_from": item.get("valid_from"),
            "valid_until": item.get("valid_until"),
        }

    @staticmethod
    def conflicts(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
        groups: dict[str, list[dict[str, Any]]] = {}
        for item in items:
            groups.setdefault(item["key"], []).append(item)

        conflicts: list[dict[str, Any]] = []
        for key, group in groups.items():
            values = {repr(item["value"]) for item in group}
            if len(values) <= 1:
                continue
            conflicts.append({
                "key": key,
                "status": "unresolved",
                "reason": "Evidence sources provide conflicting values.",
                "sources": [item["source"] for item in group],
                "hard_constraint_present": any(item["kind"] == "hard" for item in group),
            })
        return conflicts

    @staticmethod
    def confidence(source: ConstraintSource, evidence_count: int) -> float:
        base = SOURCE_PRIORITY[source] / 4.0
        corroboration = 0.15 if evidence_count > 1 else 0.0
        return round(min(1.0, base + corroboration), 4)
