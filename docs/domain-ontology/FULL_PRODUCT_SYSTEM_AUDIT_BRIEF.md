# Planvesto — Full Product & System Audit Brief

**Repository:** `Bhardwaj1-star/planvesto`  
**Branch:** `main`  
**Mode:** Audit only — no code, schema, migration, or repository changes.

## Objective

Reconstruct Planvesto from the **first user interaction to final execution**, then determine whether the product is:

- architecturally coherent
- canonically centralized
- source-of-truth consistent
- connected through one continuous user journey
- consistent across frontend, backend, persistence, tests, and documentation

Use current code as primary evidence. Documentation is evidence, not truth. Do not invent undocumented business rules.

## Audit Scope

### 1. Product & System Architecture

Map:

`User → Auth → Planning Unit → Onboarding → Financial Data → Financial State → Analysis → Goals → Strategy → Implementation → StrategyVersion → Report → Action Plan → Execution`

Identify for each stage:

- frontend route/component
- API
- backend service/engine
- repository/persistence
- validation
- source of truth
- next state

Also identify architectural boundary violations.

### 2. Complete User Journey

Reconstruct the **actual** journey, not the intended one.

Audit:

- authentication
- planning unit
- onboarding
- financial state
- goals
- financial analysis
- Strategy Builder
- recommendation
- selection
- comparison
- implementation preview/finalization
- StrategyVersion
- Report
- Action Plan
- execution

Produce a journey diagram and stage-by-stage table.

### 3. Domain & Canonicalization

Audit the entire domain, not only goals.

At minimum:

- identities and IDs
- Goal Type/Name/Priority
- Funding
- Feasibility
- Eligibility
- Financial Metrics
- Financial State
- Constraints and thresholds
- Moneywheel
- Strategy
- Technique
- Solution
- Strategy Architecture
- Recommendation
- StrategyRun
- StrategyVersion
- Scenario
- Implementation Parameters
- Report
- Action Plan
- Action Status

For every concept identify:

**Definition → Owner → Normalization → Consumers → Duplicates → Conflicts → Legacy**

Classify findings:

- CANONICAL
- MOSTLY_CANONICAL
- DUPLICATED
- CONFLICTING
- LEGACY
- IMPLICIT
- ORPHANED

### 4. Source of Truth

Determine authoritative state for:

- Financial State
- Goal
- Strategy Recommendation
- Strategy Selection
- StrategyRun
- StrategyVersion
- Report
- Action Plan
- Moneywheel

Detect use of stale/derived authority such as latest runs, ranking position, frontend state, query parameters, or cached state.

### 5. Strategy Architecture

Verify:

`Goal → Strategy → Architecture → Implementation Parameters → StrategyVersion → Report + Action Plan`

Audit strategy identity, architecture identity, primary/supporting strategies, techniques, solutions, scenarios, recommendation, selection, implementation and finalization.

Verify that architecture identity is deterministic, stable and composition-independent.

### 6. Financial Analysis & Constraints

Trace:

`Financial State → Metrics → Diagnostics → Rules → Constraints → Goal Analysis → Strategy Eligibility`

Audit:

- duplicated calculations
- metric shape mismatches
- duplicated thresholds
- diagnostic vs hard-constraint semantics
- constraint severity/role/kind
- financial capacity and feasibility

Identify the authoritative owner of every important threshold.

### 7. Moneywheel

Verify the current canonical contract:

**9 ratios**

- savings_rate
- liquid_asset_ratio
- debt_to_income_ratio
- leverage_ratio
- financial_asset_ratio
- insurance_coverage_ratio
- goal_funding_ratio
- future_funding_ratio
- required_rate_of_return

**2 rules**

- expense_coverage
- emergency_coverage

Find legacy definitions, aliases, stale tests/docs, and frontend/backend mismatches.

### 8. Frontend ↔ Backend

Compare schemas, API responses, TypeScript types and actual usage.

Find:

- field mismatches
- enum/status mismatches
- stale fields
- optionality mismatches
- frontend business-rule duplication
- client-controlled decisions

### 9. State Machines & Failure States

Build state machines for:

- onboarding
- goals
- strategy
- StrategyRun
- StrategyVersion
- Action Plan

Audit:

- valid/invalid transitions
- missing transitions
- impossible states
- frontend-only enforcement

Test behavior for:

- incomplete onboarding
- no goals
- missing financial state
- infeasible goals
- no eligible strategy
- missing StrategyVersion
- missing implementation
- missing report
- missing actions
- completed/cancelled actions
- legacy data
- malformed data
- invalid/unauthorized IDs

### 10. Security & Data Integrity

Audit authentication, authorization, planning-unit ownership, goal/version/action/report ownership, client-supplied IDs, IDOR risks, server-side validation and RLS assumptions.

Do not perform destructive tests.

### 11. Tests, Legacy & Documentation

Audit:

- stale tests
- missing regression coverage
- obsolete routes/APIs
- old workflow assumptions
- dead/orphaned code
- compatibility paths
- stale documentation

Compare findings against:

`docs/domain-ontology/CANONICAL_CENTRALIZATION_AUDIT.md`

Explicitly identify:

- already known findings
- new findings
- contradictions
- findings already fixed in current main

## Evidence Standard

Every significant finding must include:

- severity: P0/P1/P2/P3
- file path
- symbol/component
- evidence
- affected journey
- downstream impact

**P0:** production correctness, data integrity, source-of-truth failure  
**P1:** architectural/business-rule conflict  
**P2:** canonicalization, maintainability, contract inconsistency  
**P3:** cleanup/documentation

If something cannot be established from code, state:

**NOT ESTABLISHED FROM CODE**

## Final Deliverable

Return:

1. Executive Summary
2. Actual System Architecture
3. Complete User Journey + Diagram
4. End-to-End Data Flow
5. Source-of-Truth Map
6. Domain Canonicalization Matrix
7. Strategy Architecture Audit
8. Financial/Constraint Audit
9. Moneywheel Audit
10. Frontend ↔ Backend Contract Audit
11. State Machines
12. Failure-State Matrix
13. Security/Data Integrity Findings
14. Tests/Legacy/Documentation Findings
15. Existing Audit vs New Findings
16. Master Findings Matrix
17. Prioritized Remediation Backlog

For remediation, **do not implement**. Only specify:

- problem
- evidence
- affected files
- affected user journey
- canonical target state
- dependencies
- regression tests required
- whether backend/frontend/schema work would be required

## Critical Rule

Do not stop at grep/search results. Trace actual execution paths and cross-module dependencies.

The audit must answer:

> **What is Planvesto today, how does a user actually move through it, where does each decision come from, what is canonical, what conflicts, what is legacy, and what must be fixed first?**
