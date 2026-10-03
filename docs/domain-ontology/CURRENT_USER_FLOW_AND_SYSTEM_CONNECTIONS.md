# Current User Flow & System Connections

## Purpose

This document records the user-flow changes completed in the current implementation and maps how the major frontend screens, API contracts, backend services, Strategy Run, StrategyVersion, Report, and Action Plan are connected as the code exists on main today.

This is a code-state document, not a future architecture proposal.

## 1. Current Core User Journey

    Goals
      ↓
    Select Goal
      ↓
    Strategy Builder
      ↓
    Strategy Run / Decision Engine
      ↓
    Recommended + Alternative Strategy
      ↓
    Select Strategy
      ↓
    Plan Your Implementation
      ↓
    Implementation Preview / What-if
      ↓
    Finalize Implementation
      ↓
    StrategyVersion
      ├──────────────→ Goal Report
      └──────────────→ Action Plan

Core authority:

    Strategy Run = evaluation / history
    StrategyVersion = finalized implementation authority

Report and Action Plan are downstream of the finalized StrategyVersion.

## 2. Goal Planner → Strategy Builder

Primary screens:

    /investor/goal-planner
    /investor/strategy-builder

Relevant frontend API:

    frontend/lib/api/goals.ts

Key connections:

    getGoals()
    getLatestDefinedGoal()
    getDefinedGoalVersion()
    getPlanningUnitId()

Flow:

    Goal Planner
        ↓
    Goal
        ↓
    DefinedGoal
        ↓
    Strategy Builder

## 3. Strategy Builder

Screen:

    /investor/strategy-builder

Responsibility:

The Strategy Builder is responsible for strategy building and selection.

Connection:

    frontend/app/investor/strategy-builder/page.tsx
        ↓
    frontend/lib/api/strategy.ts
        ↓
    POST /api/strategy/build
        ↓
    backend/api/strategy.py
        ↓
    StrategyService.build_strategy()
        ↓
    Strategy Engine

The returned StrategyRun contains applicable strategies, scenarios, rankings, recommendation, architectures, investor priorities, feasibility/constraint information, and run metadata.

The frontend displays the top two distinct strategy options.

## 4. Strategy Recommendation

Recommendation authority is:

    run.recommendation.recommended_strategy_id

The Builder uses this value to:

- identify Recommended Architecture
- show the Recommended badge
- place the recommendation first
- show one distinct alternative

Ranking is evidence. Recommendation is the decision output.

## 5. Strategy Run History

History is loaded through:

    getStrategyRunHistory()

API:

    GET /api/strategy/runs/{goal_id}/history

History is displayed as historical Strategy Run versions.

It does not provide current decision authority.

Current decision flow:

    Current Goal
        ↓
    POST /api/strategy/build
        ↓
    Current Strategy Run
        ↓
    Decision

Not:

    Latest Strategy Run
        ↓
    Restore Decision

The latest/history endpoint remains available as a historical/compatibility surface.

## 6. Strategy Selection → Implementation

The Builder validates:

- strategy run ID
- selected strategy
- selected scenario
- architecture

It then routes to:

    /investor/strategy-scenarios

with:

    goalId
    strategyRunId
    strategyId
    scenarioId
    architectureId
    goalVersion

The Builder therefore hands exact strategy context to the implementation stage.

## 7. Selection vs Finalization

Selection answers:

    Which strategy do I want to implement?

It does not create the final StrategyVersion.

Implementation answers:

    How will the selected strategy be configured?

Finalization answers:

    What exact implementation configuration becomes authoritative?

## 8. Plan Your Implementation

Screen:

    /investor/strategy-scenarios

Frontend API connections:

    getStrategyRunById()
    previewImplementation()
    finalizeImplementation()

Backend endpoints:

    GET  /api/strategy/runs/by-id/{strategy_run_id}
    POST /api/strategy/implementation/preview
    POST /api/strategy/implementation/finalize

## 9. Implementation Preview

Preview is stateless.

    Selected StrategyRun
          +
    Implementation Parameters
          +
    Assumptions
          +
    Funding Structure
          ↓
    POST /implementation/preview
          ↓
    StrategyService.preview_implementation()
          ↓
    Strategy Engine
          ↓
    Transient StrategyRun result

Preview does not create the authoritative StrategyVersion.

## 10. Implementation Finalization

Finalization is where the decision becomes persistent.

    Selected Strategy
          +
    Scenario
          +
    Architecture
          +
    Implementation Parameters
          +
    Assumptions
          +
    Funding Structure
          ↓
    POST /implementation/finalize
          ↓
    StrategyService.finalize_implementation()
          ↓
    StrategyVersionService.create_version()
          ↓
    StrategyVersion

The finalized implementation context is captured in the StrategyVersion implementation parameters.

## 11. StrategyVersion

StrategyVersion is the source of truth after implementation finalization.

Frontend:

    frontend/lib/api/strategy-version.ts

Relevant API connections:

    getStrategyVersionById()
    getStrategyVersionHistory()
    getCurrentPrimaryStrategy()

Selected-version resolution:

    GET /api/strategy/goals/{goal_id}/selected-version

Backend:

    backend/api/strategy_version.py

The selected StrategyVersion is resolved from the explicitly selected version associated with the goal, rather than from is_latest.

## 12. StrategyVersion → Report

Canonical individual report flow:

    Goal
      ↓
    Selected StrategyVersion
      ↓
    Goal Report

Frontend hub:

    /investor/reports

Resolution:

    GET /api/strategy/goals/{goal_id}/selected-version

Report:

    GET /api/strategy/strategy-versions/{strategy_version_id}/report

PDF:

    GET /api/strategy/strategy-versions/{strategy_version_id}/report.pdf

Backend:

    GoalReportService.build_report(
        strategy_version_id=...
    )

Therefore the finalized StrategyVersion, not latest StrategyRun history, is the canonical report source.

## 13. Report Contract

All individual goals use the same report contract.

Goal-specific values populate the generic structure.

Examples:

- Education
- Retirement
- Home
- Vehicle
- Wealth Creation

do not require separate report architecture merely because their data differs.

## 14. StrategyVersion → Action Plan

Screen:

    /investor/action-plan

The Action Plan is now a goal-first execution workspace.

Flow:

    Action Plan
        ↓
    Load Goals
        ↓
    Select Goal
        ↓
    Resolve Selected StrategyVersion
        ↓
    Load Actions
        ↓
    Show Execution Points

Frontend connections:

    getGoals()
    getSelectedStrategyVersion()
    getStrategyVersionById()
    getActions()

## 15. Goal-First Action Plan States

Finalized:

    Goal
      ↓
    StrategyVersion exists
      ↓
    Load Action Plan

Not finalized:

    Goal
      ↓
    No StrategyVersion
      ↓
    Show "Build this goal's strategy"
      ↓
    Strategy Builder

Finalized but no execution points:

    StrategyVersion
      ↓
    No actions
      ↓
    Generate Execution Points

Actions exist:

    Actions
      ↓
    Pending / Completed / Skipped

No goals:

    No goals
      ↓
    Show no-goals state
      ↓
    Goal Planner

## 16. Action Plan Backend

Frontend:

    frontend/lib/api/action-plan.ts

Backend:

    backend/api/action_plan.py

Load:

    GET /api/action-plan/actions

Generate:

    POST /api/action-plan/actions/generate

Complete:

    POST /api/action-plan/actions/{action_id}/complete

Decision history:

    GET /api/action-plan/decisions
    POST /api/action-plan/decisions

When scoped to a goal's finalized strategy, Action Plan queries are scoped by strategy_version_id.

## 17. Action Status

Current status vocabulary:

    planned
    confirmed
    completed
    cancelled

The current UI represents cancelled actions as skipped where appropriate.

No new database status was introduced for skipped.

## 18. Report and Action Plan Separation

Current architecture:

                    StrategyVersion
                       /       \
                      ↓         ↓
                   Report   Action Plan
                 (detail)   (execution)

Report answers:

    What is the detailed goal strategy and why?

Action Plan answers:

    What needs to be executed?

Neither is a mandatory workflow step inside Strategy Builder.

## 19. Shared Workflow Navigation

The old shared stepper:

    Build
    Participate With Numbers
    Report
    Action Plan

has been removed from the shared navigation component.

Current StrategyWorkflowNav is limited to the Strategy Builder's Planning Basket control.

This reflects the separation of functional stages rather than one mandatory stepper.

## 20. Reports Center

Current hub:

    /investor/reports

Report categories include:

- Complete Financial Plan
- Basket Goal Report
- Individual Goal Report

Individual Goal Report availability is based on the selected StrategyVersion.

Canonical flow:

    Goal
      ↓
    Selected StrategyVersion
      ↓
    Goal Report

## 21. Legacy Report Routes

Legacy run-based report routes still exist for compatibility:

    GET /api/strategy/runs/{strategy_run_id}/report
    GET /api/strategy/runs/{strategy_run_id}/report.pdf

Legacy retirement routes also remain:

    GET /api/strategy/runs/{strategy_run_id}/retirement-report
    GET /api/strategy/runs/{strategy_run_id}/retirement-report.pdf

Preferred current route:

    /api/strategy/strategy-versions/{strategy_version_id}/report

## 22. Complete System Connection Map

                           GOALS
                             │
                             ↓
                     DefinedGoal
                             │
                             ↓
                    STRATEGY BUILDER
                             │
                      POST /build
                             │
                             ↓
                    StrategyService
                             │
                             ↓
                      Strategy Engine
                             │
             ┌───────────────┼───────────────┐
             ↓               ↓               ↓
         Rankings      Recommendation   Architectures
             │               │               │
             └───────────────┼───────────────┘
                             ↓
                    Strategy Selection
                             │
                             ↓
                 PLAN YOUR IMPLEMENTATION
                             │
              ┌──────────────┴──────────────┐
              ↓                             ↓
       Preview / What-if                 Finalize
              │                             │
       transient result                    ↓
                                      StrategyVersion
                                             │
                              ┌──────────────┴──────────────┐
                              ↓                             ↓
                           REPORT                       ACTION PLAN
                              │                             │
                     Detailed Goal Report          Execution Points
                                                            │
                                                   ┌────────┴────────┐
                                                   ↓                 ↓
                                               Complete          Decisions

## 23. Data Authority Map

| Domain | Current Authority |
|---|---|
| Goal taxonomy | backend/rules/goals.py |
| Defined Goal | DefinedGoal / DefinedGoal version |
| Strategy evaluation | Strategy Engine |
| Strategy recommendation | Strategy Decision / StrategyRun recommendation |
| Strategy history | StrategyRun history |
| Architecture identity | canonical_architecture_id() |
| Implementation preview | transient StrategyRun result |
| Final implementation | StrategyVersion |
| Selected StrategyVersion | selected-version endpoint |
| Goal Report | selected StrategyVersion |
| Action Plan | selected StrategyVersion |
| Action execution | ActionPlanItem + decision records |
| Moneywheel | canonical backend Moneywheel contract |
| Frontend | API consumer / presentation layer |

## 24. Major Code-Level Connections

### Goal → Strategy

    Goal ID
      ↓
    /api/strategy/build
      ↓
    StrategyRun

### Strategy → Implementation

    StrategyRun ID
    + Strategy ID
    + Scenario ID
    + Architecture ID
      ↓
    /api/strategy/implementation/*

### Implementation → StrategyVersion

    Finalization
      ↓
    StrategyVersionService
      ↓
    StrategyVersion

### Goal → Selected StrategyVersion

    Goal ID
      ↓
    StrategyRepository.get_selected_strategy_version_id()
      ↓
    StrategyVersionRepository.get_by_id()

### StrategyVersion → Report

    StrategyVersion ID
      ↓
    GoalReportService
      ↓
    Report / PDF

### StrategyVersion → Action Plan

    StrategyVersion ID
      ↓
    ActionPlanRepository
      ↓
    ActionPlanService / StrategyActionGenerator
      ↓
    Execution Points

## 25. Current User Journey in Plain Language

1. Create or select a financial goal.
2. Open Strategy Builder.
3. Review the two strategy architectures.
4. Recommendation is identified by the decision engine.
5. User can compare the alternative.
6. User selects a strategy.
7. User enters implementation planning.
8. User tests implementation assumptions and funding structure.
9. User finalizes implementation.
10. System creates the StrategyVersion.
11. Report reads that StrategyVersion.
12. Action Plan reads that StrategyVersion.
13. User executes action points.
14. Completed, pending, and cancelled execution state remains visible.
15. Strategy Run history remains historical/audit information.

## 26. Current Separation of Concerns

    GOAL
      = What does the investor want?

    STRATEGY BUILDER
      = What strategy architecture should address the goal?

    IMPLEMENTATION
      = How should the selected strategy be configured?

    STRATEGY VERSION
      = What exact implementation was finalized?

    REPORT
      = What is the detailed decision/report for the goal?

    ACTION PLAN
      = What must be executed?

This separation should be preserved.

## 27. Current-State Caveats

This document records the code as it exists today; it does not claim that every legacy API has already been removed.

Known compatibility/current-state items:

- Legacy latest-run endpoint still exists.
- Legacy run-based report endpoints still exist.
- Legacy retirement report routes still exist.
- Strategy API still exposes select, although the current Builder routes into implementation planning.
- Strategy API still exposes custom scenario functionality.
- Frontend API types still contain some legacy report helpers.
- The implementation-scenarios route depends on explicit query context and should validate that context against the selected StrategyRun.
- Complete Financial Plan and Basket Report are separate consolidated planning surfaces from the individual StrategyVersion-scoped Goal Report.

These are code connections/compatibility surfaces, not automatically defects.

## 28. What Must Not Be Reintroduced

Do not reintroduce:

    Latest StrategyRun
        ↓
    Current Decision

Do not reintroduce:

    Strategy Builder
        ↓
    Report
        ↓
    Action Plan

as one mandatory stepper.

The intended authority remains:

    Selected / Finalized StrategyVersion
                 ↓
           ┌─────┴─────┐
           ↓           ↓
        Report     Action Plan

## 29. User-Flow Completion State

Current implemented connections:

- [x] Goal can be selected.
- [x] Strategy Builder evaluates the current goal directly.
- [x] Recommendation is sourced from the decision output.
- [x] Alternative strategy can be compared.
- [x] Strategy selection carries exact run/strategy/scenario/architecture context.
- [x] Implementation preview is stateless.
- [x] Finalization creates StrategyVersion.
- [x] Report resolves from selected StrategyVersion.
- [x] Action Plan starts with Goal selection.
- [x] Goals without a finalized StrategyVersion are explicitly represented.
- [x] Missing execution points are explicitly represented.
- [x] Execution progress is visible.
- [x] Completed actions remain visible.
- [x] Cancelled/skipped actions remain visible.
- [x] Strategy Run history remains informational/history.

## Final Architecture

                    INVESTOR GOAL
                         │
                         ↓
                 STRATEGY BUILDER
                         │
                         ↓
                 STRATEGY DECISION
                         │
              ┌──────────┴──────────┐
              ↓                     ↓
         Recommended             Alternative
              │                     │
              └──────────┬──────────┘
                         ↓
                IMPLEMENTATION
                         │
                    Finalization
                         ↓
                  STRATEGY VERSION
                    /           \
                   ↓             ↓
                REPORT       ACTION PLAN
                               │
                               ↓
                          EXECUTION
                               │
                      ┌────────┼────────┐
                      ↓        ↓        ↓
                   Pending  Completed  Skipped

This is the current user-flow and connection map implemented in the repository.
