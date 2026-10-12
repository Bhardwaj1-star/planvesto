# Case 11 — Iterative Strategy, Execution and Revalidation

> **Canonical lifecycle alignment — 2026-10-08**
> The iterative loop starts from the Accepted Plan. Execution/What-If → Impact → Targeted Revalidation → Investor Decision → Updated Accepted Plan → Updated Action Plan. Scenarios remain separate until adopted.

> **Core:** Financial State + Investor Intent/Goals → Goal Planning/Feasibility → Strategy Decision → Implementation Design → Stress/Resilience → Decision/Recommendation → Investor Decision → Accepted Plan → Action Plan → Execution.

> **Conditional:** Whole-Plan/Multi-Goal Impact is invoked only when the decision is plan-level.

> **Change loop:** Accepted Plan → Execution/What-If → Impact Analysis → Targeted Revalidation → Investor Decision → Updated Accepted Plan → Updated Action Plan.

> Goal Funding is owned by Goal Planner/Goal Feasibility; it is not a peer Strategy Builder strategy.

## 1. Real-Life Financial Case

The investor is working with the interactive planning environment established in the earlier cases.

The investor may:

1. start with an accepted strategy;
2. test an execution change;
3. discover that the execution change makes the existing strategy less appropriate;
4. review alternative strategies;
5. select a new strategy;
6. modify the execution of the new strategy using their own numbers;
7. review the resulting impact;
8. and continue iterating until an acceptable path is found.

The important point is:

> **Financial planning is not necessarily a one-step decision. It can be an iterative decision process.**

---

## 2. The Investor Can Iterate

The system should not assume that the investor makes one decision and immediately reaches the final plan.

The investor may ask:

> "What happens if I do this?"

Then:

> "What if I do it differently?"

Then:

> "What if I use this alternative strategy?"

Then:

> "What happens if I change the execution of that strategy?"

The system should support this sequence without losing the distinction between:

- strategy;
- execution;
- what-if scenarios;
- accepted decisions;
- and the Action Plan.

---

## 3. Example

Suppose the investor starts with:

**Goal:** Education  
**Strategy:** Goal Funding

The investor tests the current execution.

### Step 1 — Execution Change

The investor reduces the planned monthly contribution.

The system calculates the impact.

The result shows that the goal may no longer be adequately funded.

### Step 2 — Strategy Re-Evaluation

The system identifies that the current strategy/path may no longer be appropriate under the new conditions.

It presents applicable alternatives.

### Step 3 — Investor Selects an Alternative

The investor chooses an alternative strategy.

### Step 4 — New Execution What-If

The investor then changes the execution parameters of the new strategy.

For example:

- contribution amount;
- existing asset deployment;
- timing;
- financing amount;
- or another relevant execution parameter.

### Step 5 — Impact Analysis

The system recalculates:

- goal outcome;
- funding requirement;
- cash-flow impact;
- liquidity;
- other-goal impact;
- and other relevant consequences.

The investor can then accept the revised path or continue experimenting.

---

## 4. Iterative Decision Loop

The conceptual loop is:

**Strategy**

↓

**Execution**

↓

**What-If Change**

↓

**Impact Analysis**

↓

**Strategy Still Appropriate?**

### If Yes

**Revise Execution**

↓

**Investor Decision**

### If No

**Strategy Re-Evaluation**

↓

**Alternative Strategies**

↓

**Investor Choice**

↓

**New Strategy**

↓

**New Execution**

↓

**What-If**

↓

**Impact Analysis**

↓

**Revalidation**

This loop can repeat as necessary.

---

## 5. Current Plan vs Scenario

The system must distinguish between:

### Accepted Plan

The strategy and execution currently accepted by the investor.

and

### Experimental Scenario

A proposed strategy or execution change being evaluated.

A scenario should not automatically overwrite the accepted plan.

The investor may test several alternatives before choosing one.

Therefore:

> **Scenario exploration is separate from plan adoption.**

---

## 6. Investor Choice Remains Central

Even after the system identifies a better or more appropriate path, the investor remains the decision-maker.

The system can say:

> "Under your changed execution, the current strategy is less appropriate."

It can then show alternatives.

The investor may:

- select an alternative;
- retain the existing strategy;
- modify the execution again;
- modify the goal;
- modify the timeline;
- or reject the proposed change.

The system should calculate and explain the consequences of the chosen path.

---

## 7. Multi-Goal Financial Plan

The iterative process also applies to a multi-goal plan.

For example:

- Education → Goal Planner / Feasibility
- Retirement → Progressive De-risking
- Loan → Debt Reduction

The investor changes Education execution.

The system determines that the change affects Retirement feasibility.

The investor may then:

- revise Education execution;
- change Education strategy;
- change Retirement execution;
- change the relevant strategy;
- or modify the overall accepted path.

The system should evaluate the actual dependencies rather than assuming that every change affects every goal.

The resulting accepted strategy set must remain coordinated as one financial plan.

---

## 8. Whole-Plan Revalidation

Each iteration does not necessarily require rebuilding the entire financial plan.

The system should determine:

1. what changed;
2. what is directly affected;
3. what dependencies are affected;
4. whether the impact is material;
5. whether the affected strategy remains appropriate;
6. whether other goals or strategies require revalidation;
7. whether whole-plan validation is required.

This preserves efficiency and prevents unnecessary strategy churn.

---

## 9. What the System Guides

At every iteration, the system's role remains impact guidance.

It should help answer:

- What changed?
- What is the effect?
- Is the goal still feasible?
- Is the current strategy still appropriate?
- What alternatives are available?
- What happens if I choose the alternative?
- What happens to my other goals?
- What happens to liquidity, debt, cash flow, or other relevant financial conditions?
- What would the revised Action Plan look like?

The system should not hide the trade-offs between alternatives.

---

## 10. Investor's Own Numbers

The interactive feature should allow the investor to participate using their own numbers.

For each iteration, the investor can change relevant inputs and observe the resulting impact.

For example:

**Strategy B**

↓

Investor enters:

- ₹X contribution;
- ₹Y existing asset;
- Z-year timeline;
- specified financing amount.

↓

System calculates:

- goal outcome;
- funding gap/surplus;
- liquidity impact;
- whole-plan impact where relevant.

The investor can then decide whether the resulting path is acceptable.

---

## 11. Strategy Builder's Role

Strategy Builder remains responsible for strategic alternatives.

It should not become an unlimited trial-and-error execution engine.

Its role is to answer:

> **"Given the current accepted/selected planning conditions, which strategies are applicable and what are the meaningful alternatives?"**

The execution what-if environment then answers:

> **"What happens if I implement this selected strategy with different numbers or execution choices?"**

If the resulting execution materially changes the strategic problem, Strategy Builder can be invoked again for strategy re-evaluation.

---

## 12. Action Plan

The Action Plan should represent only the currently accepted implementation path.

During experimentation:

> **Do not change the accepted Action Plan.**

After investor adoption:

> **Update the relevant Action Plan.**

If the investor changes strategy and then execution:

- old active actions that are no longer applicable should be revised;
- new active actions should be added;
- completed actions remain historical records.

The Action Plan therefore represents the current accepted implementation state while preserving implementation history.

---

## 13. Example of Multiple Iterations

### Initial

**Strategy:** Goal Funding  
**Execution:** ₹50,000/month

### Iteration 1

Investor changes:

**₹50,000 → ₹40,000**

Result:

Goal becomes underfunded.

### Iteration 2

System identifies that the current path may no longer be appropriate.

Investor reviews alternative strategies.

### Iteration 3

Investor selects an alternative strategy.

### Iteration 4

Investor tests:

**₹40,000 → ₹45,000/month**

Result:

Goal becomes feasible but another goal's surplus reduces.

### Iteration 5

Investor changes another execution parameter.

System recalculates the broader impact.

### Final

Investor accepts the path that provides an acceptable balance between:

- goal feasibility;
- cash flow;
- liquidity;
- other goals;
- risk;
- debt;
- and the investor's own preferences.

Only the final accepted path becomes the active implementation.

---

## 14. Decision Flow

The established conceptual flow is:

**Current Accepted Plan**

↓

**Investor What-If**

↓

**Impact Analysis**

↓

**Strategy Revalidation**

### If current strategy remains appropriate

**Execution Revision**

↓

**Investor Decision**

### If current strategy is no longer appropriate

**Strategy Builder / Alternative Strategy Evaluation**

↓

**Investor Strategy Choice**

↓

**New Strategy**

↓

**New Execution What-If**

↓

**Impact Analysis**

↓

**Revalidation**

↓

**Investor Decision**

↓

**Accepted Plan**

↓

**Action Plan**

This loop may repeat.

---

## 15. Relationship to Cases 8–10

### Case 8 — Strategy Change

The investor changes strategy.

### Case 9 — Execution Change

The investor changes execution while the strategy remains appropriate.

### Case 10 — Execution Change Triggers Strategy Re-Evaluation

The execution change makes the existing strategy potentially inappropriate.

### Case 11 — Iterative Strategy + Execution Revalidation

The investor can move through strategy and execution changes repeatedly until an acceptable path is selected.

Therefore:

> **Cases 8–11 establish an iterative decision environment rather than a one-time recommendation process.**

---

## 16. Established Business Decisions

1. Financial planning can be an iterative decision process.
2. The investor can test multiple strategy and execution alternatives.
3. Strategy and execution remain distinct concepts.
4. Execution changes can trigger strategy re-evaluation.
5. A new strategy can itself be tested through execution what-if scenarios.
6. Scenario experimentation should not automatically overwrite the accepted plan.
7. Investor adoption is required before a scenario becomes the active plan.
8. The system's role is to calculate and explain consequences at each iteration.
9. The investor remains the final decision-maker except where genuine hard constraints apply.
10. Multi-goal plans must evaluate cross-goal impacts where material.
11. Not every iteration requires a complete rebuild of the financial plan.
12. Revalidation should be targeted according to actual dependencies and material impact.
13. The accepted strategy set and accepted execution state should determine the active Action Plan.
14. Completed actions should remain historical records.
15. The exact iteration storage model, scenario history, dependency graph, revalidation triggers, and implementation mechanics remain subject to validation against the existing system.

---

## 17. Final Business Principle

> **The investor should be able to iterate between strategy and execution decisions using their own financial numbers. The system continuously guides the investor by showing the impact of each choice, identifying when re-evaluation is required, and allowing the investor to adopt the path they consider acceptable.**

Therefore:

**Strategy**

→ **Execution**

→ **What-If**

→ **Impact**

→ **Revalidation**

→ **Investor Choice**

→ **Revised Strategy/Execution where required**

→ **Revalidation**

→ **Accepted Plan**

→ **Action Plan**

This creates an interactive financial decision environment rather than a static recommendation engine.

---

## 18. Change Status

**Business concept established through real-life case validation.**

This document records the conceptual decision only.

No implementation changes are made by this document.

The exact scenario-history model, iteration limits, dependency handling, revalidation triggers, comparison mechanics, adoption flow, and implementation architecture remain to be validated against the existing system before implementation is frozen.
