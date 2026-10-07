# 00 — Canonical Decision Engine Design Summary

**Parent area:** `docs/Decision tree/`  
**Purpose:** Navigation and consolidated design summary for Steps 1–9  
**Status:** **DESIGN / AUDIT SUMMARY — RULES NOT FROZEN**

---

## 1. Purpose

This document is the **summary layer** for the nine detailed Decision Engine documents.

It does **not replace** Steps 1–9 and it is **not the final business-rule book**.

Its purpose is to give one clear view of:

- the complete Decision Engine flow;
- what each of the nine steps is responsible for;
- the current code authority identified in the detailed audits;
- the major gaps and overlaps;
- the recommended target architecture;
- what remains deliberately unfrozen;
- how the system should move from design → real-life validation → frozen Version 1 rules.

The detailed documents remain the evidence and working analysis for each step.

---

# 2. The Big Picture

The Strategy Builder should ultimately operate as **one canonical decision system**, not as a collection of independent recommendation rules.

The intended end-to-end flow is:

```text
Goal
  ↓
Goal Classification
  ↓
Hard Constraint Gate
  ↓
Strategy Applicability
  ↓
8-Fit Eligibility
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
Re-selection if required
  ↓
Final Decision
  ↓
Investor Recommendation
```

The central architectural principle is:

> **One Decision Engine, multiple input states.**

Stress scenarios should therefore re-use the same decision logic rather than create a second recommendation system.

---

# 3. The Nine Decision Domains

| Step | Decision domain | Main question | Current authority identified in audit | Target direction |
|---|---|---|---|---|
| 01 | Strategy Applicability | Which strategies may enter the candidate pool? | Strategy library + `StrategyRuleEngine` | Dedicated canonical applicability rules |
| 02 | Hard Constraints | Is the planning situation allowed to proceed? | Constraints policy/evaluator/aggregator | Complete canonical hard-constraint policy |
| 03 | 8 Eligibility Fits | Can each candidate strategy work financially? | `engines/strategy/eligibility.py` | Canonical eligibility policy + execution layer |
| 04 | Strategy Selection | Which eligible strategy wins? | `engines/strategy/decision.py::evaluate_decision()` | One canonical selection authority |
| 05 | 22 Variant Selection | Which implementation variant fits the selected strategy? | `VariantSelector` | Dedicated canonical variant rules |
| 06 | Technique Selection | Which techniques should be used? | Technique registry + TechniqueEngine + architecture | Dedicated canonical technique-selection rules |
| 07 | Architecture Composition | How are strategy, variant, techniques and components assembled? | `compose_architectures` | Downstream canonical architecture composition |
| 08 | Stress / Resilience | Does the plan remain viable under adverse conditions? | Scenario/what-if layer; incomplete stress framework | Same Decision Engine replayed under shocked inputs |
| 09 | Final Decision & Recommendation | What is the authoritative final result shown and persisted? | `DecisionResult` + Recommendation layer | One canonical final decision contract |

---

# 4. Step-by-Step Summary

## Step 1 — Strategy Applicability

### Current position

The current system has five canonical strategies:

1. Goal Funding
2. Progressive De-risking
3. Capital Preservation
4. Debt Reduction
5. Credit Utilisation

The strategy library contains goal-type and characteristic metadata, while applicability interpretation is currently executed through `StrategyRuleEngine`.

The current characteristic matching is effectively:

**Goal type matches AND ANY configured characteristic matches**

### Main gaps

- AND/OR semantics are not explicitly canonical.
- Horizon currently has a 5–7 year gap:
  - near-term ≤ 5 years
  - long-term ≥ 7 years
- Some strategies are broad because of OR semantics.
- Applicability and eligibility overlap in places.
- Missing-data behavior is not fully defined.

### Target

```text
Canonical Goal Type
  ↓
Strategy Goal-Type Gate
  ↓
Strategy Applicability Conditions
  ↓
Applicable Strategy Pool
```

Business conditions must be frozen only after real-life validation.

**Detailed document:**  
`01-STRATEGY_APPLICABILITY_CURRENT_STATE_AND_RECOMMENDATION.md`

---

## Step 2 — Hard Constraints

### Current position

The system already has a relatively strong centralized constraint foundation.

Current hard-constraint behavior includes:

- Goal Positive Horizon
- Goal Positive Target
- Critical Emergency Reserve behavior
- Critical Debt Burden / DTI behavior
- Discretionary Cannot Preempt Essential
- constraint-conflict governance

The current system also separates hard constraints from warnings and diagnostics.

### Main gaps

- Not every hard business rule has a complete first-class canonical identity in the canonical rule registry.
- Emergency reserve and DTI behaviors must not be confused with universal blocking rules.
- Financial health signals appear in several layers and need an explicit decision role.
- Missing data must not silently become a hard failure.

### Target

```text
Goal Validity
  ↓
Hard Constraint Gate
  ↓
PASS / FAIL / UNAVAILABLE
```

**Important boundary:**

> Financial health ≠ hard constraint.

**Detailed document:**  
`02-HARD_CONSTRAINTS_CURRENT_STATE_AND_RECOMMENDATION.md`

---

## Step 3 — Eight Eligibility Fits

The eight canonical fits are:

1. Cash-flow Fit
2. Liquidity Fit
3. Debt Fit
4. Asset Resource Fit
5. Risk Capacity Fit
6. Goal Constraint Fit
7. Multi-goal Conflict Fit
8. Implementation Fit

Current aggregate precedence is:

**FAIL > CONDITIONAL > PASS**

The current eligibility implementation is centralized in the strategy eligibility engine, but business-policy ownership is still engine-based rather than a dedicated canonical rule layer.

### Main gaps

- Fit vocabulary is canonical, but business conditions are not fully canonicalized.
- Some fits do not currently have symmetric PASS/CONDITIONAL/FAIL paths.
- Missing evidence generally becomes CONDITIONAL.
- Goal Constraint Fit overlaps with Applicability.
- Debt and liquidity concepts overlap with hard constraints.
- Context inputs are partly implicit.

### Target

```text
Applicable Strategy
  ↓
8 Eligibility Fits
  ↓
Aggregate Fit Status
  ↓
PASS / CONDITIONAL / FAIL
```

**Detailed document:**  
`03-8_ELIGIBILITY_FITS_CURRENT_STATE_AND_RECOMMENDATION.md`

---

## Step 4 — Strategy Selection

### Current position

The current actual runtime authority is:

`backend/engines/strategy/decision.py::evaluate_decision()`

The current principle is:

**PASS > CONDITIONAL > FAIL**

Within the selected pool, the engine uses a composite decision score involving:

- Goal Fit
- Horizon Fit
- Funding Fit
- Feasibility
- Component Fit
- Technique Execution

### Main gaps

- A stale policy module contains old strategy IDs.
- Architecture is composed before final strategy selection, creating a possible circular dependency:
  **Strategy → Architecture → Technique → Score → Strategy**
- Exact score weights and precedence are not yet frozen.
- Alternative strategy policy is not frozen.

### Target

```text
Eligible Candidate Pool
  ↓
Canonical Strategy Selection
  ↓
Primary Strategy
  ↓
Alternative(s)
```

Selection must have one authoritative owner.

**Detailed document:**  
`04-STRATEGY_SELECTION_CURRENT_STATE_AND_RECOMMENDATION.md`

---

## Step 5 — 22 Variant Selection

The system currently has **22 active canonical variants**:

| Strategy | Active variants |
|---|---:|
| Goal Funding | 6 |
| Progressive De-risking | 4 |
| Capital Preservation | 4 |
| Debt Reduction | 4 |
| Credit Utilisation | 4 |
| **Total** | **22** |

The variant definitions are centralized in the strategy library, but the executable selection conditions are in `VariantSelector`.

### Main gaps

- Selection rules are not canonicalized.
- Rule precedence is implicit.
- Some Goal Funding variants are defined but not directly reachable through current direct rules.
- Missing numeric inputs can affect rule selection.
- Variant selection currently sits inside recommendation flow.
- Reachability is not formally validated.

### Target

```text
Selected Strategy
  ↓
Variant Candidate Set
  ↓
Variant Applicability
  ↓
Variant Decision Conditions
  ↓
Deterministic Precedence
  ↓
Selected Variant
```

**Detailed document:**  
`05-22-VARIANT_SELECTION_CURRENT_STATE_AND_RECOMMENDATION.md`

---

## Step 6 — Technique Selection

There are currently **10 registered techniques**.

Eight are mapped to the current canonical strategies. Two are registered but not currently attached to a canonical strategy:

- Barbell / Dumbbell
- Tax-Loss Harvesting

### Main gaps

- Technique definitions are centralized, but selection policy is not.
- Current architecture/strategy mapping is not fully variant-specific.
- Precedence and combination rules are not frozen.
- Required/optional/conditional/mutually-exclusive behavior is not yet canonical.
- Missing-input treatment needs explicit policy.

### Target

```text
Selected Strategy
  ↓
Selected Variant
  ↓
Technique Candidate Set
  ↓
Technique Applicability
  ↓
Technique Conditions
  ↓
Selected Techniques
  ↓
Execution
```

**Detailed document:**  
`06-TECHNIQUE_SELECTION_CURRENT_STATE_AND_RECOMMENDATION.md`

---

## Step 7 — Architecture Composition

The architecture combines the selected planning elements into an executable structure.

Current architecture contains concepts such as:

- primary strategy;
- supporting strategies;
- solutions;
- techniques;
- components;
- rationale;
- trade-offs;
- feasibility;
- constraints.

Architecture identity is currently based on the stable combination of:

**Goal ID + Primary Strategy ID**

That identity should be preserved.

### Main gaps

- Architecture candidate vs final architecture is not completely separated.
- Supporting-strategy policy is embedded in composition logic.
- Technique selection is not yet variant-specific.
- Feasibility and eligibility can overlap.
- Architecture is currently composed before final strategy selection.

### Target

```text
Strategy
  ↓
Variant
  ↓
Techniques
  ↓
Architecture Composition
  ↓
Final Architecture
```

The final architecture should carry the complete selected path and its evidence.

**Detailed document:**  
`07-ARCHITECTURE_COMPOSITION_CURRENT_STATE_AND_RECOMMENDATION.md`

---

## Step 8 — Stress / Resilience

### Current position

The code currently supports:

- baseline scenario generation;
- conservative hedged scenario;
- what-if sensitivity scenarios.

However, this is **not yet a complete canonical stress/resilience decision framework**.

Missing pieces include:

- canonical stress taxonomy;
- correlated stress cases;
- formal resilience classification;
- strategy stability testing;
- formal stress-triggered re-selection;
- dedicated stress hard-constraint/eligibility replay.

### Target

```text
Base Decision
  ↓
Stress Scenario
  ↓
Same Hard Constraints
  ↓
Same 8 Fits
  ↓
Same Strategy Selection
  ↓
Same Variant Selection
  ↓
Same Architecture Composition
  ↓
Compare Results
  ↓
Resilience Classification
```

Recommended future resilience categories are:

- Robust
- Conditional
- Fragile

These are **not frozen**.

**Detailed document:**  
`08-STRESS_RESILIENCE_CURRENT_STATE_AND_RECOMMENDATION.md`

---

## Step 9 — Final Decision & Recommendation

### Current position

The current authoritative runtime decision is `DecisionResult`.

Recommendation consumes that result and adds:

- funding context;
- financial diagnostics;
- supporting-strategy explanation;
- selected variant;
- architecture;
- alternatives;
- feasibility;
- constraints.

This is directionally correct because recommendation is downstream from decision.

### Main gaps

- Variant selection currently occurs inside recommendation flow.
- Exact final decision contract is not frozen.
- Alternative policy is not frozen.
- Feasibility/resilience boundaries need clarification.
- A stale strategy-decision policy module contains old strategy IDs.
- Final investor-facing outcome labels are not frozen.

### Target

```text
Canonical Decision Result
  ↓
Final Decision
  ↓
Investor Recommendation
```

Recommendation should **explain** the decision, not silently create a new one.

**Detailed document:**  
`09-FINAL_DECISION_AND_RECOMMENDATION_CURRENT_STATE_AND_RECOMMENDATION.md`

---

# 5. The Recommended Canonical Decision Tree

The nine documents collectively point to one target sequence:

```text
1. GOAL
   ↓
2. GOAL CLASSIFICATION
   ↓
3. HARD CONSTRAINT GATE
   ↓
4. STRATEGY APPLICABILITY
   ↓
5. 8-FIT ELIGIBILITY
   ↓
6. STRATEGY SELECTION
   ↓
7. VARIANT SELECTION
   ↓
8. TECHNIQUE SELECTION
   ↓
9. ARCHITECTURE COMPOSITION
   ↓
10. STRESS / RESILIENCE
   ↓
11. RE-SELECTION IF REQUIRED
   ↓
12. FINAL DECISION
   ↓
13. INVESTOR RECOMMENDATION
```

The nine audit documents are therefore not nine independent decision systems.

They are nine documented domains of one future Decision Engine.

---

# 6. What Is Already Strong

The audits show that PlanVesto already has several useful foundations:

### 6.1 Canonical strategy library exists

There are five current canonical strategies and 22 active variants.

### 6.2 Goal taxonomy is already centralized

Goal classification and canonical goal vocabulary are already established.

### 6.3 Constraint aggregation exists

Financial/goal constraints are aggregated into a common `ConstraintSet`.

### 6.4 Eight eligibility fits are explicitly defined

The fit vocabulary is centralized and the decision layer consumes the eight-fit result.

### 6.5 DecisionResult exists

There is already an identifiable runtime decision authority.

### 6.6 Decision snapshots are persisted

Finalized StrategyVersions retain decision evidence for auditability.

### 6.7 Stress/what-if capability exists

The foundation exists even though the complete resilience framework is not yet canonical.

---

# 7. Main System Drift Risks Identified Across Steps 1–9

The detailed audits repeatedly expose the same architectural risk:

> **Definitions are more centralized than executable business rules.**

The major drift risks are:

| Risk | Meaning |
|---|---|
| Multiple rule owners | Similar business decisions can be defined in different engines |
| Stale strategy IDs | Old strategy vocabulary can remain executable |
| Applicability/eligibility overlap | Same condition may be evaluated twice with different meaning |
| Constraint/diagnostic overlap | An unhealthy metric may accidentally become a hard decision |
| Variant rules outside canonical registry | 22 variants exist, but selection logic lives elsewhere |
| Technique selection not canonical | Registry exists, selection policy is incomplete |
| Architecture before final selection | Can create circular decision influence |
| Recommendation adding decision logic | Presentation layer can accidentally become another decision engine |
| Stress as separate logic | Could create inconsistent recommendations under stress |
| Missing-data ambiguity | Missing evidence can be interpreted differently across layers |

These are the main issues the canonicalization effort must eliminate.

---

# 8. Canonical Ownership Model

The future system should have one clear business-rule owner for each decision domain.

| Domain | Recommended canonical owner |
|---|---|
| Goal classification | Canonical Goal rules |
| Hard constraints | Canonical Constraint policy |
| Strategy applicability | Canonical Applicability rules |
| 8 eligibility fits | Canonical Eligibility policy |
| Strategy selection | Canonical Strategy Selection policy |
| Variant selection | Canonical Variant rules |
| Technique selection | Canonical Technique rules |
| Architecture | Canonical Architecture rules |
| Stress/resilience | Canonical Stress/Resilience rules |
| Final decision | Canonical Decision Engine |
| Recommendation | Explanation/presentation layer |
| Historical audit | Immutable decision snapshot |

The engines should primarily **execute and orchestrate canonical policy**, rather than independently inventing business rules.

---

# 9. Business Rule Layers Must Stay Separate

The following distinctions are fundamental:

### Applicability

> Should the strategy enter the candidate pool?

### Hard Constraint

> Is the planning situation allowed to proceed under safety/validity policy?

### Eligibility

> Can this strategy work under the person's financial conditions?

### Selection

> Which viable strategy is best?

### Variant

> Which implementation form of that strategy fits?

### Technique

> Which techniques should implement the selected path?

### Architecture

> How are the selected elements assembled?

### Stress / Resilience

> Does the selected plan remain viable when inputs worsen?

### Recommendation

> How should the final decision be explained to the investor?

These should not collapse into one generic “score.”

---

# 10. What Is NOT Frozen Yet

The nine documents intentionally leave important business decisions open.

Do **not** freeze these merely because the current code already has values:

### Applicability

- exact AND/OR semantics;
- horizon bands;
- missing-data behavior;
- strategy-specific applicability conditions.

### Hard Constraints

- exact final constraint taxonomy;
- universal vs goal-specific blocking;
- unavailable-data treatment;
- complete canonical rule identity.

### Eligibility

- exact thresholds;
- status symmetry;
- missing-evidence status;
- applicability vs Goal Constraint Fit boundary;
- aggregation semantics if future policy changes.

### Strategy Selection

- exact score weights;
- score formula;
- precedence;
- conditional-vs-PASS policy;
- alternative policy.

### Variants

- exact conditions;
- deterministic precedence;
- missing-data handling;
- reachability of all 22 variants;
- baseline override policy.

### Techniques

- exact mappings;
- combination rules;
- precedence;
- readiness requirements;
- missing-input behavior.

### Architecture

- supporting strategy rules;
- candidate vs final architecture boundary;
- feasibility definition;
- final composition order.

### Stress / Resilience

- exact shocks;
- correlated stress combinations;
- materiality threshold;
- resilience thresholds;
- re-selection policy.

### Final Decision

- final outcome labels;
- final schema;
- alternative count;
- explanation contract;
- investor-facing evidence hierarchy.

---

# 11. Real-Life Validation Before Freeze

The next phase should **not be immediate refactoring**.

First validate the proposed decision framework against real financial-planning cases.

The cases should cover at least:

1. Clearly viable single strategy.
2. Multiple viable strategies.
3. PASS vs CONDITIONAL.
4. Only CONDITIONAL candidates.
5. No viable candidate.
6. Hard constraint restriction.
7. Missing data.
8. Different goal horizons.
9. Existing assets vs new contribution.
10. Debt pressure.
11. Liquidity pressure.
12. Risk-capacity mismatch.
13. Multi-goal conflict.
14. Same strategy with different variants.
15. Same variant with different techniques.
16. Different architecture paths.
17. Mild stress.
18. Severe stress.
19. Stress-driven variant change.
20. Stress-driven strategy change.
21. Stress-driven architecture change.
22. Recovery scenario.
23. Investor priority change.
24. Finalized decision snapshot reproducibility.

For every case, record:

```text
Inputs
→ Expected Business Decision
→ Current Code Decision
→ Difference
→ Rule Responsible
→ Decision Domain
→ Proposed Canonical Rule
→ Evidence
```

This becomes the evidence used to freeze Version 1.

---

# 12. Freeze Process

The recommended sequence is:

### Phase A — Design

Complete Steps 1–9.

**Current status:** substantially documented.

### Phase B — Real-Life Validation

Run representative cases against the proposed decision tree.

Identify:

- false positives;
- false negatives;
- overlapping rules;
- missing rules;
- wrong precedence;
- missing-data failures;
- stale strategy references.

### Phase C — Rule Decisions

For every unresolved business question, decide:

- exact condition;
- threshold;
- scope;
- precedence;
- missing-data behavior;
- outcome;
- evidence.

### Phase D — Canonical Rulebook V1

Only after the business decisions are agreed should the rules be frozen.

The Version 1 document should contain, for every rule:

| Field | Required |
|---|---|
| Rule ID | Yes |
| Rule name | Yes |
| Decision domain | Yes |
| Exact condition | Yes |
| Inputs | Yes |
| Thresholds | Yes, where applicable |
| Outcome | Yes |
| Precedence | Yes |
| Missing-data behavior | Yes |
| Examples | Yes |
| Owner | Yes |
| Version | Yes |

### Phase E — Refactor

Only after V1 is frozen:

- move business rules to canonical owners;
- remove duplicated rules;
- remove stale strategy IDs;
- make engines execute canonical rules;
- preserve behavior where required;
- add regression tests;
- verify all 22 variants;
- verify frontend/backend agreement.

### Phase F — Freeze in Code

The implementation and canonical rulebook must agree.

No engine should contain an undocumented alternative version of a frozen business rule.

---

# 13. Versioning Model

The detailed Steps 1–9 should remain as **historical design/audit evidence**.

They should not be repeatedly rewritten into a giant final document.

The recommended documentation structure is:

```text
docs/Decision tree/
│
├── 00-DECISION_ENGINE_DESIGN_SUMMARY.md
│
├── 01-STRATEGY_APPLICABILITY_CURRENT_STATE_AND_RECOMMENDATION.md
├── 02-HARD_CONSTRAINTS_CURRENT_STATE_AND_RECOMMENDATION.md
├── 03-8_ELIGIBILITY_FITS_CURRENT_STATE_AND_RECOMMENDATION.md
├── 04-STRATEGY_SELECTION_CURRENT_STATE_AND_RECOMMENDATION.md
├── 05-22-VARIANT_SELECTION_CURRENT_STATE_AND_RECOMMENDATION.md
├── 06-TECHNIQUE_SELECTION_CURRENT_STATE_AND_RECOMMENDATION.md
├── 07-ARCHITECTURE_COMPOSITION_CURRENT_STATE_AND_RECOMMENDATION.md
├── 08-STRESS_RESILIENCE_CURRENT_STATE_AND_RECOMMENDATION.md
└── 09-FINAL_DECISION_AND_RECOMMENDATION_CURRENT_STATE_AND_RECOMMENDATION.md
```

After business validation:

```text
docs/Decision tree/
│
├── 00-DECISION_ENGINE_DESIGN_SUMMARY.md
├── 01–09 detailed audit/design documents
│
└── CANONICAL_DECISION_ENGINE_V1.md
```

Future major changes can then create:

- `CANONICAL_DECISION_ENGINE_V2.md`
- `CANONICAL_DECISION_ENGINE_V3.md`

This preserves both **why the rules were designed** and **what the frozen rules actually are**.

---

# 14. What the V1 Canonical Document Should NOT Do

The future V1 document should not simply copy the nine audit documents.

It should be much more precise.

It should answer:

> **“Given these exact inputs, what exact decision does the system make, and why?”**

Therefore V1 should contain executable business policy, not exploratory discussion.

Example:

```text
Rule ID: STRAT-APP-001
Domain: Strategy Applicability
Condition: ...
Inputs: ...
Outcome: Applicable / Not Applicable
Precedence: ...
Missing data: ...
Version: 1.0
```

That is the document that implementation should ultimately follow.

---

# 15. Final Architectural Principle

The objective of this work is not simply to make the code cleaner.

The objective is to establish:

> **One business decision → one canonical rule → one execution owner → one auditable result.**

The final system should therefore avoid:

- duplicate business rules;
- stale strategy identities;
- hidden selection logic;
- recommendation-layer decision making;
- independent stress recommendation logic;
- undocumented thresholds;
- missing-data assumptions;
- multiple conflicting decision authorities.

---

# 16. Current Status

| Area | Status |
|---|---|
| Nine decision domains identified | **Complete** |
| Current-state code audit | **Documented** |
| Target decision sequence | **Documented** |
| Major gaps/overlaps | **Documented** |
| Canonical business rules | **Not frozen** |
| Real-life validation | **Next phase** |
| V1 rulebook | **Not yet created** |
| Refactor | **Should follow rule freeze** |
| Final code canonicalization | **Pending V1 decisions** |

---

# 17. Next Action

The next correct step is:

**Real-Life Decision Case Validation**

—not refactoring.

The goal is to use real financial-planning cases to answer the unresolved business questions in Steps 1–9.

Once those cases produce stable rules, create:

**`CANONICAL_DECISION_ENGINE_V1.md`**

and freeze the business rules there.

Only then should the code be refactored around those frozen rules.

---

## Document Status

**Design Summary — Complete**

**Business Rules — Intentionally Not Frozen**

**Next Phase — Real-Life Validation → Rule Freeze → V1 Canonical Rulebook → Code Refactor**
