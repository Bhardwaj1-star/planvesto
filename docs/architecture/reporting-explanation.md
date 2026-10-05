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

## Canonical Report Types

The current reporting layer exposes three distinct investor-facing report types. These are presentation/reporting views over canonical planning outputs; they are not separate calculation engines.

| Report | Scope | Primary Source / Service | Purpose |
|---|---|---|---|
| **Goal Report** | Single goal + its selected strategy decision | `backend/services/goal_report_service.py` | Explain one goal's funding position, financial context, selected strategy/scenario, alternatives, what-if scenarios, trade-offs, product architecture, contribution rules, action timeline and contingency context. |
| **Goal Basket Report** | Multiple goals grouped into one Goal Basket | `backend/services/basket_report_service.py` | Present the basket-level view across grouped goals, including combined goal/funding context and planning implications. |
| **Summary Financial Planning Report** | Planning-unit / investor-level | `backend/services/summary_report_service.py` + `backend/engines/summary_report/engine.py` | Aggregate the overall financial snapshot, MoneyWheel/financial health context, risk profile, goals, investment output, observations and action items into one investor-facing summary. |

### Report Relationships

**Defined Goal → Goal Report**  
Explains the complete decision context for one goal.

**Multiple Defined Goals → Goal Basket → Goal Basket Report**  
Presents the grouped multi-goal planning view. Goal Basket is the grouping/reporting boundary; it does not replace individual Goal or Strategy decisions.

**Planning Unit → Summary Financial Planning Report**  
Aggregates the broader investor-level financial and planning picture.

The Goal Basket and Multi-Goal Planning concepts should not be treated as two unrelated planning domains. The current code has a dedicated `GoalBasket` model/engine for grouping and a separate multi-goal orchestration layer for evaluating multiple goals against shared resources. Reporting surfaces the resulting basket-level view without duplicating those calculations.

## Report API / Rendering Paths

- **Goal Report:** `backend/services/goal_report_service.py`
- **Goal Basket Report:** `backend/services/basket_report_service.py` and `backend/api/basket_report.py`
- **Summary Financial Planning Report:** `backend/services/summary_report_service.py`, `backend/engines/summary_report/engine.py`, and `backend/api/summary_report.py`
- **Investor reports UI:** `frontend/app/investor/reports/page.tsx`

## Reporting Boundary by Level

| Planning Level | Canonical Output | Report |
|---|---|---|
| Individual Goal | `DefinedGoal` + selected Strategy Version / scenario | Goal Report |
| Goal Basket / Multi-Goal | Grouped goals + multi-goal planning/orchestration output | Goal Basket Report |
| Investor / Planning Unit | Financial State + MoneyWheel + Risk + Goals + Actions | Summary Financial Planning Report |
