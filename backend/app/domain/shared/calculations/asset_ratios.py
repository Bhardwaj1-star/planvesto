"""
Chapter 05 — Canonical Measurements & Formulas
Group C: Asset Ratios (§2 Group C, §3 Group C)

1. metric_liquid_asset_ratio: Liquid Asset Ratio
   Formula: (Liquid Assets ÷ Total Assets) × 100
   Requires: Total Assets > 0.

2. metric_financial_asset_ratio: Financial Asset Ratio
   Formula: (Financial Assets ÷ Total Assets) × 100
   Requires: Total Assets > 0.

3. metric_portfolio_concentration: Portfolio Concentration
   Formula: (Largest Single Asset Value ÷ Total Asset Value) × 100
   Requires: Total Assets > 0.
"""

from decimal import Decimal
from typing import Optional
from app.domain.shared.value_objects import Money, Rate


def calculate_liquid_asset_ratio(liquid_assets: Money, total_assets: Money) -> Optional[Rate]:
    """Calculate Liquid Asset Ratio (%): (Liquid Assets ÷ Total Assets) × 100"""
    if total_assets.amount <= Decimal(0):
        return None
    ratio = (liquid_assets.amount / total_assets.amount) * Decimal(100)
    return Rate.from_percentage(ratio)


def calculate_financial_asset_ratio(financial_assets: Money, total_assets: Money) -> Optional[Rate]:
    """Calculate Financial Asset Ratio (%): (Financial Assets ÷ Total Assets) × 100"""
    if total_assets.amount <= Decimal(0):
        return None
    ratio = (financial_assets.amount / total_assets.amount) * Decimal(100)
    return Rate.from_percentage(ratio)


def calculate_portfolio_concentration(largest_single_asset: Money, total_assets: Money) -> Optional[Rate]:
    """Calculate Portfolio Concentration (%): (Largest Single Asset ÷ Total Assets) × 100"""
    if total_assets.amount <= Decimal(0):
        return None
    ratio = (largest_single_asset.amount / total_assets.amount) * Decimal(100)
    return Rate.from_percentage(ratio)
