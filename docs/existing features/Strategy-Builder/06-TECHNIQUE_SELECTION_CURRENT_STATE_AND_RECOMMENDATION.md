# 06 — Technique Selection: Current State & Recommendation

## 1. Purpose

This document records the current code-verified Technique Selection system and the recommended target contract for the PlanVesto Canonical Decision Engine.

This is a design/audit document only. Technique-selection rules are not frozen and no refactor is authorized by this document.

Final business behavior will be frozen later through real-life cases.

## 2. Scope

This step answers:

> After a strategy and variant are selected, which canonical techniques should be used to implement that decision?

This covers:
- canonical technique definitions,
- current strategy-to-technique mapping,
- current execution behavior,
- selection vs execution boundary,
- missing technique-selection policy,
- unused techniques,
- recommended ownership.

It does not freeze architecture composition or stress/resilience.

## 3. Current Canonical Technique Registry

The current code contains **10 canonical techniques** in:

`backend/library/strategies/techniques_canonical.py`

| # | Technique | ID |
|---|---|---|
| 1 | Bucketing | `tech-bucketing` |
| 2 | Laddering | `tech-laddering` |
| 3 | Glide Path | `tech-glide-path` |
| 4 | Cash-flow Matching | `tech-cashflow-matching` |
| 5 | Barbell / Dumbbell | `tech-barbell` |
| 6 | Asset Earmarking | `tech-asset-earmarking` |
| 7 | Goal Segmentation | `tech-goal-segmentation` |
| 8 | Contribution Escalation | `tech-contribution-escalation` |
| 9 | Tax-Efficient Sequencing | `tech-tax-efficient-sequencing` |
| 10 | Tax-Loss Harvesting | `tech-tax-loss-harvesting` |

The registry is a definition catalog. It explicitly states that techniques are reusable strategic methods and do not contain investor-specific execution logic.

## 4. Current Strategy-to-Technique Mapping

The current five canonical strategies declare technique IDs directly in:

`backend/library/strategies/canonical.py`

| Strategy | Current techniques |
|---|---|
| Goal Funding | Asset Earmarking, Contribution Escalation, Cash-flow Matching, Bucketing, Tax-Efficient Sequencing |
| Progressive De-risking | Glide Path, Bucketing, Cash-flow Matching |
| Capital Preservation | Bucketing, Laddering, Cash-flow Matching |
| Debt Reduction | Goal Segmentation, Cash-flow Matching |
| Credit Utilisation | Cash-flow Matching, Goal Segmentation |

### Current coverage

8 of the 10 registered techniques are currently attached to at least one canonical strategy.

The two registered techniques not attached to a current strategy are:

- Barbell / Dumbbell
- Tax-Loss Harvesting

This does not necessarily mean they are wrong or obsolete. It means their current place in the canonical decision tree is not established by the strategy mapping.

## 5. Current Technique Authority

There are currently three distinct layers:

### A. Definition authority

`backend/library/strategies/techniques_canonical.py`

Owns:
- technique ID,
- name,
- description,
- purpose.

### B. Applicability/mapping authority

`backend/library/strategies/canonical.py`

Each strategy directly declares its `technique_ids`.

### C. Execution authority

`backend/engines/technique/engine.py`

This executes deterministic calculations for the selected technique.

Therefore the current system has a useful separation:

**Definition → Strategy Mapping → Execution**

But there is not yet a distinct canonical **Technique Selection Policy**.

## 6. Current Technique Execution

`backend/engines/technique/engine.py` provides executable handlers for all 10 registered techniques.

The engine returns:
- `technique_id`: str,
- `status`: Literal["calculated", "insufficient_inputs", "not_implemented"],
- `inputs`: dict[str, Any],
- `parameters`: dict[str, Any],
- `outputs`: dict[str, Any],
- `warnings`: list[str].

### Exact Execution Formulas & Mathematical Output Shapes:
1. **Bucketing (`tech-bucketing`):** Partitions goal target into $N$ horizon tranches ($N \in [1, 5]$):
   - Computes weights $w_i = \frac{1}{i+1}$, tranches target amount $T_i = \text{target} \times \frac{w_i}{\sum w_k}$.
   - Progressively allocates existing assets $A$ across tranches and tracks tranche-wise funding gaps.
2. **Contribution Escalation (`tech-contribution-escalation`):**
   - Future value with compounding escalation:
     $$\text{FV} = \sum_{y=0}^{Y-1} \left(S \times (1+e)^y \times \text{FV}_{\text{monthly}}(1 \text{ yr}) \times (1+r)^{Y-y-1}\right)$$
   - Returns year-by-year projected cash flow schedules.
3. **Glide Path (`tech-glide-path`):** Shifts allocation from growth to liquid as remaining duration $t$ drops below threshold.
4. **Laddering (`tech-laddering`):** Staggers maturities across discrete annual intervals with equal tranche targets.
5. **Cash-flow Matching (`tech-cashflow-matching`):** Direct match of projected asset cash inflows against required goal outflows.

### Scoring Integration in Strategy Decision:
Technique readiness feeds directly into `backend/rules/strategy_decision.py::calculate_technique_execution_score()`:
- `status == "calculated"`: **+1.0 point**
- `status == "insufficient_inputs"`: **+0.5 point**
- `status == "not_implemented"`: **0.0 points**
- Capped at `TECHNIQUE_EXECUTION_MAX_SCORE = 10.0`.

## 7. Current Execution Coverage

All 10 canonical technique IDs have registered executable handlers in the current TechniqueEngine:

- Bucketing
- Glide Path
- Laddering
- Cash-flow Matching
- Asset Earmarking
- Contribution Escalation
- Barbell
- Goal Segmentation
- Tax-Efficient Sequencing
- Tax-Loss Harvesting

Therefore there is currently no obvious **registry-vs-executor gap** for the 10 techniques.

However, there is a **strategy-mapping gap** for two techniques because they are executable but not attached to any current strategy.

## 8. Current Runtime Flow

The current StrategyEngine does this:

1. Determine applicable strategies.
2. Generate scenarios.
3. Compose architectures.
4. Read technique IDs from each architecture.
5. Execute those technique IDs through TechniqueEngine.
6. Pass technique outputs into the strategy decision.
7. Generate recommendation.

This is important because technique execution currently occurs **before final strategy selection**.

So the current runtime is effectively:

**Candidate Strategy → Architecture → Technique Execution → Strategy Decision**

This is different from the cleaner conceptual flow:

**Strategy → Variant → Technique Selection → Technique Execution**

That difference should be explicitly resolved before freezing the architecture.

## 9. Current Technique Scoring

Technique execution currently contributes to the strategy decision through:

`technique_execution_score`

The scoring policy gives points based on execution status:

- calculated → 1.0
- insufficient_inputs → 0.5
- not_implemented → 0.0

The score is capped at the configured technique execution maximum.

### Important design concern

This means the **availability/readiness of a technique can influence which strategy wins**.

That creates a dependency:

**Strategy candidate → technique execution → technique score → strategy selection**

This may be appropriate, but it must be an explicit product decision.

A technique should generally not become a reason to choose the wrong strategy simply because its calculation happens to be easier to execute.

## 10. Current Problems / Gaps

### Gap 1 — No dedicated Technique Selection Policy

The strategy library declares techniques, but there is no dedicated canonical rule layer answering:

> Given this strategy + variant + goal context, which subset of its techniques should actually be activated?

### Gap 2 — Strategy mapping is broader than actual selection

A strategy can declare several techniques. Current composition largely carries those technique IDs into the architecture.

Therefore:

**Declared technique ≠ necessarily selected technique**

The distinction needs to become explicit.

### Gap 3 — Variant-to-technique mapping is not canonicalized

The 22 variants do not currently declare their own technique mappings in the variant registry.

This makes it difficult to answer:

> Why is Technique X selected for Variant Y?

### Gap 4 — Two techniques have no current strategy owner

Barbell / Dumbbell and Tax-Loss Harvesting are canonical and executable but currently unassigned to a strategy.

### Gap 5 — Technique execution happens before final strategy selection

This can create unnecessary computation and circular selection influence.

### Gap 6 — Missing inputs produce execution states

For example, tax-efficient sequencing can return `insufficient_inputs` when funding-source tax information is unavailable.

This is useful evidence, but it should not automatically imply that the parent strategy is inferior unless that is explicitly intended.

### Gap 7 — Tax techniques need a clear decision boundary

Tax-Efficient Sequencing and Tax-Loss Harvesting depend on tax-specific information.

The current execution layer correctly does not infer jurisdiction-specific law, but the Decision Engine still needs to decide when these techniques are applicable.

## 11. Recommended Target Technique Flow

The recommended future flow is:

**Strategy**
↓
**Selected Variant**
↓
**Technique Candidate Set**
↓
**Technique Applicability**
↓
**Technique Conditions**
↓
**Technique Precedence / Combination Rules**
↓
**Selected Techniques**
↓
**Technique Execution**
↓
**Technique Outputs**

This separates:

**selection**

from

**calculation**.

## 12. Recommended Rule Ownership

| Responsibility | Recommended authority |
|---|---|
| Technique identity | `backend/library/strategies/techniques_canonical.py` |
| Strategy-to-technique baseline mapping | Strategy library |
| Variant-to-technique mapping | Canonical Variant/Technique rules |
| Technique applicability | Canonical Technique Selection rules |
| Technique combination rules | Canonical Technique Selection rules |
| Technique execution | `backend/engines/technique/engine.py` |
| Technique output validation | Technique execution layer |
| Strategy decision | Canonical Decision Engine |

Recommended future rule location:

`backend/rules/technique_selection.py`

The engine should execute these rules rather than contain business-policy conditions.

## 13. Recommended Technique Selection Contract

For every selected strategy + variant:

1. Load canonical technique candidates.
2. Remove techniques that are not applicable.
3. Evaluate required inputs.
4. Apply explicit combination/exclusion rules.
5. Select the required technique set.
6. Record why each technique was selected or rejected.
7. Execute only the selected techniques.
8. Return execution status and outputs.

The final result should distinguish:

- **selected**
- **not applicable**
- **insufficient inputs**
- **execution failure**

These are different states and should not be collapsed.

## 14. Recommended Variant-Level Mapping

The target model should eventually support:

**Strategy → Variant → Technique Set**

For example:

**Progressive De-risking**
→ Income-Transition Glide Path
→ Glide Path + Bucketing + Cash-flow Matching

This is preferable to assuming every technique attached to the parent strategy is automatically executed for every variant.

The exact mapping must be validated with real-life cases.

## 15. Recommended Technique Combination Policy

The future rule set should explicitly define:

### Required technique

Must be present for the variant.

### Optional technique

May be activated if supporting evidence exists.

### Conditional technique

Activated only when a defined condition is met.

### Mutually exclusive technique

Cannot coexist with another technique.

### Evidence-only technique

Calculated for analysis but does not alter the decision.

This will prevent technique selection from becoming an uncontrolled list of methods.

## 16. Real-Life Validation Cases Before Freezing

Validate at minimum:

1. Goal Funding + Existing Assets.
2. Goal Funding + SIP.
3. Goal Funding + Step-up SIP.
4. Goal Funding + hybrid funding.
5. Progressive De-risking + retirement.
6. Progressive De-risking + education.
7. Progressive De-risking + recurring vacation.
8. Capital Preservation + near-term goal.
9. Capital Preservation + staged education.
10. Debt Reduction + high EMI.
11. Debt Reduction + debt-linked goal.
12. Credit Utilisation + timing bridge.
13. Credit Utilisation + education financing.
14. Variant requiring multiple techniques.
15. Variant requiring one technique only.
16. Missing technique inputs.
17. Tax data unavailable.
18. Tax-loss harvesting data available.
19. Two techniques that may conflict.
20. Two techniques that should be combined.
21. Technique execution unavailable.
22. Technique calculated but should not influence strategy selection.

For every case record:

**Strategy → Variant → Candidate Techniques → Conditions → Selected Techniques → Execution Inputs → Outputs → Reason**

## 17. What Should NOT Be Frozen Yet

Do not freeze solely from current code:

- exact strategy-to-technique rules,
- variant-to-technique mappings,
- whether all strategy techniques are always executed,
- technique precedence,
- mutually exclusive combinations,
- tax-technique eligibility,
- whether technique readiness affects strategy selection,
- whether technique execution occurs before or after strategy selection,
- missing-input treatment,
- whether Barbell/Dumbbell should be attached to a current strategy,
- whether Tax-Loss Harvesting belongs inside the Decision Engine or downstream portfolio/tax planning.

## 18. Current vs Recommended Summary

| Area | Current state | Recommendation |
|---|---|---|
| Technique definitions | 10 canonical | Preserve |
| Execution coverage | All 10 executable | Preserve |
| Strategy mapping | 8 used by current strategies | Validate |
| Unassigned techniques | Barbell, Tax-Loss Harvesting | Decide later |
| Technique selection policy | No dedicated canonical rule layer | Create |
| Variant mapping | Not explicit | Make explicit |
| Execution | TechniqueEngine | Preserve |
| Runtime timing | Execution before final strategy decision | Reconsider |
| Technique scoring | Can affect strategy selection | Validate |
| Missing inputs | Execution status available | Preserve, but formalize decision meaning |
| Auditability | Technique outputs exist | Add selection rationale/conditions |

## 19. Decision Status

**CURRENT STATUS: DOCUMENTED — NOT FROZEN**

The repository has a strong technique definition and execution foundation: all 10 canonical techniques are registered and executable.

The main missing layer is **canonical technique selection** — especially the mapping from **Strategy + Variant → Technique Set**.

The next step is to validate these mappings and selection rules through real-life cases before freezing them.

**Next step: Step 7 — Architecture Composition: Current State & Recommendation.**
