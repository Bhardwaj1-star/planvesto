# Goal Planner — Taxonomy and Data Contracts

**Source revision:** `5a3b060e1b27915ede226f5173364e23dca1263e`

## 1. Canonical goal types

Authority in source: [backend/rules/goals.py](`https://github.com/Bhardwaj1-star/planvesto/blob/5a3b060e1b27915ede226f5173364e23dca1263e/backend/rules/goals.py#L1-L99`).

`GoalType` at lines 8–19 is a Literal with ten values:

- `retirement`
- `marriage`
- `vehicle`
- `dream_home`
- `education`
- `vacation`
- `debt_freedom`
- `wealth_creation`
- `fire_passive_income`
- `others`

Canonical display names are held in `CANONICAL_GOAL_NAMES`, lines 29–40. `others` may preserve a supplied non-empty fallback name; the other canonical types return their canonical display label via `canonical_goal_name` (lines 75–85).

`canonical_goal_type` (lines 70–73) trims and lowercases the input, then accepts a canonical ID or display name from the lookup map. Unknown input returns an empty string.

## 2. Goal priority vocabulary

- `GoalPriority`: `critical | high | medium | low`, lines 21–22.
- Aliases in `GOAL_PRIORITY_ALIASES`, lines 24–27:
  - critical: `critical`, `must-have`, `must have`
  - high: `high`, `important`
  - medium: `medium`, `moderate`, `aspirational`
  - low: `low`, `nice-to-have`, `nice to have`, `discretionary`
- `canonical_goal_priority`, lines 87–90, normalizes whitespace/case and defaults unknown or empty values to `medium`.
- `DISCRETIONARY_GOAL_TYPES`, lines 43–49: vehicle, dream_home, vacation, wealth_creation, others.
- `ESSENTIAL_GOAL_TYPES`, lines 51–57: retirement, marriage, education, debt_freedom, fire_passive_income.
- These sets are used by multi-goal rules; the categories do not themselves calculate a goal target.

## 3. Request schemas

Source: [backend/schemas/goals.py](`https://github.com/Bhardwaj1-star/planvesto/blob/5a3b060e1b27915ede226f5173364e23dca1263e/backend/schemas/goals.py#L1-L62`).

### `AssetMappingInput` — lines 9–21

| Field | Type / constraint |
|---|---|
| `asset_id` | string, length 1–100 |
| `allocation_type` | literal `currency` or `percentage` |
| `allocation_value` | float ≥ 0; infinity/NaN disallowed |
| `expected_return` | optional float, minimum -0.99, maximum 1.0; infinity/NaN disallowed |
| `return_frequency` | annual, semi-annual, semiannual, half-yearly, quarterly or monthly; default annual |

Post-validation rejects percentage allocation above 100.

### `GoalInput` — lines 23–48

| Field | Type / constraint |
|---|---|
| `planning_unit_id` | required string, length 1–100 |
| `goal_id` | optional string, length 1–100 |
| `investor_id` | optional string, length 1–100 |
| `goal_name` | required string, length 1–200 |
| `goal_type` | `GoalType`; pre-validator canonicalizes known ID/display label |
| `today_cost` | float > 0; infinity/NaN disallowed |
| `target_month` | integer 1–12 |
| `target_year` | integer 1900–2200 |
| `inflation_rate` | optional float 0–1; infinity/NaN disallowed |
| `priority` | optional string, max 50 |
| `priority_rank` | optional integer ≥ 1 |
| `flexibility` | string, default `Flexible`, length 1–50 |
| `status` | string, default `Active`, length 1–30 |
| `asset_mappings` | list of AssetMappingInput, default empty, max 100 |
| `dynamic_details` | dictionary, default empty, max 100 entries |

The schema inherits `StrictRequestModel` from `schemas.base`. That base model's full strictness configuration was not audited in this document.

`GoalCalculateRequest` at lines 50–51 adds no fields; it subclasses `GoalInput`.

### `GoalSummary` — lines 54–62

Fields: `goal_id`, `planning_unit_id`, `goal_name`, `target_amount`, optional `target_date`, `priority`, and `flexibility`.

## 4. Defined output model

Source: [backend/models/defined_goal.py](`https://github.com/Bhardwaj1-star/planvesto/blob/5a3b060e1b27915ede226f5173364e23dca1263e/backend/models/defined_goal.py#L1-L80`).

### `DefinedGoalAssetMapping` — lines 7–20

Contains optional mapping/defined-goal IDs; asset ID/name; allocation type/value; allocated amount and percentage; expected return; return frequency (default annual); projected value; optional created timestamp.

### `DefinedGoal` — lines 22–65

The returned defined snapshot includes:
- identity: `defined_goal_id`, `goal_id`, `planning_unit_id`, `investor_id`;
- version: `version` default 1 and `is_latest` default true;
- goal definition: type, name, today cost, inflation rate/source, target month/year, duration;
- target/funding: future target, projected mapped-asset value, funding gap/status, required monthly contribution, funding return assumption;
- preferences: priority, optional priority rank, flexibility, status;
- derived state: mapped assets, feasibility status/reason, available monthly surplus, monthly contribution/surplus gap, funding strategies;
- workflow/version metadata: `workflow_readiness`, `version_metadata`, created timestamp.

`funding_status` is Literal `Shortfall | On Track | Overfunded`. `feasibility_status` is Literal `feasible | constrained | infeasible | unknown`. These are distinct status vocabularies.

The `hydrate_workflow_readiness` validator at lines 57–64 restores the top-level readiness object from `version_metadata.workflow_readiness` when the top-level key is absent.

### `DefinedGoalVersionSummary` — lines 67–80

Includes defined-goal ID, goal ID, version/latest marker, today cost, future target, projected mapped-asset value, funding gap/status, feasibility status/reason and created timestamp.

## 5. Data shape caveats observed in source

- Request `priority` is an unconstrained optional string, while the separate canonical priority helper recognizes four normalized priority classes.
- `GoalInput.priority_rank` is accepted, but the shown `GoalEngine.calculate_defined_goal` stores it through `getattr(goal_input, "priority_rank", None)`; the inspected repository snapshot payload does not persist a dedicated `priority_rank` column.
- `DefinedGoal.required_monthly_contribution`, funding return, feasibility and several surplus fields are reconstructed from `version_metadata` during repository hydration rather than read from separate top-level columns.
- These are code-shape observations, not recommendations or proof of a production database defect.
