# Reporting & Explanation Architecture

**Status:** IMPLEMENTATION FOUNDATION  
**Scope:** Aggregation and explanation of planning outputs for investor-facing reports.

## Purpose

Reporting consumes canonical engine outputs and presents financial state, goals, observations, actions, investment allocation and risk context. It should not independently recalculate core financial facts.

## Current Architecture

`backend/engines/summary_report/engine.py` aggregates:
- MoneyWheel / financial snapshot
- Risk Profile
- Goals
- Investment output
- Observations
- Action items

## Current Flow

**Canonical Engines → Summary Report Aggregation → Investor Report**

## Explanation Boundary

The report layer should explain:
- what the system observed;
- why an issue matters;
- what action follows;
- which engine/source produced the observation;
- relevant strategy/goal consequences.

It should not become a second calculation engine.

## Provenance

Reports carry planning-unit context and generated metadata. Strategy recommendation records additionally retain reasoning, architecture and constraints.

## Current Implementation Status

The SummaryReport engine contains lightweight rule-based observation/action generation and placeholder-style integration comments. Therefore this layer should currently be treated as an implementation foundation, not as the final canonical reporting specification.

## Related Code

- `backend/engines/summary_report/engine.py`
- `backend/models/summary_report.py`
- `backend/services/goal_report_service.py`
- `frontend/app/investor/reports/page.tsx`

## Canonical Boundary

**Calculation engines own facts. Strategy owns decisions. Reporting owns aggregation and explanation.**
