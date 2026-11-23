/**
# Goal Planner — Case 1 and Case 2A: Proposed Functional Theory

## 1. Core rule
Case 1's verified **Available Monthly Surplus** is the fixed monthly funding ceiling for Case 2A. Case 2A must not assume, increase, or independently recalculate this capacity. The same surplus value is used to test both options.

## 2. Affordability test
Calculate the goal's required monthly contribution using the existing goal assumptions and eligible mapped funding. Deduct the goal's existing linked SIP to obtain the **Additional Required Monthly SIP**.

**A scenario is affordable when:**
Additional Required Monthly SIP ≤ Case 1 Available Monthly Surplus.

If verified surplus is missing or unavailable, Case 2A cannot be evaluated; the investor must complete Financial State first.

## 3. Case 2A — change one variable at a time

### Option A: Reduce goal amount
- Keep the original target month and year unchanged.
- Reduce today's goal amount and recalculate the future target and required contribution.
- Find the highest goal amount that satisfies the affordability test.
- Show the revised amount, future target, additional required SIP, fixed surplus and funding gap.

### Option B: Extend goal timeline
- Keep today's goal amount unchanged.
- Extend the target month and recalculate the future target and required contribution.
- Find the earliest target month that satisfies the affordability test.
- Show the revised target month, future target, additional required SIP, fixed surplus and funding gap.

## 4. Result and approval
Show the calculated result as a **proposal / preview only**. Do not change the saved goal, mapped assets, contributions or financial data automatically. Apply a revised goal only after the investor explicitly approves it through the authorised save workflow.

## 5. Guardrails
- Use the backend's verified Financial State surplus as the source of truth; never accept a browser-entered surplus.
- Preserve the existing inflation, return, mapped-asset and goal assumptions while testing each option.
- Do not change amount and timeline in the same option.
- If no affordable result is found, explain that the current surplus does not support the tested goal conditions; do not label the goal impossible.
- A passing monthly affordability test does not mean the goal is already funded or that all other constraints have passed.

**Scope:** This is a proposed functional specification kept under `changes/goal-planner/`. It is documentation only and is not connected to or deployed as the production Goal Planner.
*/
