# Goal Planning — User Journey

**Document type:** User Journey  
**Status:** Canonical journey design

This document contains only the investor's steps, the screens or information shown, the system's response, and the next step.

- **Type 1 — Broader Journey:** the complete investor journey from starting a goal to the Strategy Decision handoff.
- **Type 2 — Detailed Component Journeys:** the step-by-step journey inside each major part of Type 1.

---

# Type 1 — Broader User Journey

## 1. End-to-end flow

```
Start Goal
   ↓
Enter Goal Details
   ↓
Set Target Date and Review Target
   ↓
Choose Assets to Map
   ↓
Review Projected Assets and Funding Gap
   ↓
Review Financial Capacity
   ↓
Review Available Funding Paths
   ↓
Review Goal Feasibility Result
   ↓
Accept / Change Inputs / Stop
   ↓
Confirm Goal and Feasibility Information
   ↓
Continue to Strategy Decision
```

## 2. Main journey stages

| Stage | Investor action | System response | What the investor sees | Next step |
|---|---|---|---|---|
| 1. Start | Selects a goal or starts a new one. | Opens the goal details step and loads relevant saved information, if any. | Selected goal and available goal details. | Enter or review details. |
| 2. Goal details | Enters or reviews the goal information. | Checks the submitted information and identifies anything missing or invalid. | Entered details and any fields that need attention. | Correct missing information or continue. |
| 3. Target date and target | Enters or reviews the target date and relevant assumptions. | Calculates the time remaining and the target amount for that date. | Target date, time remaining, target amount, and displayed assumptions. | Review or change permitted inputs. |
| 4. Asset mapping | Selects assets to include in the goal view, or continues without mapping assets. | Checks the selected assets and loads their available values. | Selected assets and any unavailable or unresolved items. | Review the projected values. |
| 5. Funding gap | Reviews the projected asset values and target. | Calculates and displays the remaining gap or surplus. | Target amount, projected mapped assets, and funding gap/surplus. | Review the financial position. |
| 6. Financial capacity | Reviews the financial information used for the goal. | Loads available income, expenses, surplus, debt/EMI, liquidity, and relevant constraints. | Available information, relevant obligations, and any missing evidence. | Review funding paths. |
| 7. Funding paths | Reviews the paths the system can calculate from the available information. | Calculates the relevant alternatives and their outcomes. | Available paths, assumptions, projected outcomes, and limitations. | Compare paths and trade-offs. |
| 8. Feasibility result | Reviews the result and any reasons shown. | Displays the feasibility status and supporting information. | Feasibility status, key reasons, assumptions, and relevant alternatives. | Follow the result-specific route below. |
| 9. Investor decision | Accepts a proposal, changes relevant inputs, or stops. | Saves or recalculates only after the relevant action is confirmed. | Confirmation, updated result, or the option to stop. | Review the updated result or continue. |
| 10. Handoff | Chooses to continue after reviewing the goal result. | Passes the confirmed goal information and feasibility evidence to Strategy Decision. | Confirmation that the goal information is ready for the next step. | Continue to Strategy Decision. |

## 3. Result-specific routes

| Result shown | Investor sees | Investor's next step | System's next response |
|---|---|---|---|
| **Feasible** | The available path, its assumptions, and relevant trade-offs. | Review and accept the proposed path, change inputs, or stop. | Confirms the selected action and prepares the relevant goal information for the next step. |
| **Constrained** | The constraints, risks, trade-offs, and paths available for review. | Review the details; change relevant inputs or a funding choice if desired. | Recalculates affected results after a change, or keeps the current result if no change is made. |
| **Infeasible** | The shortfall and the reasons the current goal has not been made feasible. | Review the proposed target-amount reduction and/or target-date extension when available. | Shows the proposed adjustment and its recalculated result; waits for the investor's decision. |
| **Unknown** | The information that is missing, invalid, or not reliable enough to complete the assessment. | Provide or correct the requested information. | Recalculates after the evidence is resolved. |
| **No acceptable path** | The paths reviewed, the unmet requirements, and the constraints preventing an acceptable result. | Review the reasons, change permitted inputs if appropriate, or stop. | Recalculates only after a relevant change; does not force a path. |

## 4. Main journey exit points

The investor can leave the journey at these points:

- **Continue:** the goal and its feasibility information are ready for Strategy Decision.
- **Change and review again:** return to the relevant step, update the input, and review the recalculated result.
- **Stop:** leave without adopting the proposal or silently changing the saved goal.
- **Resolve missing information:** return when the required evidence is available.

---

# Type 2 — Detailed Component Journeys

## 5. Component A — Start and enter goal details

| Step | Investor action | System response | What the investor sees | Next step |
|---|---|---|---|---|
| A1 | Selects a goal type. | Opens the relevant goal form. | Goal type and applicable fields. | Enter details. |
| A2 | Enters or edits the goal name, current cost/target amount, target date, priority, flexibility, and other requested details. | Checks the entered fields and identifies missing or invalid information. | Entered information and field-level messages. | Correct issues or continue. |
| A3 | Supplies any requested goal-specific information. | Checks whether the information needed for this goal is available. | Any additional fields or missing-information message. | Continue when the form is complete. |
| A4 | Reviews and confirms the details. | Prepares the goal inputs for the next step. | A review of the entered goal information. | Review target and timeline. |

If the required information is missing or invalid, the investor stays on the relevant step until it is corrected or exits the journey. The system does not present a completed result using missing values as if they were known.

## 6. Component B — Review timeline and target

| Step | Investor action | System response | What the investor sees | Next step |
|---|---|---|---|---|
| B1 | Enters or confirms the target month/year. | Calculates the time remaining. | Target date and time remaining. | Review the target amount. |
| B2 | Reviews the current cost/target amount and displayed assumptions. | Calculates the target amount for the selected date using the configured calculation. | Target amount for the selected date and the assumptions shown with it. | Continue or change an input. |
| B3 | Changes the target date, target amount, or a permitted assumption. | Recalculates the outputs affected by that change. | Updated timeline, target, and affected results. | Review the updated information. |
| B4 | Confirms the displayed target information. | Passes the confirmed inputs to asset mapping and projection. | Confirmed target and timeline. | Review assets. |

## 7. Component C — Map and review assets

| Step | Investor action | System response | What the investor sees | Next step |
|---|---|---|---|---|
| C1 | Opens the asset list. | Loads assets available from the investor's financial records. | Available assets and their recorded values. | Select assets. |
| C2 | Selects or removes assets for this goal. | Checks the selected asset records and mapping. | Current selection and any asset that could not be resolved. | Review the selection. |
| C3 | Confirms the mapping. | Projects the selected, resolved assets to the goal date using the displayed assumptions. | Mapped assets, projected values, assumptions, and any limitations. | Review the funding gap. |
| C4 | Changes the asset selection or a relevant projection input. | Recalculates the affected asset projections and downstream results. | Updated projection and funding gap. | Continue or review the updated result. |

If no asset is mapped, the investor can continue when the flow allows it; the system shows the result using the available information rather than inventing an asset value.

## 8. Component D — Review funding gap and required contribution

| Step | Investor action | System response | What the investor sees | Next step |
|---|---|---|---|---|
| D1 | Reviews the target and projected mapped assets. | Calculates the funding gap or surplus. | Target, projected mapped asset value, and gap/surplus. | Review contribution information. |
| D2 | Reviews the contribution amount, when it can be calculated. | Calculates the required contribution under the displayed assumptions. | Required contribution, schedule, and assumptions. | Review financial capacity. |
| D3 | Changes a relevant target, date, asset selection, or contribution assumption. | Recalculates affected outputs. | Updated gap, contribution, and related figures. | Review the updated result. |

If a value cannot be calculated from the available information, the investor sees that it is unavailable and why, rather than a fabricated number.

## 9. Component E — Review financial capacity

| Step | Investor action | System response | What the investor sees | Next step |
|---|---|---|---|---|
| E1 | Opens the financial-capacity view. | Loads the available income, expenses, surplus, assets, liabilities, debt/EMI, and liquidity information relevant to the goal. | The available financial information and its displayed source/status. | Review the information. |
| E2 | Notices missing or incorrect information and chooses to correct it. | Opens the relevant input/update step. | The information that needs attention. | Correct it and return. |
| E3 | Confirms or returns from the financial information. | Refreshes the affected capacity figures and dependent calculations when required. | Updated capacity information or a message identifying unresolved evidence. | Review funding paths. |

## 10. Component F — Review and compare funding paths

| Step | Investor action | System response | What the investor sees | Next step |
|---|---|---|---|---|
| F1 | Opens the available funding paths. | Lists only paths that can be assessed with the available information. | Available paths and any limitations on the comparison. | Open a path or compare paths. |
| F2 | Selects a path or opens the comparison. | Shows comparable outcomes using the assumptions for each path. | Funding schedule, resources used, projected goal funding, remaining gap, and relevant cash-flow effects. | Review trade-offs. |
| F3 | Reviews debt-related paths, when relevant. | Shows the available debt, EMI, interest, tenure, and liquidity outcomes supported by the recorded information. | Path-by-path debt and cash-flow information, including unavailable items. | Compare the overall outcomes. |
| F4 | Reviews the comparison. | Shows material differences in goal outcome, cash flow, liquidity, risk, assumptions, and other-goal effects where available. | Comparison and the important limitations or trade-offs. | Continue to the feasibility result. |
| F5 | Changes a funding input or selects a different path to review. | Recalculates the affected path and comparison. | Updated path results and comparison. | Review the updated feasibility result. |

When the recorded information does not support a path or a comparison value, the system identifies the limitation instead of inventing a result. The investor can continue with the paths that can be assessed or return to correct the information.

## 11. Component G — Review Goal Feasibility

### G1. First result

| Step | Investor action | System response | What the investor sees | Next step |
|---|---|---|---|---|
| G1.1 | Requests or opens the feasibility result. | Assesses the current goal using the available financial information and relevant funding paths. | Result status, reasons, assumptions, and available paths. | Follow the displayed result route. |
| G1.2 | Reviews a feasible path. | Keeps the path as a proposal until the investor confirms the relevant action. | Path details, assumptions, and trade-offs. | Accept, change inputs, or stop. |
| G1.3 | Reviews a constrained result. | Shows the constraints and trade-offs that need attention. | Constraint details and available paths. | Review, change relevant inputs, or stop. |
| G1.4 | Reviews an infeasible result. | Shows the current shortfall and proceeds to the goal-adjustment step when that calculation can be made. | Shortfall and the available adjustment options. | Review the proposed adjustment. |
| G1.5 | Receives an Unknown result. | Identifies the evidence that needs to be supplied or corrected. | Missing or unreliable information and the step to return to. | Correct information and recalculate. |
| G1.6 | Receives No acceptable path. | Shows the unmet requirements and constraints for the paths assessed. | Reasons no assessed path can be accepted. | Change relevant inputs if appropriate, or stop. |

### G2. Review proposed goal-condition adjustments

This route is shown only when the first assessment has not made the current goal feasible.

| Step | Investor action | System response | What the investor sees | Next step |
|---|---|---|---|---|
| G2.1 | Reviews the proposed lower target amount, later target date, or combination when available. | Calculates the result for each adjustment that can be assessed. | Proposed change, revised target, updated funding figures, and relevant trade-offs. | Compare the proposals. |
| G2.2 | Selects a proposal to review further. | Shows the updated result for that proposal without silently changing the saved goal. | Updated feasibility result and the difference from the original goal. | Accept the proposal, change inputs, or stop. |
| G2.3 | Changes a proposed value or related input. | Recalculates the affected outputs. | Revised proposal and result. | Review again. |
| G2.4 | Declines all proposed adjustments. | Keeps the original goal unchanged. | Current result and options to return or stop. | Return to an earlier step or exit. |

## 12. Component H — Confirm the decision and hand off

| Step | Investor action | System response | What the investor sees | Next step |
|---|---|---|---|---|
| H1 | Reviews the selected funding path or proposed goal change. | Shows the exact proposal and the goal information affected by the decision. | Final review of the selected proposal, assumptions, and resulting figures. | Confirm or go back. |
| H2 | Confirms the decision. | Runs the appropriate save/adoption step and records the resulting state. | Confirmation or a message explaining what needs attention. | Continue when confirmation succeeds. |
| H3 | Chooses to change the proposal instead. | Returns to the relevant input or comparison step. | Previous information available for review and editing. | Update and recalculate. |
| H4 | Continues to Strategy Decision. | Passes the goal and feasibility evidence forward. | Goal information ready for the next stage. | Continue to Strategy Decision. |
| H5 | Stops without confirming. | Leaves the unaccepted proposal unadopted. | The option to leave or return later, according to the available workflow. | Exit or resume later. |

## 13. Component I — Return after an input changes

| Changed information | Investor returns to | System updates | Investor reviews next |
|---|---|---|---|
| Target date or target amount | Target and timeline | Affected target, projection, funding gap, contribution, paths, and feasibility | Updated target and result |
| Asset selection or asset value | Asset mapping | Affected asset projection, funding gap, paths, and feasibility | Updated projection and result |
| Income, expenses, or available surplus | Financial capacity | Capacity, contribution fit, relevant paths, and feasibility | Updated capacity and result |
| Debt, EMI, rate, tenure, or financing details | Financial capacity or path comparison | Relevant debt/cash-flow outcomes, affected comparisons, and feasibility | Updated path comparison and result |
| Funding schedule or displayed scenario assumption | Funding-path comparison | Calculations that depend on the changed assumption | Updated path and feasibility |
| Missing or unreliable information | The step that requested the information | Calculations dependent on the corrected evidence | Updated result |

The investor is returned to the nearest relevant step. The system does not make the investor repeat unrelated steps when their information has not changed.

## 14. Example journeys

These examples show the order of the journey. The figures are case inputs; this document does not pre-fill calculated outcomes that have not been established.

### Example A — Retirement goal

**Investor starts with these case details:**
- Retirement horizon: 25 years
- Current corpus: ₹20 lakh
- Required corpus recorded for the case: ₹2 crore
- Monthly income: ₹2 lakh
- Monthly expenses: ₹1.2 lakh
- EMI: ₹10,000
- Approximate monthly surplus: ₹70,000
- Home-loan interest assumption: approximately 8%

**Journey:**

1. Investor enters or reviews the retirement details and target date.
2. System displays the timeline and target information.
3. Investor reviews the mapped corpus and its projected value.
4. System displays the funding gap and the contribution result when calculable.
5. Investor reviews financial capacity and home-loan information.
6. System displays the funding paths supported by the case information, which may include faster repayment, continued retirement investing, and a loan-restructuring path when its inputs are available.
7. Investor compares the resulting goal funding, debt/interest, cash flow, liquidity, assumptions, and trade-offs.
8. Investor reviews the feasibility result and either continues, changes inputs, reviews a proposed goal adjustment if presented, or stops.

### Example B — Education goal

**Investor starts with these case details:**
- Current education cost: ₹20 lakh
- Target horizon: 10 years

**Journey:**

1. Investor enters or reviews the education goal and target date.
2. System displays the timeline and target information based on the configured assumptions.
3. Investor selects any assets to map to the goal.
4. System displays the projected mapped assets and funding gap.
5. Investor reviews required contribution and financial capacity when the relevant information is available.
6. System displays the funding paths it can assess and the resulting feasibility status.
7. Investor reviews the result, changes relevant inputs if needed, and confirms a decision or stops.
8. If the investor continues, the system passes the goal and feasibility evidence to Strategy Decision.

---

**Related implementation contract:** `docs/implementations/Goal-Planner.md`  
This link is provided for the implementation details; those details are not duplicated here.
