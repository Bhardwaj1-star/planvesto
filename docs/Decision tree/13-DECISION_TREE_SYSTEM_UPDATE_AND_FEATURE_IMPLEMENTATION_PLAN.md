# 13 — Decision Tree System Update & Feature Implementation Plan

**Repository:** `Bhardwaj1-star/planvesto`  
**Scope:** Decision Tree, Goal Planning/Feasibility, Multi-Goal Planning, Strategy Builder, Scenario/What-if, Revalidation, Investor Choice, Action Plan and related feature contracts.  
**Status:** **AUDIT COMPLETE — IMPLEMENTATION PLAN, NOT CODE CHANGES**  
**Evidence rule:** Existing-system findings below are based on the current repository code. The real-world cases are treated as the business-behaviour requirements already established for this project.

---

## 1. Executive Conclusion

The real-world cases are now sufficiently mature to stop expanding the case library.

The next work is **system correction and feature completion**, not another round of conceptual case creation.

The current repository already contains substantial pieces of the intended system:

- canonical strategy library;
- applicability filtering;
- centralized ConstraintSet aggregation;
- eight eligibility fits;
- decision scoring;
- variant selection;
- scenario and what-if generation;
- multi-goal orchestration;
- financial-plan aggregation;
- investor priorities;
- strategy persistence/versioning;
- Action Plan rule helpers;
- adaptation rule helpers.

However, the pieces do not yet form the complete behaviour established by the real-world cases.

The most important gaps are:

1. **Goal feasibility/planning and Strategy Builder responsibilities are still too tightly coupled.**
2. **Multi-goal planning allocates surplus but does not yet produce the full implementation Action Plan required by the cases.**
3. **StrategyEngine performs architecture and technique work before final strategy decision.**
4. **Variant selection is still performed inside recommendation rather than being a clean authoritative stage.**
5. **Eligibility is evaluated through overlapping mechanisms.**
6. **Legacy decision rules/strategy IDs remain in active decision scoring.**
7. **Investor priorities are not yet given a fully explicit authority model.**
8. **Scenario/what-if exists, but adoption, plan preservation and downstream revalidation are not yet a complete lifecycle.**
9. **Financial-state change and goal-intent change do not yet have a complete materiality → targeted revalidation → update workflow.**
10. **Investor rejection / investor-designed strategy / open strategy mode is not yet represented as a complete product capability.**
11. **Action Plan is currently much narrower than the real-world requirement.**
12. **Money Wheel / financial ratios still contain decision-like threshold behaviour that should be separated from planning interpretation.**

Therefore the implementation should be done as a **controlled architecture and feature update**, not as isolated bug fixes.

---

# 2. Business Behaviour Baseline

The accepted real-world cases establish the following system behaviour.

| Requirement | Required behaviour |
|---|---|
| Goal feasibility | Determine whether a goal is feasible using the complete financial state and goal inputs before detailed strategy design. |
| Goal Funding | A funding/feasibility mechanism, not automatically a Strategy Builder strategy. |
| Strategy Builder | Select and compare actual strategies, variants, techniques and architectures after the planning context is established. |
| Better path | If the goal is already feasible, compare the current/appropriate path with a potentially better economic path. |
| Multi-goal planning | Evaluate all accepted goals together when resources compete; do not simply solve goals independently. |
| Action Plan | Convert accepted planning/strategy decisions into concrete implementation actions. |
| Financial-state change | Material changes trigger targeted feasibility recalculation and strategy revalidation; immaterial changes should not cause strategy churn. |
| Goal change | Material goal-input changes trigger recalculation and targeted strategy update. |
| Goal cancellation | Cancel the goal, not the underlying assets; retain and remap assets where appropriate. |
| New goal | First test the new goal against the existing plan as a scenario; investor decides whether to adopt the trade-off. |
| Strategy change | Investor can change strategy after seeing consequences; system explains the impact and revalidates affected areas. |
| Multiple strategies | A complete financial plan may contain multiple coordinated strategies. |
| Execution what-if | Investor can change contribution, timing, lump sum, asset usage, debt execution, etc. without overwriting the accepted plan. |
| Execution-triggered revalidation | If an execution change makes the current strategy inappropriate, trigger targeted strategy re-evaluation. |
| Iterative planning | Investor may move repeatedly between strategy and execution decisions. |
| No acceptable path | System may conclude that no acceptable system-proposed path exists; it must not force a solution. |
| Investor-designed strategy | Investor can design a strategy; system structures, calculates, validates and explains it. |
| Strong economic signals | High debt cost/opportunity cost should inform decisions; not every strong signal is an automatic hard blocker. |
| Hard constraints | Genuine hard constraints may restrict options, but should not be confused with ordinary financial ratios or advisory preferences. |

---

# 3. Current Code Baseline

## 3.1 Strategy Builder already has substantial infrastructure

Current `StrategyEngine.execute()` performs:

**Applicability → baseline scenarios → what-if scenarios → comparison matrix → architecture composition → technique execution → decision → ranking → recommendation**

This is real working structure, but it is not yet the desired clean decision lifecycle.

### Key finding

Architecture and technique execution currently occur before `evaluate_decision()`.

That means downstream implementation structure is being produced before the authoritative strategy decision is complete.

**Change required:** separate candidate evidence generation from authoritative decision selection, then make architecture/technique execution downstream of the selected strategy where possible.

---

# 4. Gap Matrix — Real-World Requirement vs Current System

| Real-World Requirement | Existing Code | Current State | Gap | Required Change | Type | Priority |
|---|---|---|---|---|---|---|
| Goal feasibility before strategy | Goal/financial planning services + DefinedGoal | Partial | Strategy Builder still receives a pre-defined goal but Goal Funding remains represented as a canonical strategy | Establish clear feasibility contract before Strategy Builder | Modify | P0 |
| Goal Funding as feasibility/planning | Goal Funding exists as `strat-goal-funding` with 6 variants | Conflict with business model | Goal Funding is still represented inside Strategy Builder's canonical strategy library | Separate Goal Funding planning from Strategy Builder strategy semantics | Replace / Refactor | P0 |
| Multi-goal feasibility | `MultiGoalOrchestrator`, `ResourceAllocationEngine` | Partial | Allocation exists; full whole-plan action construction does not | Extend multi-goal planning into accepted-plan/action-plan workflow | Modify | P0 |
| Action Plan | `rules/action_plan.py` | Partial | Current helper mainly converts primary/supporting strategies/techniques into generic implementation actions | Build real financial actions: amount, order, timing, source, target, status, dependencies | New / Extend | P0 |
| Strategy selection | `evaluate_decision()` | Working but mixed | Selection depends on legacy rule functions and overlapping eligibility paths | Make one authoritative selection contract | Modify | P0 |
| Eight eligibility fits | `engines/strategy/eligibility.py` | Present | Eight fits and separate eligibility gate overlap | Define one gate ownership model | Modify | P0 |
| Legacy strategy IDs | `rules/strategy_decision.py` | Conflict | Legacy IDs remain in active scoring branches | Replace with canonical strategy IDs and remove stale branches | Remove / Replace | P0 |
| Variant selection | `VariantSelector` called from recommendation | Partial | Variant selection is downstream inside recommendation rather than independent authority | Create authoritative Variant Selection stage | Move / Modify | P1 |
| Better-path comparison | Scenario/comparison infrastructure | Partial | Current scenario model mostly focuses on funding sensitivities | Add explicit current-vs-alternative economic comparison | Extend | P1 |
| Investor priorities | `InvestorPriorities` | Partial | Passed into decision/ranking but exact selection authority remains unclear | Freeze ownership and influence contract | Modify | P0 |
| Multiple strategies | Architecture supports supporting strategies | Partial | Runtime/product-level coordinated multi-strategy plan is not fully established | Add accepted plan containing multiple strategy records | Extend | P1 |
| Investor strategy override | Scenario supports investor-modified scenarios | Partial | No complete accepted override/revalidation lifecycle | Add override → impact → acceptance → revalidation flow | New | P1 |
| New goal against existing plan | Financial plan + multi-goal infrastructure | Partial | No explicit proposal/scenario/adoption lifecycle | Add proposed-goal scenario and adoption state | New | P1 |
| Execution what-if | `generate_what_if_scenarios()`, `create_custom_scenario()` | Present | Simulation exists, but accepted-plan isolation/adoption lifecycle is incomplete | Formalize scenario vs accepted-plan state | Modify | P1 |
| Execution-triggered revalidation | Adaptation helpers exist | Partial | No complete dependency/materiality trigger workflow | Add targeted revalidation service | New | P1 |
| Financial-state adaptation | Financial State and planning services exist | Partial | No complete materiality + revalidation lifecycle | Add change detection/materiality/revalidation orchestration | New | P1 |
| Goal-intent adaptation | DefinedGoal recalculation exists | Partial | No explicit lifecycle for changed/cancelled goal and asset remapping | Add goal-change workflow | New | P1 |
| No acceptable path | Decision can return infeasible | Partial | Infeasible currently means no viable strategy; it does not represent investor rejection/no acceptable plan | Add explicit decision state | New | P1 |
| Investor-designed strategy | No complete open-strategy contract | Missing | System assumes library-driven strategy selection | Add structured investor-designed strategy mode | New | P2 |
| Money Wheel as measurement | Ratio calculations exist | Conflict | Constraint evaluator uses ratio thresholds to alter goal priority | Separate measurement from interpretation/decision | Replace / Refactor | P0 |
| Debt economics | DTI exists | Incomplete | DTI is stronger in current constraint path than loan economics/opportunity cost | Add debt-rate/economic comparison inputs to planning | Extend | P1 |
| Plan preservation | Strategy/financial plan persistence exists | Partial | Scenario and accepted plan lifecycle not fully separated | Introduce explicit accepted-plan vs scenario semantics | Modify | P1 |
| Auditability | Run metadata/audit trail exists | Partial | No complete lifecycle audit for proposal, acceptance, override and revalidation | Extend audit model | P1 |

---

# 5. Highest-Risk Current Conflicts

## 5.1 Goal Funding is still a Strategy Builder strategy

The canonical strategy library contains:

`strat-goal-funding`

with six funding variants.

But the real-world cases establish that Goal Funding is the **planning/feasibility mechanism that determines how a goal can become feasible**.

It should therefore not be treated as equivalent to:

- Debt Reduction
- Progressive De-risking
- Capital Preservation
- Credit Utilisation

### Required architecture

**Financial State + Goals → Goal Feasibility / Funding Paths → Strategy Builder**

Goal Funding outputs should become inputs/evidence for Strategy Builder rather than one of the same-level strategic choices.

This is a **P0 architectural correction**.

---

# 6. Strategy Decision Tree Update

## Current

**Applicability → Scenarios → Architecture → Techniques → Decision → Ranking → Recommendation**

## Target

**Planning / Feasibility → Applicability Gate → Candidate Strategies → 8-Fit Eligibility Gate → Strategy Decision / Ranking → Variant → Technique → Architecture → Stress/Resilience → Recommendation → Accepted Plan → Action Plan**

Important distinction:

- Candidate architecture may be generated as evidence if required.
- But final architecture should not determine the strategy before the strategy decision is authoritative.
- Recommendation should explain the already-made decision, not secretly make additional strategic decisions.

---

# 7. Constraint and Money Wheel Separation

Current `FinancialRatioConstraintEvaluator` turns:

- emergency coverage;
- DTI;
- savings rate;
- leverage

into status and, in critical cases, priority-changing constraints.

The real-world cases require a clearer separation.

### Money Wheel

**Measures.**

Examples:

- Savings Rate
- DTI
- Emergency Coverage
- Leverage
- Weighted Debt Rate
- Investment–Debt Spread

### Planning / Decision Layer

**Interprets those measurements in context.**

For debt, interpretation should consider:

- outstanding principal;
- interest rate;
- tenure;
- EMI;
- monthly surplus;
- goal horizon;
- expected/risk-adjusted investment return;
- liquidity;
- opportunity cost.

Therefore:

> DTI ≠ automatic debt-repayment instruction.

The same principle applies to other ratios.

---

# 8. Multi-Goal Planning Update

Current `MultiGoalOrchestrator` already:

1. evaluates goals;
2. resolves priority;
3. creates allocation items;
4. allocates available monthly surplus;
5. produces goal resolutions;
6. records audit information.

But the current implementation explicitly leaves:

`action_plan=[]`

and comments that executable Action Plan records are owned elsewhere.

This is insufficient for the real-world cases.

### Required output

Multi-goal planning must ultimately be able to produce:

**Feasible Overall Path → Accepted Strategy Set → Implementation Actions**

not merely:

**Funding Allocation → Shortfall**

---

# 9. Action Plan Feature Update

Current Action Plan rules are primarily strategy/technique descriptions.

Real-world Action Plan requirements are broader.

An action should be able to represent:

| Field | Purpose |
|---|---|
| Action | What investor needs to do |
| Reason | Why it is required |
| Goal / Plan scope | What it affects |
| Amount | Financial amount |
| Timing | When it should happen |
| Source | Where money/resource comes from |
| Destination | Where it goes |
| Dependency | What must happen first |
| Status | Proposed / Accepted / Active / Completed / Cancelled |
| Impact | Expected effect |
| Revalidation trigger | What would cause review |

Examples:

- close high-cost debt;
- restructure loan;
- increase monthly contribution;
- deploy lump sum;
- reallocate an existing asset;
- preserve a core asset and finance a timing gap;
- execute a de-risking step;
- redirect surplus after debt closure.

This is a **new feature capability**, not merely a wording change.

---

# 10. Scenario / What-if Lifecycle

Current scenario code already supports:

- contribution sensitivity;
- goal-date sensitivity;
- target sensitivity;
- step-up sensitivity;
- custom investor scenarios;
- deterministic funding calculations;
- trade-off notes;
- constraint violations.

That is valuable and should be retained.

The missing lifecycle is:

**Create Scenario → Calculate Impact → Compare with Accepted Plan → Investor Accepts/Rejects → If Accepted, Update Plan → Revalidate Affected Decisions → Update Action Plan**

A scenario must never silently overwrite the accepted plan.

---

# 11. Revalidation Architecture

The real-world cases require targeted revalidation.

## Trigger types

### A. Financial State change

Examples:

- income;
- expense;
- asset;
- liability;
- liquidity;
- surplus.

Flow:

**Change → Materiality Check → Affected Goals/Strategies → Recalculate → Revalidate → Update only affected plan elements**

### B. Goal change

Flow:

**Goal Input Change → Recalculate Funding/Feasibility → Revalidate Strategy → Update Action Plan**

### C. Execution change

Flow:

**Execution What-if → Impact → Check Strategy Validity → Keep Strategy OR Re-enter Strategy Builder**

### D. New goal

Flow:

**Proposed Goal → Whole-Plan Impact Simulation → Investor Decision → Adopt / Reject**

This should not automatically modify the existing plan.

---

# 12. Investor Decision Authority

The system should not behave as though its recommendation is an irreversible command.

Required states:

1. **System Proposed**
2. **Investor Reviewing**
3. **Investor Accepted**
4. **Investor Modified**
5. **Investor Rejected**
6. **Investor Designed**
7. **Revalidation Required**
8. **Active**
9. **Completed / Superseded**

This state model is required to support Cases 7–12 correctly.

---

# 13. Investor-Designed Strategy / Open Strategy

The current system is predominantly library-driven.

The real-world cases require a controlled open-strategy capability.

Investor can provide an approach that is not an existing canonical strategy.

PlanVesto should then:

1. structure it;
2. identify its components;
3. calculate consequences;
4. validate against hard constraints;
5. compare impact against goals;
6. expose risks/trade-offs;
7. convert accepted decisions into Action Plan.

It should **not invent a fake canonical strategy merely to force the investor into the library**.

---

# 14. Keep / Modify / Replace / Remove / New

## KEEP

- canonical strategy library infrastructure;
- centralized ConstraintSet;
- applicability engine;
- eight-fit framework;
- scenario engine;
- comparison infrastructure;
- ranking infrastructure;
- strategy repository/versioning;
- multi-goal orchestration foundation;
- financial-plan service foundation;
- adaptation helper foundation;
- Action Plan rule foundation.

## MODIFY

- StrategyEngine sequencing;
- decision authority;
- investor-priority ownership;
- eligibility gate ownership;
- variant-selection ownership;
- multi-goal output;
- scenario lifecycle;
- financial-state adaptation;
- goal-change lifecycle;
- Action Plan generation;
- Money Wheel/constraint separation.

## REPLACE

- legacy strategy-ID branches in active decision scoring;
- ratio-driven automatic decision behaviour where ratios are intended to be measurements;
- Goal Funding's current interpretation as a peer Strategy Builder strategy.

## REMOVE

- stale/duplicate strategy IDs from active decision paths;
- any automatic rule that treats a measurement threshold as a universal financial action without contextual economics;
- duplicate decision authority.

## NEW

- Goal Feasibility/Funding contract;
- accepted-plan vs scenario state;
- targeted revalidation engine;
- whole-plan impact simulation;
- new-goal proposal/adoption flow;
- investor strategy override;
- investor-designed strategy mode;
- richer Action Plan model;
- strategy/plan state lifecycle;
- debt economics measurements and contextual interpretation;
- explicit multi-strategy accepted-plan model.

---

# 15. Implementation Sequence

## Phase 0 — Canonical Baseline

Before functional changes:

- remove legacy decision IDs;
- confirm one owner for each rule;
- confirm one eligibility gate;
- define investor-priority authority;
- define Goal Funding ownership;
- define accepted-plan vs scenario semantics.

**Priority: P0**

---

## Phase 1 — Goal Feasibility / Planning Boundary

Create the clean boundary:

**Financial State + Goals → Feasibility / Funding → Planning Path**

Outputs should include:

- funding requirement;
- feasibility;
- funding alternatives;
- constraints;
- resource requirements;
- multi-goal implications.

**Priority: P0**

---

## Phase 2 — Strategy Decision Tree

Refactor runtime toward:

**Applicability → 8 Fits → Decision → Ranking → Variant → Technique → Architecture → Resilience → Recommendation**

Do not delete useful existing calculations; move them to their correct authority.

**Priority: P0**

---

## Phase 3 — Multi-Goal Planning

Upgrade current allocation into:

**Whole-plan feasibility + trade-offs + accepted path**

Do not reduce multi-goal planning to priority ranking alone.

**Priority: P0**

---

## Phase 4 — Action Plan

Build real executable actions from:

- feasibility;
- debt decisions;
- allocation;
- strategy;
- execution;
- investor acceptance.

**Priority: P0**

---

## Phase 5 — Scenario / What-if / Better Path

Formalize:

**Current Plan → Alternative Scenario → Economic Impact → Investor Choice**

Support both:

- goal-level strategy implementation;
- whole-plan impact simulation.

**Priority: P1**

---

## Phase 6 — Revalidation

Add targeted revalidation for:

- financial-state changes;
- goal changes;
- execution changes;
- strategy changes.

Avoid automatic full-plan rebuilding.

**Priority: P1**

---

## Phase 7 — Investor Choice / Open Strategy

Add:

- accept;
- reject;
- modify;
- investor-designed strategy;
- multiple coordinated strategies.

**Priority: P1/P2**

---

## Phase 8 — Frontend Feature Updates

Only after backend contracts stabilize:

- Goal Planner feasibility UI;
- Strategy Builder alternatives;
- current-vs-better-path comparison;
- whole-plan impact;
- scenario what-if;
- investor acceptance;
- Action Plan;
- revalidation notices;
- investor-designed strategy.

**Priority: P1/P2**

---

# 16. Testing Strategy

The 12 real-world cases should become the acceptance-test backbone.

Each case must eventually have:

**Given → When → Expected System Behaviour → Expected Decision State → Expected Action Plan → Expected Revalidation Behaviour**

The most important tests are not merely “API returns 200”.

They must prove:

- the correct layer owns the decision;
- an inappropriate strategy is not selected;
- an investor modification does not overwrite the accepted plan;
- a new goal does not silently sacrifice existing goals;
- cancellation does not delete assets;
- material changes trigger revalidation;
- immaterial changes do not create strategy churn;
- investor rejection is respected;
- multiple strategies can coexist;
- no acceptable path can be represented honestly.

---

# 17. Dependency Order

The implementation must **not** be done in arbitrary file order.

Correct dependency order:

**Canonical ownership**
↓
**Goal feasibility boundary**
↓
**Decision authority**
↓
**Multi-goal planning**
↓
**Scenario / acceptance lifecycle**
↓
**Revalidation**
↓
**Action Plan**
↓
**Investor/open strategy**
↓
**Frontend feature updates**
↓
**End-to-end real-world case tests**

This prevents the system from accumulating another layer of duplicated logic.

---

# 18. What Is Still Not Frozen

The following should be decided during implementation rather than invented now:

- exact scoring weights;
- exact materiality thresholds;
- exact debt-economic formulas;
- exact asset-remapping algorithm;
- exact strategy conflict-resolution algorithm;
- exact whole-plan optimization method;
- exact Open Strategy UI;
- exact persistence schema where current models can be reused;
- exact frontend presentation.

These are implementation decisions that should follow the canonical business behaviour, not precede it.

---

# 19. Final Implementation Principle

The updated system should behave as:

**Financial State**
→ **Goals / Investor Intent**
→ **Feasibility & Whole-Plan Planning**
→ **Candidate Strategies**
→ **Eligibility**
→ **Decision**
→ **Variant**
→ **Technique**
→ **Architecture**
→ **Stress / Resilience**
→ **Recommendation**
→ **Investor Decision**
→ **Accepted Plan**
→ **Action Plan**
→ **Execution / What-if**
→ **Targeted Revalidation**

with the ability to loop back when a material change occurs.

The system must remain investor-controlled:

**PlanVesto recommends, calculates, compares, validates and explains.  
The investor accepts, rejects or modifies.**

---

## 20. Immediate Next Implementation Task

Do **not** start with frontend changes.

First implementation pass should be a **backend canonicalization pass** covering:

1. Goal Funding ownership;
2. legacy strategy IDs;
3. eligibility-gate duplication;
4. investor-priority authority;
5. StrategyEngine ordering;
6. variant-selection authority;
7. Money Wheel measurement vs constraint separation.

Once this foundation is corrected, the remaining feature work can be built without recreating System Drift.
