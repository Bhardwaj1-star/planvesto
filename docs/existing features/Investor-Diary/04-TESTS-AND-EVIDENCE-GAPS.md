# Investor Diary — Tests and Evidence Gaps

**Baseline:** `d7640029310c8e58d4cdd9a033d7683b5ea10002`. No diary tests were run in this pass.

## Verification checklist

1. Entry create/update/delete/list/get authorization and not-found behavior.
2. Validation limits, blank content, date format and timezone handling.
3. Decision-record append-only behavior and whether database policies enforce it.
4. Historical source composition, duplicate events and fallback timestamps.
5. Ordering ties, list bounds and pagination.
6. Active versus legacy local persistence callers.
7. Prompt routes and stale/invalid action links.
8. UI behavior when entry loading succeeds but decision loading fails (and vice versa).
9. Confirm notes cannot mutate accepted strategy, Action Plan status or Financial State.
10. Verify production migration/RLS independently.

## Evidence boundary

Source files: `backend/api/diary.py`, `backend/services/diary_service.py`, `backend/data/diary_repository.py`, `backend/models/diary.py`, `backend/schemas/diary.py`, and the frontend page/store/components listed in the index. Open questions are not confirmed defects.
