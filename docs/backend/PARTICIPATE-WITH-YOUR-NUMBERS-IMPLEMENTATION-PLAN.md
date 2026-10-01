# Planvesto — Participate With Your Numbers
## Complete Implementation Plan: Zero → Advanced

**Repository:** Bhardwaj1-star/planvesto  
**Target branch:** backend-audit-cleanup  
**Feature:** Participate With Your Numbers  
**Scope:** Backend-first implementation with frontend interaction contract  
**Database rule:** No Supabase schema change and no SQL migration

---

## 1. Feature Definition

Participate With Your Numbers is the investor interaction layer that sits on top of the existing Goal + Strategy + Scenario system.

It answers:

> “Agar main apne actual numbers ko change karun, to outcome kya badlega?”

The investor can modify supported financial assumptions such as:

- monthly contribution
- initial lump sum
- annual contribution step-up
- goal target
- goal date / horizon
- supported funding structure parameters

The system then recalculates:

- projected outcome
- funding gap
- required contribution
- feasibility
- relevant constraints
- relevant technique outputs
- trade-offs
- delta from baseline

The feature is NOT a second Strategy Engine, Goal Engine, calculator, optimization engine, or product selector.

---

# 2. Product Principle

The intended flow is:

    Financial State
          ↓
        Goal
          ↓
      Constraints
          ↓
       Strategy
          ↓
    Solution / Variant
          ↓
    Baseline Scenario
          ↓
    Participate With Your Numbers
          ↓
    Investor Overrides
          ↓
    Recalculation
          ↓
    Constraint Re-evaluation
          ↓
    Baseline Comparison
          ↓
    Trade-offs
          ↓
    Investor Decision

The backend remains the financial authority.

The frontend collects inputs and presents canonical results.

---

# 3. Why This Feature Exists

The existing Scenario Engine already generates deterministic What-if scenarios:

- contribution +10%, +25%, +50%
- goal date +1, +3 years
- target -10%, -20%
- annual step-up 10%, 20%

Those answer:

> “What happens under predefined changes?”

Participate answers:

> “What happens if I choose my own numbers?”

Example:

    Baseline:
    SIP = ₹25,000/month

    Investor:
    “I can invest ₹32,000/month.”

    Participate:
    SIP = ₹32,000/month

    System:
    - recalculates funding
    - recalculates feasibility
    - recalculates constraints
    - compares against baseline
    - explains the trade-offs

---

# 4. Existing Architecture to Reuse

The feature must reuse the current canonical architecture.

## Goal layer

Existing:

- DefinedGoal
- goal calculation
- funding gap
- feasibility
- funding strategies

Relevant areas:

    backend/models/defined_goal.py
    backend/services/goal_service.py
    backend/engines/goal/

## Strategy layer

Existing:

- canonical Strategy Library
- strategy applicability
- eligibility
- architecture composition
- variants
- Solution Matrix
- investor priorities
- decision evaluation
- ranking
- recommendation

Relevant areas:

    backend/engines/strategy/
    backend/library/strategies/
    backend/services/strategy_service.py

## Scenario layer

Existing:

    backend/engines/strategy/scenario.py

Already provides:

- baseline scenario generation
- deterministic What-if scenarios
- custom scenario creation
- future-value helpers
- step-up calculations
- funding metrics

Do NOT duplicate these formulas inside Participate.

## Constraint layer

Existing:

    backend/engines/constraints/

Canonical ConstraintSet already contains:

- domain
- source
- source engine
- severity
- role
- kind
- passed
- message
- value
- unit
- goal ID
- evidence
- confidence
- validity
- suggested override priority
- override reason

Participate must consume and re-evaluate this canonical model.

## Technique layer

Existing:

    backend/engines/technique/engine.py

All canonical techniques have executable handlers.

Participate should re-run relevant techniques when changed inputs affect them.

## Reporting

Existing:

    backend/services/goal_report_service.py

The final report can later include baseline + investor scenario + trade-offs.

---

# 5. Canonical Centralized Architecture

There is ONE canonical backend representation.

Frontend may group it for presentation.

Correct:

    Canonical ConstraintSet
            ↓
       API response
            ↓
      Frontend grouping
            ├── What changed
            ├── What improved
            ├── What worsened
            ├── What cannot be violated
            └── What this means

Incorrect:

    Frontend:
    if debt_ratio > X:
        create a new financial constraint

The frontend must never create or reinterpret financial business rules.

Backend metadata such as role, severity, passed, domain and evidence is the source of truth.

---

# 6. Baseline vs Participated State

Every Participate evaluation has two conceptual states.

## Baseline

The original system-generated scenario.

Contains:

- planning unit
- StrategyRun
- goal
- strategy
- scenario
- architecture
- assumptions
- financial context
- constraints
- calculated outcomes

## Participated

The investor-modified derived scenario.

Contains:

- baseline reference
- explicit investor overrides
- effective inputs
- recalculated outputs
- recalculated constraints
- feasibility
- comparison
- trade-offs
- warnings
- provenance

The participated state MUST NOT overwrite the baseline.

---

# 7. Baseline Identity

A Participate request must reference a valid baseline.

Minimum identity:

- planning_unit_id
- strategy_run_id
- goal_id
- strategy_id
- scenario_id where applicable

Optional:

- architecture_id
- variant_id

The backend must resolve and validate this identity server-side.

---

# 8. Investor Override Model

Only explicitly changed values are overrides.

Conceptual request:

    {
      "monthly_contribution": 32000,
      "initial_lumpsum": 250000,
      "annual_step_up_pct": 10,
      "target_amount": null,
      "goal_date": null
    }

A missing field means:

> Keep the baseline value.

It does NOT mean zero.

The override whitelist must be explicit.

---

# 9. Authority of Inputs

## Investor-controlled

- contribution
- lump sum
- step-up
- target
- goal date / horizon
- supported funding parameters

## System-controlled

- formulas
- calculation method
- constraint classification
- feasibility state
- warnings
- provenance
- canonical strategy and technique identity

## Goal-controlled

- goal identity
- goal type
- original goal definition

## Financial-state-controlled

- existing assets
- income
- expenses
- liabilities
- declared surplus
- mapped resources

---

# 10. Critical Rule: Scenario Override Is Not Financial-State Mutation

If the investor says:

> “Main ₹40,000 SIP kar sakta hoon.”

that means:

> Evaluate a scenario using ₹40,000/month.

It does NOT automatically mean:

> Update the investor's Financial State to ₹40,000/month.

Participate initially creates a scenario override.

Financial State changes only through the existing financial-state workflow.

This prevents accidental corruption of canonical user data.

---

# 11. Effective Scenario Construction

The engine constructs:

    Effective Inputs
    =
    Baseline Inputs
    +
    Explicit Investor Overrides

Example:

    Baseline:
    monthly_contribution = 25,000
    step_up = 0%
    horizon = 12 years
    target = 75,00,000

    Override:
    monthly_contribution = 32,000

    Effective:
    monthly_contribution = 32,000
    step_up = 0%
    horizon = 12 years
    target = 75,00,000

No unrelated input may silently change.

---

# 12. Core Recalculation Pipeline

The complete execution path should be:

    1. Authenticate user
    2. Validate planning-unit ownership
    3. Load baseline StrategyRun
    4. Validate goal ownership
    5. Resolve baseline scenario
    6. Load baseline financial context
    7. Validate investor overrides
    8. Build effective scenario
    9. Recalculate goal funding
    10. Recalculate relevant strategy metrics
    11. Re-evaluate constraints
    12. Re-evaluate feasibility
    13. Re-run relevant techniques
    14. Compare against baseline
    15. Generate trade-offs
    16. Return canonical ParticipateResult

No step may bypass the canonical domain engines.

---

# 13. Goal Funding Participation

Example baseline:

    Target = ₹75 lakh
    Horizon = 12 years
    Existing mapped assets = ₹5 lakh
    SIP = ₹25,000/month

Investor changes:

    SIP = ₹32,000/month

The engine calculates:

- new projected funding
- new funding gap
- feasibility
- surplus impact
- constraint changes
- delta vs baseline

The result should expose both states.

    Baseline:
    contribution = ₹25k
    gap = X
    feasibility = Y

    Participated:
    contribution = ₹32k
    gap = A
    feasibility = B

    Delta:
    contribution = +₹7k
    gap = A - X
    feasibility = changed/unchanged

The exact numbers must come from the canonical calculation layer.

---

# 14. Goal Date Participation

If the investor changes the goal date:

1. derive the new horizon
2. re-project mapped assets
3. recalculate funding
4. recalculate feasibility
5. re-evaluate constraints
6. compare with baseline

Existing mapped assets must be projected using the new horizon.

Never blindly reuse the original projected mapped-asset value.

---

# 15. Target Participation

If target changes:

- keep original target as baseline
- use new target in participated scenario
- recalculate funding gap
- recalculate required contribution
- recalculate feasibility
- recalculate affected scenario metrics

The original goal object must not be overwritten.

---

# 16. Step-up Participation

If annual step-up changes:

    Year 1 = baseline contribution
    Year 2 = Year 1 × (1 + step-up)
    Year 3 = Year 2 × (1 + step-up)
    ...

Use the canonical step-up calculation.

Do not implement arithmetic in frontend.

---

# 17. Lump-sum Participation

Distinguish:

1. existing mapped assets
2. investor-entered additional lump sum

An additional lump sum is a scenario assumption.

It should not silently become a new permanent asset in Financial State.

If an affordability or liquidity constraint applies, it must be evaluated against the canonical constraint system.

---

# 18. Strategy Integrity

Participate does not automatically switch strategy.

Example:

    Strategy = Goal Funding
    Variant = SIP

Investor changes:

    monthly contribution = ₹40,000

The scenario remains within the same strategy/variant unless the investor explicitly selects another valid solution.

If a modification invalidates the selected strategy, return:

    status = invalidated

with an explicit reason.

Never silently substitute another strategy.

---

# 19. Scenario Status

Recommended statuses:

- valid
- valid_with_warning
- constrained
- infeasible
- invalidated
- insufficient_inputs

These describe the scenario.

They are NOT recommendation rankings.

---

# 20. Constraint Re-evaluation

After recalculation:

    Modified Inputs
          ↓
      Calculation
          ↓
    Constraint Engine
          ↓
    New ConstraintSet
          ↓
    Baseline comparison

For each relevant constraint, calculate:

- unchanged
- newly passed
- newly failed
- still passed
- still failed
- no longer applicable
- insufficient inputs

Example:

    Baseline:
    affordability = passed

    Participated:
    affordability = failed

Return an explicit constraint delta.

---

# 21. Constraint Delta Model

Conceptual structure:

    {
      "constraint_id": "...",
      "baseline": {
        "passed": true,
        "value": 0.31
      },
      "participated": {
        "passed": false,
        "value": 0.46
      },
      "change": "newly_failed",
      "message": "..."
    }

Do not infer business severity in frontend.

Use canonical backend metadata.

---

# 22. Frontend Constraint Grouping

Recommended presentation groups:

## What you changed

Directly from override input.

## What improved

Metrics/constraints with positive evidence-backed change.

## What worsened

Metrics/constraints with negative evidence-backed change.

## What cannot be violated

Canonical hard constraints and eligibility failures.

## What this means

Backend-generated explanation and trade-off evidence.

These are UI groups, not new business-domain entities.

---

# 23. Trade-off Engine

Raw numbers are not enough.

Participate must explain:

    What changed
        ↓
    What improved
        ↓
    What worsened
        ↓
    Which constraint changed
        ↓
    What the financial consequence is

Example:

    Change:
    contribution +₹7,000/month

    Benefit:
    funding gap decreases

    Cost:
    monthly surplus headroom decreases

    Constraint:
    affordability remains passed

    Meaning:
    higher contribution improves goal funding while consuming more monthly cash-flow capacity

Trade-offs must be generated from actual calculated evidence.

No generic filler.

---

# 24. Comparison Engine

Input:

    Baseline
    Participated

Output:

- metric deltas
- funding deltas
- feasibility delta
- constraint deltas
- technique deltas where applicable
- warnings
- trade-offs

Example:

    monthly_contribution:
      baseline = 25,000
      participated = 32,000
      delta = +7,000

    funding_gap:
      baseline = X
      participated = Y
      delta = Y - X

---

# 25. Technique Execution

If the selected architecture contains techniques, Participate should re-run affected techniques.

Example:

    Goal date changes
          ↓
    Glide Path affected
    Bucketing affected
    Cash-flow Matching affected

The existing TechniqueEngine remains authoritative.

Technique output remains:

- technique_id
- status
- inputs
- parameters
- outputs
- warnings

Techniques that require unavailable inputs must return insufficient_inputs rather than invented assumptions.

---

# 26. Technique Impact Optimization

Initial version may safely execute all relevant techniques in the selected architecture.

Advanced version can declare required inputs per technique and run only affected handlers.

Example:

    goal_date change
        ↓
    affected input map
        ↓
    affected techniques
        ↓
    selective execution

Correctness comes before this optimization.

---

# 27. Participate Is Not Optimization

Participate answers:

> “What happens if I choose X?”

Optimization answers:

> “What X should I choose to satisfy competing objectives?”

Do not implement optimization inside Participate.

Future architecture may be:

    Participate
        ↓
    Optimization
        ↓
    Candidate scenarios
        ↓
    Constraint filtering
        ↓
    Multi-objective comparison

That is a separate milestone.

---

# 28. Participate Is Not Probability

Do not invent probability.

Existing Scenario logic intentionally uses:

    probability = None
    method = not_estimated

Participate must preserve this.

A future Probability Engine, if needed, must be separate.

---

# 29. Proposed Backend Structure

Recommended implementation targets:

    backend/
      engines/
        participate/
          __init__.py
          engine.py
          models.py
          validation.py
          comparison.py
          tradeoffs.py

      schemas/
        participate.py

      services/
        participate_service.py

      api/
        participate.py

These are target boundaries, not permission to create unnecessary abstractions.

---

# 30. Participate Engine

Responsibility:

- effective scenario construction
- calculation orchestration
- constraint re-evaluation
- feasibility evaluation
- technique execution
- comparison
- trade-off generation

Must NOT own:

- HTTP
- authentication
- persistence
- frontend formatting
- product selection
- Financial State mutation

---

# 31. Validation Layer

Validate:

- contribution >= 0
- lump sum >= 0
- step-up within supported range
- target > 0 where required
- valid goal date
- compatible funding structure
- supported override
- supported scenario
- required baseline inputs

Distinguish clearly:

### Invalid input

The value itself is structurally invalid.

### Infeasible scenario

The input is valid, but the financial goal cannot be funded.

### Constraint violation

The input is valid but conflicts with a financial constraint.

These are different states and different messages.

---

# 32. API Design

Primary endpoint:

    POST /api/strategy/participate

Conceptual request:

    {
      "planning_unit_id": "...",
      "strategy_run_id": "...",
      "scenario_id": "...",
      "overrides": {
        "monthly_contribution": 32000,
        "annual_step_up_pct": 10
      }
    }

Response:

    ParticipateResult

The first implementation should be stateless.

---

# 33. Optional Comparison Endpoint

Only if useful after the first API is implemented:

    POST /api/strategy/participate/compare

Purpose:

    baseline
       vs
    investor scenario

It can return:

- metric deltas
- feasibility delta
- funding delta
- constraint changes
- trade-offs

If evaluate already returns these, a separate endpoint is unnecessary.

---

# 34. Persistence Strategy

Recommended first version:

**Stateless evaluation**

    POST /participate
          ↓
       calculate
          ↓
        return

Advantages:

- no schema changes
- less persistence complexity
- easier testing
- baseline remains immutable
- simple rollback

Persistence should be added only if the product requires:

- saving scenarios
- scenario history
- revisiting
- sharing
- report persistence
- audit trail

Prefer existing StrategyRun metadata before introducing new database structures.

---

# 35. Database Constraint

Non-negotiable current project rule:

> Do not modify Supabase schema.

Therefore initial Participate implementation must NOT add:

- Participate table
- migration
- RLS migration
- schema column

Existing StrategyRun metadata may be reused where appropriate.

---

# 36. Security

Every request must verify:

1. authenticated user
2. planning unit ownership
3. StrategyRun ownership
4. goal relationship
5. scenario relationship
6. scenario validity

Never trust client-supplied IDs without server-side verification.

No frontend-only authorization.

---

# 37. Frontend Workspace

Conceptual UI:

    Participate Workspace
    │
    ├── Baseline Summary
    │
    ├── Your Numbers
    │   ├── Contribution
    │   ├── Lump Sum
    │   ├── Step-up
    │   ├── Goal Target
    │   └── Goal Date
    │
    ├── Live Result
    │   ├── Projected Value
    │   ├── Funding Gap
    │   ├── Feasibility
    │   └── Required Contribution
    │
    ├── What Changed
    ├── Constraints
    ├── Trade-offs
    └── Reset / Compare / Apply

The frontend does not perform financial calculations.

---

# 38. Frontend Data Flow

Initial correct flow:

    User changes number
          ↓
    frontend sends override
          ↓
    POST /api/strategy/participate
          ↓
    Participate Engine
          ↓
    canonical result
          ↓
    frontend renders

A debounce may be used for UX, but it does not change business authority.

---

# 39. Reset

Reset means:

    overrides = {}

It does NOT:

- delete StrategyRun
- mutate Goal
- mutate Financial State
- create a new permanent scenario

The result should return to the baseline.

---

# 40. Apply

Recommended initial meaning:

> Apply this participated scenario as the investor's selected scenario.

It should not silently:

- overwrite the original goal
- overwrite Financial State
- replace the original baseline
- change Strategy Library identity

If persistence is needed, create a derived scenario/version using the existing persistence architecture.

---

# 41. Investor Decision Authority

The system provides evidence.

The investor makes the final decision.

Example system output:

    Contribution increases by ₹7,000/month.
    Funding gap decreases by X.
    Monthly liquidity headroom decreases by Y.
    Constraint Z remains satisfied.

This is decision support.

Participate must not turn a user-entered scenario into an automatic permanent recommendation.

---

# 42. Report Integration

Goal Decision Report should eventually include:

1. baseline assumptions
2. investor overrides
3. effective assumptions
4. participated outcome
5. baseline vs participated comparison
6. changed constraints
7. trade-offs
8. technique execution evidence
9. final investor-selected scenario
10. provenance

Conceptually:

    Baseline Decision
          +
    Investor Participation
          =
    Decision Journey

---

# 43. Provenance

Every persisted or reportable Participate result should be traceable to:

- baseline StrategyRun
- goal
- strategy
- scenario
- overrides
- calculation version
- strategy version
- generation time
- scenario type

Recommended conceptual metadata:

    {
      "baseline_run_id": "...",
      "goal_id": "...",
      "strategy_id": "...",
      "scenario_id": "...",
      "calculation_version": "...",
      "strategy_version": "...",
      "scenario_type": "investor_participated"
    }

---

# 44. Versioning

Participate must not depend on an implicit forever-current calculation.

If a result is persisted, it should identify the versions needed to reproduce it.

At minimum:

- calculation version
- strategy version
- technique version where relevant

This becomes important for auditability.

---

# 45. Error Contract

Recommended error categories:

- baseline_not_found
- scenario_not_found
- unsupported_override
- invalid_input
- insufficient_inputs
- invalidated
- infeasible
- unauthorized

Never return fake numbers for missing data.

Bad:

    projected_value = 0

when the required input is missing.

Good:

    status = insufficient_inputs
    warning = explicit missing input

---

# 46. Edge Cases

Must test:

### Contribution

- zero
- negative
- baseline value
- slightly above baseline
- slightly below baseline
- very high value

### Lump sum

- zero
- baseline
- additional lump sum
- invalid/unsupported value

### Step-up

- zero
- supported percentage
- negative
- extreme

### Goal date

- unchanged
- earlier
- later
- invalid/past date

### Target

- unchanged
- lower
- higher
- zero
- negative

### Feasibility transitions

- feasible → feasible
- constrained → feasible
- feasible → constrained
- constrained → infeasible
- feasible → infeasible

### Constraints

- passed → passed
- passed → failed
- failed → passed
- failed → failed

### Strategy

- remains applicable
- becomes constrained
- becomes invalidated

---

# 47. Baseline Immutability Invariant

Participate must never mutate the baseline.

Conceptually:

    baseline = immutable reference/snapshot
    participated = derived scenario

This enables:

- reset
- comparison
- audit
- repeated experimentation
- report generation

---

# 48. Golden Regression Invariant

The most important test:

    Participate(Baseline, {})
    ==
    Baseline

apart from expected metadata differences.

If no override is supplied, Participate must reproduce the baseline calculation.

This proves that Participate is an interaction layer rather than a second financial engine.

---

# 49. Single-Override Invariant

If only one input changes:

    override = { monthly_contribution: X }

then unrelated baseline inputs must remain unchanged.

Verify:

- target
- goal date
- existing assets
- return assumption
- step-up
- funding structure
- strategy identity

Only logically derived values may change.

---

# 50. Determinism

For identical:

- baseline
- overrides
- calculation version
- strategy version

the result must be deterministic.

No random values.

No hidden market forecast.

No implicit probability.

No time-dependent assumption except explicitly versioned timestamps.

---

# 51. Multiple Participations

The investor may test:

    Scenario A:
    ₹30k SIP

    Scenario B:
    ₹35k SIP

    Scenario C:
    ₹30k + 10% step-up

Each is an independent derived scenario.

One participation must not become the implicit baseline for the next unless the user explicitly chooses it.

---

# 52. Multi-Scenario Comparison

Future UI may show:

| Metric | Baseline | Scenario A | Scenario B |
|---|---:|---:|---:|
| Monthly contribution | ₹25k | ₹30k | ₹35k |
| Projected value | X | Y | Z |
| Funding gap | X | Y | Z |
| Feasibility | constrained | constrained | feasible |
| Monthly headroom | X | Y | Z |

The comparison engine owns the values.

---

# 53. Multi-Goal Boundary

Initial Participate is an individual-goal feature.

Do not pretend that changing Goal A automatically resolves Goal B.

Example:

    Goal A contribution increases
          ↓
    available monthly surplus decreases
          ↓
    Goal B may become less feasible

That is a Multi-goal Orchestration problem.

Future architecture:

    Goal Scenario
        ↓
    Multi-goal impact analysis
        ↓
    Other goals affected?
        ↓
    Consolidated Financial Plan

---

# 54. No Optimization Engine Yet

Do not create:

    backend/engines/optimization/

just for Participate.

Optimization is a later capability.

Participate is:

    user chooses X
        ↓
    system evaluates X

Optimization is:

    system searches X
        ↓
    system compares X
        ↓
    system proposes candidates

Keep the boundary clean.

---

# 55. No Probability Engine Yet

Do not create probability logic inside Participate.

If probability is eventually required, it belongs to a dedicated Probability Engine.

Current behaviour remains:

    probability = None
    method = not_estimated

---

# 56. Testing Strategy

## Unit tests

Test:

- override validation
- baseline merge
- effective scenario
- comparison
- constraint delta
- trade-off generation

## Engine tests

Test:

- SIP
- lump sum
- step-up
- goal date
- target
- existing assets
- funding variants

## Integration tests

Test:

    StrategyRun
        ↓
    Participate
        ↓
    Scenario Engine
        ↓
    Goal Engine
        ↓
    ConstraintSet
        ↓
    Comparison

## API tests

Test:

- authentication
- ownership
- valid request
- invalid request
- missing baseline
- missing scenario
- unsupported override
- insufficient inputs

## Regression tests

Verify existing Strategy Engine output remains unchanged when no overrides are supplied.

---

# 57. Performance

Initial implementation should be synchronous and deterministic.

Later optimizations may include:

- baseline context caching
- affected-technique calculation
- calculation memoization
- parallel independent technique execution

Do not introduce asynchronous infrastructure before it is needed.

---

# 58. Observability

Log safely:

- StrategyRun ID
- goal ID
- scenario ID
- override field names
- execution status
- error code
- duration

Avoid unnecessary logging of raw personal financial values.

---

# 59. Proposed Implementation Phases

## Phase 0 — Contract

Define:

- Participate terminology
- override whitelist
- baseline/participated state
- result schema
- status model
- provenance
- security contract

Exit:

- contract stable
- no duplicate business ownership

## Phase 1 — Core Engine

Build:

- ParticipateInput
- override validation
- effective scenario builder
- Goal/Scenario recalculation
- ConstraintSet re-evaluation
- ParticipateResult

Exit:

- one valid baseline can be modified
- baseline remains unchanged
- result is deterministic

## Phase 2 — Comparison

Build:

- metric delta
- funding delta
- feasibility delta
- constraint delta

Exit:

- baseline vs participation is explainable

## Phase 3 — Trade-offs

Build:

- evidence-backed trade-offs
- positive impact
- negative impact
- binding constraints
- warnings

Exit:

- every material change has an explanation

## Phase 4 — Technique Integration

Build:

- affected technique detection
- TechniqueEngine execution
- technique evidence

Exit:

- changed inputs affect relevant techniques

## Phase 5 — API

Build:

    POST /api/strategy/participate

with:

- auth
- ownership
- validation
- typed response

Exit:

- secure end-to-end backend flow

## Phase 6 — Frontend Workspace

Build:

- baseline
- input controls
- live result
- constraint groups
- trade-offs
- reset
- compare
- apply

Exit:

- investor can participate without seeing engine complexity

## Phase 7 — Optional Persistence

Only if product workflow requires:

- save
- retrieve
- history
- versioning

Prefer existing StrategyRun metadata first.

## Phase 8 — Report Integration

Add:

- overrides
- participated result
- comparison
- trade-offs
- final selected scenario
- provenance

## Phase 9 — Multi-goal Impact

Later:

- surplus competition
- cross-goal constraints
- resource allocation
- goal prioritization
- consolidated plan impact

---

# 60. Current Known Gaps

The current repository already has the foundation, but does NOT yet constitute a complete Participate feature.

Missing/partial:

- dedicated Participate Engine
- Participate schemas
- Participate service
- Participate API
- baseline vs participated contract
- constraint delta contract
- trade-off engine
- investor-authored scenario workspace
- explicit frontend workspace
- optional participation persistence
- report integration for participated scenarios
- multi-goal impact propagation

Already available:

- Goal Engine
- Scenario Engine
- custom scenario support
- ConstraintSet
- Strategy Engine
- Technique Engine
- StrategyRun
- Goal Decision Report
- PDF reporting

---

# 61. Files to Inspect Before Coding

Before Phase 1, inspect these current implementations:

    backend/engines/strategy/scenario.py
    backend/engines/strategy/engine.py
    backend/engines/strategy/decision.py
    backend/engines/strategy/composition.py
    backend/engines/technique/engine.py
    backend/engines/constraints/models.py
    backend/engines/constraints/evaluator.py
    backend/engines/constraints/aggregator.py
    backend/engines/goal/engine.py
    backend/engines/goal/funding_strategies.py
    backend/models/strategy.py
    backend/models/defined_goal.py
    backend/services/strategy_service.py
    backend/services/goal_service.py
    backend/data/strategy_repository.py
    backend/services/goal_report_service.py
    backend/schemas/strategy.py
    backend/api/strategy.py

The purpose of this inspection is reuse and interface alignment, not redesign.

---

# 62. Refactoring Rule

Refactor existing code only when necessary to support a clean Participate boundary.

Do not:

- rewrite Strategy Engine
- rewrite Goal Engine
- redesign Strategy Library
- change Supabase schema
- change frontend architecture unrelated to Participate
- introduce duplicate calculation helpers

The feature should be an extension of the current architecture.

---

# 63. Final Architecture

Individual-goal flow after completion:

    Financial State
          ↓
        Goal
          ↓
    ConstraintSet
          ↓
    Strategy Engine
          ↓
    Strategy Architecture
          ↓
    Baseline Scenario
          ↓
    ┌─────────────────────────────┐
    │ Participate Engine          │
    │                             │
    │ Investor Overrides          │
    │       ↓                     │
    │ Effective Scenario          │
    │       ↓                     │
    │ Recalculation               │
    │       ↓                     │
    │ Constraints + Techniques    │
    │       ↓                     │
    │ Comparison + Trade-offs     │
    └─────────────────────────────┘
          ↓
    Investor Decision
          ↓
    Goal Decision Report

---

# 64. Advanced Future Architecture

Eventually:

    Financial State
          ↓
        Goals
          ↓
    Multi-goal ConstraintSet
          ↓
    Strategy Engine
          ↓
    Baseline Financial Plan
          ↓
    Participate Workspace
          ↓
    Investor Scenario
          ↓
    Multi-goal Impact Analysis
          ↓
    Investment Planning
          ↓
    Product Suitability
          ↓
    Implementation Plan
          ↓
    Monitoring / Adaptation

Participate is therefore the human interaction bridge between system-generated planning and investor-owned decision making.

---

# 65. Definition of Done

Participate With Your Numbers is complete when:

- investor can select a valid baseline scenario
- investor can modify supported inputs
- backend validates all overrides
- baseline remains immutable
- effective scenario is constructed correctly
- canonical calculations are reused
- Goal Engine is reused
- Scenario Engine is reused
- constraints are recalculated
- feasibility is recalculated
- relevant techniques are recalculated
- baseline vs participated state is compared
- trade-offs are evidence-backed
- invalid scenarios are explicit
- missing inputs never produce fake values
- Financial State is not mutated by scenario overrides
- API enforces authentication and ownership
- frontend consumes canonical output
- frontend does not recreate business rules
- reset returns to baseline
- repeated evaluation is deterministic
- report can explain the participated scenario
- tests cover the complete pipeline
- no Supabase schema migration is required

---

# 66. Non-Negotiable Engineering Rules

1. Backend canonical model is the source of truth.
2. Frontend grouping is presentation only.
3. Do not modify Supabase schema.
4. Do not create SQL migrations for Participate.
5. Do not duplicate financial formulas.
6. Do not move financial rules into frontend.
7. Do not mutate Financial State from a scenario override.
8. Do not silently switch strategy.
9. Do not invent missing assumptions.
10. Do not invent probability.
11. Do not make Participate an optimization engine.
12. Do not merge deterministic What-if and investor Participate into one conceptual feature.
13. Do not overwrite baseline scenarios.
14. Do not bypass ConstraintSet.
15. Do not bypass canonical Strategy/Technique identity.
16. Do not expand scope into Product Selection or Investment Planning prematurely.
17. Do not use a new database structure unless the existing persistence mechanism is demonstrably insufficient.
18. Every material output must be traceable to its inputs and calculation path.

---

# 67. Final Product Definition

Participate With Your Numbers means:

> The investor can change their own financial assumptions and see, through the same canonical Planvesto engines, exactly how those changes affect goal funding, feasibility, constraints, strategy execution and trade-offs—without changing the underlying Financial State and without allowing the frontend to become the source of financial truth.

Canonical flow:

    BASELINE
       ↓
    INVESTOR OVERRIDE
       ↓
    EFFECTIVE SCENARIO
       ↓
    RECALCULATION
       ↓
    CONSTRAINT RE-EVALUATION
       ↓
    COMPARISON
       ↓
    TRADE-OFFS
       ↓
    INVESTOR DECISION
       ↓
    REPORT

**Next engineering milestone:** Phase 0 → Phase 1, starting with the canonical Participate contract and a stateless Participate Engine.
