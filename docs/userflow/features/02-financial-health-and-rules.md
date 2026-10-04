# Financial Health & Rules

## 1. Feature Scope
Builds the authoritative Financial State from Planning Unit records, computes canonical financial measures, classifies MoneyWheel ratios/rules, and evaluates planning constraints.

## 2. User / Request Inputs
- planning_unit_id
- scope: family or individual
- investor_id: required for individual scope and invalid for family scope

The service reads investors, income, expenses, assets, liabilities, ownership, liability responsibility and expense participation. The client does not submit the complete derived Financial State as authoritative calculation input.

## 3. Input Source / Authority Boundary
FinancialStateService is the current Financial State authority. A snapshot is reusable only when raw-input revision, Planning Unit, scope, investor and authority lineage are valid. Changed raw inputs force a rebuild. MoneyWheel reads current backend Financial State rather than trusting a client snapshot.

## 4. Canonical Rules and Calculations
Financial State derives monthly/annual income and expenses, investable surplus, assets/liquidity, liabilities/EMI burden, net worth, cash-flow/savings measures, and safety reserve.

Shared mathematics is owned by backend/engines/calculation/canonical.py:
- Savings Rate = Monthly Surplus / Monthly Income × 100
- Liquid Asset Ratio = Liquid Assets / Total Assets × 100
- Expense Coverage = Liquid Assets / Monthly Expenses
- Emergency Coverage = Liquid Assets / Essential Monthly Expenses
- DTI = Monthly Debt Payments / Gross Monthly Income × 100
- Leverage = Total Liabilities / Total Assets × 100
- Financial Asset Ratio = Financial Assets / Total Assets × 100
- Insurance Coverage Ratio = Existing Sum Assured / Required Insurance Cover × 100
- Goal Funding Ratio = Current Goal Funding / Goal Target Amount × 100
- Future Funding Ratio = Projected Goal Funding / Future Goal Target × 100
- Required Rate of Return = ((Future Goal Target / Current Goal Funding)^(1/Duration) - 1) × 100

Missing source data remains unavailable; it must not silently become zero.

## 5. MoneyWheel Rules / Decision Logic
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

Canonical rules:
1. expense_coverage
2. emergency_coverage

Expense Coverage and Emergency Coverage remain distinct. Emergency coverage uses liquid assets / essential monthly expenses.

Current emergency bands: excellent ≥9 months; healthy 6–<9; attention 3–<6; critical <3.

MoneyWheel ratios use excellent/healthy/attention/critical bands. Calculation = mathematical result; Rule = threshold interpretation; Constraint = business consequence. Current explicit hard/warning consequences cover emergency coverage, DTI and savings-rate. A critical ratio does not automatically make every goal infeasible.

## 6. Canonicalization Boundary
Metric aliases normalize through canonicalize_metric_key(). Examples:
- savings_ratio → savings_rate
- liquid_asset_to_total_asset → liquid_asset_ratio
- insurance_gap_ratio → insurance_coverage_ratio
- emergency_fund_coverage → emergency_coverage

Compatibility vocabulary must not create a second business concept.

## 7. Lifecycle / State Transitions
Raw records → FinancialState snapshot → canonical measures → MoneyWheel classification → constraint evaluation → planning consumer.

When source revisions change, the authoritative Financial State snapshot is rebuilt.

## 8. Output Contract
Outputs include current Financial State, canonical financial measures, MoneyWheel ratios/rules, classification/status, diagnostic evidence and applicable planning constraints. Derived metrics preserve availability/reason information.

## 9. Ownership Boundary
- FinancialState authority: FinancialStateService
- Shared formulas: calculation/canonical.py
- MoneyWheel rules: rules/moneywheel.py
- Constraint policy: rules/constraints.py
- Constraint evaluation: engines/constraints/evaluator.py

Consumers must not duplicate canonical formulas.

## 10. Downstream Dependencies
Outputs feed Goal Planner feasibility, Strategy Builder constraints/decision evidence, MoneyWheel UI and downstream planning.

## 11. Versioning / State Authority
FinancialState snapshots carry revision/lineage context. Current state is determined by source revision and ownership scope, not by a client-provided snapshot alone.

## 12. Code Ownership
- API: backend/api/financial_state.py
- Authority/freshness: backend/services/financial_state_service.py
- Engine/model/schema: backend/engines/financial_state/engine.py, backend/models/financial_state.py, backend/schemas/financial_state.py
- Shared calculations: backend/engines/calculation/canonical.py
- MoneyWheel: backend/api/moneywheel.py, backend/engines/moneywheel/engine.py, backend/rules/moneywheel.py
- Constraints: backend/rules/constraints.py, backend/engines/constraints/evaluator.py

## 13. Regression Contract
Scope/ownership, conversions, surplus, net worth, unavailable metrics, freshness rebuilds, canonical formulas, nine ratios, two rules, alias normalization, emergency-vs-expense semantics and constraint consequences must remain stable.

## 14. Known Implementation Notes / Gaps
1. Liquidity breakdown depends on available asset classification.
2. FinancialState does not store every MoneyWheel ratio; MoneyWheel derives canonical output separately.
3. Not every MoneyWheel ratio is currently a hard constraint.
4. Legacy snapshot normalization is compatibility behavior, not a second contract.

## 15. Important Boundaries
1. FinancialState ≠ MoneyWheel output.
2. Calculation ≠ Rule.
3. Rule ≠ Constraint.
4. Ratio status ≠ goal feasibility.
5. Client snapshot ≠ authoritative current Financial State.
6. Compatibility alias ≠ canonical metric.

## 16. End-to-End Contract
Raw financial records → FinancialState → canonical calculations → MoneyWheel ratios/rules → classification → diagnostic/constraint evaluation → downstream planning.

Scope: Financial Health & Rules only.