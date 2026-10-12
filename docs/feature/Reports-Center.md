# Reports Center

## 1. Main kaam
- Financial plan aur selected goals/strategies ke reports generate/download karna.
- Ek goal ya multiple goals ke liye report scope choose karne dena.
- Investor ko plan aur strategy decisions ka shareable record dena.

## 2. Report options visible in code
- Complete Financial Plan.
- Goal/Strategy report PDF.
- Basket report PDF.
- Summary report PDF.
- Goal-specific report availability selected goal aur strategy version par depend kar sakti hai.

## 3. Inputs
- Defined goals.
- Selected goal.
- Selected strategy version.
- Planning basket/goal selection.
- Report type.

## 4. Process
1. Goals aur available saved baskets load karo.
2. Investor report type aur relevant goal/basket choose kare.
3. Required selected strategy version resolve karo.
4. Relevant report generation/download function call karo.
5. Missing required data ho to report availability/error explain karo.

## 5. Output
- Downloadable PDF report, selected report option ke hisaab se.
- Complete plan, goal/strategy, basket ya summary scope.

## 6. Important boundaries
- Report ek snapshot/presentation hai; khud strategy execute ya Accepted Plan update nahi karta.
- Report available hone ka matlab har underlying calculation business-approved hai, aisa nahi.
- Report mein assumptions, missing inputs aur version/scope clear rehne chahiye.

## 7. Real-Life Decision Case relationships
- **Cases 4 and 9–12:** a better-path recommendation, What-If scenario, rejected proposal, and Accepted Plan are different states. A report of a scenario must not present it as adopted unless adoption is explicitly represented in the source data.
- **Cases 5–8:** goal or strategy changes can make an earlier report stale. Reports should identify the goal/strategy version and, where available, Financial State snapshot/time used.
- Multi-goal/basket reports should preserve report scope; one goal's result must not be presented as whole-plan feasibility without corresponding whole-plan analysis.
- A PDF is evidence/presentation of a result, not an investor approval event.

## 8. Code evidence
- Frontend: `frontend/app/investor/reports/page.tsx`
- Report functions: `frontend/lib/api/strategy`
- Backend report APIs: `backend/api/summary_report.py`, `backend/api/basket_report.py`

## 9. Abhi unverified
- Har report ke PDF contents aur calculations.
- Report snapshot version/time stamp.
- Saved basket persistence: current page local storage key `planvesto:planning-baskets` use karti hai.
- PDF generation errors/availability ke all cases.
- Whether report data carries explicit proposal/Accepted Plan status, adoption timestamp, and financial-state snapshot identifiers.


## 10. Scenario and Accepted Plan representation

Reports Center presents a result; it does not perform investor adoption, approve a strategy or update the Accepted Plan. When source data supports it, identify whether a report represents a recommendation, What-If scenario, rejected/proposed alternative or Accepted Plan. Never label a scenario as adopted without explicit source evidence.

For multi-goal reports, distinguish an individual-goal result from Whole-Plan / Multi-Goal Impact Analysis. One goal's feasibility does not prove combined-plan feasibility. Identify the relevant goal/strategy/plan version and Financial State snapshot/time when available, so stale reports can be recognized after material changes. Whether report payloads carry explicit scenario/adoption state, Accepted Plan version and snapshot identifiers remains unverified.


## 11. Case-derived report states and scope — Cases 4 and 7–12

- **Better-path comparison (Case 4):** distinguish current/appropriate path from the proposed alternative. The case comparison fields are initial asset, return assumption, goal target, estimated goal date, difference in years, required contribution, liquidity, risk and other-goal impact. Its ₹20 lakh initial asset, 6% current-path assumption, 10% alternative-path assumption and ₹50 lakh goal are illustrative scenario inputs, not guaranteed outcomes.
- **New goal (Case 7):** a report for a proposed goal should show incremental impact against the existing plan, not present the new goal as already adopted. Goal-level implementation and Whole-Plan Impact Simulation are distinct scopes.
- **Multiple strategies (Case 8):** a complete financial plan may contain multiple coordinated strategies. A report about one strategy/goal must not imply that it represents the entire plan unless the report scope and analysis cover the whole plan.
- **Execution What-If (Case 9):** an increase/reduction in SIP, deployment of an existing asset or debt-execution change can be reported as a scenario. It is not an accepted instruction or active Action Plan until the investor adopts it.
- **Strategy re-evaluation (Case 10):** distinguish an execution change, a resulting strategy re-evaluation and an actual adopted strategy change.
- **Iterative scenarios (Case 11):** identify the baseline and the tested iteration where the source data supports it; do not imply that every tested iteration was adopted.
- **No acceptable path / investor-designed strategy (Case 12):** a rejected system path, “no acceptable plan under current preferences and constraints,” an investor-designed proposal and an accepted investor-designed plan are distinct states.
- A report/PDF is a presentation record only. It does not constitute investor decision, acceptance, strategy execution or Action Plan update.
- Preserve goal/basket scope, assumptions, Financial State snapshot/time and goal/strategy/plan version where the source data supplies them. Do not invent missing identifiers or adoption state.
