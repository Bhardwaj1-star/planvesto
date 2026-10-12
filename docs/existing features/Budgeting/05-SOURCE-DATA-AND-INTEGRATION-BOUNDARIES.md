# Budgeting — Source Data and Integration Boundaries

**Source revision:** `6d2fca0ac37d6dee32c0678047c1df46459b3298`

## 1. Source records

Budgeting derives its view from four direct frontend Supabase reads. It does not persist a separate calculated monthly overview in the inspected implementation.

- Income rows supply amount and frequency.
- Expense rows supply type, amount and frequency.
- Liability rows supply name, EMI amount and frequency.
- Budget limit rows supply the category's planned monthly amount and Need/Want classification.

The query scope is the planning-unit ID read from localStorage. Ownership enforcement depends on database policies and the surrounding authentication/session context; the helper itself is not an ownership check.

## 2. Relation to Financial State

Backend sources inspected:
- [`backend/api/financial_state.py`](https://github.com/Bhardwaj1-star/planvesto/blob/main/backend/api/financial_state.py)
- [`backend/services/financial_state_service.py`](https://github.com/Bhardwaj1-star/planvesto/blob/main/backend/services/financial_state_service.py)
- [`backend/engines/financial_state/engine.py`](https://github.com/Bhardwaj1-star/planvesto/blob/main/backend/engines/financial_state/engine.py)
- [`backend/rules/financial_metrics.py`](https://github.com/Bhardwaj1-star/planvesto/blob/main/backend/rules/financial_metrics.py)

The Financial State API has a separate authenticated endpoint family under `/api/financial-state`, including build, latest snapshot and history. It supports family and individual scope and calls ownership-validation helpers in the route.

The backend Financial State engine derives income, expenses, surplus and EMI burden through its own service/engine path. Its availability semantics and expense classification rules are not identical by definition to Budgeting's local data layer.

**Boundary:** Both surfaces use cash-flow facts, but this source pass does not establish a single shared calculation implementation or prove that displayed Budgeting surplus equals the current Financial State surplus.

## 3. Goal Planner and Strategy Builder consumers

Other code/docs refer to cash-flow or surplus metrics in planning workflows. That alone does not prove that these consumers read Budgeting's `BudgetOverview` object. The Budgeting data layer exports frontend-local types and no backend endpoint contract for its overview was identified in this path.

The exact data handoff from Budgeting's derived figures to Goal Planner or Strategy Builder remains unverified.

## 4. Cross-feature category semantics

The frontend category map and backend `is_essential_expense()` use different literal category sets. The source code establishes the difference; it does not establish whether the difference is intentional, whether forms normalize labels, or whether it causes a production discrepancy.

## 5. External effects not established

- Changing a Budgeting limit is not shown here to update an income/expense source record.
- No automatic Goal Planner or Strategy Builder recomputation is triggered directly by `saveBudgetLimits()` in the inspected function.
- Realtime listeners refresh the Budgeting page's own data; they do not demonstrate cross-feature synchronization.
