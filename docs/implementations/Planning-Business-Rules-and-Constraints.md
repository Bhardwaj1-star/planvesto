# Planning Rules & Constraints — Financial Planner Guide

## 1. Why this guide exists

This is the cross-feature reference for financial planners using Planvesto. It explains:

- Which financial and planning rules currently exist in the backend code.
- What each rule means in day-to-day planning.
- Which feature uses the rule and what effect it can have.
- What information is needed before the rule can be applied.
- Where the current system has gaps, inconsistent thresholds, or behavior that needs confirmation.

**This is a code-audited guide, not a promise that every planned workflow is fully implemented.** The values below are the values found in the audited code. They are not universal financial-advice standards and should not be presented as guaranteed outcomes.

### How to interpret a rule

| Label | Meaning for the planner |
|---|---|
| **Hard constraint** | A condition that can block a specific planning path or make it unacceptable. |
| **Eligibility check** | Tests whether a strategy can be considered or can proceed conditionally. |
| **Warning** | Flags a concern for review; it does not automatically block a decision. |
| **Measurement / evidence** | Describes the investor's financial position. It becomes a blocker only if a separate rule says so. |
| **Calculation / classification** | Calculates or categorizes information used by a later decision. |
| **Missing evidence** | Required information is unavailable, so the planner should not assume the check passed. |

A **Critical ratio is not automatically a hard failure**. The rule that consumes the ratio determines whether it becomes a warning, a constraint, or simply evidence.

---

## 2. How the planning features work together

| Feature / component | Its responsibility | What it contributes to a decision |
|---|---|---|
| **Financial State** | Holds the investor's financial information and cash-flow picture. | Income, expenses, assets, liabilities and related financial inputs. |
| **Moneywheel (including financial-health assessment)** | Calculates and interprets governed financial measurements. | Ratios, status bands, data availability and financial-health evidence. |
| **Goal Planner** | Defines a goal's future requirement and funding position. | Goal target, timeline, mapped-resource projection, funding gap and contribution requirement. |
| **Goal Feasibility** | Assesses whether a goal's funding path is workable under relevant conditions. | Feasibility result, reasons, constraints and funding-path context. Goal Funding belongs here—not as a fifth Strategy Builder strategy. |
| **Constraint / Safety Evaluation** | Checks applicable rules, warnings, preferences, conflicts and missing evidence. | What a proposal must respect, what needs review and which evidence is incomplete. |
| **Risk Profiler** | Assesses required risk against observable financial capacity and, separately, behavioral evidence. | Risk-related evidence and conditional/fail outcomes where supported. |
| **Strategy Builder** | Evaluates the four canonical strategies and prepares two options. | Applicability, viability, variants, techniques, solution proposals and trade-offs. |
| **Action Plan / Accepted Plan** | Separates a proposal from an adopted plan and its actions. | Actions follow the relevant investor decision; a preview is not acceptance or execution. |

### Planner's end-to-end review

1. Confirm the investor's financial information is current and usable.
2. Review Moneywheel measurements and note unavailable ratios.
3. Confirm the canonical goal, its priority, target date and assumptions.
4. Review Goal Planner's future target, mapped assets, projected funding and gap.
5. Review Goal Feasibility and all applicable hard constraints, warnings and missing evidence.
6. Where relevant, check risk capacity and effects on other goals or shared resources.
7. Review Strategy Builder's two options, their applicability and viability, and their trade-offs.
8. Keep proposal, investor acceptance, Accepted Plan and execution as separate states.
9. Recalculate or revalidate affected decisions when material inputs change.

Do not assume that every feature automatically receives every constraint. The shared constraint aggregator accepts optional sources; the actual call path must supply the relevant evidence.

---

## 3. The shared constraint framework

The backend has a common constraint framework, but **not all rules and thresholds are centralized in it**.

| Code location | Role in the system | Planner-level meaning | Current limitation |
|---|---|---|---|
| `backend/engines/constraints/models.py` | Defines the shared constraint record format. | Provides a common structure for rule identity, source, severity, role, evidence, validity and optional goal association. | A common format does not mean every rule is defined here. |
| `backend/engines/constraints/policy.py` | Owns selected rule IDs, thresholds, priority ranks, source priority and helper policies. | Central policy reference for some of the system's shared rules. | Only part of the business rulebook is centralized here. |
| `backend/engines/constraints/aggregator.py` | Combines available constraint results from several sources. | Brings supplied rule-engine, ratio, Moneywheel, risk and strategy outputs together. | Sources are optional; omitted sources cannot contribute their constraints to that aggregation. |
| `backend/engines/constraints/adapters.py` | Converts domain results into the common constraint format. | Makes results from different features comparable in a shared structure. | An adapter translates a rule result; it does not own the underlying business decision. |
| `backend/rules/canonical.py` | Registers canonical rule metadata such as identity, scope and role. | Helps identify the intended rule catalogue. | It is not a complete record of every active runtime rule or threshold. |
| `backend/rules/constraints.py` | Re-exports selected policy symbols for older callers. | Compatibility path for older code. | It should not be treated as a second intended policy owner. |

### How constraint information is handled

- A constraint may include its source, evidence, confidence, validity period and relationship to a goal.
- Recognized source categories include financial state, observed behavior, declared constraints and preferences.
- Source priority in the audited policy is: financial state **4**, observed behavior **3**, declared constraint **2**, preference **1**.
- If confidence is missing, a helper derives it from source priority and evidence count.
- If the same constraint key has conflicting values, the helper records an **unresolved conflict**; it does not automatically know which value is correct.
- Priority validation rejects unknown keys, duplicate keys, non-integer ranks below 1 and duplicate ranks.
- Behavioral observations require a supported dimension and evidence. Missing observations remain insufficient evidence; the system should not invent a behavioral score.
- The audited observed-behavior policy marks behavioral constraints for **product selection only**. They should not silently become goal-feasibility blockers.

**Planner action:** if an important constraint is absent from a result, do not conclude that the investor passed it. First confirm that the relevant source was available and passed into the decision.

---

## 4. Moneywheel / Financial Health measurements

The canonical ratio list is in `backend/rules/moneywheel.py`; calculations and status assignment are handled by the Moneywheel engine and related calculation functions.

### 4.1 Current ratio bands in code

| Measurement | Calculation used by code | Excellent | Healthy | Attention | Critical |
|---|---|---:|---:|---:|---:|
| **Savings Rate** | (Income − Expenses) ÷ Income × 100 | ≥30% | ≥20% and <30% | ≥10% and <20% | <10% |
| **Liquid Asset Ratio** | Liquid assets ÷ total assets × 100 | ≥25% | ≥15% and <25% | ≥10% and <15% | <10% |
| **Debt-to-Income Ratio** | Monthly debt payments ÷ gross monthly income × 100 | <20% | ≥20% and <30% | ≥30% and <40% | ≥40% |
| **Leverage Ratio** | Total liabilities ÷ total assets × 100 | <20% | ≥20% and <30% | ≥30% and <50% | ≥50% |
| **Financial Asset Ratio** | Financial assets ÷ total assets × 100 | ≥70% | ≥50% and <70% | ≥30% and <50% | <30% |
| **Insurance Coverage Ratio** | Existing sum assured ÷ required cover × 100 | ≥80% | ≥60% and <80% | ≥40% and <60% | <40% |
| **Goal Funding Ratio** | Current goal funding ÷ goal target × 100 | ≥100% | ≥80% and <100% | ≥50% and <80% | <50% |
| **Future Funding Ratio** | Projected goal funding ÷ future goal target × 100 | ≥100% | ≥80% and <100% | ≥50% and <80% | <50% |
| **Required Rate of Return** | Annualized return implied by target, current funding and duration | <8% | ≥8% and <12% | ≥12% and <15% | ≥15% |

### 4.2 How a planner should use these measurements

- **Savings Rate:** indicates how much of income remains after expenses. An attention/critical status can create a savings warning; it is not automatically a strategy decision.
- **Liquid Asset Ratio:** describes the liquid portion of total assets. It is not, by itself, a hard block on a goal.
- **Debt-to-Income:** indicates debt-payment burden relative to gross income. In a separate evaluator, a high value can constrain certain high-priority discretionary goals.
- **Leverage:** describes liabilities relative to assets. Its status band is evidence; check the downstream rule before treating it as a blocker.
- **Financial Asset Ratio:** describes financial assets as a share of total assets.
- **Insurance Coverage:** compares existing sum assured with the code's required-cover calculation.
- **Goal Funding / Future Funding:** compare current or projected funding with a goal's target. Confirm the target date and assumptions before interpreting the result.
- **Required Rate of Return:** indicates the return implied by the target and funding assumptions. It is **not a forecast, guarantee or permission to take excessive risk**.

### 4.3 Missing data rule

If required inputs are missing, a denominator is zero, or a calculated result is not finite, Moneywheel marks the ratio unavailable and records a reason rather than manufacturing a number.

An unavailable ratio is not the same as a healthy ratio. Resolve or disclose the missing input before relying on that measurement.

### 4.4 Additional reserve, debt and goal checks

| Rule | Current code behavior | Effect for the planner |
|---|---|---|
| Emergency reserve below 3 months | Classified as critical by the ratio evaluator. Certain high/critical-priority discretionary goals can receive a failed hard constraint and a suggested priority reduction to Low. | May constrain the affected discretionary goal; it does not automatically make every goal infeasible. |
| Emergency reserve below the 6-month healthy benchmark, but not critical | Produces a warning. | Requires review; it is not the same as a hard failure. |
| Emergency reserve at least 9 months | Evaluator has a separate excellent band. | This band is hardcoded in the evaluator rather than fully owned by the shared policy. |
| Debt-to-income ≥40% | Classified as critical; certain high/critical-priority discretionary goals can receive a failed hard constraint and suggested priority reduction to Low. | Can constrain the relevant discretionary goal. |
| Debt-to-income 30% to below 40% | Produces a warning. | Review debt burden and affordability; warning is not automatically a block. |
| Savings rate in attention/critical bands | Can produce a warning that expense reduction may be needed. | Advisory warning, not a hard block by itself. |
| Goal horizon must be positive | Zero or negative duration fails the validity check. | Confirm the goal date; a past date is not a valid future funding horizon. |
| Future goal target must be positive | A non-positive target fails the validity check. | Correct or confirm the target before planning. |

### 4.5 Threshold ownership gaps

- Savings, debt and leverage bands are not all owned by one central policy file.
- The evaluator has its own reserve bands, including the 9-month excellent threshold.
- Some benchmark values are repeated in the canonical policy, Moneywheel rules and evaluator.
- The rule catalogue may describe a ratio as evidence while a separate evaluator gives it a goal-specific blocking effect.

These are centralization and consistency gaps identified in code, not evidence that every threshold is currently producing the same result in every feature.

---

## 5. Canonical goals, priorities and essential/discretionary rules

### 5.1 Canonical goal list

The backend's canonical goal taxonomy is:

1. Retirement
2. Marriage
3. Vehicle
4. Dream Home
5. Education
6. Vacation
7. Debt Freedom
8. Wealth Creation
9. FIRE / Passive Income
10. Others

The **goal type is the canonical identity**. A beneficiary, child, purpose detail or other circumstance should be stored as context rather than becoming a new goal type. For example, “child education” should be represented as the Education goal with relevant beneficiary/context details—not as a separate canonical goal.

The normalizer accepts canonical IDs or display names case-insensitively. Unknown values normalize to an empty canonical type; they should be validated rather than silently turned into a new goal.

### 5.2 Priority rules

- Canonical priorities: **Critical, High, Medium, Low**.
- Recognized alternate labels such as “must-have”, “important”, “moderate”, “aspirational”, “nice-to-have” and “discretionary” are normalized to canonical levels.
- Missing or unrecognized priority currently defaults to **Medium** in `canonical_goal_priority()`.
- Shared priority ranks are **Critical = 0, High = 1, Medium = 2, Low = 3**. Lower number means higher precedence.

**Planner caution:** a missing priority can therefore become Medium without the planner explicitly choosing it. Confirm the priority where it materially affects a decision.

### 5.3 Current essential/discretionary classification in code

| Classification | Goal types |
|---|---|
| **Discretionary** | Vehicle, Dream Home, Vacation, Wealth Creation, Others |
| **Essential** | Retirement, Marriage, Education, Debt Freedom, FIRE / Passive Income |

The policy says a discretionary goal must not preempt an essential goal or safety-reserve funding.

**Limitation:** the classification is fixed in code. It may not reflect every investor's circumstances; for example, a vehicle may be essential for one investor and discretionary for another. Treat this as a current system classification, not a complete human judgement.

---

## 6. Goal Planner rules and calculations

The main calculation logic is in `backend/engines/goal/engine.py` and its target, funding-gap and asset-projection helpers, with assumptions and shared calculation functions in related modules.

| Rule / calculation | What the code currently does | What the planner should verify |
|---|---|---|
| **Goal identity** | Normalizes the goal to the canonical taxonomy. | Confirm the correct canonical goal; keep beneficiary/purpose in contextual details. |
| **Goal duration** | Calculates remaining months from the target month/year and reference date. A past date produces zero duration. | Confirm the target date; zero duration can fail the positive-horizon constraint. |
| **Default inflation** | Uses 6% if no goal-specific inflation rate is supplied. | Confirm the assumption is appropriate for the goal and visible in the explanation; 6% is a code default, not a universal forecast. |
| **Future target** | Inflates today's goal cost over the remaining duration. | Verify today's cost, inflation assumption and time horizon. |
| **Mapped assets** | Projects mapped assets using current value, allocation details, expected return and duration. A mapped asset must exist in the planning unit and have a name. | Verify asset identity, value, allocation and return assumptions. Mapping a resource to a goal does not prove it is legally earmarked or locked. |
| **Funding return** | Uses an allocated-value-weighted expected return for mapped assets; if there is no mapped capital, it falls back to 8%. | Treat the result as an assumption, not guaranteed performance. Confirm the source of the return. |
| **Funding gap** | Future target minus projected mapped assets. Positive = Shortfall; approximately zero (within ₹0.01) = On Track; negative = Overfunded. | Review both target and projected assets. The helper can convert a non-calculable gap to zero, which risks making invalid data look On Track if callers do not preserve the error state. |
| **Required monthly contribution** | For a positive gap and positive duration, calculates an end-of-month monthly contribution using annual return divided by 12 and number of months. Non-positive gap or zero duration returns zero. | A zero contribution does not necessarily mean a goal is healthy; check the gap and horizon separately. |
| **Retirement corpus** | Requires current age and life expectancy in dynamic details for an active retirement calculation; uses a separate retirement corpus calculation and an 8% retirement-return assumption. | Ensure age and life expectancy are present. The 8% value is a code assumption, not a promise. |
| **Cancelled retirement goal** | Has a special fallback of age 30 and life expectancy 85. | This fallback needs review because missing data in a cancelled record can be replaced with assumed ages. |
| **Goal-level required return** | Derives the return implied by current funding, target and duration when inputs permit. | Do not confuse required return with forecast return, and do not treat an undefined value as zero. |

### Goal Planner and Goal Feasibility ownership

- **Goal Planner** owns goal requirements, target calculations, resource projection, funding gap, required contribution and goal-level funding context.
- **Goal Feasibility** assesses whether a funding path is workable under relevant conditions.
- **Strategy Builder** consumes relevant goal/feasibility evidence to evaluate strategy options; it should not silently replace Goal Planner's calculation or feasibility conclusion.
- Funding mechanisms such as SIP, lump sum, step-up contribution and combinations belong to the **goal funding / feasibility domain**, not to a fifth Strategy Builder strategy.

**Audit limitation:** the calculation functions are visible in code, but the complete orchestration of debt prepayment, EMI changes, liquidity, competing goals, opportunity cost and goal adjustment needs call-path verification before claiming every branch is active.

---

## 7. Multi-goal and shared-resource rules

The main rule owner is `backend/rules/multi_goal.py`, with shared policy in `backend/engines/constraints/policy.py`.

- Priority is normalized to Critical, High, Medium or Low and mapped to a precedence rank.
- A discretionary goal must not preempt an essential goal.
- Funding statuses in code include fully funded, partially funded, unfunded, within surplus, surplus shortfall and requires review.
- Feasibility statuses include pass, conditional and infeasible.
- Shared-resource analysis matters when goals compete for assets, surplus, liquidity or other limited resources.

**Important:** the existence of a priority rule does not by itself prove that a downstream feature blocks a proposal, changes its ranking or only displays a warning. The actual consumer determines the effect.

When a decision materially changes shared resources or an existing Accepted Plan, identify which other goals may be affected and revalidate those decisions. Do not assume that every isolated decision requires rebuilding the entire plan.

---

## 8. Strategy Builder rules

The relevant backend areas include `backend/rules/eligibility.py`, `backend/engines/strategy/eligibility.py`, `backend/engines/strategy/decision.py`, `backend/rules/strategy_decision.py` and the rules engine.

### 8.1 The four canonical strategies

1. Progressive De-risking
2. Capital Preservation
3. Debt Reduction
4. Credit Utilisation

**Goal Funding is not a fifth Strategy Builder strategy.** It remains in Goal Planner / Goal Feasibility.

The internal backend contains eight eligibility checks. They are an internal assessment set—not a requirement to show eight separate UI stages.

| Internal check | What it assesses | Planner interpretation |
|---|---|---|
| Cash-flow fit | Whether the proposed funding/repayment requirement fits available surplus. | A proposal can fail if required monthly cash flow exceeds usable surplus. |
| Liquidity fit | Whether available liquid resources can support required liquidity. | Do not use resources without checking reserve and liquidity needs. |
| Debt fit | Whether debt burden and repayment conditions support the proposal. | Check affordability and repayment sustainability. |
| Asset/resource fit | Whether the needed assets or resources are available. | Confirm data and resource availability. |
| Risk-capacity fit | Whether the proposal is compatible with observable capacity to bear risk. | Required risk should not exceed demonstrated capacity. |
| Goal-constraint fit | Whether goal type, horizon, funding gap and applicable goal constraints allow the path. | A goal-specific constraint can make a candidate unacceptable. |
| Multi-goal conflict fit | Whether the proposal creates a material conflict with other goals/resources. | Assess shared-resource effects where relevant. |
| Implementation fit | Whether there is a credible way to carry out the proposal. | A theoretically attractive option may still be impractical. |

The eligibility logic uses **PASS / CONDITIONAL / FAIL** outcomes. Missing evidence should not be silently treated as a pass.

### 8.2 Applicability is different from viability

- **Applicability:** Does this strategy fit the kind of problem and the investor's situation?
- **Viability:** Can it work under the investor's financial conditions and applicable constraints?
- **Recommendation:** How should the evidence, assumptions and trade-offs be explained?
- **Adoption:** Has the investor explicitly accepted the proposal?

A strategy may be applicable but not viable. A warning or poor ratio is not automatically a hard blocker; the specific rule decides its effect.

### 8.3 Current scoring and consistency warning

The audited strategy code contains scoring constants, including:

- Primary goal-type match: 25
- Other-goal match: 10
- Characteristic match: 5
- Optimal horizon: 30; baseline horizon: 15
- Feasibility PASS: 15; CONDITIONAL: 8; FAIL: 0
- Technique score maximum: 10
- Failed eligibility: −1000

These are code-level scoring values, not necessarily a complete or approved planner-facing ranking policy. Do not interpret a score as proof that an option is financially suitable.

**Identified mismatch:** scoring code refers to legacy strategy IDs such as `strat-dynamic-accumulation`, `strat-calibrated-growth`, `strat-high-liquidity-flex`, `strat-cap-preservation` and `strat-debt-reduction`. These do not cleanly map to the four canonical strategy names. The mapping needs reconciliation before strategy scores are treated as consistent across the system.

### 8.4 Two-option decision rule

The Strategy Builder guide requires two options for each decision, while still being honest about their status:

- Both options must come from the four canonical strategies.
- Show applicability and viability separately, with reasons.
- Do not present a failed option as suitable or recommendable.
- If neither is acceptable, the valid result is **No Acceptable Strategy / No Acceptable Path**.
- Do not invent score weights, thresholds, tie-breakers or eligibility outcomes.
- Keep proposal, investor decision, Accepted Plan and execution separate.

This describes the business rule for planner-facing behavior; it does not prove every screen currently enforces it.

---

## 9. Risk Profiler rules

The audited Risk Profiler consumes required-risk information from canonical calculations when available, while an override path also exists.

- **Risk capacity** is assessed from observable financial information such as surplus, emergency reserve, EMI/debt, assets and liabilities.
- If required risk is within capacity, the check can pass; if it exceeds capacity, it can fail; if evidence is missing, the result can be conditional.
- Behavioral dimensions include decision consistency, reaction to volatility, discipline, intervention tendency, and response to loss/uncertainty.
- Behavioral observations require evidence. Missing observations should remain unknown rather than becoming an invented score.
- The audited observed-behavior policy labels these behavioral constraints for **product selection only**; do not silently use them as goal-feasibility blockers.

**Planner action:** distinguish financial ability to take risk from behavioral comfort with risk. They are related, but not interchangeable.

---

## 10. Insurance and protection rules

The audited required-life-cover formula is:

**Required cover = 10 × gross annual income + outstanding liabilities**

- Negative inputs are floored at zero.
- Existing assets are not netted off in this formula.
- Recognized life-policy types in code include term, endowment, whole life, ULIP and money back.
- Recognized health-policy types include health and health insurance.

This is the formula currently found in code, not proof that a ten-times-income rule is sufficient for every family. Confirm liabilities, dependants, future goals, existing cover and the applicable planning methodology before treating the result as a final recommendation.

Moneywheel's Insurance Coverage Ratio compares existing sum assured with this required-cover calculation. Its status bands are listed in Section 4.

---

## 11. Financial State and budget classifications

The audited code includes these classifications:

| Area | Current classification / behavior | Planner note |
|---|---|---|
| Short-term liabilities | Credit Card, Personal Loan, Consumer Loan, Other | Verify that every liability is categorized correctly; unknown categories may be misrepresented if not reviewed. |
| Essential expenses | Housing, Utilities, Groceries, Healthcare, Insurance, Education, Debt Payments | This classification affects cash-flow interpretation; confirm context where an expense does not fit neatly. |
| Unknown expense type | Defaults to Other | “Other” is a fallback, not confirmation that the expense is unimportant. |
| Financial State calculations | Wrappers delegate to canonical cash-flow/savings calculations. | The wrapper should not be mistaken for an independent second formula owner. |
| Safety-reserve helper | A 12-month fallback exists in the audited helper. | This is distinct from the ratio evaluator's 3-, 6- and 9-month bands. Confirm which path a feature uses. |

The 12-month fallback and reserve-evaluation bands are an example of why a planner should not assume every feature uses one shared reserve threshold.

---

## 12. Action Plan and investor adoption

The audited action-plan logic can assign high priority to a primary strategy action and medium priority to supporting strategy/technique actions. This does **not** prove that the investor accepted or executed those actions.

Keep these states separate:

1. Calculation or preview
2. Proposed strategy / solution
3. Investor decision
4. Accepted Plan
5. Action Plan
6. Actual execution

A preview must not silently accept a proposal, change goal priority, earmark an asset or overwrite an Accepted Plan. After a material input change, revalidate affected decisions rather than assuming the previous result still applies.

---

## 13. Key gaps identified in the code audit

| Gap | Why it matters to a financial planner | What needs to be verified or corrected |
|---|---|---|
| Not all thresholds are centralized | Different features may classify the same situation differently. | Establish one policy owner for shared thresholds and make consumers use it. |
| Rule registry is incomplete | A rule may run in code without being fully represented in the canonical catalogue. | Reconcile registered rules with active runtime rules. |
| Constraint aggregation uses optional sources | A decision may be missing a constraint if the relevant source was not supplied. | Trace every feature's actual call path and inputs. |
| Critical ratio does not always mean hard failure | A planner could mistake a warning for a blocker or miss a real blocker. | Document the effect of each rule at the point where it is consumed. |
| Legacy Strategy IDs conflict with canonical strategy names | Scoring and business labels may not refer to the same strategy. | Map or retire legacy IDs and test the four-strategy allowlist. |
| Reserve thresholds differ across helpers | Different screens or calculations may use different benchmarks. | Decide and document the intended threshold by purpose; remove accidental duplication. |
| Funding-gap helper can turn a non-calculable result into zero | Invalid data can appear to mean “On Track” if the caller loses the error state. | Preserve an explicit unavailable/error status. |
| Important assumptions use defaults | A planner may not see that 6%, 8%, or 10× income was assumed. | Make assumptions and their source visible and governable. |
| Unknown priority defaults to Medium | A missing investor decision can affect goal order. | Surface the default and require confirmation where material. |
| Essential/discretionary categories are fixed | The classification may not match the investor's real circumstances. | Decide whether the classification should allow context-specific review. |
| Malformed numeric strategy constraints can be ignored | A bad input might not trigger the intended check. | Validate input and surface an explicit invalid-data outcome. |
| Full feature call paths are not yet proven | A rule's existence does not prove every feature applies it. | Trace active callers and tests for each rule and constraint. |

---

## 14. Planner's quick review checklist

Before relying on a Planvesto recommendation, confirm:

- [ ] The goal uses one of the canonical goal types.
- [ ] Target date, current cost, inflation and return assumptions are visible and reasonable for the case.
- [ ] Asset mappings refer to real, correctly valued resources; mapping is not mistaken for earmarking.
- [ ] Funding gap, required contribution and required return are interpreted separately.
- [ ] Unavailable inputs are not being treated as zero or as a pass.
- [ ] Reserve and debt warnings are distinguished from hard constraints.
- [ ] The applicable constraint sources were actually supplied to the decision.
- [ ] Required risk is not being confused with risk capacity or behavioral comfort.
- [ ] Other goals and shared resources are reviewed when the decision could materially affect them.
- [ ] Strategy applicability and viability are shown separately.
- [ ] A failed option is not presented as suitable merely to fill a two-option display.
- [ ] A recommendation is not mistaken for investor acceptance or execution.
- [ ] Material changes trigger targeted recalculation/revalidation.

---

## 15. Audit boundary and next review

This guide consolidates the principal rule-bearing backend modules reviewed for this audit. It does not claim that every frontend form, API endpoint, database path, test and deployment route has been exhaustively traced.

The next verification pass should:

1. Trace each rule from definition to its active feature/API caller and tests.
2. Reconcile duplicate thresholds and assumptions under clear policy ownership.
3. Resolve the legacy Strategy ID versus canonical four-strategy mismatch.
4. Verify that every relevant feature receives the required canonical ConstraintSet and preserves missing/conflicting evidence.
5. Test that unavailable or invalid calculations cannot appear as healthy, zero-gap or passing outcomes.

**Bottom line:** use this guide to understand the rules currently visible in code, but treat the identified gaps as open audit items—not as proof that the system is already fully centralized or consistent.
