"""Declarative Section Configurations for Reports.

Centralizes report section definitions, headers, layout schemas, and formatting rules.
"""
from __future__ import annotations

from typing import Any, Dict, List


GOAL_REPORT_SECTIONS = [
    {"id": "exec_summary", "title": "1. Executive Summary & Problem Setup"},
    {"id": "financial_position", "title": "2. Financial Position & Capacity Snapshot"},
    {"id": "feasibility", "title": "3. Goal Feasibility & Surplus Capacity Analysis"},
    {"id": "funding_solutions", "title": "4. Goal Funding Solutions Comparison"},
    {"id": "product_architecture", "title": "5. Strategic Product & Bucket Architecture"},
    {"id": "cash_flow_trajectory", "title": "6. Multi-Year Cash Flow Trajectory Projection"},
    {"id": "what_if_matrix", "title": "7. Deterministic What-If Decision Matrix"},
    {"id": "contribution_rules", "title": "8. Actionable Contribution & Portfolio Rules"},
    {"id": "action_plan_timeline", "title": "9. Implementation Action Plan Timeline"},
    {"id": "contingency_matrix", "title": "10. Contingency & Risk Management Matrix"},
    {"id": "alternatives", "title": "11. Evaluated Strategy Alternatives"},
    {"id": "technique_execution", "title": "12. Technique Execution Evidence"},
    {"id": "client_decision", "title": "13. Client Decision View & Implementation Checklist"},
    {"id": "provenance", "title": "14. Data Provenance & Traceability"},
]

BASKET_REPORT_SECTIONS = [
    {"id": "basket_overview", "title": "1. Goal Basket Overview & Prioritization Ladder"},
    {"id": "financial_position", "title": "2. Consolidated Financial Position & Capacity"},
    {"id": "shared_pool", "title": "3. Shared Resource Pool Allocation Architecture"},
    {"id": "consolidated_cash_flow", "title": "4. Consolidated Multi-Year Cash Flow Trajectory"},
    {"id": "bucket_architecture", "title": "5. Strategic Product & Bucket Architecture"},
    {"id": "action_plan_timeline", "title": "6. Integrated Implementation Timeline"},
    {"id": "contingency_matrix", "title": "7. Cross-Goal Contingency & Risk Matrix"},
]

FINANCIAL_PLAN_SECTIONS = [
    {"id": "financial_position", "title": "1. Consolidated Family Financial Position & Net Worth"},
    {"id": "moneywheel_scan", "title": "2. MoneyWheel Diagnostic Health & Vulnerability Scan"},
    {"id": "consolidated_funding", "title": "3. Consolidated Funding Capacity & Resource Waterfall"},
    {"id": "goal_ladder", "title": "4. Multi-Goal Strategic Priority Ladder & Allocations"},
    {"id": "family_cash_flow", "title": "5. Family Multi-Year Cash Flow Trajectory"},
    {"id": "ratio_constraints", "title": "6. Key Financial Health & Ratio Constraints"},
    {"id": "contingency_matrix", "title": "7. Family Contingency & Shock-Absorber Matrix"},
    {"id": "governance_protocol", "title": "8. Ongoing Governance & Rebalancing Protocol"},
]

SUMMARY_REPORT_SECTIONS = [
    {"id": "financial_snapshot", "title": "1. Financial Snapshot & Key Metrics"},
    {"id": "goals_summary", "title": "2. Goal Portfolio & Funding Status"},
    {"id": "observations", "title": "3. Cross-Engine Diagnostic Observations"},
    {"id": "action_items", "title": "4. Prioritized Action Recommendations"},
    {"id": "investment_profile", "title": "5. Risk Profile & Investment Allocation"},
]
