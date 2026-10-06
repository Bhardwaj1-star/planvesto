# Variant-Based Reporting Architecture

## Purpose

Make **Strategy Variant** a first-class input to Planvesto reporting while supporting all current reporting scopes:

- Individual Goal Report
- Goal Basket Report
- Complete Financial Plan / Multi-Goal Plan
- Summary Financial Planning Report

The architecture uses **one common reporting/rendering foundation**, while each report scope consumes the appropriate level of financial and strategic data.

---

## 1. Reporting Hierarchy

Reporting is not only a Goal-level concern.

```
                 FINANCIAL PLANNING
                        │
          ┌─────────────┴─────────────┐
          │                           │
     Goal-level                  Portfolio-level
          │                           │
   Strategy + Variant          Multi-Goal Orchestration
          │                           │
          ├──────────────┐            ├──────────────┐
          ↓              ↓            ↓              ↓
     Goal Report     Goal Basket   Complete Plan   Summary
```

| Report | Scope | Primary purpose | Variant relationship |
|---|---|---|---|
| Goal Report | One goal | Explain one goal's strategy and implementation | **Direct** — one selected Variant |
| Basket Report | Selected goals | Show joint funding, priority, cash flow and shared architecture | **Aggregates each goal's Variant** |
| Complete Financial Plan | All goals + family financial state | Show consolidated allocation, constraints, trade-offs and plan | **Consumes all goal Variants + multi-goal decisions** |
| Summary Report | Executive / cross-domain | Compact financial snapshot, goals, observations, actions, allocation and risk | **Consumes normalized outputs; Variant may be summarized** |

**Key rule:** Variant belongs to the **goal strategy layer**. Composite reports do not invent a single Variant for the whole portfolio unless a separate portfolio-level architecture is explicitly defined.

---

## 2. Core Architecture

### Goal-level pipeline

```
Goal Data
   ↓
Financial Calculations
   ↓
Strategy Decision
   ↓
Variant Selection
   ↓
Canonical Goal Report Model
   ↓
Goal Report Config
   ↓
Common Renderer
```

### Composite-report pipeline

```
Goal Reports / Goal Report Models
            ↓
   Multi-Goal Orchestration
            ↓
   Composite Report Model
            ↓
   Composite Report Config
            ↓
      Common Renderer
```

### Full system

```
Goal Data
   ↓
Financial Calculations
   ↓
Strategy Decision
   ↓
Variant Selection
   ↓
Goal Report Model
   ↓
        ┌──────────────────────┐
        │                      │
        ↓                      ↓
   Goal Report          Multi-Goal Orchestration
        │                      ↓
        │               Basket / Complete Plan
        │                      │
        └──────────────┬───────┘
                       ↓
                Report Config
                       ↓
                Common Renderer
                       ↓
                      PDF
```

---

## 3. Architecture Layers

| Layer | Responsibility |
|---|---|
| Goal Type | Goal-specific inputs, terminology, milestones and calculations |
| Strategy | High-level strategic intent |
| Variant | Implementation/funding/protection architecture for the goal |
| Multi-Goal Orchestration | Priority, shared surplus, conflicts, trade-offs and allocation across goals |
| Report Model | Normalized data required by a report |
| Report Config | Defines report structure and section requirements |
| Common Renderer | Visual rendering and PDF export |

**Rule:** Variant determines **goal implementation architecture**. Report Config determines **what to show**. Renderer determines **how to render it**.

---

## 4. Canonical Variant Set

### Progressive De-risking

- Goal-Date Glide Path
- Payment-Tranche Glide Path
- Recurring-Cashflow Glide Path
- Income-Transition Glide Path

### Capital Preservation

- Full-Goal Preservation
- First-Payment Preservation
- Rolling Reserve Preservation
- Protected-Core Preservation

### Debt Reduction

- Goal-Gap Debt Reduction
- EMI-Relief Debt Reduction
- Residual-Gap Debt Reduction
- Goal-Linked Debt Reduction

### Credit Utilisation

- Residual-Gap Bridge
- Partial-Goal Financing
- EMI-Cap Financing
- Timing-Bridge Financing

These are architecture labels. SIP, Lumpsum, Bucketing, Laddering, Cash-flow Matching, etc. remain techniques/components.

---

## 5. Variant Selection

Variant selection occurs **after Strategy eligibility** and before report/scenario generation.

```
Strategy eligible
      ↓
Identify funding/protection pattern
      ↓
Select Variant
      ↓
Validate Variant constraints
      ↓
Build Goal Report Model
```

Example:

```
Education
→ Progressive De-risking
→ Payment-Tranche Glide Path
→ Goal Report Model
```

The selected Variant must be persisted or otherwise deterministically recoverable from the strategy/report context so composite reports can consume it.

---

## 6. Goal Report

The Goal Report is the primary Variant-aware report.

### Inputs

```
Goal
Strategy Version / Run
Selected Strategy
Selected Variant
Financial calculations
Constraints
Scenarios
Actions
```

### Typical sections

- Goal summary
- Funding requirement / gap
- Strategy decision
- Selected Variant
- Variant-specific schedule
- Liquidity / de-risking
- Debt / credit
- Constraints
- Scenarios
- Trade-offs
- Action plan

### Example

**Education + Progressive De-risking + Payment-Tranche Glide Path**

```
Goal Summary
→ Education Corpus
→ Payment Tranches
→ Tranche-wise De-risking
→ Liquidity Requirement
→ Residual Loan Requirement
→ Scenarios
→ Actions
```

---

## 7. Goal Basket Report

A Basket Report is **not a new Strategy Variant**.

It is a composite report over selected goals.

The current Basket Report already aggregates:

- selected goals
- priority ladder
- shared pool allocation
- combined cash-flow trajectory
- product/bucket architecture
- action timeline
- contingency matrix
- per-goal strategy summary

### Target architecture

```
Goal A → Strategy A → Variant A ─┐
Goal B → Strategy B → Variant B ─┼→ Basket Orchestration
Goal C → Strategy C → Variant C ─┘
                                  ↓
                         Basket Report Model
                                  ↓
                         Basket Report Config
                                  ↓
                           Common Renderer
```

### Important rule

The Basket Report should **show each goal's selected Variant** where relevant, but its own architecture is based on **cross-goal orchestration**, not a Goal Variant.

---

## 8. Complete Financial Plan / Multi-Goal Report

The Complete Financial Plan is the **family/portfolio-level consolidated report**.

The current implementation builds a consolidated plan through `MultiGoalPlanningService`, including:

- all goals
- financial state
- consolidated funding
- resource allocation
- goal plans
- strategy versions
- constraints/conflicts
- audit trail
- family cash-flow trajectory
- health/ratio scan
- contingency/governance outputs

### Target architecture

```
Goal A → Variant A ─┐
Goal B → Variant B ─┼→ MultiGoalPlanningService
Goal C → Variant C ─┘
                         ↓
              Priority / Resource Allocation
                         ↓
                 Trade-offs / Constraints
                         ↓
              Complete Plan Report Model
                         ↓
              Complete Plan Report Config
                         ↓
                  Common Renderer
```

The Complete Financial Plan therefore contains **Variant-aware goal rows/sections**, plus the multi-goal layer that explains how those goals compete for shared resources.

---

## 9. Summary Report

The Summary Report is an executive-level reporting surface.

It should consume the canonical normalized model rather than independently recalculating financial logic.

Typical content:

- Financial snapshot
- Goals
- Observations
- Actions
- Investment allocation
- Risk profile

Variant detail should normally be **summarized**, not reproduced in full.

Example:

```
Goal: Education
Strategy: Progressive De-risking
Variant: Payment-Tranche Glide Path
Status: On Track
```

Detailed tranche/de-risking schedules remain in the Goal Report.

---

## 10. Report Config Architecture

Report Config must exist at two levels.

### Goal Config

```
Goal Type + Strategy + Variant
        ↓
GoalReportConfig
```

Controls:

- goal-specific sections
- variant-specific schedules
- section ordering
- terminology
- required fields
- scenario presentation
- action presentation

### Composite Config

```
Report Scope + Composite Context
        ↓
CompositeReportConfig
```

Examples:

```
BasketReportConfig
CompleteFinancialPlanConfig
SummaryReportConfig
```

These configs control aggregation/presentation, not financial calculations.

---

## 11. Canonical Report Models

Use separate logical models for separate scopes, with shared primitives.

### Shared primitives

- ReportMetadata
- GoalSummary
- StrategySummary
- VariantSummary
- FundingSummary
- ConstraintSummary
- ScenarioSummary
- ActionSummary

### Goal model

```
GoalReportModel
├── GoalSummary
├── StrategySummary
├── VariantSummary
├── Funding
├── DeRisking / Liquidity
├── Debt / Credit
├── Constraints
├── Scenarios
└── Actions
```

### Basket model

```
BasketReportModel
├── BasketMetadata
├── GoalReportSummary[]
├── PriorityLadder
├── SharedPoolAllocation
├── CombinedCashFlow
├── BasketArchitecture
├── Actions
└── ContingencyMatrix
```

### Complete Plan model

```
CompleteFinancialPlanModel
├── FinancialState
├── GoalReportSummary[]
├── ConsolidatedFunding
├── ResourceAllocation
├── MultiGoalTradeOffs
├── Constraints
├── CashFlowTrajectory
├── HealthScan
└── Governance
```

### Summary model

```
SummaryReportModel
├── FinancialSnapshot
├── GoalSummaries
├── Observations
├── Actions
├── InvestmentAllocation
└── RiskProfile
```

---

## 12. Common Renderer

All PDF scopes should converge on the same rendering foundation.

Renderer owns:

- page layout
- typography
- headers / footers
- tables
- charts
- page breaks
- reusable section components
- page numbering
- PDF export

Renderer must not own:

- goal calculations
- strategy selection
- variant selection
- multi-goal allocation
- debt calculations
- financial rules

### Do not build

```
education_pdf_generator.py
wedding_pdf_generator.py
basket_pdf_generator.py
retirement_pdf_generator.py
complete_plan_pdf_generator.py
```

### Build

```
report_engine/
├── renderer/
├── section_components/
├── models/
├── configs/
│   ├── goal/
│   ├── basket/
│   ├── complete_plan/
│   └── summary/
└── strategy_variant_mappings/
```

---

## 13. Current Repository → Target

### Verified current reporting paths

The repository currently has separate PDF/report implementations:

| Current path | Current role |
|---|---|
| `GoalReportService` | Individual Goal Strategy Report |
| `BasketReportService` | Selected-goal Basket Report |
| `FinancialPlanService` | Complete Financial Plan / consolidated multi-goal report |
| `SummaryReportRenderer` | Summary Financial Planning Report |

The APIs also expose separate PDF endpoints for Goal, Basket and Complete Financial Plan reports.

Therefore the architecture must **not** treat GoalReportService as the only reporting system.

### Target

```
                    Canonical Financial Outputs
                              │
              ┌───────────────┴────────────────┐
              │                                │
        Goal Strategy Layer              Multi-Goal Layer
              │                                │
      Strategy + Variant             Allocation / Conflicts
              │                                │
              └───────────────┬────────────────┘
                              ↓
                    Scope-specific Model
                              ↓
                    Scope-specific Config
                              ↓
                       Common Renderer
                              ↓
                             PDF
```

---

## 14. Implementation Order

### Phase 1 — Reporting Registry

Inventory all report types and define ownership:

- Goal Report
- Basket Report
- Complete Financial Plan
- Summary Report

### Phase 2 — Variant Selector

```
select_variant(goal, strategy, financial_context) → Variant
```

### Phase 3 — Shared Report Primitives

Define reusable:

- GoalSummary
- StrategySummary
- VariantSummary
- FundingSummary
- ConstraintSummary
- ScenarioSummary
- ActionSummary

### Phase 4 — Goal Report Config + Model

Make the existing Goal Report Variant-aware.

### Phase 5 — Composite Models

Create canonical models for:

- Basket
- Complete Financial Plan
- Summary

### Phase 6 — Common Renderer

Move shared PDF layout/rendering into one engine.

### Phase 7 — Migrate Existing Services

Migrate incrementally:

1. Goal Report
2. Basket Report
3. Complete Financial Plan
4. Summary Report

Preserve existing API contracts where practical.

---

## 15. Non-Negotiable Rules

1. **Variant belongs to the Goal Strategy layer.**
2. **Basket and Complete Financial Plan are composite reports, not Goal Variants.**
3. **Composite reports must consume each goal's Variant where relevant.**
4. **Do not invent a single portfolio Variant unless a portfolio-level architecture is explicitly defined.**
5. **No report-specific financial calculation logic inside the renderer.**
6. **Report Config controls structure, not business calculations.**
7. **Report Models are renderer-independent.**
8. **One common PDF rendering foundation serves all report scopes.**
9. **Adding a new Goal Variant must not require a new PDF engine.**
10. **Existing report API contracts should remain stable during migration.**

---

## Definition of Done

The reporting architecture is complete when:

- Goal Strategy Reports are Variant-aware.
- Basket Reports aggregate per-goal Strategy + Variant information.
- Complete Financial Plans consume per-goal Variants plus multi-goal orchestration outputs.
- Summary Reports consume normalized outputs without duplicating financial calculations.
- Each reporting scope has a canonical report model.
- Report Config is separate from calculations.
- One common renderer handles PDF layout/export.
- Existing Goal, Basket and Complete Plan PDF endpoints continue to work.
- New goal/variant combinations require configuration/data mapping—not a new PDF generator.
- Regression tests cover all four reporting scopes.
