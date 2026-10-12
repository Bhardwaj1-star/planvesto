# Reports Center — Report Surfaces and Endpoint Contracts

**Baseline:** `d7640029310c8e58d4cdd9a033d7683b5ea10002`.

## UI options

`frontend/app/investor/reports/page.tsx` presents Complete Financial Plan, Goal Basket Decision Report, Individual Goal Report and Summary Planning Report. It loads goals from Goal Planner data, reads saved baskets from localStorage and checks selected Strategy Versions. UI availability depends on goals, basket selection and strategy-version presence.

A localStorage basket is a client-side selection, not proof of a persisted basket-level strategy run. The UI's “at least two goals” basket requirement is a front-end condition; backend validation must be checked separately.

## Backend report families and APIs

- **Summary JSON/PDF:** `backend/api/summary_report.py`, prefix `/api/summary-report`.
  - `GET /api/summary-report?planning_unit_id={id}`: Generates JSON summary.
  - `GET /api/summary-report/pdf?planning_unit_id={id}`: Downloads PDF summary.
- **Basket Report / PDF (`backend/api/basket_report.py`):**
  - `POST /api/basket-report`: Generates multi-goal consolidated JSON report.
  - `POST /api/basket-report/pdf`: Generates multi-goal consolidated PDF report (`Content-Disposition: attachment; filename=goal-basket-report.pdf`).
  - *Request Payload:* `planning_unit_id: str`, `basket_name: str`, `goal_ids: list[str]`.
  - *Service Implementation:* `backend/services/basket_report_service.py::BasketReportService`.
    - Enforces: 2 to 3 goals recommended for visual density; minimum 1 goal required. Each goal must have an approved, selected `StrategyVersion`.
    - Generates 7 consolidated sections:
      1. *Executive Summary:* Basket name, total future target, total required monthly contribution, overall funding gap.
      2. *Priority Laddering:* Ordered by `rules.multi_goal.get_priority_rank()` and target date.
      3. *Shared Pool Contribution Architecture:* Distribution across SIP, Lumpsum, and Step-up.
      4. *Consolidated Cash Flow Trajectory:* Multi-year year-by-year projected accumulation trajectory table.
      5. *3-Bucket Product Architecture:* Liquidity, Core Compounder, and Satellite Growth.
      6. *Implementation Roadmap & Timeline:* Staged milestones across goals.
      7. *Contingency & Stress Defense Matrix:* Risk event mitigation table.
- **Individual Goal Report:** `backend/services/goal_report_service.py::GoalReportService.build_report()`. Consumes single goal + selected `StrategyVersion`.
- **Retirement Report Adapter:** `backend/services/strategy_service.py::get_retirement_report()`. Adapts retirement decision output with 3-bucket architecture and year-by-year wealth trajectory table.
- **PDF Generation Technology:** Generated locally using ReportLab (`SimpleDocTemplate`, `Table`, `Paragraph`, `TableStyle`) via `backend/report_engine/renderer.py::CommonPdfRenderer`. No external internet or browser dependencies.

## Preconditions and Validation Rules

1. Each included goal must have a finalized `DefinedGoal` snapshot.
2. Each goal must have a selected `StrategyVersion` persisted in `StrategyRepository`.
3. If any goal lacks a selected strategy version, `BasketReportService` raises HTTP 400: `"Goal '{name}' requires an approved Strategy Version before generating a basket report."`
4. Planning unit ownership is strictly validated against authenticated token via `verify_planning_unit_ownership()`.
