# Frontend vs Backend Mismatch Audit & Integration Matrix
**Planvesto Strategy, Goal Decision & Financial Planning Architecture**  
**Date:** October 2026  
**Target Repository:** `planvesto` (`Bhardwaj1-star/planvesto`)  
**Branch:** `backend-audit-cleanup`

---

## 1. Executive Summary

Backend me `GoalDecisionReport`, `BasketReportService`, `FinancialPlanService`, aur canonical strategy execution complete ho chuka hai (388 pytest test cases passing, zero schema migrations).  
Lekin **Frontend (`frontend/`) aur Backend (`backend/`) ke contracts, response shapes aur route connections ke beech critical mismatches** paye gaye hain. Agar koi user web UI se goal report, retirement report ya basket report kholega to runtime crashes (e.g. `undefined` access), fallback default text, ya missing visual modules show honge.

Ye audit document har ek mismatch ko **Severity (Critical / High / Medium / Low)**, **Exact Code Locations**, **Root Cause**, **Failure Symptoms**, aur **Remediation Code** ke saath detail karta hai.

---

## 2. Mismatch Severity Matrix

| ID | Module / Feature | Frontend File | Backend File / Route | Severity | Impact Summary |
|---|---|---|---|---|---|
| **MM-01** | Goal Decision Report Header & Details | `frontend/app/investor/goal-report/page.tsx` & `frontend/lib/api/strategy.ts` | `backend/services/goal_report_service.py` (`GoalDecisionReport`) | **CRITICAL** | Frontend expects top-level `report.goal_name`, `report.goal_details`; Backend returns nested `report.goal` object. Header title is blank/undefined; `Object.keys(report.goal_details)` throws `TypeError`. |
| **MM-02** | Strategy Recommendation Fields | `frontend/app/investor/goal-report/page.tsx` | `backend/services/goal_report_service.py` | **HIGH** | Frontend expects `report.strategy.name` and `report.strategy.objective`; Backend returns `report.strategy.selected_strategy_name` and `report.strategy.rationale`. Causes fallback defaults ("Strategy not selected"). |
| **MM-03** | Legacy Retirement Report Crash | `frontend/app/investor/retirement-report/page.tsx` | `GET /api/strategy/runs/{id}/retirement-report` | **CRITICAL** | Frontend expects legacy `{ title: string, sections: ReportSection[] }` and loops over `report.sections`. Backend returns full canonical `GoalDecisionReport` object without a `sections` array, causing immediate runtime crash. |
| **MM-04** | Goal Basket Reports Unconnected | `frontend/components/PlanningBasketButton.tsx` & `frontend/app/investor/reports/page.tsx` | `POST /api/basket-report` & `POST /api/basket-report/pdf` | **HIGH** | Backend has complete Basket Report & PDF engine, but Frontend has 0 API client functions in `lib/api/strategy.ts`, no UI in Reports Center, and `PlanningBasketButton` only saves to local storage without backend connection. |
| **MM-05** | Complete Financial Plan `ratio_constraints` | `frontend/app/investor/action-plan/page.tsx` | `backend/services/financial_plan_service.py` (`/api/financial-plan`) | **MEDIUM** | Frontend expects `plan.ratio_constraints: RatioConstraintEvaluation[]` (`rule_id`, `rule_name`, `status`, `target_threshold`, `current_ratio`). Backend returns raw audit trail constraints, hiding the evaluation widget in the UI. |
| **MM-06** | Rich PDF Modules Missing in Web UI | `frontend/app/investor/goal-report/page.tsx` | `GoalReportService` (`cash_flow_trajectory`, `product_architecture`, `contingency_matrix`, `action_plan_timeline`) | **MEDIUM** | Backend generates 5 enterprise-grade sections in JSON, but frontend web UI only renders basic charts & asset allocation, ignoring multi-year cash flows, 3-bucket architecture, and contingency plan. |
| **MM-07** | Surplus Zero Incompleteness Warning | `frontend/app/investor/action-plan/page.tsx` | `backend/services/financial_plan_service.py` | **LOW** | When user monthly surplus is 0, frontend shows "Incomplete Financial State". Backend defaults surplus to 0.0 but does not provide diagnostic onboarding hints. |

---

## 3. Deep Dive: Critical & High Mismatches

---

### MM-01: Goal Decision Report Schema Divergence

#### 📍 Locations:
- **Frontend:**
  - `frontend/lib/api/strategy.ts` (Interface: `GoalStrategyReport`)
  - `frontend/app/investor/goal-report/page.tsx` (Lines 110–135)
- **Backend:**
  - `backend/services/goal_report_service.py` (`GoalReportService.build_report`)
  - `backend/schemas/strategy.py` (`GoalDecisionReport`)

#### 🔍 Root Cause Analysis:
1. **Frontend Contract:**
   ```typescript
   export interface GoalStrategyReport {
     goal_id: string;
     goal_name: string;        // <--- Expects top-level
     goal_type: string;        // <--- Expects top-level
     goal_details: {           // <--- Expects dictionary of key/values
       [key: string]: string | number;
     };
     strategy: {
       name: string;           // <--- Expects name
       objective: string;      // <--- Expects objective
       ...
     };
   }
   ```
2. **Backend Contract Returned:**
   ```python
   {
       "report_type": "goal_decision_report",
       "goal": {               # <--- Nested under "goal"
           "id": "goal_123",
           "name": "Child Education",
           "type": "education",
           "priority": "essential",
           "target_amount": 2500000.0,
           "timeline_years": 10
       },
       "goal_calculation": { ... },
       "strategy": {
           "selected_strategy_name": "Aggressive Wealth Growth", # <--- Field name
           "strategy_type": "growth",
           "rationale": "High time horizon with moderate risk tolerance", # <--- Field name
           ...
       }
   }
   ```

#### 💥 Failure Symptoms:
- Web page shows `undefined` for Goal Name in the header.
- In `goal-report/page.tsx`:
  ```typescript
  Object.keys(report.goal_details).length > 0
  ```
  Since `report.goal_details` is `undefined`, this throws an unhandled `TypeError: Cannot convert undefined or null to object`, crashing the page.

#### 🛠️ Solution Options:
- **Backend Backward-Compatibility Layer (Non-breaking):**
  Add top-level aliases in `GoalReportService.build_report()`:
  ```python
  # Compatibility aliases for legacy frontend
  report["goal_id"] = goal_dict.get("id")
  report["goal_name"] = goal_dict.get("name")
  report["goal_type"] = goal_dict.get("type")
  report["goal_details"] = {
      "Target Amount": f"₹{goal_dict.get('target_amount', 0):,.0f}",
      "Time Horizon": f"{goal_dict.get('timeline_years', 0)} years",
      "Priority": goal_dict.get("priority", "medium").title(),
  }
  report["strategy"]["name"] = report["strategy"].get("selected_strategy_name")
  report["strategy"]["objective"] = report["strategy"].get("rationale")
  ```
- **Frontend Type & Component Update:**
  Update `GoalStrategyReport` in `frontend/lib/api/strategy.ts` to support both `report.goal?.name` and `report.goal_name`.

---

### MM-02: Strategy Recommendation Field Names

#### 📍 Locations:
- `frontend/app/investor/goal-report/page.tsx` (Lines 160–180)
- `backend/services/goal_report_service.py`

#### 🔍 Root Cause Analysis:
- Frontend renders:
  ```tsx
  <h3>{report.strategy?.name || "Strategy not selected"}</h3>
  <p>{report.strategy?.objective || "Goal-specific strategy recommendation"}</p>
  ```
- Backend returns:
  `selected_strategy_name` and `rationale` inside `report["strategy"]`.

#### 💥 Failure Symptoms:
Even when the strategy engine succeeds and selects a strategy, the UI displays the fallback placeholder texts: *"Strategy not selected"* and *"Goal-specific strategy recommendation"*.

---

### MM-03: Legacy Retirement Report Crash

#### 📍 Locations:
- **Frontend:** `frontend/app/investor/retirement-report/page.tsx`
- **Backend:** `backend/api/routes/strategy.py` (`GET /runs/{strategy_run_id}/retirement-report`)

#### 🔍 Root Cause Analysis:
- `frontend/app/investor/retirement-report/page.tsx` was written for an old mock endpoint that returned:
  ```typescript
  interface RetirementReport {
    title: string;
    sections: ReportSection[];
    download_url?: string;
  }
  ```
- The frontend page renders:
  ```tsx
  {report.sections.map((section, idx) => ( ... ))}
  ```
- Backend canonical cleanup refactored `/runs/{strategy_run_id}/retirement-report` to redirect to `GoalReportService.build_report()`, returning a structured `GoalDecisionReport`. It **does not have a `sections` array**.

#### 💥 Failure Symptoms:
Visiting `/investor/retirement-report?run_id=...` immediately throws:
`TypeError: Cannot read properties of undefined (reading 'map')` at `report.sections.map`.

#### 🛠️ Solution:
Provide a `sections` view adapter in backend route handler or update frontend to render the canonical decision view.

---

### MM-04: Missing Goal Basket Client & Reports UI

#### 📍 Locations:
- **Backend:**
  - `POST /api/basket-report`
  - `POST /api/basket-report/pdf`
  - `backend/services/basket_report_service.py`
- **Frontend:**
  - `frontend/components/PlanningBasketButton.tsx`
  - `frontend/app/investor/reports/page.tsx`
  - `frontend/lib/api/strategy.ts`

#### 🔍 Root Cause Analysis:
1. `backend/api/routes/basket_report.py` is fully implemented and tested.
2. In frontend:
   - `frontend/lib/api/strategy.ts` does **not** have `generateBasketReport(goalIds: string[])` or `downloadBasketReportPdf(goalIds: string[])`.
   - `frontend/app/investor/reports/page.tsx` has cards for:
     1. Complete Financial Plan (`/investor/action-plan`)
     2. Individual Goal Strategy (`/investor/goal-report`)
     3. Retirement Blueprint (`/investor/retirement-report`)
     *Basket Goal Report (2–3 bundled goals) card is completely missing.*
   - `PlanningBasketButton.tsx` stores selected goal IDs in browser `localStorage("planning_basket")` but has no button or handler to trigger `POST /api/basket-report`.

#### 💥 Failure Symptoms:
Users can select goals into a basket, but cannot view or download the bundled Basket Goal Decision Report.

---

### MM-05: Complete Financial Plan `ratio_constraints` Omission

#### 📍 Locations:
- **Frontend:** `frontend/app/investor/action-plan/page.tsx` (Lines 290–330)
- **Backend:** `backend/services/financial_plan_service.py` (`FinancialPlanService.build_plan`)

#### 🔍 Root Cause Analysis:
- Frontend renders a table for Ratio Constraints:
  ```tsx
  {plan.ratio_constraints && plan.ratio_constraints.length > 0 && (
    <div className="card">
       <h3>Financial Health Diagnostic Rules</h3>
       ...
    </div>
  )}
  ```
  Where each item is expected to have:
  - `rule_name`: string
  - `status`: "PASS" | "WARNING" | "FAIL"
  - `target_threshold`: string
  - `current_ratio`: string
  - `reason`: string
- Backend `FinancialPlanService` computes:
  - `money_wheel_scan`
  - `audit_trail["constraints"]`
  - `audit_trail["constraint_conflicts"]`
  Lekin `plan["ratio_constraints"]` formatted list top-level par expose nahi hoti.

#### 💥 Failure Symptoms:
Diagnostic rules card silently disappears from `/investor/action-plan`, depriving the investor of the visual health check table.

---

### MM-06: Rich Actionable Report Modules Present in Backend JSON but Missing in Web UI

#### 📍 Locations:
- `backend/services/goal_report_service.py`
- `frontend/app/investor/goal-report/page.tsx`

#### 🔍 Overview:
Backend now produces 5 institutional-grade planning sections:
1. `cash_flow_trajectory`: Year-by-year balance, annual contribution, returns, inflation-adjusted cost.
2. `product_architecture`: 3-bucket allocation (`Emergency/Liquidity`, `Core Compounder`, `Satellite Growth`).
3. `contribution_rules`: 5 actionable rules (SIP step-up, bonus deployment, cash sweep, dividend reinvestment, rebalancing).
4. `action_plan_timeline`: 4-phase milestone roadmap (Immediate, Accumulation, Mid-Flight, Pre-Maturity).
5. `contingency_matrix`: 4 stress scenarios (Job loss, Market drawdown, Medical emergency, Inflation spike).

**Current State:**
Ye 5 modules **PDF download** me to render hote hain (`generate_pdf`), lekin `goal-report/page.tsx` me sirf basic summary aur charts render hote hain. Frontend web UI me in 5 modules ke modern cards/tables add karna zaroori hai taaki web dashboard aur PDF 100% synchronized rahein.

---

## 4. Remediation Plan & Action Items

### Phase 1: Immediate Backend Dual-Contract Compatibility (Zero Frontend Risk)
Without changing any frontend code, backend can immediately support both new and legacy frontend expectations:

1. **`GoalReportService.build_report()` Compatibility Layer:**
   - Inject `goal_id`, `goal_name`, `goal_type`, `goal_details` at top-level.
   - Inject `strategy.name = selected_strategy_name` and `strategy.objective = rationale`.
2. **`GET /api/strategy/runs/{id}/retirement-report` Adapter:**
   - Synthesize a `sections: ReportSection[]` array from the canonical report so `/investor/retirement-report` page displays gracefully without crashing.
3. **`FinancialPlanService.build_plan()` Ratio Constraint Formatter:**
   - Format `ratio_constraints` array from `money_wheel_scan` and `audit_trail` constraints.

### Phase 2: Frontend Client & Component Enhancements
1. **`frontend/lib/api/strategy.ts`:**
   - Update `GoalStrategyReport` TypeScript interface with optional nested `goal` and `strategy` canonical fields.
   - Add `buildBasketReport(goalIds: string[]): Promise<BasketReportResponse>`.
   - Add `downloadBasketReportPdf(goalIds: string[]): Promise<Blob>`.
2. **`frontend/app/investor/reports/page.tsx`:**
   - Add **"Goal Basket Decision Report"** card allowing users to select 2–3 goals and view/download the multi-goal strategy.
3. **`frontend/app/investor/goal-report/page.tsx`:**
   - Add web UI accordions/cards for:
     - 3-Bucket Product Architecture
     - Multi-Year Cash Flow Trajectory Table
     - 4-Phase Action Plan Timeline
     - Contingency & Stress Matrix

---

## 5. Verification Checklist

- [ ] `GET /api/strategy/runs/{id}/report` provides both canonical (`report.goal.name`) and legacy (`report.goal_name`, `report.goal_details`) fields.
- [ ] `GET /api/strategy/runs/{id}/retirement-report` returns valid `sections` array for legacy UI.
- [ ] `POST /api/basket-report` callable from frontend API client.
- [ ] `/investor/goal-report` loads cleanly without JavaScript console errors.
- [ ] `/investor/action-plan` renders Financial Health Diagnostic Rules (`ratio_constraints`).
- [ ] All 388+ backend pytest cases remain 100% passing.
