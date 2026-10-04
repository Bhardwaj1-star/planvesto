# Financial Health & Rules

## 1. Feature Scope

Financial Health & Rules constructs the current authoritative Financial State from Planning Unit financial records, exposes canonical financial calculations, builds the MoneyWheel diagnostic contract, and evaluates financial constraints.

```text
Planning Unit Financial Records
└── FinancialStateService
    └── Current FinancialState
        ├── income / expenses / surplus
        ├── assets / liquidity
        ├── liabilities / debt burden
        ├── net worth
        └── derived financial facts
            └── MoneyWheel
                ├── 9 canonical ratios
                └── 2 canonical coverage rules
                    └── Constraint evaluation
                        └── Planning evidence
```

It does not own Goal definition or Strategy selection.

## 2. Request Inputs

Financial State is scoped by:

- `planning_unit_id`
- `scope = family | individual`
- `investor_id` when scope is individual

Validation is owned by `FinancialStateService._validate_context()`.

Rules:

- Planning Unit ID is required.
- Individual scope requires investor ID.
- Family scope rejects investor ID.
- Individual investor must belong to the Planning Unit.

The service reads:

- investors
- income
- expenses
- assets
- liabilities
- asset ownership
- liability responsibility
- expense participation

## 3. FinancialState Authority

The current Financial State authority is:

`backend/services/financial_state_service.py`

```text
Raw Planning Unit Records
        ↓
FinancialStateService._inputs()
        ↓
FinancialStateService._revision()
        ↓
FinancialStateEngine.build()
        ↓
FinancialState snapshot
        ↓
Current FinancialState
```

The client does not own the complete derived Financial State.

Missing source data remains unavailable; the service must not silently convert missing derived facts into authoritative zero values.

## 4. Freshness / Snapshot Contract

Current code computes a deterministic raw-input revision using SHA-256 over normalized financial-state inputs.

```text
Current raw records
└── _revision()
    └── input_revision
        ↓
latest stored snapshot
    ├── same revision + valid context
    │   └── reuse
    └── changed revision / invalid lineage
        └── rebuild and save
```

A reusable snapshot must match:

- Planning Unit
- scope
- investor context
- stored `input_revision`
- FinancialState context

Action-completion snapshots additionally require valid:

- action ID
- StrategyVersion ID
- completed action record
- snapshot lineage

Therefore the current service-level FinancialState path is revision-aware; a stale snapshot is rebuilt rather than treated as current.

## 5. Canonical Calculation Layer

Shared financial mathematics is owned by:

`backend/engines/calculation/canonical.py`

The canonical calculation layer provides pure calculations and `DerivedFact` outputs.

Canonical formulas currently implemented:

- **Savings Rate** = Monthly Surplus / Monthly Income × 100
- **Liquid Asset Ratio** = Liquid Assets / Total Assets × 100
- **Expense Coverage** = Liquid Assets / Monthly Expenses
- **Emergency Coverage** = Liquid Assets / Essential Monthly Expenses
- **DTI** = Monthly Debt Payments / Gross Monthly Income × 100, with ratio form also supported
- **Leverage Ratio** = Total Liabilities / Total Assets × 100
- **Financial Asset Ratio** = Financial Assets / Total Assets × 100
- **Insurance Coverage Ratio** = Existing Sum Assured / Required Insurance Cover × 100
- **Goal Funding Ratio** = Current Goal Funding / Goal Target Amount × 100
- **Future Funding Ratio** = Projected Goal Funding / Future Goal Target × 100
- **Required Rate of Return** = ((Future Goal Target / Current Goal Funding)^(1 / Duration) − 1) × 100

The canonical layer also contains other derived calculations, but only the MoneyWheel contract is listed below as the feature's canonical 9+2 contract.

```text
FinancialState
└── canonical.py
    └── mathematical result / DerivedFact
        ├── MoneyWheel classification
        └── Constraint interpretation
```

Calculation ownership and decision authority are separate. Consumers must not implement competing versions of the same formula.

## 6. MoneyWheel Canonical Contract

### Canonical ratios

1. `savings_rate`
2. `liquid_asset_ratio`
3. `debt_to_income_ratio`
4. `leverage_ratio`
5. `financial_asset_ratio`
6. `insurance_coverage_ratio`
7. `goal_funding_ratio`
8. `future_funding_ratio`
9. `required_rate_of_return`

### Canonical rules

1. `expense_coverage`
2. `emergency_coverage`

The coverage rules are distinct:

- Expense Coverage = liquid assets / monthly expenses
- Emergency Coverage = liquid assets / essential monthly expenses

`current_liquidity_ratio` is **not** a synonym for `liquid_asset_ratio`. It is a compatibility definition with a different formula:

`Liquid Assets / Short-Term Liabilities`.

## 7. MoneyWheel Threshold Ownership

MoneyWheel classification is owned by:

`backend/rules/moneywheel.py`

Current canonical classification bands include:

- Savings Rate: excellent ≥30%, healthy 20–<30%, attention 10–<20%, critical <10%
- Liquid Asset Ratio: excellent ≥25%, healthy 15–<25%, attention 10–<15%, critical <10%
- DTI: excellent <20%, healthy 20–<30%, attention 30–<40%, critical ≥40%
- Leverage: excellent <20%, healthy 20–<30%, attention 30–<50%, critical ≥50%
- Financial Asset Ratio: excellent ≥70%, healthy 50–<70%, attention 30–<50%, critical <30%
- Insurance Coverage: excellent ≥80%, healthy 60–<80%, attention 40–<60%, critical <40%
- Goal Funding: excellent ≥100%, healthy 80–<100%, attention 50–<80%, critical <50%
- Future Funding: same 100/80/50 boundaries
- Required Rate of Return: excellent <8%, healthy 8–<12%, attention 12–<15%, critical ≥15%
- Emergency / Expense Coverage: excellent ≥9 months, healthy 6–<9, attention 3–<6, critical <3

Thresholds are rule policy, not mathematical formula definitions.

## 8. Compatibility / Alias Boundary

`canonicalize_metric_key()` is the compatibility normalizer.

Current legacy mappings:

- `savings_ratio` → `savings_rate`
- `liquid_asset_to_total_asset` → `liquid_asset_ratio`
- `insurance_gap_ratio` → `insurance_coverage_ratio`
- `emergency_fund_coverage` → `emergency_coverage`

Compatibility-only definitions currently retained include:

- `emergency_fund_coverage`
- `current_liquidity_ratio`
- `expense_ratio`
- `solvency_ratio`

These are not additional canonical MoneyWheel concepts. New business logic must use canonical keys.

## 9. Constraint Boundary

Constraint evaluation is owned by:

`backend/engines/constraints/evaluator.py`

Current ratio evaluation consumes the canonical calculation functions for:

- savings rate
- emergency coverage
- DTI
- leverage

The evaluator also resolves monthly income/expenses and essential monthly expenses from its financial context.

```text
Canonical Metric
    ↓
MoneyWheel Classification
    ↓
Constraint Evaluator
    ├── hard constraint
    ├── warning
    └── no constraint consequence
```

A critical metric is not automatically equivalent to goal infeasibility.

## 10. Current Constraint Consequences

Current code implements:

### Emergency coverage

- critical (<3 months): hard constraint for high/critical discretionary goals; suggested priority may be reduced to low.
- attention (3–<6 months): warning.

### DTI

- critical (≥40%): hard constraint for high/critical discretionary goals; suggested priority may be reduced to low.
- attention (30–<40%): warning.

### Savings rate

- critical or attention: warning.

Constraint severity and MoneyWheel classification are separate concepts.

## 11. FinancialPlanService Duplicate Surface

There is a **confirmed remaining duplicate calculation surface** in:

`backend/services/financial_plan_service.py`

Its MoneyWheel health scan currently calculates:

- DTI as outstanding liabilities / annual income
- emergency coverage as `(financial_assets * 0.2) / monthly_expenses`

These are not the canonical formulas.

Therefore this feature document must **not** describe FinancialPlanService's scan as authoritative MoneyWheel calculation.

Required architectural boundary:

```text
Canonical calculation layer
└── owns financial formulas

MoneyWheel rules
└── owns classification thresholds

FinancialPlanService
└── must consume canonical facts
    └── must not redefine DTI/emergency coverage
```

This is a current implementation gap, not a documentation decision.

## 12. Financial State → Downstream Boundary

```text
FinancialStateService
├── Goal Planner feasibility
├── MoneyWheel
├── Constraint evaluation
├── Risk / suitability context
├── Strategy Builder financial context
├── Reports
└── Multi-goal planning
```

Downstream consumers consume Financial State and canonical facts. They do not become alternate owners of FinancialState construction.

## 13. D1 Action-Completion Boundary

Current FinancialStateService also supports D1 actual-state persistence.

```text
Completed Action
    +
client-submitted actual_state
    +
source snapshot
    +
expected input revision
    +
StrategyVersion/action lineage
        ↓
FinancialStateService.save_actual_state()
        ↓
action_completion snapshot
```

The submitted state is validated as a FinancialState and accepted only when the expected raw-input revision and source snapshot still match.

This is a lifecycle write path, not a second FinancialState calculation owner.

## 14. Code Ownership

- Financial State service: `backend/services/financial_state_service.py`
- Financial State engine: `backend/engines/financial_state/engine.py`
- Financial State snapshot repository: `backend/data/financial_state_repository.py`
- Canonical calculations: `backend/engines/calculation/canonical.py`
- MoneyWheel engine: `backend/engines/moneywheel/engine.py`
- MoneyWheel rules / aliases: `backend/rules/moneywheel.py`
- Constraint evaluation: `backend/engines/constraints/evaluator.py`
- Constraint thresholds / rule IDs: `backend/rules/constraints.py`
- Financial State model: `backend/models/financial_state.py`

## 15. Regression Contract

### FinancialState authority

- current state is built from Planning Unit records;
- scope and ownership are validated;
- raw-input revision is checked before reusing a snapshot;
- changed raw inputs force rebuild;
- action-completion snapshots retain lineage.

### Canonical calculations

- identical inputs produce identical canonical results;
- missing required inputs remain unavailable;
- DTI uses monthly debt payments / gross monthly income;
- emergency coverage uses liquid assets / essential monthly expenses;
- liquid asset ratio remains distinct from current liquidity ratio.

### MoneyWheel

- exactly 9 canonical ratios are exposed;
- exactly 2 canonical coverage rules are exposed;
- aliases normalize to canonical keys;
- canonical thresholds remain deterministic.

### Constraints

- emergency critical/attention behavior remains distinct;
- DTI critical/attention behavior remains distinct;
- savings-rate attention/critical produces warning evidence;
- MoneyWheel classification does not automatically become goal infeasibility.

### Duplicate protection

- FinancialPlanService must not introduce alternate DTI/emergency formulas;
- downstream consumers should use canonical calculation/fact outputs.

## 16. Current Implementation Gaps

Confirmed from current code:

1. FinancialPlanService still contains duplicate DTI and emergency-coverage calculations.
2. Compatibility definitions remain in `rules/moneywheel.py`; they must stay boundary-only.
3. Constraint evaluation has fallback context extraction for legacy field names; canonical upstream FinancialState should remain the preferred source.
4. Threshold ownership is purpose-specific: identical metric semantics may share classification policy, but distinct business consequences remain in their rule owner.

## 17. Final Financial Health Contract

```text
PLANNING UNIT RECORDS
    ↓
FINANCIALSTATESERVICE
    ↓
CURRENT FINANCIALSTATE
    ↓
CANONICAL CALCULATIONS
    ↓
MONEYWHEEL
    ├── 9 ratios
    └── 2 coverage rules
    ↓
CONSTRAINT EVALUATION
    ├── hard
    ├── warning
    └── diagnostic evidence
    ↓
GOAL / STRATEGY / REPORT / MULTI-GOAL CONSUMERS
```

Scope: this document is verified against the current Financial Health, canonical calculation, MoneyWheel and constraint code. Confirmed duplicate implementation gaps are explicitly retained as gaps rather than presented as canonical behavior.