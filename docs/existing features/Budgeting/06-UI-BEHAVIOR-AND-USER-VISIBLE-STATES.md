# Budgeting — UI Behavior and User-Visible States

**Source revision:** `6d2fca0ac37d6dee32c0678047c1df46459b3298`

Primary source: [`frontend/app/investor/budgeting/page.tsx`](https://github.com/Bhardwaj1-star/planvesto/blob/main/frontend/app/investor/budgeting/page.tsx)

## 1. State declared by the page

The page declares state for:
- Monthly vs Annual period display (initially Monthly).
- Loaded `BudgetData`, loading flag and load error.
- Whether budget editing is active, draft BudgetItems, save-success notice and save-in-progress flag.
- Target type (percentage/amount), savings target input (initially 30), and desired-surplus input (initially 65000).

State declaration proves the controls' local state exists, not that every control is connected to a persisted business rule.

## 2. Initial load and retry

On mount, the page calls `loadBudgetData()`. It clears the previous load error, assigns returned data (or null), captures thrown errors, and turns off the loading state in `finally`.

The inspected error branch displays an “Unable to Load Budget Data” message and a retry button. Retry resets the loading flag and calls the fetch callback.

## 3. Editing and saving

- Starting edit copies the displayed items into a draft.
- Category editing updates either `budgetMonthly` or `classification` in the draft.
- Save submits category, classification and monthly amount for every draft item.
- On success, edit mode closes, a success notice is shown, and data reloads.
- The success notice is scheduled to clear after four seconds.
- On failure, the handler logs the error to the console; the inspected handler does not set a separate visible save-error message.
- Reset discards draft edits by restoring the currently loaded items and closing edit mode.

## 4. Annual presentation

The period toggle uses a multiplier of 12 for Annual display. The data source still provides monthly normalized amounts. The toggle is presentation logic, not a separate annual budget persistence contract.

## 5. Need vs Want

The page computes Need and Want totals from each item's `actualMonthly`, not its `budgetMonthly`, and applies the selected display multiplier. Percentages are computed from the unscaled monthly actuals, which keeps the ratios unchanged when switching the display period.

## 6. Observability limitations

- Browser rendering and interactive behavior were not executed.
- The complete visual layout is not described as verified merely from state and handler inspection.
- The declared savings target and desired-surplus inputs require call-site tracing before concluding whether they affect displayed calculations; their presence alone is not evidence of functional target-setting.
