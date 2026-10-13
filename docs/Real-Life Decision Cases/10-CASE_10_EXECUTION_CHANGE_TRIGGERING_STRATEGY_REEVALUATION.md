# Case 10 — Execution Change Triggering Strategy Re-evaluation

> **Canonical lifecycle alignment — 2026-10-08**
> Execution change first triggers Impact Analysis and targeted Strategy Revalidation. It does not automatically imply strategy replacement.

> **Core:** Financial State + Investor Intent/Goals → Goal Planning/Feasibility → Strategy Decision → Implementation Design → Stress/Resilience → Decision/Recommendation → Investor Decision → Accepted Plan → Action Plan → Execution.

> **Conditional:** Whole-Plan/Multi-Goal Impact is invoked only when the decision is plan-level.

> **Change loop:** Accepted Plan → Execution/What-If → Impact Analysis → Targeted Revalidation → Investor Decision → Updated Accepted Plan → Updated Action Plan.

> Goal Funding is owned by Goal Planner/Goal Feasibility; it is not a peer Strategy Builder strategy.

## 1. Real-Life Financial Case

The investor has an accepted strategy and an active Execution Plan.

The investor then changes an execution parameter through the interactive what-if experience.

Initially, the change may appear to be only an execution change.

However, the resulting impact may be significant enough that the existing strategy is no longer appropriate for the investor's updated situation.

The key question is:

> **"If I change my execution plan, does the existing strategy still remain appropriate?"**

This creates an important boundary between execution guidance and strategy selection.

---

## 2. Execution Change Does Not Automatically Mean Strategy Change

Case 9 established that an investor can change execution while keeping the same strategy.

Therefore, the system should first test whether the existing strategy remains appropriate.

The conceptual flow is:

**Execution Change**

↓

**What-If Impact Analysis**

↓

**Strategy Still Appropriate?**

### If Yes

The investor can continue with the same strategy and update the Execution Plan.

### If No

The system must first recalculate Goal Planner feasibility/funding consequences. It should re-evaluate a canonical Strategy Builder decision only if the changed funding/execution conditions materially affect that strategy's applicability, viability, constraints, or outcome. It must not silently replace an accepted strategy.

---

## 3. Example

Suppose the investor has:

**Goal Planner funding path:** existing asset + monthly contribution

with an accepted implementation based on:

- existing asset utilisation;
- monthly contribution;
- target amount;
- target timeline.

The investor tests a major execution change.

For example:

> "I do not want to use the existing asset anymore."

The system recalculates the goal.

The result may show:

- required monthly contribution increases;
- funding gap appears;
- goal timeline changes;
- available surplus becomes insufficient;
- another goal is affected;
- or the existing Goal Planner funding path is no longer feasible or appropriate.

At that point, the system should not simply accept the execution change as though nothing else changed.

It should say, in effect:

> **"With this execution change, the current strategy/path may no longer be appropriate. These alternative strategies are available for consideration."**

---

## 4. System's Role

The system remains a guidance and advisory system.

Therefore, it can identify:

- that a current canonical strategy, if affected, has become less suitable;
- why it has become less suitable;
- what financial consequences resulted from the execution change;
- and what alternative strategies may address the new situation.

But the system should not automatically impose the new strategy.

The investor remains the decision-maker.

The system guides:

> **"Your execution change has changed the financial conditions. Because of that, the current strategy is no longer the strongest/appropriate path. Here are the alternatives and their consequences."**

The investor then chooses.

---

## 5. Strategy Re-Evaluation Is Different From Automatic Strategy Replacement

This distinction is critical.

### Wrong approach

**Execution Change**

↓

System automatically replaces Strategy A with Strategy B.

### Correct approach

**Execution Change**

↓

**Impact Analysis**

↓

**Current Strategy Re-evaluation**

↓

If inappropriate:

**Alternative Strategy Options**

↓

**Investor Decision**

↓

**Accepted Strategy**

↓

**Updated Execution Plan**

↓

**Updated Action Plan**

The system identifies the need for re-evaluation; the investor decides the resulting strategy.

---

## 6. Example — Goal Planner Funding-Path Change

Suppose:

- Goal = ₹50 lakh
- Horizon = 8 years
- Current Goal Planner funding path = existing asset + monthly contribution.

Investor changes execution:

> Existing asset will no longer be used.

The system recalculates.

Possible result:

- required contribution becomes materially higher;
- available surplus is insufficient;
- goal feasibility changes;
- another goal becomes constrained.

Goal Planner first recalculates feasibility and funding consequences. Strategy Builder then re-evaluates the relevant canonical strategy decision only if the change materially affects its applicability, viability, constraints, or outcome.

If not, it can present alternatives such as:

- another Goal Planner funding path, if available and feasible;
- Progressive De-risking where relevant;
- Capital Preservation where capital protection becomes important;
- Credit Utilisation where an appropriate timing/funding gap exists;
- or another applicable strategy.

The exact alternatives depend on the investor's actual situation and eligibility.

---

## 7. Example — Debt Reduction

Suppose the selected strategy is:

**Debt Reduction**

The investor tests a major execution change:

> "I will not make the planned lump-sum prepayment."

The system recalculates:

- outstanding principal;
- interest cost;
- repayment timeline;
- released cash flow;
- goal funding;
- liquidity;
- and other financial consequences.

If the change makes the original Debt Reduction path materially less appropriate, the system should trigger strategy re-evaluation.

The investor can then consider an alternative path.

Again:

> **The system should identify and explain the consequence; the investor chooses.**

---

## 8. Strategy Re-Evaluation Should Be Targeted

A change in one execution parameter does not automatically require the entire financial plan to be rebuilt.

The system should first determine:

1. what changed;
2. which goal is affected;
3. which strategy is affected;
4. which dependencies are affected;
5. whether the change is material;
6. whether the current strategy remains appropriate;
7. whether other strategies are affected.

Only where the change has material broader consequences should whole-plan validation be expanded.

This prevents unnecessary strategy churn.

---

## 9. Multi-Goal Financial Plan

In a multi-goal plan, a strategy re-evaluation for one goal does not automatically invalidate strategies for every other goal.

Example:

**Existing plan**

- Education → Goal Planner / Feasibility
- Retirement → Progressive De-risking
- Loan → Debt Reduction

Investor changes Education execution.

The system should first determine whether:

- only Education strategy is affected;
- Education execution affects Retirement feasibility;
- debt strategy is affected;
- or the complete financial plan needs broader validation.

Possible result:

**Education strategy changes**

while:

**Retirement strategy remains unchanged**

and:

**Debt Reduction remains unchanged.**

Alternatively, a material change may affect multiple strategies.

The system should calculate the actual impact rather than assuming either outcome.

---

## 10. Strategy Alternatives

When re-evaluation is triggered, the system should use the Strategy Builder's existing decision framework.

The relevant strategy alternatives should be:

- applicable to the investor's situation;
- evaluated against the relevant constraints;
- assessed for applicability and viability against the relevant hard constraints;
- and compared on the relevant financial outcomes.

For each Strategy Builder decision, present exactly two options from the four canonical strategies. Do not use Scoring or the 8 Eligibility Fits. A funding-path change by itself is not a Strategy change; Goal Planner recalculates the funding path first, and Strategy Builder re-evaluates only where the strategy decision is materially affected.

It should not simply display every strategy in the library.

---

## 11. Investor Choice

After re-evaluation, the investor may:

### Option A — Keep the Existing Strategy

The investor may decide that the trade-offs are acceptable.

The system should then retain the strategy and update the execution plan.

### Option B — Select an Alternative Strategy

The investor chooses one of the alternatives.

The system then updates:

- strategy;
- execution;
- implementation;
- and Action Plan as required.

### Option C — Change the Execution Again

The investor may modify another execution parameter and run another what-if scenario.

This creates an iterative decision process.

The investor can participate until they find an acceptable path.

---

## 12. Interactive Decision Environment

Case 10 extends the interactive model established in Cases 7–9.

The investor can move through:

**Current Plan**

↓

**Execution What-If**

↓

**Impact**

↓

**Strategy Re-Evaluation if Required**

↓

**Alternative Strategy**

↓

**Alternative Execution**

↓

**Impact**

↓

**Investor Choice**

This is not a one-shot recommendation.

It is an interactive planning and decision environment.

---

## 13. Action Plan

The Action Plan should always reflect the **accepted** path.

If the investor only experiments:

> Existing Action Plan remains unchanged.

If the investor accepts an execution change but keeps the same strategy:

> Update relevant Execution Plan and Action Plan items.

If the investor accepts a new strategy:

> Update strategy, execution, and affected Action Plan items.

Completed actions should remain historical records.

Only active/future actions should be revised where relevant.

---

## 14. Relationship to Earlier Cases

### Case 8 — Investor Strategy Change

The investor intentionally changes the strategy.

**Trigger:** strategy choice.

**Response:** trade-off analysis → investor decision.

### Case 9 — Execution Plan What-If

The investor changes execution while expecting the strategy to remain unchanged.

**Trigger:** execution choice.

**Response:** impact analysis → investor decision.

### Case 10 — Execution Change Triggers Strategy Re-Evaluation

The investor changes execution.

The resulting impact makes the current strategy potentially inappropriate.

**Trigger:** execution change.

**Response:** impact analysis → strategy re-evaluation → alternative strategies → investor decision.

Therefore the three cases form a progression:

**Strategy Change**

→ Case 8

**Execution Change**

→ Case 9

**Execution Change → Strategy Re-Evaluation**

→ Case 10

---

## 15. Decision Flow

The established conceptual flow is:

**Accepted Strategy**

↓

**Accepted Execution Plan**

↓

**Investor Changes Execution**

↓

**What-If Scenario**

↓

**Impact Analysis**

↓

**Current Strategy Re-Evaluation**

### If still appropriate

**Same Strategy**

↓

**Updated Execution**

↓

**Updated Action Plan**

### If no longer appropriate

**Alternative Strategy Evaluation**

↓

**Investor Decision**

### If investor keeps existing strategy

**Existing Strategy**

↓

**Updated Execution**

↓

**Updated Action Plan**

### If investor selects alternative

**New Accepted Strategy**

↓

**New Execution**

↓

**Updated Action Plan**

↓

**Investor Execution**

---

## 16. Established Business Decisions

1. An execution change should first be evaluated as an execution change.
2. An execution change does not automatically imply a strategy change.
3. The system should test whether the existing strategy remains appropriate after the execution change.
4. A material execution change can trigger strategy re-evaluation.
5. The system should not silently replace the existing strategy.
6. The system should explain why the current strategy may no longer be appropriate.
7. The system should present applicable alternative strategies.
8. The investor remains the decision-maker.
9. The investor can keep the existing strategy if they accept the trade-offs.
10. The investor can select an alternative strategy if they prefer it.
11. The investor can continue experimenting through the what-if environment.
12. Strategy re-evaluation should be targeted rather than automatically rebuilding the entire financial plan.
13. In a multi-goal plan, unrelated strategies should remain intact unless the changed execution materially affects them.
14. The accepted strategy and execution determine the resulting Action Plan.
15. What-if experiments should not overwrite the accepted plan until the investor adopts them.
16. The exact materiality threshold, strategy re-evaluation trigger, cross-strategy dependency model, and implementation mechanics remain subject to validation against the existing system.

---

## 17. Final Business Principle

> **An execution change should first be treated as an execution change. If its consequences make the existing strategy no longer appropriate, the system should identify that condition, explain the trade-offs, and offer alternative strategies. The investor decides whether to keep the existing strategy or change it.**

Therefore:

**Execution Change**

→ **Impact Analysis**

→ **Strategy Still Appropriate?**

→ **Yes: Update Execution**

→ **No: Re-evaluate Strategy**

→ **Investor Choice**

→ **Updated Strategy + Execution + Action Plan**

This preserves investor autonomy while allowing the system to intelligently detect when an execution decision has changed the strategic problem.
