# Case 8 — Investor Strategy Change and Multi-Strategy Financial Plan

> **Canonical lifecycle alignment — 2026-10-08**
> A strategy change is a proposed change. Multiple strategies may coexist, but the investor must adopt the proposed change before it becomes part of the Accepted Plan.

> **Core:** Financial State + Investor Intent/Goals → Goal Planning/Feasibility → Strategy Decision → Implementation Design → Stress/Resilience → Decision/Recommendation → Investor Decision → Accepted Plan → Action Plan → Execution.

> **Conditional:** Whole-Plan/Multi-Goal Impact is invoked only when the decision is plan-level.

> **Change loop:** Accepted Plan → Execution/What-If → Impact Analysis → Targeted Revalidation → Investor Decision → Updated Accepted Plan → Updated Action Plan.

> Goal Funding is owned by Goal Planner/Goal Feasibility; it is not a peer Strategy Builder strategy.

## 1. Real-Life Financial Case

An investor already has an established financial plan with one or more selected strategies.

The investor may later decide that they want to change, replace, or combine strategies.

The system should not treat the originally recommended strategy as permanently binding.

The system is designed to provide **guidance and advisory support**, while the investor remains the decision-maker.

For example:

- the system identifies an 18% loan as a materially high-cost obligation;
- the system therefore gives debt reduction higher priority than initiating a new investment;
- the investor understands the trade-off but still chooses to invest;
- the system should not silently prevent that decision;
- instead, it should explain the consequences and update the resulting plan.

Therefore:

> **Recommendation is guidance; investor choice determines the accepted financial path, subject to genuinely hard constraints.**

---

## 2. Question — Can the Investor Change the Strategy?

Yes.

The investor can change the selected strategy if they are willing to accept the associated trade-offs.

The system should:

1. explain why the current strategy was recommended;
2. show the economic and planning consequences of changing it;
3. allow the investor to choose an alternative where the decision is not a genuinely hard constraint;
4. recalculate the affected goals and financial plan;
5. revalidate the resulting path;
6. update implementation requirements;
7. update the Action Plan.

The system should not confuse **strong advisory priority** with an absolute prohibition.

For example, an 18% loan may create a very strong recommendation to reduce the debt before initiating a new investment. But if the investor knowingly accepts the trade-off, the system should model that choice and show its consequences.

---

## 3. Hard Constraint vs Advisory Priority

The system needs a clear distinction.

### Hard Constraint

A condition that the planning system genuinely cannot or should not violate.

A hard constraint can prevent a path from being accepted.

### Advisory Priority

A financially important signal that should influence the recommendation but does not necessarily prevent the investor from choosing another path.

Example:

**18% debt cost**

↓

Strong economic priority for debt reduction

↓

System recommends debt reduction

↓

Investor chooses to invest instead

↓

System explains the additional cost/risk/trade-off

↓

System recalculates the plan

This preserves investor autonomy while retaining the system's advisory value.

---

## 4. Strategy Builder Does Not Mean One Strategy Per Financial Plan

The Strategy Builder should not be interpreted as:

> "Find one strategy for the entire investor."

A financial plan can contain multiple goals and multiple financial problems.

Therefore:

> **One financial plan can contain multiple strategies operating simultaneously.**

The strategy set should be coordinated rather than treated as mutually exclusive.

For example:

| Financial requirement | Applicable strategy |
|---|---|
| Education goal funding / feasibility | Goal Planner funding path (not a Strategy Builder strategy) |
| Retirement risk transition | Progressive De-risking |
| High-cost debt | Debt Reduction |
| Goal timing/liquidity gap | Credit Utilisation |
| Capital that must be protected | Capital Preservation |

The exact combination depends on the investor's financial state, goals, constraints, and accepted trade-offs. Goal Planner funding paths remain separate from Strategy Builder strategies. For each individual Strategy Builder decision, present exactly two Strategy options; a whole plan may contain multiple coordinated strategies across different goals or requirements.

---

## 5. Existing Two-Strategy Output

The Strategy Builder already provides two strategies for the relevant decision/goal.

This should remain meaningful.

The two strategies represent alternative approaches for the decision being evaluated.

However, when the complete financial plan contains multiple goals or financial requirements, the system may select different strategies for different parts of the plan.

Therefore:

> **Two alternatives for one decision do not mean that the complete financial plan can contain only two strategies.**

A complete financial plan may contain a coordinated set of strategies.

---

## 6. Multi-Goal Example

Consider an investor with:

- Education Goal;
- Retirement Goal;
- an expensive outstanding loan;
- and a future liquidity requirement.

The resulting financial plan could simultaneously use:

### Goal Planner funding path — Education Goal

Goal Planner determines whether Education is feasible and compares its funding paths. This is not a Strategy Builder strategy and is not counted among the four canonical strategies.

### Strategy A — Progressive De-risking

For the Retirement Goal as it approaches its target period.

### Strategy B — Debt Reduction

For the expensive loan.

### Strategy C — Credit Utilisation

Where an appropriate temporary funding/timing gap exists and borrowing is viable.

### Strategy D — Capital Preservation

Where specific capital needs protection.

These strategies are not automatically contradictory.

They can operate together when their responsibilities are distinct and the combined plan remains feasible.

---

## 7. Coordinated Strategy Model

The correct conceptual model is:

**Financial Plan**

↓

**Goals + Financial State + Constraints + Investor Choices**

↓

**Identify Multiple Financial Requirements**

↓

**Determine Applicable Strategy for Each Requirement**

↓

**Select Strategy Alternatives**

↓

**Coordinate the Accepted Strategy Set**

↓

**Validate Whole-Plan Feasibility**

↓

**Implementation**

↓

**Action Plan**

Therefore the Strategy Builder is better understood as a **strategy composition and decision system**, rather than a single-strategy selector for the entire financial plan.

---

## 8. Investor Changes an Existing Strategy

Suppose the investor is currently following:

**Debt Reduction**

because of an 18% loan.

The investor later decides:

> "I understand the cost of keeping the loan, but I want to invest the available surplus instead."

The system should not simply replace the strategy without analysis.

It should compare:

### Current Accepted Path

**Debt Reduction**

versus

### Investor-Proposed Path

**Investment / alternative strategy**

and show the relevant consequences, such as:

- debt cost;
- expected investment outcome;
- liquidity;
- risk;
- goal funding;
- cash-flow impact;
- effect on other goals;
- and resulting Action Plan changes.

The investor can then accept the alternative.

---

## 9. Strategy Change Does Not Automatically Mean Full Plan Replacement

Changing one strategy should trigger a **targeted revalidation**.

The system should identify:

- which goal or financial requirement is affected;
- which dependencies change;
- which other strategies may be affected;
- whether whole-plan feasibility changes;
- whether existing Action Plan items remain valid.

Only the affected parts should be recalculated where possible.

However, if the strategy change materially affects the whole financial plan, a broader whole-plan validation should occur.

This avoids unnecessary strategy churn.

---

## 10. Investor Choice and Trade-offs

The system's role is not to hide trade-offs.

If the investor chooses a path that is economically less attractive than the recommended path, the system should make the difference visible.

For example:

> Recommended: reduce 18% debt.

Investor choice:

> Continue investing instead.

The system can explain:

- additional interest cost retained;
- investment return assumption required to compensate;
- liquidity benefit;
- risk introduced;
- effect on goal probability/feasibility;
- and downstream Action Plan changes.

The investor can knowingly accept the trade-off.

This is consistent with the system's advisory role.

---

## 11. Strategy Change in a Multi-Goal Plan

In a multi-goal plan, changing one strategy should not automatically remove the other strategies.

Example:

**Existing coordinated plan**

- Education → Goal Planner / Feasibility
- Retirement → Progressive De-risking
- Loan → Debt Reduction

Investor changes the loan decision.

The resulting plan might become:

- Education → Goal Planner / Feasibility
- Retirement → Progressive De-risking
- Loan → Investor-selected alternative path

The other strategies remain unless the change materially affects their feasibility or dependencies.

The system therefore maintains a **coordinated strategy set**, not a single global strategy.

---

## 12. Strategy Builder Output

For a relevant goal or decision, Strategy Builder can continue to present:

### Strategy 1

The system's recommended/appropriate strategy.

### Strategy 2

A meaningful alternative/better-path strategy.

The investor can compare them.

At the whole-plan level, however, the accepted output can contain:

> **Strategy 1 for Requirement A + Strategy 2 for Requirement B + Strategy 3 for Requirement C + ...**

The system must then validate the combination as one financial plan.

---

## 13. Action Plan

Action Plan remains the implementation layer.

When the investor changes a strategy, the Action Plan should be updated.

For example:

### Previous Action Plan

- prepay high-cost loan;
- redirect released EMI toward the goal;
- continue existing goal contribution.

### Investor changes strategy

- stop planned prepayment;
- retain the loan;
- deploy available surplus toward investment;
- continue required goal funding.

The Action Plan should reflect the investor's accepted choice rather than continuing to instruct the investor to execute the old strategy.

Completed historical actions should remain history.

---

## 14. Decision Flow

The established conceptual flow is:

**Existing Financial Plan**

↓

**Current Strategy Set**

↓

**Investor Proposes Strategy Change**

↓

**Trade-off / Impact Analysis**

↓

**Affected Goal & Dependency Recalculation**

↓

**Whole-Plan Validation Where Material**

↓

**Investor Decision**

### If rejected

**Existing accepted strategy continues.**

### If accepted

**Updated Strategy Set**

↓

**Updated Implementation**

↓

**Updated Action Plan**

↓

**Investor Execution**

---

## 15. Relationship to Case 5 and Case 7

### Case 5 — Financial State Change

The investor's financial circumstances change.

The system checks materiality and revalidates the existing plan.

### Case 7 — New Goal

The investor proposes a new goal.

The system first evaluates it as a separate scenario against the existing plan.

### Case 8 — Strategy Change

The investor intentionally changes an existing strategic choice.

The system evaluates the consequences and allows the investor to accept the alternative where it is not a genuinely hard constraint.

These are three different triggers:

| Case | Trigger | Primary response |
|---|---|---|
| Case 5 | Financial State changes | Revalidate |
| Case 7 | New goal proposed | Scenario + investor decision |
| Case 8 | Strategy choice changes | Trade-off analysis + revalidation |

---

## 16. Established Business Decisions

1. The investor can change a strategy after understanding its trade-offs.
2. The system is guidance/advisory, not an authority that permanently locks the investor into its recommendation.
3. Genuine hard constraints may restrict an option; advisory priorities should normally inform rather than automatically prohibit.
4. An 18% loan can therefore be a strong debt-reduction priority without automatically preventing an investor from choosing another path.
5. The system should show the economic consequences of an investor override.
6. A financial plan can contain multiple strategies simultaneously.
7. Multiple goals may require different strategies operating together.
8. The existing two-strategy Strategy Builder output remains useful as alternatives for the relevant decision/goal.
9. Two alternatives for one decision do not imply that the complete financial plan is limited to two strategies.
10. Strategy changes should trigger targeted revalidation and broader validation only when materially necessary.
11. Changing one strategy should not automatically invalidate unrelated strategies.
12. The accepted strategy set should be coordinated and validated as one financial plan.
13. Action Plan should reflect the investor's accepted strategy, not continue obsolete instructions.
14. Completed actions remain historical records; active/future actions can be revised.
15. The exact strategy-composition, conflict-resolution, hard-constraint override, and implementation mechanics remain subject to validation against the existing system.

---

## 17. Final Business Principle

> **The system recommends the financially appropriate path and explains the trade-offs, but the investor can choose another path when it is not a genuinely hard constraint.**

And:

> **A complete financial plan may contain multiple coordinated strategies operating simultaneously across different goals and financial requirements.**

Therefore:

**Strategy Builder = alternatives for the relevant decision**

while

**Financial Plan = coordinated set of accepted strategies across the investor's complete situation.**

---

## 18. Change Status

**Business concept established through real-life case validation.**

This document records the conceptual decision only.

No implementation changes are made by this document.

The exact strategy-composition model, cross-strategy conflict handling, investor override mechanics, and whole-plan validation rules remain to be validated against the existing system before implementation is frozen.
