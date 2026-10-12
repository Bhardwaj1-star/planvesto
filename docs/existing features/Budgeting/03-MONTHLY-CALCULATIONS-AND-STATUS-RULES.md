# Budgeting — Monthly Calculations and Status Rules

**Source revision:** `6d2fca0ac37d6dee32c0678047c1df46459b3298`

Primary source: [`frontend/lib/api/budgeting.ts`](https://github.com/Bhardwaj1-star/planvesto/blob/main/frontend/lib/api/budgeting.ts)

## 1. Frequency normalization

The local `toMonthly(amount, frequency)` helper uses these rules:

| Frequency | Monthly amount |
|---|---:|
| Annual | amount / 12 |
| Quarterly | amount / 3 |
| Monthly | amount |
| Any other value | amount (default branch) |

The helper does not reject unknown frequency values; they are treated like monthly amounts. The source does not establish whether every upstream form restricts frequency to the three expected values.

## 2. Income

All selected income rows for the planning unit are normalized to monthly values and summed. The result is not rounded until the overview is built.

## 3. Actual outflow aggregation

1. Each expense row contributes its monthly-normalized amount to the key in `expense_type`, or `Other` when missing/falsy.
2. Each qualifying liability EMI contributes its monthly-normalized amount to a category inferred from `liability_name`.
3. Expenses and liability EMIs are added into the same `expenseByCategory` map.
4. Category actuals are rounded individually with `Math.round` when BudgetItems are created.
5. `totalActual` is calculated from the unrounded category map, then the overview total is rounded.

This means displayed category amounts and the rounded overview total can differ by rounding effects. Also, if an expense and liability use overlapping category labels, their values are combined under the same key.

## 4. Budget limits and item inclusion

- A category's budget is the stored `budget_monthly` value if a matching limit exists; otherwise it is zero.
- A stored classification wins; otherwise the local default map is used, with `Want` as the final fallback.
- A category is hidden only when both rounded actual equals zero and budget equals zero.
- Categories that have a budget limit but no current spend can still appear.
- Items sort with Need before Want, then actual monthly amount descending within each classification.

## 5. Variance and status

`varianceMonthly = actualMonthly - budgetMonthly`.

Status is determined by `deriveStatus(budget, actual)`:

- If budget is zero: status is On Track only when actual is zero; otherwise Over Budget.
- Otherwise calculate variance = actual − budget and tolerance = 5% of budget.
- Over Budget if variance is strictly greater than the tolerance.
- Under Budget if variance is strictly less than negative tolerance.
- Otherwise On Track.

The comparisons are strict. Values exactly at either 5% boundary remain On Track.

## 6. Overview and savings target

- Monthly expenses: rounded `totalActual`.
- Monthly surplus: rounded monthly income minus the unrounded total actual.
- Savings target percentage: hard-coded to 30.
- Savings target monthly: rounded income × 30%.
- Need and Want totals: sum the rounded item actuals within each classification, then round the result.

The page also declares local state for a target type, savings target input (initially `"30"`) and desired surplus input (initially `"65000"`). In the inspected data-layer contract, the returned savings target remains hard-coded at 30%; the inputs' state declaration alone does not establish that changing them affects calculations or persists data.

## 7. Period selector boundary

The page has Monthly/Annual display state and uses a multiplier of 12 for Annual presentation. The data-layer output is monthly. The UI period toggle is a display conversion; it does not change the query window or make the underlying source rows annual records.

## 8. Calculation caveats requiring verification

- The Budgeting data layer's essential/Need defaults differ in names from the backend's `backend/rules/financial_metrics.py` essential-expense set. For example, frontend defaults include `Food & Groceries`, while backend lists `Groceries`. This is a source-level mismatch, not proof of a user-visible incorrect result.
- Budgeting counts qualifying liability EMI as expense-category outflow. The backend Financial State engine has its own expense and EMI calculations. Their intended reconciliation is not established.
- No calculation tests were executed during this pass.
