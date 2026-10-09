# MoneyWheel — Consolidated Change Register

**Scope:** MoneyWheel-only business decisions, calculation/diagnostic boundaries, and implementation changes identified in the existing project documents.  
**Document type:** Change register / source-of-truth summary  
**Status:** Business direction documented; some changes are not implemented or not frozen.  
**Out of scope:** Goal Planner, Strategy selection, and general Constraints implementation except where their boundary with MoneyWheel must be explicit.

---

## 1. Canonical Responsibility

```text
Raw Financial Inputs
    ↓
Financial State
    ↓
Canonical Financial Calculations
    ↓
MoneyWheel
    ↓
Financial diagnostic signals + explanations
    ↓
Constraints / Planning interpretation
    ↓
Strategy / Plan decisions
```

- Financial State owns normalized current financial facts.
- Canonical Calculation owns shared mathematical calculations.
- MoneyWheel classifies available measures and explains the financial condition.
- Constraints owns planning restrictions, warnings, hard blockers, and overrides.
- MoneyWheel does not independently decide debt repayment, investment, goal priority, strategy, or product selection.

## 2. Change Register

| ID | Change | Required state | Status in source documents |
|---|---|---|---|
| MW-01 | MoneyWheel must be a diagnostic/measurement layer, not a final decision-maker. | Keep ratios and diagnostic status separate from actions/strategy decisions. | Business direction established; current architecture docs describe the boundary. |
| MW-02 | Generic MoneyWheel ratio thresholds must not automatically trigger planning actions. | A ratio is evidence; downstream policy interprets it in goal and financial context. | Business decision established in real-life cases; code still has classifications and separate constraint rules. |
| MW-03 | Separate calculation ownership from classification ownership. | Canonical calculation functions calculate values; MoneyWheel rules classify them. | Present in current code architecture. |
| MW-04 | Keep MoneyWheel separate from Constraints. | MoneyWheel emits diagnostic status; Constraints decides warning/hard constraint/override. | Documented boundary; overlap still exists in current system. |
| MW-05 | Use the final canonical set of 9 ratios. | Retain the 9 ratios listed in Section 3; do not reintroduce Solvency Ratio as a separate ratio. | Current `backend/rules/moneywheel.py` and engine use these 9 keys. |
| MW-06 | Keep Expense Coverage and Emergency Coverage as separate coverage rules, not extra ratios. | Report normal-expense coverage and essential-expense/emergency coverage separately. | Business design documented; verify actual result/API/UI integration separately. |
| MW-07 | Remove automatic decision-making from generic DTI/savings/other ratio thresholds. | Threshold status may describe the measure but must not by itself decide debt repayment or investment allocation. | Business direction established; current MoneyWheel classifications and Constraints rules still require reconciliation. |
| MW-08 | Add debt-economics measurements as candidates, not frozen MoneyWheel metrics. | Weighted Debt Rate and Investment–Debt Spread remain proposed measurements until formulas, inputs, ownership and UI/API contracts are approved. | Explicitly not finalised in code in the concept change log. |
| MW-09 | Preserve missing-data integrity. | Missing input, zero denominator, or undefined return must be marked unavailable; do not invent a value. | Current MoneyWheel engine implements unavailable states for missing/invalid ratio inputs. |
| MW-10 | Avoid duplicate financial calculations downstream. | Consumers should use canonical measures instead of locally recalculating DTI, emergency coverage, or other shared facts. | Audit documents identify duplicate calculations in some downstream paths. |
| MW-11 | Make MoneyWheel output explainable and traceable. | Each available measure should expose key, name, value, unit, status, formula, explanation and availability; result should carry rule-set version and calculation timestamp. | Current onboarding-to-MoneyWheel architecture documents this contract; verify end-to-end persistence/UI. |
| MW-12 | Reconcile final business design against the older implementation. | Audit ratio set, formulas, thresholds, coverage rules, severity, goal-impact rules, required-return calculation, result schema and downstream input contract. | Required work is explicitly listed in `docs/product/MONEYWHEEL-CONSTRAINTS.md`; not all reconciliation is complete. |

---

## 3. Canonical MoneyWheel Measures

### 3.1 Nine ratios

```text
MoneyWheel Ratios
├── 1. Savings Rate
├── 2. Liquid Asset Ratio
├── 3. Debt-to-Income Ratio (DTI)
├── 4. Leverage Ratio
├── 5. Financial Asset Ratio
├── 6. Insurance Coverage Ratio
├── 7. Goal Funding Ratio
├── 8. Future Funding Ratio
└── 9. Required Rate of Return
```

**Solvency Ratio is not a separate canonical ratio** in this design because it is derived from Leverage Ratio.

### 3.2 Two separate coverage rules

```text
Coverage Rules
├── Expense Coverage
│   └── Liquid Assets / Monthly Expenses
└── Emergency Coverage
    └── Liquid Assets / Essential Monthly Expenses
```

These coverage rules must not be counted as two additional ratios.

---

## 4. Threshold / Decision Boundary

```text
Canonical Calculation
    └── Calculates a numeric measure
          ↓
MoneyWheel Rule
    └── Classifies the measure
          ├── Excellent
          ├── Healthy
          ├── Attention
          └── Critical
                ↓
Constraint / Planning Policy
    └── Interprets evidence in context
          ├── Informational evidence
          ├── Warning
          ├── Soft constraint
          └── Hard constraint / override, when explicitly justified
                ↓
Planning / Strategy decision
```

- Classification thresholds are metric-specific; there is no single threshold shared by every ratio.
- A MoneyWheel status of `critical` is not, by itself, a strategy rejection or an instruction to repay debt.
- DTI and savings-rate signals may inform planning, but a financial action must be based on the responsible planning/constraint policy and relevant context.
- Genuine hard constraints remain possible. This change does **not** mean removing all hard constraints.
- Existing hard thresholds and boundary conditions must be reconciled consistently across MoneyWheel, Constraints, reports and any other consumer.

---

## 5. Debt Economics — Proposed, Not Final

The real-life Goal Funding case identified two candidate measurements:

```text
Debt Economics Candidates
├── Weighted Debt Rate
│   └── Sum(Outstanding Principal × Loan Interest Rate)
│       / Total Outstanding Principal
└── Investment–Debt Spread
    └── Relevant Investment Return Assumption
        − Weighted Debt Rate
```

Required handling:

- These are candidate measurements, not approved automatic decision rules.
- A positive Investment–Debt Spread does not automatically mean investing is better.
- A negative spread does not automatically trigger a universal debt-repayment rule.
- Investment returns are assumptions/scenarios, not guaranteed outcomes.
- Liquidity, loan terms, goal horizon, cash flow, repayment capacity, risk and alternative paths must be considered by the responsible planning layer.
- Do not label either measure as implemented in MoneyWheel until code, data contracts, formulas, classification, tests and UI/API integration have been verified.

---

## 6. Current Implementation Evidence

### Backend

```text
backend/
├── api/
│   └── moneywheel.py
├── models/
│   └── moneywheel.py
├── schemas/
│   └── moneywheel.py
├── rules/
│   └── moneywheel.py
├── engines/
│   ├── calculation/
│   │   └── canonical.py
│   └── moneywheel/
│       ├── engine.py
│       └── financial_state_adapter.py
├── services/
│   └── moneywheel_service.py
└── data/
    └── moneywheel_repository.py
```

### Frontend / persistence

```text
frontend/
├── app/investor/moneywheel/
│   └── page.tsx
├── lib/api/
│   └── moneywheel.ts
└── supabase/migrations/
    └── 009_moneywheel.sql
```

### Current code facts verified from repository files

- `backend/rules/moneywheel.py` defines the 9 canonical ratio keys and ratio-specific status ranges.
- `backend/engines/moneywheel/engine.py` calls canonical calculation functions for those 9 ratios and marks invalid/missing inputs unavailable.
- `backend/engines/moneywheel/financial_state_adapter.py` maps Financial State values into Moneywheel input.
- The adapter shown in the current code maps income, surplus, expenses, essential expenses, liquid assets, EMI, assets, liabilities, financial assets and existing insurance sum assured.
- The displayed adapter does not itself populate all goal-specific inputs required for Goal Funding Ratio, Future Funding Ratio and Required Rate of Return. Verify how those fields are supplied in the full service/request path before claiming the complete ratio set is available end-to-end.
- The MoneyWheel page currently reports that up to 9 ratios are available; coverage-rule presentation and persistence must be verified separately.
- Current code contains threshold classifications. The business change is **not** “delete every threshold”; it is “do not let diagnostic thresholds automatically make the downstream planning decision.”

---

## 7. Known Gaps / Reconciliation Work

```text
MoneyWheel Reconciliation
├── A. Ratio contract
│   ├── Confirm 9 canonical ratio keys
│   ├── Confirm formulas against canonical calculation functions
│   ├── Confirm metric-specific classification ranges and boundary inclusivity
│   └── Confirm unavailable-data behavior
├── B. Coverage contract
│   ├── Expense Coverage
│   └── Emergency Coverage
├── C. Decision boundary
│   ├── MoneyWheel = diagnostic classification
│   ├── Constraints = restriction / warning / override policy
│   └── Planning = contextual financial decision
├── D. Duplicate calculations
│   ├── Find local DTI calculations
│   ├── Find local Emergency Coverage calculations
│   └── Replace duplicates with canonical calculation outputs where applicable
├── E. Debt economics candidates
│   ├── Weighted Debt Rate — not frozen
│   └── Investment–Debt Spread — not frozen
├── F. Output contract
│   ├── Value / unit / formula / status / explanation / availability
│   ├── Rule-set version / calculation timestamp
│   └── API, persistence and frontend consistency
└── G. Tests
    ├── Formula tests
    ├── Threshold boundary tests
    ├── Missing / zero / invalid input tests
    ├── Diagnostic status does not directly select a strategy
    └── Regression tests for Constraints / reports / planning consumers
```

---

## 8. Source Documents

- `docs/product/MONEYWHEEL-CONSTRAINTS.md` — MoneyWheel business design, 9 ratios + 2 coverage rules, constraint boundary, reconciliation checklist.
- `docs/architecture/onboarding-to-moneywheel.md` — onboarding → Financial State → canonical calculations → MoneyWheel; result contract and missing-data behavior.
- `docs/architecture/financial-state.md` — Financial State ownership, snapshot freshness and canonical calculation boundary.
- `docs/architecture/CANONICAL-CALCULATION-SYSTEM.md` — shared calculation ownership and separation from domain classification.
- `docs/architecture/FINANCIAL-PLANNING-LAYER-MAP.md` — current code-grounded layer map and duplicate-calculation/overlap findings.
- `docs/architecture/code-architecture-consistency-audit.md` — DTI threshold-boundary inconsistency and duplicate calculation findings.
- `docs/Decision tree/Real-Life Decision Cases/00-GOAL_FUNDING_CONCEPT_CHANGE_LOG.md` — MoneyWheel should measure; generic ratio thresholds should not automatically decide; Weighted Debt Rate and Investment–Debt Spread are candidates, not frozen.
- `docs/Decision tree/Real-Life Decision Cases/13-DECISION_TREE_SYSTEM_UPDATE_AND_FEATURE_IMPLEMENTATION_PLAN.md` — identifies MoneyWheel/financial-ratio decision-like threshold behaviour as a required system correction.

---

## 9. Completion Checklist

- [ ] Confirm 9 ratio formulas match canonical calculation functions.
- [ ] Confirm 9 ratio status ranges and exact boundary behavior.
- [ ] Confirm Expense Coverage and Emergency Coverage are implemented and exposed separately.
- [ ] Confirm missing/invalid inputs remain unavailable rather than receiving invented defaults.
- [ ] Audit all consumers for local duplicate DTI / coverage calculations.
- [ ] Separate diagnostic classification from constraint/action decisions in every consumer.
- [ ] Reconcile threshold boundaries across MoneyWheel, Constraints and reports.
- [ ] Decide whether Weighted Debt Rate and Investment–Debt Spread are approved; until then, keep them explicitly proposed.
- [ ] Verify API schema, persistence, frontend display and rule-set version end-to-end.
- [ ] Add/confirm unit, boundary, integration and regression tests.
- [ ] Update implementation status only after code and tests confirm the change.

**Final rule:** MoneyWheel describes the financial condition. It does not independently decide what the investor must do.
