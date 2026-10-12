# Budgeting — UI Entry and Data Boundary

**Source revision:** `6d2fca0ac37d6dee32c0678047c1df46459b3298`

## 1. Route and entry point

- Page source: [`frontend/app/investor/budgeting/page.tsx`](https://github.com/Bhardwaj1-star/planvesto/blob/main/frontend/app/investor/budgeting/page.tsx)
- Route implied by the Next.js app directory: `/investor/budgeting`.
- Sidebar source: [`frontend/components/InvestorSidebar.tsx`](https://github.com/Bhardwaj1-star/planvesto/blob/main/frontend/components/InvestorSidebar.tsx), which links “Budgeting” to `/investor/budgeting`.
- The page is a client component (`"use client"`) and imports `loadBudgetData`, `saveBudgetLimits`, and `subscribeToBudgetChanges` from the Budgeting data layer.

## 2. Data access boundary

Source: [`frontend/lib/api/budgeting.ts`](https://github.com/Bhardwaj1-star/planvesto/blob/main/frontend/lib/api/budgeting.ts)

The inspected data layer uses the frontend Supabase client and reads these tables directly:

| Table | Selected fields in the Budgeting query | Purpose in calculation |
|---|---|---|
| `income` | `amount, frequency` | Monthly income total |
| `expenses` | `expense_id, expense_type, amount, frequency` | Category spend |
| `liabilities` | `liability_id, liability_name, emi_amount, frequency` | EMI outflows grouped into categories |
| `budget_limits` | `*` | User-defined monthly limits and classification |

All four reads filter on `planning_unit_id`. They are issued together with `Promise.all`.

## 3. Planning-unit resolution

`loadBudgetData()` calls a local helper that reads `planvesto-planning-unit-id` from browser `localStorage`. If the value is absent, the function returns `null` before querying Supabase.

The inspected page sets `budgetData` to `null` in this case. The complete user-facing treatment of this state should be checked in the remainder of the page and in browser behavior; it is not equivalent to proof that no financial records exist.

## 4. Error handling at the data boundary

- Errors from the `income`, `expenses`, or `liabilities` query are thrown.
- Any error from the `budget_limits` query is treated as an empty list, with a source comment specifically mentioning a possibly absent table.
- The page catches load errors and records a message for an error state with a retry control.
- Save errors are caught in the page and written to `console.error`; the inspected handler does not set a dedicated visible save-error state.

The fallback for any `budget_limits` error is broader than a missing-table condition. The source alone does not show whether a given error is schema-related, permission-related, or transient.

## 5. Save and refresh boundary

The page maps its current edit draft to `category`, `classification`, and `budgetMonthly`, then calls `saveBudgetLimits(planningUnitId, items)`. On success, it exits edit mode, displays a success notice, and reloads data.

The data layer performs one upsert per item; it does not batch the full list into one request in the inspected implementation.

## 6. Explicitly not established

- No dedicated FastAPI Budgeting endpoint was identified in the inspected page/data-layer path.
- No end-to-end browser test was executed.
- The active planning-unit ID's lifecycle and integrity are not established by reading this helper alone.
- A direct frontend query does not, by itself, establish production RLS correctness; see [07 — Database and security evidence](07-DATABASE-AND-SECURITY-EVIDENCE.md).
