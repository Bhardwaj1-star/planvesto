# Retirement Planning Flow Specification

## Purpose

Define the intended end-to-end retirement-planning experience and the technical contract needed to take an investor from a completed retirement goal through strategy selection to a visible retirement report and downloadable PDF.

This document is the authoritative implementation guide for the retirement-planning flow. It complements `docs/STRATEGY_CONVERSION_SPEC.md`; it does not replace the strategy-engine specification.

---

## 1. Target User Flow

```text
Onboarding / Financial State
        ↓
Retirement Goal
        ↓
Strategy Builder
        ↓
Compare eligible strategy architectures
        ↓
Select strategy + implementation parameters
        ↓
Strategy Version / Approval lifecycle
        ↓
Action Plan
        ↓
Retirement Report
        ↓
Download PDF
```

The user should not need to discover internal routes manually. A completed retirement-planning flow must expose a clear next action at each stage.

---

## 2. Core Principles

1. Retirement planning is goal-first and strategy-first.
2. The Strategy Engine decides which strategy architectures are applicable; legacy Safety/Liquidity/Growth/Flexibility scores must not act as the decision authority.
3. The retirement report must consume the persisted final strategy/recommendation contract rather than independently recomputing a different recommendation.
4. Web report and PDF must represent the same underlying report data.
5. No Supabase schema changes or migrations are required for this flow unless explicitly approved later.
6. Internal lifecycle routes may exist for implementation, but the primary investor UX should remain simple and contextual.

---

## 3. Strategy Builder Completion

After a retirement goal is loaded, Strategy Builder must:

- load the latest valid Defined Goal;
- build or load the Strategy Run;
- show eligible strategy architectures;
- explain goal fit, feasibility, constraints, trade-offs, assumptions and implementation techniques;
- allow the investor to select an architecture and its editable implementation parameters;
- persist the selected strategy version.

The Strategy Builder should provide a clear continuation action after a successful selection.

### Required post-selection state

The UI must clearly communicate that the strategy has been saved and expose the next lifecycle action. For retirement planning, the eventual destination is the retirement report.

---

## 4. Approval / Action Plan Lifecycle

`Strategy Approval`, `Strategy Edit`, `Custom Scenarios`, and `Strategy History` are implementation/lifecycle capabilities, not necessarily primary navigation destinations.

They must not be deleted blindly because they can participate in strategy versioning and lifecycle management.

Recommended investor-facing flow:

```text
Build & Compare
   ↓
Select Architecture
   ↓
Approval / Version confirmation (when required)
   ↓
Action Plan
   ↓
Retirement Report
```

Optional capabilities such as Custom Scenarios and History should remain accessible contextually rather than cluttering the primary navigation.

---

## 5. Retirement Report Contract

The retirement report must be generated from the final persisted Strategy Run / Strategy Recommendation.

It should include, where available:

- investor / planning context;
- retirement goal summary;
- current financial state relevant to retirement;
- selected strategy architecture;
- why the strategy fits the goal;
- feasibility status;
- important constraints;
- assumptions;
- trade-offs;
- implementation direction / techniques;
- relevant scenarios or stress-test summary;
- recommendation reasoning;
- alternatives where applicable;
- implementation/action direction;
- report metadata/version information.

The report must not reintroduce the legacy composite-score presentation as the strategy decision authority.

---

## 6. Web Report

Route: `/investor/retirement-report`

The web report should be reachable after the retirement strategy flow is completed without requiring the user to manually construct a URL.

The page must:

1. Load the persisted retirement report for the relevant Strategy Run.
2. Render the report using the same data contract used by the PDF exporter.
3. Show a visible `Download PDF` action.
4. Display a useful error state when the report cannot be loaded.
5. Prevent duplicate download actions while PDF generation is in progress.

---

## 7. PDF Export

The backend already has a retirement-report PDF service/exporter and an API endpoint for PDF generation.

Expected API capability:

```text
GET /api/strategy/runs/{strategy_run_id}/retirement-report.pdf?planning_unit_id=...
```

The frontend download action must:

1. identify the current Strategy Run;
2. request the PDF endpoint with the required planning-unit context and authorization;
3. receive PDF bytes;
4. trigger a browser download with a meaningful filename;
5. restore the button to its normal state after completion or failure.

The PDF must be generated from the same retirement report model rendered by the web view.

---

## 8. Completion CTA Requirement

The critical UX requirement is:

> Once retirement planning has successfully produced and persisted a valid strategy result, the investor must have an obvious path to `View Retirement Report`, and the report must expose `Download PDF`.

Do not rely only on a hidden route or sidebar entry.

Recommended CTA behavior:

```text
Strategy selected successfully
        ↓
[View Retirement Report]
        ↓
Retirement Report
        ↓
[Download PDF]
```

If an approval/action-plan step is mandatory in the current lifecycle, the CTA should point to the next required step and then expose the report when that step is complete.

---

## 9. Navigation Cleanup

Primary investor navigation should remain focused on the product's core journey.

Recommended primary structure:

```text
Overview
  Dashboard

Plan
  Goal Planner

Decide
  Strategy Builder

Implement
  Action Plan

Review
  Goal History
  Strategy History
  Investor Diary

Account
  Profile
```

Pages such as Strategy Edit, Strategy Approval, and Custom Scenarios should not be exposed as unnecessary primary navigation items. They should remain available only where their lifecycle context requires them.

Other existing investor pages must be classified by actual dependency before deletion. Do not remove a route merely because it is absent from the sidebar.

---

## 10. Unnecessary-Page Cleanup Rules

Before deleting any route/page:

- search all frontend links and router navigation;
- search backend/API references;
- search tests and E2E flows;
- check whether it represents immutable strategy versioning or approval state;
- check whether another page links to it contextually;
- remove dead imports and dead navigation entries;
- run frontend build and backend tests.

Classification should be:

- **KEEP** — required product capability;
- **CONTEXTUAL** — keep route but remove from primary navigation;
- **MERGE** — capability should be absorbed into another screen;
- **REMOVE** — demonstrably unused and not part of the intended lifecycle.

---

## 11. Acceptance Tests

The implementation is complete only when all of the following are true:

### Strategy flow
- Retirement goal can be saved.
- Strategy Builder loads the saved retirement goal.
- Eligible retirement strategies are produced.
- Legacy dimension scores are not the decision authority.
- Strategy architecture and recommendation information are visible.
- Strategy selection persists successfully.

### Report flow
- A valid final Strategy Run can produce a retirement report.
- Strategy Builder exposes the appropriate next-step/report CTA.
- Retirement Report page loads successfully.
- Report reflects the final Strategy Run / Recommendation.
- `Download PDF` is visible.
- PDF endpoint returns a valid PDF.
- Browser download completes with a meaningful filename.

### Regression
- Existing backend tests pass.
- Frontend build/type checking passes.
- PDF/report regression tests pass.
- CI is green.

---

## 12. Implementation Order

Execute in this order to avoid large, ambiguous changes:

1. Audit current retirement Goal → Strategy Run lifecycle.
2. Verify strategy selection persistence.
3. Verify the report API and PDF endpoint against the persisted Strategy Run.
4. Wire the missing completion CTA/navigation.
5. Verify web report rendering.
6. Verify PDF download end-to-end.
7. Audit all investor routes and classify KEEP / CONTEXTUAL / MERGE / REMOVE.
8. Remove only demonstrably unnecessary primary navigation/routes.
9. Run backend tests + frontend build.
10. Run CI and perform a manual retirement-planning smoke test.

---

## 13. Explicit Non-Goals

- No new financial-planning calculations in this document.
- No replacement of the Strategy Engine specification.
- No Supabase schema redesign.
- No broad frontend redesign.
- No deletion of lifecycle pages without dependency evidence.

The goal is to make the existing retirement planning system coherent, complete, navigable, and actually usable through report generation and PDF download.
