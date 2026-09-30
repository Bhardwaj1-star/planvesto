# Remaining Backend Implementation Gaps

## Purpose
This document is the implementation checklist for `feature/multi-goal-backend-v2` after comparing the branch against the existing `docs/backend/STEP-01` through `STEP-08` plans.

**Important:** Presence of the step documents does not mean the step is implemented. This file lists the gaps that must be completed before backend closure.

## Current assessment
The repository still contains the existing single-goal Strategy Engine and the existing planning-context orchestration layer. The documented multi-goal pipeline is not yet fully implemented.

---

## GAP 1 — Multi-Goal Orchestrator
**Related:** STEP-02

Implement the actual multi-goal orchestration engine/service.

Required:
- Accept investor financial context and selected goals.
- Preserve client-selected goal priority.
- Invoke the existing single-goal Strategy Engine independently for each goal.
- Collect each goal's strategy/feasibility/funding result.
- Coordinate the results across goals.
- Produce a deterministic consolidated orchestration result.

Expected architecture (adapt to existing repository conventions):
- `backend/engines/orchestration/`
- `backend/services/multi_goal_planning_service.py`
- request/response schemas where required
- existing `backend/api/orchestration.py` only as the API boundary

Do not rewrite the existing single-goal Strategy Engine.

---

## GAP 2 — Financial Ratio / Constraint Layer
**Related:** STEP-03

Implement the separate constraint evaluation layer required by the approved business rules.

Required:
- Read available financial-state values.
- Calculate/use only explicitly approved financial ratios.
- Determine whether a goal/strategy has a relevant constraint.
- Distinguish warning/informational conditions from hard constraints.
- Return machine-readable constraint results to orchestration.

Business rule:
- Client chooses goal priority.
- Planvesto checks relevant financial ratios/financial-health conditions.
- Where an explicitly defined rule conflicts with the client's priority, the system may override the resulting allocation/strategy outcome.
- The client priority must remain traceable.
- The override reason must be available to the final report.

Do not invent ratio thresholds during implementation.

---

## GAP 3 — Shared Resource Allocation
**Related:** STEP-04

Implement deterministic allocation of shared resources across goals.

Required:
- Determine resources available for goals.
- Detect competition between goals.
- Apply client priority.
- Apply approved ratio/constraint rules.
- Resolve partial funding and infeasible combinations.
- Preserve the reason for material allocation decisions.
- Return both goal-level and consolidated allocation results.

The allocator must not silently change client priority.

---

## GAP 4 — Consolidated Financial Plan
**Related:** STEP-05

Create the canonical backend Financial Plan object/result.

It must consolidate:
- investor financial context;
- all selected goals;
- client-selected priority;
- resolved allocation/outcome;
- per-goal strategy;
- funding requirement;
- allocation;
- feasibility;
- ratio/constraint findings;
- cross-goal trade-offs;
- unresolved limitations/actions.

This object becomes the single source consumed by reporting. Reporting must not recalculate business logic.

---

## GAP 5 — Report / PDF Generation
**Related:** STEP-06

Implement report generation from the finalized Financial Plan.

Required report sections:
- overall financial-plan summary;
- goal-by-goal strategy and funding outcome;
- client-selected priorities;
- system-resolved differences, where applicable;
- ratio/constraint findings;
- cross-goal trade-offs;
- feasibility/infeasibility;
- required actions.

Important:
The report must explain system-driven allocation overrides. It must not imply that the client manually changed their priority.

The report layer must consume the finalized Financial Plan rather than independently recomputing decisions.

PDF output must follow the project's existing backend conventions.

---

## GAP 6 — API Integration
**Related:** STEP-07

Connect the complete pipeline through the backend API.

Required flow:

`API Request → Financial Context → Goals → Single-Goal Strategy Engine → Ratio/Constraint Evaluation → Multi-Goal Allocation → Consolidated Financial Plan → Report`

Rules:
- API routes should orchestrate calls, not contain business calculations.
- Reuse existing authentication/ownership conventions.
- Use stable request/response schemas.
- Return deterministic validation/infeasibility errors.

Do not modify frontend as part of this work.

---

## GAP 7 — Tests / Backend Closure
**Related:** STEP-08

Add/complete tests for the entire pipeline.

Minimum scenarios:
1. One goal — regression against existing single-goal behavior.
2. Multiple independent goals.
3. Multiple goals competing for the same surplus.
4. Client priority preserved when no constraint conflicts.
5. Ratio/constraint-driven allocation change.
6. Traceability of client priority vs resolved outcome.
7. Partial funding.
8. Infeasible combination.
9. Correct report explanation for an override.
10. Auth/ownership behavior.
11. End-to-end API flow.

Backend closure requires passing unit + integration/end-to-end tests.

---

## Explicit Non-Scope
Do NOT:
- redesign frontend;
- modify Supabase schema;
- create SQL migrations;
- duplicate/rewrite the single-goal Strategy Engine;
- implement product selection;
- implement risk profiling;
- invent financial-ratio thresholds;
- hide infeasible goals or cross-goal trade-offs.

---

## Implementation Order
Execute in this order:

1. Multi-Goal Orchestrator
2. Financial Ratio / Constraint Layer
3. Shared Resource Allocation
4. Consolidated Financial Plan
5. Report/PDF Generation
6. API Integration
7. Full QA / Regression / Backend Closure

Do not mark a step complete merely because its files exist. Mark it complete only when its documented behavior is implemented and tested.

## Final Definition of Done
The backend is complete only when a real authenticated request containing multiple goals can:

1. load the investor's financial context;
2. evaluate each goal using the existing Strategy Engine;
3. evaluate relevant approved constraints;
4. resolve competition for shared resources;
5. produce one consolidated Financial Plan;
6. preserve client priority and explain any system-driven resolution;
7. generate the final goal reports/PDF;
8. pass the complete automated test suite;
9. do all of the above without frontend changes or database-schema changes.
