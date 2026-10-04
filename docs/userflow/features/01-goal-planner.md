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
