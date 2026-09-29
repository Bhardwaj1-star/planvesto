# Step 06 — Financial Plan & Goal Reports

## Purpose
Generate downloadable/report-ready outputs from the final Financial Plan without duplicating financial logic.

## Required report content
- Overall financial-plan summary.
- Goal-by-goal strategy and funding outcome.
- Client-selected priorities.
- Any system-resolved allocation differences and reasons.
- Relevant ratio/constraint findings.
- Cross-goal trade-offs.
- Feasibility/infeasibility and required actions.

## Rule
The report is where system overrides/reasons are explained. The screen/API data should not falsely imply that the client manually changed priority.

## Architecture
Report generation consumes the finalized Financial Plan object. It must not independently recalculate strategy or allocation decisions.

## Output
Provide a stable report model and PDF generation path using the project's existing backend conventions. Do not change database schema or frontend.

## Tests
Verify single-goal, multi-goal, conflict/override, and infeasible-plan reports contain the correct traceable explanations.
