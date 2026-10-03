# Planvesto — Final System Architecture, Canonicalization & Hardening Specification

## 0. Purpose

This document is the working specification for the final system-hardening phase of Planvesto.

It defines:
- how the product connects end-to-end,
- what each layer owns,
- which object is authoritative at each stage,
- which known conflicts must be resolved,
- and what conditions must be true before the system is architecturally complete.

It is not a generic checklist. The implementation team must use it as the reference for the final audit and remediation.

Rule: audit first, prove the problem, define the canonical owner, then change code.

## 1. Target Product Architecture

USER
↓
AUTHENTICATION
↓
PLANNING UNIT
↓
ONBOARDING / RAW FINANCIAL DATA
↓
FINANCIAL STATE
↓
FINANCIAL METRICS & ANALYSIS
↓
GOALS
↓
GOAL FEASIBILITY + CONSTRAINTS
↓
STRATEGY CANDIDATES
↓
RECOMMENDATION
↓
STRATEGY SELECTION
↓
IMPLEMENTATION PREVIEW
↓
IMPLEMENTATION FINALIZATION
↓
STRATEGY VERSION
↓
REPORT
↓
ACTION PLAN
↓
EXECUTION

Every arrow represents a contract. No parallel path may silently become a second source of truth.

## 2. Domain Ownership Model

| Domain | Canonical Owner | Role |
|---|---|---|
| Authentication | Server authentication layer | Establish identity |
| Planning Unit | Planning Unit domain | Root ownership boundary |
| Raw Financial Data | Persisted investor data | Source input |
| Financial State | Financial State builder/snapshot | Canonical current position |
| Financial Metrics | Metric calculation layer | Derived financial facts |
| Goal Type | backend/rules/goals.py | Canonical classification |
| Goal Priority | Canonical priority rules | Goal ordering/weight |
| Constraints | Constraint domain | Planning restrictions/effects |
| Moneywheel | Moneywheel domain | 9 ratios + 2 rules |
| Strategy Library | Strategy registry | Candidate strategies |
| Strategy Architecture | Canonical identity/composition | Strategy structure |
| Recommendation | Recommendation output | Recommended candidate |
| Strategy Selection | Selection context | User choice |
| Implementation | Implementation workflow | Configuration/what-if |
| StrategyVersion | Versioning domain | Finalized strategy authority |
| Report | Report service | Detailed StrategyVersion representation |
| Action Plan | Action-plan domain | StrategyVersion execution layer |
| Execution | Action lifecycle | Actual implementation |
| History | StrategyRun/history | Audit and historical context |

Core principle:

One concept → one canonical definition → one authoritative owner → explicit compatibility boundary.

## 3. Financial Data → Financial State

Raw onboarding data is input, not planning output.

Canonical flow:

Raw Investor Data
→ Financial State Builder
→ Financial State Snapshot
→ Metrics / Analysis / Constraints / Strategy

Financial State must be server-derived and internally consistent.

The final audit must verify that derived financial state cannot be independently fabricated by frontend code or by downstream execution events.

## 4. Financial Metrics

Every financial metric must have:
1. one canonical name,
2. one calculation definition,
3. one value shape/unit,
4. one calculation owner,
5. documented consumers.

Examples requiring verification:
- savings rate
- liquidity
- DTI
- leverage
- financial asset ratio
- insurance coverage
- goal funding
- future funding
- required return
- emergency coverage

A metric may have multiple presentation bands, but its underlying calculation must not be reimplemented differently by another service.

## 5. Goal Domain

### Goal Type

Canonical Goal Type is owned by backend/rules/goals.py.

Canonical taxonomy includes:
- emergency_fund
- debt_freedom
- education
- marriage
- home
- home_improvement
- vehicle
- travel
- retirement
- financial_independence
- family_care
- healthcare
- business
- lifestyle
- wealth_creation
- legacy_giving
- other

Aliases normalize into these canonical values at the boundary.

Example:
Child Education → goal_type=education, goal_name=Child Education

Goal Name and Goal Type are not interchangeable.

### Goal Priority

Priority is centralized through canonical_goal_priority() and get_priority_rank().

No engine should independently reinterpret priority aliases.

## 6. Goal Feasibility

Goal feasibility answers:

Can this goal be funded under the investor's current financial state and planning constraints?

Canonical flow:

Financial State + Goal + Constraints + Funding Capacity
→ Feasibility

The audit must resolve the existing vocabulary split:
- feasible / conditional / infeasible
- feasible / constrained / infeasible

Do not rename values until semantics are proven.

## 7. Constraints

Canonical flow:

Financial Fact / Metric
→ Diagnostic Evidence
→ Goal-specific Business Rule
→ Constraint Result
→ Planning Effect

Financial Metric Status is not automatically Constraint Severity.

A critical ratio may remain diagnostic evidence. A goal-specific rule may convert it into a hard planning constraint.

This distinction must remain explicit in code and tests.

## 8. Funding Semantics

There are multiple funding vocabularies.

Goal-level examples:
- Shortfall
- On Track
- Overfunded

Allocation/execution examples:
- fully_funded
- partially_funded
- unfunded
- within_surplus
- surplus_shortfall
- requires_review

The audit must determine whether these are different concepts.

If different, keep them separate and name them explicitly.

If identical, establish one canonical vocabulary.

Do not merge them merely to reduce enum count.

## 9. Moneywheel — Canonical Contract

Backend canonical Moneywheel contract:

### 9 Ratios
1. savings_rate
2. liquid_asset_ratio
3. debt_to_income_ratio
4. leverage_ratio
5. financial_asset_ratio
6. insurance_coverage_ratio
7. goal_funding_ratio
8. future_funding_ratio
9. required_rate_of_return

### 2 Rules
1. expense_coverage
2. emergency_coverage

Therefore:

Moneywheel = 9 ratios + 2 rules.

Frontend consumes this backend contract and must not recreate the old 12-ratio vocabulary.

## 10. Legacy Compatibility

Legacy data may exist, but legacy representations must never become current business authority.

Required pattern:

Legacy Input
→ Compatibility Adapter
→ Canonical Domain Model
→ Business Logic

Known legacy Moneywheel values include:
- savings_ratio
- expense_ratio
- emergency_fund_coverage
- current_liquidity_ratio
- solvency_ratio
- insurance_gap_ratio

They remain compatibility representations unless the domain audit proves that a value is a distinct canonical metric.

## 11. Critical Liquidity Metric Conflict

The audit identified a collision between:
- current_liquidity_ratio
- liquid_asset_ratio

These cannot be treated as aliases merely because both describe liquidity.

Compare:
- numerator
- denominator
- unit
- formula
- semantic purpose
- threshold usage
- consumers

If they are identical, establish one canonical name.

If they are different, retain two explicit canonical definitions.

No silent fallback between them.

## 12. Threshold Architecture

Thresholds currently appear across:
- backend/rules/constraints.py
- backend/rules/moneywheel.py
- backend/engines/constraints/evaluator.py
- financial-plan logic

Each threshold must be classified as:
1. metric calculation boundary,
2. diagnostic band,
3. planning constraint,
4. eligibility threshold,
5. strategy-selection threshold,
6. intentionally distinct business benchmark.

Two thresholds using the same metric are not automatically duplicates.

Target:

Business Rule → One authoritative threshold owner → All consumers.

## 13. Known Financial Calculation Conflict

The read-only audit identified competing calculations in consolidated planning logic.

### DTI

A consolidated planning path calculates DTI from outstanding liabilities relative to annual income. This may differ materially from a debt-service-based DTI definition.

### Emergency Coverage

A consolidated planning path estimates emergency coverage using a percentage of financial assets rather than classified liquid assets divided by expenses.

These are not merely duplicated constants. They can produce different conclusions for the same investor.

Final remediation must establish the canonical metric definition and make all planning consumers use it.

## 14. Strategy Domain

Strategy Builder is the central planning decision tool.

Its responsibility is:

Goal
→ Strategy Candidates
→ Recommended + Alternative
→ User Selection

It should not simultaneously own Report generation, Action Plan execution, or historical decision authority.

## 15. Strategy Identity

Strategy Architecture identity is based on:

Goal ID + Primary Strategy ID

Supporting strategies, techniques, and solutions are composition data.

Changing composition must not change architecture identity.

The canonical architecture ID generator is the only authority for architecture IDs.

## 16. StrategyRun vs StrategyVersion

This is the most important authority boundary.

StrategyRun represents:
- evaluation,
- candidate generation,
- recommendation context,
- scenarios,
- historical runs,
- audit/history.

StrategyVersion represents:
- finalized implementation,
- immutable strategy configuration,
- implementation parameters,
- finalized strategy context,
- authoritative downstream decision.

Canonical rule:

StrategyRun = evaluation/history
StrategyVersion = finalized decision authority

After finalization, Report and Action Plan must not select the current decision from:
- latest StrategyRun,
- is_latest,
- ranking position,
- historical recommendation.

Every remaining latest-run consumer must be classified and corrected if it affects current decision output.

## 17. Strategy Implementation Lifecycle

Intended lifecycle:

Strategy Selection
→ Implementation Preview
→ What-if / Parameters
→ Implementation Finalization
→ StrategyVersion

Implementation Parameters answer:

How is the selected strategy configured for this investor and goal?

They are not a strategy.

StrategyVersion is the immutable snapshot of the finalized configuration.

## 18. Approval Lifecycle

The audit found a separate approval concept:
- implementation finalization creates a provisional StrategyVersion,
- action generation requires an approval snapshot.

The final lifecycle must explicitly define:

Selected
→ Implementation Preview
→ Finalized / Provisional StrategyVersion
→ Approved
→ Report / Action Plan / Execution

The final audit must prove:
- who creates approval,
- what is approved,
- which StrategyVersion is approved,
- how approval is persisted,
- how approval is validated,
- what happens if the StrategyVersion changes.

Do not assume provisional and approved mean the same thing.

## 19. Report Architecture

All individual goals use the same report contract. Goal-specific data populates the generic structure.

Canonical relationship:

Goal → StrategyVersion → Goal Report

Version-scoped backend routes include:
- /api/strategy/strategy-versions/{strategy_version_id}/report
- /api/strategy/strategy-versions/{strategy_version_id}/report.pdf

Legacy run-based routes may remain for compatibility but must not become current decision authority.

Frontend Reports Center:
- /investor/reports

## 20. Action Plan Architecture

Action Plan is execution, not another strategy decision layer.

Canonical relationship:

Goal
→ Selected StrategyVersion
→ Execution Points
→ Pending / Completed / Skipped

If no StrategyVersion exists:
Goal → No finalized strategy → Strategy Builder

If no execution points exist:
StrategyVersion → No execution points → Generate execution points

Existing cancelled actions may be displayed as Skipped. Do not invent a new persistence status without a separate business/schema decision.

## 21. Execution and Financial State Integrity

A critical finding requires explicit remediation.

Action completion accepts a client-provided actual_state, validates it as FinancialState, and can persist it as the latest financial snapshot.

Potential alternate authority:

Client
→ Action Completion
→ actual_state
→ Financial State Snapshot

The final audit must determine:
- which execution fields may change Financial State,
- which values must come from server-owned records,
- whether execution may update only actual execution impact,
- whether unrelated financial facts can be overwritten,
- what validation is required.

Execution must not become an uncontrolled alternative source of truth for Financial State.

## 22. Onboarding Ownership

Current boundary:

Frontend onboarding
→ Raw investor data
→ Supabase persistence
→ Backend Financial State builder
→ Financial State snapshot

This can remain valid if the ownership boundary is explicit.

The final audit must ensure:
- frontend persists raw inputs only,
- backend owns derived Financial State,
- backend owns calculated metrics,
- planning engines consume server-derived state,
- frontend cannot persist derived planning state as authoritative data.

## 23. Auth and Ownership

Planning Unit is the root ownership boundary.

Every child resource must be validated against authenticated ownership and planning unit.

Audit:
- goals
- FinancialState snapshots
- StrategyRuns
- StrategyVersions
- reports
- action plans
- execution actions
- approval snapshots

Identifier knowledge alone must never grant access.

## 24. State Machine

### Goal

Created → Defined → Feasibility Evaluated

### Strategy

Candidates Generated → Recommendation → Selected

### Implementation

Selected → Preview → Finalized

### StrategyVersion

Provisional / Finalized → Approved → Current Authority

### Action Plan

Not Generated → Planned → Confirmed → Completed / Cancelled

The final audit must identify any state that bypasses these transitions or creates an impossible combination.

## 25. Client vs Server Authority

Client provides intent and input.

Server/domain layer owns domain truth.

Frontend may provide:
- user-entered data,
- selected goal,
- selected strategy,
- implementation parameters,
- what-if inputs,
- execution confirmation.

Backend/domain layer owns:
- canonicalization,
- calculations,
- thresholds,
- constraints,
- feasibility,
- eligibility,
- recommendation,
- Strategy identity,
- StrategyVersion,
- approval validity,
- authoritative Financial State.

## 26. Known Remediation Backlog

### P0 — Decision Authority
Remove or bound every current-decision dependency on latest StrategyRun.

Target:
Finalized Decision → StrategyVersion → Report / Action Plan / Execution

### P0 — Financial State Integrity
Resolve the client actual_state → authoritative snapshot path.

### P1 — Financial Metric Authority
Resolve competing DTI and emergency-coverage calculations.

### P1 — Approval Lifecycle
Define and enforce finalized vs approved semantics.

### P1 — Approval Integrity
Approval must be validated against exact planning unit, goal, StrategyVersion, and decision context.

### P1 — Liquidity Metric Authority
Resolve current_liquidity_ratio vs liquid_asset_ratio.

### P1 — Threshold Ownership
Establish one authoritative owner for each genuinely duplicated business rule.

### P1 — Status Vocabulary
Resolve feasibility, funding, and eligibility vocabularies.

### P2 — Legacy Aliases
Ensure aliases are compatibility-only.

### P2 — Onboarding Boundary
Document and enforce raw-data vs derived-state ownership.

### P2 — Regression Tests
Every canonical authority must have regression coverage.

### P3 — Documentation
Update domain ontology documents after implementation and second audit.

## 27. Required Audit Deliverable

The completed code-first audit must produce exactly:

1. Executive System Verdict
2. End-to-End Architecture Trace
3. Source-of-Truth Matrix
4. StrategyRun vs StrategyVersion Authority Audit
5. Financial State & Metric Audit
6. Threshold Ownership Audit
7. Goal / Funding / Feasibility / Eligibility Vocabulary Audit
8. Legacy Alias Audit
9. Strategy Lifecycle Audit
10. Approval Lifecycle Audit
11. Report & Action Plan Audit
12. Execution & Data Integrity Audit
13. Auth & Ownership Audit
14. State Machine Audit
15. Frontend ↔ Backend Contract Audit
16. Documentation / Test Drift
17. Prioritized Remediation Backlog
18. Canonical Target Architecture
19. Final Sign-off Conditions

Every finding must include:
- exact file,
- function/class,
- call path,
- current behavior,
- domain meaning,
- why it is wrong/risky,
- canonical owner,
- proposed target,
- affected consumers,
- priority,
- backend/frontend/schema impact,
- regression test required.

Do not report generic observations when repository evidence exists.

## 28. Implementation Protocol

The audit itself is read-only.

AUDIT
→ PROVEN FINDINGS
→ CANONICAL DECISIONS
→ TARGET CONTRACT
→ REGRESSION TEST PLAN
→ IMPLEMENTATION
→ CI
→ SECOND READ-ONLY AUDIT
→ DOCUMENT UPDATE
→ FINAL SIGN-OFF

A finding is closed only when:
- canonical authority is explicit,
- competing authority is removed or bounded,
- regression coverage exists,
- CI passes,
- second audit confirms the result.

Do not modify schema or migrations merely for conceptual cleanliness.

Do not redesign frontend unless a verified contract requires it.

Do not invent business rules.

## 29. Final System Definition

The final Planvesto system should behave as:

RAW DATA
↓
CANONICAL FINANCIAL STATE
↓
CANONICAL METRICS
↓
GOAL + CONSTRAINTS
↓
STRATEGY DECISION
↓
IMPLEMENTATION
↓
STRATEGY VERSION
↓
REPORT
↓
ACTION PLAN
↓
EXECUTION

There must not be competing parallel paths such as:
- Raw Data → Service A → Metric A
- Raw Data → Service B → Metric B
- StrategyRun → Report
- StrategyVersion → Report
- Legacy Alias → Business Rule
- Client actual_state → FinancialState

unless the difference is explicitly intentional, documented, and governed.

The architectural objective is:

One canonical domain model.
One authoritative calculation path.
One decision authority.
Explicit lifecycle transitions.
Bounded compatibility.
Test-enforced contracts.

## 30. Final Sign-off Gate

The system is ready for final sign-off only when:

- Financial State has one authoritative construction path.
- Financial metrics have canonical definitions.
- Goal taxonomy is centralized.
- Goal priority is centralized.
- Funding semantics are explicit.
- Feasibility semantics are explicit.
- Eligibility is canonical.
- Constraint semantics are canonical.
- Threshold ownership is resolved.
- Moneywheel is exactly 9 ratios + 2 rules.
- Legacy aliases cannot become authoritative.
- Strategy identity is stable and canonical.
- StrategyRun is history/evaluation only.
- StrategyVersion is the finalized decision authority.
- Approval lifecycle is explicit and validated.
- Report is StrategyVersion-sourced.
- Action Plan is StrategyVersion-sourced.
- Execution cannot silently overwrite unrelated FinancialState.
- Auth/ownership is consistent across all child resources.
- Frontend consumes backend domain contracts.
- State transitions are coherent.
- Relevant regression tests pass.
- Full CI passes.
- A second read-only audit confirms the architecture.
- Domain documentation matches verified implementation.

Only after this gate is the final system-hardening phase complete.

## 31. Audit Completion Status — Current Gate

The repository audit is **not yet considered fully complete**.

The existing sections capture the target architecture, known findings, remediation priorities, and sign-off conditions. However, the final evidence-backed audit deliverable has not yet been closed.

### What is already established

- End-to-end target architecture is documented.
- Domain ownership model is documented.
- StrategyRun vs StrategyVersion authority boundary is defined.
- Financial State architecture is defined.
- Goal canonicalization and priority ownership are defined.
- Constraint semantics are defined.
- Moneywheel canonical contract is defined as 9 ratios + 2 rules.
- Known legacy aliases are documented.
- Liquidity metric collision is documented.
- Threshold ownership problem is documented.
- DTI and emergency-coverage calculation conflicts are documented.
- Approval lifecycle concerns are documented.
- Action Plan / Report authority is documented.
- Execution / `actual_state` integrity risk is documented.
- Onboarding ownership boundary is documented.
- Auth / ownership model is documented.
- Remediation priorities and final sign-off conditions are documented.

### What is still required before remediation begins

The final audit must convert the existing findings into repository-proven evidence.

For every material finding, the audit must provide:

- exact file,
- exact function/class,
- actual call path,
- current behavior,
- domain meaning,
- evidence for the finding,
- canonical owner,
- canonical target,
- affected consumers,
- priority,
- backend/frontend/schema impact,
- required regression test.

The following areas require explicit evidence closure:

1. StrategyRun vs StrategyVersion — repository-wide current-decision consumers.
2. Financial State and metric definitions — exact formulas and ownership.
3. DTI calculation conflict — exact competing implementations.
4. Emergency coverage calculation conflict — exact competing implementations.
5. Threshold ownership — complete inventory and semantic classification.
6. `current_liquidity_ratio` vs `liquid_asset_ratio` — formula/unit/consumer comparison.
7. Funding / feasibility / eligibility vocabularies — semantic equivalence or intentional separation.
8. Approval lifecycle — creation, validation, StrategyVersion binding, and enforcement.
9. Execution `actual_state` — client authority and FinancialState persistence path.
10. Onboarding ownership — raw data vs derived FinancialState boundary.
11. Frontend ↔ backend contract duplication.
12. Legacy aliases — compatibility-only vs authoritative usage.
13. Tests — exact current failures, stale contracts, and missing regression coverage.
14. Documentation drift — current code vs domain/architecture documentation.

### Audit status model

Use these states explicitly:

- **VERIFIED** — proven against current repository code/tests.
- **CONFIRMED CONFLICT** — competing implementations or authorities are proven.
- **NOT ESTABLISHED** — repository evidence is insufficient; do not invent semantics.
- **COMPATIBILITY ONLY** — legacy path exists but is not authoritative.
- **REMEDIATION REQUIRED** — verified issue with a defined canonical target.

Do not mark a finding as resolved merely because the target architecture is documented.

### Final audit gate

The next Coding Agent task is **completion of the existing audit, not a new audit and not implementation**.

Required sequence:

Existing Audit Findings
→ Repository Evidence Closure
→ Final 19-Section Audit Deliverable
→ Canonical Decisions
→ Target Contracts
→ Regression Test Plan
→ Implementation
→ CI
→ Second Read-Only Audit
→ Final Sign-Off

Until the evidence closure and final 19-section deliverable are complete:

- no remediation implementation should begin,
- no business semantics should be guessed,
- no schema/migration changes should be introduced,
- no frontend redesign should be introduced.

This section supersedes any interpretation that the presence of the remediation backlog means the audit itself is complete.
