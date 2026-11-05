from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class Observation(BaseModel):
    """Cross‑engine insight that will be shown in the report.
    The fields are deliberately lightweight – the report layer only needs
    a short description, its relevance score and a reference to the source
    engine output.
    """
    description: str = Field(..., description="Human‑readable observation text")
    relevance: float = Field(..., ge=0.0, le=1.0, description="Score used for prioritisation")
    source: str = Field(..., description="Engine name that produced this observation")
    details: Optional[Dict[str, Any]] = Field(None, description="Any extra data useful for rendering")

class ActionItem(BaseModel):
    """Decision‑oriented action derived from the aggregated data."""
    description: str = Field(..., description="What the investor should consider/do")
    priority: float = Field(..., ge=0.0, le=1.0, description="Higher = more urgent/important")
    source: str = Field(..., description="Engine or rule that suggested the action")
    details: Optional[Dict[str, Any]] = Field(None)

class GoalSummary(BaseModel):
    """Compact representation of a single goal for the report."""
    id: str
    name: str
    target_amount: float
    currency: str = "INR"
    horizon_years: float
    current_funding: float
    funding_gap: float
    feasibility: str  # e.g. "on_track", "shortfall", "overfunded"
    required_contribution: Optional[float] = None

class SummaryReport(BaseModel):
    """Top‑level contract returned by the Summary Report service.
    All fields are optional because partial data is allowed – the report
    must still render when some engines lack information.
    """
    financial_snapshot: Dict[str, Any]
    goals: List[GoalSummary]
    observations: List[Observation]
    actions: List[ActionItem]
    investment_allocation: Optional[Dict[str, Any]] = None
    risk_profile: Optional[Dict[str, Any]] = None
    provenance: Optional[Dict[str, Any]] = None
