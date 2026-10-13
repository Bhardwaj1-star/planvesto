# Strategy Applicability — Current State & Recommended Decision Framework

> **Current-state audit only — not target policy:** Any Goal Funding / `strat-goal-funding` Strategy row, variant, candidate, or behavior described below records legacy runtime observed during audit. Canonical target ownership is Goal Planner / Goal Feasibility; Goal Funding is not a Strategy Builder strategy. Follow `docs/implementations/Strategy-Builder.md` and `docs/Real-Life Decision Cases/strategy-decision-tree.md` for target rules. Preserve these observations as audit evidence; do not implement them as target behavior.


**Parent area:** `docs/existing features/Strategy-Builder/`  
**Decision Engine phase:** Step 1 — Strategy Applicability  
**Status:** Analysis / design only — rules are **not frozen** and no refactor is authorized by this document.

---

## 1. Purpose

This document isolates the first decision step of the PlanVesto Decision Engine:

> **Strategy Applicability — which strategies are allowed to enter the downstream decision pool for a defined goal?**

The purpose at this stage is **not to finalize business rules**.

The objective is to:

1. document what the current code does;
2. break the applicability step into explicit sub-decisions;
3. identify gaps, ambiguity and duplicated responsibility;
4. propose a cleaner target framework;
5. leave the actual business conditions open for later validation through real-life financial-planning examples.

The rules will be frozen only after the proposed conditions are tested against representative real-life cases.

---

# 2. Scope

This document covers only **strategy applicability**.

It does not freeze or redesign:

- hard constraints;
- the 8 eligibility fits;
- strategy selection;
- the 22 strategy variants;
- technique selection;
- architecture composition;
- stress testing;
- final recommendation.

Those are downstream Decision Engine steps.

The intended conceptual boundary is:

**Goal → Canonical Goal Type → Strategy Applicability → Applicable Strategy Pool → downstream decision steps**

---

# 3. Current Canonical Strategy Set

The current strategy library contains five canonical strategies:

| Strategy ID | Strategy | Current applicability scope |
|---|---|---|
| `strat-goal-funding` | Goal Funding | All canonical goal types; broad funding characteristics |
| `strat-progressive-de-risking` | Progressive De-risking | All corpus goals except Debt Freedom |
| `strat-capital-preservation` | Capital Preservation | All corpus goals except Debt Freedom |
| `strat-debt-reduction` | Debt Reduction | All canonical goal types |
| `strat-credit-utilisation` | Credit Utilisation | Education, Marriage, Dream Home, Vehicle, Others |

These definitions currently live in:

`backend/library/strategies/canonical.py`

The strategy library therefore already provides a useful **definition-level vocabulary** through:

- `applicable_goal_types`
- `applicable_goal_characteristics`

However, the interpretation of those characteristics is currently implemented in an engine rather than being a complete canonical applicability rule system.

---

# 4. Current Applicability Flow

The current execution path is approximately:

```text
Defined Goal
    ↓
Canonical Goal Type
    ↓
Loop through canonical strategies
    ↓
StrategyRuleEngine.evaluate()
    ↓
Goal-type match?
    ↓
Applicable characteristics evaluated
    ↓
If ANY characteristic matches
    ↓
Strategy considered applicable
```

The current filtering function is:

`backend/engines/strategy/applicability.py`

It delegates the actual evaluation to:

`backend/engines/rules/engine.py::StrategyRuleEngine`

This is an important architectural distinction:

> `filter_applicable_strategies()` is primarily orchestration/filtering. The current business interpretation is inside `StrategyRuleEngine`.

---

# 5. Current Signal Vocabulary

The current `StrategyRuleEngine` derives these applicability signals from the defined goal:

| Signal | Current code condition |
|---|---|
| `shortfall` | funding status = shortfall |
| `on_track` | funding status = on track |
| `overfunded` | funding status = overfunded |
| `near_term` | duration ≤ 5 years |
| `long_term` | duration ≥ 7 years |
| `fixed_timeline` | flexibility = fixed |
| `flexible_timeline` | flexibility ≠ fixed |
| `high_priority` | canonical priority = critical or high |

These signals are currently calculated directly inside `StrategyRuleEngine`.

---

# 6. Current Strategy-by-Strategy Applicability

## 6.1 Goal Funding

### Existing code

**Goal types:** all canonical goal types.

**Characteristics:**

- shortfall
- on_track
- overfunded
- near_term
- long_term
- fixed_timeline
- flexible_timeline
- high_priority

### Current behavior

Because the engine considers a strategy applicable when **at least one** configured characteristic matches, Goal Funding has an intentionally broad applicability footprint.

### Interpretation

This is consistent with the strategy library's description that Goal Funding is the unified goal-funding architecture.

### Recommendation

Keep Goal Funding as the broadest funding architecture, but later define precisely:

- whether every valid goal should always have Goal Funding as an applicable strategy;
- whether Goal Funding is a baseline architecture or a conditionally applicable strategy;
- whether its characteristics are genuinely applicability conditions or descriptive context;
- whether overfunded/on-track states should influence applicability or only downstream selection.

**Do not freeze these yet.**

---

## 6.2 Progressive De-risking

### Existing code

**Goal types:** all corpus goal types except Debt Freedom.

**Characteristics:**

- near_term
- fixed_timeline
- on_track
- shortfall

### Current behavior

Any one matching characteristic can make the strategy applicable.

### Recommendation

The later canonical rule should distinguish between:

- time-to-goal;
- funding status;
- timeline certainty;
- whether sufficient capital is already accumulated;
- whether de-risking is relevant to the actual goal.

The key question to validate with real-life examples is:

> Is a near-term goal alone sufficient to make Progressive De-risking applicable, or should there also be a funding/asset condition?

No final rule should be frozen yet.

---

## 6.3 Capital Preservation

### Existing code

**Goal types:** all corpus goal types except Debt Freedom.

**Characteristics:**

- near_term
- fixed_timeline
- high_priority
- shortfall
- on_track

### Current behavior

Any one matching characteristic can make Capital Preservation applicable.

### Recommendation

Later validate whether:

- near-term alone is sufficient;
- high priority alone is sufficient;
- shortfall alone is sufficient;
- fixed timeline alone is sufficient;
- combinations should be required;
- preservation should depend on the amount of capital already exposed to risk.

This should be tested against actual examples before freezing.

---

## 6.4 Debt Reduction

### Existing code

**Goal types:** all canonical goal types.

**Characteristics:**

- shortfall
- high_priority

### Current behavior

A shortfall alone can make Debt Reduction applicable.

A high-priority goal alone can also make it applicable.

### Recommendation

This needs particularly careful real-life validation.

A goal shortfall does **not automatically mean debt reduction is the appropriate strategy**.

The future canonical rule should distinguish:

- existence of liabilities;
- debt burden;
- debt cost;
- EMI pressure;
- available surplus;
- goal priority;
- effect of debt reduction on goal feasibility.

The strategy library itself states that debt reduction is a resource-allocation decision rather than an automatic recommendation.

Therefore applicability should eventually be more specific than simply:

`shortfall OR high_priority`

But the exact condition should be frozen only after examples are tested.

---

## 6.5 Credit Utilisation

### Existing code

**Goal types:**

- education
- marriage
- dream_home
- vehicle
- others

**Characteristics:**

- shortfall
- near_term
- fixed_timeline

### Current behavior

Any one matching characteristic can make Credit Utilisation applicable after the goal-type gate.

### Recommendation

This is the strategy where the current OR-based applicability is most obviously worth testing.

A credit strategy should eventually require evidence that:

1. there is a legitimate financing/timing need;
2. credit is relevant to the goal;
3. repayment capacity exists;
4. alternative funding paths have been considered;
5. financing improves or preserves overall goal feasibility.

However, these may belong partly to downstream **eligibility** rather than applicability.

Therefore we should first test the boundary:

> What makes credit a candidate strategy, and what makes that candidate financially acceptable?

That boundary should be decided through real-life cases before freezing.

---

# 7. Major Current-State Issue: OR Semantics

The current engine effectively evaluates strategy characteristics as:

```text
Goal type matches
AND
ANY configured characteristic matches
→ Applicable
```

This is a major point to document before refactoring.

For example, if a strategy has:

```text
shortfall
near_term
fixed_timeline
```

the current implementation does **not** require all three.

Only one needs to be true.

This may be correct for some strategies and too broad for others.

Therefore:

> **The current OR behavior should be treated as an implementation fact, not as the final business rule.**

---

# 8. Horizon Boundary Gap

The current code defines:

- `near_term` = duration ≤ 5 years
- `long_term` = duration ≥ 7 years

Therefore a goal between **5 and 7 years** does not satisfy either signal.

This creates an explicit unresolved boundary.

Example:

| Goal duration | Current signal |
|---:|---|
| 3 years | near_term |
| 5 years | near_term |
| 5.5 years | neither |
| 6 years | neither |
| 7 years | long_term |
| 10 years | long_term |

### Recommendation

Do not patch this immediately.

Instead, create real-life examples around:

- 4–5 year goals;
- 5–7 year goals;
- 7–10 year goals;
- very long-term goals.

Then decide whether the system should use:

- near / medium / long;
- continuous time bands;
- strategy-specific horizons;
- or another model.

The final boundary should be a canonical business decision, not an incidental coding threshold.

---

# 9. Applicability vs Eligibility

This distinction should be preserved throughout the Decision Engine.

### Applicability asks:

> **Should this strategy even enter the candidate pool?**

### Eligibility asks:

> **Given that it is a candidate, can this strategy actually work under the person's financial conditions?**

Therefore:

```text
Applicable
    ≠
Eligible
    ≠
Selected
```

A strategy can therefore be:

- applicable but fail eligibility;
- applicable and conditionally eligible;
- applicable and fully eligible;
- not applicable and therefore never reach eligibility.

This separation should become part of the canonical Decision Engine contract.

---

# 10. Recommended Target Framework

The recommended target is to separate applicability into explicit gates.

```text
Defined Goal
    ↓
Canonical Goal Type
    ↓
Strategy Goal-Type Gate
    ↓
Strategy Applicability Conditions
    ↓
Applicable Strategy Pool
    ↓
Hard Constraints
    ↓
8 Eligibility Fits
    ↓
Strategy Selection
```

The applicability step itself should eventually be structured as:

### Gate A — Goal-Type Participation

Does this strategy participate in this goal type?

### Gate B — Applicability Conditions

Does the goal/context contain the characteristics that make this strategy relevant?

### Gate C — Applicability Decision

Return:

- applicable;
- not applicable;
- optionally, missing-data/undetermined if the business contract requires it.

The exact conditions are intentionally **not frozen in this document**.

---

# 11. Recommended Rule Ownership

The target architecture should have one canonical owner for strategy applicability.

Recommended future location:

`backend/rules/strategy_applicability.py`

Its responsibility should be to define the business policy.

The execution layer should not independently invent applicability conditions.

### Target responsibility split

| Layer | Responsibility |
|---|---|
| `backend/library/strategies/canonical.py` | Strategy definition and metadata |
| `backend/rules/strategy_applicability.py` | Canonical applicability policy |
| `backend/engines/strategy/applicability.py` | Execute/filter using canonical policy |
| downstream eligibility engine | Determine financial feasibility |
| strategy decision engine | Select among eligible candidates |

This is a target architecture recommendation, not a current-state claim.

---

# 12. Recommended Inputs to Consider

The applicability framework should eventually be able to evaluate, where relevant:

### Goal attributes

- canonical goal type;
- duration / time-to-goal;
- target;
- funding status;
- goal priority;
- timeline flexibility.

### Financial context

- liabilities;
- EMI burden;
- investable surplus;
- existing assets;
- liquidity;
- risk capacity;
- other goal interactions.

### Strategy context

- strategy-specific participation;
- strategy-specific characteristics;
- whether the strategy is primary or supporting;
- dependencies on another strategy.

Not every strategy should necessarily use every input.

The final rule contract should specify exactly which inputs are authoritative for each strategy.

---

# 13. Missing Data Policy — Open Decision

The current implementation does not establish a complete canonical policy for missing applicability inputs.

This needs to be decided later.

Possible outcomes include:

1. **Fail closed** — missing required input means not applicable.
2. **Fail open** — missing input does not prevent candidacy.
3. **Undetermined** — strategy remains unresolved until downstream data is available.

### Recommendation

Do not choose one yet.

Use real-life examples to determine whether missing data can safely produce a strategy candidate or whether it creates an unacceptable false recommendation.

---

# 14. What Should Be Frozen Later

After real-life validation, the following should become explicit canonical rules:

1. strategy participation by goal type;
2. applicability condition vocabulary;
3. AND/OR semantics;
4. horizon definitions;
5. timeline semantics;
6. funding-status semantics;
7. priority semantics;
8. strategy-specific financial-context requirements;
9. missing-data behavior;
10. whether applicability can produce an "undetermined" state;
11. primary vs supporting strategy applicability;
12. exact rule IDs and versioning.

Until then, these remain design questions.

---

# 15. Real-Life Validation Method

Before freezing rules, test the framework against representative cases.

For each case:

| Field | Example |
|---|---|
| Goal | Education |
| Horizon | 6 years |
| Funding status | Shortfall |
| Priority | High |
| Timeline | Fixed |
| Assets | Existing corpus |
| Surplus | Positive |
| Liabilities | Moderate EMI |
| Question | Which strategies should enter the candidate pool? |

Then evaluate:

1. What does current code return?
2. What should a financial planner reasonably consider applicable?
3. Why?
4. Is the difference applicability or eligibility?
5. Does the rule generalise to other goals?
6. Does the rule create false positives/false negatives?

Only after multiple cases agree should the condition be frozen.

---

# 16. Current vs Recommended Summary

| Area | Current implementation | Recommended direction |
|---|---|---|
| Strategy definitions | Centralized in strategy library | Keep |
| Goal-type participation | Stored in strategy definitions | Keep as canonical metadata |
| Applicability evaluation | `StrategyRuleEngine` | Move business policy to canonical rules |
| Signal calculation | Inside engine | Centralize/reuse canonical signal definitions |
| Characteristic semantics | Implicit | Explicit |
| AND/OR behavior | Effectively ANY match | Decide through real-life cases |
| Horizon | ≤5 / ≥7 | Validate and explicitly define |
| Priority | Critical/High → high_priority | Validate role |
| Funding status | shortfall/on-track/overfunded | Validate role |
| Timeline | fixed vs non-fixed | Validate semantics |
| Missing data | Incomplete policy | Define later |
| Applicability vs eligibility | Conceptually separate | Freeze as explicit contract |
| Strategy selection | Downstream | Keep separate |
| Refactor | Not yet | Only after rules are validated |

---

# 17. Decision Status

### Confirmed from current code

- There are five canonical strategies.
- Strategy definitions contain applicable goal types and characteristics.
- Goal type is checked first.
- Current characteristic matching is effectively OR-based.
- Current horizon signals are ≤5 years and ≥7 years.
- Applicability is separated from component activation.
- Applicability is separated conceptually from downstream decision/ranking.

### Recommended, but not yet frozen

- dedicated canonical applicability rule owner;
- explicit applicability gates;
- explicit AND/OR semantics;
- explicit horizon model;
- explicit missing-data behavior;
- explicit boundary between applicability and eligibility;
- real-life scenario validation before rule freezing.

### Not to do yet

- Do not refactor the applicability engine.
- Do not move rules into a new file yet.
- Do not change current strategy behavior.
- Do not freeze thresholds based only on the current implementation.
- Do not treat this document as the final business rulebook.

---

# 18. Next Step

The next activity is **not coding**.

We should now create real-life financial-planning scenarios for the five strategies and use those scenarios to determine:

> **Which conditions genuinely make each strategy applicable?**

Once those cases produce a stable pattern, the applicability rules can be frozen and only then refactored into the canonical Decision Engine rule layer.

**Document status: Analysis complete / Business rules intentionally open.**
