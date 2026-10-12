# Onboarding Wizard — Implementation Evidence & Multi-Step Intake Flow

**Frontend Root:** `frontend/app/investor/onboarding/page.tsx`  
**Sub-Pages:** `frontend/app/investor/onboarding/*/page.tsx`  
**Backend Ledger APIs:** `/api/financial-state`, `/api/goals`, `/api/profile`, `/api/insurance`

---

## 1. Role in the Platform

The Onboarding Wizard is the investor's entry door into Planvesto. It collects personal identity, household composition, cash inflows, outflows, balance sheet holdings, and aspirational goals. 

Onboarding populates the primary Supabase ledger tables (`investors`, `income`, `expenses`, `assets`, `liabilities`, `goals`, `insurance_policies`), which subsequent build triggers compile into the authoritative `FinancialState` snapshot.

---

## 2. The 8 Multi-Step Intake Wizard Pages

Implemented as dedicated routes under `frontend/app/investor/onboarding/`:

| Step # | Route | Purpose & Collected Fields | Persisted Entity |
|---|---|---|---|
| 1 | `/personal-information` | Full name, date of birth, PAN, employment status, retirement age | `investors` |
| 2 | `/family-dependents` | Spouse, children, parents, financial dependence status | `family_members` |
| 3 | `/income` | Salary, business profits, rental, dividends, amount, frequency | `income` |
| 4 | `/expenses` | Rent, groceries, utilities, discretionary lifestyle spends, category | `expenses` |
| 5 | `/liabilities` | Home loan, car loan, personal loan, credit cards, outstanding balance, monthly EMI, interest rate | `liabilities` |
| 6 | `/assets` | Bank savings, fixed deposits, mutual funds, direct stocks, real estate, gold, provident funds | `assets` |
| 7 | `/insurance` | Life insurance, health insurance, sum assured, annual premium, PDF policy document upload | `insurance_policies` |
| 8 | `/goals` | Goal type (Retirement, House, Education, etc.), target year, today's cost, client priority | `goals` |

---

## 3. Workflow Progression & Completion Gate

1. **Step-by-Step Validation:** Each sub-page enforces positive amounts, valid frequencies, and mandatory name/date fields.
2. **Auto-Save & Realtime State:** Entries write directly to Supabase with the active `planning_unit_id`.
3. **Onboarding Finalization Gate:**
   - On completion of Step 8, the frontend calls:
     ```text
     POST /api/financial-state/build
     ```
   - This assembles the initial `FinancialState` snapshot.
   - User is then routed to `/investor/moneywheel` or `/investor/dashboard` with fully populated diagnostics.
