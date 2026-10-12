# Case 5 — Plan Adaptation After Financial State Change

> **Canonical lifecycle alignment — 2026-10-08**
> A financial-state change triggers materiality assessment and targeted revalidation. Do not automatically rebuild the whole plan or replace a strategy.

> **Core:** Financial State + Investor Intent/Goals → Goal Planning/Feasibility → Strategy Decision → Implementation Design → Stress/Resilience → Decision/Recommendation → Investor Decision → Accepted Plan → Action Plan → Execution.

> **Conditional:** Whole-Plan/Multi-Goal Impact is invoked only when the decision is plan-level.

> **Change loop:** Accepted Plan → Execution/What-If → Impact Analysis → Targeted Revalidation → Investor Decision → Updated Accepted Plan → Updated Action Plan.

> Goal Funding is owned by Goal Planner/Goal Feasibility; it is not a peer Strategy Builder strategy.

## 1. Real-Life Financial Case

A financial plan has already been created for an investor.

The plan was based on the investor's:

- current Financial State;
- active goals;
- goal horizons;
- available surplus;
- assets;
- liabilities;
- liquidity;
- and other relevant financial information.

The plan has already passed through:

**Goal Feasibility → Strategy Builder → Implementation → Action Plan**

The investor then experiences a **material change in financial reality**.

For example:

- income materially decreases or increases;
- expenses materially change;
- a major asset is acquired, sold, or materially changes;
- a liability is created, repaid, or materially restructured;
- available monthly surplus changes;
- a goal target or horizon changes;
- a new goal is added;
- or a major implementation decision changes the Financial State.

The important question is no longer whether the original plan was correct when it was created.

The question is:

> **Does the existing plan still work under the investor's new financial reality?**

---

## 2. Question — Should Every Financial Change Trigger a New Plan?

No.

Financial State can change continuously, but not every change is important enough to invalidate an existing plan.

The system should therefore distinguish between:

- a normal/immaterial change; and
- a material change that can affect the existing plan.

The principle is:

> **Financial State changes → assess whether the change is material to the existing plan.**

An immaterial change should not unnecessarily cause the entire decision system to generate a new strategy.

---

## 3. What Counts as a Material Change?

The exact thresholds are not frozen by this case, but material changes can include:

- material income change;
- material expense change;
- significant asset change;
- significant liability change;
- major change in available surplus;
- material liquidity change;
- new goal;
- changed goal target;
- changed goal horizon;
- major debt restructuring;
- major implementation decision that changes the Financial State.

The important test is not simply:

> "Did something change?"

It is:

> **"Could this change materially affect the feasibility or recommended path of the existing plan?"**

---

## 4. What Should Happen After a Material Change?

The system should not immediately replace the existing strategy.

The correct sequence is:

**Updated Financial State**

↓

**Materiality Check**

↓

If immaterial:

**Existing Plan Continues**

If material:

↓

**Recalculate Relevant Goal Feasibility**

↓

**Revalidate Existing Strategy**

↓

If existing strategy remains appropriate:

**Retain Existing Strategy**

If it no longer remains appropriate:

**Generate Alternative Paths / Strategies**

↓

**Compare Alternatives**

↓

**Update Implementation**

↓

**Update Future Action Plan**

This creates an adaptation process rather than unnecessary strategy changes.

---

## 5. Should the Existing Strategy Be Replaced Automatically?

No.

The first question should be:

> **Does the existing strategy still work under the updated Financial State?**

If yes, the existing strategy should remain.

If no, the system should determine what changed and generate alternative paths.

This prevents unnecessary strategy churn.

The system should not change a strategy merely because the Financial State has moved slightly.

---

## 6. Example

Suppose an investor originally had:

- Monthly income: ₹3,00,000
- Monthly expenses: ₹1,50,000
- Monthly surplus: ₹1,50,000
- Retirement goal: feasible under the existing plan
- Education goal: feasible under the existing plan
- Selected strategy: already implemented
- Action Plan: active

Later, the investor's income falls to ₹2,40,000.

The system should not simply say:

> "Old strategy cancelled."

It should determine:

1. Has the change been material?
2. What happens to available surplus?
3. Are the goals still individually feasible?
4. Are the goals still collectively feasible?
5. Does the existing strategy remain appropriate?
6. Does the implementation still work?
7. Which future actions remain valid?
8. Are alternative paths now required?

The result could be:

- existing strategy remains valid;
- contribution needs to be temporarily reduced;
- another goal needs a different funding path;
- an asset may need to be used;
- or a new strategy may be required.

The answer should come from the updated financial analysis rather than from a generic rule.

---

## 7. Existing Action Plan Must Be Treated as a Living Plan

Action Plan is not a static report generated once.

It represents the actions the investor needs to execute over time.

Therefore, when Financial State changes, the system should preserve action history.

### Example

| Action | Status |
|---|---|
| Close high-interest loan | Completed |
| Reallocate ₹10 lakh | Completed |
| Start monthly investment | Active |
| Increase contribution next year | Pending |
| Rebalance portfolio | Pending |

If the Financial State changes:

- completed actions remain completed;
- active actions are re-evaluated;
- pending/future actions are checked against the new Financial State;
- actions that are no longer appropriate can be changed;
- new actions can be added.

The system should therefore update the **future execution plan**, not rewrite history.

---

## 8. When Should a New Alternative Path Be Generated?

A new alternative path should be considered when the existing plan is materially affected.

The sequence should be:

**Material Change**

↓

**Recalculate Feasibility**

↓

**Revalidate Existing Strategy**

↓

If still appropriate:

**Continue Existing Path**

If materially degraded or no longer appropriate:

**Generate Alternative Paths**

↓

**Compare Alternatives**

↓

**Select / construct the appropriate path**

↓

**Update Implementation**

↓

**Update Action Plan**

This keeps adaptation proportional to the actual financial change.

---

## 9. Case 5 Is About Adaptation, Not Constant Optimisation

The purpose is not to continuously search for a new strategy every time a number changes.

The purpose is:

> **Maintain a valid financial plan as the investor's financial reality changes.**

Therefore:

- small changes should not cause unnecessary replanning;
- material changes should trigger reassessment;
- existing strategies should be retained when they remain appropriate;
- alternatives should be generated when the existing path is materially affected;
- implementation should be updated when required;
- future actions should be updated accordingly.

---

## 10. Relationship to the Earlier Cases

Case 5 builds on the decisions established in Cases 1–4.

### Case 1

**Debt economics and opportunity cost can affect goal feasibility.**

### Case 2

**Once a goal is feasible, funding mechanisms can be used and Strategy Builder can determine the detailed execution strategy.**

### Case 3

**Multiple goals must be evaluated together and alternative paths may be required to make the overall plan feasible.**

### Case 4

**Even when a goal is feasible, Strategy Builder can identify a better strategic path, which the investor can test through the Implementation Layer.**

### Case 5

**An existing plan must be able to adapt when the investor's Financial State materially changes.**

---

## 11. Established Business Decisions

From this case, the following principles are established:

1. The financial plan is based on the investor's current Financial State.
2. Financial State changes over time.
3. Not every change should trigger complete replanning.
4. The system should assess whether a change is material to the existing plan.
5. Material changes should trigger relevant feasibility reassessment.
6. The existing strategy should be revalidated before being replaced.
7. If the existing strategy still works, it should normally be retained.
8. If the existing strategy is materially affected, alternative paths/strategies should be generated and compared.
9. Implementation should be updated when the selected path changes.
10. Action Plan is a living implementation plan.
11. Completed actions should remain part of the historical record.
12. Active and future actions should be re-evaluated when the Financial State materially changes.
13. New actions may be added when required.
14. Adaptation should avoid unnecessary strategy churn.
15. The exact materiality thresholds and adaptation algorithms are **not frozen by this case** and require further real-life validation.

---

## 12. Decision Boundary

The complete relationship established so far is:

**Financial State**

↓

**Goal Planner / Goal Feasibility**

↓

**Strategy Builder**

↓

**Implementation Layer**

↓

**Action Plan**

↓

**Investor Execution**

And over time:

**Updated Financial State**

↓

**Materiality Check**

↓

**Revalidate Existing Plan**

↓

**Continue Existing Path OR Generate New Alternative Path**

↓

**Update Implementation**

↓

**Update Future Action Plan**

This makes adaptation a continuous capability of the financial decision system rather than a separate one-time planning event.

---

## 13. Final Business Principle

> **A financial plan is not a one-time answer. It is a decision system that must remain valid as the investor's financial reality changes.**

The system should preserve what has already been correctly executed, reassess what remains to be executed, and change the future path only when the new Financial State requires it.

---

## 14. Change Status

**Business concept established through real-life case validation.**

Implementation has **not** been changed by this document.

The exact materiality thresholds, event triggers, reassessment scope, adaptation algorithm, and action-plan versioning rules remain to be validated through additional real-life cases before implementation is frozen.
