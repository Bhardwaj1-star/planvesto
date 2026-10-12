# Dashboard — Tests and Evidence Gaps

**Baseline:** `d7640029310c8e58d4cdd9a033d7683b5ea10002`. No Dashboard-specific test suite was run in this documentation pass.

## Verification checklist

1. Confirm route rejects invalid scope and mismatched investor/scope parameters.
2. Verify family and individual Financial State ownership and metric provenance.
3. Test missing versus zero metrics; ensure UI does not convert unknown to zero.
4. Test goal with latest DefinedGoal, missing DefinedGoal and cancelled DefinedGoal.
5. Validate coverage at zero/negative/normal targets and projected values above target.
6. Confirm goal target-date fallback formats and invalid source values.
7. Verify realtime subscription coverage, cleanup and refresh behavior.
8. Compare Dashboard vs Budgeting metrics only after source and period alignment.
9. Check browser loading, no-goal, API-error and partially available Financial State states.

## Evidence boundary

Source paths reviewed include `backend/api/dashboard.py`, `backend/services/dashboard_service.py`, `backend/schemas/dashboard.py`, `frontend/app/investor/financial-state/page.tsx`, `frontend/lib/api/dashboard.ts` and `frontend/lib/dashboard/realtime.ts`. Production rows, realtime delivery, browser behavior and runtime test outcomes remain unverified. Questions above are not confirmed defects.
