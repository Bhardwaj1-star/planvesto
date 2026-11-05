from __future__ import annotations

from typing import Any

DIMENSIONS = (
    "financial_role",
    "decision_authority",
    "experience_evidence",
    "responsibility_load",
    "investment_context",
    "information_dependency",
)


def build_identity_profile(*, evidence: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """Describe investor identity from supplied evidence; never infer unsupported labels."""
    evidence = evidence or []
    by_dimension = {d: [] for d in DIMENSIONS}
    for item in evidence:
        dimension = item.get("dimension")
        if dimension in by_dimension:
            by_dimension[dimension].append({
                "value": item.get("value"),
                "source": item.get("source", "unknown"),
                "evidence": item.get("evidence", []),
                "confidence": item.get("confidence", 0.0),
                "status": item.get("status", "declared"),
            })
    return {
        "dimensions": by_dimension,
        "evidence_sufficient": {d: bool(items) for d, items in by_dimension.items()},
        "unsupported_dimensions": [d for d, items in by_dimension.items() if not items],
    }
