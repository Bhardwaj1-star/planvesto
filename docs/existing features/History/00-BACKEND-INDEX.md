# History — Evidence Index

**Branch:** `main` · **Audited baseline:** `d7640029310c8e58d4cdd9a033d7683b5ea10002`  
**Status:** Source inspection only; no tests run.

History is not one canonical table or a single verified timeline in the inspected implementation. It is presented through separate feature surfaces and record families.

## Component documents

| Document | Scope |
|---|---|
| [01 — History surfaces and data families](01-HISTORY-SURFACES-AND-DATA-FAMILIES.md) | Goal/strategy history pages and record types |
| [02 — APIs, repositories and lifecycle meaning](02-APIS-REPOSITORIES-AND-LIFECYCLE.md) | Data ownership, ordering, versions and state distinctions |
| [03 — UI selection and navigation](03-UI-SELECTION-AND-NAVIGATION.md) | Goal selection, URL parameters and rendering |
| [04 — Tests and evidence gaps](04-TESTS-AND-EVIDENCE-GAPS.md) | Unverified chronology, authorization and acceptance semantics |

## Current surfaces found

- `frontend/app/investor/goal-history/page.tsx`
- `frontend/app/investor/strategy-history/page.tsx`

A standalone `frontend/app/investor/history/page.tsx` was not found at the expected path. This does not prove no other history component exists elsewhere.

## Record families

DefinedGoal versions; Strategy Runs and Strategy Versions; Financial State snapshots; Moneywheel snapshots; Action Plan decision records; diary financial decision history. These have different schemas, sources and lifecycle meanings. Separate APIs do not establish a unified event stream, nor does a newer record prove acceptance or rejection of an earlier one.
