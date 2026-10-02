"""Investment Planning Engine foundation.

Boundary:
    Risk Profiler -> approved risk boundary -> Investment Engine

Implementation hierarchy:
    Strategic Asset Allocation
        -> Sub-Asset Allocation
        -> Product Category
        -> Product Selection
        -> Allocation Amount

This foundation deliberately does not invent risk-score thresholds, target
asset-allocation percentages, or product-selection rules.
"""
from __future__ import annotations
from engines.investment.models import AllocationLayer, InvestmentEngineInput, InvestmentPlan

class InvestmentEngine:
    """Builds an investment-plan structure from an approved risk boundary."""

    LAYERS = (
        "strategic_asset_allocation",
        "sub_asset_allocation",
        "product_category",
        "product_selection",
        "allocation_amount",
    )

    def build(self, payload: InvestmentEngineInput) -> InvestmentPlan:
        profile = payload.risk_profile or {}
        constraints = list(profile.get("constraints") or [])
        required = profile.get("risk_required") or {}
        capacity = profile.get("risk_capacity") or {}
        tolerance = profile.get("risk_tolerance") or {}

        dimensions_available = all(
            bool(dimension.get("available"))
            for dimension in (required, capacity, tolerance)
        )

        decision_log: list[str] = []
        if not dimensions_available:
            decision_log.append(
                "Investment planning requires Risk Required, Risk Capacity, "
                "and Risk Tolerance to be available."
            )
        else:
            decision_log.append(
                "Risk boundary received from Risk Profiler; allocation policy "
                "mapping is pending explicit business rules."
            )

        layers = [AllocationLayer(layer=layer) for layer in self.LAYERS]

        return InvestmentPlan(
            status="ready" if dimensions_available else "requires_review",
            risk_boundary={
                "risk_required": required,
                "risk_capacity": capacity,
                "risk_tolerance": tolerance,
            },
            current_allocation=payload.current_portfolio.get("allocation", {}),
            constraints=constraints,
            layers=layers,
            decision_log=decision_log,
        )
