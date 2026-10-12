# Profile — Backend Evidence Index

**Branch:** `main` · **Baseline:** `d7640029310c8e58d4cdd9a033d7683b5ea10002`  
**Status:** Source inspection only; no tests run or production data queried.

## Component documents

| Document | Scope |
|---|---|
| [01 — UI profile vs engine profile](01-UI-PROFILE-VS-ENGINE-PROFILE.md) | Account/onboarding UI and separate profile-engine output |
| [02 — Build API, engine and contracts](02-BUILD-API-ENGINE-AND-CONTRACTS.md) | Request, evidence normalization, risk/identity/behavioral outputs |
| [03 — Persistence, versions and integration](03-PERSISTENCE-VERSIONS-AND-INTEGRATION.md) | Snapshot freshness, version allocation and history |
| [04 — Tests and evidence gaps](04-TESTS-AND-EVIDENCE-GAPS.md) | Engine, UI, ownership and stale-state verification |

## Runtime paths

**UI profile:** `/investor/profile` → onboarding store + Supabase Auth user details → account/financial-information tabs.

**Profile engine:** `POST /api/profile/build` → authentication/ownership and optional snapshot ownership → `ProfileService` → current individual Financial State snapshot → `ProfileEngine` → persisted profile run, constraints and conflicts.

These are related but not equivalent. The UI completion percentage counts six local onboarding categories; it is not the profile engine's risk/suitability result.

## Primary source paths

`frontend/app/investor/profile/page.tsx`, `frontend/components/profile/FinancialInformationSection.tsx`, onboarding provider/store, `backend/api/profile.py`, `backend/schemas/profile.py`, `backend/services/profile_service.py`, `backend/engines/profile/engine.py`, `backend/engines/profile/{behavioral,constraints,identity,risk,strategy_context}.py`, `backend/data/profile_repository.py`.
