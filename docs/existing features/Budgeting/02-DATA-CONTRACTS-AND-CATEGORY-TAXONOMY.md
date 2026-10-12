# Budgeting — Data Contracts and Category Taxonomy

**Source revision:** `6d2fca0ac37d6dee32c0678047c1df46459b3298`

## 1. TypeScript contracts

Source: [`frontend/lib/api/budgeting.ts`](https://github.com/Bhardwaj1-star/planvesto/blob/main/frontend/lib/api/budgeting.ts)

### `BudgetLimitRow`

| Field | Declared type | Meaning supported by source |
|---|---|---|
| `budget_limit_id` | `string` | Persisted limit row identifier |
| `planning_unit_id` | `string` | Planning-unit scope |
| `category` | `string` | Category key |
| `classification` | `"Need" | "Want"` | User classification |
| `budget_monthly` | `number` | Stored monthly limit |
| `created_at`, `updated_at` | `string` | Timestamps |

### `BudgetItem`

The calculated item contains `id`, `category`, `classification`, `budgetMonthly`, `actualMonthly`, `varianceMonthly`, `status`, `icon`, and `percentageOfBudget`. Status is restricted in TypeScript to `"Under Budget" | "On Track" | "Over Budget"`.

### `BudgetOverview`

The overview contains monthly income, expenses and surplus; savings target amount and percentage; and Need/Want actual totals. These are client-derived values, not a separately persisted overview record in the inspected data layer.

## 2. Category display metadata

The data layer defines category-to-icon mappings and default Need/Want classifications in local constants.

**Categories with explicit defaults found in source:**

| Category | Default classification |
|---|---|
| Housing | Need |
| Food & Groceries | Need |
| Utilities | Need |
| Transportation | Need |
| Education | Need |
| Healthcare | Need |
| Insurance | Need |
| Debt Payments | Need |
| Family Support | Need |
| Travel | Want |
| Entertainment | Want |
| Shopping | Want |
| Other | Want |
| Home Loan | Need |
| Car Loan | Need |
| Personal Loan | Need |
| Education Loan | Need |
| Business Loan | Need |
| Credit Card | Need |

For categories not listed in the defaults, the fallback is `Want`. This is an implementation default, not a claim that the classification is universally correct.

## 3. Expense and liability category derivation

- Expense category is `expense_type`; a falsy/missing value falls back to `Other`.
- Liability grouping inspects `liability_name` and matches exact names or names starting with a known type plus `" - "`.
- Recognized liability prefixes: Home Loan, Car Loan, Personal Loan, Education Loan, Business Loan, Credit Card, and Other.
- If no liability prefix matches, the code uses `Debt Payments`.
- A liability row is skipped for Budgeting aggregation when `emi_amount` is falsy or less than/equal to zero.

These string rules are sensitive to category naming. No canonical shared category enum between the frontend Budgeting data layer and backend Financial State rules was established in this pass.

## 4. Stored versus derived identifiers

A BudgetItem ID is the stored `budget_limit_id` when a limit row exists. Otherwise, it is generated client-side from the category using a `derived-` prefix and a lowercase, non-alphanumeric-to-hyphen transformation.

The generated ID is for the displayed derived item; it is not a database row ID.

## 5. Contract gaps

- Database-generated TypeScript types exist in `frontend/lib/database.types.ts`, but their full consistency with all deployed migrations was not validated against a live schema.
- The UI casts query rows to `BudgetLimitRow`; runtime validation of returned row shapes is not present in the inspected code.
- Whether category aliases such as `Groceries` and `Food & Groceries` are intended to be equivalent is not specified by these type declarations.
