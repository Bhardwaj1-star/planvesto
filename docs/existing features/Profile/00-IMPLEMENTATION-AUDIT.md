# Profile — Implementation Audit

**Audited baseline:** `55d8b40235087b7c1f0052d4736303665fb5e41e`  
**Status:** Source inspection only; production state not independently verified. No application code changed.

## Source evidence
UI: `frontend/app/investor/profile/page.tsx`; form: `frontend/components/profile/FinancialInformationSection.tsx`; onboarding store/provider; API: `backend/api/profile.py`; service/engine: `backend/services/profile_service.py`, `backend/engines/profile/engine.py`.

## UI versus engine
The page reads personal information, income, expenses, assets, liabilities and goals from onboarding state. It loads email from Supabase Auth, derives initials, calculates completion from six local categories (name, income, expenses, assets, liabilities, goals), supports account/financial-information tabs and signs out before redirecting to login.

The backend Profile API has a separate profile engine. The engine describes resolving planning constraints from evidence; this is not equivalent to the page's six-item completion percentage. UI completeness must not be conflated with validated risk profile or suitability.

## API and authority
The router prefix is `/api/profile`. POST `/build` authenticates, verifies investor ownership and optional snapshot ownership; service ValueErrors become 422. GET `/latest` and `/history` require planning-unit/investor IDs and validate investor ownership; history limit is 1–100. The service builds from Financial State context and persists/retrieves profile results. Onboarding UI state alone does not prove a profile-engine result was rebuilt; latest result does not prove its input snapshot is current.

## Verification gaps
No tests were run. Verify store freshness, tab routing, sign-out errors, UI completion versus engine output, build/snapshot ownership, latest-not-found response, history ordering/limit, stale Financial State handling and persistence of declared constraints/observed behavior/preferences.