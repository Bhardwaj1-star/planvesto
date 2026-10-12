# Profile — Tests and Evidence Gaps

**Baseline:** `d7640029310c8e58d4cdd9a033d7683b5ea10002`. Test files were located but not run.

## Test files located

- `backend/tests/test_profile_engine.py`
- `backend/tests/test_profile_strategy_context.py`
- `backend/tests/test_behavioral_profile.py`
- `backend/tests/test_investor_identity_profile.py`
- `backend/tests/test_risk_profile.py`
- `backend/tests/test_risk_profile_integration.py`
- `backend/tests/test_risk_profiler_consolidation.py`

## Verification checklist

1. Build/latest/history authorization and snapshot ownership.
2. Stale Financial State snapshot rejection.
3. Profile version conflict/retry and concurrent version allocation.
4. Partial failure between profile-run and constraints/conflicts writes.
5. Constraint normalization, confidence, conflicting evidence and priority validation.
6. Missing/unavailable Financial State metrics do not become false facts.
7. Distinguish UI completion percentage from engine result and risk profile.
8. Verify which optional engine inputs are actually wired by the service.
9. Validate latest/history ordering and profile input snapshot provenance.
10. Production migration/RLS and browser behavior.

## Evidence boundary

The current source indicates code paths; it does not prove production deployment, data freshness or passing tests. Items above are verification questions, not confirmed defects.
