# Financial Health & Rules

```text
User
└── Financial information deta hai
    └── Financial State
        └── System important measures calculate karta hai
            ├── Savings
            ├── Debt
            ├── Liquidity
            ├── Emergency Coverage
            └── Required Return
                └── Rules
                    ├── Measure calculate hota hai
                    ├── Uska business threshold dekha jata hai
                    └── Rule decide karta hai
                        ├── Pass
                        ├── Warning / Diagnostic
                        └── Hard Constraint
                            └── Planning decision ko affect karta hai
```

## 6. Input Source Boundary

Financial State request inputs:
- planning_unit_id
- scope: family or individual
- investor_id: required for individual scope and invalid for family scope

The service then reads the Planning Unit's existing financial records:
- investors
- income
- expenses
- assets
- liabilities
- asset ownership
- liability responsibility
- expense participation

Goal: the client does not submit the complete derived Financial State as the authoritative calculation input.

## 7. Financial State Calculations

Financial State derives the base financial picture:
- Income: monthly, annual and breakdown from amount + frequency.
- Expenses: monthly, annual and breakdown from amount + frequency + individual participation.
- Investable surplus: monthly income - monthly expenses.
- Assets: total assets, breakdown, allocation and liquidity breakdown.
- Liabilities: total liabilities, breakdown, allocation and monthly EMI burden.
- Net worth: total assets - total liabilities.
- Cash-flow ratio and savings/investment rate.
- Safety reserve months and required safety reserve amount.

Every derived Metric has value, available and reason. Missing source data must remain unavailable; it must not silently become zero.

## 8. Financial State Freshness and Authority

FinancialStateService is the current Financial State authority.

A snapshot is reusable only when its raw-input revision, Planning Unit, scope, investor and authority lineage are valid. If raw inputs changed, the service rebuilds the state.

MoneyWheel API intentionally ignores a client-provided Financial State snapshot and reads the current backend Financial State.

## 9. Canonical Calculation Layer

Shared financial mathematics is owned by backend/engines/calculation/canonical.py.

Canonical calculations used by this feature include:
- Savings Rate = Monthly Surplus / Monthly Income × 100
- Liquid Asset Ratio = Liquid Assets / Total Assets × 100
- Expense Coverage = Liquid Assets / Monthly Expenses
- Emergency Coverage = Liquid Assets / Essential Monthly Expenses
- Debt-to-Income Ratio = Monthly Debt Payments / Gross Monthly Income × 100
- Leverage Ratio = Total Liabilities / Total Assets × 100
- Financial Asset Ratio = Financial Assets / Total Assets × 100
- Insurance Coverage Ratio = Existing Sum Assured / Required Insurance Cover × 100
- Goal Funding Ratio = Current Goal Funding / Goal Target Amount × 100
- Future Funding Ratio = Projected Goal Funding / Future Goal Target × 100
- Required Rate of Return = ((Future Goal Target / Current Goal Funding)^(1 / Duration) - 1) × 100

One canonical formula owner must be reused by consumers rather than duplicated.

## 10. MoneyWheel Canonical Contract

Canonical ratios:
1. savings_rate
2. liquid_asset_ratio
3. debt_to_income_ratio
4. leverage_ratio
5. financial_asset_ratio
6. insurance_coverage_ratio
7. goal_funding_ratio
8. future_funding_ratio
9. required_rate_of_return

Canonical coverage rules:
1. expense_coverage
2. emergency_coverage

Legacy metric names are compatibility inputs only and normalize to canonical keys.

Example: emergency_fund_coverage → emergency_coverage.

## 11. Coverage Semantics

Expense Coverage and Emergency Coverage are distinct:
- Expense Coverage = Liquid Assets / Monthly Expenses.
- Emergency Coverage = Liquid Assets / Essential Monthly Expenses.

Current Emergency Coverage classification:
- excellent: >= 9 months
- healthy: 6 to <9 months
- attention: 3 to <6 months
- critical: <3 months

## 12. Canonical Ratio Thresholds

MoneyWheel classifies ratios as excellent, healthy, attention or critical.

| Ratio | Excellent | Healthy | Attention | Critical |
|---|---:|---:|---:|---:|
| Savings Rate | >=30% | 20–<30% | 10–<20% | <10% |
| Liquid Asset Ratio | >=25% | 15–<25% | 10–<15% | <10% |
| DTI | <20% | 20–<30% | 30–<40% | >=40% |
| Leverage | <20% | 20–<30% | 30–<50% | >=50% |
| Financial Asset Ratio | >=70% | 50–<70% | 30–<50% | <30% |
| Insurance Coverage | >=80% | 60–<80% | 40–<60% | <40% |
| Goal Funding Ratio | >=100% | 80–<100% | 50–<80% | <50% |
| Future Funding Ratio | >=100% | 80–<100% | 50–<80% | <50% |
| Required Rate of Return | <8% | 8–<12% | 12–<15% | >=15% |

Coverage rules use 9 / 6 / 3 month bands. Exact boundary behavior is owned by rules.moneywheel.classify().

## 13. Rule vs Constraint Boundary

Calculation = mathematical result.

Rule = interpretation against an approved threshold.

Constraint = business consequence applied to a planning decision.

Current explicit constraint rules:
- Emergency coverage critical can create a hard constraint on high/critical discretionary goals and suggest priority low.
- Emergency coverage attention produces a warning.
- DTI critical can create a hard constraint on high/critical discretionary goals and suggest priority low.
- DTI attention produces a warning.
- Savings-rate deficit produces a warning.

A critical ratio does not automatically mean every goal is infeasible. Constraint evaluation is decision-specific.

## 14. Canonicalization Boundary

Metric aliases are normalized through canonicalize_metric_key() before downstream classification.

Current compatibility examples:
- savings_ratio → savings_rate
- liquid_asset_to_total_asset → liquid_asset_ratio
- insurance_gap_ratio → insurance_coverage_ratio
- emergency_fund_coverage → emergency_coverage

Compatibility vocabulary must not create a second business concept.

## 15. Code Ownership

- Financial State API: backend/api/financial_state.py
- Financial State authority/freshness: backend/services/financial_state_service.py
- Financial State calculation: backend/engines/financial_state/engine.py
- Financial State model: backend/models/financial_state.py
- Request contract: backend/schemas/financial_state.py
- Shared calculations: backend/engines/calculation/canonical.py
- MoneyWheel API: backend/api/moneywheel.py
- MoneyWheel engine: backend/engines/moneywheel/engine.py
- MoneyWheel rules: backend/rules/moneywheel.py
- Constraint policy: backend/rules/constraints.py
- Constraint evaluator: backend/engines/constraints/evaluator.py

## 16. Regression Contract

Financial State tests must protect scope ownership, monthly/annual conversions, surplus, net worth, ownership allocation and unavailable-metric semantics.

Freshness tests must prove unchanged inputs can reuse a valid snapshot and changed inputs force rebuild.

Canonical calculation tests must prove formulas, units and invalid-denominator behavior.

MoneyWheel tests must prove the nine canonical ratios, two canonical rules, legacy alias normalization, emergency-vs-expense coverage semantics and threshold classification.

Constraint tests must prove emergency, DTI and savings rules remain distinct from ratio status and apply only their defined planning consequences.

## 17. Current Implementation Notes

1. FinancialState liquidity breakdown currently depends on the asset records/classification available to the Financial State engine.
2. FinancialState does not itself store every MoneyWheel ratio; MoneyWheel calculates and normalizes its canonical output separately.
3. The current constraint evaluator explicitly covers emergency coverage, DTI and savings rate; not every MoneyWheel ratio is currently a hard constraint.
4. Legacy MoneyWheel snapshot normalization is compatibility behavior, not a second canonical contract.

## 18. End-to-End Contract

Raw financial records → FinancialStateService → current FinancialState → canonical calculations → MoneyWheel ratios/rules → classification → diagnostic/constraint evaluation → downstream planning.

Scope: this update is limited to Financial Health & Rules. Other feature documents are intentionally untouched in this step.