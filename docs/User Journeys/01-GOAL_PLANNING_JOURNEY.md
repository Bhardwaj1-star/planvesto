# Goal Planning Journey

**Document type:** User Journey  
**Scope:** Investor starts a goal, reviews the funding position, sees the feasibility result, and decides whether to continue.

This document describes the journey in simple language: what the investor does, what the system shows, and what happens next. It does not define calculations or technical implementation.

## Type 1 — Complete journey

1. **Start a goal**
   - Investor selects an existing goal or starts a new one.
   - The system opens the goal details.
   - **Next:** Enter or review the details.

2. **Enter goal details**
   - Investor enters or reviews the goal amount and target date, along with any details requested for that goal.
   - The system checks whether the required information is present. If something is missing, it tells the investor what needs attention.
   - **Next:** Correct missing details or continue.

3. **Review the target and timeline**
   - Investor reviews the goal's target date and current target amount.
   - The system shows the time remaining and the target amount for the selected date, along with the assumptions shown to the investor.
   - **Next:** Continue or change the details.

4. **Review existing assets**
   - Investor selects the assets to consider for this goal, or continues without mapping assets when the journey allows it.
   - The system shows the selected assets and their projected values where these can be calculated.
   - **Next:** Review the funding position.

5. **Review the funding gap**
   - Investor reviews the target amount and projected assets.
   - The system shows the remaining gap or surplus and the required contribution when it can be calculated.
   - **Next:** Review the available financial information.

6. **Review financial capacity**
   - Investor reviews the available income, expenses, surplus, debt/EMI and other relevant financial information.
   - The system shows the information available for the assessment and identifies anything important that is missing.
   - **Next:** Review the funding options that can be assessed.

7. **Review funding options**
   - Investor reviews the funding options available for the goal.
   - The system shows the outcomes and relevant trade-offs it can assess from the available information.
   - **Next:** Review the goal's feasibility result.

8. **Review the feasibility result**
   - Investor reviews the result and the reasons shown with it.
   - The system explains the current result and the next available action.
   - **Next:** Follow the relevant route below.

9. **Choose what to do next**
   - If the goal is feasible, the investor can review the proposed path and choose whether to continue.
   - If the goal is constrained, the investor reviews the constraint and can change relevant information or funding choices.
   - If the goal is infeasible, the system may show a proposed lower target amount, later target date, or a combination for the investor to review.
   - If the result is unknown, the investor supplies or corrects the missing information.
   - If no acceptable path is available, the investor reviews the reasons and can change relevant inputs or stop.
   - **Next:** Review the updated result, confirm a decision, or leave the journey.

10. **Continue to Strategy Decision**
    - Investor chooses to continue after reviewing the goal and feasibility information.
    - The system passes the goal and its feasibility information to Strategy Decision.
    - **Next:** Continue to Strategy Decision.

## Type 2 — Detailed component journeys

### A. Goal details

1. Investor selects a goal and enters or reviews the requested details.
2. The system checks the details and points out anything missing or invalid.
3. Investor corrects the information, or leaves the journey.
4. When ready, the investor continues to the target and timeline.

### B. Target and timeline

1. Investor enters or confirms the target date and goal amount.
2. The system shows the time remaining and the target amount for that date.
3. Investor reviews the displayed assumptions and changes the permitted inputs if needed.
4. The system updates the affected information.
5. Investor continues to asset mapping.

### C. Assets and funding gap

1. Investor opens the available asset list.
2. Investor selects the assets to consider for the goal, or continues without mapping assets when allowed.
3. The system shows the selected assets and their projected values where available.
4. The system shows the funding gap or surplus and the required contribution when calculable.
5. Investor reviews the result and continues, or returns to change the target or asset selection.

### D. Financial capacity and funding options

1. Investor reviews the financial information shown for the goal.
2. If information is missing or incorrect, the investor returns to the relevant place to correct it.
3. The system updates the affected funding information.
4. Investor reviews the funding options the system can assess and compares their outcomes.
5. Investor continues to the feasibility result or returns to change a relevant input.

### E. Feasibility and next step

1. Investor opens or requests the feasibility result.
2. The system shows the result and the reasons for it.
3. Investor follows the next step shown:
   - **Feasible:** review the path and decide whether to continue.
   - **Constrained:** review the issue and change relevant inputs or funding choices if needed.
   - **Infeasible:** review any proposed target or date adjustment that is available.
   - **Unknown:** provide or correct the missing information.
   - **No acceptable path:** review why the available options do not meet the requirements, then change relevant inputs or stop.
4. When an input changes, the system updates the affected result for the investor to review again.
5. Investor confirms a decision and continues to Strategy Decision, or leaves without accepting the proposal.

## Simple example

An investor wants to fund education in 10 years.

1. The investor enters the education goal and target date.
2. The system shows the timeline and target information.
3. The investor selects any existing assets to consider for the goal.
4. The system shows the projected asset value, funding gap and required contribution when calculable.
5. The investor reviews financial capacity and the funding options available.
6. The system shows the feasibility result and its reasons.
7. The investor reviews the result, changes relevant inputs if needed, and chooses to continue or stop.

The system does not automatically choose a Strategy Builder strategy during this journey. Strategy Decision comes next.

---

**Related document:** `docs/implementations/Goal-Planner.md`
