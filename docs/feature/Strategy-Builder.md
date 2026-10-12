# Strategy Builder

## 1. Main kaam
- Goal aur financial context ke basis par strategy run karna.
- Available strategy candidates, recommendation aur relevant architecture/scenario inspect karna.
- Strategy runs/history aur comparison/edit/scenario pages se related workflow support karna.
- Recommendation ko investor decision se alag rakhna.

## 2. Inputs
- Defined goal ya selected planning basket.
- Financial state aur goal context.
- Strategy run request.
- Strategy/scenario/architecture selection.
- Existing strategy run history.

## 3. Canonical business model
- Target decision tree mein chaar canonical strategies hain:
  - Progressive De-risking.
  - Capital Preservation.
  - Debt Reduction.
  - Credit Utilisation.
- Goal Funding fifth Strategy Builder strategy nahi; Goal Planner/feasibility layer ka hissa hai.
- Applicability (relevant hai?) aur viability (actual numbers mein kaam kar sakti hai?) alag checks hain.
- Koi acceptable strategy na ho to force karke select nahi karna.

## 4. Variants and techniques
- Target variant set aur technique mapping source decision-tree document mein listed hain.
- Technique reusable method hai; Solution investor-specific concrete path hai.
- SIP/contribution escalation ko automatically Strategy Builder strategy ya core technique nahi samajhna.
- Target business tree mein listed har variant/technique current code mein implemented hai, aisa assume nahi karna.

## 5. Opportunity Cost se relationship
- Goal Planner/feasibility mein alternative funding paths aur unka opportunity cost assess karne ka business concept documented hai.
- Strategy Builder ko Goal Planner ka feasibility/funding context consume karna chahiye; usi feasibility ko silently independently redefine nahi karna chahiye.
- Strategy Builder meaningful execution alternatives compare kar sakta hai: goal result, contribution, timing, liquidity, debt cost, risk aur competing-goal impact.
- Evidence ke bina kisi alternative ko “better” mat declare karo.
- Current runtime mein Opportunity Cost evidence explicitly pass hota hai ya calculations strategy selection ko affect karti hain, abhi verify nahi.

## 6. Process visible in UI
1. Goal/basket load aur select karo.
2. Strategy run/recommendation load ya generate karo.
3. Available strategy/architecture/scenario details inspect karo.
4. Strategy ya scenario select karke related comparison/edit/history workflows use karo.
5. Result aur trade-offs review karo.
6. Investor acceptance/active-plan update ka exact behavior verify karna baaki hai.

## 7. Output
- Strategy run/recommendation.
- Strategy candidates and relevant rationale/metrics.
- Architecture/scenario data where available.
- Strategy run history.
- Comparison/edit/scenario views via supporting routes.

## 8. Relationship to Accepted Plan and Action Plan
- Generated recommendation, saved scenario, investor adoption, Accepted Plan and Action Plan are separate lifecycle states.
- Canonical target lifecycle: goal feasibility/funding context → Strategy Decision → Variant → Technique/Method → Architecture → Solution → Stress/Resilience and targeted revalidation → Recommendation → Investor Decision → Accepted Plan → Action Plan → Execution.
- A What-If scenario remains isolated from the active Accepted Plan until the investor adopts the revised path.
- Execution changes do not automatically mean the canonical strategy has changed. Re-evaluate strategy only when the changed execution materially affects applicability, viability, constraints or outcomes.
- No acceptable path is a valid outcome. An investor-designed strategy may be evaluated, but it must not be activated merely because no standard candidate passed.

## 9. Taxonomy and decision boundary
- **Strategy:** high-level financial responsibility selected for the situation.
- **Variant:** structural form of the selected strategy.
- **Technique:** reusable mechanism selected because the Strategy + Variant requires it.
- **Method/Policy:** contextual rule for applying a technique.
- **Architecture:** composed structure of selected elements and dependencies.
- **Solution:** investor-specific implementation outcome; it must not merely duplicate a Variant or Technique under another label.
- **Action:** concrete step derived from the accepted implementation.
- Goal Planner owns goal funding feasibility and funding mechanisms. Action Plan owns accepted implementation actions and their execution status. History stores past versions/runs and does not prove current adoption.

## 10. Supporting routes
- Strategy comparison: `/investor/strategy-comparison`
- Strategy edit: `/investor/strategy-edit`
- Strategy history: `/investor/strategy-history`
- Strategy scenarios: `/investor/strategy-scenarios`

## 11. Code evidence
- Frontend: `frontend/app/investor/strategy-builder/page.tsx`
- API: `backend/api/strategy.py`, `backend/api/strategy_edit.py`, `backend/api/strategy_version.py`
- Strategy engine: `backend/engines/strategies` and related engine modules; exact runtime order needs audit.

## 12. Real-Life Decision Case references
- Case 1 and 2: Goal Funding ownership and Goal Planner → Strategy Builder boundary.
- Cases 3–4: feasibility, strategy/implementation design and accepted Action Plan lifecycle.
- Cases 5–8: changed financial state, changed goal intent, new goals and multi-strategy plans.
- Cases 9–11: What-If isolation, impact analysis, targeted revalidation, investor adoption and iterative plan updates.
- Case 12: no acceptable standard path and investor-designed strategy handling.
- Case 15: Asset Mapping vs Asset Earmarking boundary.
- Canonical source: `docs/Decision tree/Real-Life Decision Cases/strategy-decision-tree.md`.

## 13. Abhi unverified
- Exact strategy/variant selection rules and thresholds.
- Opportunity Cost calculation/pass-through/decision impact.
- Complete technique-to-solution mapping.
- Whether Solution has one consistent meaning in the registry/runtime across all strategies.
- Scenario persistence, acceptance and current-plan update.
- Whether all target canonical variants and techniques are active in runtime.
- Stress/resilience, materiality and multi-goal impact rules.
- Exact point at which architecture is composed relative to strategy selection in current runtime.


## 14. Cross-feature concepts within Strategy Builder

### Implementation Design
Strategy Builder owns the strategy-side design from selected Strategy/Variant through Technique, Method/Policy, Architecture and a concrete Solution proposal. The proposal may compare resource use, contributions, timing, liquidity, debt effects and competing-goal consequences where relevant data exists. A Technique is not a Solution, and a Solution proposal is not an Action Plan. Active plan state changes only after explicit investor adoption.

### What-If / Scenario
A What-If scenario is an alternative evaluated against a known baseline. It must remain separate from the active Accepted Plan while being explored. Record baseline, changed inputs/assumptions, projected outcomes and validation status where supported. A saved scenario or report does not prove investor acceptance. The existing scenario route does not by itself prove runtime isolation or persistence.

### Constraint / Safety Evaluation
Constraints define the allowed/restricted decision space before strategy evaluation. Distinguish hard constraints from preferences, blockers from warnings, and failed checks from insufficient inputs. Applicability asks whether a strategy fits; viability asks whether it can work under actual conditions. Exact runtime gates remain to be audited.

### Stress / Resilience Evaluation
The canonical decision tree includes Stress / Resilience before final decision output. It tests whether the proposed path remains acceptable under defined adverse/changed assumptions, including relevant funding, liquidity, debt/EMI and goal-timing effects. It is distinct from applicability, viability and impact analysis. Stress cases, thresholds, warnings versus hard failures, and missing-input behavior remain unverified.

### Investor-designed strategy path
If all standard strategies fail, “No Acceptable Strategy” remains valid; do not force a standard recommendation. Where policy permits, an investor-designed path can be captured as a separate proposal and evaluated against constraints, feasibility, impact and resilience. It is not automatically safe, viable or accepted, and must not be relabelled as one of the four canonical strategies. It becomes active only through the explicit Investor Decision / Accepted Plan lifecycle.

### Technique policy and hierarchy
Technique policy statuses are **Required**, **Conditional**, **Optional**, **Not Applicable** and **Insufficient Inputs**; the last two are not equivalent. Preserve **Strategy → Variant → Technique → Method/Policy → Architecture → Solution → Action**. Goal Funding and Contribution Escalation remain Goal Planner responsibilities; Duration/Horizon Matching is a method, not a separate core technique.

### Impact analysis and debt economics
Whole-Plan / Multi-Goal Impact is conditional when a new goal, existing Accepted Plan, shared-resource conflict or material cross-goal effect makes it relevant; it is not a mandatory gate for every individual-goal strategy decision. Material changes may require targeted revalidation of affected decisions. Debt Reduction/Credit Utilisation analysis may require effective debt cost, repayment terms, EMI capacity, borrowing capacity, financing cost and a credible repayment path. Calculation ownership, materiality thresholds and invalidation rules remain unverified.

Canonical lifecycle: Goal Planner feasibility/funding → Strategy/Variant/Technique/Method → Architecture/Solution proposal → relevant impact and resilience checks → recommendation → explicit Investor Decision → Accepted Plan → Action Plan → execution. This is a business contract, not proof of runtime implementation.


## 15. Canonical Strategy → Variant → Technique registry from the decision tree

The following mappings are transcribed from `docs/Decision tree/Real-Life Decision Cases/strategy-decision-tree.md`. They record the documented target business model; they do not assert that every item is implemented in runtime.

### Progressive De-risking variants
| Situation | Variant |
|---|---|
| Single future goal date | Goal-Date Glide Path |
| Multiple defined future payments | Payment-Tranche Glide Path |
| Recurring future requirement | Recurring-Cashflow Glide Path |
| Accumulation transitioning into recurring income | Income-Transition Glide Path |

### Capital Preservation variants
| Situation | Variant |
|---|---|
| Entire required capital needs protection | Full-Goal Preservation |
| Immediate/next payment needs protection | First-Payment Preservation |
| Repeating reserve requirement | Rolling Reserve Preservation |
| Only core/required capital needs protection | Protected-Core Preservation |

### Debt Reduction variants
| Situation | Variant |
|---|---|
| Debt creates a goal funding gap | Goal-Gap Debt Reduction |
| EMI burden suppresses cash-flow capacity | EMI-Relief Debt Reduction |
| Remaining debt/capital gap needs optimisation | Residual-Gap Debt Reduction |
| Debt and another goal must be coordinated | Goal-Linked Debt Reduction |

### Credit Utilisation variants
| Situation | Variant |
|---|---|
| Small residual funding gap | Residual-Gap Bridge |
| Defined portion intentionally financed | Partial-Goal Financing |
| Borrowing constrained by sustainable EMI | EMI-Cap Financing |
| Temporary timing mismatch | Timing-Bridge Financing |

### Canonical technique set
| Technique | Primary purpose |
|---|---|
| Glide Path | Gradually change risk/capital positioning as a requirement approaches |
| Bucketing | Organize capital/resources by time or liability needs |
| Cash-flow Matching | Match future cash requirements with appropriate resources/cash flows |
| Laddering | Stagger maturities/resources against multiple predictable requirements |
| Asset Earmarking | Designate resources for a specific goal/protected capital pool |
| Goal Segmentation | Separate competing goal/debt/resource requirements |
| Debt Repayment Prioritisation | Determine which debt receives repayment priority |
| Debt Cost Optimisation | Reduce or optimise effective debt cost |
| Debt Prepayment Optimisation | Determine whether available capital should be used for prepayment |
| EMI Capacity Analysis | Determine sustainable repayment capacity |
| Borrowing Capacity Analysis | Determine how much borrowing can responsibly be supported |
| Financing Cost Comparison | Determine whether borrowing is economically justified |

### Variant-to-technique policy matrix

| Strategy / Variant | Required techniques | Conditional techniques |
|---|---|---|
| Progressive De-risking — Goal-Date Glide Path | Glide Path | Bucketing, Cash-flow Matching |
| Progressive De-risking — Payment-Tranche Glide Path | Glide Path, Cash-flow Matching | Bucketing |
| Progressive De-risking — Recurring-Cashflow Glide Path | Bucketing, Cash-flow Matching | Glide Path |
| Progressive De-risking — Income-Transition Glide Path | Glide Path, Bucketing | Cash-flow Matching |
| Capital Preservation — Full-Goal Preservation | Bucketing, Asset Earmarking | Cash-flow Matching, Laddering |
| Capital Preservation — First-Payment Preservation | Cash-flow Matching, Bucketing | Asset Earmarking |
| Capital Preservation — Rolling Reserve Preservation | Bucketing, Cash-flow Matching | Laddering |
| Capital Preservation — Protected-Core Preservation | Asset Earmarking, Bucketing | Cash-flow Matching, Laddering |
| Debt Reduction — Goal-Gap Debt Reduction | Goal Segmentation, Debt Repayment Prioritisation | Debt Cost Optimisation, Cash-flow Matching, Debt Prepayment Optimisation |
| Debt Reduction — EMI-Relief Debt Reduction | EMI Capacity Analysis, Debt Cost Optimisation | Debt Repayment Prioritisation, Debt Prepayment Optimisation |
| Debt Reduction — Residual-Gap Debt Reduction | Goal Segmentation, Cash-flow Matching | Debt Repayment Prioritisation, Debt Cost Optimisation, Debt Prepayment Optimisation |
| Debt Reduction — Goal-Linked Debt Reduction | Goal Segmentation, Cash-flow Matching | Debt Cost Optimisation, Debt Prepayment Optimisation |
| Credit Utilisation — Residual-Gap Bridge | Borrowing Capacity Analysis, Financing Cost Comparison | Cash-flow Matching, EMI Capacity Analysis |
| Credit Utilisation — Partial-Goal Financing | Financing Cost Comparison, Goal Segmentation | Borrowing Capacity Analysis, EMI Capacity Analysis |
| Credit Utilisation — EMI-Cap Financing | EMI Capacity Analysis, Borrowing Capacity Analysis | Financing Cost Comparison |
| Credit Utilisation — Timing-Bridge Financing | Cash-flow Matching, Financing Cost Comparison | Borrowing Capacity Analysis, EMI Capacity Analysis |

Technique policy statuses are **Required**, **Conditional**, **Optional**, **Not Applicable** and **Insufficient Inputs**. **Not Applicable** and **Insufficient Inputs** are not equivalent. Laddering is conditional, not a default Capital Preservation technique; it applies where multiple predictable maturity/payment dates justify staggered maturities.

### Technique and taxonomy exclusions recorded by the source
- Contribution Escalation belongs to Goal Planner / Goal Funding, not the core Strategy Decision Tree.
- Duration / Horizon Matching is a decision/analysis method, not a separate core technique.
- Tax-specific techniques such as Tax-Efficient Sequencing and Tax-Loss Harvesting are not forced into the four-strategy decision tree; the source places them in the appropriate investment/tax implementation layer unless a later business decision promotes them.
- A Technique is not a Solution. A Solution is the investor-specific concrete implementation outcome and must not merely duplicate a Variant or Technique under another label.

## 16. Canonical rejection conditions and no-acceptable-path outcome

### Credit Utilisation rejection conditions
Credit fails when borrowing capacity is insufficient, EMI is unsustainable, financing cost is unjustified, repayment path is undefined, borrowing merely transfers an existing debt problem into another form, or hard financial constraints are violated.

### Strategy selection boundaries
- Debt Reduction is not selected merely because debt exists; the source ties it to material improvement in cash-flow capacity, goal funding, affordability or resilience.
- Capital Preservation is not selected merely because a goal exists; it becomes primary when capital has become protection-sensitive.
- Progressive De-risking is not selected merely because a goal has a future date; the source requires a meaningful future requirement where gradual risk reduction improves the probability of meeting it.
- If all candidate strategies fail applicability/viability, **No Acceptable Strategy** is a valid outcome, not a system error. The system must not force a strategy merely to produce a recommendation.

## 17. Goal-specific situation mapping in the canonical source

| Goal | Situation | Strategy | Variant |
|---|---|---|---|
| Retirement | Long accumulation horizon | Progressive De-risking | Goal-Date Glide Path |
| Retirement | Required retirement capital needs protection | Capital Preservation | Protected-Core Preservation |
| Retirement | Income transition | Progressive De-risking | Income-Transition Glide Path |
| Retirement | Debt suppresses retirement funding | Debt Reduction | EMI-Relief Debt Reduction |
| Marriage | Several years away | Progressive De-risking | Goal-Date Glide Path |
| Marriage | Capital ready and date near | Capital Preservation | Full-Goal Preservation |
| Marriage | Multiple scheduled payments | Progressive De-risking | Payment-Tranche Glide Path |
| Marriage | Existing debt suppresses funding | Debt Reduction | Goal-Gap Debt Reduction |
| Vehicle | Purchase several years away | Progressive De-risking | Goal-Date Glide Path |
| Vehicle | Purchase near and capital ready | Capital Preservation | Full-Goal Preservation |
| Vehicle | Existing EMI affects affordability | Debt Reduction | EMI-Relief Debt Reduction |
| Vehicle | Partial financing justified | Credit Utilisation | Partial-Goal Financing |
| Dream Home | Down-payment accumulation | Progressive De-risking | Goal-Date Glide Path |
| Dream Home | Purchase approaching, core capital ready | Capital Preservation | Protected-Core Preservation |
| Dream Home | Existing debt reduces affordability | Debt Reduction | EMI-Relief Debt Reduction |
| Dream Home | Defined financing requirement | Credit Utilisation | Partial-Goal Financing |
| Dream Home | Gap too large / EMI unsustainable | No acceptable path | — |
| Education | Long education horizon | Progressive De-risking | Goal-Date Glide Path |
| Education | Staged education payments | Progressive De-risking | Payment-Tranche Glide Path |
| Education | Next tuition payment near | Capital Preservation | First-Payment Preservation |
| Education | Core capital needs protection | Capital Preservation | Protected-Core Preservation |
| Education | Responsible residual gap | Credit Utilisation | Residual-Gap Bridge |
| Education | Defined portion intentionally financed | Credit Utilisation | Partial-Goal Financing |
| Education | Existing debt suppresses funding | Debt Reduction | Goal-Gap Debt Reduction |
| Vacation | Future accumulation | Progressive De-risking | Goal-Date Glide Path |
| Vacation | Near-term and funds available | Capital Preservation | Full-Goal Preservation |
| Vacation | Recurring requirement | Progressive De-risking | Recurring-Cashflow Glide Path |
| Vacation | Existing debt creates pressure | Debt Reduction | EMI-Relief Debt Reduction |
| Vacation | Financing unaffordable | No acceptable path | — |
| Debt Freedom | High-cost debt priority | Debt Reduction | Goal-Gap Debt Reduction |
| Debt Freedom | EMI burden too high | Debt Reduction | EMI-Relief Debt Reduction |
| Debt Freedom | Multiple debts need ordering | Debt Reduction | Goal-Gap / Goal-Linked |
| Debt Freedom | Debt payoff competes with another goal | Debt Reduction | Goal-Linked Debt Reduction |
| Debt Freedom | New expensive borrowing required | No acceptable Credit path | — |
| Wealth Creation | Long-term accumulation | Progressive De-risking | Goal-Date Glide Path |
| Wealth Creation | Target approaching | Capital Preservation | Protected-Core Preservation |
| Wealth Creation | High-cost debt suppresses accumulation | Debt Reduction | Goal-Gap Debt Reduction |
| Wealth Creation | Defined leverage with sustainable repayment | Credit Utilisation | EMI-Cap Financing |
| FIRE / Passive Income | Long accumulation | Progressive De-risking | Income-Transition Glide Path |
| FIRE / Passive Income | Target approaching | Capital Preservation | Protected-Core Preservation |
| FIRE / Passive Income | Passive-income transition | Progressive De-risking | Income-Transition Glide Path |
| FIRE / Passive Income | Debt reduces passive-income cash flow | Debt Reduction | EMI-Relief Debt Reduction |
| FIRE / Passive Income | Recurring withdrawals started | Capital Preservation | Rolling Reserve Preservation |
| FIRE / Passive Income | Unsustainable borrowing required | No acceptable path | — |
| Others | Fixed future requirement | Progressive De-risking | Goal-Date Glide Path |
| Others | Immediate capital requirement | Capital Preservation | Full-Goal Preservation |
| Others | Debt materially constrains objective | Debt Reduction | Goal-Gap Debt Reduction |
| Others | Sustainable residual gap | Credit Utilisation | Residual-Gap Bridge |
| Others | No strategy satisfies constraints | No acceptable strategy | — |

## 18. Investor strategy change, multi-strategy plans and investor-designed mode

- A complete financial plan can contain multiple coordinated strategies simultaneously across different goals/financial requirements. Two alternatives shown for one decision do not mean the full plan can contain only two strategies.
- Recommendation is guidance; investor choice determines the accepted path, subject to genuine hard constraints. Distinguish hard constraints from advisory priorities.
- Strategy change does not automatically require full-plan replacement. Revalidate affected strategy/goal decisions and update relevant implementation/actions if the investor adopts the change.
- Case 12 defines **No Acceptable Path** as a valid state when no proposed path is acceptable under current preferences/constraints; the system must not force a recommendation.
- If the investor wants to design their own strategy, preserve it as a separate investor-designed proposal, evaluate it against constraints, feasibility, impact and resilience, and explain numerical consequences. Investor-designed does not mean guidance-free, automatically viable, safe or accepted; it must not be relabelled as one of the four canonical strategies.
- The source records the lifecycle: Financial State + Investor Intent/Goals → Goal Planning/Feasibility → Strategy Decision → Implementation Design → Stress/Resilience → Decision/Recommendation → Investor Decision → Accepted Plan → Action Plan → Execution. Whole-Plan/Multi-Goal Impact is conditional on a plan-level decision.
- Case source conflicts are retained rather than silently resolved: Case 8's header says Goal Funding is not a Strategy Builder strategy, while its body labels Goal Funding as “Strategy A”; Cases 10–11 also use Goal Funding as a strategy in places. The Full Audit Report records these inconsistencies. The canonical Strategy Decision Tree classifies Goal Funding under Goal Planner/Goal Feasibility, not among the four strategies.

## 19. Source status and traceability
- Canonical source: `docs/Decision tree/Real-Life Decision Cases/strategy-decision-tree.md`.
- Related cases: `00-GOAL_FUNDING_CONCEPT_CHANGE_LOG.md`, Cases 3–12, and Case 15 Asset Mapping vs Asset Earmarking.
- This section records the target business taxonomy and case decisions; it does not assert implementation.
- The Full Audit Report records an inconsistent meaning of `Solution` in runtime: Goal Funding solution records wrap a Variant, while records for the other four strategies wrap a Technique. This is a source-reported audit finding, not a claim of correction.
- “Canonical/final” and “not frozen” statuses differ across source documents; preserve each source status until explicitly reconciled.


### Source discrepancies recorded in the Full Audit Report

The source audit records these contradictions; they are preserved here as unresolved source facts, not silently reconciled:
- **Case 3:** its main body places Action Plan before Strategy Builder, while the canonical lifecycle places Strategy Decision/Implementation Design before Investor Decision, Accepted Plan and Action Plan.
- **Case 8:** its header says Goal Funding is not a Strategy Builder strategy, while its body labels Goal Funding as “Strategy A”.
- **Cases 10–11:** the bodies describe Goal Funding/funding-path changes using strategy-change language, although the audit says a funding-path change should first be modelled as such and not assumed to be a canonical strategy change.
- **Solution taxonomy in current runtime:** the audit reports Goal Funding solution records wrap a Variant, while records for the other four strategies wrap a Technique. This is an implementation finding in the source audit, not a corrected runtime behavior.
- **Status terminology:** the source set uses “canonical”, “final” and “not frozen” without a single shared status model; this feature does not infer a unified status beyond what each source explicitly states.


### Case 4 — better-path implementation comparison
The source case compares a current/appropriate path with a proposed alternative after the goal is already feasible. Comparison fields are initial asset, return assumption, goal target, estimated goal date, difference in years, required contribution, liquidity, risk and other-goal impact. Its illustrative inputs are ₹20 lakh initial asset, 6% current-path return assumption, 10% alternative-path return assumption and ₹50 lakh goal target. These are scenario assumptions, not guaranteed returns. The investor can test implementation using their own financial numbers; generating the alternative does not adopt it.


### Case 8 — recorded investor strategy-change example
The source example uses an outstanding loan with an 18% cost. The system may give Debt Reduction strong advisory priority, but where that is not a genuine hard constraint, the investor may choose to invest instead after seeing the trade-offs. The comparison may include debt cost, expected investment outcome/assumption, liquidity, risk, goal funding, cash-flow impact, other-goal impact and resulting Action Plan changes. The system recalculates and revalidates the investor-selected path; it does not silently block the choice or replace the plan before adoption. The 18% rate is a case example, not a default threshold.
