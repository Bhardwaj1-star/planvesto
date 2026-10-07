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

> Financial State + Goals → Feasibility → Whole-Plan Impact → Strategy → Execution → What-If → Revalidation → Investor Decision → Action Plan

These are not competing flows.

The first is the **Strategy Decision Tree**.

The second is the **complete PlanVesto financial decision lifecycle** around it.

This document creates the missing common structure so that future audits do not repeatedly rediscover the same boundaries.

---

# 2. Simple Canonical System Structure From the Real-Life Cases

The complete system should be understood in the following layers.

```text
A. INPUT / CURRENT FINANCIAL REALITY
        │
        ├── Financial State
        │     ├── Income
        │     ├── Expenses
        │     ├── Assets
        │     ├── Liabilities
        │     └── Insurance / related state
        │
        ├── Goals
        ├── Investor Preferences / Priorities
        └── Existing Accepted Plan
                │
                ▼
B. GOAL PLANNING / FEASIBILITY
        │
        ├── Goal validity
        ├── Funding requirement
        ├── Goal feasibility
        ├── Required return / funding gap
        ├── Available resources
        ├── Goal horizon / timing
        ├── Debt economics
        ├── Liquidity implications
        ├── Opportunity-cost comparison
        └── Alternative feasible paths
                │
                ▼
C. WHOLE-PLAN / MULTI-GOAL IMPACT
        │
        ├── Existing goals
        ├── New / changed goal
        ├── Resource allocation
        ├── Cross-goal conflicts
        ├── Cash-flow impact
        ├── Liquidity impact
        └── Impact on accepted plan
                │
                ▼
D. HARD CONSTRAINT / SAFETY GATE
        │
        ├── Genuine hard constraints
        ├── Goal validity constraints
        ├── Non-negotiable safety conditions
        └── Constraint conflicts / governance
                │
                ▼
E. STRATEGY DECISION
        │
        ├── Strategy Applicability
        ├── Candidate Strategies
        ├── Strategy Viability Evidence
        ├── Strategy Selection
        ├── Alternative Strategy / Better Path
        └── Investor priorities / trade-offs
                │
                ▼
F. STRATEGY IMPLEMENTATION DESIGN
        │
        ├── Variant
        ├── Techniques
        ├── Architecture
        └── Detailed execution structure
                │
                ▼
G. IMPACT / STRESS / WHAT-IF
        │
        ├── Execution what-if
        ├── Strategy what-if
        ├── Goal-change scenario
        ├── New-goal scenario
        ├── Financial-state-change scenario
        └── Stress / resilience
                │
                ▼
H. REVALIDATION
        │
        ├── Did the change materially affect the plan?
        ├── Is current strategy still appropriate?
        ├── Is variant still appropriate?
        ├── Is architecture still appropriate?
        └── Targeted re-selection where required
                │
                ▼
I. INVESTOR DECISION / ADOPTION
        │
        ├── Accept proposed path
        ├── Reject proposed path
        ├── Modify inputs
        ├── Select another strategy
        └── Design own strategy
                │
                ▼
J. ACCEPTED PLAN
        │
        ├── Accepted strategy set
        ├── Accepted execution state
        └── Accepted assumptions
                │
                ▼
K. ACTION PLAN
        │
        ├── Active actions
        ├── Future actions
        ├── Completed actions / history
        └── Revisions after accepted changes
                │
                ▼
L. MONITOR / ADAPT
        │
        ├── Material financial-state change
        ├── Goal change
        ├── Execution change
        ├── New goal proposal
        └── Re-enter affected planning/decision layers
```

This is the **system-level structure**.

The Strategy Builder Decision Tree is only one part of it.

---

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

Once Goal Planner establishes the relevant feasible financial path, Strategy Builder becomes:

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

The real-life cases establish two distinct situations.

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

The existing nine Decision Tree documents should not be discarded.

They should become the **Strategy Decision subsystem** inside the broader system.

The resulting hierarchy is:

```PLANVESTO FINANCIAL DECISION SYSTEM
│
├── 1. Financial State
│
├── 2. Goal Planning / Feasibility
│
├── 3. Whole-Plan / Multi-Goal Impact
│
├── 4. Strategy Decision Engine
│     ├── Applicability
│     ├── Constraint Gate
│     ├── Candidate Viability
│     ├── Strategy Selection
│     ├── Variant
│     ├── Technique
│     ├── Architecture
│     └── Stress / Resilience
│
├── 5. Implementation / Impact Engine
│     ├── Execution What-If
│     ├── Strategy What-If
│     └── Whole-Plan Impact
│
├── 6. Investor Decision / Adoption
│
├── 7. Accepted Plan
│
├── 8. Action Plan
│
└── 9. Monitoring / Adaptation
```

This is the **simple system structure** that should be used as the reference for the next comparison.

---

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

The most important conclusion from the real-life cases is:

> **PlanVesto is not only a Strategy Builder. It is a financial decision system in which Goal Planning, Strategy Decision, Impact Analysis, Investor Choice, Action Planning and Adaptation form one connected lifecycle.**

The Strategy Decision Tree remains important, but it should sit inside this broader lifecycle.

The system should therefore be understood as:

**Financial Reality**

→ **Goal / Whole-Plan Feasibility**

→ **Strategy Decision**

→ **Implementation Design**

→ **Impact / What-If**

→ **Revalidation**

→ **Investor Choice**

→ **Accepted Plan**

→ **Action Plan**

→ **Monitoring / Adaptation**

This structure is the baseline against which the existing Decision Tree documentation and then the implementation should be reconciled.

---

## Status

**Real-life system structure: established for alignment purposes.**

**Existing Decision Tree: retained as the Strategy Decision subsystem.**

**8-fit gate: role requires reconciliation before implementation.**

**Goal Funding ownership: requires reconciliation before implementation.**

**Implementation plan: should be regenerated only after the three-layer comparison is complete.**
