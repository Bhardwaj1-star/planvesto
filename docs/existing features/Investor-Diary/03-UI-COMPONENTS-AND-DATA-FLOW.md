# Investor Diary — UI Components and Data Flow

**Baseline:** `d7640029310c8e58d4cdd9a033d7683b5ea10002`.

## Active page composition

`frontend/app/investor/diary/page.tsx` loads entries and decisions in parallel via `getDiaryEntries()` and `getDecisions()`, shows Diary and Decision History tabs, and opens `BackendWriteEntryModal`. Saving closes the modal and reloads both lists. The page includes loading/error states and a retry action.

Active components include `DiaryBook`, `DiaryActionPlan`, `DecisionHistoryView` and `BackendWriteEntryModal`. `WriteEntryModal.tsx` also exists in the repository, but the inspected page imports the backend-backed modal; file presence alone does not mean the older modal is active.

## Client helpers

`frontend/lib/diary/diaryStore.ts` exposes the page-facing diary/decision helpers; `frontend/lib/api/diary.ts` provides backend requests. Trace actual helper implementation before assuming every operation uses the same endpoint or persistence path.

The backend-backed modal rejects blank content, resolves planning-unit ID and invokes entry creation; save errors are surfaced to the user. This is separate from the display-only contextual prompts and decision-history view.

## UI verification

Confirm date/timezone formatting, list ordering, tags/prompts display, edit/delete paths, refresh after mutations, prompt destination validity, loading/error/retry behavior and behavior when one of the two parallel list requests fails. Also identify any remaining local-storage persistence caller before removing or consolidating legacy helpers.
