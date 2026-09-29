# STEP-09 — Individual Goal Report & PDF

## Purpose
Define the missing individual-goal reporting flow. The existing Strategy Builder already produces a strategy for an individual goal; this step must expose a goal-specific report/action output without confusing it with the consolidated multi-goal financial plan.

## Required Architecture

`Financial State → Selected Goal → Strategy Engine → Goal Strategy Result → Goal Report / Action Plan → Goal PDF`

The Multi-Goal Orchestrator remains responsible for combining multiple goal results into the Consolidated Financial Plan. It must not replace the individual-goal report flow.

## Requirements

1. **Individual Goal Report**
   - Accept one goal and the investor's relevant financial context.
   - Use the existing single-goal Strategy Engine; do not duplicate or rewrite its business logic.
   - Report the goal-specific strategy, feasibility/funding result, relevant financial-ratio constraints, assumptions, trade-offs, and recommended actions.
   - Preserve the client's selected goal priority separately from any system-resolved priority.

2. **Individual Goal Action Plan**
   - Provide actionable steps specific to that goal.
   - Actions must be derived from the finalized goal strategy/result, not independently recalculated by the reporting layer.
   - Clearly identify prerequisite financial-ratio actions when they affect the goal.

3. **Individual Goal PDF**
   - Generate a downloadable PDF for the selected goal.
   - PDF generation must consume the finalized goal report model; it must not create a second calculation path.
   - Existing single-goal report/PDF functionality must remain backward compatible.

4. **Multi-Goal Separation**
   - Individual Goal Report = one goal's strategy and actions.
   - Consolidated Financial Plan = all selected goals after cross-goal constraints/resource allocation.
   - Master PDF must remain separate from the individual Goal PDF.

5. **Frontend Contract**
   - Strategy Builder's existing Report / Action entry point should expose the individual goal report.
   - The existing consolidated Action Plan page remains responsible for the complete financial plan PDF.
   - Do not make the frontend perform financial calculations.

6. **API Contract**
   - Add/confirm a goal-specific report endpoint/service using existing auth and ownership checks.
   - Return a stable typed report model suitable for both screen rendering and PDF generation.
   - Routes should only validate/request/return data; business logic belongs in services/engines.

7. **Testing**
   Add tests covering:
   - one goal report generation;
   - goal-specific strategy data is preserved;
   - client priority vs resolved priority;
   - ratio constraint findings and prerequisite actions;
   - infeasible/partial funding result;
   - PDF generation from the finalized report model;
   - ownership/auth failure;
   - regression of existing single-goal Strategy Engine and reports;
   - separation between individual Goal PDF and consolidated Financial Plan PDF.

## Constraints

- Do not modify the Supabase schema.
- Do not create SQL migrations.
- Do not rewrite the existing Strategy Engine.
- Do not duplicate financial calculations inside reporting/PDF code.
- Do not remove or alter the existing consolidated multi-goal report/PDF flow.

## Definition of Done

An investor can select one goal, build its strategy, open its Report / Action Plan, and download a goal-specific PDF. Multiple goals can still flow through the Multi-Goal Orchestrator into the separate Consolidated Financial Plan and master PDF.
