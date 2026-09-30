# Planvesto Backend Audit & Cleanup — Coding Agent Instructions

## Objective

Clean and harden the Planvesto backend without changing the product concept, frontend, Supabase schema, or financial-planning philosophy.

The target architecture is:

```text
Financial State
      ↓
Canonical Financial Metrics / Business Rules
      ↓
Moneywheel / Constraints / Goal Engine
      ↓
Strategy Eligibility
      ↓
Strategy Selection
      ↓
Conditional → Adapt → Re-check
      ↓
Multi-Goal Allocation
      ↓
Financial Plan
      ↓
Action Plan
```

## Non-negotiable rules

1. Do NOT redesign the frontend.
2. Do NOT create or modify Supabase migrations/schema unless explicitly required by a proven defect and separately approved.
3. Do NOT rewrite working modules merely for style.
4. Do NOT duplicate business rules to make an engine convenient.
5. Every business rule must have one authoritative definition.
6. Engines apply/evaluate rules; services coordinate workflows; repositories access data; APIs handle transport/authentication.
7. Preserve existing API contracts unless a documented bug requires a breaking change.
8. Preserve audit/version/history behaviour.
9. Every behavioural change must have tests.
10. Do not remove functionality before proving that it is duplicate/dead/obsolete.

---

# Phase 0 — Baseline

Before editing code:

- Run the complete backend test suite.
- Record current failures separately from new failures.
- Inventory every backend directory and Python module.
- Identify API → service → engine → repository/data call paths.
- Do not start refactoring until this baseline is recorded.

Deliverable:
`docs/backend-audit-cleanup/BASELINE.md`

Include:
- test command
- pass/fail counts
- known failures
- Python/runtime assumptions
- current entry points

---

# Phase 1 — Responsibility Map

Create:
`docs/backend-audit-cleanup/RESPONSIBILITY_MAP.md`

For every backend folder, record:

| Layer | Allowed responsibility | Not allowed |
|---|---|---|
| `api/` | HTTP, auth, request/response handling | Financial decisions |
| `schemas/` | Input/output structure validation | Hidden business decisions |
| `services/` | Workflow coordination | Canonical financial rules |
| `engines/` | Calculations/evaluation/decision mechanics | Duplicated rule definitions |
| `rules/` | Authoritative business rules | API/database workflow |
| `library/` | Strategy knowledge/definitions | Investor-specific decisions |
| `data/` | Database access/persistence | Financial policy decisions |
| `models/` | Data structures | Workflow logic |
| `tests/` | Verification | Production logic |

Mark every module as:
- KEEP
- MOVE
- MERGE
- DELETE (only if proven dead/duplicate)
- NEEDS DECISION

---

# Phase 2 — Financial Truth Consolidation

This is the highest-priority cleanup.

Audit these together:
- Moneywheel
- Financial Health
- Health Score
- `rules/moneywheel.py`
- `rules/financial_state.py`
- `engines/rules/`
- `engines/constraints/`
- financial-state engine/service

Find every calculation/classification for:
- cash-flow ratio
- savings/investment rate
- emergency reserve
- liquidity
- debt ratios
- leverage
- insurance/protection baseline
- financial health status
- other Moneywheel metrics

Create:
`docs/backend-audit-cleanup/FINANCIAL_RULE_REGISTRY.md`

For every rule:

| Rule | Current locations | Authoritative location | Consumers | Action |
|---|---|---|---|---|

Target:

```text
ONE canonical calculation/rule
        ↓
multiple consumers
```

Do not maintain separate Moneywheel and Financial Health calculations if they represent the same financial truth.

If Financial Health is only a derived interpretation of canonical metrics, make that relationship explicit rather than creating another calculation system.

---

# Phase 3 — Rule Architecture

Create:
`docs/backend-audit-cleanup/RULE_ARCHITECTURE.md`

Separate:

### Rule
“What is financially/business-wise true?”

### Engine
“How do we calculate/evaluate it?”

### Service
“In what workflow do we use it?”

### Strategy Library
“What reusable strategies exist?”

Audit all hardcoded thresholds and classifications currently hidden inside services/engines.

Move only genuine business rules to the authoritative rule layer.

Do not blindly move calculation code into `rules/` if it is algorithmic rather than policy/business truth.

---

# Phase 4 — Strategy System Audit

Audit:
- `library/strategies/`
- strategy registry/catalog
- strategy components
- eligibility
- applicability
- composition
- decision engine
- ranking
- scenario generation
- recommendation
- strategy versioning
- primary strategy lifecycle

Verify these boundaries:

```text
Strategy Library
= What strategies exist?

Eligibility
= Which strategies are allowed?

Applicability
= Which strategies fit this investor/goal/context?

Adaptation
= Can a conditional strategy be modified to become valid?

Decision
= Which valid strategy should be selected according to the business rules?

Scenario
= What happens under different assumptions?
```

Remove duplicate decision logic only after tracing all callers.

Verify library version and implementation version handling remains intact.

---

# Phase 5 — Conditional Strategy Closure

Implement and test the complete loop:

```text
CONDITIONAL
    ↓
ADAPT
    ↓
RE-CHECK
    ↓
PASS → eligible
FAIL → remove
```

A strategy must not remain eligible merely because it was initially classified as CONDITIONAL.

Add tests for:
- adaptation succeeds
- adaptation fails
- re-check changes status
- adapted strategy is persisted correctly
- failed strategy is excluded from final recommendation

---

# Phase 6 — Financial State Authority

Financial State must be the authoritative investor financial context.

Audit multi-goal orchestration and every place where financial context is constructed.

Do not derive the investor's complete financial context from whichever goal happens to be processed first.

Required direction:

```text
Investor Financial State
        ↓
Goals consume Financial State
        ↓
Strategies consume Financial State + Goal context
```

Add regression tests for multiple goals with materially different properties.

---

# Phase 7 — Multi-Goal Audit

Audit:
- goal ordering
- priority
- available surplus
- resource allocation
- funding gaps
- trade-offs
- partial funding
- conflicting goals
- final consolidated plan

Verify that one goal cannot accidentally mutate another goal's financial context.

Test:
1. one goal
2. two compatible goals
3. two competing goals
4. three goals with insufficient surplus
5. equal priority goals
6. future goal vs near-term goal
7. zero/negative available surplus

---

# Phase 8 — Security & Validation

Audit every API endpoint for:
- authentication
- planning-unit ownership
- goal ownership
- strategy ownership
- strategy-version ownership
- input validation
- numeric bounds
- impossible dates
- negative financial values
- oversized values
- arbitrary dictionaries

Special attention:
`rule_overrides`

Do not allow arbitrary client input to silently modify authoritative financial/business rules.

If overrides are required for simulation/testing, model them explicitly as scenario inputs and keep them separate from production business rules.

Add negative/security tests for cross-user access and invalid financial inputs.

---

# Phase 9 — Repository & Data Integrity

Audit every repository for:
- ownership scoping
- accidental unscoped queries
- repeated queries
- N+1 patterns
- inconsistent version updates
- multi-step writes
- missing transaction boundaries
- stale snapshot handling

Do not optimize prematurely. Fix correctness first.

Where a version/snapshot operation logically requires atomicity, use an appropriate transaction/database function rather than separate writes.

---

# Phase 10 — Service Cleanup

Audit large services, especially Moneywheel and multi-goal planning services.

For each service ask:

> “Is this coordinating a workflow, or is it secretly implementing business policy?”

Extract genuine reusable business rules/calculations from services.

Do not split files merely to reduce file size.

Keep cohesive workflow logic together.

---

# Phase 11 — Dead/Duplicate Code

Search for:
- duplicate functions
- duplicate calculations
- wrapper modules that only forward calls
- obsolete aliases
- unused engines
- placeholder engines exposed as production capabilities
- old strategy IDs
- legacy APIs
- unreachable code

For every candidate:

1. Find all references.
2. Confirm runtime usage.
3. Confirm tests.
4. Confirm frontend/API dependency.
5. Only then merge/remove/replace.

Do not delete based on filename similarity alone.

---

# Phase 12 — QA / End-to-End Verification

Add/strengthen tests for the complete business path:

```text
Financial State
 → Goals
 → Financial Metrics
 → Constraints
 → Eligibility
 → Strategy Selection
 → Adaptation/Re-check
 → Multi-Goal Allocation
 → Financial Plan
 → Action Plan
```

Minimum scenario suite:

- healthy investor
- weak cash flow
- high debt
- insufficient emergency reserve
- single goal
- multiple competing goals
- conditional strategy that becomes valid
- conditional strategy that fails adaptation
- insufficient surplus
- invalid input
- unauthorized investor access

Run the complete suite after every major cleanup phase.

---

# Phase 13 — Final Architecture Gate

Create:
`docs/backend-audit-cleanup/FINAL_AUDIT.md`

Report:

| Category | Before | After | Status |
|---|---|---|---|
| Duplicate financial rules | | | |
| Duplicate calculations | | | |
| Rule ownership | | | |
| Moneywheel/Financial Health | | | |
| Strategy architecture | | | |
| Multi-goal | | | |
| Security | | | |
| Data integrity | | | |
| Test coverage | | | |
| Dead code | | | |

Also include:
- files changed
- files deleted
- files moved
- business rules centralized
- API behaviour changes
- unresolved issues
- tests executed
- known limitations

---

# Coding Agent Execution Rules

## Work order

**Do not attempt the entire cleanup in one uncontrolled refactor.**

Execute in this exact order:

1. Baseline
2. Responsibility map
3. Financial Truth / Moneywheel / Financial Health consolidation
4. Rule architecture
5. Strategy system
6. Conditional adaptation/re-check
7. Financial State authority
8. Multi-goal
9. Security/validation
10. Repository integrity
11. Service cleanup
12. Dead/duplicate code
13. E2E QA
14. Final audit

## After every phase

- Run relevant tests.
- Review git diff.
- Confirm no unrelated files changed.
- Document architectural decisions.
- Do not proceed if a phase introduces unexplained failures.

## Definition of Done

The backend is considered cleaned only when:

- One authoritative source exists for each business rule.
- Financial metrics are calculated once and reused.
- Moneywheel and Financial Health have explicit, non-overlapping responsibilities.
- Services coordinate instead of hiding policy.
- Strategy Library, eligibility, adaptation and decision layers have distinct responsibilities.
- Conditional strategies are re-evaluated after adaptation.
- Financial State is the authoritative investor context.
- Multi-goal allocation works without goal-order dependency.
- Client input cannot override production business rules unintentionally.
- Ownership/security checks are consistent.
- Critical writes preserve data integrity.
- End-to-end business scenarios pass.
- No duplicate/dead component remains without documented justification.

## Important

Do not optimize for “fewer files.”

Optimize for:

**one source of truth + clear responsibility + predictable flow + testable business rules + safe changeability.**
