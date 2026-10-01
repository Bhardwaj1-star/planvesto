"""Investment Engine domain contracts.

The Investment Engine implements an approved risk boundary. It does not
recalculate Risk Required, infer Risk Tolerance, or create a risk profile.

Allocation mapping remains intentionally policy-driven: no asset-allocation
percentages or product-selection rules are embedded until explicitly defined.
"""
from __future__ import annotations
from typing import Any, Literal
from pydantic import BaseModel, Field

InvestmentPlanningStatus = Literal["ready", "requires_review"]

class InvestmentEngineInput(BaseModel):
    risk_profile: dict[str, Any]
    financial_state: dict[str, Any] = Field(default_factory=dict)
    goals: list[dict[str, Any]] = Field(default_factory=list)
    current_portfolio: dict[str, Any] = Field(default_factory=dict)

class AllocationLayer(BaseModel):
    layer: Literal[
        "strategic_asset_allocation",
        "sub_asset_allocation",
        "product_category",
        "product_selection",
        "allocation_amount",
    ]
    status: Literal["pending", "available", "not_applicable"] = "pending"
    data: dict[str, Any] = Field(default_factory=dict)
    constraints: list[dict[str, Any]] = Field(default_factory=list)

class InvestmentPlan(BaseModel):
    status: InvestmentPlanningStatus = "requires_review"
    risk_boundary: dict[str, Any] = Field(default_factory=dict)
    target_allocation: dict[str, Any] = Field(default_factory=dict)
    current_allocation: dict[str, Any] = Field(default_factory=dict)
    allocation_gap: dict[str, Any] = Field(default_factory=dict)
    layers: list[AllocationLayer] = Field(default_factory=list)
    constraints: list[dict[str, Any]] = Field(default_factory=list)
    decision_log: list[str] = Field(default_factory=list)
