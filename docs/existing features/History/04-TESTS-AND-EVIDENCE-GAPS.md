# History — Tests and Evidence Gaps

**Baseline:** `d7640029310c8e58d4cdd9a033d7683b5ea10002`. No history tests were run in this pass.

## Verification checklist

1. Goal versions: immutable snapshot semantics, current/latest pointer and ownership.
2. Strategy runs: descending order, stable tie-breaking and goal association.
3. Strategy versions: version lineage and selected-version semantics.
4. Financial State history: scope/investor ownership and limit behavior.
5. Moneywheel history: ordering and snapshot provenance.
6. Action decision history: deleted/cancelled/completed action retention and before/after payloads.
7. Diary decisions: append-only behavior and separation from user-authored notes.
8. UI: empty states, loading/error recovery, deep links and selection races.
9. Confirm whether any unified timeline exists before describing one.

## Evidence boundary

Relevant UI sources are `frontend/app/investor/goal-history/page.tsx` and `frontend/app/investor/strategy-history/page.tsx`. Backends are feature-specific. This audit does not claim a single History API, unified event schema, production ordering or successful test outcomes. Verification questions are not confirmed defects.
