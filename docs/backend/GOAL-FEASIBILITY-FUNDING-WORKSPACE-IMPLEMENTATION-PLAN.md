# Planvesto — Goal Feasibility → Funding Decision Workspace
## Complete Process & Implementation Plan

Repository: Bhardwaj1-star/planvesto
Target branch: main
Scope: Goal Feasibility, missing-data resolution, funding-strategy evaluation, investor decision, and Strategy Builder handoff.
Backend authority: canonical backend/domain engines.
Database constraint: no Supabase schema change and no SQL migration for this implementation.

---

# 1. Purpose

This document is the implementation contract for the complete Goal Feasibility → Funding Decision workflow.

Target flow:

Goal Created
→ Goal Feasibility
→ Can feasibility be calculated?
→ YES: evaluate funding alternatives
→ compare alternatives
→ investor decision
→ Strategy Builder

or:

Goal Created
→ UNKNOWN
→ identify only missing information
→ collect missing data through the existing Financial State/onboarding workflow
→ refresh Financial State
→ recalculate Goal Feasibility
→ generate/evaluate funding alternatives
→ compare
→ investor decision
→ Strategy Builder

The feature answers two distinct questions:
1. Can this goal be funded from the investor's current/projected resources?
2. Which applicable funding architecture can be evaluated, and what are its consequences?

These questions must not be collapsed into one calculation.

---

# 2. Product Principles

Goal Feasibility is a first-class planning state, not merely a report field.

Canonical sequence:

Financial Data → Financial State → Goal → Goal Feasibility → Funding Strategy Evaluation → Strategy Feasibility/Constraints → Investor Decision → Strategy Builder

Backend is the source of truth.

Frontend may collect inputs, submit supported parameters, navigate workflows, and render backend results. It must not calculate financial outcomes, create funding rules, define constraints, or silently change Financial State.

---

# 3. Current Implementation Status

Already implemented:

- Canonical Goal Feasibility in backend/services/goal_service.py.
- DefinedGoal feasibility fields in backend/models/defined_goal.py.
- Workflow readiness and missing-data metadata.
- Financial State refresh/recalculation path.
- Dedicated route: /investor/goal-planner/[goalId]/feasibility.
- GoalFeasibility component with Unknown → workspace navigation.
- Canonical funding strategy generation in backend/engines/goal/funding_strategies.py.
- Funding architectures including SIP, lump sum, lump sum + SIP, step-up SIP, lump sum + step-up SIP, and existing-assets coverage where applicable.
- Strategy-level funding result data including requirements, gap, status, constraints and trade-offs.
- Backend and frontend tests for the existing feasibility workflow.

Latest substantive workspace commit inspected:
bda8f4ef — Add goal feasibility funding workspace.

Latest repository commit inspected:
39f705bb — Update feasibility and funding workflow.

That latest commit changed only frontend/tsconfig.tsbuildinfo relative to the preceding substantive commit. It did not complete the remaining interactive funding-decision capabilities.

---

# 4. Remaining Product Gaps

1. Interactive Funding Strategy Workspace
   The current page mainly displays/evaluates backend-generated strategies. It must allow supported funding parameters to be changed and recalculated through the backend.

2. Funding Alternative Comparison
   Multiple applicable architectures need a clear comparison surface based on canonical backend results.

3. Investor Funding Decision
   The investor must explicitly select a funding architecture where the existing architecture supports persistence/selection.

4. Recommendation vs Selection
   System evaluation/recommendation and investor choice must remain separate facts.

5. Strategy Builder Handoff
   The selected funding architecture and relevant goal context must reach Strategy Builder through the canonical application layer.

---

# 5. Domain Definitions

## Goal Feasibility
Determines whether the defined goal can be funded under current/projected resources.

Possible states:
- feasible
- constrained
- infeasible
- unknown

## Strategy Feasibility
Determines whether a particular funding/strategy architecture is viable under the investor's state and constraints.

Goal Feasibility and Strategy Feasibility are distinct.

## Unknown
Unknown means the system lacks authoritative information required for calculation. It is an actionable workflow state, not a failure or an infeasibility decision.

---

# 6. Unknown / Missing-Data Workflow

When Goal Feasibility is Unknown:

1. Investor clicks Unknown.
2. Feasibility & Funding workspace opens.
3. Backend workflow readiness identifies missing data.
4. Workspace shows only missing prerequisites.
5. Investor is routed to the existing Financial State/onboarding flow.
6. returnTo preserves the feasibility workspace.
7. Financial State is refreshed.
8. Goal Feasibility is recalculated.
9. Funding strategies are regenerated/evaluated.
10. Results are shown in the same workspace.

Existing information must never be requested again.

Example: if income exists but expenses are missing, ask for expenses only.

Do not create a second financial-data collection system.

---

# 7. Financial State Refresh Contract

After missing information is completed:

Planning Unit → canonical Financial State build/refresh → latest snapshot → Defined Goal → Goal Feasibility → funding strategy generation/evaluation.

The frontend must never calculate investable surplus itself.

---

# 8. Funding Strategy Layer

Canonical owner:
backend/engines/goal/funding_strategies.py

Current strategy coverage includes:
- SIP
- Lump Sum
- Lump Sum + SIP
- Step-Up SIP
- Lump Sum + Step-Up SIP
- Existing Assets coverage where applicable.

The final strategy set must remain backend-controlled by applicability/business rules.

Frontend must not hardcode business strategy definitions.

---

# 9. Funding Strategy Evaluation Contract

Each evaluated strategy should expose, where applicable:

- strategy identity
- description
- supported parameters
- required upfront funding
- required monthly funding
- annual step-up
- available resources
- available monthly surplus
- remaining funding gap
- feasibility/status
- constraints
- trade-offs
- calculation reason/evidence
- provenance.

Canonical execution:

Funding Strategy → validate parameters → calculate funding → calculate gap → evaluate constraints → determine strategy feasibility → generate trade-offs → return canonical result.

---

# 10. Interactive Funding Workspace

The remaining workspace should let an investor:

- inspect applicable funding architectures
- select an architecture for evaluation
- modify supported parameters
- explicitly recalculate
- see updated funding requirements
- see funding gap changes
- see feasibility changes
- see constraint changes
- see trade-offs
- compare alternatives.

Only parameters supported by the canonical backend/domain contract may be exposed.

Frontend must not contain formulas such as future-value, PMT, surplus thresholds, or feasibility rules.

---

# 11. Scenario vs Financial State

If an investor tests a monthly contribution of ₹40,000, that initially means:

Evaluate a scenario using ₹40,000.

It must not silently mean:

Change the investor's permanent Financial State to ₹40,000.

Scenario testing must preserve baseline state. Actual Financial State changes belong to the Financial State workflow.

---

# 12. Baseline vs Investor Scenario

Every interactive evaluation should conceptually preserve two states:

Baseline: system-generated result using canonical current inputs.
Investor Scenario: derived result using explicit investor overrides.

Baseline must not be overwritten.

Comparison should expose changes in:
- contribution
- upfront funding
- target/date where applicable
- funding gap
- feasibility
- constraints
- trade-offs.

---

# 13. System Recommendation vs Investor Decision

Mandatory distinction:

System recommendation ≠ Investor selection.

The system may evaluate or recommend one architecture. The investor may choose another valid architecture.

The backend must never silently convert recommendation into selection.

Investor selection must use the existing canonical strategy-selection/decision mechanism, extended only if necessary.

Do not store the final decision only in React state.

---

# 14. Strategy Builder Handoff

Target sequence:

Goal → Goal Feasibility → Selected Funding Architecture → Strategy Builder.

Handoff should preserve:
- planning unit
- goal ID
- selected funding architecture
- supported funding parameters
- relevant feasibility evidence
- relevant constraints.

Strategy Builder must consume this context rather than recreate Goal Feasibility independently.

---

# 15. Canonical Responsibility Map

| Responsibility | Canonical owner |
|---|---|
| Financial State | FinancialStateEngine / existing Financial State service |
| Goal definition | DefinedGoal / Goal domain |
| Goal calculation | Goal calculation layer |
| Goal feasibility | GoalService + canonical goal/funding outputs |
| Funding architecture generation | backend/engines/goal/funding_strategies.py |
| Constraints | RuleEngine / ConstraintAggregator |
| Strategy applicability | Strategy Engine |
| Strategy evaluation | canonical Strategy/Funding evaluation |
| Investor selection | existing canonical selection/decision mechanism |
| Workflow readiness | orchestration/workflow models |
| Frontend presentation | Feasibility & Funding workspace |

If a canonical owner already exists, extend it. Do not create a parallel engine/service.

---

# 16. Implementation Plan

## Phase 0 — Audit

Inspect:
- backend/services/goal_service.py
- backend/engines/goal/
- backend/engines/goal/funding_strategies.py
- backend/models/defined_goal.py
- backend/services/strategy_service.py
- backend/engines/strategy/
- backend/api/
- backend/models/orchestration.py
- existing strategy-selection APIs
- StrategyRun and decision persistence
- frontend feasibility workspace
- frontend goal API types.

Deliverable: authority map identifying existing capability, canonical owner, reusable API, missing capability, and duplicate risk.

Exit criterion: no implementation begins until ownership is clear.

## Phase 1 — Stabilize Feasibility

Verify:
- Financial State prerequisite detection
- missing-data calculation
- Financial State refresh
- latest snapshot lookup
- feasible/constrained/infeasible/unknown states
- returnTo
- workflow readiness.

Exit criterion: valid required Financial State cannot leave feasibility Unknown.

## Phase 2 — Canonical Funding Contract

Formalize the existing funding-strategy output without creating duplicate models.

Ensure every displayed strategy has a consistent backend contract for identity, parameters, funding requirements, gap, status, constraints, trade-offs and evidence.

Exit criterion: one backend authority generates all funding strategy results.

## Phase 3 — Interactive Funding Evaluation

Implement the missing backend/application capability for investor-modified funding parameters.

Flow:
Frontend parameters → backend validation → canonical funding calculation → Goal Feasibility → constraint evaluation → trade-offs → canonical response.

Do not mutate baseline or Financial State.

Exit criterion: changing a supported parameter changes the backend result and the UI renders that result.

## Phase 4 — Comparison

Allow multiple applicable funding alternatives to be compared using backend results.

Compare at minimum:
- upfront funding
- monthly funding
- funding gap
- feasibility
- constraints
- trade-offs.

Exit criterion: investor can understand alternative funding architectures without leaving the workspace.

## Phase 5 — Investor Selection

Add explicit selection using the canonical backend decision/selection mechanism.

Preserve:
- system evaluation/recommendation
- investor selection
- selection timestamp/context where existing infrastructure supports it.

Exit criterion: selection is authoritative backend state, not frontend-only state.

## Phase 6 — Strategy Builder Handoff

Pass selected funding architecture and goal context into Strategy Builder.

Exit criterion: Strategy Builder opens with the correct canonical funding context and does not duplicate feasibility logic.

## Phase 7 — End-to-End QA

Verify both paths:

Path A:
Goal → Feasibility → Funding Options → Parameter Change → Evaluate → Compare → Select → Strategy Builder.

Path B:
Goal → Unknown → Missing Data → Financial State → Return → Recalculate → Funding Options → Evaluate → Select → Strategy Builder.

Also verify a no-viable-strategy path where alternatives are constrained/infeasible and no automatic selection occurs.

---

# 17. API/Application Requirements

Before creating endpoints, inspect existing Goal APIs and selection APIs.

Required capabilities are conceptually:

1. Read current Goal Feasibility.
2. Evaluate a funding architecture with supported parameters.
3. Select a funding architecture.

Only create new endpoints where the existing API does not already provide the capability.

Potential conceptual route for evaluation:
POST /api/goal/{goalId}/feasibility/funding/evaluate

Potential conceptual route for selection:
POST /api/goal/{goalId}/feasibility/funding/select

These are implementation candidates, not mandatory routes. Reuse existing canonical APIs if equivalent functionality already exists.

---

# 18. No Database Changes

Non-negotiable for this implementation:

- no new Supabase table
- no new column
- no SQL migration
- no new RLS migration.

Reuse existing persistence/decision infrastructure where possible.

---

# 19. Validation Rules

Backend must distinguish:

Invalid input: structurally invalid parameter.
Infeasible strategy: valid inputs but goal cannot be funded through that architecture.
Constraint violation: valid inputs conflict with an applicable financial constraint.
Unknown: authoritative prerequisite information is unavailable.

Do not collapse these states.

---

# 20. Security

Every evaluation/selection request must verify:

1. authenticated user
2. planning-unit ownership
3. goal ownership/relationship
4. relevant strategy context
5. requested funding architecture validity.

Never trust frontend-supplied ownership or authorization.

---

# 21. UI Target

The final Feasibility & Funding workspace should contain:

A. Goal Summary
- target
- date
- required corpus
- mapped resources
- funding gap.

B. Missing Information
- only when blocked
- exact missing data
- reason
- action
- returnTo.

C. Goal Feasibility
- status
- explanation
- evidence.

D. Funding Strategy Options
- applicable architectures.

E. Strategy Parameters
- only supported investor controls.

F. Evaluate / Recalculate
- explicit backend evaluation.

G. Strategy Results
- funding requirements
- gap
- feasibility
- constraints
- trade-offs.

H. Comparison
- alternative strategies side by side.

I. System Evaluation
- recommendation/evidence if applicable.

J. Investor Decision
- explicit selection.

K. Continue
- Strategy Builder.

Unrelated Planvesto screens must not be redesigned.

---

# 22. Test Plan

## Backend

Feasibility:
- missing snapshot
- missing income
- missing expenses
- Financial State refresh
- feasible
- constrained
- infeasible.

Funding:
- SIP
- lump sum
- lump sum + SIP
- step-up SIP
- lump sum + step-up SIP
- existing assets.

Interactive parameters:
- contribution change
- lump-sum change
- step-up change
- target change
- date change
- invalid input
- unsupported parameter.

Comparison:
- baseline vs investor scenario
- funding-gap delta
- feasibility delta
- constraint delta
- trade-off output.

Decision:
- recommendation exists
- recommendation and investor selection can differ
- selection reaches canonical backend state.

Handoff:
- selected funding architecture reaches Strategy Builder
- correct goal/planning-unit context
- no duplicate feasibility calculation.

## Frontend

Test:
- Unknown workspace navigation
- missing-data rendering
- returnTo
- refresh result
- supported parameter controls
- evaluation request
- result rendering
- comparison
- recommendation does not auto-select
- explicit selection
- Strategy Builder handoff.

## Architectural regression tests

Guard against:
- financial calculations in React
- duplicate feasibility logic
- duplicate funding strategy definitions
- frontend-created constraints
- recommendation becoming selection
- baseline mutation
- scenario mutation of Financial State
- report-level business logic
- Strategy Builder duplicating Goal Feasibility.

---

# 23. Documentation Requirements

After implementation, update the canonical architecture documents where the new behavior changes system ownership or flow.

At minimum review:
- backend/PLANNING_SYSTEM_FLOW.md
- docs/domain-ontology/CANONICAL_DOMAIN_MODEL.md.

This document remains the feature-specific implementation contract.

---

# 24. Definition of Done

Goal Feasibility:
- [ ] prerequisites are canonical
- [ ] Unknown is actionable
- [ ] only missing data is requested
- [ ] Financial State refresh works
- [ ] feasibility recalculates after refresh.

Funding:
- [ ] applicable strategies are generated canonically
- [ ] supported parameters are editable
- [ ] backend evaluates changed parameters
- [ ] results include funding requirement, gap, status, constraints and trade-offs
- [ ] alternatives can be compared.

Decision:
- [ ] recommendation and investor decision are separate
- [ ] investor can explicitly select a funding architecture
- [ ] selection uses canonical backend state/mechanism.

Handoff:
- [ ] selected funding architecture reaches Strategy Builder
- [ ] goal context is preserved
- [ ] no duplicate feasibility calculation exists.

Architecture:
- [ ] no frontend financial business logic
- [ ] no duplicate funding engine
- [ ] no duplicate feasibility engine
- [ ] no unnecessary new abstraction
- [ ] no Supabase schema change
- [ ] no SQL migration
- [ ] no unrelated frontend redesign.

QA:
- [ ] backend tests pass
- [ ] frontend tests pass
- [ ] type checks pass
- [ ] end-to-end workflow verified
- [ ] canonical ownership audit passes.

---

# 25. Final Target Architecture

Financial Data
→ Financial State
→ Goal
→ Goal Feasibility
→ Funding Alternatives
→ Strategy Evaluation
→ Comparison
→ System Evaluation/Recommendation
→ Investor Decision
→ Selected Funding Architecture
→ Strategy Builder
→ Strategy Decision
→ Action Plan

Unknown path:
Goal Feasibility = Unknown
→ Missing Data
→ Existing Financial State workflow
→ Financial State refresh
→ Feasibility recalculation
→ Funding Evaluation.

Critical boundary:

Goal Feasibility determines whether/how the goal can be funded under available resources.

Strategy Builder determines the broader financial strategy architecture.

Neither layer should absorb the other's responsibility.

---

# 26. Non-Negotiable Engineering Rules

1. Backend remains the source of truth.
2. Goal Feasibility remains distinct from Strategy Feasibility.
3. Unknown is an actionable workflow state.
4. Missing information is collected incrementally.
5. Existing information is reused.
6. Funding strategies are generated by canonical backend logic.
7. Frontend never performs financial business calculations.
8. Scenario inputs do not silently mutate Financial State.
9. Baseline remains immutable during scenario evaluation.
10. System recommendation and investor decision remain separate.
11. Investor decision is explicit.
12. Strategy Builder consumes canonical funding context.
13. No duplicate engines/services for existing business logic.
14. No invented business rules.
15. No Supabase schema changes or migrations for this implementation.
16. Reports remain presentation layers over canonical outputs.
17. Unresolved business ambiguity must be documented rather than guessed.

---

# 27. Completion Standard

The current repository has the foundation: Goal Feasibility, workflow readiness, missing-data routing, Financial State refresh, canonical funding-strategy generation, and a dedicated Feasibility & Funding workspace.

The remaining work is to turn that read/evaluate surface into a complete interactive decision workflow:

Missing Data → Financial State → Goal Feasibility → Funding Evaluation → Comparison → Investor Selection → Strategy Builder.

Completion must be demonstrated by actual backend/frontend code, tests, and end-to-end verification. A visually complete page alone is not sufficient.