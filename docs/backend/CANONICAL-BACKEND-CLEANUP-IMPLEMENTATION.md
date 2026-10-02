# Canonical Backend Cleanup — Implementation Plan

**Branch:** `backend-audit-cleanup`  
**Scope:** Backend canonicalization, dead/duplicate implementation removal, report-layer consolidation  
**Status:** Audit complete; implementation pending  
**Constraints:** No frontend redesign/change, no Supabase schema changes, no SQL migrations, no git CLI commands, no invented business rules.

---

## 1. Objective

The backend has reached a point where the canonical implementations exist, but legacy/specialized implementations still coexist with them.

The cleanup objective is:

> **One business responsibility → one canonical implementation → one authoritative data flow → no dead duplicate implementation.**

Cleanup must remove code that is no longer part of the current architecture without removing legitimate domain behavior merely because it is named after a specific goal.

---

## 2. Source Blueprint — Required Decision Architecture

The Financial Planning Engine System Blueprint is the architectural baseline for this cleanup.

The source blueprint defines this full decision-support loop:

**Financial State → Goals → Constraints → Proposed Action / Problem → Strategy Engine → Calculation Engine → Scenario Engine → Probability / Uncertainty → Optimization Engine → Explainability → Investor Decision → Updated Financial State**

For the current backend implementation, **Financial Data** is the source layer feeding Financial State, while **Goal Feasibility** is an explicit planning stage derived from goal requirements and available financial resources before strategy evaluation.

Therefore the implementation-level flow is:

**Financial Data → Financial State → Goals → Goal Feasibility → Constraints → Proposed Action / Problem → Strategy Engine → Calculation → Scenarios → Probability / Uncertainty → Optimization / Comparison → Explainability → Decision Options → Investor Decision → Updated Financial State**

A report is a presentation/output layer around canonical decision outputs. It is not an additional business-decision engine.

### Blueprint responsibilities

| Responsibility | Required role |
|---|---|
| Financial Data | Raw investor/family financial reality |
| Financial State | Normalized/calculated current financial reality |
| Goals | Desired future outcomes and flexibility |
| Goal Feasibility | Funding requirement, gap/surplus and required contribution evidence |
| Constraints | What can/cannot change |
| Proposed Action / Problem | What the investor is considering / problem to test |
| Strategy Engine | Generate possible financial paths |
| Calculation Engine | Quantify consequences |
| Scenario Engine | Stress-test strategy outcomes |
| Probability / Uncertainty | Estimate outcome ranges where appropriate |
| Optimization Engine | Compare fit and trade-offs |
| Explainability | Explain why outcomes differ |
| Investor Decision | Investor's final choice |
| Updated Financial State | New reality after action; next planning snapshot |

### Strategy Engine contract

The Strategy Engine is the strategy-building layer, not merely a downstream solution label.

It can generate contribution, goal, capital-deployment, debt, portfolio, cash-flow, combination and withdrawal strategies. Rules and constraints reduce the search space; combinations must not be generated blindly.

Current canonical internal flow:

**Applicability → Eligible Strategy Set → Scenario Generation → Comparison → Architecture Composition → Decision Evaluation → Ranking → Recommendation**

No service may become a second strategy-generation or decision authority.

### Goal Feasibility

The blueprint's Goal Engine responsibilities require the system to derive, where mathematically possible, horizon, funding gap, required return and required contribution/funding requirement before alternative strategies are evaluated.

Goal Feasibility must remain distinct from Strategy Feasibility.

**Goal Feasibility:** Can the defined financial objective be funded under the investor's current/projected financial resources?

**Strategy Feasibility:** Is this specific strategy architecture viable/appropriate under the financial state and constraints?

Eligibility Fit is evidence, not the final investor decision. Conditional strategies may be adapted and re-checked.

### Calculation / Scenario / Optimization / Explainability boundaries

**Calculation** answers what each strategy mathematically produces. Reusable calculations must not be duplicated in services, APIs or reports.

**Scenario** asks what happens when assumptions/conditions change, including return, contribution, step-up, date, repayment or volatility variations.

**Probability / Uncertainty** is conceptually distinct from deterministic scenario calculation. If this capability is not implemented on a path, record it as a gap rather than inventing a substitute.

**Optimization / Comparison** occurs after strategies are generated and evaluated. It compares goal fit, cash-flow, liquidity, debt, portfolio, risk, flexibility, outcome quality and trade-offs. It is not synonymous with maximizing return.

**Explainability** exposes assumptions, evidence, consequences and trade-offs. Report formatting may present this information, but reports must not independently recreate decision logic.

### Report architecture

Individual Goal Decision Report:

**Strategy Run → GoalReportService → Structured Goal Decision Report → PDF**

Consolidated Financial Plan / Multi-Goal Report:

**Per-goal results → Cross-Goal Allocation / Conflict Resolution → Consolidated Financial Plan → Report**

The two report scopes may compose one another but must not duplicate underlying business logic.

### Multi-Goal orchestration

For multiple goals:

**Financial State → Goals → Goal Feasibility → Constraints → Strategy Engine per goal → Cross-Goal Orchestration → Resource Allocation / Conflict Resolution → Consolidated Financial Plan → Report → Investor Decision → Updated Financial State**

The Multi-Goal layer owns prioritisation, shared-resource competition, allocation, liquidity/resource conflicts, cross-goal trade-offs and consolidated plan assembly. It must not duplicate individual-goal Strategy Engine logic.

### Canonical implementation map

| Responsibility | Canonical owner |
|---|---|
| Financial-state calculation | FinancialStateEngine |
| Financial-state persistence | FinancialStateSnapshotRepository |
| Goal definition/calculation | DefinedGoal / Goal domain |
| Goal feasibility evidence | Goal calculation + funding/feasibility outputs |
| Constraint evaluation | RuleEngine + ConstraintAggregator |
| Proposed action/problem | Action / decision-context layer |
| Strategy applicability/generation | Strategy Engine |
| Scenario generation | Strategy Engine scenario module |
| Mathematical calculation | Calculation / strategy calculation layer |
| Probability / uncertainty | Probability / uncertainty layer where implemented |
| Strategy comparison | Strategy Engine comparison module |
| Architecture composition | Strategy Engine composition module |
| Decision evaluation | Strategy Engine decision module |
| Ranking/recommendation | Strategy Engine ranking + recommendation modules |
| Explainability/evidence | Canonical decision/report evidence outputs |
| Individual-goal report | GoalReportService |
| Cross-goal orchestration | Multi-Goal Orchestration layer |
| Consolidated financial plan | FinancialPlanService / consolidated-plan layer |
| Investor selection | Strategy selection/persistence flow |
| Updated-state feedback | Financial-state update / next planning cycle |

### Blueprint-to-code rule

Where a source-blueprint capability is not implemented in code, classify it as an **implementation gap**. Do not silently claim completion and do not invent a new business rule during cleanup.

## 3. Confirmed Legacy Retirement Report Layer

The following files are legacy and are candidates for deletion after reference migration:

### DELETE

- `backend/services/retirement_report_renderer.py`
- `backend/services/retirement_report_pdf.py`
- `backend/services/retirement_report_pdf_service.py`
- `backend/services/retirement_report_exporter.py`

### Why

The current `StrategyService.get_retirement_report()` is already a backward-compatible alias to:

`GoalReportService.build_report()`

The dedicated retirement renderer/PDF stack therefore duplicates functionality that is now provided by the canonical goal report stack.

---

## 4. Required Retirement Cleanup

### 4.1 StrategyService

Remove:

- import of `RetirementReportRenderer`
- `self.report_renderer = RetirementReportRenderer()`

Keep:

- `get_retirement_report()` temporarily as a compatibility alias if required by current API/frontend consumers.

The alias must delegate only to `GoalReportService`.

### 4.2 API

Current canonical routes:

- `GET /api/strategy/runs/{strategy_run_id}/report`
- `GET /api/strategy/runs/{strategy_run_id}/report.pdf`

Current compatibility routes:

- `GET /api/strategy/runs/{strategy_run_id}/retirement-report`
- `GET /api/strategy/runs/{strategy_run_id}/retirement-report.pdf`

Do **not** remove the compatibility routes during this cleanup unless frontend consumers are explicitly migrated.

Instead:

- remove `RetirementReportPDFService` import;
- make the retirement PDF route delegate to `GoalReportService.generate_pdf()`;
- make the retirement JSON route delegate through the canonical report service;
- preserve response compatibility where possible;
- document the retirement routes as compatibility aliases, not separate report implementations.

---

## 5. Test Cleanup

Legacy tests that directly instantiate retirement-only report classes must be migrated.

### Review / migrate

- `backend/tests/test_retirement_report_pdf.py`
- retirement-report portions of `backend/tests/test_retirement_planning_flow.py`
- retirement-report portions of `backend/tests/test_e2e_strategy_flow.py`
- retirement-report portions of `backend/tests/test_strategy_decision_authority.py`

The goal is not to delete coverage. The goal is to move coverage from implementation-specific classes to the canonical contract.

Tests should verify:

1. Retirement is a valid goal type.
2. A retirement StrategyRun can generate a canonical Goal Decision Report.
3. The canonical report can generate a PDF.
4. Generic report generation works for non-retirement goals.
5. Compatibility retirement routes, if retained, produce the canonical report/PDF.
6. No retirement-specific renderer/exporter is required.

---

## 6. Broader Cleanup Audit

Retirement is the first confirmed duplicate layer, but the same audit must be applied to the whole backend.

For every backend responsibility, classify implementations as:

### A — CANONICAL
The implementation currently authoritative for the business responsibility.

### B — COMPATIBILITY
Required temporarily for an existing consumer but delegates to A.

### C — LEGACY
Old implementation that duplicates A and has no required runtime consumer.

### D — DEAD
Unreferenced code with no active architectural role.

### E — DOMAIN LOGIC
Goal-specific behavior that is still legitimate and must not be deleted merely because it contains a goal name.

Only C and D should be deleted.

---

## 7. Audit Targets

### 7.1 Reports

Audit every:

- `*_report_service.py`
- `*_report_renderer.py`
- `*_report_exporter.py`
- `*_report_pdf.py`
- `*_report_pdf_service.py`
- report API route
- report model/schema
- report test

Confirm whether each responsibility has exactly one canonical implementation.

Known report services currently include:

- `goal_report_service.py`
- `financial_plan_service.py`
- `basket_report_service.py`
- retirement-specific report files listed above

Do not assume all three non-retirement services are duplicates. Determine their distinct responsibility and whether they compose the canonical report layer.

---

### 7.2 Strategy Layer

Audit:

- `backend/engines/strategy/`
- `backend/services/strategy_service.py`
- strategy repositories
- strategy schemas/models
- scenario generation
- comparison/ranking
- architecture generation
- what-if scenarios
- strategy selection persistence

Confirm that no older calculation or decision path is still independently producing strategy outputs.

---

### 7.3 Calculation Layer

Identify:

- duplicate future-value/PMT implementations;
- old goal calculators;
- calculation helpers duplicated inside services;
- calculations performed again in reporting code;
- calculations performed in API handlers.

Canonical rule:

> Calculation happens in the calculation/strategy domain layer; reports consume persisted outputs and do not recalculate business decisions.

---

### 7.4 Multi-Goal Layer

Audit:

- `backend/engines/orchestration/`
- `backend/services/multi_goal_planning_service.py`
- basket report generation
- financial-plan generation

Determine which layer owns:

- goal prioritization;
- surplus allocation;
- inter-goal competition;
- aggregate plan;
- per-goal strategy runs;
- consolidated reporting.

There must not be two independent multi-goal orchestration paths.

---

### 7.5 Financial Plan Layer

Audit:

- `FinancialPlanService`
- financial-plan API routes
- financial-plan PDF generation
- any older consolidated-plan implementation.

The final architecture should distinguish:

**Individual Goal Decision Report**

from

**Consolidated Financial Plan / Multi-Goal Report**

They may compose one another, but neither should duplicate the other's business calculations.

---

### 7.6 Schemas / Models

Audit for:

- duplicate response models;
- legacy report dataclasses;
- retirement-only report contracts;
- generic and legacy versions of the same object;
- fields retained only for deleted implementations.

Do not change database schema as part of this cleanup.

---

### 7.7 API Compatibility

For every route, record:

- canonical route;
- compatibility route;
- active frontend consumer;
- service called;
- whether the route can eventually be removed.

No route should call a legacy implementation.

---

### 7.8 Tests

Tests must follow canonical contracts rather than implementation internals.

Remove tests only when they exclusively test deleted code.

Preserve equivalent behavioral coverage against canonical services.

---

## 8. Dependency-First Deletion Rule

Never delete a file merely because it looks obsolete.

For every candidate deletion:

1. Search every repository reference.
2. Identify imports.
3. Identify runtime callers.
4. Identify API callers.
5. Identify frontend callers.
6. Identify tests.
7. Determine whether the consumer should migrate or remain compatible.
8. Migrate consumers.
9. Re-search the repository.
10. Delete only after zero required runtime references remain.

Final condition:

`Deleted File → 0 Required References`

---

## 9. Canonicalization Rules

### Rule 1 — One authority

There must be one authoritative implementation per business responsibility.

### Rule 2 — Services orchestrate

Services coordinate repositories and engines. They must not contain duplicate business calculations.

### Rule 3 — Engines calculate/decide

Engines own business rules, calculations, eligibility, strategy construction, and decision logic appropriate to their domain.

### Rule 4 — Reports consume

Report generation consumes canonical persisted outputs. It must not silently create an alternative calculation path.

### Rule 5 — Exporters are presentation adapters

PDF/HTML exporters should serialize canonical report objects. They must not become alternative business-logic authorities.

### Rule 6 — Compatibility is allowed, duplication is not

A compatibility endpoint/helper is acceptable only if it delegates to the canonical implementation.

### Rule 7 — No speculative cleanup

Do not delete code because it appears old without tracing its consumers and architectural responsibility.

---

## 10. Cleanup Order

Execute in this order:

### Phase 1 — Inventory

Create a complete backend inventory of:

- services;
- engines;
- repositories;
- schemas;
- models;
- API routes;
- report generators;
- exporters;
- tests.

### Phase 2 — Dependency graph

For every duplicate/legacy candidate record:

`Producer → Consumer → Consumer Type → Canonical Replacement`

### Phase 3 — Canonical mapping

Mark each implementation:

`CANONICAL | COMPATIBILITY | LEGACY | DEAD | DOMAIN LOGIC`

### Phase 4 — Consumer migration

Move required consumers to canonical services before deletion.

### Phase 5 — Delete

Delete only confirmed LEGACY/DEAD implementations.

### Phase 6 — Reference sweep

Search the repository again for:

- deleted module names;
- deleted classes;
- old route/service names;
- duplicate calculation functions.

### Phase 7 — Verification

Run available backend tests/checks.

If CI is unavailable, explicitly record verification as unavailable rather than claiming success.

---

## 11. Explicit Non-Goals

This cleanup must **not**:

- modify frontend architecture;
- redesign frontend;
- modify Supabase schema;
- create SQL migrations;
- run SQL migrations;
- invent business rules;
- change goal taxonomy;
- change Strategy Engine business behavior unless required solely to remove a confirmed duplicate implementation;
- remove valid retirement domain logic;
- remove compatibility routes that active frontend code still requires without migration planning.

---

## 12. Completion Criteria

Cleanup is complete only when:

- [ ] Every backend business responsibility has one canonical implementation.
- [ ] Legacy retirement report implementation is removed.
- [ ] No API route calls a deleted/legacy report service.
- [ ] No active service imports deleted report modules.
- [ ] No tests require deleted implementation classes.
- [ ] Report JSON and PDF use the canonical GoalReportService.
- [ ] Individual-goal and consolidated financial-plan responsibilities are clearly separated.
- [ ] Multi-goal orchestration has one authoritative path.
- [ ] Duplicate calculation paths are removed or explicitly justified.
- [ ] Repository-wide reference sweep is clean.
- [ ] Backend verification results are recorded honestly.
- [ ] Frontend and database remain untouched.

---

## 13. Immediate Next Implementation Batch

The first concrete cleanup batch should be:

1. Remove retirement renderer/exporter/PDF service/PDF exporter dependencies.
2. Redirect the compatibility retirement PDF route to `GoalReportService.generate_pdf()`.
3. Remove the unused retirement renderer initialization from `StrategyService`.
4. Migrate retirement report tests to canonical report tests.
5. Re-run repository reference audit.
6. Confirm the four retirement implementation files have zero required references.
7. Then continue the same audit methodology across financial-plan, basket-report, calculation, orchestration, and other backend services.

This document is an implementation plan, not a claim that the cleanup has already been executed.
