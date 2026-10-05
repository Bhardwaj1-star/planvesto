# Goal Planner

## 1. User Inputs

```text
User
└── Goal Planner
    ├── Goal identity
    │   ├── planning_unit_id
    │   ├── goal_id (optional for create/update)
    │   ├── goal_type
    │   └── goal_name
    │
    ├── Goal target
    │   ├── today_cost
    │   ├── target_month
    │   ├── target_year
    │   └── inflation_rate (optional)
    │
    ├── Goal preference
    │   ├── priority
    │   ├── flexibility
    │   └── status
    │
    ├── Existing assets for this goal (optional)
    │   └── asset_mappings
    │       ├── asset_id
    │       ├── allocation_type
    │       ├── allocation_value
    │       ├── expected_return (optional)
    │       └── return_frequency
    │
    └── Context
        ├── investor_id (optional)
        ├── dynamic_details
        └── specialized_data
```

## 2. Canonical Goal Identity

Goal taxonomy is owned by `backend/rules/goals.py`.

```text
Goal Input
└── canonical_goal_type()
    └── canonical_goal_name()
        └── DefinedGoal
```

Canonical goal types currently implemented — exactly 10:

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

Important identity rules:

- Goal types are exact canonical IDs; no aliases or legacy goal-type mappings are accepted.
- Unknown goal types are rejected by the backend request contract.
- Beneficiary, sub-purpose and circumstances belong in `dynamic_details` / `specialized_data`; they are not new goal types.

Canonical goal display names are also defined in `CANONICAL_GOAL_NAMES`.

## 3. Priority Contract

The canonical priority vocabulary is:

```text
critical / high / medium / low
```

`canonical_goal_priority()` owns the alias mapping:

- `must-have` → `critical`
- `important` → `high`
- `moderate` / `aspirational` → `medium`
- `nice-to-have` / `discretionary` → `low`

**Current code gap:** `GoalService.save_and_define_goal()` canonicalizes goal type/name but does not canonicalize `request.priority` before `ensure_goal_record()` / persistence. Therefore the document does not claim priority persistence is fully canonicalized yet.

## 4. Validation Contract

`backend/schemas/goals.py` currently enforces:

- `today_cost > 0`
- `target_month = 1..12`
- `target_year = 1900..2200`
- `inflation_rate = 0..1` when supplied
- `allocation_type = currency | percentage`
- percentage allocation cannot exceed 100
- expected return = `-0.99..1.0`
- return frequency = annual / semi-annual / semiannual / half-yearly / quarterly / monthly
- asset mappings are bounded by request schema size

Repository lookup constrains mapped assets to the same Planning Unit.

## 5. Goal Calculation Pipeline

```text
GoalInput
└── GoalEngine.calculate_defined_goal()
    ├── canonical goal type/name
    ├── inflation rate
    ├── duration_years
    ├── mapped asset projection
    ├── funding return assumption
    ├── future_target
    ├── funding_gap
    └── required_monthly_contribution
        ↓
    DefinedGoal
```

Generic target calculation:

```text
today_cost + inflation + duration
└── future_target

mapped assets + expected return + duration
└── projected_mapped_asset_value

future_target − projected_mapped_asset_value
└── funding_gap
    ├── > 0 → Shortfall
    ├── ≈ 0 → On Track
    └── < 0 → Overfunded
```

Funding status is owned by `backend/engines/goal/funding_gap.py` and the canonical calculation layer.

## 6. Asset Projection

Asset projection is owned by:

`backend/engines/goal/asset_projection.py`

When an expected return is not supplied, the code uses `DEFAULT_ASSET_RETURNS` with an explicit fallback of 8%.

Supported return-frequency normalization:

- monthly → 12
- quarterly → 4
- semi-annual / semiannual / half-yearly → 2
- annual → 1

The projection output contains:

- allocated amount
- allocated percentage
- projected value
- expected return
- return frequency

The default asset-return table is a code-level calculation dependency, not a frontend-owned assumption.

## 7. Retirement Calculation

Retirement uses a specialized corpus calculation inside the same Goal Engine.

```text
today_cost / 12
+ inflation
+ years_to_retirement
+ current_age
+ life_expectancy
+ retirement_return = 8%
└── calculate_retirement_corpus()
    ├── retirement_age
    ├── retirement_years
    └── future_target / required corpus
```

**Important current-code boundary:** `GoalService._enrich_retirement_context()` returns immediately; its older DOB-enrichment code is unreachable. Therefore current retirement calculation requires `currentAge` and `lifeExpectancy` in `dynamic_details`; the service does not currently auto-fill current age from investor DOB.

## 8. Goal Feasibility

Feasibility is owned by:

`backend/services/goal_service.py::_apply_feasibility()`

```text
DefinedGoal
└── FinancialStateService.get_current_snapshot()
    └── investable_surplus_monthly
        ├── unavailable → unknown
        ├── funding_gap <= 0 → feasible
        ├── required contribution <= surplus → feasible
        ├── surplus > 0 but insufficient → constrained
        └── no surplus → infeasible
```

The service also records:

- available monthly surplus
- required monthly contribution
- monthly contribution surplus gap
- reason
- funding strategies
- workflow readiness

Feasibility is a goal-funding/planning check. It is not Strategy Builder eligibility or strategy selection.

## 9. Preview vs Save

### Preview

POST `/api/goals/calculate`

```text
GoalInput
→ validation
→ GoalEngine calculation
→ feasibility
→ preview DefinedGoal
```

No DefinedGoal database snapshot is persisted by the preview path.

### Save

POST `/api/goals`

```text
GoalInput
→ canonical goal type/name
→ goal record upsert/creation
→ material-change check
→ GoalEngine calculation
→ feasibility
→ DefinedGoal snapshot
```

## 10. DefinedGoal Versioning

DefinedGoal is the versioned downstream goal snapshot.

```text
Goal
├── DefinedGoal v1
├── DefinedGoal v2
└── ...
```

The repository marks the previous latest snapshot as non-latest and inserts the new snapshot as latest.

**Current code gap:** `GoalRepository.has_material_change()` only checks:

- `today_cost`
- `target_month`
- `target_year`
- asset allocation type/value
- `dynamic_details`

It does not compare every persisted field, including:

- `inflation_rate`
- `priority`
- `flexibility`
- `status`
- asset expected return
- asset return frequency
- `specialized_data`

Therefore those fields are not yet fully represented in material-revision detection.

## 11. Revision → Strategy Boundary

When a material new DefinedGoal version is saved, current code calls:

`StrategyService.on_defined_goal_updated()`

to recalculate StrategyRun evaluation for the new goal version.

The old DefinedGoal remains historical.

The current StrategyVersion authority is separately protected by exact DefinedGoal binding; a selection whose DefinedGoal ID/version no longer matches the latest goal is rejected by StrategyRepository.

## 12. Ownership and Persistence

```text
Authenticated User
    ↓
Planning Unit
    ↓
Goal
    ↓
DefinedGoal version
    ↓
DefinedGoal asset mappings
```

Relevant ownership/persistence code:

- API validation/routes: `backend/api/goals.py`
- request schema: `backend/schemas/goals.py`
- persistence/versioning: `backend/data/goal_repository.py`
- model: `backend/models/defined_goal.py`
- calculation orchestration: `backend/engines/goal/engine.py`
- target calculation: `backend/engines/goal/target_calculator.py`
- asset projection: `backend/engines/goal/asset_projection.py`
- funding gap/contribution: `backend/engines/goal/funding_gap.py`
- taxonomy: `backend/rules/goals.py`
- feasibility: `backend/services/goal_service.py`

## 13. Final Goal Planner Output

```text
User Input
└── Canonical DefinedGoal
    ├── goal identity
    ├── target
    ├── duration
    ├── inflation
    ├── future target
    ├── mapped assets
    ├── projected mapped asset value
    ├── funding gap
    ├── funding status
    ├── required monthly contribution
    ├── feasibility status
    ├── feasibility reason
    └── DefinedGoal version
        ↓
    Downstream Strategy Planning
```

## 14. Regression Contract

### Identity

- legacy goal aliases resolve to canonical goal types;
- education is not a separate canonical goal type;
- Retirement and Financial Independence remain distinct;
- canonical goal names remain stable;
- priority alias normalization remains deterministic.

### Validation

- invalid target month/year is rejected;
- non-positive today cost is rejected;
- invalid inflation is rejected;
- invalid asset allocation is rejected;
- invalid expected return/frequency is rejected;
- foreign Planning Unit assets are rejected.

### Calculation

- duration is deterministic from target date/reference date;
- future target uses the selected/default inflation rate;
- mapped asset projection respects allocation and compounding frequency;
- funding gap returns the canonical funding status;
- required monthly contribution is deterministic;
- retirement requires current age and life expectancy and uses the retirement corpus calculation.

### Feasibility

- unavailable Financial State → unknown;
- fully funded goal → feasible;
- contribution within surplus → feasible;
- positive but insufficient surplus → constrained;
- zero available surplus → infeasible.

### Lifecycle

- preview does not persist a DefinedGoal snapshot;
- save persists a DefinedGoal snapshot;
- material revisions create new versions according to the current material-change implementation;
- latest DefinedGoal is the current goal snapshot.

## 15. Current Implementation Gaps

These are confirmed from the current code:

1. Goal priority has a canonical function, but save/persistence does not currently apply it before storing the priority.
2. Material-change detection does not cover all persisted goal fields.
3. Retirement DOB auto-enrichment is currently unreachable; required retirement context must be supplied in `dynamic_details`.
4. Specialized fields in `specialized_data` / `dynamic_details` are not automatically calculation-driving unless the Goal Engine explicitly consumes them.

## 16. Goal Planner End-to-End Contract

```text
USER INPUT
    ↓
SCHEMA VALIDATION
    ↓
CANONICAL GOAL TYPE / NAME
    ↓
GOAL CALCULATION
    ├── duration
    ├── future target
    ├── asset projection
    ├── funding return
    ├── funding gap
    └── required contribution
    ↓
CURRENT FINANCIAL STATE
    ↓
GOAL FEASIBILITY
    ├── feasible
    ├── constrained
    ├── infeasible
    └── unknown
    ↓
DEFINED GOAL SNAPSHOT
    ↓
VERSIONED GOAL
    ↓
STRATEGY PLANNING
```

Scope: this document is verified against the current Goal Planner backend contracts and records only code-supported behavior or explicitly confirmed implementation gaps.