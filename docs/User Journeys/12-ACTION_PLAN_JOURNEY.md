# Action Plan Journey

**Document Type:** User Journey  
**Status:** CANONICAL DESIGN  
**Scope:** Accepted Plan → Actions → Execution → Impact Review

## 1. Main Journey

```
Investor Accepts a Path
          ↓
     Accepted Plan
          ↓
 System Identifies Required Actions
          ↓
       Action List
          ↓
     Investor Reviews
          ↓
    Confirm / Change
          ↓
     Action Plan Ready
          ↓
       Execution
          ↓
    Progress Update
          ↓
      Impact Review
```

## 2. Action List

```
Accepted Plan
     ↓
Required Actions
     ↓
Goal / Plan Link
     +
Purpose
     +
Amount / Timing
     +
Order / Dependencies
     +
Source / Destination
     ↓
Investor Review
```

Show a detail only when it is defined by the accepted decision or available evidence.

Actions may come from accepted goal-funding changes, debt/cash-flow changes, multi-goal allocation, or strategy implementation. They are not limited to Strategy Builder actions.

## 3. Execution Change

```
Investor Changes Execution
          ↓
      What-If
          ↓
     Impact Review
          ↓
   Current Path Still Valid?
       ┌──┴───┐
       ↓      ↓
      Yes     No
       ↓      ↓
 Review /   Review Affected
 Update     Goal / Strategy
 Execution      ↓
       └───┬───┘
           ↓
    Investor Decision
       ┌───┴────┐
       ↓        ↓
    Reject    Accept
       ↓        ↓
 Keep Current  Update Accepted
 Plan + Actions Plan + Relevant
               Future Actions
                    ↓
             Preserve History
```

A What-If scenario does not change the active Action Plan by itself. Recheck other goals only when the change has a relevant plan-level or cross-goal impact.

## 4. Progress and Outcome

```
Action Status
     +
Execution Evidence
     ↓
Compare Expected / Actual Impact
     ↓
Progress + Variance
     ↓
Review Next Action
```

Completing an action does not by itself mean the goal was achieved. Keep action status separate from actual financial results.

## 5. Core Boundary

```
Investor Adoption
       ↓
  Accepted Plan
       ↓
   Action Plan
       ↓
    Execution
```

A recommendation or unaccepted scenario is not an active Action Plan. When a revised path is accepted, update only affected future actions and preserve completed-action history.

## References

- [Action Plan feature definition](../feature/Action-Plan.md)
- [Action Plan implementation specification](../implementations/Action-Plan.md)
- [Case 3 — Multi-Goal Feasibility and Action Plan](../Real-Life%20Decision%20Cases/03-CASE_3_MULTI_GOAL_FEASIBILITY_AND_ACTION_PLAN.md)
- [Case 4 — Better-Path Strategy and Implementation](../Real-Life%20Decision%20Cases/04-CASE_4_BETTER_PATH_STRATEGY_AND_IMPLEMENTATION.md)
- [Case 9 — Execution Plan What-If and Impact Guidance](../Real-Life%20Decision%20Cases/09-CASE_9_EXECUTION_PLAN_WHAT_IF_AND_IMPACT_GUIDANCE.md)
- [Case 10 — Execution Change Triggering Strategy Re-evaluation](../Real-Life%20Decision%20Cases/10-CASE_10_EXECUTION_CHANGE_TRIGGERING_STRATEGY_REEVALUATION.md)
- [Case 11 — Iterative Strategy, Execution and Revalidation](../Real-Life%20Decision%20Cases/11-CASE_11_ITERATIVE_STRATEGY_EXECUTION_AND_REVALIDATION.md)
