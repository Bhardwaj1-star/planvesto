from __future__ import annotations

from typing import Any


def to_strategy_context(profile: dict[str, Any]) -> dict[str, Any]:
    """Expose a read-only planning context to Strategy Engine without strategy logic."""
    return {
        "profile_run_id": profile.get("profile_run_id"),
        "profile_version": profile.get("version"),
        "engine_version": profile.get("engine_version"),
        "constraints": [
            {
                "key": item["key"],
                "value": item["value"],
                "unit": item.get("unit"),
                "kind": item["kind"],
                "confidence": item.get("confidence"),
                "priority_rank": item.get("priority_rank"),
                "source": item.get("source"),
            }
            for item in profile.get("constraints", [])
        ],
        "priorities": list(profile.get("priorities", [])),
        "conflicts": list(profile.get("conflicts", [])),
    }
