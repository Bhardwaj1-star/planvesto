# Planvesto Backend — Existing vs Target Architecture Gap & Refactor Specification

**Status:** Backend refactor specification  
**Target branch:** `backend-audit-cleanup`  
**Scope:** Backend/domain architecture and implementation planning  
**Basis:** Current repository inspection + existing backend architecture documents  
**Explicit exclusions:** Frontend redesign, Supabase schema changes, SQL migrations, Git CLI commands, and unapproved business-rule invention.

---

## 1. Purpose

This document identifies the gap between the **existing backend structure** and the **currently locked Planvesto architecture**, then defines the precise refactor boundary.

The objective is **not to rewrite the existing backend**.

> **Preserve the existing single-goal Strategy Engine; build the missing multi-goal decision architecture around it.**

---

## 2. Existing Backend — What Already Exists

The current backend already contains:

- API layer
- Service layer
- Supabase/data repositories
- Domain models and schemas
- Goal calculation engine
- Strategy Library/catalog
- Single-goal Strategy Engine
- Strategy applicability/rule engine
- Scenario generation
- Strategy architecture composition
- Decision evaluation
- Ranking and recommendation
- Strategy version/selection flow
- Planning-context orchestration
- MoneyWheel rule definitions

### Existing single-goal Strategy Engine

`backend/engines/strategy/engine.py` already performs:

```
Defined Goal
    ↓
Strategy Applicability
    ↓
Scenarios
    ↓
Architecture Composition
    ↓
Decision Evaluation
    ↓
Ranking
    ↓
Recommendation
```

This remains the **per-goal Strategy Engine**.

It must not become the multi-goal allocator.

---

## 3. Target Architecture

```
Financial Data
      ↓
MoneyWheel
      ↓
Financial Situation

Risk Data
      ↓
Risk Profiler
      ↓
Strategic Asset Allocation
      ↓
Sub-Asset Allocation
      ↓
Product Category
      ↓
Product Selection

Goal Data
      ↓
Goal Requirement / Horizon / Feasibility

Goal + Problem + Constraints
      ↓
Multi-Goal Orchestrator
      ↓
Single-Goal Strategy Engine
      ↓
Goal-Level Strategy / Scenario / Decision
      ↓
Cross-Goal Resource Allocation
      ↓
Consolidated Financial Plan
      ↓
Report / Decision Output
```

Responsibility split:

- **MoneyWheel:** diagnose what is financially happening.
- **Risk Profiler:** determine investor risk structure and strategic allocation.
- **Goal Engine:** determine what money must accomplish and when.
- **Investment Engine:** determine how investable capital is allocated and implemented.
- **Strategy Builder:** solve a specific financial problem.
- **Product Selection:** identify actual products implementing approved allocation.

These layers may exchange facts, but they must not be collapsed into one engine.

---

## 4. Gap Summary

| Area | Existing | Target | Gap |
|---|---|---|---|
| Financial State | Repository/context exists | Canonical financial context | Minor contract cleanup |
| MoneyWheel | Ratio/rule definitions | Metrics → relationships → situation → story | **Refactor** |
| Goal Engine | Goal calculations exist | Requirement/horizon/feasibility | **Contract cleanup** |
| Strategy Library | Catalog exists | Hybrid + personalized | **Rule/catalog cleanup** |
| Single-Goal Strategy Engine | Exists | Same responsibility | **Preserve** |
| Planning Context | Exists | Context assembly only | **Preserve / narrow** |
| Multi-Goal Orchestrator | Not complete | Cross-goal coordination | **Major gap** |
| Resource Allocation | Not complete | Shared surplus/assets/liquidity allocation | **Missing** |
| Consolidated Financial Plan | Not canonical | Single final planning object | **Missing** |
| Investment Engine | No separate layer | Allocation → implementation | **Missing / separate scope** |
| Product Selection | Not implemented | Product implementation layer | **Separate scope** |
| Scenario Engine | Deterministic scenarios exist | Scenario analysis | **Partial** |
| Probability Engine | No probability model | Probability/uncertainty | **Missing** |
| Optimization | Ranking exists | Cross-goal optimization | **Partial / missing** |
| Explainability | Recommendation/rule evidence exists | Structured decision explanation | **Partial** |
| Reporting | Renderers exist | Consume finalized Financial Plan | **Refactor boundary** |

---

## 5. MoneyWheel Gap

### Existing

`backend/rules/moneywheel.py` already contains the core ratio definitions:

- Savings Rate
- Liquid Asset Ratio
- Debt-to-Income Ratio
- Leverage Ratio
- Financial Asset Ratio
- Insurance Coverage Ratio
- Goal Funding Ratio
- Future Funding Ratio
- Required Rate of Return

Separate coverage definitions:

- Expense Coverage
- Emergency Coverage

### Target

```
Financial State
    ↓
Metrics
    ↓
Relationships / Diagnostics
    ↓
Financial Situation
    ↓
Financial Story
```

MoneyWheel should not become a generic health score and should not choose a Strategy.

### Refactor

Separate:

1. metric calculation;
2. diagnostic relationships;
3. financial situation;
4. financial story.

MoneyWheel may provide financial context/evidence to downstream planning, but it does not structurally determine Strategy Builder output.

---

## 6. Goal Engine Gap

The existing Goal Engine already handles:

- target calculation;
- duration;
- inflation;
- asset mapping;
- projected asset value;
- funding gap;
- required monthly contribution;
- specialized goal calculations.

Required boundary:

```
Goal Data
   ↓
Future Requirement
   ↓
Current / Projected Funding
   ↓
Funding Gap
   ↓
Feasibility Context
```

Goal Engine remains responsible for **goal mathematics**, not strategy selection or cross-goal allocation.

---

## 7. Strategy Library Gap

The current Strategy Library contains strategy definitions and applicability metadata.

Current strategy scope:

- Goal Funding
- Progressive De-risking
- Capital Preservation
- Debt Reduction
- Credit Utilisation

Keep:

```
Strategy
≠ Technique
≠ Allocation
≠ Product Selection
```

Techniques include:

- Bucketing
- Glide Path
- Cashflow Matching
- Laddering
- Tax-efficient sequencing

### Refactor

Clean stale/legacy applicability and decision rules so:

```
Strategy Library
      ↓
Applicability Rules
      ↓
Applicable Strategies
```

is deterministic and based only on approved business rules.

Do not invent missing rules.

---

## 8. Single-Goal Strategy Engine — Preserve

The existing Strategy Engine is the strongest reusable part of the current architecture.

Its responsibility remains:

> Given one DefinedGoal and its context, determine applicable strategies, scenarios, architectures and the goal-level recommendation.

It should continue to handle:

- applicability;
- scenario generation;
- architecture composition;
- decision evaluation;
- ranking;
- recommendation.

### Do not move into it

- multi-goal resource allocation;
- portfolio-level allocation;
- cross-goal optimization;
- product selection;
- risk profiling.

---

## 9. Major Gap — Multi-Goal Orchestrator

This is the primary missing backend layer.

Target:

```
Multi-Goal Planning Service
          ↓
Multi-Goal Orchestrator
          ↓
     ┌────┼────┐
   Goal 1 Goal 2 Goal 3
     ↓    ↓    ↓
 Single Single Single
 Strategy Strategy Strategy
 Engine Engine Engine
     └────┼────┘
          ↓
 Cross-Goal Coordination
```

Responsibilities:

1. Load financial context.
2. Load selected goals.
3. Preserve client-selected priority.
4. Run the existing Strategy Engine independently for each goal.
5. Collect goal-level feasibility/funding/strategy results.
6. Detect competition for shared resources.
7. Apply explicit financial constraints.
8. Resolve conflicts deterministically.
9. Preserve client priority and system-resolved outcome.
10. Produce consolidated planning output.

The existing `PlanningOrchestrationService` should remain context/module-availability orchestration, not become the decision engine.

---

## 10. Missing — Shared Resource Allocation

A multi-goal plan needs a separate allocator.

Shared resources may include:

- future cash-flow surplus;
- existing assets;
- available liquidity;
- other explicitly supported funding sources.

Example:

```
Available surplus = ₹50K
Goal A requirement = ₹25K
Goal B requirement = ₹20K
Goal C requirement = ₹15K
Total requirement = ₹60K
Available = ₹50K
```

The single-goal Strategy Engine cannot resolve this conflict.

The allocator must:

- identify competition;
- apply client priority;
- apply approved constraints;
- resolve partial funding;
- identify infeasible combinations;
- preserve decision evidence.

It must never silently change client priority.

---

## 11. Client Priority vs System Resolution

The backend must preserve two distinct values:

```
client_selected_priority
system_resolved_outcome
```

If an approved financial rule requires a different allocation outcome:

- client priority remains recorded;
- system resolution is recorded separately;
- reason/evidence is preserved;
- final reporting explains the difference.

The system must not imply that the client manually changed their priority.

---

## 12. Missing — Consolidated Financial Plan

A canonical backend Financial Plan object is required.

Minimum conceptual contents:

```
FinancialPlan
├── Financial Context
├── MoneyWheel Findings
├── Goals
├── Client Priorities
├── Resolved Allocation
├── Goal-Level Strategies
├── Funding Requirements
├── Feasibility
├── Constraints / Diagnostics
├── Cross-Goal Trade-offs
├── Unresolved Limitations
└── Actions
```

This becomes the **single source for reporting**.

Reporting must not independently recalculate financial decisions.

---

## 13. Investment Engine Boundary

Investment Planning is separate from Strategy Builder.

Target:

```
Risk Profiler
      ↓
Strategic Asset Allocation
      ↓
Sub-Asset Allocation
      ↓
Product Category
      ↓
Product Selection
      ↓
Implementation
```

This should not be inserted into the current Strategy Engine.

Goal context may constrain implementation through horizon/liquidity requirements, but must not silently overwrite investor risk profile.

This is a separate implementation scope from the current multi-goal refactor.

---

## 14. Scenario / Probability / Optimization Gap

### Scenario Engine

Existing scenario generation is usable as a deterministic baseline.

Current implementation explicitly does not claim statistical probability:

```
probability_of_success = None
success_probability_method = "not_estimated"
```

**Status: partial/usable.**

### Probability Engine

No actual probability/distribution/Monte Carlo layer currently exists.

**Status: missing.**

### Optimization

Current ranking is not equivalent to full multi-goal optimization.

Cross-goal resource optimization remains part of orchestration/allocation work.

**Status: partial.**

---

## 15. Reporting Boundary

Current report/rendering code must not become a second decision engine.

Target:

```
Financial Plan
     ↓
Structured Report Data
     ↓
PDF / Client Report
```

Business calculations and decision rules happen before rendering.

The report should consume:

- goal-level strategies;
- funding outcomes;
- allocation;
- constraints;
- client priority;
- system resolution;
- trade-offs;
- feasibility;
- required actions.

---

## 16. Refactor Architecture

Recommended responsibility:

```
backend/
│
├── api/
│   └── orchestration.py
│
├── services/
│   ├── planning_orchestration_service.py
│   ├── multi_goal_planning_service.py       ← cross-goal application layer
│   └── strategy_service.py
│
├── engines/
│   ├── goal/                                ← goal mathematics
│   ├── strategy/                            ← existing single-goal engine
│   ├── orchestration/                       ← NEW cross-goal logic
│   ├── rules/                               ← rule evaluation
│   └── calculation/                         ← pure calculations
│
├── rules/
│   ├── moneywheel.py
│   ├── goals.py
│   └── strategy_decision.py
│
├── library/
│   └── strategies/
│
├── models/
└── schemas/
```

Do not introduce a parallel architecture where an existing responsibility already has a valid implementation.

---

## 17. Implementation Order

### Phase 1 — Contract Freeze
Freeze boundaries between Financial State, MoneyWheel, Goal Engine, Strategy Engine and Orchestrator.

### Phase 2 — MoneyWheel
Complete metric output, diagnostic relationships, financial situation and financial story.

### Phase 3 — Strategy/Rule Cleanup
Verify strategy applicability, goal-type mappings, stale rule IDs, rule roles and missing-rule handling.

### Phase 4 — Multi-Goal Orchestrator
Build context loading, goal collection, per-goal Strategy Engine invocation and result collection.

### Phase 5 — Resource Allocation
Build shared-resource detection, priority handling, constraint handling, conflict resolution, partial and infeasible outcomes.

### Phase 6 — Consolidated Financial Plan
Create the canonical final planning object.

### Phase 7 — Reporting
Make report generation consume the Financial Plan.

### Phase 8 — API Integration

```
API Request
 → Financial Context
 → Goals
 → Single-Goal Strategy Engine
 → Constraint Evaluation
 → Multi-Goal Allocation
 → Consolidated Financial Plan
 → Report
```

### Phase 9 — QA
Regression + unit + integration + end-to-end tests.

---

## 18. Testing Requirements

Minimum backend tests:

1. One-goal regression.
2. Multiple independent goals.
3. Multiple goals competing for the same surplus.
4. Client priority preserved when no conflict exists.
5. Constraint-driven allocation change.
6. Client priority vs system-resolved outcome traceability.
7. Partial funding.
8. Infeasible combination.
9. Report explanation of system resolution.
10. Authentication/ownership.
11. End-to-end API flow.

A component is not complete merely because its file exists. Its documented behavior must be implemented and tested.

---

## 19. Explicit Non-Scope

Do not:

- redesign frontend;
- modify Supabase schema;
- create SQL migrations;
- rewrite the existing single-goal Strategy Engine;
- implement product selection in this refactor;
- redesign Risk Profiler in this refactor;
- invent financial-ratio thresholds;
- silently change client priorities;
- hide infeasible goals or cross-goal trade-offs.

---

## 20. Definition of Done

The backend refactor is complete when an authenticated multi-goal request can:

1. Load investor financial context.
2. Load selected goals.
3. Evaluate each goal through the existing single-goal Strategy Engine.
4. Evaluate relevant approved constraints.
5. Detect competition for shared resources.
6. Resolve resource conflicts deterministically.
7. Preserve client priority and any system resolution.
8. Produce one consolidated Financial Plan.
9. Generate the final report from that Financial Plan.
10. Pass required regression/integration/end-to-end tests.

No frontend or database-schema change is required for this architecture.

---

## Final Principle

> **Do not replace the existing core. Add the missing decision layer around it.**

The existing backend already has usable Goal and single-goal Strategy machinery. The principal architectural gap is the layer that coordinates multiple goals, shared resources and final consolidated decision output.
