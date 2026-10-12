# Investor Diary — API, Service and Contracts

**Baseline:** `d7640029310c8e58d4cdd9a033d7683b5ea10002`.

## Router and authorization

`backend/api/diary.py` registers `/api/diary`. Requests authenticate and verify ownership of the supplied planning unit. The router exposes list/get/create/update/delete operations for entries and reads/creates for financial-decision records. Entry lookup is scoped by planning unit and entry ID; missing entries return 404. Exact response/error behavior should be confirmed per endpoint before client changes.

## Models and validation

`backend/models/diary.py` defines:
- `DiaryEntry`: planning unit, date, optional title, content, tags, contextual prompts, follow-up note, importance and timestamps.
- `FinancialDecision`: date, title, summary, category, source/source ID, metrics, notes and historical marker.
- `ContextualPrompt`: trigger, question, action text/href and prompt type.

Categories are limited to Strategy, Investment, Debt, Goal, Allocation and General. Prompt types are goal, strategy, liability, investment and budget.

`backend/schemas/diary.py` applies request length limits and strict request-model behavior. Create content has length 1–10,000; title max 200; tags max 30 items; prompts max 20; follow-up note max 2,000. Backend model validation also rejects blank planning-unit IDs/content and blank financial-decision title/summary. Frontend types are not a substitute for server validation.

## Service responsibilities

`DiaryService` wraps repository operations and can compose historical decision evidence from other feature records. Keep a user-authored note distinct from a structured financial-decision row: one is narrative, the other carries source-linked metrics and history metadata.

## Data boundary

`DiaryRepository` uses `diary_entries` and `financial_decision_history`. Access authorization must be enforced by backend ownership checks and database policy; the presence of a planning-unit field in a request is not proof of authorization.
