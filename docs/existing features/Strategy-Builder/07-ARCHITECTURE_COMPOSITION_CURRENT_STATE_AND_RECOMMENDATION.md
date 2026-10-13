# 07 — Architecture Composition: Current State & Recommendation

> **Current-state audit only — not target policy:** Any Goal Funding / `strat-goal-funding` Strategy row, variant, candidate, or behavior described below records legacy runtime observed during audit. Canonical target ownership is Goal Planner / Goal Feasibility; Goal Funding is not a Strategy Builder strategy. Follow `docs/implementations/Strategy-Builder.md` and `docs/Real-Life Decision Cases/strategy-decision-tree.md` for target rules. Preserve these observations as audit evidence; do not implement them as target behavior.


## 1. Purpose

This document records the current code-verified Architecture Composition system and the recommended target contract for the PlanVesto Canonical Decision Engine.

This is a design/audit document only. Architecture-composition rules are not frozen and no refactor is authorized by this document.

Final business behavior will be frozen later through real-life cases.

## 2. Scope

This step answers:

> After strategy, variant and technique decisions, how should the final strategy architecture be assembled?

It covers:
- architecture identity,
- primary and supporting strategies,
- components,
- solutions,
- techniques,
- constraints,
- feasibility,
- rationale,
- current ordering,
- current gaps,
- recommended target ownership.

It does not freeze stress/resilience or final recommendation behavior.

## 3. Current Architecture Model

The current architecture object is:

`backend/models/strategy.py::StrategyArchitecture`

It contains:

- `architecture_id`
- `primary_strategy_id`
- `supporting_strategy_ids`
- `solution_ids`
- `technique_ids`
- `rationale`
- `trade_offs`
- `feasibility_status`
- `constraints`

This is a strong foundation because the architecture explicitly separates the primary strategy from supporting strategies.

## 4. Current Architecture Identity

Architecture identity is handled by:

`backend/engines/strategy/identity.py`

The current identity is based only on:

**Goal ID + Primary Strategy ID**

Supporting strategies, techniques and solutions are deliberately excluded from identity.

Therefore:

> Architecture identity is composition-independent.

This is consistent with the system's canonical identity requirement and prevents a change in composition from silently creating a new architecture identity.

## 5. Current Architecture Composition Authority

The current composition authority is:

`backend/engines/strategy/composition.py::compose_architectures()`

It composes architectures from:
- canonical strategy definitions,
- canonical components,
- canonical solutions,
- canonical techniques,
- financial context,
- diagnostics.

The library provides definitions; the composition engine performs runtime assembly.

## 6. Current Component System

Canonical components are defined in:

`backend/library/strategies/components.py`

Current component families include:

- Funding
- Accumulation
- Transition
- Preservation
- Liquidity
- Debt
- Credit
- Orchestration
- Income

Each component has centralized activation metadata.

Examples:

| Component | Current activation |
|---|---|
| Funding | funding status = Shortfall |
| Accumulation | duration >= 7 years |
| Transition | duration <= 7 years |
| Preservation | priority = High |
| Liquidity | duration <= 5 years |
| Debt | liabilities/debt inputs present |
| Credit | funding gap + positive surplus + EMI input |
| Orchestration | On Track / Overfunded |
| Income | duration <= 5 years |

These are useful canonical component signals, but their relationship to final architecture composition is still partly implemented by engine code.

## 7. Current Supporting-Strategy Logic

The composition engine evaluates whether one strategy can support another.

A candidate supporting strategy is rejected when:

- it is the same as the primary strategy,
- either strategy explicitly conflicts with the other,
- any component pair is incompatible.

Otherwise it can become a supporting strategy.

The architecture therefore supports:

**Primary Strategy + Supporting Strategies**

rather than forcing every goal into one isolated strategy.

## 8. Current Preferred Component Activation

For each candidate primary strategy, the composition engine checks component preference against the current context.

If preferred components exist:

- those components become the architecture activation reason,
- compatible strategies can be added as supporting strategies.

If no preferred component matches:

- the architecture is still retained,
- but it is marked as having no preferred component activation.

This is important:

> Component activation does not currently remove a strategy from the candidate set.

Applicability and component activation are therefore separate concepts.

## 9. Current Solution Model

The canonical solution matrix is:

`backend/library/strategies/solution_matrix.py`

It explicitly defines:

**Strategy = responsibility / architecture**

**Solution = concrete implementation path inside the strategy**

For Goal Funding:

- the six variants are represented as solutions.

For the other four strategies:

- their declared techniques are currently represented as solutions.

This means the solution layer is not yet symmetrical across all five strategies.

## 10. Current Architecture Assembly

For each applicable strategy the composition engine:

1. loads its canonical components,
2. evaluates preferred component activation,
3. identifies compatible supporting strategies,
4. collects components,
5. loads canonical solutions,
6. validates component references,
7. validates technique references,
8. checks required inputs,
9. carries diagnostics into architecture constraints,
10. creates the architecture object.

Architecture feasibility becomes conditional when:

- required strategy inputs are missing,
- diagnostic constraints exist,
- no canonical solutions are mapped.

## 11. Current Architecture Feasibility

The current architecture has three states:

- feasible
- conditional
- infeasible

In current composition code, architecture creation itself generally produces:

- `feasible` when required inputs/solutions/diagnostics are satisfactory,
- `conditional` when missing inputs, diagnostics, or missing solutions exist.

The actual strategy decision can subsequently reject an architecture through eligibility.

Therefore architecture feasibility and strategy eligibility are related but not identical.

## 12. Current Runtime Ordering — Important Issue

The current StrategyEngine sequence is approximately:

**Applicable Strategies**
→ **Scenarios**
→ **What-if Scenarios**
→ **Architecture Composition**
→ **Technique Execution**
→ **Strategy Decision**
→ **Ranking**
→ **Recommendation**

This means architecture is currently composed **before the final strategy decision**.

Therefore the current architecture is simultaneously:

- a candidate representation,
- an input to strategy selection,
- and a downstream implementation representation.

This is the most important architecture-level design issue to resolve.

## 13. Current Technique Relationship

The architecture receives:

`technique_ids=list(primary.technique_ids)`

Therefore all techniques declared by the primary strategy are currently carried into the architecture.

This is broader than the target concept discussed in Step 6:

**Strategy + Variant → Selected Technique Set**

The architecture currently does not appear to select techniques at variant level.

## 14. Current Diagnostic Relationship

Financial-state diagnostics can be copied into architecture constraints.

The composition engine specifically carries critical/warning diagnostic messages into architecture constraints.

The architecture rationale states that these constraints are carried into implementation without changing priority-based ranking.

This is a useful separation:

**Diagnostic evidence can constrain implementation without automatically becoming strategy-selection policy.**

However, this boundary must remain explicit when the final Decision Engine is designed.

## 15. Current Architecture Problems / Gaps

### Gap 1 — Architecture is both candidate and output

Architecture is currently composed before strategy selection but is also returned as the selected implementation architecture.

This creates an unclear boundary between:

**candidate architecture**

and

**final architecture**.

### Gap 2 — Technique selection is not variant-specific

Architecture currently copies strategy-level techniques rather than consuming an explicit selected technique set.

### Gap 3 — Solution model is asymmetric

Goal Funding solutions are variants.

Other strategies currently expose techniques as solutions.

This means "solution" has different meanings across strategy families.

### Gap 4 — Component activation can create supporting strategies

The current engine can add supporting strategies based on component compatibility and activation.

This is useful, but the exact business policy for when a supporting strategy should be added is not yet a canonical decision rule.

### Gap 5 — Required-input checking is generic

Missing inputs are detected against `StrategyDefinition.required_inputs`, but the meaning of those inputs is not yet represented as a complete canonical architecture contract.

### Gap 6 — Architecture feasibility and eligibility overlap

Some architecture constraints can look similar to eligibility conditions.

The future model should clearly distinguish:

- strategy eligibility,
- variant feasibility,
- technique readiness,
- architecture feasibility.

### Gap 7 — Composition is executable business policy

The composition engine contains meaningful policy about:
- support compatibility,
- preferred components,
- diagnostics,
- missing solutions,
- missing inputs.

This should eventually be driven by canonical rules rather than embedded solely in orchestration code.

## 16. Recommended Target Architecture Flow

The recommended conceptual sequence is:

**Goal**
→ **Goal Classification**
→ **Hard Constraints**
→ **Strategy Applicability**
→ **8-Fit Eligibility**
→ **Strategy Selection**
→ **Variant Selection**
→ **Technique Selection**
→ **Architecture Composition**
→ **Stress / Resilience**
→ **Final Recommendation**

Architecture should therefore be a **downstream composition stage**, not the mechanism that decides which strategy wins.

## 17. Recommended Architecture Contract

The final architecture should answer:

1. What is the primary strategy?
2. Which supporting strategies are required?
3. Which variant is selected?
4. Which techniques are selected?
5. Which components are activated?
6. Which solutions implement the decision?
7. What constraints apply?
8. What trade-offs exist?
9. What evidence supports the composition?
10. Is the architecture feasible, conditional, or infeasible?

Conceptually:

**Primary Strategy + Supporting Strategies + Variant + Techniques + Components + Solutions + Constraints**

## 18. Recommended Supporting-Strategy Rule

Supporting strategies should not be added merely because their components happen to fit.

Recommended target rule:

> Add a supporting strategy only when it materially addresses a requirement that the primary strategy cannot satisfy alone, is compatible with the primary strategy, and does not violate hard constraints.

This is a recommendation, not a frozen rule.

## 19. Recommended Architecture Identity

Preserve the current identity model:

**Architecture ID = Goal ID + Primary Strategy ID**

Do not include:
- supporting strategies,
- variants,
- techniques,
- components,
- solutions

in the architecture identity unless the product later explicitly decides that architecture versions must be independently addressable.

Composition changes should remain data changes to the same canonical architecture identity.

## 20. Recommended Architecture Feasibility Contract

Architecture feasibility should be calculated after strategy/variant/technique selection.

Recommended conceptual statuses:

| Status | Meaning |
|---|---|
| Feasible | Required architecture inputs and selected implementation path are available |
| Conditional | Architecture is possible but requires a defined change or missing evidence |
| Infeasible | Architecture cannot currently be implemented under the binding constraints |

The exact status rules should be frozen after real-life cases.

## 21. Recommended Rule Ownership

| Responsibility | Recommended authority |
|---|---|
| Strategy identity | Strategy Library |
| Strategy selection | Canonical Decision Engine |
| Variant selection | Canonical Variant Rules |
| Technique selection | Canonical Technique Rules |
| Component definitions | Component Registry |
| Component activation | Canonical Architecture/Component Rules |
| Supporting-strategy compatibility | Canonical Architecture Rules |
| Solution mapping | Solution Matrix |
| Architecture feasibility | Canonical Architecture Rules |
| Architecture assembly | Architecture Engine |
| Architecture identity | Canonical Identity helper |

Recommended future rule location:

`backend/rules/architecture.py`

The engine should assemble the architecture from those rules.

## 22. Real-Life Validation Cases Before Freezing

Validate at minimum:

1. One strategy with one component.
2. One strategy with multiple components.
3. Strategy requiring a supporting strategy.
4. Two compatible strategies.
5. Two conflicting strategies.
6. Same component activated by multiple signals.
7. Missing required input.
8. Missing canonical solution.
9. Missing canonical technique.
10. Critical diagnostic present.
11. Warning diagnostic present.
12. Strategy is eligible but architecture is conditional.
13. Strategy is eligible and architecture is feasible.
14. Variant changes but architecture identity remains stable.
15. Technique changes but architecture identity remains stable.
16. Supporting strategy changes but architecture identity remains stable.
17. Multiple supporting strategies.
18. No compatible supporting strategy.
19. Goal Funding architecture with each funding variant.
20. Architecture remains feasible under a what-if scenario.

For every case record:

**Strategy → Variant → Techniques → Components → Supporting Strategies → Solutions → Constraints → Feasibility → Architecture ID**

## 23. What Should NOT Be Frozen Yet

Do not freeze solely from current code:

- exact supporting-strategy activation conditions,
- exact component activation thresholds,
- whether architecture must always be downstream of strategy selection,
- whether a supporting strategy can itself have a selected variant,
- variant-specific component mappings,
- variant-specific solution mappings,
- technique-to-component relationships,
- architecture feasibility thresholds,
- diagnostic-to-architecture behavior,
- whether architecture feasibility can ever override strategy selection,
- final stress/resilience interaction.

## 24. Current vs Recommended Summary

| Area | Current state | Recommendation |
|---|---|---|
| Architecture model | Strong explicit object | Preserve |
| Identity | Goal + primary strategy | Preserve |
| Primary/supporting strategies | Supported | Preserve |
| Components | Canonical registry | Preserve and formalize activation rules |
| Solutions | Canonical matrix | Clarify meaning across strategies |
| Techniques | Strategy-level | Move toward Strategy + Variant selection |
| Composition timing | Before final decision | Move downstream conceptually |
| Feasibility | feasible/conditional/infeasible | Preserve, formalize rules |
| Diagnostics | Carried into constraints | Preserve as implementation evidence |
| Supporting strategies | Engine-derived | Canonicalize activation policy |
| Rule ownership | Partly in composition engine | Move business policy to canonical architecture rules |
| Auditability | Rationale/constraints exist | Add explicit composition evidence |

## 25. Decision Status

**CURRENT STATUS: DOCUMENTED — NOT FROZEN**

The repository already has a strong architecture model and composition engine. The biggest architectural issue is **timing and ownership**: architecture is currently composed before final strategy selection, while the target Decision Engine should conceptually select strategy → variant → techniques first and then compose the final architecture.

The next step is:

**Step 8 — Stress / Resilience: Current State & Recommendation.**


---

## 26. Verification Correction — Candidate Architecture vs Final Architecture

The full runtime verification confirms that architecture composition currently occurs **before** `evaluate_decision()` and technique execution also occurs before the authoritative strategy decision.

Therefore the documented target sequence:

**Strategy → Variant → Technique → Architecture → Final Decision**

is not the current runtime sequence.

This creates an important business/architecture question that must be resolved before refactoring:

> Is the current architecture a candidate/evidence object used to evaluate a strategy, or should architecture only be composed after strategy, variant and technique selection?

The existing code supports candidate architectures before final selection. The target document should therefore treat downstream-only architecture as a **proposed target**, not as an already-proven design fact.

No code change is authorized by this clarification.

