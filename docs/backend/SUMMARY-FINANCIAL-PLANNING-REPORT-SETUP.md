# Summary Financial Planning Report — Setup Specification

## 1. Purpose

Define the setup and boundaries for the **Summary Financial Planning Report**.

This document is a specification/setup document only. It does not implement the report.

## 2. Report Role

The Summary Financial Planning Report is a client-facing, high-level view of the investor's financial planning position.

It should answer:

> **"Meri current financial position kya hai, mere goals ki situation kya hai, mera investment risk profile kya hai, aur investment position broadly kya hai?"**

It is a summary output, not the detailed financial planning analysis.

## 3. Authoritative Inputs

The report will consume outputs from exactly these four planning components:

1. **MoneyWheel**
   - Current financial situation and financial diagnosis.
2. **Risk Profiler**
   - Risk Required, Risk Capacity, Risk Tolerance and resulting Risk Profile.
3. **Goal Engine**
   - Goal targets, timelines, funding position, funding gaps and required contributions.
4. **Investment Engine**
   - Investment allocation / implementation position.

### Explicitly out of scope

The Summary Report will not depend on:

- Strategy Builder
- Strategy Engine
- Multi-Goal Orchestration
- Product Selection Engine
- Insurance Suitability Engine

These may be incorporated into later planning/reporting layers.

## 4. High-Level Data Flow

```
Financial Data
     ↓
MoneyWheel
Risk Profiler
Goal Engine
Investment Engine
     ↓
Summary Financial Report Service
     ↓
Summary Report Model
     ↓
PDF Renderer
     ↓
Downloadable Summary Financial Planning Report
```

The report layer must consume engine outputs. It must not independently recreate financial calculations.

## 5. Proposed Report Sections

The initial structure is:

### A. Financial Snapshot
High-level investor financial position.

### B. Financial Situation
MoneyWheel-derived financial condition and key observations.

### C. Risk Profile
Risk Required + Risk Capacity + Risk Tolerance + resulting risk profile.

### D. Goals & Funding
Goal Engine-derived goal status, target, timeline, funding position and gap.

### E. Investment Position
Investment Engine-derived allocation / investment position.

### F. Key Observations
Cross-component observations supported by the four engine outputs.

### G. Key Actions
High-level planning actions derived from the available outputs.

The exact rules, thresholds, wording and action logic are intentionally **not finalized** in this document.

## 6. Technical Components

Planned backend components:

- Summary Financial Report Service
- Summary Report Model / schema
- Summary PDF Renderer
- Summary Report API endpoints
- Automated tests

Existing PDF/download infrastructure may be reused where appropriate, but the new summary report must have its own clear report contract.

## 7. Proposed API Surface

### JSON

`GET /api/financial-planning/summary?planning_unit_id={id}`

Returns the structured Summary Financial Planning Report.

### PDF

`GET /api/financial-planning/summary.pdf?planning_unit_id={id}`

Returns the downloadable PDF.

Exact route naming can be finalized during implementation.

## 8. Architecture Rules

1. No financial calculation should be duplicated inside the report layer.
2. MoneyWheel remains responsible for financial-situation diagnosis.
3. Risk Profiler remains responsible for risk-profile construction.
4. Goal Engine remains responsible for goal calculations.
5. Investment Engine remains responsible for investment implementation/allocation outputs.
6. The report is an aggregation/presentation layer, not a decision engine.
7. Missing or unavailable engine data must be represented explicitly; the report must not invent values.
8. The report must preserve the provenance of important outputs where practical.
9. Report generation must be deterministic for the same planning state and engine outputs.
10. Detailed-report requirements will be handled separately.

## 9. Business Rules — Pending

The following must be decided before implementation:

- Which MoneyWheel metrics appear in the summary.
- How MoneyWheel metrics become "key observations."
- Exact Risk Profile representation.
- How Goal Engine outputs are summarized.
- Which Investment Engine outputs appear.
- How cross-engine observations are generated.
- What qualifies as a key action.
- Missing-data behavior.
- Data-quality/confidence display.
- Status labels and interpretation rules.
- Report ordering and prioritization.
- PDF presentation rules.

## 10. Definition of Done

The Summary Financial Planning Report is considered ready when:

1. The four authoritative engines provide the required inputs.
2. A stable summary report contract exists.
3. The report service consumes those four outputs.
4. No report-layer financial calculations duplicate engine logic.
5. JSON report generation works.
6. PDF generation works.
7. PDF download works through an authenticated API.
8. Tests cover normal, partial-data and failure scenarios.
9. Multi-Goal Orchestration and Strategy Builder are not required for this report.
