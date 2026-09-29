# Planvesto Backend Build Plan

## Purpose
This directory is the source of truth for the backend build sequence. Coding agents must read these documents before changing backend code.

## Current repository baseline
- Repository: `Bhardwaj1-star/planvesto`
- `main` is currently the baseline commit.
- `feature/multi-goal-financial-plan-v2` and `feature/multi-goal-plan-v2` currently compare identical to `main`; they do not contain additional commits to reuse.
- Existing backend already contains API, service, data/repository, model/schema, engine and strategy-version layers.
- Existing `StrategyEngine` is the single-goal strategy decision layer and must be reused rather than replaced.
- Existing `api/orchestration.py` + `PlanningOrchestrationService` currently build planning context/module availability; they are not yet the full multi-goal decision orchestrator.

## Non-negotiable scope
1. Backend only.
2. Do not redesign or modify frontend.
3. Do not modify the Supabase schema.
4. Do not create SQL migrations.
5. Do not duplicate existing strategy logic; extend through clear orchestration/service boundaries.
6. Preserve existing API compatibility unless a documented backend change is required.
7. Every implementation step must include tests for the business logic it introduces.

## Target backend flow
Financial State -> Goals -> Goal Priority + Financial-Ratio Checks -> Multi-Goal Orchestrator -> Existing Strategy Engine per goal -> Cross-Goal Resource Allocation / Conflict Resolution -> Consolidated Financial Plan -> Action Plan + Report/PDF data.

## Build sequence
- Step 1: Repository baseline, architecture contract and implementation boundaries.
- Step 2: Multi-goal input/context assembly and goal validation.
- Step 3: Goal priority resolution: client priority + financial-ratio constraints/checks; system resolution is allowed internally, with override reasoning exposed in the report rather than as a screen control.
- Step 4: Cross-goal resource allocation and conflict resolution.
- Step 5: Execute/reuse single-goal StrategyEngine for each eligible goal.
- Step 6: Consolidate goal-level outputs into one Financial Plan.
- Step 7: Generate structured report/PDF payloads for individual goals and the complete plan.
- Step 8: End-to-end backend tests, regression checks and cleanup of obsolete duplicate branches/code.

Each step should have its own document under `docs/backend/`. Do not implement later steps early unless required as a dependency and documented in that step's file.
