# Planvesto — Strategy & Goal Decision System
## Implementation Status, Architecture, Route Map & Remaining Build Plan

**Repository:** `Bhardwaj1-star/planvesto`  
**Branch:** `backend-audit-cleanup`  
**Document status:** Working implementation map  
**Scope:** Backend Strategy Builder, Goal Feasibility, Constraints, Scenario Engine, Decision Output and Goal Decision Reports

---

## 1. Executive Summary

Planvesto ka current backend direction ek simple calculator ya portfolio recommender nahi hai.

Target system:

`Financial Data → Financial State → Goals → Constraints → Strategy Engine → Scenarios → Comparison → Decision Support → Report → Investor Decision`

The central principle is:

> **System investor ke liye final financial decision nahi leta. System financially meaningful alternatives construct, calculate, compare aur explain karta hai; final decision investor ka hota hai.**

Current implementation mein is architecture ke major foundations already exist:

- Financial State context
- MoneyWheel diagnostic layer
- Risk Profiler constraint input
- Goal Engine / DefinedGoal
- Goal feasibility
- Goal funding solution variants
- Canonical rules
- Canonical strategies
- Canonical techniques
- Canonical strategy variants
- Canonical components
- Strategy solution matrix
- Centralized ConstraintSet
- Strategy applicability / eligibility
- Strategy composition / architecture
- Baseline scenarios
- Goal Funding scenario variants
- Strategy decision evaluation
- Rankings / recommendation
- Deterministic What-if scenarios
- Strategy Run persistence
- Goal Decision Report service
- Goal Decision Report PDF generation
- API routes for JSON report and PDF download
- Tests covering the major layers

Important: **CI verification is intentionally not part of this document's completion claim.**

---

# 2. Original Product Decision

## 2.1 Strategy Builder ka purpose

Strategy Builder ka kaam:

1. Current financial state ko samajhna.
2. Goal requirements ko understand karna.
3. Constraints identify karna.
4. Financial problem ke liye applicable strategies identify karna.
5. Har strategy ke andar possible solutions / variants generate karna.
6. Consequences calculate karna.
7. Scenarios compare karna.
8. Trade-offs explain karna.
9. Investor ko decision-ready output dena.

Strategy Builder ko:

- generic portfolio builder nahi banna,
- product selector nahi banna,
- risk profiler replace nahi karna,
- investor ke goals khud decide nahi karne,
- sirf highest-return option choose nahi karna.

---

# 3. Locked System Architecture

## 3.1 Core financial planning architecture

```
Financial Data
     ↓
Financial State
     ↓
 ┌───────────────┬───────────────┐
 ↓               ↓               ↓
MoneyWheel    Risk Profiler   Goal Engine
 ↓               ↓               ↓
Financial      Risk            Goal
Constraints    Constraints     Requirements
 └───────────────┴───────────────┘
                 ↓
       Centralized ConstraintSet
                 ↓
          Strategy Engine
                 ↓
       Strategy Architectures
                 ↓
          Baseline Scenarios
                 ↓
       Calculation / Comparison
                 ↓
       Decision Evaluation
                 ↓
       Ranking / Recommendation
                 ↓
       Investor Decision
                 ↓
              Report
```

What-if analysis is a separate sensitivity layer:

```
Selected / evaluated baseline strategies
                 ↓
       What-if Scenario Generator
                 ↓
      Sensitivity / Trade-off Output
```

What-if scenarios **baseline decision ranking ko replace nahi karte**.

---

# 4. Core Domain Boundaries

| Component | Owns | Does not own |
|---|---|---|
| Financial State | Current financial reality | Recommendations |
| Canonical Calculation Layer | Reusable derived financial facts | Domain decisions |
| MoneyWheel | Financial diagnosis | Strategy/product selection |
| Risk Profiler | Risk capacity/required/tolerance structure | Goal funding |
| Goal Engine | Goal requirement, calculation, feasibility | Portfolio construction |
| Strategy Builder | Specific financial problem solving | Generic portfolio construction |
| Investment Engine | Capital allocation / implementation structure | Financial diagnosis |
| Product Selection | Actual financial products | Risk profiling |
| Financial Plan | Consolidated planning output | Raw calculation ownership |
| Report | Presentation / decision explanation | Decision logic |

Reference ontology:
`docs/architecture/FINANCIAL-PLANNING-ONTOLOGY.md`

---

# 5. Goal Engine and Goal Feasibility

## Responsibility

Goal Engine answers:

> Future mein kya accomplish karna hai, kab, kitna aur current resources se kitna funded hai?

A `DefinedGoal` contains the goal calculation and funding state, including:

- future target
- mapped assets
- projected mapped asset value
- funding gap
- funding status
- required monthly contribution
- funding return assumption
- feasibility status
- available monthly surplus
- monthly contribution surplus gap
- feasibility reason
- funding strategies

## Feasibility states

- `feasible`
- `constrained`
- `infeasible`
- `unknown`

Feasibility is not the final strategy decision.

### Current logic

Latest family Financial State snapshot se:

`investable_surplus_monthly`

liya jata hai.

Then:

- Funding gap <= 0 → feasible
- Required contribution <= available surplus → feasible
- Required contribution > surplus but surplus > 0 → constrained
- Surplus <= 0 → infeasible
- Required state unavailable → unknown

This is a **goal feasibility diagnostic**, not a strategy selection mechanism.

Relevant implementation:

- `backend/models/defined_goal.py`
- `backend/services/goal_service.py`
- `backend/engines/goal/...`
- `backend/data/goal_repository.py`

---

# 6. Goal Funding Architecture

A key business decision was:

> SIP, Lumpsum, Step-up SIP etc. ko separate top-level strategies nahi banana.

They are **funding variants / solutions of one Strategy: Goal Funding.**

## Goal Funding

Canonical strategy:

`strat-goal-funding`

Current variants:

1. Existing Assets
2. SIP
3. Lumpsum
4. Lumpsum + SIP
5. Lumpsum + Step-up SIP
6. Step-up SIP

These are generated by:

`backend/engines/goal/funding_strategies.py`

The engine determines:

- required lumpsum
- required monthly contribution
- starting monthly contribution
- annual step-up
- remaining funding gap
- feasibility status
- explanation / reason

### Why this architecture

Otherwise Strategy Library mein:

- SIP
- Lumpsum
- Step-up SIP
- Lumpsum + SIP

alag strategies ban jaati.

That would confuse:

**Strategy ≠ Solution / Variant ≠ Implementation Parameter.**

Current architecture correctly keeps:

`Goal Funding = Strategy`

and:

`SIP / Lumpsum / Step-up = Variants`

---

# 7. Strategy Library

Current canonical top-level strategies:

1. `strat-goal-funding`
2. `strat-progressive-de-risking`
3. `strat-capital-preservation`
4. `strat-debt-reduction`
5. `strat-credit-utilisation`

## 7.1 Goal Funding

Responsibility:

> Goal ko fund karne ke possible capital/contribution architectures create karna.

Variants:

- Existing Assets
- SIP
- Lumpsum
- Lumpsum + SIP
- Lumpsum + Step-up SIP
- Step-up SIP

---

## 7.2 Progressive De-risking

Responsibility:

> Goal ke close aate hue accumulated capital ko transition / protect karna.

Associated techniques include:

- Glide Path
- Bucketing
- Cash-flow Matching

---

## 7.3 Capital Preservation

Responsibility:

> Required capital ko preserve karna jab capital preservation goal/problem ka primary requirement ho.

Associated techniques include:

- Bucketing
- Laddering
- Cash-flow Matching

---

## 7.4 Debt Reduction

Responsibility:

> Debt burden reduce karna aur future cash-flow capacity release karna.

Associated techniques / solution architecture:

- Goal Segmentation
- Cash-flow Matching

---

## 7.5 Credit Utilisation

Responsibility:

> Funding/timing mismatch ko credit bridge ke through solve karna, subject to constraints.

Associated techniques / solution architecture:

- Cash-flow Matching
- Goal Segmentation

---

# 8. Canonicalization Work Completed

System mein identity duplication avoid karne ke liye canonical registries establish ki gayi hain.

## 8.1 Canonical Rules

File:

`backend/rules/canonical.py`

Contains:

- canonical rule IDs
- rule scopes
- rule roles
- eligibility
- hard constraints
- ranking inputs
- recommendation-only evidence
- architecture constraints
- explanatory evidence
- classification / transformation roles

Business thresholds ko unnecessarily change nahi kiya gaya; registry identity/metadata authority provide karti hai.

---

## 8.2 Canonical Strategies

File:

`backend/library/strategies/canonical.py`

Versioned canonical strategy registry.

Compatibility layer:

`backend/library/strategies/catalog.py`

---

## 8.3 Canonical Techniques

Files:

- `backend/library/strategies/techniques_canonical.py`
- `backend/library/strategies/techniques.py`

Current canonical techniques include:

- Bucketing
- Laddering
- Glide Path
- Cash-flow Matching
- Barbell
- Asset Earmarking
- Goal Segmentation
- Contribution Escalation
- Tax-efficient Sequencing
- Tax-loss Harvesting

---

## 8.4 Canonical Strategy Variants

File:

`backend/library/strategies/variants.py`

Defines:

`StrategyVariantDefinition`

with:

- variant_id
- strategy_id
- variant_type
- description
- required inputs
- version
- active status

---

## 8.5 Canonical Components

File:

`backend/library/strategies/components.py`

Current component families:

- funding
- accumulation
- transition
- preservation
- liquidity
- debt
- credit
- orchestration
- income

These describe architectural responsibilities, not financial products.

---

# 9. Strategy Solution Matrix

File:

`backend/library/strategies/solution_matrix.py`

This is the bridge between:

**Strategy → Solution → Goal Applicability → Technique / Variant**

It formalizes the distinction:

```
Strategy
   ↓
Solution
   ↓
Variant / Technique
   ↓
Goal applicability
```

Goal Funding solutions are derived from canonical variants.

Other strategies derive solutions from their canonical techniques.

This matrix does not calculate investor-specific values. Runtime engines remain responsible for actual investor calculations.

---

# 10. Constraints Architecture

The important architectural decision was:

> Constraint ownership decentralized rahega, lekin Strategy Engine ko ek centralized canonical ConstraintSet milega.

Sources:

- Goal Rules
- MoneyWheel
- Risk Profiler
- Financial State
- other domain diagnostics

Then:

```
Goal Rules
MoneyWheel
Risk Profiler
Financial State
      ↓
Constraint Aggregator
      ↓
Canonical ConstraintSet
      ↓
Strategy Engine
```

Main implementation:

- `backend/engines/constraints/models.py`
- `backend/engines/constraints/aggregator.py`
- `backend/engines/constraints/evaluator.py`
- `backend/services/strategy_service.py`

This avoids every downstream engine inventing its own interpretation of financial constraints.

---

# 11. MoneyWheel Role

MoneyWheel is diagnostic.

Its question:

> **Financially abhi kya ho raha hai?**

Core metrics include:

1. Savings Rate
2. Liquid Asset Ratio
3. Debt-to-Income Ratio
4. Leverage Ratio
5. Financial Asset Ratio
6. Insurance Coverage Ratio
7. Goal Funding Ratio
8. Future Funding Ratio
9. Required Rate of Return

Coverage:

- Expense Coverage
- Emergency Coverage

MoneyWheel:

`Observe → Calculate → Diagnose → Explain`

It does not directly choose:

- strategy
- product
- portfolio
- asset allocation

---

# 12. Risk Profiler Role

Risk Profiler strategy engine ko investment-related constraints provide karta hai.

Important distinction:

**Risk profile is not the Strategy Library.**

It is an input boundary for investment planning and can contribute constraints to the Strategy Engine where relevant.

Current implementation includes:

- Risk Required
- Risk Capacity
- Risk Tolerance
- constraints with key/value/unit/kind/source/evidence/confidence/validity

---

# 13. Strategy Engine Runtime

Main files:

- `backend/engines/strategy/engine.py`
- `backend/engines/strategy/applicability.py`
- `backend/engines/strategy/eligibility.py`
- `backend/engines/strategy/composition.py`
- `backend/engines/strategy/decision.py`
- `backend/engines/strategy/ranking.py`
- `backend/engines/strategy/scenario.py`

## Runtime flow

```
DefinedGoal
Financial Context
Investor Priorities
Canonical ConstraintSet
        ↓
Applicable Strategies
        ↓
Baseline Scenarios
        ↓
Strategy Architectures
        ↓
Decision Evaluation
        ↓
Ranking
        ↓
Recommendation
```

---

# 14. Strategy Applicability

Strategy Engine first determines which canonical strategies can participate.

Applicability considers:

- goal type
- goal state
- financial characteristics
- strategy rules
- relevant constraints

This prevents every strategy from being blindly evaluated for every goal.

---

# 15. Strategy Composition

File:

`backend/engines/strategy/composition.py`

Architecture can contain:

- primary strategy
- supporting strategies
- component IDs
- technique IDs
- rationale
- trade-offs
- constraints
- feasibility state

The architecture layer is important because a real financial problem may require:

```
Primary Strategy
      +
Supporting Strategy
      +
Techniques
      ↓
Strategy Architecture
```

This is the basis for hybrid strategies.

---

# 16. Baseline Scenario Engine

Baseline scenarios are the scenarios that participate in strategy comparison and decision ranking.

For Goal Funding, baseline scenarios correspond to funding variants.

Example:

```
Goal Funding
 ├── Existing Assets
 ├── SIP
 ├── Lumpsum
 ├── Lumpsum + SIP
 ├── Lumpsum + Step-up SIP
 └── Step-up SIP
```

Each scenario carries calculated metrics and funding information.

Baseline scenarios are decision-relevant.

---

# 17. Decision Engine

File:

`backend/engines/strategy/decision.py`

Decision evaluation considers dimensions such as:

- eligibility
- goal fit
- horizon fit
- funding fit
- feasibility
- component fit
- constraints

Goal Funding evaluates its funding variants individually.

The architecture was deliberately changed so that:

> **A Goal Funding strategy is not evaluated as one opaque object. Its funding variants are separately visible as scenarios.**

This makes the report explainable.

---

# 18. Investor Priorities

Investor priorities are required before comparison and ranking.

The system therefore does not silently invent an investor preference.

This supports:

```
System:
Here are financially valid alternatives.

Investor:
These are my priorities.

System:
Now compare the alternatives under those priorities.
```

Final authority remains with the investor.

---

# 19. What-if Scenario Engine

The latest major addition is deterministic What-if analysis.

File:

`backend/engines/strategy/scenario.py`

Generated dimensions:

### Contribution changes

- +10%
- +25%
- +50%

### Goal horizon changes

- +1 year
- +3 years

### Goal target changes

- -10%
- -20%

### Contribution escalation

- 10% annual step-up
- 20% annual step-up

Each scenario:

- is marked `custom`
- is not investor-modified
- keeps the strategy ID
- carries assumptions
- carries funding structure
- carries calculated outcomes
- carries trade-off information

---

# 20. Important What-if Boundary

What-if scenarios are **not** part of baseline decision ranking.

Correct architecture:

```
Baseline Scenarios
      ↓
Decision / Ranking
      ↓
Selected / Evaluated Strategy
```

separately:

```
Strategy
   ↓
What-if Generator
   ↓
Sensitivity Analysis
   ↓
Trade-offs
```

This prevents a sensitivity scenario from silently becoming the system's recommendation.

---

# 21. What-if Calculation Corrections

Two important implementation details were addressed.

## Goal-date change

Existing mapped assets are re-projected to the new horizon using:

- allocated amount
- expected return

The system does not blindly reuse the original projected asset value.

## Contribution impact

Required contribution is not treated as already included in projected mapped assets.

The what-if contribution stream is calculated incrementally on top of mapped resources.

This avoids double-counting / undercounting the effect of additional contributions.

---

# 22. StrategyRun Persistence

Model:

`backend/models/strategy.py`

StrategyRun now carries:

`what_if_scenarios`

Repository persistence:

`backend/data/strategy_repository.py`

What-if scenarios are stored in run metadata and hydrated back into `Scenario` objects.

Therefore report generation can operate on persisted engine output instead of recalculating it.

---

# 23. Goal Decision Report Layer

Main file:

`backend/services/goal_report_service.py`

This is the presentation / decision-explanation layer.

It does **not** invent a new financial calculation engine.

It reads persisted StrategyRun + DefinedGoal + financial context and creates a complete report model.

---

# 24. Goal Decision Report Structure

Current report contains:

1. Executive Summary
2. Financial Position
3. Goal & Calculation
4. Feasibility & Funding Options
5. Funding Solutions
6. Strategy & Architecture
7. Why This Strategy
8. What-if Analysis
9. Trade-offs
10. Alternatives
11. Assumptions & Evidence
12. Decision
13. Data Provenance

This is intentionally more than a generic financial statement.

It is a **decision report**.

---

# 25. Report Data Flow

```
StrategyRun
     +
DefinedGoal
     +
Financial State
     +
Investor Priorities
     +
Persisted Scenarios
     +
Persisted What-if Scenarios
     ↓
GoalReportService
     ↓
Goal Decision Report Model
     ↓
 ┌───────────────┐
 ↓               ↓
JSON            PDF
```

The report layer should explain engine output, not silently create a second decision engine.

---

# 26. PDF Generation

The GoalReportService uses ReportLab.

Current PDF sections include:

- Executive Summary
- Financial Position
- Goal & Calculation
- Feasibility
- Funding Solutions
- Strategy Architecture
- Reasons
- What-if analysis
- Trade-offs
- Alternatives
- Assumptions
- Decision
- Data Provenance

The generated file is intended to be a client-facing decision document.

---

# 27. Current API Routes

Main API:

`backend/api/strategy.py`

## Build strategy

`POST /api/strategy/build`

Flow:

```
Authenticate
 ↓
Verify goal ownership
 ↓
StrategyService.build_strategy()
 ↓
StrategyEngine
 ↓
Persist StrategyRun
 ↓
Return StrategyRun
```

---

## Financial plan PDF

`GET /api/strategy/financial-plan.pdf`

This is the consolidated Financial Plan PDF route.

---

## Goal Decision Report JSON

`GET /api/strategy/runs/{strategy_run_id}/report`

Query parameter:

`planning_unit_id`

Flow:

```
Authenticate
 ↓
Verify StrategyRun ownership
 ↓
GoalReportService.build_report()
 ↓
JSON report
```

---

## Goal Decision Report PDF

`GET /api/strategy/runs/{strategy_run_id}/report.pdf`

Flow:

```
Authenticate
 ↓
Verify StrategyRun ownership
 ↓
GoalReportService.generate_pdf()
 ↓
application/pdf
 ↓
attachment download
```

Current filename pattern:

`goal-strategy-report-{strategy_run_id}.pdf`

Therefore the generic Goal Decision Report **does have a direct PDF download route in the current branch.**

---

# 28. Legacy Retirement Report Routes

There are still legacy routes:

- `/retirement-report`
- `/retirement-report.pdf`

The PDF route currently delegates to GoalReportService, but the JSON retirement route still delegates through the older StrategyService method.

This is a compatibility area, not the desired final generic report architecture.

Recommended future state:

```
Generic Goal Decision Report
        ↓
single report service
        ↓
goal type specific presentation only where required
```

Do not maintain separate decision brains for retirement, education, vacation etc.

---

# 29. Summary Financial Planning Report

Separate route:

`backend/api/summary_report.py`

Routes:

- `GET /api/summary-report/json`
- `GET /api/summary-report/pdf`

This represents the consolidated planning report.

Conceptually:

```
Individual Goal Decision Report
              ↓
     Multi-goal / Financial Plan
              ↓
    Summary Financial Report
```

The individual goal report and consolidated financial plan should remain separate report levels.

---

# 30. What Has Been Built vs What Is Not Yet Complete

## BUILT / IMPLEMENTED

### Domain / architecture

- Financial planning ontology
- Engine boundaries
- Strategy responsibility model
- Strategy vs solution vs variant distinction
- Centralized ConstraintSet concept
- Investor decision authority

### Goal layer

- DefinedGoal
- funding gap
- funding status
- feasibility
- feasibility reason
- surplus-aware feasibility
- goal funding variants

### Strategy Library

- canonical strategy registry
- canonical technique registry
- canonical variant registry
- canonical component registry
- canonical rule registry
- strategy solution matrix

### Strategy Engine

- applicability
- eligibility
- components
- architecture composition
- supporting strategies
- baseline scenarios
- strategy comparison
- decision evaluation
- ranking
- recommendation
- investor priorities

### Scenario Engine

- Goal Funding variants as scenarios
- deterministic what-if scenarios
- contribution sensitivity
- horizon sensitivity
- target sensitivity
- step-up sensitivity
- explicit assumptions
- separation of baseline vs what-if

### Persistence

- StrategyRun
- scenarios
- what-if scenarios
- run metadata
- repository hydration

### Reporting

- GoalReportService
- JSON report model/output
- PDF report generation
- 13-section report
- funding solutions
- strategy architecture
- alternatives
- trade-offs
- what-if analysis
- provenance

### API

- strategy build
- latest run
- run history
- strategy selection
- priorities
- custom scenarios
- goal report JSON
- goal report PDF
- financial plan PDF
- summary report routes

### Tests

Tests exist for major additions including:

- canonical rules
- canonical strategies
- canonical techniques
- canonical variants
- canonical components
- constraints
- MoneyWheel
- goal funding strategies
- goal report
- report PDF structure
- strategy solution matrix
- canonical strategy consumption
- what-if scenarios
- investment engine foundation

---

# 31. Important Current Integration Gap

Although the report route exists, the Strategy Engine implementation in the current branch needs a final consistency pass around What-if propagation.

The current `StrategyEngineResult` constructor expects `what_if_scenarios`, but the return construction shown in the engine still uses the older positional constructor shape.

Therefore the final implementation must make this internally consistent:

```
StrategyEngine.execute()
       ↓
what_if_scenarios generated
       ↓
StrategyEngineResult.what_if_scenarios
       ↓
StrategyService
       ↓
StrategyRun.what_if_scenarios
       ↓
Repository metadata
       ↓
GoalReportService
       ↓
PDF
```

This is a code integration issue to close, not a new product decision.

---

# 32. Remaining Work — Priority Order

## P0 — Close runtime consistency

### 1. Fix StrategyEngineResult propagation

Ensure constructor accepts:

- applicable strategies
- baseline scenarios
- priorities
- comparison matrix
- rankings
- recommendation
- architectures
- what-if scenarios

Ensure every return path passes the field.

Special case:

When no applicable strategies exist, return an empty what-if list.

---

### 2. Verify every StrategyService run-construction path

Every StrategyRun creation path should preserve:

`what_if_scenarios`

including:

- manual build
- custom scenario update
- priority update
- strategy selection
- goal update / rebuild paths
- any other result-derived run creation

No path should silently drop the data.

---

### 3. Verify repository round-trip

Test:

```
Engine result
 ↓
StrategyRun
 ↓
repository save
 ↓
repository read
 ↓
what_if_scenarios
```

The report must receive exactly the persisted scenarios.

---

# 33. P1 — Report API Hardening

## 1. Standardize report naming

Final generic route:

`/api/strategy/runs/{strategy_run_id}/report`

Final PDF:

`/api/strategy/runs/{strategy_run_id}/report.pdf`

Legacy retirement endpoints should either:

- become compatibility aliases, or
- be deprecated once frontend migration is complete.

---

## 2. Add explicit response contract

The generic report should have a stable schema / response model instead of relying indefinitely on an untyped dictionary.

Recommended contract:

`GoalDecisionReport`

with typed sections:

- executive_summary
- financial_state
- goal_calculation
- feasibility
- funding_solutions
- strategy
- what_if_analysis
- trade_offs
- alternatives
- assumptions
- decision
- provenance

---

## 3. PDF download tests

Test:

- authentication
- ownership
- content type
- content disposition
- PDF starts correctly
- required sections exist
- no missing persisted scenario data

---

# 34. P1 — Frontend Report Consumption

Backend route exists, but frontend should consume the final generic report contract.

Expected UI:

```
Goal Result
   ↓
Strategy Result
   ↓
View Decision Report
   ├── Summary
   ├── Funding Options
   ├── Selected Architecture
   ├── What-if
   ├── Trade-offs
   ├── Alternatives
   └── Download PDF
```

Important:

Frontend should not recreate financial calculations.

Frontend responsibilities:

- display
- interaction
- scenario selection / modification where supported
- download
- explanation

Backend remains authoritative.

---

# 35. P1 — Investor-configured What-if Scenarios

Current deterministic What-if scenarios are system-generated.

Next layer:

```
Investor changes:
- contribution
- goal date
- target
- step-up
- lump sum
```

Then:

```
Custom Scenario Request
        ↓
Scenario Engine
        ↓
Calculation
        ↓
Scenario Result
        ↓
Trade-off Explanation
```

This must remain separate from baseline recommendation unless the investor explicitly asks to rerun comparison under the modified assumptions.

---

# 36. P1 — Full Strategy Solution Mapping

Current solution matrix establishes the architecture.

Next layer should make the mapping explicit enough for runtime:

```
Goal Type
   +
Financial Constraints
   +
Strategy
   ↓
Applicable Solutions
   ↓
Techniques
   ↓
Required Inputs
   ↓
Implementation Parameters
```

This is where goal-specific strategy architecture becomes fully deterministic.

The system should answer:

> For THIS goal and THIS financial state, which solutions inside this strategy are actually applicable?

---

# 37. P2 — Strategy Library Expansion

After the five canonical strategies are stable, additional strategies can be introduced only when there is a clear financial responsibility that is not already covered.

Possible future responsibilities should not be added merely as techniques.

Rule:

> If it solves a different financial problem, consider a Strategy. If it is a way of implementing an existing strategy, keep it as a Solution / Variant / Technique.

This prevents Strategy Library bloat.

---

# 38. P2 — Multi-goal Orchestration

Individual goal strategy is the current decision unit.

Next major layer:

```
Goal A
Goal B
Goal C
   ↓
Multi-goal constraints
   ↓
Resource competition
   ↓
Capital allocation
   ↓
Consolidated Financial Plan
```

This is where conflicts such as:

- multiple goals using the same surplus
- competing timelines
- competing lump-sum requirements
- liquidity conflicts
- debt vs goal funding
- retirement vs near-term goal

must be resolved.

The existing architecture already has multi-goal planning-related components, but the complete orchestration layer should be treated as a separate milestone.

---

# 39. P2 — Decision Trace / Auditability

Final system should be able to answer:

> Why did the system produce this strategy architecture?

Expected trace:

```
Input
 ↓
Financial State
 ↓
Goal
 ↓
Constraint
 ↓
Rule
 ↓
Eligible Strategy
 ↓
Solution
 ↓
Scenario
 ↓
Metric
 ↓
Comparison
 ↓
Decision Evidence
 ↓
Report
```

This is important for explainability and future regulated financial-planning use.

---

# 40. P2 — Calculation Canonicalization Completion

Canonical calculation layer exists in:

`backend/engines/calculation/canonical.py`

Continue moving reusable mathematical facts toward one canonical source.

Rules:

- no duplicated formulas across engines
- no hidden assumptions
- no silent default returns
- missing data remains missing
- every derived fact exposes inputs / formula / availability where appropriate

---

# 41. P3 — Product Selection Integration

Product selection is intentionally downstream.

Correct eventual flow:

```
Financial State
 ↓
Goals
 ↓
Constraints
 ↓
Strategy
 ↓
Investment Plan
 ↓
Product Suitability
 ↓
Products
```

Do not move product selection into Strategy Library.

---

# 42. P3 — Investment Planning Integration

Risk Profiler remains the foundation.

Strategy Builder may say:

> Goal funding architecture requires X.

Investment Engine can then answer:

> Available capital ko investment structure mein kaise implement karna hai?

These are separate responsibilities.

---

# 43. What Should NOT Be Built

The following are explicitly outside the intended architecture:

### Do not build a universal fixed return assumption

No universal:

`10%`

rule.

Return assumptions must be explicit and scenario-specific.

### Do not make the system choose the investor's goal

Goal definition belongs to the investor / goal-planning layer.

### Do not create a separate Strategy Engine for every goal

Use one reusable Strategy Engine with goal-specific applicability and architecture.

### Do not permanently hard-code dates

Goal horizon is an input.

### Do not ignore existing assets

Mapped assets must participate in funding and scenario calculations.

### Do not hide assumptions

Every material assumption must be exposed in the report.

### Do not equate optimization with maximum return

Optimization is multi-dimensional.

### Do not turn techniques into strategies without a separate responsibility

This creates an unmaintainable Strategy Library.

---

# 44. Final Intended End-to-End Flow

## Individual Goal

```
User Financial Data
        ↓
Financial State
        ↓
MoneyWheel + Risk + Goal Engine
        ↓
Goal Feasibility
        ↓
Central ConstraintSet
        ↓
Strategy Applicability
        ↓
Strategy Architecture
        ↓
Solutions / Variants
        ↓
Baseline Scenarios
        ↓
Calculation
        ↓
Scenario Comparison
        ↓
Decision Evaluation
        ↓
Ranking / Recommendation
        ↓
Investor Review
        ↓
Investor Decision
        ↓
Goal Decision Report
        ↓
PDF Download
```

## Sensitivity

```
Baseline Strategy
        ↓
What-if Engine
        ↓
Contribution / Horizon / Target / Step-up changes
        ↓
Scenario outcomes
        ↓
Trade-offs
        ↓
Investor understanding
```

## Multi-goal future

```
Goal A ─┐
Goal B ─┼→ Multi-goal Orchestrator
Goal C ─┘
              ↓
      Resource allocation
              ↓
      Consolidated Financial Plan
              ↓
      Summary Financial Report
```

---

# 45. Current Route Map

| Route | Purpose | Status |
|---|---|---|
| `POST /api/strategy/build` | Build StrategyRun | Implemented |
| `GET /api/strategy/runs/{goal_id}/latest` | Latest strategy run | Implemented |
| `GET /api/strategy/runs/{goal_id}/history` | Run history | Implemented |
| `POST /api/strategy/scenarios/custom` | Add custom scenario | Implemented |
| `POST /api/strategy/priorities` | Update investor priorities | Implemented |
| `POST /api/strategy/select` | Persist strategy selection | Implemented |
| `GET /api/strategy/runs/{strategy_run_id}/report` | Goal Decision Report JSON | Implemented |
| `GET /api/strategy/runs/{strategy_run_id}/report.pdf` | Goal Decision Report PDF | Implemented |
| `GET /api/strategy/financial-plan.pdf` | Consolidated Financial Plan PDF | Implemented |
| `GET /api/summary-report/json` | Summary Financial Report | Implemented |
| `GET /api/summary-report/pdf` | Summary Financial Report PDF | Implemented |
| `GET /api/strategy/runs/{strategy_run_id}/retirement-report` | Legacy retirement report | Compatibility / cleanup pending |
| `GET /api/strategy/runs/{strategy_run_id}/retirement-report.pdf` | Legacy retirement PDF alias | Compatibility / cleanup pending |

---

# 46. Current Files — Major Responsibility Map

| File / Directory | Responsibility |
|---|---|
| `backend/services/goal_service.py` | Defined Goal + feasibility |
| `backend/engines/goal/funding_strategies.py` | Funding variants |
| `backend/models/defined_goal.py` | Goal calculation / feasibility model |
| `backend/library/strategies/canonical.py` | Strategy identity |
| `backend/library/strategies/variants.py` | Strategy variants |
| `backend/library/strategies/techniques_canonical.py` | Technique identity |
| `backend/library/strategies/components.py` | Components |
| `backend/library/strategies/solution_matrix.py` | Strategy → solution mapping |
| `backend/rules/canonical.py` | Rule identity |
| `backend/engines/constraints/aggregator.py` | Central ConstraintSet |
| `backend/engines/rules/engine.py` | Goal/rule assessment |
| `backend/engines/strategy/applicability.py` | Strategy applicability |
| `backend/engines/strategy/composition.py` | Architecture composition |
| `backend/engines/strategy/scenario.py` | Baseline + What-if scenarios |
| `backend/engines/strategy/decision.py` | Decision evaluation |
| `backend/engines/strategy/ranking.py` | Ranking |
| `backend/engines/strategy/engine.py` | Main Strategy Engine orchestration |
| `backend/services/strategy_service.py` | Service / persistence orchestration |
| `backend/data/strategy_repository.py` | StrategyRun persistence |
| `backend/services/goal_report_service.py` | Goal Decision Report |
| `backend/api/strategy.py` | Strategy + report API |
| `backend/api/summary_report.py` | Summary Financial Report API |

---

# 47. Implementation Sequence From Here

Recommended build order:

### Phase 1 — Runtime closure
1. Fix StrategyEngineResult What-if propagation.
2. Audit every StrategyRun creation path.
3. Verify repository round-trip.
4. Add/strengthen report route tests.

### Phase 2 — Report closure
5. Make GoalDecisionReport typed.
6. Standardize generic report route.
7. Remove/alias legacy retirement report paths.
8. Verify PDF download end-to-end.

### Phase 3 — Investor interaction
9. Custom What-if API.
10. Scenario comparison interaction.
11. Explicit investor decision persistence.
12. Report reflects final investor decision.

### Phase 4 — Strategy intelligence
13. Complete runtime Strategy → Solution applicability.
14. Add deterministic required-input validation.
15. Improve architecture composition.
16. Improve trade-off explanations.

### Phase 5 — Multi-goal
17. Multi-goal resource conflict detection.
18. Goal prioritization.
19. Resource allocation.
20. Consolidated Financial Plan.
21. Summary Financial Report.

### Phase 6 — Implementation layer
22. Investment Planning integration.
23. Product Suitability.
24. Insurance Suitability.
25. Implementation Action Plan.

### Phase 7 — Auditability
26. Decision trace.
27. Evidence provenance.
28. Assumption versioning.
29. Rule/version trace.
30. Full audit trail.

---

# 48. Final Definition of Done

The Strategy / Goal Decision system should be considered mature when this statement is true:

> Given an investor's current financial state, one defined goal, investor priorities and canonical constraints, Planvesto can deterministically construct applicable strategy architectures, expose their solutions and variants, generate comparable baseline scenarios, generate sensitivity scenarios, explain the financial trade-offs, preserve the resulting decision state, and produce a traceable client-facing report — without silently inventing assumptions or making the investor's final decision.

The final architecture remains:

```
STATE
  ↓
GOAL
  ↓
CONSTRAINTS
  ↓
STRATEGY
  ↓
SOLUTION / VARIANT
  ↓
SCENARIO
  ↓
CALCULATION
  ↓
COMPARISON
  ↓
DECISION EVIDENCE
  ↓
INVESTOR DECISION
  ↓
REPORT
```

**This is the implementation direction to preserve going forward.**
