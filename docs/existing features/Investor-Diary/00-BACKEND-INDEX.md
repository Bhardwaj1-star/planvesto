# Investor Diary — Backend Evidence Index

**Branch:** `main` · **Baseline:** `d7640029310c8e58d4cdd9a033d7683b5ea10002`  
**Status:** Source inspection only; no tests run or production database queried.

## Component documents

| Document | Scope |
|---|---|
| [01 — API, service and data contracts](01-API-SERVICE-AND-CONTRACTS.md) | Entry and decision endpoints, validation, authorization |
| [02 — Persistence and decision-history semantics](02-PERSISTENCE-AND-DECISION-HISTORY.md) | Diary entries versus structured financial decisions |
| [03 — UI components and client data flow](03-UI-COMPONENTS-AND-DATA-FLOW.md) | Active page composition, store helpers and modals |
| [04 — Tests and evidence gaps](04-TESTS-AND-EVIDENCE-GAPS.md) | Ownership, validation, legacy paths and UI verification |

## Runtime path

```text
/investor/diary
  -> diaryStore.ts / lib/api/diary.ts
  -> /api/diary
  -> auth + planning-unit ownership
  -> DiaryService + DiaryRepository
  -> diary_entries / financial_decision_history
```

## Primary source paths

`frontend/app/investor/diary/page.tsx`, `frontend/components/diary/DiaryBook.tsx`, `DecisionHistoryView.tsx`, `BackendWriteEntryModal.tsx`, `frontend/lib/diary/diaryStore.ts`, `frontend/lib/api/diary.ts`, `backend/api/diary.py`, `backend/services/diary_service.py`, `backend/data/diary_repository.py`, `backend/models/diary.py`, `backend/schemas/diary.py`, migration `009_investor_diary.sql`.

The retained [implementation audit](00-IMPLEMENTATION-AUDIT.md) is a summary, not proof that notes are lifecycle state. A diary note and a structured decision record remain separate from authoritative goal, strategy, Financial State and Action Plan records.
