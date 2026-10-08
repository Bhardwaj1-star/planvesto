# 14 — Real-Life Cases → Simple Canonical System Structure → Decision Tree Alignment

**Parent area:** `docs/Decision tree/`  
**Purpose:** Establish one simple system structure from the real-life financial cases, then align that structure against the existing Decision Tree documentation before any implementation plan is finalized.  
**Status:** **BUSINESS STRUCTURE / ALIGNMENT AUDIT — NOT YET FROZEN**

---

## 1. Why This Document Exists

The Real-Life Decision Cases developed during validation exposed system responsibilities that cannot safely be inferred from the existing Strategy Builder Decision Tree alone.

The existing Decision Tree documents describe the internal Strategy Decision sequence:

> Goal → Goal Classification → Hard Constraint Gate → Strategy Applicability → 8-Fit Eligibility → Strategy Selection → Variant → Technique → Architecture → Stress/Resilience → Final Decision → Recommendation

The real-life cases establish a broader financial-planning lifecycle:

> Financial State + Goals → Goal Feasibility → [when applicable] Whole-Plan / Multi-Goal Impact → Strategy → Execution → What-If → Revalidation → Investor Decision → Action Plan

**Important boundary:** Whole-Plan / Multi-Goal Impact is conditional. It is not a mandatory input to the Strategy Decision Tree for an individual goal. It applies when the planning problem involves multiple goals, an existing accepted plan, a new goal against that plan, or a material cross-goal/resource conflict.

These are not competing flows.

The first is the **Strategy Decision Tree**.

The second is the **complete PlanVesto financial decision lifecycle** around it.

This document creates the missing common structure so that future audits do not repeatedly rediscover the same boundaries.

---

# 2. Simple Canonical System Structure From the Real-Life Cases

The real-life cases establish a **core lifecycle plus conditional branches and loops**. They do not establish one mandatory linear sequence for every decision.

## A. Core planning lifecycle

```text
FINANCIAL STATE
      +
INVESTOR INTENT / GOALS
      ↓
GOAL PLANNING / FEASIBILITY
      ↓
STRATEGY DECISION
      ↓
STRATEGY IMPLEMENTATION DESIGN
      ↓
STRESS / RESILIENCE
      ↓
DECISION / RECOMMENDATION
      ↓
INVESTOR DECISION / ADOPTION
      ↓
ACCEPTED PLAN
      ↓
ACTION PLAN
      ↓
EXECUTION
```

## B. Conditional Whole-Plan / Multi-Goal branch

Whole-Plan / Multi-Goal Impact is **not a mandatory input to every individual-goal Strategy Decision**.

Invoke it when the decision is inherently plan-level, including:
- multiple goals competing for the same resources;
- a new goal proposed against an existing Accepted Plan;
- a material cross-goal change;
- an accepted-plan change whose consequences extend beyond the affected goal.

```text
PROPOSED / CHANGED GOAL OR PLAN
        ↓
GOAL FEASIBILITY
        ↓
WHOLE-PLAN / MULTI-GOAL IMPACT
        ↓
INVESTOR DECISION
   ├── REJECT → EXISTING ACCEPTED PLAN REMAINS
   └── ACCEPT → AFFECTED STRATEGY / IMPLEMENTATION
```

## C. Strategy Decision subsystem

```text
Goal Context + Financial State + Feasibility/Funding Evidence + Constraints
        ↓
Constraint / Safety Evaluation
        ↓
Strategy Applicability
        ↓
Candidate Viability
        ↓
Strategy Selection
        ↓
Variant
        ↓
Technique
        ↓
Method / Policy
        ↓
Architecture / Solution
        ↓
Stress / Resilience
        ↓
Decision Output
```

## D. Iterative adaptation loop

```text
ACCEPTED PLAN
     ↓
EXECUTION / EXECUTION CHANGE / WHAT-IF
     ↓
IMPACT ANALYSIS
     ↓
TARGETED REVALIDATION
     ↓
STILL VALID?
  ├── YES → CONTINUE / UPDATE EXECUTION
  └── NO  → AFFECTED PLANNING / STRATEGY DECISION
                 ↓
          INVESTOR DECISION
                 ↓
          UPDATED ACCEPTED PLAN
                 ↓
          UPDATED ACTION PLAN
```

This is the canonical system structure. Individual real-life cases instantiate different branches of it.


# 3. The Most Important Boundary

The real-life cases establish three different questions.

### Goal Planner / Feasibility

> **WHAT IS FINANCIALLY FEASIBLE?**

It works from the actual Financial State and goals.

It can compare alternative financial paths and determine what conditions make a goal or whole plan feasible.

### Strategy Builder

> **HOW SHOULD A FEASIBLE PATH BE STRUCTURED AND EXECUTED?**

It selects the appropriate strategy and then determines variant, techniques and architecture.

### Action Plan

> **WHAT DOES THE INVESTOR ACTUALLY NEED TO DO?**

It represents the accepted implementation path.

These three responsibilities must not be collapsed.

---

# 4. Goal Funding Boundary

The real-life cases changed the meaning of Goal Funding.

Goal Funding should not be treated simply as:

- SIP;
- Lump Sum;
- Step-up SIP;
- Lump Sum + SIP;
- Existing Assets.

Those are possible funding mechanisms.

The higher-level Goal Funding / Goal Feasibility function is:

```Financial State
      +
Goal
      ↓
Funding Requirement
      ↓
Alternative Feasible Paths
      ↓
Mathematical Comparison
      ↓
Goal Feasibility / Funding Path
```

Therefore:

> **Goal Funding is a Goal Planner / feasibility responsibility, not automatically a peer Strategy Builder strategy.**

The current five canonical Strategy Builder strategies should therefore not be assumed to contain Goal Funding as a normal strategic decision until the ownership is reconciled.

---

# 5. Strategy Builder Decision Structure

Once Goal Planner establishes the relevant feasible financial path, Strategy Builder becomes. If the planning problem is plan-level, Whole-Plan / Multi-Goal Impact is evaluated before the Strategy Decision; it is not a mandatory step for an individual-goal Strategy Decision:

```Feasible Planning Path
        ↓
Strategy Applicability
        ↓
Candidate Strategies
        ↓
Strategy Viability
        ↓
Strategy Selection
        ↓
Variant
        ↓
Techniques
        ↓
Architecture
        ↓
Execution Design
```

The strategy layer should not independently recreate the entire Goal Planner feasibility calculation.

---

# 6. Hard Constraints vs Financial Measurements

The cases also establish a critical boundary.

A financial measurement is not automatically a decision rule.

For example:

> DTI = 37%

is a measurement.

It does not by itself mean:

> repay debt immediately.

The decision requires context:

- goal;
- goal horizon;
- surplus;
- debt rate;
- outstanding principal;
- tenure;
- EMI;
- liquidity;
- required funding;
- opportunity cost;
- competing goals;
- risk capacity.

Therefore:

```Financial State
   ↓
Measurements / Diagnostics
   ↓
Contextual Financial Analysis
   ↓
Hard Constraint only if genuinely non-negotiable
   ↓
Planning / Strategy Decision
```

Money Wheel should therefore remain primarily a **measurement/health view**, while planning engines interpret those measurements in context.

---

# 7. 8-Fit Eligibility: Alignment Decision Required

The existing Decision Tree documentation defines eight eligibility fits:

1. Cash-flow Fit
2. Liquidity Fit
3. Debt Fit
4. Asset Resource Fit
5. Risk Capacity Fit
6. Goal Constraint Fit
7. Multi-goal Conflict Fit
8. Implementation Fit

The real-life cases, however, introduce a stronger architectural question:

> If Financial State already provides the relevant financial components, and hard constraints already handle genuine blockers, should these eight fits remain as a separate decision gate?

At this stage the answer is:

**Do not automatically implement the 8-fit gate as an additional independent layer.**

First determine the ownership of each fit.

A fit may become:

- a hard-constraint input;
- a Goal Planner feasibility input;
- a Strategy Applicability condition;
- a Strategy Selection evidence dimension;
- an implementation-readiness check;
- or a diagnostic/explanation field.

The objective is to avoid evaluating the same business fact twice under different names.

Therefore the existing 8-fit document is **not deleted**, but its role must be reconciled before the Decision Tree is frozen.

---

# 8. Applicability vs Viability vs Selection

The system should maintain three different questions:

### Applicability

> Should this strategy enter the candidate pool?

### Viability

> Given the client's actual financial situation and goal path, can this strategy reasonably work?

### Selection

> Among viable candidates, which path is preferable under the accepted decision policy?

The existing 8-fit layer may currently be doing part of the second question.

The Financial State / Goal Planner may also be doing part of it.

This is precisely where duplication can occur.

The canonical architecture must assign each question one owner.

---

# 9. Better-Path / Alternative Strategy

Case 4 establishes that a goal can already be feasible while the current financial structure may not be optimal.

Therefore the system must distinguish:

### Feasibility

> Can the goal be achieved?

from:

### Better Path

> Can the goal be achieved earlier, more efficiently, with different contributions, different risk, better liquidity, or better whole-plan consequences?

This means Strategy Builder should be capable of comparing meaningful alternatives after feasibility is established.

The comparison must expose trade-offs rather than silently replace the current path.

---

# 10. Multi-Goal Planning

The real-life cases establish two distinct situations. Whole-Plan / Multi-Goal Impact is used only for the plan-level situation; it is not inserted into every individual-goal Strategy Decision.

### Existing multi-goal plan

All goals are already part of the planning problem.

The system should construct a feasible overall path considering:

- all goals;
- resource allocation;
- timing;
- priority;
- conflicts;
- financial state;
- and alternative paths.

### New proposed goal

A new goal should initially be evaluated as a **separate scenario against the existing accepted plan**.

The system should show:

- new goal feasibility;
- incremental funding requirement;
- impact on existing goals;
- financial-state impact;
- alternative paths;
- implementation consequences.

The investor decides whether to adopt the new goal.

Therefore:

> **Proposal ≠ adoption.**

---

# 11. Investor Choice Is a System Layer

The cases establish that PlanVesto is decision support, not an authority that silently changes the investor's plan.

The investor can:

- accept the recommendation;
- reject it;
- choose another strategy;
- change execution;
- change goal inputs;
- test a what-if;
- design their own strategy.

The system should calculate and explain consequences.

Only an accepted change becomes the active plan.

---

# 12. Scenario vs Accepted Plan

The system must maintain a strict separation:

```Accepted Plan
     │
     ├── What-if Scenario A
     ├── What-if Scenario B
     ├── Strategy Alternative
     └── Investor-designed Scenario
              │
              ▼
        Impact Analysis
              │
              ▼
        Investor Decision
              │
        ┌─────┴─────┐
        │           │
      Reject      Accept
        │           │
        ▼           ▼
 Keep Plan      Update Plan
```

A scenario must never silently overwrite the accepted plan.

---

# 13. Execution Change vs Strategy Change

Case 9–11 establish an important revalidation rule.

If the investor changes:

- SIP amount;
- lump sum;
- timing;
- asset use;
- contribution escalation;
- debt execution;

first evaluate it as an **execution change**.

If the change materially affects the strategic problem:

> re-evaluate the current strategy.

Do not automatically rebuild the entire financial plan.

Therefore:

```
Execution Change
      ↓
Impact Analysis
      ↓
Material?
  ├── No → Keep Strategy
  └── Yes → Revalidate Strategy
                 ↓
          If required → Strategy Builder
```

---

# 14. Financial-State Change

Case 5 establishes the same principle for Financial State changes.

Not every change should trigger complete replanning.

Examples:

- income change;
- expense change;
- asset change;
- liability change;
- liquidity change;
- surplus change.

The system should:

1. detect whether the change is material;
2. identify affected goals/strategies;
3. recalculate affected feasibility;
4. revalidate the current strategy;
5. preserve it if still appropriate;
6. generate alternatives only if required;
7. update the accepted plan/action plan only after investor acceptance.

The exact materiality thresholds are not yet frozen.

---

# 15. Goal Change

A material goal change should trigger:

```Goal Change
   ↓
Recalculate Funding Requirement
   ↓
Recalculate Feasibility
   ↓
Re-evaluate Relevant Strategy
   ↓
Re-evaluate Execution
   ↓
Investor Decision
```

Important:

> Changing a goal does not automatically mean the current strategy is invalid.

It means the affected planning path must be revalidated.

Also:

> Cancel Goal ≠ Cancel Asset.

Assets remain in Financial State and can be reassigned/replanned against remaining goals.

---

# 16. Stress / Resilience

Stress is not a second decision engine.

It should test the same accepted/proposed planning path under changed assumptions.

```Base Inputs
   ↓
Base Decision
   ↓
Stress Inputs
   ↓
Same Decision Logic
   ↓
Compare
   ↓
Resilience / Stability
```

A stress result may trigger targeted revalidation of:

- feasibility;
- strategy;
- variant;
- architecture.

Exact stress thresholds and resilience categories remain to be frozen.

---

# 17. No Acceptable Path

The system must support:

> **No acceptable plan under current preferences and constraints.**

This is a valid outcome.

The system must not:

- force a strategy;
- silently sacrifice another goal;
- hide a funding gap;
- change investor priorities without approval;
- invent a recommendation.

It should explain:

- why the objective is currently infeasible or unacceptable;
- which trade-offs were evaluated;
- what would need to change.

---

# 18. Investor-Designed Strategy

The system should also support an open mode:

```Investor Defines Approach
        ↓
PlanVesto Structures It
        ↓
Calculates
        ↓
Validates
        ↓
Explains Consequences
        ↓
Investor Accepts / Modifies / Rejects
        ↓
Action Plan if Accepted
```

The system can provide strong advisory guidance while preserving investor choice.

Genuine hard constraints still apply.

Strong economic priorities do not automatically become prohibitions.

---

# 19. Action Plan

The Action Plan is not merely a recommendation narrative.

It is the implementation state of the accepted plan.

It should contain:

- active actions;
- future actions;
- completed actions;
- dependencies;
- amounts/timing where applicable;
- revisions after accepted plan changes.

Its lifecycle is:

```Accepted Strategy + Accepted Execution
                 ↓
              Action Plan
                 ↓
       Execute / Complete Actions
                 ↓
             History
```

When the accepted strategy changes, future/active actions are updated while completed actions remain historical.

---

# 20. Monitoring / Adaptation

The complete system is therefore iterative:

```CURRENT ACCEPTED PLAN
        ↓
MONITOR
        ↓
Change detected / Investor proposes change
        ↓
IMPACT ANALYSIS
        ↓
TARGETED REVALIDATION
        ↓
Investor Decision
        ↓
ACCEPTED PLAN UPDATE
        ↓
ACTION PLAN UPDATE
```

This loop is the outer lifecycle around the Strategy Decision Tree.

---

# 21. Alignment With Existing Decision Tree Documents

The existing Decision Tree documents are valuable and should remain the **internal Strategy Decision reference**, but they do not by themselves cover the complete real-life planning lifecycle.

| Real-life system responsibility | Existing Decision Tree coverage | Alignment |
|---|---|---|
| Financial State as core input | Partial | Needs explicit upstream boundary |
| Goal Planner / feasibility | Partial / outside Strategy Decision Tree | Needs explicit boundary |
| Goal Funding as feasibility function | Conflicts with current Strategy Builder strategy list | **Needs correction** |
| Opportunity-cost comparison | Partial | Needs explicit ownership |
| Whole-plan / multi-goal impact | Partial | Needs outer planning layer |
| Hard constraints | Strongly documented | Keep, but preserve diagnostic vs constraint boundary |
| Strategy applicability | Strongly documented | Keep |
| 8-fit eligibility | Documented | **Role must be revalidated before retaining as separate gate** |
| Strategy selection | Documented | Keep as Strategy Builder decision |
| Variant selection | Documented | Keep |
| Technique selection | Documented | Keep |
| Architecture | Documented | Keep |
| Stress/resilience | Documented but incomplete | Keep as replay/revalidation layer |
| Final decision | Documented | Keep as decision contract |
| Recommendation | Documented | Keep downstream |
| Better-path alternatives | Partial | Extend into strategy/impact layer |
| Investor acceptance | Not sufficiently represented | **New outer lifecycle layer** |
| Scenario vs accepted plan | Partial | **Needs explicit lifecycle** |
| Execution what-if | Not part of Steps 1–9 core | **New impact layer** |
| Strategy revalidation | Partial | **Needs explicit lifecycle** |
| Financial-state adaptation | Partial | **Needs explicit lifecycle** |
| Goal-intent adaptation | Partial | **Needs explicit lifecycle** |
| New-goal proposal/adoption | Partial | **Needs explicit lifecycle** |
| No acceptable path | Partial | **Needs explicit outcome** |
| Investor-designed strategy | Not represented as a first-class mode | **New capability** |
| Action Plan | Not a Decision Tree stage | **Separate implementation layer** |
| Monitoring/adaptation loop | Not a Decision Tree stage | **Outer lifecycle** |

---

# 22. What the Existing Decision Tree Should Become

The existing nine Decision Tree audit documents become the **Strategy Decision subsystem** inside the broader financial decision system.

```text
PLANVESTO FINANCIAL DECISION SYSTEM

1. Financial State
2. Investor Intent / Goals
3. Goal Planning / Feasibility
4. [Conditional] Whole-Plan / Multi-Goal Impact
5. Strategy Decision Engine
   ├─ Constraint / Safety Evaluation
   ├─ Applicability
   ├─ Candidate Viability
   ├─ Strategy Selection
   ├─ Variant
   ├─ Technique
   ├─ Method / Policy
   ├─ Architecture / Solution
   └─ Stress / Resilience
6. Decision / Recommendation
7. Investor Decision / Adoption
8. Accepted Plan
9. Action Plan
10. Execution
11. Monitoring / Adaptation
12. Targeted Revalidation / Iteration
```

The Strategy Decision Engine must not absorb Goal Feasibility, investor adoption, or Action Plan ownership.


# 23. Where the 8 Fits Should Sit After Reconciliation

The existing documentation currently places:

```
Hard Constraints
   ↓
8-Fit Eligibility
   ↓
Strategy Selection
```

The real-life cases suggest that this may be unnecessarily repetitive if the eight fits are simply restating information already available from:

- Financial State;
- Goal Feasibility;
- Whole-Plan Impact;
- Hard Constraints;
- Strategy Applicability.

Therefore the correct next step is **not** to automatically preserve the 8-fit gate.

Instead:

```
Financial State
     +
Goal Feasibility
     +
[When applicable] Whole-Plan / Multi-Goal Impact
     +
Hard Constraints
     +
Strategy Applicability
          ↓
Strategy Viability Evidence
          ↓
Strategy Selection
```

Then map each of the eight existing fit concepts into that structure.

Some may remain useful as evidence.

Some may merge into existing gates.

Some may become selection factors.

Some may become diagnostics.

Only after this mapping should a separate 8-fit gate be retained or removed.

---

# 24. Canonical Decision Ownership

The broader system should have one owner for each question.

| Question | Canonical owner |
|---|---|
| What is the client's current financial reality? | Financial State |
| Is the goal financially feasible? | Goal Planner / Feasibility |
| What funding paths can make it feasible? | Goal Planner / Feasibility |
| What happens to the whole plan? | Whole-Plan / Multi-Goal Impact |
| What is genuinely non-negotiable? | Hard Constraint Policy |
| Which strategies can enter consideration? | Strategy Applicability |
| Can a strategy work in this context? | Strategy Viability / reconciled eligibility evidence |
| Which strategy is preferable? | Strategy Selection |
| Which variant? | Variant Selection |
| Which techniques? | Technique Selection |
| How are they assembled? | Architecture |
| Does it survive stress? | Stress / Resilience |
| What is the final system decision? | Decision Engine |
| How is it explained? | Recommendation |
| What happens if I change execution? | Impact / What-If Engine |
| Should current strategy be reconsidered? | Revalidation |
| What did investor accept? | Plan / Adoption layer |
| What must investor do? | Action Plan |
| What changed later? | Monitoring / Adaptation |
| What if investor designs their own approach? | Open Strategy / Impact Engine |

---

# 25. Real-Life Cases Mapped to the System

| Case | Primary system responsibility |
|---|---|
| Case 1 — Debt vs retirement opportunity cost | Goal feasibility + opportunity-cost analysis |
| Case 2 — Education feasibility then execution | Goal Planner → Strategy Builder boundary |
| Case 3 — Multi-goal feasibility | Whole-plan / multi-goal planning |
| Case 4 — Better path | Strategy alternatives + impact comparison |
| Case 5 — Financial-state change | Monitoring + targeted revalidation |
| Case 6 — Goal change/cancellation | Goal re-planning + targeted revalidation |
| Case 7 — New goal proposal | Scenario + whole-plan impact + investor adoption |
| Case 8 — Strategy change | Strategy selection + investor adoption |
| Case 9 — Execution what-if | Impact engine |
| Case 10 — Execution triggers strategy re-evaluation | Impact → revalidation → Strategy Builder |
| Case 11 — Iterative strategy/execution | Full iterative lifecycle |
| Case 12 — No acceptable path / investor-designed strategy | Outcome + Open Strategy mode |

This mapping prevents the cases from being treated as isolated features.

---

# 26. What We Must NOT Do Yet

Before implementation:

1. Do not blindly implement the existing 8-fit gate.
2. Do not treat Goal Funding as a normal Strategy Builder strategy without resolving ownership.
3. Do not move DTI/financial-health measurements directly into hard constraints without contextual policy.
4. Do not build a second decision engine for stress.
5. Do not let Recommendation make new decisions.
6. Do not let scenarios overwrite the accepted plan.
7. Do not make every financial-state change trigger full replanning.
8. Do not automatically replace an existing strategy after a goal/execution change.
9. Do not force an investor into a system-generated strategy.
10. Do not implement all real-life cases as independent feature silos.

---

# 27. The Correct Next Comparison

The next audit should compare **three layers**, not two:

```
REAL-LIFE BUSINESS CASES
          ↓
SIMPLE CANONICAL SYSTEM STRUCTURE
          ↓
EXISTING DECISION TREE DOCUMENTATION
          ↓
CURRENT CODE IMPLEMENTATION
```

For every system responsibility, record:

| Responsibility | Real-life requirement | Canonical system layer | Existing Decision Tree document | Current code | Status |
|---|---|---|---|---|---|

Possible status values:

- **Aligned**
- **Partially aligned**
- **Overlapping**
- **Missing**
- **Contradictory**
- **Needs business decision**

This is the comparison that should drive the implementation plan.

---

# 28. Final Structural Principle

> **PlanVesto is a financial decision system, not merely a Strategy Builder.**

The canonical lifecycle is:

**Financial State + Investor Intent/Goals**
→ **Goal Planning / Feasibility**
→ **[when applicable] Whole-Plan / Multi-Goal Impact**
→ **Strategy Decision**
→ **Implementation Design**
→ **Stress / Resilience**
→ **Decision / Recommendation**
→ **Investor Decision / Adoption**
→ **Accepted Plan**
→ **Action Plan**
→ **Execution**

And the controlled change loop is:

**Accepted Plan → Execution / What-If → Impact Analysis → Targeted Revalidation → Investor Decision → Updated Accepted Plan → Updated Action Plan**

This structure replaces any earlier representation that treated Strategy, Execution, What-If, Revalidation and Investor Decision as one undifferentiated straight line.


# 29. Product Management Guardrails

The canonical structure must be governed by the following product rules:

1. **One business rule → one canonical owner.** The same decision must not be independently made by multiple layers.
2. **Financial State represents financial reality.** It should not silently become the Strategy Decision Engine.
3. **Goal Planner owns goal feasibility and funding-path analysis.**
4. **Goal Funding is a Goal Planner / feasibility responsibility, not a fifth peer Strategy Builder strategy.**
5. **Strategy Builder consumes the established planning context; it must not recreate Goal Planner feasibility independently.**
6. **Applicability, viability and selection remain distinct questions.**
7. **A measurement is not automatically a decision rule.** Ratios and health indicators require contextual interpretation.
8. **The 8-Fit framework must be reconciled before it is retained as an independent gate.**
9. **Scenario / What-If is not the accepted plan.** A scenario must never silently overwrite the active plan.
10. **Investor acceptance is required before a proposed change becomes the active plan.**
11. **Material changes trigger targeted revalidation, not automatic full replanning.**
12. **Stress / resilience replays the same decision logic under changed assumptions; it is not a second decision engine.**
13. **No Acceptable Path is a valid outcome.** The system must not force a recommendation.
14. **Investor-designed strategies are supported and evaluated rather than artificially converted into a library strategy.**
15. **Action Plan is downstream of the accepted plan.**
16. **Monitoring feeds controlled revalidation and adaptation.**
17. **Recommendation explains the decision; it must not become a hidden second decision-maker.**
18. **Completed actions remain historical when future/active actions are revised.**

---

# 30. Canonical Product Ownership Map

| Product question | Canonical owner | Primary output |
|---|---|---|
| What is the investor's current financial reality? | Financial State | Financial reality |
| What does the investor want? | Goal Planner / Goal Context | Goal context |
| Is the goal/path feasible? | Goal Planner / Feasibility | Feasibility result |
| Which funding paths are feasible? | Goal Planner / Feasibility | Funding paths |
| What happens to all goals together? | Whole-Plan / Multi-Goal Impact | Whole-plan impact |
| What is genuinely non-negotiable? | Hard Constraint Policy | Constraint result |
| Which strategies can be considered? | Strategy Applicability | Candidate pool |
| Can a candidate work here? | Strategy Viability / eligibility evidence | Viability evidence |
| Which strategy is preferable? | Strategy Selection | Selected strategy |
| Which variant applies? | Variant Selection | Selected variant |
| Which techniques are needed? | Technique Selection | Technique set |
| How are techniques assembled? | Architecture | Implementation architecture |
| Does the plan survive changed assumptions? | Stress / Resilience | Resilience result |
| What happens under a proposed change? | Impact / What-If | Scenario impact |
| Does the current decision still hold? | Revalidation | Revalidation result |
| What did the investor accept? | Plan / Adoption | Accepted plan |
| What must be executed? | Action Plan | Actions |
| What changed later? | Monitoring / Adaptation | Change trigger |
| What if the investor proposes their own strategy? | Open Strategy / Impact | Evaluated investor strategy |

This ownership map is the product-level contract. Lower-level documents may describe implementation detail, but they must not create competing business ownership.

---

# 31. Relationship to the Strategy Decision Tree

This document defines the broader PlanVesto financial decision system.

The separate strategy-decision-tree.md defines the Strategy Decision subsystem in detail, including:

- the four canonical Strategy Builder strategies;
- strategy applicability;
- strategy viability;
- strategy selection;
- variants;
- techniques;
- technique conditions;
- hard rejection rules;
- goal-specific strategy situations;
- decision output.

Therefore:

```
PlanVesto Financial Decision System
        │
        ├── Financial State
        ├── Goal Planning / Feasibility
        ├── Whole-Plan Impact
        │
        └── Strategy Decision Subsystem
              ├── Applicability
              ├── Viability
              ├── Selection
              ├── Variant
              ├── Technique
              ├── Architecture
              └── Stress / Resilience
```

The two documents are complementary, not competing.

The implementation plan in 13-DECISION_TREE_SYSTEM_UPDATE_AND_FEATURE_IMPLEMENTATION_PLAN.md is the separate execution roadmap for bringing the repository toward this canonical product structure.

---

# 32. Canonical Product Principle

PlanVesto should be treated as a **financial decision system**.

Its core lifecycle is:

**Financial Reality**
→ **Goal Planning / Feasibility**
→ **[conditional] Whole-Plan / Multi-Goal Impact**
→ **Strategy Decision**
→ **Implementation Design**
→ **Stress / Resilience**
→ **Decision / Recommendation**
→ **Investor Decision / Adoption**
→ **Accepted Plan**
→ **Action Plan**
→ **Execution**

When circumstances or execution change:

**Accepted Plan → Impact / What-If → Targeted Revalidation → Investor Decision → Updated Accepted Plan → Updated Action Plan**

Whole-Plan analysis is invoked only when the decision is plan-level. It is not a hidden mandatory gate inside every individual-goal Strategy Decision.

**Goal Funding belongs to Goal Planner / Goal Feasibility. It is not a fifth peer Strategy Builder strategy.**

This document is the consolidated canonical business/product reference for the Real-Life Decision Cases.
