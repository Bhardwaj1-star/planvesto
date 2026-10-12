# Goal Planner — Goal Calculation Engine

**Source revision:** `5a3b060e1b27915ede226f5173364e23dca1263e`

## 1. Entry point

[backend/engines/goal/engine.py](`https://github.com/Bhardwaj1-star/planvesto/blob/5a3b060e1b27915ede226f5173364e23dca1263e/backend/engines/goal/engine.py#L17-L173`) defines `GoalEngine.calculate_defined_goal` at lines 20–172. It receives:
- a validated `GoalInput`;
- an asset lookup keyed by asset ID;
- version and latest-marker values;
- optional reference date.

It returns a `DefinedGoal` model.

## 2. Generic calculation path

Observed sequence in `calculate_defined_goal`:

1. Canonicalize goal type/name using `rules.goals` (lines 28–29).
2. Select request inflation or `DEFAULT_INFLATION_RATE` and label source `custom/default` (lines 31–36).
3. Compute duration from target month/year and reference date (lines 38–42).
4. Resolve and project every mapped asset (lines 45–87).
5. Calculate total projected mapped-asset value and a weighted funding return assumption (lines 88–91).
6. For retirement, calculate a retirement corpus; for all other types, inflate today's cost to target date (lines 93–123).
7. Calculate target-date funding gap/status (lines 124–127).
8. Calculate required monthly contribution (lines 128–133).
9. Put calculation metadata in `version_metadata` (lines 134–145).
10. Construct the `DefinedGoal` output (lines 146–172).

## 3. Duration and target calculation

Source: [backend/engines/goal/target_calculator.py](`https://github.com/Bhardwaj1-star/planvesto/blob/5a3b060e1b27915ede226f5173364e23dca1263e/backend/engines/goal/target_calculator.py#L1-L80`).

- `DEFAULT_INFLATION_RATE = 0.06` (line 4).
- `calculate_duration` (lines 7–18) calculates months between reference month and target month, returns zero for a negative interval, and rounds years to three decimal places.
- `calculate_future_target` (lines 20–27) delegates to `engines.calculation.canonical.calculate_goal_future_target`; if that returns `None`, it returns 0.
- The exact canonical inflation formula is in `backend/engines/calculation/canonical.py::calculate_goal_future_target`; this document does not duplicate its implementation.

## 4. Retirement branch

In `GoalEngine.calculate_defined_goal`, lines 93–116:
- reads `currentAge/current_age` and `lifeExpectancy/life_expectancy` from `dynamic_details`;
- if either is absent and status is not `Cancelled`, raises ValueError;
- for a cancelled goal only, missing current age defaults to 30 and life expectancy to 85;
- sets retirement return assumption to 0.08;
- uses `today_cost / 12` as current monthly expense passed into `calculate_retirement_corpus`;
- stores calculated retirement age and retirement years in metadata;
- sets funding return assumption to the retirement return.

The GoalService has an earlier enrichment layer at [backend/services/goal_service.py](`https://github.com/Bhardwaj1-star/planvesto/blob/5a3b060e1b27915ede226f5173364e23dca1263e/backend/services/goal_service.py#L38-L81`): for retirement only, it tries to derive missing current age from the first investor DOB for the planning unit and defaults missing life expectancy to 85. Explicit request values remain authoritative.

The target-calculator retirement formula at [target_calculator.py lines 30–80](`https://github.com/Bhardwaj1-star/planvesto/blob/5a3b060e1b27915ede226f5173364e23dca1263e/backend/engines/goal/target_calculator.py#L30-L80`) validates expense, ages and return; inflates annual expense to retirement; and values it as a finite growing annuity over the post-retirement period. This generic GoalEngine branch and the separate specialized-target module are distinct code paths.

## 5. Other goal types

For every non-retirement type in this engine, lines 117–123 call `calculate_future_target(today_cost, inflation_rate, duration_years)`. The generic engine does not dispatch to `calculate_specialized_target` in the inspected method.

Separate file: [backend/engines/goal/specialized.py](`https://github.com/Bhardwaj1-star/planvesto/blob/5a3b060e1b27915ede226f5173364e23dca1263e/backend/engines/goal/specialized.py#L1-L210`) defines `calculate_specialized_target` at lines 119–210 for retirement, education, vacation/travel and generic goal types. It contains specialized inputs/defaults such as education inflation 8% and travel inflation 6%. Its existence is verified, but its callers and runtime reachability are not established by this file alone. See [08 — Tests and evidence gaps](08-TESTS-AND-EVIDENCE-GAPS.md).

## 6. Calculation metadata

The generic engine writes:
- `asset_count`;
- `calculation_source = "GoalEngine"`;
- `funding_model` = `retirement_corpus` for retirement, otherwise `target_gap_plus_monthly_contribution`;
- `funding_return_assumption`;
- `required_monthly_contribution`;
- `dynamic_details`;
- for retirement, `retirement_age` and `retirement_years`.

These are stored under `DefinedGoal.version_metadata`; repository hydration uses metadata for several derived values.
