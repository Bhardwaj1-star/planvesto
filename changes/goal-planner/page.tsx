/**
# Goal Planner — Proposed Functional Theory

## 1. Centralized Verified Monthly Surplus
**Current system state:** Monthly Surplus is only partially canonicalized in the existing system. Financial State calculates and stores `investable_surplus_monthly`, and Goal Planner reads that Financial State value. However, the existing code does not yet establish consistent system-wide use of one canonical value in every module; some places still accept or derive `available_monthly_surplus` independently, and the Financial State frontend includes a local fallback calculation.
**Required system-wide direction:** The **Verified Monthly Surplus** must become a centralized, canonical system-wide value. It is not specific to Case 1 or the Goal Planner. Wherever monthly surplus is used across the system, the same centralized verified value must be referenced. This requires system-wide standardization; changing only Goal Planner is not sufficient.
Case 1 uses this value as its funding-capacity reference, and Case 2A and Case 2B also use it when testing affordability. Case 2A tests goal changes against this fixed surplus. Case 2B keeps the goal amount and target date fixed and tests alternative contribution structures. Do not treat budgeting actions as Goal Planner methods.

## 2. Case 2A — Adjust goal amount or timeline
Test one goal condition at a time:
- **Option A — Reduce goal amount:** keep the target month/year fixed; find the highest affordable today's goal amount.
- **Option B — Extend timeline:** keep today's goal amount fixed; find the earliest affordable target month.
- A scenario passes the SIP-affordability test when its additional required monthly SIP is within the centralized, canonical Verified Monthly Surplus.

## 3. Case 2B — Keep goal amount and target date fixed
Case 2B tests two funding structures. The goal amount and target date do not change.

### Option A — Step-Up SIP
- Calculate a contribution schedule that can meet the fixed future goal target using the approved Chapter 05 **Step-up / Changing Contribution Schedule** method.
- The annual Step-Up SIP rate has an initial maximum limit of **10%**.
- If the required annual step-up rate is **10% or less**, retain the Step-Up SIP route and show the required starting SIP / contribution schedule and the monthly surplus capacity needed to support it. Compare the required starting contribution with the centralized, canonical Verified Monthly Surplus and show any surplus gap.
- If the required annual step-up rate is **above 10%**, do not present that higher rate as the recommended Step-Up SIP solution. Cap the tested annual step-up at **10%** and move to Option B to calculate the approximate initial lump sum needed to cover the remaining goal funding gap.

### Option B — Initial Lump Sum + Step-Up SIP (10% cap)
- Keep the goal amount and target date fixed.
- Hold the annual Step-Up SIP rate at the maximum **10%** and combine the recurring contribution schedule with an initial lump sum.
- Calculate the approximate initial lump sum required so that the combined projected value of eligible existing funding, the lump sum and the step-up contribution schedule can meet the future goal target.
- Show the assumed initial lump sum, starting SIP, 10% annual step-up schedule, required monthly contribution capacity and any remaining funding gap.
- Treat the lump sum as a required scenario amount, not proof that the investor owns or has available that amount. Confirm eligibility, liquidity, timing and competing commitments before treating any asset or cash as available.

## 4. Calculation and affordability rules
- Use Chapter 05's dated cash-flow method for changing contribution schedules; do not use the constant-SIP formula for a Step-Up SIP.
- For the combined lump-sum route, project the initial lump sum and each dated step-up contribution to the goal date using one consistent approved return and timing basis.
- Use the centralized, canonical Verified Monthly Surplus as the monthly capacity reference. Do not increase or fabricate surplus inside Case 2B.
- Count each existing asset, lump sum and contribution only once. Preserve goal assumptions and eligible funding rules.
- If required inputs, an approved method or reliable evidence are missing, report the result as unresolved / insufficient evidence rather than inventing a value.

## 5. Result and approval
Display each feasibility outcome as a **proposal / preview**. The investor can edit the goal through the Goal Planner UI. The Goal Planner does not sell assets, commit a lump sum, or change SIP contributions.

## 6. Goal Planner UI flow
- Remove the existing Goal Planner feasibility UI; it will be replaced by the proposed flow described here.
- The Goal Planner UI should focus only on presenting the **Feasibility Test** and its outcome. Do not add strategy recommendations, budgeting controls or contribution-management actions to this screen.
- The investor can edit goal details through the Goal Planner UI.
- After the feasibility result is shown, provide a clear **Select Affordability Test** action. The user can select the affordability test they want to carry forward.
- Carry the selected affordability test and its relevant scenario context forward to the **Strategy Builder**. The Strategy Builder is the next stage for taking the selected test forward.
- This UI flow defines selection and hand-off only; it does not itself sell assets, commit a lump sum, or change SIP contributions.

## 7. Scope and dependencies
This is a proposed functional specification under `changes/goal-planner/`; it is documentation only and is not connected to or deployed as the production Goal Planner. Chapter 10 defines the feasibility decision boundaries; Chapter 05 owns the canonical contribution, step-up and combined lump-sum calculation methods. The centralized, canonical Verified Monthly Surplus is the required system-wide monthly surplus reference.
*/