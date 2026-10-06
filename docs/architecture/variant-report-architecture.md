# Variant-Based Report Architecture

## Purpose

Make **Strategy Variant** a first-class input to financial-plan reporting without creating a separate PDF engine for every goal or variant.

### Target flow

```
Goal Data
   ↓
Financial Calculations
   ↓
Strategy Decision
   ↓
Strategy Variant Selection
   ↓
Canonical Report Model
   ↓
Report Config
   ↓
Common PDF Renderer
   ↓
PDF
```

---

## 1. Architecture Hierarchy

```
Goal Type → Strategy → Variant → Report Config → Report Model → Renderer
```

| Layer | Responsibility |
|---|---|
| Goal Type | Goal-specific inputs, terminology, milestones and calculations |
| Strategy | High-level strategic intent |
| Variant | Implementation/funding architecture selected for the situation |
| Report Config | Defines what the report should contain and in what order |
| Report Model | Normalized financial/report data |
| PDF Renderer | Common visual rendering and PDF export |

**Rule:** Variant decides the **report architecture**, not the PDF layout.

---

## 2. Variant Selection

Variant selection happens **after Strategy eligibility** and **before report/scenario generation**.

### Selection inputs

- Goal type
- Goal horizon / target date
- Funding gap
- Payment structure
- Recurring vs one-time requirement
- Liquidity requirement
- Debt / EMI constraint
- Credit requirement
- Income-transition requirement
- Multi-goal conflicts

### Selection pattern

```
Strategy eligible
      ↓
Identify funding/protection pattern
      ↓
Match Variant
      ↓
Validate Variant constraints
      ↓
Generate Report Config
```

### Example

```
Education
→ Progressive De-risking
→ Payment-Tranche Glide Path
→ Education + tranche Report Config
→ Common PDF Renderer
```

---

## 3. Canonical Variant Set

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

These are **architecture labels**. SIP, Lumpsum, Bucketing, Laddering, Cash-flow Matching, etc. remain techniques/components—not Variants.

---

## 4. Report Config

Report Config maps:

```
Goal Type + Strategy + Variant → Report Structure
```

A config can define:

- section inclusion
- section order
- section titles
- required data fields
- variant-specific schedules
- tables/charts
- narrative blocks
- scenario presentation
- action-plan presentation

### Example

**Education + Progressive De-risking + Payment-Tranche Glide Path**

Config should request:

1. Goal summary
2. Funding requirement / gap
3. Payment tranches
4. Tranche-wise de-risking schedule
5. Liquidity requirement
6. Residual loan/credit requirement
7. Scenarios
8. Action plan

The config should **not** perform financial calculations or PDF layout.

---

## 5. Canonical Report Model

The Report Model is the renderer-independent output.

Typical sections:

```
Report Metadata
Goal Summary
Strategy Decision
Selected Variant
Funding Analysis
Liquidity / De-risking Schedule
Debt / Credit Analysis
Scenarios
Trade-offs
Action Plan
Constraints / Assumptions
```

### Separation rule

- **Calculations** produce financial outputs.
- **Report Model** normalizes those outputs.
- **Report Config** decides what is shown.
- **Renderer** decides how it looks.

---

## 6. Common PDF Renderer

Use **one shared renderer** for financial planning reports.

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

Renderer must **not** contain:

- Education logic
- Wedding logic
- Retirement logic
- Variant-selection logic
- Financial calculations

### Do not build

```
education_pdf_generator.py
wedding_pdf_generator.py
retirement_pdf_generator.py
variant_x_pdf_generator.py
```

### Build

```
report_engine/
├── renderer
├── section_components
├── report_models
├── report_configs
└── strategy_variant_mappings
```

---

## 7. Example Mappings

| Goal | Strategy | Variant | Report Pattern |
|---|---|---|---|
| Education with staged tuition | Progressive De-risking | Payment-Tranche Glide Path | Corpus → tranches → de-risking → liquidity |
| Recurring travel | Progressive De-risking | Recurring-Cashflow Glide Path | Reserve → withdrawal → refill |
| Retirement | Progressive De-risking | Income-Transition Glide Path | Accumulation → transition → distribution |
| Near-term wedding | Capital Preservation | Full-Goal Preservation | Required corpus → protection → payment readiness |
| Wedding with residual loan | Credit Utilisation | Residual-Gap Bridge | Self-funding → residual gap → financing |
| Home constrained by EMI | Credit Utilisation | EMI-Cap Financing | Down payment → loan capacity → EMI feasibility |

---

## 8. Current → Target

### Current

```
Goal
 ↓
Strategy Version / Run
 ↓
GoalReportService
 ↓
PDF
```

The repository already has working goal-report PDF generation, but multiple report/PDF paths still exist and Variant is not yet a formal report input.

### Target

```
Goal
 ↓
Strategy
 ↓
Variant
 ↓
Canonical Report Model
 ↓
Report Config
 ↓
Common PDF Renderer
 ↓
PDF
```

Existing API contracts should be preserved where practical while migrating report assembly/rendering behind this architecture.

---

## 9. Implementation Order

### Phase 1 — Variant Selector
Create a deterministic selector:

```
select_variant(goal, strategy, financial_context) → Variant
```

### Phase 2 — Report Config Registry
Create:

```
get_report_config(goal_type, strategy, variant) → ReportConfig
```

### Phase 3 — Canonical Report Model
Normalize financial outputs into a renderer-independent model.

### Phase 4 — Common Renderer
Move shared PDF layout/rendering into one engine.

### Phase 5 — Migrate Goal Report
Make the existing Goal Strategy Report use:

```
Strategy → Variant → Report Config → Report Model → Renderer
```

### Phase 6 — Migrate Other Reports
Classify and progressively migrate:

- Complete Financial Plan
- Basket Report
- Summary Report
- Specialized report surfaces

---

## 10. Non-Negotiable Rules

1. **No variant-specific PDF engines.**
2. **No financial calculations inside the renderer.**
3. **Variant must be explicit in report generation.**
4. **Report Config controls structure, not business calculations.**
5. **Report Model is renderer-independent.**
6. **Techniques are not Variants.**
7. **Existing API contracts should remain stable during migration.**
8. **Adding a new goal/variant should normally require configuration and data mapping—not a new PDF engine.**

---

## Definition of Done

The architecture is complete when:

- Variant is an explicit report-generation input.
- Variant selection is deterministic and testable.
- Goal + Strategy + Variant resolves to a Report Config.
- Financial calculations remain outside reporting/rendering.
- A canonical Report Model exists.
- One common PDF renderer handles the report output.
- Existing report endpoints continue to work.
- New goal/variant combinations do not require new PDF generators.
- Regression tests validate report structure and valid PDF output.
