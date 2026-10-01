from __future__ import annotations

from typing import Any, Literal

BehaviorDimension = Literal[
    "decision_consistency",
    "volatility_reaction",
    "discipline",
    "intervention_tendency",
    "loss_uncertainty_response",
]

DIMENSIONS: tuple[BehaviorDimension, ...] = (
    "decision_consistency",
    "volatility_reaction",
    "discipline",
    "intervention_tendency",
    "loss_uncertainty_response",
)

PRODUCT_SELECTION_ONLY = "product_selection"


class BehavioralRules:
    """Convert observed historical behavior into implementation constraints.

    No hypothetical answers are scored. Missing observations remain unknown.
    """

    @staticmethod
    def normalize(observation: dict[str, Any]) -> dict[str, Any]:
        dimension = observation.get("dimension")
        if dimension not in DIMENSIONS:
            raise ValueError("Unsupported behavioral dimension")

        evidence = observation.get("evidence") or []
        if not evidence:
            raise ValueError("Behavioral observations require evidence")

        valid_from = observation.get("valid_from")
        valid_until = observation.get("valid_until")
        validity = observation.get("validity")
        if not isinstance(validity, dict):
            validity = {"valid_from": valid_from, "valid_until": valid_until, "status": "valid"}
        else:
            valid_from = valid_from or validity.get("valid_from")
            valid_until = valid_until or validity.get("valid_until")

        confidence = observation.get("confidence")
        if confidence is None:
            from engines.profile.constraints import ConstraintRules
            confidence = ConstraintRules.confidence("observed_behavior", len(evidence))

        return {
            "key": observation["key"],
            "value": observation["value"],
            "unit": observation.get("unit"),
            "kind": observation.get("kind", "soft"),
            "source": "observed_behavior",
            "dimension": dimension,
            "evidence": evidence,
            "confidence": confidence,
            "validity": validity,
            "valid_from": valid_from,
            "valid_until": valid_until,
            "downstream_use": PRODUCT_SELECTION_ONLY,
        }

    @staticmethod
    def resolve(observations: list[dict[str, Any]]) -> dict[str, Any]:
        normalized = [BehavioralRules.normalize(item) for item in observations]
        by_dimension: dict[str, list[dict[str, Any]]] = {d: [] for d in DIMENSIONS}
        for item in normalized:
            by_dimension[item["dimension"]].append(item)

        dimensions = {}
        for dimension, items in by_dimension.items():
            if not items:
                dimensions[dimension] = {
                    "status": "insufficient_evidence",
                    "constraints": [],
                }
                continue
            dimensions[dimension] = {
                "status": "observed",
                "constraints": items,
            }

        return {
            "dimensions": dimensions,
            "downstream_use": PRODUCT_SELECTION_ONLY,
        }
