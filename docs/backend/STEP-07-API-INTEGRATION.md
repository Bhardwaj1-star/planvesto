# Step 07 — API Integration & End-to-End Flow

## Purpose
Expose the completed backend planning pipeline through stable API contracts while preserving existing authentication/ownership conventions.

## Flow
Request → financial context → selected goals → single-goal Strategy Engine per goal → ratio/constraint evaluation → multi-goal allocation → consolidated Financial Plan → report generation.

## Responsibilities
- Define/extend request and response schemas using existing project conventions.
- Reuse current authentication and ownership checks.
- Connect service layers without putting business logic in API routes.
- Return deterministic errors for invalid/infeasible requests.
- Keep report generation downstream of the finalized Financial Plan.

## Do NOT
- Put calculations in FastAPI routes.
- Change Supabase schema.
- Redesign frontend.
- Duplicate Strategy Engine logic.

## Completion gate
A complete authenticated end-to-end request can build a multi-goal plan and generate the corresponding report using the backend only.
