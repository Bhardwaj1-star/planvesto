# Financial State — Implementation Evidence & Architecture Index

**Backend Core:** `backend/engines/financial_state/engine.py`, `backend/services/financial_state_service.py`, `backend/api/financial_state.py`  
**Frontend Entry:** `frontend/app/investor/financial-state/page.tsx`  
**Data Repository:** `backend/data/financial_state_repository.py`  
**Core Models:** `backend/models/financial_state.py`

---

## 1. Role and System Position

`FinancialState` is the **single source of truth** for all financial balance sheet and cash flow facts across the Planvesto platform.
Every downstream module consumes this snapshot:
- **MoneyWheel:** Evaluates 11 diagnostic financial ratios against benchmark bands.
- **Goal Planner & Multi-Goal:** Supplies investable monthly surplus, liquid assets, and essential expenses.
- **Risk Profiler:** Derives objective Risk Capacity from safety reserve months, DTI, surplus, and asset concentration.
- **Constraint Evaluator:** Evaluates emergency reserve critical status and debt burden constraints.
- **Strategy Builder:** Gated by financial capacity and feasibility.

---

## 2. API Surface (`/api/financial-state`)

- `GET /api/financial-state/current?planning_unit_id={id}&scope={family|individual}`: Retrieves authoritative latest snapshot.
- `POST /api/financial-state/build`: Triggers deterministic recalculation of financial state from source ledger rows.
- `GET /api/financial-state/snapshots/{snapshot_id}`: Retrieves an immutable historical snapshot.
- `GET /api/financial-state/history`: Lists previous historical snapshots with pagination.

---

## 3. Scopes & Aggregation Rules

The engine supports two strict scopes:
1. **`family`:** Aggregates all income, expense, asset, liability, and insurance rows belonging to any investor in the planning unit.
2. **`individual`:** Scoped to a specific `investor_id`. Expenses are weighted by `expense_participant_rows.participation_percentage`.

---

## 4. Exact Mathematical Metrics & Calculation Rules

Implemented in `backend/engines/financial_state/engine.py::FinancialStateEngine.build()`:

### A. Cash Flow Normalization (`engines/calculation/engine.py`)
All items normalize frequency to monthly and annual amounts:
- `Annual`: $\text{monthly} = \text{amount} / 12$, $\text{annual} = \text{amount}$
- `Monthly`: $\text{monthly} = \text{amount}$, $\text{annual} = \text{amount} \times 12$
- `Quarterly`: $\text{monthly} = \text{amount} / 3$, $\text{annual} = \text{amount} \times 4$
- `Semi-Annual`: $\text{monthly} = \text{amount} / 6$, $\text{annual} = \text{amount} \times 2$

### B. Core Balance Sheet Metrics
1. **Monthly Income:** $\sum \text{monthly\_income}_i$
2. **Monthly Expenses:** $\sum \text{monthly\_expenses}_j$
3. **Essential Monthly Expenses:** Sum of expenses where `is_essential_expense(expense_type)` is true (`rules/financial_metrics.py`).
4. **Investable Surplus:**
   $$\text{investable\_surplus\_monthly} = \text{income\_monthly} - \text{expenses\_monthly}$$
   $$\text{investable\_surplus\_annual} = \text{investable\_surplus\_monthly} \times 12$$
5. **Total Assets:** $\sum \text{asset\_value}_k$
6. **Liquid Assets:** Sum of assets classified as `liquid` or `cash` in `asset_type_master`.
7. **Financial Assets:** Liquid assets + Investments (equities, mutual funds, fixed deposits, retirement accounts).
8. **Total Liabilities:** $\sum \text{liability\_outstanding}_l$
9. **Monthly EMI Burden:** $\sum \text{liability\_monthly\_emi}_l$
10. **Net Worth:**
    $$\text{net\_worth} = \text{total\_assets} - \text{total\_liabilities}$$
11. **Insurance Sum Assured:** Total life insurance cover across valid policies.
12. **Safety Reserve Months:**
    $$\text{safety\_reserve\_months} = \frac{\text{liquid\_assets}}{\text{essential\_monthly\_expenses}}$$

---

## 5. Strict Metric Contract (`Metric` model)

Every financial fact is wrapped in a strict typed contract:
```python
class Metric(BaseModel):
    value: float | None = None
    available: bool = True
    reason: str | None = None
```
**Principle:** Missing data is **NEVER** silently defaulted to `0.0`. If income or expenses are unentered, `available=False` with `reason="MISSING_INPUT"`, preventing false zero-surplus recommendations.
