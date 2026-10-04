# Financial Health & Rules

## 1. Feature Scope

Financial Health & Rules builds the authoritative Financial State from Planning Unit records, computes canonical financial measures, classifies MoneyWheel ratios/rules, and evaluates planning constraints.

```text
Planning Unit Financial Records
└── Financial State
    └── Canonical Calculations
        ├── Cash flow / savings
        ├── Assets / liquidity
        ├── Liabilities / debt burden
        ├── Net worth
        ├── Coverage measures
        └── Goal funding / required return
            └── MoneyWheel ratios
                └── MoneyWheel rules
                    └── Constraint evaluation
                        └── Diagnostic / planning evidence
                            └── Downstream planning
```

The feature owns financial-state construction, shared financial mathematics, MoneyWheel classification, and constraint evaluation boundaries. It does not own goal definition, strategy selection, or downstream strategy decisions.

## 2. User / Request Inputs

Financial Health is driven by:

- `planning_unit_id`
- `scope`: family or individual
- `investor_id`: required for individual scope and invalid for family scope

The service reads the underlying Planning Unit records required to construct the current state:

- investors
- income
- expenses
- assets
- liabilities
- ownership
- liability responsibility
- expense participation

The client does not submit the complete derived Financial State as authoritative calculation input.

## 3. Input Source / Authority Boundary

| Source | Examples | Authority |
|---|---|---|
| Planning Unit financial records | income, expenses, assets, liabilities | Existing Planning Unit data |
| Ownership/context | Planning Unit, scope, investor | FinancialStateService validation |
| Derived financial state | monthly income, expenses, surplus, assets, liabilities, net worth | FinancialStateService |
| MoneyWheel calculations | canonical ratios/rules | Calculation + MoneyWheel rule owners |
| Constraint policy | hard/warning/diagnostic consequences | Constraint rule owner |

FinancialStateService is the current Financial State authority.

A FinancialState snapshot is reusable only when its:

- raw-input revision
- Planning Unit
- scope
- investor context
- authority lineage

remain valid.

Changed raw inputs force a rebuild.

MoneyWheel must read the current backend Financial State rather than treating a client-provided snapshot as authoritative.

## 4. Input Consumption Boundary

Every input consumed by Financial Health must have a defined semantic role.

### State-building inputs

These establish the Financial State:

- income records
- expense records
- asset records
- liability records
- investor/Planning Unit ownership context
- liability responsibility
- expense participation

### Calculation-driving state

The Financial State supplies the inputs needed for:

- monthly/annual income and expenses
- investable surplus
- assets and liquidity
- liabilities / EMI burden
- net worth
- cash-flow / savings measures
- safety reserve
- MoneyWheel ratios
- goal funding and required-return calculations where applicable

### Context / scope inputs

- planning_unit_id
- scope
- investor_id

These determine ownership and calculation scope; they are not themselves financial measures.

Missing source data remains unavailable. It must not silently become zero.

## 5. Canonical Rules and Calculations

Shared financial mathematics is owned by:

`backend/engines/calculation/canonical.py`

Canonical calculations currently documented by the system are:

- **Savings Rate** = Monthly Surplus / Monthly Income × 100
- **Liquid Asset Ratio** = Liquid Assets / Total Assets × 100
- **Expense Coverage** = Liquid Assets / Monthly Expenses
- **Emergency Coverage** = Liquid Assets / Essential Monthly Expenses
- **DTI** = Monthly Debt Payments / Gross Monthly Income × 100
- **Leverage** = Total Liabilities / Total Assets × 100
- **Financial Asset Ratio** = Financial Assets / Total Assets × 100
- **Insurance Coverage Ratio** = Existing Sum Assured / Required Insurance Cover × 100
- **Goal Funding Ratio** = Current Goal Funding / Goal Target Amount × 100
- **Future Funding Ratio** = Projected Goal Funding / Future Goal Target × 100
- **Required Rate of Return** = ((Future Goal Target / Current Goal Funding)^(1/Duration) - 1) × 100

These are calculations, not business decisions.

Calculation results preserve availability/reason information. Missing source data must remain unavailable rather than being silently converted to zero.

### Calculation ownership boundary

```text
Financial State
└── calculation/canonical.py
    └── Mathematical result
        └── MoneyWheel rule classification
            └── Constraint interpretation
```

Consumers must not create competing implementations of these canonical formulas.

## 6. MoneyWheel Canonical Contract

MoneyWheel has one canonical contract:

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

Expense Coverage and Emergency Coverage are distinct.

- Expense Coverage = liquid assets / monthly expenses
- Emergency Coverage = liquid assets / essential monthly expenses

Emergency coverage is therefore not another name for expense coverage.

### Rule classification

Current emergency bands:

- excellent: ≥ 9 months
- healthy: 6–<9 months
- attention: 3–<6 months
- critical: <3 months

MoneyWheel ratios use excellent/healthy/attention/critical bands where defined.

The boundary is:

```text
Calculation
└── mathematical result

Rule
└── threshold / classification interpretation

Constraint
└── business consequence for planning
```

A critical ratio does not automatically make every goal infeasible.

Current explicit hard/warning consequences cover emergency coverage, DTI and savings-rate.

## 7. Canonicalization / Compatibility Boundary

Metric aliases normalize through:

`canonicalize_metric_key()`

Known compatibility mappings include:

- `savings_ratio` → `savings_rate`
- `liquid_asset_to_total_asset` → `liquid_asset_ratio`
- `insurance_gap_ratio` → `insurance_coverage_ratio`
- `emergency_fund_coverage` → `emergency_coverage`

Compatibility vocabulary is not a second business concept.

The canonical key is the only key that should be used for new business logic. Legacy aliases exist only at compatibility boundaries where required.

## 8. Lifecycle / State Transitions

```text
Raw Planning Unit Records
    ↓
FinancialStateService
    ↓
Authoritative FinancialState Snapshot
    ↓
Canonical Financial Calculations
    ↓
MoneyWheel Ratios
    ↓
MoneyWheel Rule Classification
    ↓
Constraint Evaluation
    ↓
Diagnostic / Planning Evidence
    ↓
Goal / Strategy / Planning Consumers
```

When source revisions change, the authoritative Financial State snapshot is rebuilt.

Current-state selection is based on source revision and ownership scope, not on a client-provided snapshot alone.

## 9. Financial State Output Contract

The Financial State output must represent the current authoritative financial condition for the requested Planning Unit scope.

It includes, where source data is available:

- monthly/annual income
- monthly/annual expenses
- investable surplus
- assets
- liquid assets / liquidity
- liabilities
- EMI / debt burden
- net worth
- cash-flow / savings measures
- safety reserve
- revision / lineage context
- availability / reason information for unavailable derived values

FinancialState is the authoritative state consumed by downstream financial planning.

It is distinct from the MoneyWheel output.

## 10. MoneyWheel Output Contract

```text
Current FinancialState
└── Canonical MoneyWheel Output
    ├── 9 canonical ratios
    ├── 2 canonical rules
    ├── ratio classifications
    ├── rule classifications
    ├── diagnostic evidence
    └── applicable constraint consequences
```

The MoneyWheel output must preserve the distinction between:

- calculated value
- classification/status
- business constraint consequence

A MoneyWheel classification is not itself a goal-feasibility result.

## 11. Constraint Output Boundary

Constraint evaluation consumes canonical financial measures and rule classifications.

It may produce:

- hard constraints
- warning constraints
- diagnostics
- supporting evidence

Constraint evaluation does not own the underlying mathematical formulas.

Constraint consequences are business policy. They must not be duplicated inside calculation code or UI code.

## 12. Code Ownership

- API: `backend/api/financial_state.py`
- Financial State authority/freshness: `backend/services/financial_state_service.py`
- Financial State engine/model/schema: `backend/engines/financial_state/engine.py`, `backend/models/financial_state.py`, `backend/schemas/financial_state.py`
- Shared calculations: `backend/engines/calculation/canonical.py`
- Calculation exports: `backend/engines/calculation/__init__.py`
- MoneyWheel API: `backend/api/moneywheel.py`
- MoneyWheel engine: `backend/engines/moneywheel/engine.py`
- MoneyWheel rules / aliases: `backend/rules/moneywheel.py`
- Constraint policy: `backend/rules/constraints.py`
- Constraint evaluation: `backend/engines/constraints/evaluator.py`
- Downstream strategy consumers: Strategy Builder / planning services; they consume the outputs and do not redefine the canonical financial formulas.

## 13. Downstream Dependency Boundary

Financial Health & Rules provides evidence to:

```text
Financial Health & Rules
├── Goal Planner
│   └── goal-level feasibility
│
├── Strategy Builder
│   ├── financial context
│   ├── constraint evidence
│   ├── risk / suitability evidence
│   └── strategy decision inputs
│
├── MoneyWheel UI
│   └── ratios / rules / classifications
│
└── Multi-goal / downstream planning
    └── financial decision context
```

Downstream consumers may consume canonical outputs, but must not reimplement the same mathematical definitions.

## 14. Versioning / State Authority

FinancialState snapshots carry revision and lineage context.

The current state is determined by:

- Planning Unit ownership
- scope
- investor context
- source/raw-input revision
- FinancialState authority lineage

A client-provided historical snapshot cannot override the current authoritative Financial State.

When an action completion submits an actual state, that path is subject to the system's explicit FinancialState authority/freshness validation and current-snapshot requirements.

## 15. Regression Contract

Tests must protect these invariants.

### Authority

- FinancialStateService remains the current Financial State authority.
- stale source revisions do not remain current.
- client snapshots cannot silently override current state.
- scope and ownership boundaries remain enforced.

### Calculations

- canonical formulas remain centralized;
- savings rate uses the canonical definition;
- liquid asset ratio remains distinct from current liquidity;
- DTI uses the canonical debt-payment/income definition;
- emergency coverage uses essential monthly expenses;
- expense coverage remains distinct from emergency coverage;
- unavailable inputs remain unavailable rather than becoming zero.

### MoneyWheel

- exactly the canonical nine ratios remain authoritative;
- exactly the two canonical rules remain authoritative;
- aliases normalize to canonical keys;
- emergency coverage remains distinct from expense coverage;
- ratio classification remains separate from constraint consequence.

### Constraints

- constraint evaluation consumes canonical outputs;
- hard/warning/diagnostic consequences remain policy-owned;
- a critical financial ratio does not automatically equal goal infeasibility.

### Lifecycle

- changed raw inputs rebuild the authoritative FinancialState;
- current state is selected from valid revision/lineage context;
- downstream consumers use current state.

## 16. Known Implementation Notes / Gaps

These are implementation observations already identified by the system documentation/audit:

1. Liquidity breakdown depends on available asset classification.
2. FinancialState does not store every MoneyWheel ratio; MoneyWheel derives canonical output separately.
3. Not every MoneyWheel ratio is currently a hard constraint.
4. Legacy snapshot normalization is compatibility behavior, not a second contract.
5. Canonical metric aliases remain in compatibility paths and must not become competing business vocabulary.
6. Parallel metric calculations / threshold bands identified by the broader audit require continued verification so that shared mathematics remains centralized and purpose-specific thresholds remain owned by their respective rule/policy layer.

These are implementation points, not new product decisions.

## 17. Important Semantic Boundaries

1. **FinancialState ≠ MoneyWheel output**
2. **Calculation ≠ Rule**
3. **Rule ≠ Constraint**
4. **Ratio status ≠ Goal feasibility**
5. **Client snapshot ≠ authoritative current FinancialState**
6. **Compatibility alias ≠ canonical metric**
7. **Current FinancialState ≠ historical FinancialState snapshot**
8. **Financial Health evidence ≠ Strategy decision**
9. **Financial Health constraint evidence ≠ strategy eligibility by itself**

These boundaries prevent downstream features from becoming competing owners of financial semantics.

## 18. Final Financial Health & Rules Output

```text
Planning Unit Financial Records
    ↓
Authoritative FinancialState
    ├── Income / Expenses
    ├── Investable Surplus
    ├── Assets / Liquidity
    ├── Liabilities / EMI
    ├── Net Worth
    └── Safety Reserve
    ↓
Canonical Calculations
    ├── savings_rate
    ├── liquid_asset_ratio
    ├── debt_to_income_ratio
    ├── leverage_ratio
    ├── financial_asset_ratio
    ├── insurance_coverage_ratio
    ├── goal_funding_ratio
    ├── future_funding_ratio
    └── required_rate_of_return
    ↓
Canonical Rules
    ├── expense_coverage
    └── emergency_coverage
    ↓
Classification / Diagnostics
    ↓
Constraint Evaluation
    ├── hard constraints
    ├── warnings
    └── diagnostics
    ↓
Downstream Planning
    ├── Goal feasibility
    ├── Strategy decision evidence
    ├── MoneyWheel UI
    └── Multi-goal / planning context
```

The final output must make clear:

- what the current Financial State is;
- which canonical calculations were available;
- which MoneyWheel ratios/rules were derived;
- how those ratios/rules were classified;
- which constraint consequences apply;
- what evidence is available to downstream planning;
- and which authority owns each layer.

## 19. Financial Health & Rules End-to-End Contract

RAW PLANNING UNIT RECORDS
    ↓
OWNERSHIP / SCOPE VALIDATION
    ↓
FINANCIAL STATE CONSTRUCTION
    ↓
AUTHORITATIVE FINANCIALSTATE SNAPSHOT
    ↓
CANONICAL CALCULATIONS
    ├── income / expenses
    ├── surplus
    ├── liquidity / assets
    ├── liabilities / debt burden
    ├── net worth
    ├── coverage
    ├── funding
    └── required return
    ↓
MONEYWHEEL
    ├── 9 canonical ratios
    └── 2 canonical rules
    ↓
RULE CLASSIFICATION
    ↓
CONSTRAINT EVALUATION
    ↓
DIAGNOSTIC / PLANNING EVIDENCE
    ↓
DOWNSTREAM CONSUMERS
    ├── Goal Planner
    ├── Strategy Builder
    ├── MoneyWheel UI
    └── Multi-goal / planning services

Scope: Financial Health & Rules only.
