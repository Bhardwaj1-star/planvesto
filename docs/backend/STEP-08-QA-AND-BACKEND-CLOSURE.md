# Step 08 — QA & Backend Closure

## Purpose
Validate the complete backend system before declaring the backend phase closed.

## Required validation
- Unit tests for calculation/strategy/orchestration/constraint/allocation logic.
- Integration tests for the complete multi-goal flow.
- Authentication and ownership checks.
- Single-goal regression tests.
- Multi-goal competition and priority-conflict tests.
- Ratio/constraint tests using only approved business rules.
- Report-generation tests, including override explanations.
- Error handling and infeasible-plan tests.

## Regression rule
Existing single-goal functionality must remain intact. Multi-goal orchestration must compose existing engines rather than silently changing their contracts.

## Repository hygiene
- Remove only obsolete duplicate branches/files created specifically for abandoned implementation attempts, and only after verifying they are not referenced.
- Do not delete existing production code merely to simplify structure.
- Keep `docs/backend/` as the source of implementation steps and update documents if implementation decisions change.

## Explicit non-scope
No frontend redesign, no Supabase schema changes, and no SQL migrations as part of backend closure.

## Final gate
Backend is closed only when tests pass, the end-to-end flow works, reports are generated correctly, and no known business-rule contradiction remains in the implemented pipeline.
