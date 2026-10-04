# MoneyWheel

## 1. Feature Scope

MoneyWheel presents the current FinancialState through the canonical financial-ratio and rule contract.

```text
User
└── MoneyWheel
    └── Current FinancialState
        └── Canonical calculations
            ├── Savings
            ├── Liquidity
            ├── Debt
            ├── Leverage
            ├── Financial Assets
            ├── Insurance
            ├── Goal Funding
            ├── Future Funding
            └── Required Return
                ↓
            Coverage rules
                ├── Expense Coverage
                └── Emergency Coverage
                    ↓
                Classification / Diagnostics
                    ↓
                Planning Evidence
```

MoneyWheel is a presentation/decision-evidence layer over canonical FinancialState calculations and rules. It is not the owner of raw financial data.

## 2. User / Request Inputs

MoneyWheel consumes:

- Planning Unit context
- scope
- investor context where applicable
- current authoritative FinancialState

It must use the current backend FinancialState rather than trusting an arbitrary client snapshot as current.

## 3. Input Source / Authority Boundary

| Layer | Authority |
|---|---|
| Raw financial records | Planning Unit data |
| Current FinancialState | FinancialStateService |
| Shared financial mathematics | `backend/engines/calculation/canonical.py` |
| MoneyWheel ratios/rules | `backend/rules/moneywheel.py`, MoneyWheel engine |
| Constraint consequences | Constraint policy/evaluator |

MoneyWheel must not duplicate canonical formulas in UI code.

## 4. Canonical Ratio Contract

The canonical ratios are exactly:

1. `savings_rate`
2. `liquid_asset_ratio`
3. `debt_to_income_ratio`
4. `leverage_ratio`
5. `financial_asset_ratio`
6. `insurance_coverage_ratio`
7. `goal_funding_ratio`
8. `future_funding_ratio`
9. `required_rate_of_return`

These keys are the authoritative MoneyWheel vocabulary.

## 5. Canonical Rule Contract

The canonical rules are:

1. `expense_coverage`
2. `emergency_coverage`

Definitions:

- Expense Coverage = Liquid Assets / Monthly Expenses
- Emergency Coverage = Liquid Assets / Essential Monthly Expenses

They are distinct rules because their denominator has different business meaning.

## 6. Calculation Contract

MoneyWheel consumes canonical calculations including:

- Savings Rate = Monthly Surplus / Monthly Income × 100
- Liquid Asset Ratio = Liquid Assets / Total Assets × 100
- DTI = Monthly Debt Payments / Gross Monthly Income × 100
- Leverage = Total Liabilities / Total Assets × 100
- Financial Asset Ratio = Financial Assets / Total Assets × 100
- Insurance Coverage Ratio = Existing Sum Assured / Required Insurance Cover × 100
- Goal Funding Ratio = Current Goal Funding / Goal Target × 100
- Future Funding Ratio = Projected Goal Funding / Future Goal Target × 100
- Required Rate of Return = ((Future Goal Target / Current Goal Funding)^(1/Duration) - 1) × 100

Calculation ownership remains in the canonical calculation layer.

## 7. Classification / Rule Logic

Current emergency coverage bands:

- excellent: ≥ 9 months
- healthy: 6–<9 months
- attention: 3–<6 months
- critical: <3 months

Where ratio bands are defined, MoneyWheel distinguishes:

```text
Calculated value
    ↓
Classification / status
    ↓
Business rule consequence
```

A critical ratio is not automatically a goal-feasibility failure.

## 8. Canonicalization Boundary

Metric aliases normalize through `canonicalize_metric_key()`.

Known compatibility aliases include:

- `savings_ratio` → `savings_rate`
- `liquid_asset_to_total_asset` → `liquid_asset_ratio`
- `insurance_gap_ratio` → `insurance_coverage_ratio`
- `emergency_fund_coverage` → `emergency_coverage`

Legacy aliases are compatibility vocabulary only and must not become competing business concepts.

## 9. Lifecycle / State Authority

```text
Raw Financial Records
    ↓
FinancialStateService
    ↓
Current FinancialState
    ↓
Canonical Calculations
    ↓
MoneyWheel Ratios / Rules
    ↓
Classification
    ↓
Diagnostics / Constraints
    ↓
Planning Consumers
```

Changed raw inputs invalidate stale FinancialState according to the FinancialState revision contract.

## 10. Output Contract

MoneyWheel output contains:

- canonical ratio keys
- calculated values where available
- availability/reason information
- classifications/statuses
- rule results
- diagnostic evidence
- applicable constraint consequences

The output must preserve the distinction between metric value, rule classification and business consequence.

## 11. Ownership Boundary

- API: `backend/api/moneywheel.py`
- MoneyWheel engine: `backend/engines/moneywheel/engine.py`
- Canonical calculations: `backend/engines/calculation/canonical.py`
- MoneyWheel rules/aliases: `backend/rules/moneywheel.py`
- Constraint evaluation: `backend/engines/constraints/evaluator.py`
- Constraint policy: `backend/rules/constraints.py`
- Frontend contract/UI: MoneyWheel frontend API/components

## 12. Downstream Dependencies

MoneyWheel evidence feeds:

- Goal Planner feasibility context
- Strategy Builder constraints/decision evidence
- financial-health presentation
- dashboard/report evidence

It does not select a strategy or create an Action Plan.

## 13. Regression Contract

Tests must protect:

- exactly nine canonical ratios;
- exactly two canonical rules;
- emergency vs expense coverage distinction;
- canonical alias normalization;
- unavailable inputs remain unavailable;
- current FinancialState is used;
- formulas remain owned by canonical calculation layer;
- classification remains distinct from constraint consequence;
- critical ratio does not automatically mean goal infeasibility.

## 14. Known Implementation Notes / Gaps

1. FinancialState does not store every MoneyWheel ratio; MoneyWheel derives canonical output separately.
2. Not every MoneyWheel ratio is currently a hard constraint.
3. Legacy aliases remain compatibility behavior.
4. Thresholds must remain purpose-specific and must not be duplicated as competing rule definitions.

## 15. Important Semantic Boundaries

1. MoneyWheel ≠ FinancialState authority.
2. Ratio ≠ Rule.
3. Rule ≠ Constraint.
4. Ratio status ≠ Goal feasibility.
5. Compatibility alias ≠ canonical metric.
6. MoneyWheel evidence ≠ StrategyVersion authority.
7. Current FinancialState ≠ historical snapshot.

## 16. Final MoneyWheel Output

```text
Current FinancialState
    ↓
9 Canonical Ratios
    ↓
2 Canonical Rules
    ↓
Classification / Diagnostics
    ↓
Constraint Consequences
    ↓
Financial Planning Evidence
```

## 17. MoneyWheel End-to-End Contract

CURRENT FINANCIALSTATE
    ↓
CANONICAL CALCULATIONS
    ↓
9 RATIOS + 2 RULES
    ↓
CLASSIFICATION
    ↓
DIAGNOSTIC / CONSTRAINT EVIDENCE
    ↓
GOAL / STRATEGY / REPORTING CONSUMERS

Scope: MoneyWheel only.