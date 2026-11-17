"""
api/schemas/financial_state.py
Transport schemas for Financial State endpoints.
"""

from decimal import Decimal
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class FinancialStateRequest(BaseModel):
    planning_unit_id: str
    scope: str = "family"  # family or individual
    investor_id: Optional[str] = None
    target_year: Optional[int] = None
    target_month: Optional[int] = None


class FinancialStateResponse(BaseModel):
    planning_unit_id: str
    scope: str
    investor_id: Optional[str] = None
    as_of_date: str
    net_worth: Decimal
    total_assets: Decimal
    total_liabilities: Decimal
    net_monthly_income: Decimal
    monthly_expenses: Decimal
    available_monthly_surplus: Decimal
    data_readiness: Dict[str, Any]
