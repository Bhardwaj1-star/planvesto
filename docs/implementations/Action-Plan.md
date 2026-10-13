# Action Plan — Implementation

## 1. Inputs
- Current Accepted Plan and the investor's adopted decision.
- Current Financial State and relevant goals.
- Accepted funding changes, debt/cash-flow changes, resource allocations and strategy implementation details.
- Existing active actions and completed-action history.
- Baseline and expected-impact information needed to assess execution.

Do not invent action details that are absent from the accepted decision or supporting evidence.

## 2. Identify Required Actions

```
Accepted Plan
     ↓
Identify Required Changes
     ↓
Convert Changes to Actions
     ↓
Link Each Action to Goal / Plan
     ↓
Active Action List
```

Potential action sources:
- Goal-funding or feasibility changes.
- Debt repayment, prepayment, restructuring or EMI changes.
- Cash-flow changes.
- Accepted allocation changes across goals.
- Strategy and implementation steps.
- Future actions required by an investor-adopted execution change.

These are possible sources, not unconditional action rules. Include an action only when it follows from the accepted path and available evidence.

## 3. Action Details
For each action, provide only details supported by the accepted decision:
- What to do and why.
- Related goal / plan.
- Amount.
- Timing or deadline.
- Priority and order.
- Dependencies.
- Source and destination.
- Expected impact.

If a detail is unavailable, do not manufacture a value.

## 4. Investor Review

```
Generated / Updated Actions
          ↓
     Investor Review
          ↓
    Confirm / Change / Reject
          ↓
     Apply Allowed Decision
```

A generated list is not proof that the investor has adopted a new financial path. Changes that alter the Accepted Plan must go through the investor-decision process. The exact rules for which individual action fields may be changed directly are not yet frozen.

## 5. Execution and Progress

```
Active Action
     ↓
Execution Update
     ↓
Record Status + Available Evidence
     ↓
Compare Expected / Actual Impact
     ↓
Progress + Variance
```

Keep these separate:
- Action status.
- Evidence that the action was executed.
- Actual financial result.
- Difference between expected and actual impact.
- Goal or plan feasibility after execution.

Marking an action complete does not prove that the expected result occurred or that the goal was achieved. If actual evidence is unavailable, do not report a fabricated result.

## 6. Execution What-If and Impact

```
Current Accepted Plan
          ↓
Investor Tests a Change
          ↓
Calculate Relevant Impact
          ↓
Check Affected Goal / Plan
          ↓
Revalidation Required?
       ┌──┴───┐
       ↓      ↓
      No      Yes
       ↓      ↓
Review       Recheck Affected
Execution    Decisions / Strategy
       └──┬───┘
          ↓
    Investor Decision
       ┌──┴───┐
       ↓      ↓
    Reject   Accept
       ↓      ↓
 Keep Current Update Accepted
 Plan/Actions Plan + Relevant
              Future Actions
```

- A What-If is a scenario; it must not change active actions by itself.
- Assess impact relevant to the change, such as goal funding, cash flow, liquidity, debt/EMI or another goal.
- Revalidate affected decisions only when the change requires it.
- Whole-plan review is conditional on plan-level decisions or material cross-goal effects.
- Do not automatically replace a strategy because an execution input changed.

## 7. Reconcile Actions After Adoption
After the investor adopts a revised path:
- Add actions required by the new accepted path.
- Revise or deactivate affected future actions only under an approved rule.
- Preserve unaffected actions unless their dependency or evidence has materially changed.
- Preserve completed-action history.
- Ensure the active list reflects the current accepted path.

The exact rules for replacing/deactivating old actions, resolving dependencies and handling edits to completed actions are not yet frozen. Do not infer or invent those rules.

## 8. Outputs
- Active action list linked to the accepted goal / plan.
- Defined action details and current status.
- Investor decisions about actions.
- Execution progress.
- Expected-versus-actual impact and variance, where evidence is available.
- Updated future actions after an adopted change.
- Preserved completed-action history.

## 9. Unresolved Business Rules
- Exact action-generation coverage for every funding, debt, cash-flow, multi-goal and strategy path.
- Which action details investors may change directly.
- Exact sequencing and dependency rules.
- Conditions that require impact review or targeted revalidation.
- Rules for revising or deactivating old actions after adoption.
- Handling of completed-action edits and historical actions.
- Due-date, reminder and overdue behavior.

Until these rules are defined by the governing product rules, leave them unresolved rather than adding assumptions.
