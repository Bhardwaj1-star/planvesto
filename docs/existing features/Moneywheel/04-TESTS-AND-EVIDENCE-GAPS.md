# Moneywheel — Tests and Evidence Gaps

**Baseline:** `d7640029310c8e58d4cdd9a033d7683b5ea10002`. Tests were located but not run.

## Test files located

- `backend/tests/test_moneywheel.py`
- `backend/tests/test_moneywheel_api.py`
- `backend/tests/test_moneywheel_api_contract.py`
- `backend/tests/test_moneywheel_financial_state_adapter.py`
- `backend/tests/test_moneywheel_service.py`

Finding a test file is not proof that it passes in the current environment.

## Verification checklist

1. Each of the nine canonical keys appears exactly once and keeps stable units/formula metadata.
2. Threshold boundary values are tested on both sides of each boundary.
3. Missing inputs, zero denominators, zero funding and non-finite calculations return unavailable outputs with reasons.
4. Client-supplied snapshot fields cannot override server-owned Financial State.
5. Planning-unit ownership is enforced on calculate/latest/history.
6. Snapshot ordering, history limit and transient retry behavior are correct.
7. The stored Financial State snapshot matches the data used for calculation.
8. UI category counts, unavailable labels, loading/error states and history display match the API contract.
9. Report consumers treat Moneywheel as diagnostic evidence, not a strategy/acceptance authority.
10. Production migration/RLS and database constraints are checked independently.

## Evidence boundary

This audit is source-derived. It does not prove production schema, actual RLS, deployed code, end-to-end browser behavior or test results. Potential issues above are verification questions, not confirmed defects.
