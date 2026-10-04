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

Financial State is the authoritative planning state. Its normal construction remains server-derived from raw financial data; however, per approved D1, action completion may submit a full actual_state, and that client-submitted snapshot is authoritative for the resulting FinancialState. The implementation must therefore make the client-to-state authority explicit, validate the snapshot and ownership boundary, and prevent ambiguity about which snapshot is current.

The final implementation must verify that only the approved action-completion path can establish a new authoritative snapshot and that unrelated authority paths do not silently compete with it.

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
Education → goal_type=education, goal_name=Education

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

Execution is an explicit, controlled authority boundary for Financial State when an action completion submits actual_state, as approved by D1. It must not create an ambiguous second path: the completion contract, validation, snapshot persistence, lineage, and current-state selection must all agree that the submitted snapshot is authoritative.

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
- persistence and validation of authoritative Financial State.

Approved D1 exception: on action completion, the client-submitted full actual_state is itself authoritative for the resulting FinancialState snapshot. The backend remains responsible for validating, persisting, and exposing that authoritative state consistently.

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

## 30. Post-Audit Story — What Is Finalized, What Remains, and How We Finish

This document has now moved from **audit mode** into **execution mode**.

The story so far is:

1. **The system was audited end-to-end.**  
   The audit is complete. The remaining problems are no longer unknown repository mysteries; they are identified authority conflicts, duplicated definitions, contract mismatches, lifecycle gaps, and test/document drift.

2. **The canonical direction was defined.**  
   The target architecture is centralized around explicit domain owners, canonical contracts, bounded compatibility, and one finalized decision authority.

3. **The business decisions are now finalized.**  
   D1–D8 are resolved and must be treated as binding business decisions for implementation. They override earlier “decision pending” language and any audit recommendation that conflicts with an explicitly approved option.

4. **What is still missing is not another broad audit.**  
   The remaining work is to turn the approved model into the actual system: centralize canonical definitions, remove/bound competing authorities, align APIs and frontend contracts, repair lifecycle integrity, update regression coverage, run CI, and perform one final read-only verification.

### 30.1 Approved Business Decisions — Binding Implementation Baseline

| Decision | Approved option | Binding implementation rule |
|---|---|---|
| **D1 — Execution / FinancialState authority** | **A** | Client-submitted full actual_state is authoritative and may establish/update FinancialState on action completion. |
| **D2 — Report state basis** | **C** | Provide both finalized-decision state/context and a separate current/latest state view; never silently mix them. |
| **D3 — Liquidity identity** | **B** | current_liquidity_ratio and liquid_asset_ratio remain distinct canonical metrics. |
| **D4 — Threshold ownership** | **B** | Centralize only when metric + business purpose are identical; retain distinct thresholds otherwise. |
| **D5 — Emergency coverage** | **B** | Canonical emergency coverage = liquid assets / essential monthly expenses. The 20% financial-assets estimate is not canonical coverage. |
| **D6 — Vocabulary** | **B** | constrained = funding/feasibility limitation; conditional = strategy eligibility condition. |
| **D7 — Approval** | **B** | Approval is an explicit user action bound to the exact StrategyVersion + Goal context. |
| **D8 — Goal revision** | **C** | Old StrategyVersion remains history, but loses current authority for the revised goal; a new version must be finalized. |

**Decision status: D1–D8 RESOLVED.**

No implementation should reinterpret these decisions without a new explicit business decision.

### 30.2 Current State of the System

| Area | Status | Meaning |
|---|---|---|
| Repository/system audit | **DONE** | The codebase has been audited and the verified authority conflicts/remediation surfaces are known. |
| Domain canonicalization direction | **DEFINED** | Canonical owners and target architecture are established. |
| Business decision gates D1–D8 | **DONE** | All unresolved business semantics from the execution plan are explicitly resolved. |
| Canonical implementation | **NOT DONE** | The code still contains the audited competing paths, aliases, duplicated rules, and contract drift that remediation must remove/bound. |
| Centralized authority enforcement | **NOT DONE** | Canonical owners exist conceptually; code must now enforce them. |
| Regression suite alignment | **NOT DONE** | Existing tests contain legacy/run-authority assumptions and coverage gaps. |
| CI validation | **NOT DONE** | The prior audit environment could not execute the full suites because dependencies/tooling were unavailable. |
| Second read-only audit | **NOT DONE** | This happens only after implementation and CI validation. |
| Final sign-off | **NOT READY** | Sign-off requires all gates below to pass. |

### 30.3 The Remaining Roadmap

The remaining work is intentionally sequential. Do not jump to P2/P3 while P0 authority boundaries are still unresolved.

#### PHASE 0 — Freeze the Canonical Baseline

**Goal:** make the approved decisions and target contracts the implementation source of truth.

- Treat D1–D8 as resolved.
- Update implementation notes/contracts that still describe these decisions as unresolved.
- Identify every current consumer that conflicts with an approved decision.
- Do not redesign unrelated product behavior.

**Exit condition:** the implementation team has one approved semantic baseline and no unresolved D1–D8 business gate.

#### PHASE 1 — P0: Establish Decision and State Authority

**Goal:** make the system structurally obey the canonical authority model.

1. **StrategyRun → StrategyVersion**
   - Current finalized reports/plans/actions must stop deriving current decisions from latest/linked StrategyRun.
   - StrategyVersion must contain or reference the complete finalized goal/version/architecture/implementation context required downstream.
   - Run-based routes may remain only as explicitly bounded history/compatibility surfaces.

2. **FinancialState freshness/integrity**
   - Ensure current decision consumers do not silently use stale snapshots after raw financial input changes.
   - Choose and implement the audited freshness mechanism.
   - Verify every current-state consumer follows the same authority path.

3. **D1 client actual_state authority**
   - Preserve the approved client-submitted full snapshot authority.
   - Make action completion the explicit authority boundary.
   - Validate ownership/scope and snapshot shape.
   - Persist action-to-snapshot lineage.
   - Ensure current-state selection consistently recognizes the authoritative snapshot.
   - Prevent unrelated, competing execution paths from silently writing different state.

**P0 exit condition:** current decisions have one version authority, FinancialState freshness is deterministic, and action completion has one explicit state-authority contract.

#### PHASE 2 — P1: Centralize Financial Semantics and Lifecycle Rules

**Goal:** eliminate duplicate financial definitions and ambiguous lifecycle semantics.

1. Canonicalize DTI and emergency coverage.
2. Keep liquidity metrics distinct and remove incompatible fallback.
3. Classify every threshold by metric + business purpose and centralize only genuine duplicates.
4. Normalize goal priority at the boundary and in all consumers.
5. Enforce distinct funding/feasibility/eligibility vocabulary.
6. Implement explicit approval command, exact binding, validation, and reapproval/invalidation behavior required by D7.
7. Enforce D8 goal-version binding and new finalization after goal revision.

**P1 exit condition:** each financial/business rule has an explicit owner, each lifecycle transition has a valid authority, and no consumer silently substitutes a different semantic.

#### PHASE 3 — P2: Compatibility and Contract Hardening

**Goal:** prevent legacy representations from re-entering canonical business logic.

- Bound all legacy aliases to compatibility adapters.
- Validate Moneywheel as exactly **9 ratios + 2 rules**.
- Align frontend/backend contracts.
- Remove unrestricted or mismatched status/key contracts.
- Keep onboarding writes limited to the intended raw-data boundary.
- Update regression tests that encode superseded run/legacy-key behavior.

**P2 exit condition:** legacy input may be accepted where required, but canonical output and business logic cannot be bypassed.

#### PHASE 4 — P3: Documentation Synchronization

**Goal:** make documentation describe the system that actually exists.

Update the ontology, lifecycle, API/contract, authority, and compatibility documentation only after P0–P2 behavior is implemented and tested.

**P3 exit condition:** documentation, API contracts, tests, and implementation describe the same canonical system.

#### PHASE 5 — Verification and Sign-off

**Goal:** prove the remediation rather than assuming it.

1. Run targeted regression tests for every changed authority boundary.
2. Run full backend/frontend tests and typechecks.
3. Run migration/RLS integration tests where applicable.
4. Require CI green.
5. Conduct the second read-only audit.
6. Compare the second audit against this document and the approved D1–D8 register.
7. Close only findings whose competing authority has been removed or explicitly bounded and whose regression test exists.
8. Perform final sign-off.

### 30.4 Dependency Graph

The implementation dependency is:

D1–D8 resolved
→ P0 authority
→ P1 financial/lifecycle semantics
→ P2 contracts/compatibility/tests
→ P3 documentation
→ CI
→ second audit
→ sign-off

The critical rule is:

**Do not use tests or documentation work to hide unresolved authority problems. Fix the authority first, then lock it with tests.**

### 30.5 Definition of “Canonicalized and Centralized”

The system is considered canonicalized only when all of the following are true:

- One canonical definition exists for every domain concept.
- One authoritative owner exists for every calculation/business rule.
- Duplicate implementations either disappear or become explicit compatibility adapters.
- Current decision output has one authority.
- State transitions cannot bypass the intended lifecycle.
- Frontend contracts consume backend canonical contracts rather than recreating business semantics.
- Legacy names cannot become internal business authority.
- Regression tests fail if a competing authority returns.
- Documentation matches the verified implementation.

In practical terms, the remaining job is **not to create another architecture**. It is to make the existing approved architecture true in code.

### 30.6 What We Should NOT Do Next

- Do not perform another broad repository audit before implementing the already-verified backlog.
- Do not invent new business rules while coding.
- Do not silently reverse D1–D8 because the earlier audit recommended a different option.
- Do not rename concepts merely for aesthetic consistency.
- Do not introduce migrations unless the selected canonical contract actually requires persisted/schema change.
- Do not mark a phase complete because code compiles; the authority boundary must have regression coverage and CI evidence.

---

## 30. Final Sign-off Gate

The system is currently **NOT ready for final sign-off**. The audit and D1–D8 business decisions are complete; implementation, centralization, regression validation, CI, and the second audit remain.

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

## 31. Audit Completion Status — Evidence Closure

**Evidence closure: COMPLETE (2026-10-03).** Section 32 closes the repository-evidence gaps listed here and fulfills the Section 27 deliverable. Audit completion does not mean the implementation is complete or that Section 30 sign-off is satisfied. No code, schema, migration, frontend, or PR changes were made during the audit.

Finding labels:

- **VERIFIED** — established from current repository code, contract, migration, or test source.
- **CONFIRMED CONFLICT** — competing implementations or authorities are established.
- **NOT ESTABLISHED** — repository evidence is insufficient; semantics are not inferred.
- **COMPATIBILITY ONLY** — legacy surface is bounded to compatibility or history use.
- **REMEDIATION REQUIRED** — verified issue has a proposed canonical target; no fix is implied.

### Test execution limits

- `python -m pytest ...` failed with `No module named pytest`.
- Direct pytest collection for seven selected backend files produced seven collection errors and zero executed tests. Errors include unresolved `api`/`models` imports and missing `pydantic`/`fastapi`; retrying with `PYTHONPATH=/workspaces/planvesto/backend` produced the same result.
- `cd frontend && npm test` failed with `tsx: not found`; `cd frontend && npm run typecheck` failed with `tsc: not found`.
- No dependencies were installed. No live Supabase data/policies or destructive scenarios were tested. Migration files prove declared policies, not production deployment state.

## 32. Completed Code-First Audit — 19-Section Deliverable

### 1. Executive System Verdict

**CONFIRMED CONFLICT / REMEDIATION REQUIRED — P0:** StrategyVersion is the intended finalized authority but is not the sole current authority. Latest StrategyRun paths supply multi-goal/basket report content and planning inputs; version-scoped reports and action generation still read linked-run decision/composition fields. **CONFIRMED CONFLICT / REMEDIATION REQUIRED — P0:** completion can persist client-provided `actual_state` as latest FinancialState. **CONFIRMED CONFLICT / REMEDIATION REQUIRED — P1:** consolidated-plan DTI and emergency coverage use noncanonical inputs/formulas. **NOT ESTABLISHED:** approval writer and approval acceptance semantics. System sign-off is not ready.

### 2. End-to-End Architecture Trace

| Boundary | Current call path and behavior | Status / owner / impact |
|---|---|---|
| Auth → Planning Unit | `api.auth.authenticate_user()` → `verify_planning_unit_ownership()`; frontend `getPlanningUnitId()` selects/creates an owned unit. | **VERIFIED.** Auth + Planning Unit domain. |
| Onboarding → Raw Data | Onboarding provider → `lib/onboarding/persistence.ts` → direct Supabase raw-table writes guarded by RLS. | **VERIFIED.** Raw data is input; frontend does not write FinancialState snapshots. |
| Raw Data → FinancialState | `FinancialStateService.build()` → `FinancialStateEngine.build()` → snapshot insert. | **VERIFIED.** Backend builder owns derived state. Latest snapshot has no raw revision check. |
| Metrics → Analysis → Constraints | Canonical calculation functions feed FinancialState/Moneywheel; RuleEngine, constraint evaluator and FinancialPlanService have parallel calculations/bands. | **CONFIRMED CONFLICT.** Calculation layer should own formulas; rule owner should own purpose-specific thresholds. |
| Goal → Feasibility | `/api/goals` → GoalService → GoalEngine → versioned DefinedGoal → `_apply_feasibility()` using FinancialState surplus. | **VERIFIED.** Stale snapshots can affect current feasibility. |
| Candidates → Recommendation | StrategyService assembles rules/constraints/risk → StrategyEngine → StrategyRun. | **VERIFIED.** Run owns an evaluation, not finalized implementation. |
| Selection → Preview → Finalization | Selection is transient; preview stateless; finalization inserts provisional StrategyVersion and updates run selection fields. | **VERIFIED / CONFIRMED CONFLICT.** No separate selection record or visible finalization idempotency guard. |
| Version → Report / Actions | Version route resolves a linked run; report reads that run; action generator reads run architecture; run-ID report endpoints remain. | **CONFIRMED CONFLICT.** StrategyVersion must be sufficient for finalized downstream output. |
| Execution → FinancialState | Completion request may supply `actual_state`; service validates and inserts it as latest snapshot. | **CONFIRMED CONFLICT.** Backend FinancialState builder must remain authority. |

Evidence anchors: `backend/api/auth.py::authenticate_user` / `verify_planning_unit_ownership`; `frontend/lib/onboarding/persistence.ts::saveIncomeSources` / `saveSimpleList`; `backend/services/financial_state_service.py::build`; `backend/services/goal_service.py::_apply_feasibility`; `backend/services/strategy_service.py::finalize_implementation`; `backend/services/action_plan_service.py::complete_action_with_actual_state`.

### 3. Source-of-Truth Matrix

| Domain | Current authority | Target / finding |
|---|---|---|
| Raw financial inputs | Supabase onboarding tables | **VERIFIED:** persisted input authority. |
| FinancialState | Latest snapshot by `calculated_at` | **CONFIRMED CONFLICT:** derived state may be stale; bind to raw revision or rebuild. |
| Financial metrics | Canonical calculation module plus local reimplementations | **CONFIRMED CONFLICT:** centralize formulas; separate metric from policy band. |
| Goal | Raw goal row plus versioned DefinedGoal | **VERIFIED:** DefinedGoal owns calculated planning fields. |
| Recommendation/history | StrategyRun recommendation for that run | **VERIFIED:** evaluation authority only. |
| Final implementation | StrategyVersion plus linked run metadata | **CONFIRMED CONFLICT:** version lacks goal-version/architecture context used downstream. |
| Selected version per goal | Highest run version with non-null selected-version ID | **CONFIRMED CONFLICT:** no explicit current goal-to-version pointer. |
| Approval | Existence of approval snapshot for PU/version | **NOT ESTABLISHED:** no app writer/validation flow found. |
| Report | Generated from linked run, even when addressed by StrategyVersion | **CONFIRMED CONFLICT:** target is version-sourced report. |
| Action Plan | Actions keyed by version; generator also reads run architecture | **CONFIRMED CONFLICT:** target is version-sourced composition. |
| Execution | Latest snapshot can derive from request `actual_state` | **CONFIRMED CONFLICT:** target is server-derived or validated actual evidence. |

Evidence: `backend/data/financial_state_repository.py::get_latest`; `backend/data/strategy_repository.py::get_selected_strategy_version_id`; `backend/services/goal_report_service.py::_load_by_strategy_version`; `backend/services/strategy_action_generator.py::generate`.

### 4. StrategyRun vs StrategyVersion Authority Audit

**SR-1 — current-plan latest-run consumers. CONFIRMED CONFLICT / REMEDIATION REQUIRED, P0.** `MultiGoalPlanningService.build_multi_goal_plan()` → `get_latest_run()` → `GoalReportService.build_report(..., run.strategy_run_id)`; report supplies strategy/recommendation/feasibility for allocation (`backend/services/multi_goal_planning_service.py::build_multi_goal_plan`, `backend/services/goal_report_service.py::build_report`). `BasketReportService.build_report()` similarly gets latest run per goal. These are current output, not history.

**SR-2 — version report reads linked-run decisions. CONFIRMED CONFLICT / REMEDIATION REQUIRED, P0.** `/strategy-versions/{id}/report` → `_load_by_strategy_version()` → linked StrategyRun → `build_report()`. It verifies selected-version ID equality, then reads selected strategy, recommendation, scenario and architecture from run. Target owner is StrategyVersion; consumers are reports/PDFs.

**SR-3 — selected version is inferred from run history. CONFIRMED CONFLICT / REMEDIATION REQUIRED, P1.** `StrategyRepository.get_selected_strategy_version_id()` chooses greatest `run_version` with non-null version ID, without requiring latest run or current DefinedGoal version. `on_defined_goal_updated()` can copy old version ID to a run for the new DefinedGoal version.

**SR-4 — action composition reads run architecture. CONFIRMED CONFLICT / REMEDIATION REQUIRED, P1.** `StrategyActionGenerator.generate()` reads linked `run.selected_architecture` to choose supporting strategies and techniques. Architecture composition is absent from StrategyVersion.

Run history/latest-run UI and prior priorities used to seed a *new* build are legitimate history/new-evaluation use. Run-ID report/retirement routes are **COMPATIBILITY ONLY as intended**, but are still callable for current report output and therefore not actually bounded to history. Provenance-only run-ID collection in FinancialPlanService is history use.

**Canonical target:** evaluation/history stays in StrategyRun; immutable StrategyVersion contains finalized strategy, goal version and architecture; all current reports/plans/actions resolve from that version. Regression tests: mutate latest run after finalization and prove outputs do not change; reject goal/version mismatch; generate actions only from version composition.

### 5. Financial State & Metric Audit

**VERIFIED canonical definitions (`backend/engines/calculation/canonical.py`):** liquid-asset ratio = liquid assets / total assets × 100; expense coverage = liquid assets / monthly expenses; emergency coverage = liquid assets / essential monthly expenses; DTI = monthly debt payments / gross monthly income; savings, leverage, financial-asset, insurance, goal/future funding and required-return calculations are also defined there. Moneywheel engine consumes those functions.

**FS-1 — freshness. CONFIRMED CONFLICT / REMEDIATION REQUIRED, P0.** Onboarding mutates raw rows; `FinancialStateSnapshotRepository.get_latest()` orders only by `calculated_at`. GoalService reads latest snapshot and rebuilds only when absent; StrategyService reads latest. Owner/target: backend builder, snapshot bound to raw revision or rebuilt for current decisions. Consumers: feasibility, strategy, analysis, report, action generation. Test: raw mutation then downstream build reflects changed value.

**FS-2 — duplicate formulas. CONFIRMED CONFLICT / REMEDIATION REQUIRED, P1.** `FinancialPlanService._build_moneywheel_health_scan()` and `_build_ratio_constraints()` calculate DTI as outstanding liabilities / annual income and emergency coverage as `(financial_assets * 0.2) / monthly_expenses`. Canonical DTI uses monthly debt payments / gross monthly income; canonical emergency/expense coverage uses classified liquid assets. The 20% estimate’s business owner is **NOT ESTABLISHED**. Target: consume canonical facts and separately named planning rules. Test same fixture yields same canonical metric across surfaces.

### 6. Threshold Ownership Audit

| Threshold | Owner / consumers | Semantic classification and result |
|---|---|---|
| Savings rate: <10, 10–<20, 20–<30, ≥30% | `rules/moneywheel.py::RULES`; 20% constant in `rules/constraints.py`; Moneywheel and constraint evaluator. | Same diagnostic measure; shared 20% boundary is genuine overlap. **VERIFIED**, internal alias remains. |
| Liquid-asset ratio: <10, 10–<15, 15–<25, ≥25% | `rules/moneywheel.py`; Moneywheel. | Liquid/total assets, percent. Not current liquidity. **VERIFIED.** |
| DTI: <20, 20–<30, 30–<40, ≥40% | constants `rules/constraints.py`, bands `rules/moneywheel.py`; evaluator and Moneywheel. | Same payment-service DTI; benchmark strings are duplicate literals. **CONFIRMED overlap; centralize.** |
| Leverage: <20, 20–<30, 30–<50, ≥50% | `rules/moneywheel.py`; RuleEngine critical threshold begins at 30%. | Same metric, different severity in 30–50% range. **CONFIRMED CONFLICT.** |
| Financial asset ratio: <30, 30–<50, 50–<70, ≥70%; plan guardrail 50% | Moneywheel rules and FinancialPlanService. | Diagnostic bands vs plan guardrail; policy identity **NOT ESTABLISHED**. |
| Insurance: <40, 40–<60, 60–<80, ≥80% | Moneywheel rules. | Coverage diagnostic; `insurance_gap_ratio` alias is not inverted. |
| Goal/future funding: <50, 50–<80, 80–<100, ≥100% | Moneywheel rules. | Current and projected metrics are distinct despite shared bands. |
| Required return: <8, 8–<12, 12–<15, ≥15% | Moneywheel rules. | Diagnostic only; suitability cutoff **NOT ESTABLISHED**. |
| Coverage 3/6/9 months | Legacy Moneywheel rules; critical/healthy constants 3/6 in constraint rules. | Expense vs essential-expense denominators differ. Keep separate. |
| Reserve sizing: cash-flow ratio ≤50→3, ≤70→6, ≤85→9, else 12 months | `rules/financial_state.py::required_safety_reserve_months`; FinancialStateEngine. | Reserve amount sizing, not coverage bands. **VERIFIED distinct.** |
| Current liquidity: <0.75, 0.75–<1, 1–<1.5, ≥1.5x | Legacy Moneywheel rule registry; RuleEngine. | Liquid assets / short-term liabilities; no equivalent canonical Moneywheel input is established. Alias substitution is invalid. **CONFIRMED CONFLICT.** |
| Financial-plan guardrails: savings 25% pass/15% conditional, DTI 40%, reserve 6 months, assets 50% | FinancialPlanService. | Same/similar names but mixed purposes; DTI/emergency formulas conflict. Savings/asset policy equivalence **NOT ESTABLISHED**. |
| Goal feasibility | funding gap ≤0 or required ≤ surplus → feasible; positive surplus insufficient → constrained; no surplus → infeasible. | GoalService planning feasibility, not ratio band. **VERIFIED.** |
| Eligibility | contribution ≤ surplus; liquid ≥ reserve; resources ≥ required; risk required ≤ capacity. | Relative comparisons in Strategy eligibility; global risk-capacity cutoff **NOT ESTABLISHED**. |
| Horizon and scenario bands | Horizon score uses <4 / 4–<10 / ≥10; characteristics use ≤5 / ≥7. Scenario funded ratio uses 1/.85/.70. | Distinct strategy purposes; scenario labels do not match cutoffs exactly. **CONFIRMED CONFLICT** on label/boundary. |
| Risk capacity | RiskProfiler records evidence; eligibility compares required risk with capacity. | Separate numeric cutoff **NOT ESTABLISHED**. |

**Owner recommendation:** centralize only identical formula + role thresholds (e.g. DTI bands, savings 20% diagnostic boundary). Preserve reserve sizing, expense coverage and emergency coverage as separate rules. FinancialPlanService values are not canonical until policy intent is established.

### 7. Goal / Funding / Feasibility / Eligibility Vocabulary Audit

- **VERIFIED:** `canonical_goal_type()` owns backend goal taxonomy; GoalService uses it. Strategy eligibility directly reads `GOAL_TYPE_ALIASES`, and frontend duplicates UI labels. Target: backend normalization authority; frontend map presentation-only.
- **CONFIRMED CONFLICT:** `canonical_goal_priority()` maps `Important→high`, etc., but GoalService does not normalize priority before saving. RuleEngine checks raw `critical/high`; other consumers canonicalize. Test aliases yield identical behavior.
- **VERIFIED distinct funding concepts:** goal status `Shortfall/On Track/Overfunded` describes target funding; allocation `fully_funded/partially_funded/unfunded/...` describes distribution of surplus. Keep separate types.
- **NOT ESTABLISHED equivalence:** `constrained` means limited funding in goal/allocation paths; Strategy eligibility `conditional` also covers missing evidence, required change and de-risking. Do not rename without a product decision.
- **VERIFIED eligibility contract:** eight named fits use pass/conditional/fail; numeric checks compare requirement/evidence rather than define global financial cutoffs.

### 8. Legacy Alias Audit

| Alias | Behavior / normalization | Classification |
|---|---|---|
| Legacy goal labels | `rules/goals.py::canonical_goal_type()` normalizes; GoalService uses it; eligibility directly uses alias dict; frontend duplicates labels. | **COMPATIBILITY ONLY** at boundary; **REMEDIATION REQUIRED** for bypass/duplicate map. |
| Priority labels | Normalizer exists but raw input may persist and raw RuleEngine checks remain. | **CONFIRMED CONFLICT.** |
| `savings_ratio` | Legacy snapshot → `savings_rate`; evaluator emits/consumes old key. | Snapshot **COMPATIBILITY ONLY**; internal vocabulary **REMEDIATION REQUIRED**. |
| `liquid_asset_to_total_asset` | Legacy snapshot → `liquid_asset_ratio`. | **COMPATIBILITY ONLY.** |
| `insurance_gap_ratio` | Legacy snapshot → `insurance_coverage_ratio` without inversion. | **COMPATIBILITY ONLY**, name misleading. |
| `emergency_fund_coverage` | Active expense-based constraint/diagnostic input; can reconstruct `expense_coverage`. | **CONFIRMED active competing vocabulary**; not essential-expense emergency coverage. |
| `current_liquidity_ratio` | Liquid/short-term-liability multiple; RuleEngine substitutes liquid-asset percent. | **CONFIRMED CONFLICT.** |
| `expense_ratio` | Moneywheel registry defines need-expense percentage; ProfileEngine emits expense/income ratio unit=`ratio`. | **CONFIRMED competing meaning**; equivalence **NOT ESTABLISHED**. |
| `solvency_ratio` | Registry defines one-minus-leverage; no production consumer located. | Legacy definition; active consumer **NOT ESTABLISHED**. |
| `strat-cap-preservation` | Strategy registry maps to canonical `strat-capital-preservation`. | **COMPATIBILITY ONLY.** |
| Architecture IDs | StrategyService normalizes old IDs to canonical goal+primary identity. | **COMPATIBILITY ONLY.** |
| Report compatibility fields | `goal_funding`, `goal_context`, duplicate top-level fields are emitted. | **COMPATIBILITY ONLY** output. |
| Retirement route / `MoneyWheelEngine` | Legacy run-ID route and public import alias remain. | Import alias **COMPATIBILITY ONLY**; report route remains live authority bypass. |

Canonical ratio output is fixed to nine keys; **CONFIRMED CONFLICT:** `_canonical_rules()` passes any stored two-item `metadata.rules` without key validation. Regression must reject/normalize noncanonical keys.

### 9. Strategy Lifecycle Audit

- **VERIFIED:** StrategyRun contains candidates/scenarios/rankings/recommendation; selection validates against run and remains transient; preview is stateless.
- **CONFIRMED CONFLICT / P1:** finalization inserts provisional StrategyVersion and updates run; no idempotency guard found.
- **CONFIRMED CONFLICT / P1:** DefinedGoal recalculation can carry old StrategyVersion ID to new goal version.
- **CONFIRMED CONFLICT / P1:** StrategyVersion status permits six states, creation service only draft/provisional, while StrategyEditService can request approved for an approved/primary parent; runtime failure is **NOT ESTABLISHED** because tests could not run.
- **Target:** versioning domain owns finalized context; bind version to goal/version/architecture; separate approval state. Tests cover retry, changed goal and edit lifecycle.

### 10. Approval Lifecycle Audit

**NOT ESTABLISHED / REMEDIATION REQUIRED, P1.** Migration defines approval snapshot fields (PU, strategy/version, goal/DefinedGoal, suitability, acknowledgement) and allows authenticated owner insert. No application approval writer was found. `ActionPlanRepository.is_strategy_version_approved()` only checks row existence for PU/version. `StrategyEditService` returns `approval_snapshot_required=False` while action generation requires an approval snapshot. Target: explicit approval command bound to exact PU/goal/DefinedGoal/version/context; validate cross-record ownership and suitability. Backend/frontend approval flow and possibly RLS/schema work. Tests: valid approval, mismatched IDs/context, edited version and action gate.

### 11. Report & Action Plan Audit

- **CONFIRMED CONFLICT / P0:** version report loads linked StrategyRun and reads its decisions; run-ID report/PDF/retirement routes bypass StrategyVersion. Report is generated on demand. `_load()` reads latest FinancialState, not a version-bound snapshot; whether report should be current-state or finalization-state is **NOT ESTABLISHED**.
- **CONFIRMED CONFLICT / P1:** action items are version-keyed, but generator reads linked run architecture to choose supporting strategies/techniques.
- **VERIFIED:** ActionPlan status transitions are guarded in ActionPlanService; planned/confirmed may complete/cancel; terminal actions cannot be modified/deleted.
- **Target:** version contains sufficient goal, architecture and implementation context; current report/actions use only that version; legacy run routes restricted to history/preview. Test latest-run mutation cannot change outputs.

### 12. Execution & Data Integrity Audit

**EX-1 — CONFIRMED CONFLICT / REMEDIATION REQUIRED, P0.** `/api/action-plan/actions/{action_id}/complete` accepts `ActionCompletionRequest.actual_state`; service validates as FinancialState and calls snapshot repository insert. It verifies action ownership/path ID, but does not establish payload values came from server-owned raw records or ensure payload identity matches action. Current authority can be client data. Target: server-derived state or validated narrow execution facts, preserve unrelated financial data, explicit action→snapshot link. Consumers: all latest-snapshot decision paths. Regression: forged financial values, mismatched PU/scope rejected; valid completion records lineage.

`ActionPlanService.complete_action()` is a second completion method that does not save a FinancialState snapshot; no non-test caller found. Active production use **NOT ESTABLISHED**; verify/remove or unify. Test both paths if retained.

### 13. Auth & Ownership Audit

- **VERIFIED:** backend bearer-token authentication and PU ownership helper; child checks validate resource ID with PU; goals also validate investor/assets. Action, strategy, version and DefinedGoal endpoints call applicable helpers.
- **VERIFIED in migration:** raw-table RLS uses owned PU. **CONFIRMED integrity gap:** approval insert RLS checks PU ownership only; it does not demonstrate all referenced foreign records belong to that PU.
- **NOT ESTABLISHED:** production database has applied current migration policies; no live query was made.
- **Target/tests:** validate approval cross-record ownership and run cross-PU IDOR tests for goals, versions, runs, actions, snapshots; test migration policies in integration CI.

### 14. State Machine Audit

| Domain | Evidence-backed state / issue |
|---|---|
| Onboarding | Seven frontend steps; completion derived from row presence. Persisted backend state **NOT ESTABLISHED**. |
| Goal | Backend goal status is string; UI has fixed set. DefinedGoal has `is_latest`, funding and feasibility status. **CONFIRMED contract ambiguity.** |
| StrategyRun | Open status string (`completed`, `recalculated` observed), mutable latest/selection metadata. **CONFIRMED conflict** with immutable history. |
| Selection | Transient until finalization; no separate persisted state. **VERIFIED.** |
| Implementation | Stateless preview → provisional version; duplicate finalize guard absent. **CONFIRMED conflict.** |
| Version / approval | Six version labels plus separate approval snapshot; edit path can request disallowed status. **CONFIRMED conflict.** |
| Report | Generated on demand; fixed `investor_decision_required` status after finalize is ambiguous; persisted report state **NOT ESTABLISHED**. |
| Action | planned → confirmed → completed/cancelled; terminal guards enforced. **VERIFIED.** |
| Execution | Completion methods differ in whether they persist FinancialState. **CONFIRMED conflict.** |

### 15. Frontend ↔ Backend Contract Audit

- **VERIFIED mostly aligned:** frontend Moneywheel field shapes and FinancialState Metric core fields correspond to Pydantic models.
- **CONFIRMED mismatch:** frontend Moneywheel keys are unrestricted strings/lists unbounded; backend enforces 9/2 lengths but stored-rule adapter bypasses rule-key validation.
- **CONFIRMED mismatch:** frontend StrategyRun type includes optional `approval_status` not present in backend and omits backend `what_if_scenarios`.
- **CONFIRMED mismatch:** frontend GoalStatus is closed union; backend GoalInput status is free string. UI priority accepts display and canonical vocabulary; backend field is string.
- **VERIFIED vocabulary split:** StrategyArchitecture uses `conditional`; goal/allocation feasibility uses `constrained`; no normalizer equating them found.
- **Target owner:** backend model/schema contract; generate or contract-test TypeScript types. Tests: serialization fixture, key/status validation, TypeScript compile.

### 16. Documentation / Test Drift

- **CONFIRMED documentation drift:** ontology says Moneywheel has 12 ratios / RULES v1.3; current output model is 9 ratios + 2 rules and RULE_SET_VERSION 2.0.
- **CONFIRMED documentation drift:** target flow says version authority while current multi-goal/basket/report paths consume runs.
- **Stale-to-target tests:** `test_financial_ratio_constraints.py` asserts legacy ratio keys; `test_multi_goal_planning_service.py` and `test_basket_report_service.py` mock latest-run/current report paths. They match present behavior but conflict with target.
- **Coverage gaps:** report-version test does not check linked-run decision/architecture/goal-version consistency; Moneywheel test does not cover stored two-rule pass-through; action tests do not test client actual-state authority.
- **Exact runs:** backend selected suite: 7 collection errors, 0 tests; missing imports/dependencies noted in Section 31. Frontend `npm test`: `tsx: not found`; `npm run typecheck`: `tsc: not found`. These are environment failures, not assertion failures. No dependency install attempted.

### 17. Prioritized Remediation Backlog

| Priority | Problem / evidence | Current → canonical owner / required change | Risk / consumers / impact / regression test |
|---|---|---|---|
| **P0** | Current plans/reports/actions still take latest/linked-run decision data (Sections 32.4, .11). | Mixed Run/Version → complete StrategyVersion. Persist goal/version/architecture and route all current outputs through it. | Stale recommendation/composition. Backend + API; schema likely. Test mutated latest run cannot alter report, basket/plan or actions. |
| **P0** | FinancialState snapshots lack raw revision freshness (Section 32.5). | Latest timestamp → builder tied to raw revision or rebuild. | Stale feasibility/strategy. Backend + onboarding; schema likely for revision. Test mutate raw input, verify downstream. |
| **P0** | Client `actual_state` persisted as latest snapshot (Section 32.12). | Request payload → server-derived/validated execution data. | Arbitrary values affect all planning. Backend/API, possible schema lineage. Test forged values/scope rejected and valid snapshot linked. |
| **P1** | Financial-plan DTI/emergency calculations and leverage status diverge (Sections 32.5–6). | Local calculations → canonical metric plus distinct approved policies. | Misleading plan constraints. Backend. Test same fixture and boundary statuses across outputs. |
| **P1** | Approval writer/validation absent; edit status disagrees with approval-row gate (Section 32.10). | Row existence/status → exact version-bound approval command. | Actions blocked or unlocked inconsistently. Backend/frontend, RLS/schema possible. Test binding, mismatches, edit and action gate. |
| **P1** | Liquidity fallback is unit/formula-incompatible; priority raw aliases persist (Sections 32.6–8). | Fallback/raw labels → distinct canonical metrics and boundary normalization. | Wrong health/ranking. Backend/API. Test invalid alias fallback and equivalent priorities. |
| **P1** | `conditional` vs `constrained` semantics are not resolved (Section 32.7). | Multiple local types → explicit domain-specific types unless approved equivalence. | Consumers conflate limited funding and missing evidence. Backend/frontend; migration only if persisted vocabulary changes. Tests by status meaning. |
| **P2** | Moneywheel rules can bypass key validation; frontend types are underconstrained (Section 32.8, .15). | Stored/free keys → canonical output validation. | Legacy vocabulary escapes API. Backend/frontend. Test invalid metadata and exact nine/two keys. |
| **P2** | Existing tests encode run-ID/legacy-key contracts and miss authority regressions (Section 32.16). | Legacy tests → target contract regressions. | Future changes retain competing authority. Backend/frontend tests only. Execute CI after dependencies available. |
| **P3** | Ontology and flow docs stale/inconsistent (Section 32.16). | Old description → evidence-backed implementation plus approved target. | Agents implement stale contracts. Documentation only after decisions. |

### 18. Canonical Target Architecture

Existing target flow in Sections 1 and 29 remains unchanged:

`Auth → Planning Unit → Raw Data → server-derived FinancialState → canonical metrics → Goal/Feasibility/Constraints → StrategyRun evaluation → selection/preview → immutable StrategyVersion → version-sourced Report → version-sourced Action Plan → server-validated Execution.`

StrategyRun remains history/evaluation. StrategyVersion owns finalized goal/version, architecture composition and implementation parameters. Approval is separate, explicit and version-bound. Legacy aliases normalize only at read/input boundaries; output remains canonical. Execution cannot silently overwrite unrelated FinancialState.

### 19. Final Sign-off Conditions

**Audit status: COMPLETE. System sign-off: NOT READY; remediation required.**

- [ ] StrategyVersion is the sole finalized decision authority for current reports, plans and actions.
- [ ] Version captures goal/version/architecture context; mismatch is rejected.
- [ ] FinancialState freshness is tied to raw revisions or rebuilt before current decisions.
- [ ] DTI, emergency coverage, liquidity and thresholds have explicit owners and consistent consumers.
- [ ] Funding/feasibility/eligibility vocabularies are documented without guessed equivalence.
- [ ] Approval writer, validation, version binding and changed-version behavior are explicit and tested.
- [ ] Client actual-state payload cannot silently overwrite server-authoritative FinancialState.
- [ ] Aliases cannot become business authority or noncanonical output.
- [ ] Frontend/backend types and docs match verified contracts.
- [ ] Relevant regression tests and full CI pass with dependencies installed.
- [ ] A second read-only audit confirms all competing authority paths are removed or bounded.
