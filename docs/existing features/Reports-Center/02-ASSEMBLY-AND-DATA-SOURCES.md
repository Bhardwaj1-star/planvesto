# Reports Center — Assembly and Canonical Data Sources

**Baseline:** `d7640029310c8e58d4cdd9a033d7683b5ea10002`.

## Individual Goal Report

`GoalReportService` loads a strategy run by ID, resolves the exact DefinedGoal version linked to that run and rejects missing run/goal records. It builds Financial State context through `FinancialStateService`. Its docstring states that the report is a presentation/decision-explanation layer: it must not invent financial calculations, and What-If values should come from stored scenarios. Missing source data is represented explicitly.

## Basket and complete-plan reports

`BasketReportService` combines goal reports and multi-goal information into a basket output. Its extraction helpers include fallbacks for duration, target date and numeric fields; verify those defaults before interpreting output as source-confirmed values. `FinancialPlanService` composes GoalRepository, StrategyRepository, StrategyService, GoalReportService and MultiGoalPlanningService to build a consolidated live plan.

## Summary report

`SummaryReportService.generate()` delegates to `SummaryReportEngine`. The engine is described as aggregating canonical outputs rather than recalculating financial facts. It reads Financial State, GoalRepository and Moneywheel snapshot/service data and uses the risk-profiler engine. Output includes financial snapshot, goals, observations/actions and risk profile fields where available.

## Authority boundary

Calculation, goal feasibility, strategy evaluation and Moneywheel diagnostics own their respective logic. A report may format, summarize and explain those outputs; it should not become a parallel engine. Any derived metric in a report needs traceable canonical source or explicitly documented report-level arithmetic.
