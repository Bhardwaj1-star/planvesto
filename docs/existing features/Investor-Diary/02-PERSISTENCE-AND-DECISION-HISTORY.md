# Investor Diary — Persistence and Decision-History Semantics

**Baseline:** `d7640029310c8e58d4cdd9a033d7683b5ea10002`.

## Diary entry persistence

`DiaryRepository.list_entries()` filters by planning unit and orders by date then created time descending. `get_entry()` scopes lookup by planning unit and ID. Create inserts an entry and expects returned row data; update/delete also filter by planning unit and ID and raise when no row is affected. The inspected repository does not show an explicit page limit in list calls.

## Financial decision records

The repository stores structured decisions in `financial_decision_history`; listing uses date and created-time descending order. The service can also compose historical events from other sources, including strategy/approval-related records, into decision history. These composed historical rows should not be mistaken for current state or all be treated as user-authored diary notes.

The service describes financial decisions as append-only, but the exact enforcement must be verified across API, repository and database policies. Do not infer append-only guarantees from a comment alone.

## Authority boundaries

- Diary entry: investor-authored context.
- Structured financial decision: historical evidence with source and optional source ID.
- Goal/Strategy Version: authoritative feature records for their respective objects.
- Strategy approval/accepted-plan state: only what its explicit persisted lifecycle records establish.
- Action Plan: action status and execution evidence.
- Financial State snapshot: calculated state at a point in time.

A diary note saying “accepted”, “completed” or “changed” does not perform a state transition. A prompt's action link does not prove execution. A decision history entry does not automatically establish an accepted plan.

## Migration evidence

`frontend/supabase/migrations/009_investor_diary.sql` is source evidence for intended tables/policies. Production migration status and effective RLS were not inspected.
