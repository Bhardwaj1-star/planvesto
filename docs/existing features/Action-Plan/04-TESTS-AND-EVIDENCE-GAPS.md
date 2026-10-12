# Action Plan — Tests and Evidence Gaps

**Baseline:** `d7640029310c8e58d4cdd9a033d7683b5ea10002`. Test file located but not run: `backend/tests/test_action_plan_lifecycle.py`.

## Verification checklist

1. Creation rejected without approved Strategy Version and selected-version lineage.
2. All action transitions and invalid transition errors.
3. Only approved editable fields can change during modify.
4. Repeated generation and duplicate actions.
5. Cross-planning-unit/action/version ownership checks.
6. Stale Financial State snapshot rejection.
7. Projected/actual state planning-unit and family-scope validation.
8. Persistence failure after snapshot write, action update or decision insert.
9. Deleted/cancelled/completed action history retention.
10. UI errors, loading states, filters, query-param goal selection and refresh.
11. Verify completion causes only documented state transitions; do not assume automatic strategy re-selection.

## Evidence boundary

Reviewed source paths are listed in `00-BACKEND-INDEX.md`. The existence of a test file is not a passing test result. Database RLS, production schema and end-to-end behavior remain unverified. Items above are verification questions, not confirmed defects.
