# Profile — Build API, Engine and Contracts

**Baseline:** `d7640029310c8e58d4cdd9a033d7683b5ea10002`.

## API contract

Router `backend/api/profile.py` uses prefix `/api/profile`:
- `POST /build`: authenticate, verify investor ownership, optionally verify Financial State snapshot ownership, then call ProfileService. A service ValueError is translated to HTTP 422.
- `GET /latest`: returns latest profile run or 404 when absent.
- `GET /history`: returns history with limit constrained to 1–100 (default 20).

## Request and source state

`ProfileBuildRequest` is defined in `backend/schemas/profile.py`. The service obtains the current **individual** Financial State snapshot. If a supplied snapshot ID differs from the current snapshot, the build is rejected as stale. It strips internal `__snapshot_authority` metadata before engine input. The persisted input snapshot records declared constraints, observed behavior, preferences, priorities, Financial State and snapshot ID.

## Engine composition

`ProfileEngine` uses:
- `BehavioralRules` to resolve observed behavior;
- `ConstraintRules` to normalize declared constraints/preferences and derive confidence;
- `build_risk_profile` for risk evidence;
- `build_identity_profile` for identity evidence;
- Financial State facts such as monthly surplus, reserve months, debt-service ratio and expense ratio when the corresponding metrics are available.

It detects conflicts and validates priority rankings. Priority ranks annotate constraints; the engine docstring states that priorities do not change authority. Engine version currently appears as `profile-engine-v6`.

## Limits of inference

The service call shown passes financial state and declared/observed/preferences/priorities. Optional identity/assets/liabilities/goals parameters exist on the engine signature but are not supplied by this call in the inspected path. Do not claim those optional inputs are populated by this endpoint without evidence.
