# PlanVesto — Canonical Decision Engine

**Document Type:** Product & Architecture Decision Specification  
**Status:** Proposed target architecture; code-verified current state  
**Scope:** PlanVesto decision-making system  
**Repository:** `Bhardwaj1-star/planvesto`  
**Source of truth for current-state assessment:** Backend code only

---

## 1. Executive Summary

PlanVesto already contains many decision rules, canonical registries, strategy definitions, constraints, eligibility checks, ranking logic, variant selection, technique execution, and scenario generation.

The current issue is not the absence of decision logic. The issue is **fragmented decision authority**.

The intended direction is therefore:

> **Build a Canonical Decision Engine for PlanVesto, with Strategy Decisioning as one domain inside it.**

The Decision Engine should centralize the **decision contract and business-rule authority**, while domain modules remain separated.

It must **not** become one monolithic engine containing every rule.

### Target principle

```text
Canonical Decision Framework
        │
        ├── Goal Decisioning
        ├── Financial / Constraint Decisioning
        ├── Eligibility Decisioning
        ├── Strategy Decisioning
        ├── Variant Decisioning
        ├── Technique Decisioning
        ├── Architecture Decisioning
        ├── Stress / Resilience Decisioning
        └── Recommendation Decisioning
```

The existing Strategy Builder becomes a major consumer/domain of this framework rather than the architectural boundary of decision-making.

---

## 2. Product Objective

The Decision Engine should answer, consistently and explainably:

> **Given the investor's goals, financial state, risk capacity, constraints, priorities and available resources, what decision is valid, why is it valid, what alternatives exist, and how resilient is that decision under stress?**

The engine must provide:

1. **Deterministic decision authority**
2. **One canonical owner for each business rule**
3. **Explicit decision stages**
4. **PASS / CONDITIONAL / FAIL semantics where applicable**
5. **Traceable evidence and rationale**
6. **Clear separation between hard constraints and decision preferences**
7. **Stable strategy and variant selection**
8. **Stress/resilience evaluation**
9. **No contradictory downstream re-decision**
10. **Testable decision contracts**

---

# 3. Current System — Code-Verified

## 3.1 What already exists

The repository already has meaningful canonical infrastructure.

### Goal taxonomy

`backend/rules/goals.py` is an authoritative goal taxonomy.

It defines:

- canonical goal types,
- canonical goal names,
- priority vocabulary,
- priority aliases,
- essential/discretionary classification,
- canonicalization functions.

This is already close to the desired model.

### Canonical rule registry

`backend/rules/canonical.py` already defines:

- canonical rule IDs,
- rule scope,
- rule role,
- source module,
- descriptions,
- rule-set version,
- registry validation.

Current roles include:

- hard constraint,
- eligibility,
- ranking input,
- recommendation only,
- architecture constraint,
- explanatory evidence,
- classification,
- transformation.

This is an important foundation for the Decision Engine.

**Current limitation:** the registry mostly provides metadata/identity. It does not yet make all referenced business behavior canonical and executable from one rule authority.

---

## 3.2 Canonical strategies already exist

The current strategy library contains **5 canonical strategies**:

1. `strat-goal-funding`
2. `strat-progressive-de-risking`
3. `strat-capital-preservation`
4. `strat-debt-reduction`
5. `strat-credit-utilisation`

These definitions live under:

`backend/library/strategies/canonical.py`

They contain metadata such as:

- applicable goal types,
- applicable characteristics,
- constraints,
- required inputs,
- techniques,
- levers/components,
- scoring-related metadata.

The strategy definitions themselves should remain canonical library objects.

---

## 3.3 22 active variants already exist

`backend/library/strategies/variants.py` contains the canonical active strategy variants.

The current system count is **22 active variants**:

### Goal Funding — 6

- `existing_assets`
- `sip`
- `lumpsum`
- `lumpsum_plus_sip`
- `lumpsum_plus_step_up_sip`
- `step_up_sip`

### Progressive De-risking — 4

- `goal_date_glide_path`
- `payment_tranche_glide_path`
- `recurring_cashflow_glide_path`
- `income_transition_glide_path`

### Capital Preservation — 4

- `full_goal_preservation`
- `first_payment_preservation`
- `rolling_reserve_preservation`
- `protected_core_preservation`

### Debt Reduction — 4

- `goal_gap_debt_reduction`
- `emi_relief_debt_reduction`
- `residual_gap_debt_reduction`
- `goal_linked_debt_reduction`

### Credit Utilisation — 4

- `residual_gap_bridge`
- `partial_goal_financing`
- `emi_cap_financing`
- `timing_bridge_financing`

The variant registry is canonical for **definition**, but not yet for the complete **selection policy**.

---

# 4. The Core Gap: Definition vs Decision Authority

The current system has two different concepts that are not yet consistently separated:

### Canonical definition

Example:

> This strategy/variant exists, has this ID, name, purpose, inputs and applicability metadata.

### Executable decision rule

Example:

> When EMI/income >= 40%, select `emi_relief_debt_reduction`.

The first is already largely centralized.

The second is still distributed through engine code.

This distinction is the central architectural problem.

---

# 5. Current vs Target Decision Ownership

| Decision Area | Current Code | Current State | Target |
|---|---|---|---|
| Goal normalization | `rules/goals.py` | Centralized | Keep |
| Goal classification | `rules/goals.py` | Centralized | Keep |
| Rule identity | `rules/canonical.py` | Central metadata registry | Expand as authority |
| Hard constraints | `engines/constraints/` | Relatively centralized | Formalize as canonical domain |
| Strategy definitions | `library/strategies/canonical.py` | Canonical | Keep |
| Variant definitions | `library/strategies/variants.py` | Canonical | Keep |
| Strategy applicability | `engines/rules/engine.py` | Engine-owned executable logic | Move policy to canonical rules |
| Eligibility vocabulary | `rules/eligibility.py` | Centralized | Keep/expand |
| Eligibility behavior | `engines/strategy/eligibility.py` | Engine-owned | Move rule policy to canonical layer |
| Strategy selection | `engines/strategy/decision.py` + `rules/strategy_decision.py` | Split authority | One canonical selection policy |
| Scoring | `rules/strategy_decision.py` | Intended canonical policy but contains stale strategy IDs | Replace/freeze |
| Variant selection | `engines/strategy/variant_selector.py` | Hardcoded executable rules | Move policy to canonical layer |
| Technique selection | Strategy metadata + engine flow | Partially centralized | Define explicit authority |
| Architecture activation | `library/strategies/components.py` + composition engine | Metadata exists; semantics distributed | Canonicalize decision policy |
| Scenarios | `engines/strategy/scenario.py` | Execution/calculation | Keep as calculation layer |
| What-if | `engines/strategy/scenario.py` | Exploratory sensitivity | Separate from canonical stress decisioning |
| Stress testing | No verified single canonical policy | Fragmented/limited | Define canonical resilience policy |
| Recommendation | `engines/strategy/recommendation.py` | Consumes DecisionResult | Keep downstream of Decision Engine |
| Ranking | `engines/strategy/ranking.py` | Says DecisionResult is authoritative | Keep as presentation/evidence layer after freeze |

---

# 6. Important Current-Code Mismatches

## 6.1 Strategy selection is not fully canonical

`backend/engines/strategy/decision.py` is currently described as the authoritative Strategy Builder decision layer.

It performs:

- eligibility evaluation,
- architecture evaluation,
- goal fit scoring,
- horizon fit scoring,
- funding fit scoring,
- feasibility scoring,
- component fit scoring,
- technique execution scoring,
- final decision scoring,
- PASS-over-CONDITIONAL pooling,
- final architecture selection.

This is actual business decision logic.

### Target

The engine should orchestrate a canonical selection policy rather than own the policy itself.

---

## 6.2 `rules/strategy_decision.py` is currently unsafe as a canonical authority

The file is explicitly named as an authoritative Strategy Builder decision/scoring policy module.

However, its scoring logic references stale strategy IDs such as:

- `strat-dynamic-accumulation`
- `strat-calibrated-growth`
- `strat-high-liquidity-flex`
- `strat-cap-preservation`

These do not match the current canonical five-strategy registry.

Therefore:

> **This file must not be treated as the final canonical strategy-selection contract in its current form.**

It should be replaced/reconciled as part of the canonicalization phase.

---

## 6.3 Strategy applicability is split

`backend/engines/rules/engine.py` implements applicability signals directly:

- shortfall,
- on_track,
- overfunded,
- near_term,
- long_term,
- fixed_timeline,
- flexible_timeline,
- high_priority.

Current horizon boundaries include:

- near-term: `duration <= 5`
- long-term: `duration >= 7`

These semantics currently live in executable engine code rather than a dedicated canonical applicability policy.

### Target

The definitions and thresholds must be explicitly owned by the canonical Decision Engine rule layer.

---

# 7. Eligibility — Current State

The system already defines 8 canonical eligibility fits:

1. `cashflow_fit`
2. `liquidity_fit`
3. `debt_fit`
4. `asset_resource_fit`
5. `risk_capacity_fit`
6. `goal_constraint_fit`
7. `multi_goal_conflict_fit`
8. `implementation_fit`

`backend/rules/eligibility.py` owns the vocabulary.

`backend/engines/strategy/eligibility.py` owns the actual evaluation behavior.

Current evaluation includes examples such as:

- required contribution <= available surplus → PASS
- required contribution > available surplus → CONDITIONAL
- surplus <= 0 → FAIL
- liquid assets >= required liquidity → PASS
- liquidity shortfall → CONDITIONAL
- risk requirement <= capacity → PASS
- risk requirement above capacity but de-risked implementation possible → CONDITIONAL
- risk requirement above capacity without acceptable de-risking → FAIL
- higher-priority goal materially compromised → FAIL
- implementation evidence unavailable → CONDITIONAL.

### Target

The **fit definitions, thresholds, precedence and missing-data semantics** should become canonical decision policy.

The engine should evaluate that policy.

---

# 8. Hard Constraints Must Remain Separate

The existing architecture already distinguishes hard constraints from softer diagnostics and recommendation evidence.

`backend/engines/rules/engine.py` uses explicit decision roles.

The constraints package also has a dedicated evaluator and policy layer.

This separation should be preserved.

### Decision Engine principle

```text
Hard Constraint
      ↓
Can decision proceed?
      ↓
Eligibility
      ↓
Which valid option is better?
      ↓
Ranking / Selection
      ↓
Recommendation
```

A ranking score must never silently override a failed hard constraint.

---

# 9. Strategy Selection — Proposed Canonical Contract

Strategy selection should become a formal Decision Engine stage.

### Inputs

- canonical goal
- goal characteristics
- financial state
- investor priorities
- hard constraints
- eligibility results
- applicable strategies
- strategy metadata
- scenario evidence
- architecture evidence

### Selection sequence

```text
1. Remove hard-constraint failures
2. Evaluate all eligibility fits
3. Classify each strategy:
      PASS / CONDITIONAL / FAIL
4. Prefer PASS pool
5. If no PASS, evaluate CONDITIONAL pool
6. Apply canonical selection score/policy
7. Apply deterministic tie-breakers
8. Select primary strategy
9. Preserve ordered alternatives
10. Produce decision evidence + rationale
```

The exact scoring weights and tie-breakers remain **TO DECIDE** before refactoring.

---

# 10. Variant Selection — Current vs Target

Current variant selection is executable code in:

`backend/engines/strategy/variant_selector.py`

It is deterministic and already covers all five strategies.

Examples:

### Goal Funding

- baseline funding strategy if available;
- mapped assets >= future target → `existing_assets`;
- no surplus + positive gap → `lumpsum`;
- otherwise → `step_up_sip`.

### Progressive De-risking

- retirement/FIRE → income transition;
- education/tranches → payment tranche;
- vacation/multiple trips → recurring cash-flow;
- otherwise → goal-date glide path.

### Capital Preservation

- vacation/repeat → rolling reserve;
- education/years → first payment;
- positive surplus + target → protected core;
- otherwise → full goal preservation.

### Debt Reduction

- debt freedom/linked liability → goal-linked debt reduction;
- EMI/income >= 40% → EMI relief;
- no surplus → residual gap;
- otherwise → goal gap.

### Credit Utilisation

- timing bridge or <=1 year → timing bridge;
- EMI/income >= 30% → EMI cap;
- education/dream home → partial financing;
- otherwise → residual gap bridge.

### Target

The 22 variant definitions remain in the strategy library.

The **selection conditions become canonical Decision Engine policy**.

The selector becomes an execution adapter.

---

# 11. Technique and Architecture

The repository already has canonical technique definitions and a canonical strategy solution matrix.

The solution matrix establishes:

> Strategy = responsibility / architecture  
> Solution = concrete implementation path.

It also reuses canonical strategy, variant and technique IDs.

The component registry also contains canonical activation metadata, including rules based on:

- funding status,
- duration,
- priority,
- liabilities,
- liquidity,
- surplus,
- funding gap.

### Current gap

The metadata is centralized, but the exact relationship between:

```text
Strategy
→ Variant
→ Technique
→ Component
→ Architecture
```

is not yet defined as one canonical decision contract.

### Target

Architecture composition should consume already-made canonical decisions instead of independently inventing strategy/business logic.

---

# 12. Stress Testing vs What-if

The current code has `generate_what_if_scenarios()`.

It generates exploratory sensitivity cases including:

- contribution increases,
- longer goal horizon,
- target reductions,
- contribution step-ups.

There is also an elevated-inflation baseline scenario.

These are useful, but they should not automatically be considered a complete canonical stress-testing framework.

### Target distinction

**What-if**

> “What happens if the investor changes X?”

**Stress test**

> “Does the recommended decision remain valid under adverse conditions?”

The Decision Engine should eventually define canonical stress scenarios and resilience semantics.

Potential structure:

```text
Base Decision
    ↓
Canonical Stress Set
    ↓
Re-evaluate constraints
    ↓
Re-evaluate eligibility
    ↓
Re-evaluate strategy/variant stability
    ↓
Measure outcome deterioration
    ↓
Resilience classification
```

The exact stress shocks and re-selection authority remain **TO DECIDE**.

---

# 13. Proposed Decision Engine Architecture

## 13.1 Conceptual architecture

```text
                    PLANVESTO DECISION ENGINE
                              │
                    ┌─────────┴─────────┐
                    │ Decision Context  │
                    └─────────┬─────────┘
                              │
              ┌───────────────┴────────────────┐
              │                                │
       Canonical Rules                    Canonical Library
              │                                │
       ┌──────┼────────┐                ┌──────┼──────┐
       │      │        │                │      │      │
     Goals Constraints Eligibility   Strategies Variants Techniques
       │      │        │
       └──────┴────────┘
                  │
            Decision Pipeline
                  │
       ┌──────────┼───────────┐
       │          │           │
   Applicability Eligibility Selection
                              │
                         Variant
                              │
                         Technique
                              │
                        Architecture
                              │
                       Stress/Resilience
                              │
                       Recommendation
```

---

# 14. Proposed Canonical Rule Domains

The target rule layer should evolve toward clearly separated domains.

```text
backend/rules/
├── canonical.py
├── goals.py
├── eligibility.py
├── strategy_applicability.py
├── strategy_eligibility.py
├── strategy_selection.py
├── strategy_variants.py
├── strategy_techniques.py
├── strategy_architecture.py
└── strategy_stress.py
```

These names are a proposed target structure.

The exact file split should be decided during implementation based on existing module boundaries; the architectural principle is more important than the filenames.

---

# 15. Decision Engine vs Library vs Engine

This separation should be explicit.

## Canonical Rules

Define:

> **What business rule is true?**

Examples:

- eligibility thresholds,
- applicability conditions,
- selection precedence,
- variant conditions,
- stress criteria.

## Canonical Library

Defines:

> **What options exist?**

Examples:

- 5 strategies,
- 22 variants,
- techniques,
- components,
- solution definitions.

## Execution Engines

Define:

> **How do we calculate/evaluate/execute the rule?**

Examples:

- financial calculations,
- scenario calculations,
- technique calculations,
- data transformation,
- orchestration.

## Decision Result

Defines:

> **What did the system decide and why?**

This becomes the authoritative output consumed downstream.

---

# 16. Target Decision Pipeline

The final decision pipeline should be:

```text
Input Context
    ↓
Normalize / Canonicalize
    ↓
Goal Classification
    ↓
Financial State / Constraint Evaluation
    ↓
Hard Constraint Gate
    ↓
Strategy Applicability
    ↓
Eligibility — 8 Fits
    ↓
PASS / CONDITIONAL / FAIL
    ↓
Strategy Selection
    ↓
Variant Selection
    ↓
Technique Selection
    ↓
Architecture Composition
    ↓
Stress / Resilience
    ↓
Re-selection if canonical policy permits
    ↓
Final Decision
    ↓
Recommendation / Explanation / Report
```

The important principle is:

> **Downstream layers should not independently re-decide an upstream business decision.**

---

# 17. What Must Be Decided Before Refactoring

## Decision A — Applicability

Freeze:

- goal characteristic vocabulary,
- horizon thresholds,
- funding-state semantics,
- priority semantics,
- fixed/flexible timeline semantics,
- applicability precedence.

## Decision B — Hard Constraints

Freeze:

- true hard gates,
- conflict policy,
- missing-data behavior,
- override policy.

## Decision C — Eligibility

Freeze for all 8 fits:

- definition,
- PASS criteria,
- CONDITIONAL criteria,
- FAIL criteria,
- thresholds,
- missing-data behavior,
- precedence.

## Decision D — Strategy Selection

Freeze:

- eligibility gate,
- PASS vs CONDITIONAL precedence,
- scoring dimensions,
- weights,
- tie-breakers,
- feasibility role,
- alternative strategy ordering.

## Decision E — Variant Selection

Freeze:

- every one of the 22 variant conditions,
- precedence,
- fallback,
- missing-data behavior,
- exclusivity.

## Decision F — Techniques

Freeze:

- strategy-to-technique relationship,
- technique selection conditions,
- mandatory vs optional techniques,
- execution readiness semantics.

## Decision G — Architecture

Freeze:

- component activation,
- component dependencies,
- architecture validity,
- resource-conflict handling.

## Decision H — Stress / Resilience

Freeze:

- stress set,
- shock sizes,
- correlated shocks,
- evaluation metrics,
- resilience labels,
- re-selection rules.

---

# 18. Refactor Sequence

Refactoring should be behavior-controlled and staged.

### Phase 1 — Decision Contract

Freeze the canonical Decision Engine contract.

### Phase 2 — Rule Inventory

For every existing rule classify it:

- KEEP
- MOVE
- MERGE
- REPLACE
- REMOVE
- NEW

### Phase 3 — Canonicalization

Move business-rule authority into canonical rule modules.

Do not change business behavior unless explicitly decided.

### Phase 4 — Engine Adaptation

Change engines to consume canonical policies.

Engines should calculate and orchestrate.

### Phase 5 — Remove Conflicting Logic

Remove:

- duplicate thresholds,
- stale strategy IDs,
- duplicate selection logic,
- downstream re-decision paths.

### Phase 6 — Decision-Level Tests

Test:

- applicability,
- each eligibility fit,
- strategy selection,
- each variant,
- architecture,
- stress behavior.

### Phase 7 — End-to-End Verification

Verify the complete:

```text
Input → Decision Engine → Recommendation → Report
```

flow.

### Phase 8 — Consolidated Implementation

Changes should be delivered as one coherent implementation change rather than fragmented business-rule migrations.

---

# 19. Acceptance Criteria

The Canonical Decision Engine architecture is considered established when:

### Authority

- every business decision has one authoritative owner;
- canonical rule IDs map to real executable policy;
- no stale strategy-selection IDs remain.

### Strategy

- 5 canonical strategies remain unchanged unless explicitly decided;
- 22 active variants remain canonical;
- variant selection is deterministic and canonical.

### Eligibility

- 8 fits have one authoritative policy;
- PASS / CONDITIONAL / FAIL semantics are consistent;
- missing-data behavior is explicit.

### Constraints

- hard constraints cannot be silently overridden by ranking;
- constraint roles are explicit.

### Architecture

- technique/component/architecture relationships are deterministic;
- downstream layers do not independently contradict strategy decisions.

### Stress

- stress testing has a defined canonical policy;
- resilience results are explainable;
- re-selection behavior is explicit.

### Engineering

- engines execute/orchestrate canonical policy;
- business thresholds are not duplicated across engines;
- decision outputs contain evidence and rationale;
- tests protect the decision contract.

---

# 20. Product-Level Definition of Done

The Decision Engine is not complete merely because a central Python class exists.

It is complete when:

> **PlanVesto can make a financial decision through one explicit, deterministic, explainable and testable decision contract, regardless of which product surface invoked it.**

Strategy Builder is then one consumer of that contract, rather than the owner of the entire decision architecture.

---

# 21. Current Status

**Status: Architecture/design phase.**

No refactor should begin until the unresolved decision policies in Section 17 are explicitly frozen.

The existing repository provides a strong starting point:
- canonical goal taxonomy,
- canonical rule registry,
- canonical strategy registry,
- canonical variant registry,
- canonical solution matrix,
- canonical components,
- constraint policy,
- eligibility vocabulary,
- strategy decision flow.

The primary work is therefore **consolidation of authority, removal of conflicting/stale logic, and formalization of the Decision Engine contract**, not rebuilding the system from zero.
