# Case 6 — Goal / Intent Change and Feasibility Recalculation

## 1. Real-Life Financial Case

An investor intentionally changes one of their financial goals or one of the inputs that define that goal.

Examples include:

- increasing the target amount;
- decreasing the target amount;
- extending the timeline;
- shortening the timeline;
- changing the target date;
- changing the existing corpus available for the goal;
- changing relevant funding assumptions;
- changing other planning inputs that affect the goal;
- or cancelling the goal altogether.

The important point is that a goal is not defined only by its target amount.

A goal's planning outcome depends on the complete set of inputs used to determine its funding requirement and feasibility.

---

## 2. Question — What Happens When the Investor Changes a Goal?

A goal/intent change is a change to the planning input.

The system should therefore:

1. update the goal;
2. recalculate the affected funding requirement;
3. recalculate feasibility using the updated goal and current Financial State;
4. determine the required funding path;
5. create or update the appropriate strategy based on the new situation.

The system should not assume that changing a goal automatically invalidates the entire existing financial plan.

It should recalculate the affected planning chain.

---

## 3. Goal Amount Is Only One Planning Input

The effect is not limited to the target amount.

For example:

### Target Amount Changes

**₹50 lakh → ₹75 lakh**

The funding requirement generally increases.

**₹50 lakh → ₹35 lakh**

The funding requirement generally decreases.

### Timeline Changes

If the investor extends the timeline:

**8 years → 12 years**

the required periodic surplus/contribution may decrease.

If the investor shortens the timeline:

**8 years → 5 years**

the required periodic surplus/contribution may increase.

### Target Date Changes

Moving the goal date earlier generally increases the required funding intensity.

Moving it later generally reduces the required periodic funding requirement, all else being equal.

### Other Goal Inputs

Changes to other planning inputs can similarly affect:

- required corpus;
- required monthly contribution;
- required lump sum;
- funding gap;
- feasibility;
- strategy;
- and the resulting Action Plan.

Therefore:

> **Goal feasibility must be recalculated from the complete updated goal definition, not from the target amount alone.**

---

## 4. Relationship Between Goal and Financial State

Goal planning inputs and Financial State are connected.

Conceptually:

**Goal Definition**

↓

**Funding Requirement**

↕

**Financial State / Available Resources**

↓

**Feasibility**

↓

**Funding Path**

↓

**Strategy**

The same Financial State can produce a different feasibility result when the goal changes.

Likewise, the same goal can produce a different feasibility result when the Financial State changes.

Therefore, the system should evaluate the two together rather than treating goal changes as an isolated database update.

---

## 5. Goal Cancellation Is Different

When an investor cancels a goal, the goal requirement is removed.

However:

> **Canceling a goal does not mean canceling the assets that were accumulated for that goal.**

The investor may already have assets mapped to the cancelled goal.

Those assets remain part of the investor's Financial State.

The system should therefore:

1. deactivate/remove the cancelled goal from active planning;
2. identify assets currently mapped to that goal;
3. retain those assets in the Financial State;
4. determine the appropriate destination for those assets;
5. re-map them to the remaining relevant goals where appropriate;
6. recalculate the remaining goals;
7. reassess overall feasibility;
8. create or update strategies if required.

### Key Principle

**Cancel Goal ≠ Cancel Asset.**

The goal relationship changes; the underlying financial assets do not disappear.

---

## 6. Example — Goal Cancellation

Suppose an investor has:

- Education Goal — ₹50 lakh
- Retirement Goal — ₹3 crore

The investor has already accumulated ₹15 lakh specifically mapped to Education.

The investor later decides:

> "I no longer want this education goal."

The system should not remove the ₹15 lakh from the investor's Financial State.

Instead:

**Education Goal Cancelled**

↓

**₹15 lakh Education-linked assets identified**

↓

**Assets retained**

↓

**Assets reassigned/mapped appropriately**

↓

**Retirement and other active goals recalculated**

↓

**Overall feasibility recalculated**

↓

**Strategy / Action Plan updated if required**

The exact asset destination may depend on the investor's remaining goals and the relevant planning logic.

---

## 7. Does a Goal Change Automatically Mean the Existing Strategy Is Wrong?

No.

The goal change means the planning input has changed.

The system should first recalculate the affected feasibility.

Then it determines what strategy is appropriate under the new situation.

The resulting strategy may:

- remain the same;
- require modification;
- be replaced;
- or no longer be required.

The decision should come from the recalculated financial situation.

Therefore:

> **Goal change → Recalculate → Determine required funding path → Determine appropriate strategy.**

Not:

> **Goal change → Automatically replace strategy.**

---

## 8. Proportional Relationship Between Goal Inputs and Funding Requirement

Goal planning variables are connected.

A change in one variable can alter the required contribution or lump sum.

For example:

| Change | General effect |
|---|---|
| Target amount increases | Higher funding requirement |
| Target amount decreases | Lower funding requirement |
| Timeline increases | Lower periodic funding requirement, all else equal |
| Timeline decreases | Higher periodic funding requirement, all else equal |
| Target date moves earlier | Higher funding intensity |
| Target date moves later | Lower funding intensity, all else equal |
| Existing goal corpus increases | Lower future funding requirement |
| Existing goal corpus decreases | Higher future funding requirement |
| Funding assumptions change | Funding requirement may change |
| Goal cancelled | Goal funding requirement removed |

These are general directional relationships. The actual result must be recalculated from the complete planning inputs.

---

## 9. Goal Change Does Not Require a Separate Planning System

The system should not create a separate decision mechanism for:

- amount change;
- date change;
- timeline change;
- corpus change;
- or other individual goal-input changes.

They are all changes to the goal's planning inputs.

The same feasibility process should handle them.

Conceptually:

**Updated Goal Inputs**

↓

**Recalculate Goal Funding Requirement**

↓

**Recalculate Feasibility**

↓

**Determine Required Funding Path**

↓

**Determine / Update Strategy**

↓

**Update Implementation and Action Plan if required**

This keeps the planning logic centralized.

---

## 10. Relationship to Earlier Cases

### Case 1

**Debt economics and opportunity cost can affect goal feasibility.**

### Case 2

**Once a goal is feasible, funding mechanisms can be used and Strategy Builder can determine the detailed execution strategy.**

### Case 3

**Multiple goals must be evaluated together and alternative paths may be required to make the overall plan feasible.**

### Case 4

**Even when a goal is feasible, Strategy Builder can identify a better strategic path and the investor can test its implementation using their financial numbers.**

### Case 5

**When the Financial State materially changes, the existing plan is revalidated and adapted where necessary.**

### Case 6

**When the investor intentionally changes the goal or any material goal-planning input, the affected feasibility is recalculated and the appropriate funding path and strategy are determined from the updated situation.**

---

## 11. Established Business Decisions

From this case, the following principles are established:

1. Goal changes are changes to planning inputs.
2. Goal planning is not dependent only on the target amount.
3. Target amount, timeline, target date, existing corpus and other relevant planning inputs can affect feasibility.
4. Any material change to relevant goal-planning inputs requires feasibility recalculation.
5. The recalculation uses the updated goal together with the current Financial State.
6. A goal change does not automatically invalidate the existing strategy.
7. The system recalculates first and then determines whether the existing strategy remains appropriate or a different strategy is required.
8. Goal cancellation removes the goal requirement but does not remove the assets accumulated for that goal.
9. Assets mapped to a cancelled goal remain part of the investor's Financial State.
10. Those assets should be appropriately reassigned/mapped to remaining goals where applicable.
11. The resulting funding path, strategy, implementation and Action Plan should be updated where the recalculated situation requires it.
12. Goal changes and Financial State changes are related but distinct triggers:
    - Case 5: **Financial State changes.**
    - Case 6: **Goal/intent changes.**
13. The exact mathematical formulas, asset-reassignment rules, and strategy-update rules remain subject to further implementation validation.

---

## 12. Decision Boundary

The established planning relationship is:

**Investor Intent / Goal Definition**

+

**Current Financial State**

↓

**Goal Funding Requirement**

↓

**Goal Feasibility**

↓

**Required Funding Path**

↓

**Strategy Builder**

↓

**Implementation**

↓

**Action Plan**

When the investor changes the goal:

**Updated Goal Definition**

↓

**Recalculate**

↓

**New Feasibility**

↓

**New / Updated Funding Path**

↓

**New / Updated Strategy if required**

↓

**Updated Implementation / Action Plan if required**

This means goal changes are handled through the same centralized planning process rather than through separate rules for every type of goal modification.

---

## 13. Final Business Principle

> **A goal is a set of planning inputs, not just a target amount. When the investor changes any material part of that goal, the system recalculates what is required to achieve it under the current Financial State and determines the appropriate funding path and strategy.**

And:

> **Canceling a goal changes the goal mapping, not the existence of the investor's assets.**

---

## 14. Change Status

**Business concept established through real-life case validation.**

Implementation has **not** been changed by this document.

The exact feasibility formulas, goal-input dependency rules, asset-reassignment rules after goal cancellation, and strategy-update mechanics remain to be validated against the existing implementation before they are frozen.
