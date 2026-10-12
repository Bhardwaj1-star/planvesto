# Budgeting — Tests and Evidence Gaps

**Source revision:** `6d2fca0ac37d6dee32c0678047c1df46459b3298`

## 1. Test evidence examined

This pass inspected the Budgeting page, data layer, related Financial State code and relevant SQL migrations. A dedicated Budgeting test file or a Budgeting-specific test run was not verified in this pass. This should be treated as “test coverage not established,” not proof that no tests exist anywhere in the repository.

No tests were executed during this documentation pass.

## 2. Directly evidenced implementation facts

- Budgeting is rendered at `frontend/app/investor/budgeting/page.tsx`.
- Budgeting's direct Supabase data access and local calculations are in `frontend/lib/api/budgeting.ts`.
- Stored category limits are represented by `public.budget_limits` in migration 016.
- Budget limit writes are per-item upserts with conflict key `planning_unit_id,category`.
- The Budgeting view normalizes source values to monthly amounts and separately aggregates qualifying liability EMIs.
- Realtime subscriptions listen for changes to income, expenses, liabilities and budget limits.
- The backend Financial State has a separate calculation path and separate availability semantics.

## 3. Open verification questions

1. **Test inventory:** Search the complete repository test tree for coverage of monthly normalization, classification defaults, status thresholds, category aggregation, save failures and realtime refresh.
2. **Rounding:** Verify expected behavior when per-category rounded values do not sum to the rounded overview total.
3. **Frequency values:** Confirm allowed values for income, expense and liability frequency fields; unknown values currently fall through as monthly.
4. **Liability overlap:** Verify whether counting EMI rows in Budgeting actual outflows alongside expense records can double-count any real-world payment in the application's data-entry model.
5. **Category taxonomy:** Reconcile literal category names across frontend Budgeting and backend Financial State rules, especially Food & Groceries vs Groceries.
6. **Savings target controls:** Trace all reads/writes of target type, savings target input and desired-surplus input to determine whether they have functional effects.
7. **Missing budget table handling:** Determine whether treating all budget-limit query errors as an empty list masks permission or network failures.
8. **Partial writes:** Determine expected user experience and recovery behavior when one item upsert fails after previous items succeeded.
9. **RLS in production:** Inspect effective policies and migration status in the actual target database.
10. **Cross-feature handoff:** Trace whether Goal Planner, Strategy Builder or other consumers use a shared canonical surplus value or recalculate independently.
11. **Realtime:** Test subscription status, filters, event delivery, debounce behavior and cleanup.
12. **Page behavior:** Run browser-level checks for no planning-unit ID, empty records, failed load, failed save and a category with a limit but no spend.

## 4. Evidence boundary

The items above are unresolved verification questions, not confirmed bugs and not redesign decisions. No implementation is selected for replacement, merge or removal here. The purpose is to separate observed code from behavior that still requires tests, environment access or full call-path tracing.
