# Strategy Builder

## 1. Main kaam
- Goal Planner se feasibility/funding result lena.
- Suitable strategy aur uska variant select karna.
- Required techniques aur unke use ka tareeka decide karna.
- Parts ko investor ke actual numbers ke saath implementation path mein jodna.
- Risks, trade-offs aur relevant goals par impact samjhana.
- Recommendation dena; investor ke accept karne se pehle plan automatically replace nahi karna.
- Goal Planner ka feasibility calculation dobara nahi karna.

## 2. Inputs
- Goal aur actual requirement.
- Goal Planner ka funding gap/feasibility result.
- Financial situation, assets, debt, EMI, monthly surplus aur liquidity.
- Goal timeline aur capital protection ki zaroorat.
- Genuine restrictions.
- Investor preferences aur accepted trade-offs.
- Strategy sirf goal ke naam se select nahi honi chahiye.

## 3. Chaar canonical strategies

### Progressive De-risking
- Future goal ke nazdeek aane par risk dheere-dheere kam karna useful ho.
- Example: education payment ki date paas aane par required capital ko zyada protect karna.

### Capital Preservation
- Required capital ya uske hissa ko loss/timing risk se bachana priority ho.
- Example: agle tuition payment ke liye zaroori paisa protect karna.

### Debt Reduction
- Debt cash flow, affordability ya goal funding ko materially affect kare.
- Debt ghatane/badalne se financial position improve ho sakti ho.
- Sirf debt hone se yeh strategy automatic select nahi hoti.

### Credit Utilisation
- Genuine funding/timing gap ho aur borrowing sustainable ho.
- Check karo: existing resources consider hue, borrowing capacity sufficient hai, EMI sustainable hai, financing cost justified hai, repayment path credible hai.
- Zaroori gate fail ho to Credit Utilisation recommend mat karo.

- Goal Funding fifth strategy nahi; woh Goal Planner ka kaam hai.

## 4. Applicability vs viability
- **Applicability:** Kya strategy is situation mein relevant hai?
- **Viability:** Kya strategy investor ke numbers aur restrictions mein kaam kar sakti hai?
- Har candidate ke liye reason dikhana: kyun fit hoti hai, kyun fail hoti hai, aur selected strategy kyun choose hui.
- Koi acceptable strategy na ho to force karke select mat karo.

## 5. Canonical variants

| Strategy | Variant |
|---|---|
| Progressive De-risking | Goal-Date Glide Path |
| Progressive De-risking | Payment-Tranche Glide Path |
| Progressive De-risking | Recurring-Cashflow Glide Path |
| Progressive De-risking | Income-Transition Glide Path |
| Capital Preservation | Full-Goal Preservation |
| Capital Preservation | First-Payment Preservation |
| Capital Preservation | Rolling Reserve Preservation |
| Capital Preservation | Protected-Core Preservation |
| Debt Reduction | Goal-Gap Debt Reduction |
| Debt Reduction | EMI-Relief Debt Reduction |
| Debt Reduction | Residual-Gap Debt Reduction |
| Debt Reduction | Goal-Linked Debt Reduction |
| Credit Utilisation | Residual-Gap Bridge |
| Credit Utilisation | Partial-Goal Financing |
| Credit Utilisation | EMI-Cap Financing |
| Credit Utilisation | Timing-Bridge Financing |

- Yeh target business tree ki list hai; current code mein sab variants implemented hone ka proof nahi.

## 6. Techniques
- **Glide Path:** goal nazdeek aane par risk/capital position dheere-dheere badalna.
- **Bucketing:** paisa ko time ya need ke hisaab se groups mein rakhna.
- **Cash-flow Matching:** future payments ko suitable resources/cash flow se match karna.
- **Laddering:** alag payment dates ke liye maturities/resources ko stagger karna.
- **Asset Earmarking:** asset ya uske hissa ko goal ke liye reserve/protect karna.
- **Goal Segmentation:** goals, debt aur resource needs ko alag samajhna.
- **Debt Repayment Prioritisation:** kaunsa debt pehle repay karna munasib hai.
- **Debt Cost Optimisation:** debt cost reduce/optimise karne ke options.
- **Debt Prepayment Optimisation:** extra cash se early repayment ka benefit compare karna.
- **EMI Capacity Analysis:** sustainable EMI capacity assess karna.
- **Borrowing Capacity Analysis:** responsibly kitna borrow ho sakta hai.
- **Financing Cost Comparison:** loan cost ko alternatives se compare karna.
- Har technique har case mein required nahi. Status: required, conditional, optional, not applicable, ya information insufficient.
- Technique ek tareeka hai; Solution investor ke numbers se nikla concrete path hai.
- SIP/contribution escalation Goal Planner ke funding mechanisms hain; inhe automatically Strategy Builder strategy/technique mat samjho.

## 7. Asset Mapping vs Asset Earmarking
- **Asset Mapping:** Goal Planner mein asset ko planning ke liye goal se associate karna.
- **Asset Earmarking:** strategy/implementation ke context mein asset ko reserve/protect karna.
- Mapping ka matlab asset locked, sold ya protected hona nahi.
- Same asset ko competing goals ke liye reserve karne par conflict dikhana.
- Earmarking ka matlab particular investment product kharidna nahi.

## 8. Decision output
- Goal aur assessed situation.
- Goal Planner ka feasibility/funding result.
- Genuine restrictions.
- Applicable strategies aur rejected/failed strategies ke reasons.
- Selected strategy aur variant, reasons ke saath.
- Required/conditional techniques.
- Investor ke numbers par based concrete Solution.
- Risks, benefits, trade-offs aur other-goal impact.
- Investor ka accept/reject/modify decision.

## 9. Current path vs alternative
- Goal feasible hone ka matlab current path hi best hona nahi.
- Meaningful alternative ho to current aur alternative path compare karo.
- Compare: projected goal result, required contribution, time to goal, liquidity, risk, debt cost aur other-goal impact.
- Evidence ke bina alternative ko “better” mat bolo.
- Returns assumptions hain, guarantees nahi.

## 10. Multiple strategies in one plan
- Ek investor ke alag goals ke liye alag strategies ho sakti hain.
- Example: Education, Retirement aur debt ke liye alag strategies.
- Same money/cash flow compete kare to combined plan impact check karo.
- Ek decision ke alternatives ka matlab poore plan mein sirf do strategies allowed hona nahi.

## 11. Investor ka decision
- System recommendation aur trade-offs explain kare; force na kare, jab tak genuine hard constraint block na kare.
- Strategy change proposal hai; investor accept kare tabhi Accepted Plan ka hissa bane.
- Alternative reject ho to existing Accepted Plan automatically overwrite na ho.
- Investor apna path design kar sakta hai:
  - investor approach aur numbers deta hai;
  - system structure, calculation, risks aur trade-offs samjhata hai;
  - genuine restrictions check hoti hain;
  - accept hone se pehle path active plan nahi banta.

## 12. Strategy vs execution vs what-if
- **Strategy:** overall approach.
- **Execution:** amount, timing aur implementation actions.
- Execution number change hone ka matlab zaroori nahi strategy change hona.
- Pehle execution impact calculate karo.
- Existing strategy suitable na rahe to re-evaluation trigger karo.
- System chupke se strategy replace na kare.
- What-if aur Accepted Plan alag rahen.
- Investor scenario accept kare tabhi Execution Plan/Action Plan update hon.

## 13. Revalidation
- Har change par poora plan rebuild karna zaroori nahi.
- Check karo: kya badla, kaunsa goal/strategy directly affected hai, aur kaun se dependencies materially affected hain.
- Affected parts re-check karo; broader impact ho to whole-plan validation.
- Flow: execution what-if → impact → strategy re-check if needed → investor decision → accepted plan update.
- Completed actions history mein rahen; active/future actions zaroorat par revise hon.

## 14. No acceptable strategy
- “No acceptable strategy” valid result hai, system error nahi.
- Recommendation ke liye strategy force mat karo.
- Explain karo kaunsi condition acceptable path rok rahi hai aur kya badalne se situation improve ho sakti hai.
- Investor-designed path bhi impact aur hard-constraint checks se guzrega.
- Accepted hone se pehle woh active plan nahi hai.

## 15. Target business flow
- Goal Planner feasibility/funding result.
- Genuine restrictions check.
- Strategy applicability → strategy viability → strategy selection.
- Variant → technique → technique ka use.
- Architecture: selected parts ko ek structure mein jodna.
- Solution: investor ke numbers se nikla concrete path.
- Stress/resilience check.
- Recommendation aur reason.
- Investor accept/reject/modify.
- Accepted Plan → Action Plan → Execution.
- Yeh target flow hai; current code isi order mein chalta hai, iska proof nahi.

## 16. Abhi unverified
- Exact strategy/variant selection rules.
- Required/conditional technique rules.
- Calculation/comparison formulas.
- Strategy conflicts solve karne ke rules.
- Stress/resilience limits.
- Material-impact thresholds.
- What-if save/compare/accept implementation.
- Accepted Plan/Action Plan ka code-level behaviour.

## 17. Source documents
- `strategy-decision-tree.md` — strategies, variants, techniques aur decision flow.
- `00-GOAL_FUNDING_CONCEPT_CHANGE_LOG.md` — Goal Funding boundary.
- `03-CASE_3_MULTI_GOAL_FEASIBILITY_AND_ACTION_PLAN.md` — multi-goal impact.
- `04-CASE_4_BETTER_PATH_STRATEGY_AND_IMPLEMENTATION.md` — current vs alternative path.
- `05-CASE_5_PLAN_ADAPTATION_AFTER_FINANCIAL_STATE_CHANGE.md` — financial changes.
- `06-CASE_6_GOAL_INTENT_CHANGE_AND_RECALCULATION.md` — goal changes.
- `07-CASE_7_NEW_GOAL_AGAINST_EXISTING_PLAN.md` — new goal scenario.
- `08-CASE_8_INVESTOR_STRATEGY_CHANGE_AND_MULTI_STRATEGY_PLAN.md` — investor choice/multiple strategies.
- `09-CASE_9_EXECUTION_PLAN_WHAT_IF_AND_IMPACT_GUIDANCE.md` — execution what-if.
- `10-CASE_10_EXECUTION_CHANGE_TRIGGERING_STRATEGY_REEVALUATION.md` — strategy re-evaluation.
- `11-CASE_11_ITERATIVE_STRATEGY_EXECUTION_AND_REVALIDATION.md` — iterative loop.
- `12-CASE_12_NO_ACCEPTABLE_PATH_AND_INVESTOR_DESIGNED_STRATEGY.md` — no acceptable path/investor-designed strategy.
- `15-CANONICAL_ASSET_MAPPING_VS_ASSET_EARMARKING_DECISION_CASE.md` — mapping vs earmarking.
- `FULL_AUDIT_REPORT.md` — conflicts and implementation limitations.
