# Reports Center — Backend Evidence Index

**Branch:** `main` · **Baseline:** `d7640029310c8e58d4cdd9a033d7683b5ea10002`  
**Status:** Source inspection only; no tests run or production database queried.

## Component documents

| Document | Scope |
|---|---|
| [01 — Report surfaces and endpoint contracts](01-REPORT-SURFACES-AND-ENDPOINTS.md) | Individual goal, basket, complete plan and summary report paths |
| [02 — Report assembly and canonical data sources](02-ASSEMBLY-AND-DATA-SOURCES.md) | Service composition and data authority |
| [03 — PDF rendering and UI behavior](03-PDF-RENDERING-AND-UI.md) | Renderer boundary, report selection and download flow |
| [04 — Tests and evidence gaps](04-TESTS-AND-EVIDENCE-GAPS.md) | Source freshness, output consistency and error handling |

## Runtime families

- Goal decision report: `GoalReportService` uses a strategy run and its defined-goal version.
- Goal basket report: `BasketReportService` aggregates supplied goal IDs.
- Complete financial plan: `FinancialPlanService` composes goal, strategy and multi-goal services.
- Summary report: `SummaryReportService` delegates to `SummaryReportEngine`, which aggregates canonical outputs including Financial State, Moneywheel and risk profile inputs.

## Primary source paths

`frontend/app/investor/reports/page.tsx`, `frontend/lib/api/strategy.ts`, `backend/api/summary_report.py`, `backend/api/basket_report.py`, goal-report/financial-plan API modules, `backend/services/goal_report_service.py`, `basket_report_service.py`, `financial_plan_service.py`, `summary_report_service.py`, `summary_report_renderer.py`, `backend/engines/summary_report/engine.py`, `backend/report_engine/renderer.py`.

Reports are output/presentation layers; they should not independently invent calculations or act as decision authority. Component-specific evidence and verification gaps are documented in the files above.