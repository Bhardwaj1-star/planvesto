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

The current implementation exposes three investor-facing report surfaces. They operate at different planning scopes and must not be treated as interchangeable.

| Report | Scope | Primary Source / Service | Purpose |
|---|---|---|---|
| **Goal Report** | Single goal + its selected strategy decision | `backend/services/goal_report_service.py` | Explain one goal's funding position, financial context, selected strategy/scenario, alternatives, what-if scenarios, trade-offs, product architecture, contribution rules, action timeline and contingency context. |
| **Goal Basket Report** | A client-defined grouping of existing goals | `backend/services/basket_report_service.py` | Produce a basket-level presentation across selected goals, including priority laddering, shared contribution architecture, consolidated cash-flow trajectory, basket product architecture, timeline and contingency matrix. |
| **Summary Financial Planning Report** | Planning-unit / investor-level | `backend/services/summary_report_service.py` + `backend/engines/summary_report/engine.py` | Aggregate the overall financial snapshot, MoneyWheel/financial health context, risk profile, goals, investment output, observations and action items into one investor-facing summary. |

## Goal Basket vs Multi-Goal Planning

These are **different code concepts in the current repository** and must remain distinct unless the implementation is deliberately refactored.

### Goal Basket

Goal Basket is a grouping/reporting construct.

Code:
- `backend/models/goal_basket.py`
- `backend/services/goal_basket_service.py`
- `backend/engines/basket/engine.py`
- `backend/api/goal_basket.py`
- `backend/services/basket_report_service.py`
- `backend/api/basket_report.py`

The current `GoalBasketEngine` validates that the selected goal IDs exist and summarizes them by goal count, IDs, priorities, names, total required monthly contribution and total funding gap.

The `BasketReportService` goes further at the presentation layer: it builds a combined basket report with priority laddering, shared contribution architecture, combined cash-flow trajectory, basket product architecture, action timeline and contingency information.

### Multi-Goal Planning

Multi-Goal Planning is a planning/orchestration engine, not merely a grouping.

Code:
- `backend/services/multi_goal_planning_service.py`
- `backend/engines/orchestration/engine.py`
- `backend/rules/multi_goal.py`
- `backend/schemas/multi_goal_planning.py`
- `backend/api/orchestration.py`

The current `MultiGoalPlanningService` loads every goal in the planning unit, requires a selected current Strategy Version for each goal, obtains each goal's report/strategy evidence, builds a shared Financial State context, applies the canonical ConstraintAggregator, and passes the goals to `MultiGoalOrchestrator`.

The `MultiGoalOrchestrator`:
1. evaluates each goal using its existing strategy evidence;
2. resolves priority/overrides;
3. sends goals to `ResourceAllocationEngine`;
4. allocates available monthly surplus across competing goals;
5. returns per-goal resolutions, funding status, allocated contribution, shortfall, trade-offs and an audit trail.

Therefore:

**Goal Basket = grouping + basket-level reporting.**

**Multi-Goal Planning = shared-resource planning + allocation/orchestration across goals.**

They may operate on the same set of goals, but the current code gives them different responsibilities.

## Report Relationships

**Defined Goal → Goal Report**  
Explains the complete decision context for one goal.

**Goal Basket → Goal Basket Report**  
Presents the grouped basket-level view.

**Multiple Goals → Multi-Goal Planning / Orchestration**  
Resolves shared-resource competition and contribution allocation across goals. Its canonical output is `MultiGoalPlanResult`, exposed through `backend/api/orchestration.py`; it is not the same object as `GoalBasketSummary`.

**Planning Unit → Summary Financial Planning Report**  
Aggregates the broader investor-level financial and planning picture.

## Report API / Rendering Paths

- **Goal Report:** `backend/services/goal_report_service.py`
- **Goal Basket:** `backend/services/goal_basket_service.py`, `backend/api/goal_basket.py`
- **Goal Basket Report:** `backend/services/basket_report_service.py`, `backend/api/basket_report.py`
- **Multi-Goal Planning:** `backend/services/multi_goal_planning_service.py`, `backend/engines/orchestration/engine.py`, `backend/api/orchestration.py`
- **Summary Financial Planning Report:** `backend/services/summary_report_service.py`, `backend/engines/summary_report/engine.py`, `backend/api/summary_report.py`
- **Investor reports UI:** `frontend/app/investor/reports/page.tsx`

## Reporting Boundary by Level

| Planning Level | Canonical Output | Report / Surface |
|---|---|---|
| Individual Goal | `DefinedGoal` + selected Strategy Version / scenario | Goal Report |
| Goal Basket | `GoalBasket` / `GoalBasketSummary` | Goal Basket Report |
| Multi-Goal Planning | `MultiGoalPlanResult` | Multi-Goal Planning / Orchestration output |
| Investor / Planning Unit | Financial State + MoneyWheel + Risk + Goals + Actions | Summary Financial Planning Report |
