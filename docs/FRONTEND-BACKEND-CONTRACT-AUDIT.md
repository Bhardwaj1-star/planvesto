# Frontend ↔ Backend Contract Audit

## Purpose
This document defines the mismatches found between the current frontend and the completed multi-goal backend. It is an implementation handoff for the coding agent.

## Current architecture
The backend now supports the multi-goal planning pipeline: financial context → goal strategies → constraints → resource allocation → consolidated Financial Plan → reporting.

The frontend still primarily follows the earlier goal-management/single-goal interaction model. Do not change backend business logic to accommodate the old frontend contract.

---

## Mismatch 1 — Multi-Goal Planning API is not wired into frontend

### Backend
The backend exposes the orchestration layer under `/api/orchestration` and has a dedicated multi-goal planning service.

### Frontend
The current frontend API layer does not have the corresponding multi-goal planning client flow.

### Required change
Add a frontend API client/service for the finalized multi-goal planning contract and use it from the appropriate planning flow.

### Rule
The frontend must consume the backend's canonical response; do not duplicate strategy/allocation calculations in React/TypeScript.

---

## Mismatch 2 — Goal priority representation

### Backend
The multi-goal planning contract uses normalized priority values such as `critical`, `high`, `medium`, and `low`.

### Frontend
The existing Goal Planner currently uses the older display-oriented priority value `Important`/equivalent legacy representation rather than the normalized backend contract.

### Required change
Create an explicit frontend mapping between UI labels and backend priority enum values. Do not send display strings directly to the backend.

Example:
- UI: Important → API: `high`
- UI: Must-have → API: `critical`
- UI: Nice-to-have → API: `medium`

Final mappings must follow the actual product UX decision; do not invent additional priority semantics.

---

## Mismatch 3 — Goal planning vs goal CRUD

### Current frontend behavior
Goal screens primarily create/update/read individual goals and perform individual calculations.

### Backend architecture
Individual goal management and multi-goal financial planning are separate concerns.

### Required change
Keep goal CRUD as data capture/management. Add a separate planning action that submits the selected goal set to the multi-goal planning API.

Do not replace goal CRUD with orchestration.

---

## Mismatch 4 — Financial Plan response is not consumed by frontend

### Backend output
The consolidated Financial Plan contains the resolved multi-goal outcome, including goal-level strategy/funding/allocation information and cross-goal decisions.

### Frontend gap
The current planning UI does not consume this canonical Financial Plan result as its primary planning result.

### Required change
Create typed frontend models matching the backend response and render the Financial Plan result from that response.

The frontend must not recompute:
- strategy selection;
- funding gap;
- resource allocation;
- constraint resolution;
- cross-goal trade-offs.

---

## Mismatch 5 — Client priority vs system-resolved outcome

### Backend rule
Client-selected goal priority remains traceable. A defined financial-ratio/constraint rule can change the resulting allocation/strategy outcome.

### Frontend requirement
The UI must distinguish:
1. Client-selected priority.
2. System-resolved planning outcome.
3. Reason/constraint causing the difference.

Do not present a system resolution as if the client manually changed priority.

The detailed explanation can remain report-first if that is the approved UX direction; the screen only needs to show the appropriate high-level state.

---

## Mismatch 6 — Report/PDF integration

### Backend
Goal/financial-plan reporting is generated from the finalized planning result.

### Frontend gap
The frontend must provide an action to request/download the finalized report without rebuilding the plan client-side.

### Required change
Wire the report endpoint/contract to the frontend download action once the exact backend endpoint is finalized.

---

## Mismatch 7 — Error and infeasibility states

### Backend
The planning pipeline can return validation, constraint, allocation, and infeasibility outcomes.

### Frontend requirement
Map backend errors/statuses to explicit UI states:
- invalid request;
- incomplete financial context;
- infeasible goal combination;
- resource conflict/resolution;
- report generation failure.

Do not replace backend error semantics with generic `Something went wrong` messages.

---

## Mismatch 8 — Contract typing and field names

The frontend and backend must use one canonical contract for:
- goal identifiers;
- priority;
- target amount/value;
- target date/duration;
- strategy result;
- funding requirement;
- allocation;
- constraints;
- resolved outcome;
- report metadata.

Before implementation, compare the actual backend Pydantic schemas against the frontend TypeScript interfaces and remove legacy/duplicate definitions.

---

## Implementation order
1. Inspect finalized backend request/response schemas.
2. Create/update frontend TypeScript types from those contracts.
3. Add the multi-goal API client.
4. Map existing Goal Planner data into the backend request.
5. Add the planning submission/action.
6. Consume the consolidated Financial Plan response.
7. Add high-level constraint/resolution states.
8. Wire report/PDF download.
9. Add frontend integration tests for the complete contract.

## Explicit non-scope
- Do not modify Supabase schema.
- Do not move business calculations into frontend.
- Do not duplicate backend strategy/allocation logic.
- Do not redesign unrelated screens.
- Do not invent new financial-ratio rules.
- Do not change backend contracts merely to preserve legacy frontend fields unless the backend contract audit proves the change is necessary.

## Definition of Done
A user can enter/select multiple goals in the existing frontend, submit them through the canonical multi-goal planning API, receive and display the consolidated Financial Plan, understand any system-resolved outcome at the appropriate UI/report level, and download the generated report—without frontend-side duplication of financial planning logic.
