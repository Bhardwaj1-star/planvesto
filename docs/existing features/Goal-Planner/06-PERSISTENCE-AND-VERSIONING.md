# Goal Planner — Persistence and Versioning

**Source revision:** `5a3b060e1b27915ede226f5173364e23dca1263e`

## 1. Repository and tables referenced

Source: [backend/data/goal_repository.py](`https://github.com/Bhardwaj1-star/planvesto/blob/5a3b060e1b27915ede226f5173364e23dca1263e/backend/data/goal_repository.py#L9-L94`).

The repository uses `get_supabase()` and references these tables:
- `goals`
- `assets`
- `defined_goals`
- `defined_goal_asset_mappings`

This documents table names and queries visible in Python. It does not verify the live database schema, constraints, RLS or stored rows.

## 2. Transient retry wrapper

`GoalRepository._execute`, lines 14–23, retries up to three times for exceptions whose class names are `RemoteProtocolError`, `ConnectError`, `ReadTimeout`, or `WriteTimeout`. Delay is `0.5 × 2**attempt` seconds. Other errors and final-attempt errors are re-raised.

## 3. Base goal record

- `list_goals`, lines 25–27: selects `goal_id, planning_unit_id, goal_name, target_amount, target_date, priority, flexibility` from `goals`, filtered by planning unit and ordered by `created_at`.
- `get_planning_unit_assets`, lines 29–31: selects all columns from `assets` filtered by planning unit.
- `get_goal`, lines 33–35: selects one goal by planning unit and goal ID.
- `ensure_goal_record`, lines 37–48: writes name, target amount (= today cost), first-of-month target date, priority (default `Important`) and flexibility. If a supplied goal ID exists in that planning unit, it updates the record; otherwise it inserts a new record and returns its ID.

## 4. Defined-goal snapshot reads

- Latest snapshot query filters by planning unit, goal ID and `is_latest = True` (lines 50–52).
- Version lookup filters by planning unit, goal ID and version (lines 54–56).
- Version history selects identity/version flags, today cost, future target, projected mapped asset value, funding gap/status, metadata and created timestamp; order is descending by version (lines 58–60).
- `_hydrate_defined_goal`, lines 62–70, loads mapping rows separately by `defined_goal_id`, normalizes legacy goal type/name, and reconstructs several derived fields from `version_metadata`.

## 5. Snapshot writes

`save_defined_goal_snapshot`, lines 72–81:
1. marks the current latest snapshot false for the same planning unit and goal;
2. inserts the new `defined_goals` row with `is_latest = True`;
3. if mappings exist, inserts them into `defined_goal_asset_mappings`;
4. returns the new defined-goal ID.

The defined-goal row stores primary calculation fields plus `version_metadata`; the repository does not include required monthly contribution or feasibility as separate top-level fields in the shown insert payload. Mapping rows store allocation values, calculated amount/percentage, expected return, frequency and projected value.

## 6. Material-change detection

`has_material_change`, lines 86–94, returns true when:
- today cost differs by more than 0.01;
- target month or year differs;
- the map of asset ID → (allocation type, allocation value) differs;
- `version_metadata.dynamic_details` differs from request `dynamic_details`.

The check does not compare every GoalInput field. In particular, the material-change function shown does not compare inflation rate, expected return/frequency within a mapping, priority, flexibility or status. The service separately compares status, priority and flexibility before deciding to return the existing snapshot. This is a code-level boundary to validate, not a proposed behavior.

## 7. Save lifecycle and strategy recalculation hook

In [backend/services/goal_service.py](`https://github.com/Bhardwaj1-star/planvesto/blob/5a3b060e1b27915ede226f5173364e23dca1263e/backend/services/goal_service.py#L248-L309`):
- if there is no latest snapshot, version starts at 1 and change is material;
- otherwise it checks material change;
- if no material change and status/priority/flexibility are unchanged, it returns the current snapshot after refreshing feasibility;
- otherwise version increments by one;
- new snapshot is calculated, feasibility is applied, and snapshot is saved;
- for material changes after version 1, it attempts `StrategyService.on_defined_goal_updated`;
- success/failure is recorded in `version_metadata.strategy_recalculation`, and metadata is written back;
- exceptions are caught and logged, so failure of the strategy-recalculation hook does not undo the already-saved snapshot in this code path.

## 8. History reads

`get_version_history`, lines 323–333, builds summaries from repository rows and reads feasibility status/reason from `version_metadata.goal_feasibility`, defaulting status to `unknown` when absent.
