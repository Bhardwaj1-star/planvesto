# Profile — Build API, Engine and Contracts

**Baseline:** `d7640029310c8e58d4cdd9a033d7683b5ea10002`.

## API contract

Router `backend/api/profile.py` uses prefix `/api/profile`:
- `POST /build`: authenticate, verify investor ownership, optionally verify Financial State snapshot ownership, then call ProfileService. A service ValueError is translated to HTTP 422.
- `GET /latest`: returns latest profile run or 404 when absent.
- `GET /history`: returns history with limit constrained to 1–100 (default 20).

## Request and source state

`ProfileBuildRequest` is defined in `backend/schemas/profile.py`. The service obtains the current **individual** Financial State snapshot. If a supplied snapshot ID differs from the current snapshot, the build is rejected as stale. It strips internal `__snapshot_authority` metadata before engine input. The persisted input snapshot records declared constraints, observed behavior, preferences, priorities, Financial State and snapshot ID.

## Engine composition and RiskProfilerEngine Architecture

`ProfileEngine` (`backend/engines/profile/engine.py`, version `profile-engine-v6`) coordinates:
1. `BehavioralRules` to resolve observed behavior into observed dimensions.
2. `ConstraintRules` (`backend/engines/constraints/policy.py`) to normalize constraints/preferences and compute evidence confidence:
   $$\text{confidence} = \text{round}\left(\min\left(1.0, \frac{\text{SOURCE\_PRIORITY}[\text{source}]}{4.0} + 0.15 \times (\text{evidence\_count} > 1)\right), 4\right)$$
   Where source priorities are: `financial_state: 4`, `observed_behavior: 3`, `declared_constraint: 2`, `preference: 1`.
3. `build_identity_profile` (`backend/engines/profile/identity.py`) for investor identity evidence.
4. **Authoritative `RiskProfilerEngine` (`backend/engines/risk_profiler/engine.py`):**
   Produces a canonical `RiskProfile` across **3 locked dimensions**:
   - **Dimension 1: Canonical Risk Required (`risk_need_required_return`):**
     Pure mathematical derived fact calculated from future target, current funding, and duration:
     $$r = \left(\frac{\text{future\_target}}{\text{current\_funding}}\right)^{\frac{1}{\text{duration}}} - 1$$
     Status is `"authoritative"` when inputs exist, else `"unavailable"`.
   - **Dimension 2: Risk Capacity (Observable Financial Constraints):**
     Derived deterministically from balance sheet and cash flow facts:
     - `risk_capacity_surplus`: Monthly investable surplus (INR/month).
     - `risk_capacity_reserve`: Liquid safety reserve (months).
     - `risk_capacity_debt_service_ratio`: $\text{EMI} / \text{Income}$ (ratio).
     - `risk_exposure_max_asset_concentration`: $\text{Largest Asset} / \text{Total Assets}$ (ratio).
     - `risk_exposure_outstanding_debt`: Total liabilities outstanding (INR).
     - `risk_need_shortest_goal_horizon`: Minimum goal duration (years).
   - **Dimension 3: Risk Tolerance (Observed Behavioral Dimensions):**
     Product selection preference from observed investor decisions (`BehavioralRules`), marked as soft constraint (`confidence: 0.75`).
   - **Overall Risk Status:** `"complete"` (all 3 dimensions available), `"partial"` (any 1 or 2 available), or `"requires_review"` (none available).
5. Financial State facts such as monthly surplus, reserve months, debt-service ratio and expense ratio when the corresponding metrics are available.

It detects conflicts and validates priority rankings. Priority ranks annotate constraints; the engine docstring states that priorities do not change authority. Engine version currently appears as `profile-engine-v6`.

## Limits of inference

The service call shown passes financial state and declared/observed/preferences/priorities. Optional identity/assets/liabilities/goals parameters exist on the engine signature but are not supplied by this call in the inspected path. Do not claim those optional inputs are populated by this endpoint without evidence.
