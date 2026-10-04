# Goal Planner

## 1. User Inputs

```text
User
└── Goal Planner
    ├── Goal identity
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
        ├── planning_unit_id
        ├── investor_id (optional)
        ├── dynamic_details
        └── specialized_data
```

## 2. Canonical Rules

```text
Goal Input
└── Canonicalization
    ├── goal_type → canonical_goal_type()
    │   └── e.g. "child education" → "education"
    ├── goal_name → canonical_goal_name()
    └── priority → canonical_goal_priority()
        └── Canonical priority:
            critical / high / medium / low
```

Other input rules enforced in code:

- `today_cost > 0`
- `target_month = 1..12`
- `target_year = 1900..2200`
- `inflation_rate = 0..100%` when supplied
- asset allocation type = `currency` or `percentage`
- percentage allocation cannot exceed 100%
- asset expected return = `-99%..100%` when supplied
- asset return frequency = annual / semi-annual / quarterly / monthly variants
- mapped asset must belong to the same Planning Unit

## 3. Goal Calculations

```text
Goal Inputs
└── Duration
    └── target date − reference date
        └── duration_years

Duration + today_cost + inflation
└── Future Target
    └── future_target

Mapped Assets
└── Asset Projection
    ├── allocated_amount
    ├── allocated_percentage
    └── projected_value

Mapped Asset Returns
└── Weighted Funding Return
    └── funding_return_assumption

Future Target − Projected Mapped Assets
└── funding_gap
    ├── > 0 → Shortfall
    ├── ≈ 0 → On Track
    └── < 0 → Overfunded

Funding Gap + return assumption + duration
└── required_monthly_contribution
```

### Retirement-specific calculation

For `retirement`, the code uses a separate retirement-corpus calculation:

```text
Current monthly expense
+ current age
+ life expectancy
+ years to retirement
+ inflation
+ retirement return assumption (8%)
└── retirement corpus / future_target
```

For other goal types, the generic future-target calculation is used.

## 4. Feasibility Rules

Feasibility is a **goal-funding check**, not a strategy decision.

```text
Defined Goal
└── Current Financial State
    └── investable_surplus_monthly
        ├── Financial State unavailable
        │   └── feasibility = unknown
        │
        └── Financial State available
            ├── funding_gap <= 0
            │   └── feasible
            │
            ├── required_monthly_contribution <= surplus
            │   └── feasible
            │
            ├── surplus > 0
            │   └── constrained
            │
            └── surplus <= 0
                └── infeasible
```

The feasibility result also records:

- available monthly surplus
- required monthly contribution
- monthly contribution surplus gap
- reason
- funding strategies

## 5. Final Goal Planner Output

```text
User Input
└── Canonical DefinedGoal
    ├── Goal identity
    ├── Target
    ├── Funding projection
    ├── funding_gap
    ├── funding_status
    ├── required_monthly_contribution
    └── feasibility_status
        ├── feasible
        ├── constrained
        ├── infeasible
        └── unknown
            └── Goal becomes input for downstream strategy planning
```

## Code Ownership

- Input contract: `backend/schemas/goals.py`
- Goal calculation orchestration: `backend/engines/goal/engine.py`
- Target/duration calculation: `backend/engines/goal/target_calculator.py`
- Asset projection: `backend/engines/goal/asset_projection.py`
- Funding gap/contribution: `backend/engines/goal/funding_gap.py`
- Goal taxonomy/priority rules: `backend/rules/goals.py`
- Feasibility: `backend/services/goal_service.py::_apply_feasibility()`
- Goal Planner UI: `frontend/app/investor/goal-planner/page.tsx`


## 6. Input Source Boundary

Goal Planner combines three sources:

| Source | Examples | Authority |
|---|---|---|
| User goal input | goal type, target, priority, flexibility, inflation | Goal Planner request |
| Existing financial data | assets, liabilities, Financial State, investable surplus | Existing Planning Unit / Financial State |
| Goal context | specialized data, dynamic details | Goal Planner request |

Goal Planner owns goal definition and goal-specific funding calculation. It consumes Financial State for feasibility but must not become a competing owner of Financial State metrics.

---

## 7. Input Consumption Boundary

Every Goal Planner input must be classified as calculation-driving, canonical/decision, or contextual.

### Calculation-driving inputs

- goal_type
- today_cost
- target_month
- target_year
- inflation_rate
- asset_mappings: asset, allocation type/value, expected return, return frequency
- retirement dynamic details used by the retirement-corpus calculation: current age, life expectancy, desired retirement monthly expense

### Canonical / decision inputs

- goal_name
- priority
- flexibility
- status
- goal_type

### Contextual / specialized inputs

The current UI exposes additional fields for education beneficiary, marriage beneficiary, home location, vehicle type/condition, travel frequency/geography, selected liability, legacy contribution, passive-income target, wealth target and other specialized metadata.

These must not automatically be treated as calculation inputs merely because the UI collects them. A field is calculation-driving only when an explicit backend calculation consumer exists.

---

## 8. Specialized Goal Planner Inputs

The current Goal Planner UI exposes:

- retirement: life expectancy, desired lifestyle monthly expense
- financial independence: desired passive income amount
- education: beneficiary
- marriage: beneficiary
- home: preferred location
- vehicle: vehicle type and condition
- travel: frequency and domestic/international
- wealth creation: target wealth/corpus
- debt freedom: selected liability
- legacy giving: contribution amount

Important boundary: specialized UI data and generic Goal Engine calculations are not automatically equivalent. Any specialized field not explicitly consumed by the calculation layer remains contextual metadata until its calculation semantics are implemented.

---

## 9. Preview vs Save Lifecycle

### Calculate / Preview

POST /api/goals/calculate

User input
→ validation
→ goal calculation
→ preview result

Preview calculates the goal but does not persist a DefinedGoal snapshot.

### Save

POST /api/goals

User input
→ ownership validation
→ canonicalization
→ goal calculation
→ persistence
→ DefinedGoal version snapshot

The persisted DefinedGoal is the versioned goal definition consumed by downstream planning.

---

## 10. Goal Versioning and Revision Boundary

DefinedGoal is versioned.

Goal
├── DefinedGoal v1
│   └── historical
├── DefinedGoal v2
│   └── current
└── ...

When a material goal change occurs:

1. the previous DefinedGoal remains history;
2. a new DefinedGoal version is created;
3. downstream planning uses the new current goal version;
4. old strategy/action state must not silently become current for the revised goal.

### Current material-change implementation

The repository currently checks:

- today_cost
- target_month
- target_year
- asset mapping allocation type/value
- dynamic_details

The current check does not visibly include every persisted goal field, including:

- inflation_rate
- priority
- flexibility
- status
- asset expected_return
- asset return_frequency
- specialized_data

This is an implementation gap that must be explicitly resolved before declaring goal-revision semantics final.

---

## 11. Ownership and Persistence Boundary

Ownership chain:

Authenticated User
    ↓
Planning Unit
    ↓
Goal
    ↓
DefinedGoal version
    ↓
Asset mappings

The Goal API validates:

- Planning Unit ownership
- investor ownership when supplied
- mapped asset ownership / Planning Unit membership

Code ownership:

- Input contract: backend/schemas/goals.py
- API validation/routes: backend/api/goals.py
- Goal persistence/versioning: backend/data/goal_repository.py
- Goal model: backend/models/defined_goal.py
- Goal calculation: backend/engines/goal/*
- Goal taxonomy/priority: backend/rules/goals.py
- Feasibility: backend/services/goal_service.py::_apply_feasibility()
- UI: frontend/app/investor/goal-planner/page.tsx

---

## 12. Final Goal Planner Output Contract

User Input
└── Canonical DefinedGoal
    ├── Goal identity
    ├── Target
    ├── Duration
    ├── Future target
    ├── Funding projection
    ├── funding_gap
    ├── funding_status
    ├── required_monthly_contribution
    ├── mapped assets
    └── feasibility_status
        ├── feasible
        ├── constrained
        ├── infeasible
        └── unknown
            └── Downstream Strategy Planning

The output must be sufficient to identify what the goal is, what it costs today, when it is required, what it is expected to cost in the future, what assets are mapped, what funding gap exists, what monthly contribution is required, whether it is currently fundable, and which DefinedGoal version is current.

---

## 13. Goal Planner Regression Contract

Tests should protect these invariants.

### Identity

- goal-type aliases canonicalize to one canonical goal type;
- child education does not become a separate canonical goal type;
- retirement remains distinct from financial independence;
- priority canonicalizes to critical/high/medium/low.

### Validation

- invalid target month/year is rejected;
- non-positive today_cost is rejected;
- invalid inflation is rejected;
- invalid allocation type is rejected;
- percentage allocation above 100% is rejected;
- invalid expected return/frequency is rejected;
- foreign Planning Unit assets are rejected.

### Calculation

- duration is deterministic from target date;
- future target uses the applicable inflation assumption;
- mapped asset projections respect allocation and return frequency;
- funding gap produces the correct funding status;
- required monthly contribution is deterministic;
- retirement uses retirement-specific corpus logic.

### Feasibility

- missing Financial State → unknown;
- fully funded goal → feasible;
- required contribution within surplus → feasible;
- positive but insufficient surplus → constrained;
- zero/negative surplus → infeasible.

### Lifecycle

- preview does not persist a DefinedGoal snapshot;
- save persists the goal/DefinedGoal state;
- material goal revision creates a new version;
- historical versions remain history;
- current planning reads the current DefinedGoal version.

### Ownership

- Planning Unit ownership is enforced;
- investor ownership is enforced when applicable;
- mapped assets cannot cross Planning Unit boundaries.

---

## 14. Current Implementation Gaps

These are code-backed gaps, not new product assumptions.

1. Priority canonicalization exists through canonical_goal_priority(), but save_and_define_goal() must be verified to normalize priority before persistence.
2. Material-change detection does not visibly cover every persisted goal field. Revision semantics need an explicit final contract.
3. Specialized UI inputs are broader than the currently explicit generic calculation path. Calculation-driving vs contextual fields must remain clearly separated.
4. Default asset-class return assumptions exist in the calculation layer. They should have one authoritative owner and must not be duplicated in UI/business-rule code.
5. Goal Planner owns funding and feasibility; Strategy Builder owns downstream strategy eligibility and strategy decision.

---

## 15. Goal Planner End-to-End Contract

USER INPUT
    ↓
API VALIDATION
    ↓
CANONICALIZATION
    ↓
GOAL CALCULATION
    ├── duration
    ├── future target
    ├── asset projection
    ├── funding return
    ├── funding gap
    └── required contribution
    ↓
FINANCIAL STATE DEPENDENCY
    ↓
FEASIBILITY
    ├── feasible
    ├── constrained
    ├── infeasible
    └── unknown
    ↓
DEFINED GOAL SNAPSHOT
    ↓
VERSIONED GOAL
    ↓
DOWNSTREAM STRATEGY PLANNING

Scope: this update is limited to Goal Planner. Other feature documents are intentionally untouched.
