# PlanVesto — Canonical Business Source of Truth

**Authority:** Real-Life Decision Cases folder  
**Status:** Consolidated business baseline for reconciliation; numerical policies marked unresolved remain open  
**Scope:** Goal Planning/Feasibility, Strategy Decision, Multi-Goal Impact, Implementation, Investor Adoption, Action Plan, Execution, What-If and Revalidation  
**Rule:** This document is derived from the Real-Life Decision Cases. Other documentation and current code must be reconciled against it—not used to silently overrule it.  
**Created:** 2026-10-12

---

## 1. Authority and interpretation

This is the single consolidated business reference for the decisions represented by the Real-Life Decision Cases folder.

Authority order:
1. This consolidated source of truth for rules that it explicitly marks as established.
2. The specific Real-Life Decision Case for its concrete scenario and reasoning.
3. Other documentation and implementation plans as evidence of intended/current behavior, not as authority to reverse a business rule.
4. Active code and tests as evidence of what is implemented today—not as proof that the behavior is correct.

If two case documents genuinely conflict, do not guess or choose based on repetition. Record the conflict as **OPEN BUSINESS DECISION** and preserve both source references until the owner resolves it.

Status labels used here:
- **ESTABLISHED** — repeatedly supported by the case library and stated as a business boundary.
- **TARGET BEHAVIOUR** — required product behaviour, but runtime support may be incomplete.
- **OPEN POLICY** — responsibility is known but the exact algorithm, threshold or rule is not frozen.
- **CURRENT IMPLEMENTATION** — only asserted after a code-path/test check.

This document describes business truth. It does not claim that the current code already conforms.

## 2. Product model: three distinct decision levels

### 2.1 Goal Planning / Goal Feasibility — “What is financially feasible?”

**ESTABLISHED.** Goal Planner owns:
- goal definition and relevant assumptions;
- asset mapping and projected asset contribution;
- funding requirement and funding gap;
- individual-goal feasibility;
- alternative funding/financial paths;
- mathematical comparison of their consequences and opportunity costs;
- identifying what financial conditions would make the goal feasible.

Goal Funding is the feasibility/path analysis function, not simply a list of SIP/lump-sum options.

Possible funding mechanisms—existing assets, periodic contributions/SIP, lump sum, step-up contributions, or combinations—are inputs/components of a funding path. They are not automatically peer Strategy Builder strategies.

The exact optimization method, return assumptions, uncertainty treatment and numerical materiality thresholds remain **OPEN POLICY**.

### 2.2 Strategy Decision / Strategy Builder — “How should a feasible path be structured?”

**ESTABLISHED.** Strategy Builder consumes goal context, current Financial State, Goal Planner feasibility/funding evidence and relevant constraints. It must not independently recreate or contradict Goal Planner's feasibility calculation.

It decides:
- which strategies are applicable;
- which candidates are viable under the investor's circumstances and constraints;
- which viable strategy is preferable;
- which variant fits;
- which techniques are required, conditional, optional or not applicable;
- how techniques are translated through methods/policies into architecture/solution.

Applicability, viability and selection are separate decisions.

### 2.3 Action Plan — “What does the investor need to do?”

**ESTABLISHED.** Action Plan is downstream of investor adoption of a proposed path. It turns the accepted implementation into concrete actions. A recommendation, scenario or unaccepted proposal must not silently become the active Action Plan.

## 3. Canonical individual-goal Strategy Builder taxonomy

### 3.1 Strategy set

The canonical Strategy Builder peer set contains four strategies:

1. **Progressive De-risking**
2. **Capital Preservation**
3. **Debt Reduction**
4. **Credit Utilisation**

**Goal Funding is not a fifth peer Strategy Builder strategy.** It belongs to Goal Planner / Goal Feasibility.

This is a business rule; migration of the current `strat-goal-funding` registry entry, its variants, scenarios, scoring, APIs, saved runs/versions and legacy data is a separate engineering task. Do not delete or migrate those structures without a migration plan.

### 3.2 Applicability rules

**Progressive De-risking**
- Candidate when a meaningful future requirement has an identifiable horizon, capital is in a growth/accumulation phase, and gradual protection can improve the probability of meeting the requirement.
- A future goal date alone is insufficient.
- It is not the primary strategy when the requirement is immediate and protection dominates.

**Capital Preservation**
- Candidate when required capital is identifiable and sufficiently close/protection-sensitive, capital loss could materially impair the goal, and protecting that capital matters more than additional growth.
- A goal's mere existence is insufficient.

**Debt Reduction**
- Candidate when material debt constrains cash flow, affordability, resilience or goal funding and reducing/restructuring it materially improves the position.
- The existence of debt, DTI or EMI alone does not determine the decision.
- Compare debt cost, repayment effects, liquidity, opportunity cost, goal funding and alternative feasible paths.

**Credit Utilisation**
- Candidate only for a genuine funding/timing gap after reasonable own-resource options have been considered.
- Viability requires sufficient borrowing capacity, sustainable EMI/repayment, justified financing cost, a credible repayment path and compliance with hard constraints.
- Failure of a material viability gate means Credit Utilisation fails and must not be recommended as an acceptable candidate.

### 3.3 Decision order

For an individual goal:

1. Goal context and actual requirement
2. Current Financial State
3. Goal Planner feasibility/funding evidence
4. Hard constraints and safety evaluation
5. Strategy applicability
6. Candidate viability
7. Strategy selection among viable candidates
8. Variant selection
9. Technique policy/selection
10. Method and policy
11. Architecture / concrete solution
12. Stress and resilience evaluation
13. Explainable decision / recommendation

Whole-Plan Impact is not a mandatory stage for every individual-goal decision. It is a conditional branch when the decision has material cross-goal or accepted-plan consequences.

### 3.4 Variant catalogue

**Progressive De-risking**
- Goal-Date Glide Path
- Payment-Tranche Glide Path
- Recurring-Cashflow Glide Path
- Income-Transition Glide Path

**Capital Preservation**
- Full-Goal Preservation
- First-Payment Preservation
- Rolling Reserve Preservation
- Protected-Core Preservation

**Debt Reduction**
- Goal-Gap Debt Reduction
- EMI-Relief Debt Reduction
- Residual-Gap Debt Reduction
- Goal-Linked Debt Reduction

**Credit Utilisation**
- Residual-Gap Bridge
- Partial-Goal Financing
- EMI-Cap Financing
- Timing-Bridge Financing

Variants describe forms of a strategy. They are not techniques, solutions or funding mechanisms.

### 3.5 Core technique catalogue

- Glide Path
- Bucketing
- Cash-flow Matching
- Laddering
- Asset Earmarking
- Goal Segmentation
- Debt Repayment Prioritisation
- Debt Cost Optimisation
- Debt Prepayment Optimisation
- EMI Capacity Analysis
- Borrowing Capacity Analysis
- Financing Cost Comparison

Technique policy statuses:
- **Required** — variant cannot be properly executed without it.
- **Conditional** — use only when a defined condition exists.
- **Optional** — may help but is not necessary.
- **Not Applicable** — should not be used for the current situation.
- **Insufficient Inputs** — relevant, but required data is missing.

**Not Applicable is not the same as Insufficient Inputs.**

The authoritative variant-to-technique policy is maintained in the detailed Strategy Decision Tree document, which must be kept consistent with this taxonomy. Laddering is conditional when multiple predictable maturity/payment dates justify it; it is not a default technique for Capital Preservation.

Reclassification:
- Contribution Escalation belongs to Goal Planner / Goal Funding as a funding mechanism.
- Duration/Horizon Matching is an analysis method, not a core technique.
- Tax-specific techniques belong in the relevant investment/tax implementation layer unless a future explicit business decision promotes them into this subsystem.

### 3.6 Canonical hierarchy

**Strategy → Variant → Technique → Method/Policy → Solution → Action**

Entity types must not be collapsed. A technique is not a solution; SIP/lump sum is not automatically a strategy; a method is not a variant.

### 3.7 No acceptable strategy

**ESTABLISHED.** “No Acceptable Strategy / No Acceptable Path” is a valid decision outcome, not a system error. If all candidates fail applicability, viability, hard constraints or resilience, the system must explain why and what conditions could change the result. It must not force a recommendation to fill an output field.

## 4. Hard constraints versus advisory priorities

- A **hard constraint** can genuinely exclude or block a path.
- An **advisory priority** influences ranking and explanation but does not automatically prohibit an investor from choosing another path.
- Financial ratios, scores and diagnostic indicators are evidence; they are not automatically decisions.
- A strong signal such as high-cost debt should be explained and incorporated into opportunity-cost comparison. It must not become an absolute prohibition unless an explicit hard-constraint policy says so.
- An investor may choose a non-preferred path when it is not blocked by a genuine hard constraint. The system must explain consequences and recalculate the affected plan.

The exact hard-constraint catalogue and thresholds remain **OPEN POLICY** where not explicitly frozen by a case.

## 5. Asset Mapping versus Asset Earmarking

**Asset Mapping** is upstream, owned by Goal Planning:
- associates an existing asset/resource with a goal for planning;
- estimates its projected contribution;
- contributes evidence to funding/feasibility;
- does not itself reserve, restrict or permanently commit the asset.

**Asset Earmarking** is downstream, owned by strategy/technique/implementation:
- intentionally designates resources to be reserved/protected for a goal;
- requires a strategic/implementation reason;
- may be partial and need not equal the mapped amount;
- must not silently reserve the same capital for mutually competing goals;
- does not itself select an investment product.

**Cancel Goal ≠ Cancel Asset.** Cancelling a goal removes/invalidates its goal mapping and triggers a decision about releasing any earmarking; it does not delete the underlying asset from Financial State.

Mapping contributes evidence; it does not guarantee feasibility.

## 6. Multi-goal and whole-plan decisions

Individual-goal feasibility and combined-plan feasibility are different questions.

When goals compete for shared surplus/assets/liquidity, or a proposed change affects an Accepted Plan, the system must evaluate:
- individual goal requirements and feasibility;
- total resources available;
- combined feasibility;
- cross-goal conflicts and trade-offs;
- priority as an input, not the sole decision mechanism;
- alternative resource/funding paths and their consequences.

Whole-Plan / Multi-Goal Impact is invoked when the decision is inherently plan-level, including:
- competing goals sharing resources;
- a new goal proposed against an existing Accepted Plan;
- material cross-goal change;
- a plan change affecting other goals or overall allocation.

It must not be a hidden mandatory gate inside every individual-goal Strategy Decision.

A rejected new goal or rejected plan-level proposal must not consume committed resources or alter the existing Accepted Plan.

The complete optimization algorithm, priority weighting and conflict-resolution thresholds remain **OPEN POLICY**.

## 7. Better-path proposals and investor authority

If a goal is already feasible, the system may compare the current path with a potentially better path. “Better” must be demonstrated with financial projections and trade-offs, not asserted from a higher assumed return alone. Compare relevant dimensions such as goal timing, contributions, liquidity, risk, debt, opportunity cost and other-goal impact.

A better path is a **proposal**, not an automatic replacement.

Investor authority:
- Recommendation ≠ adoption.
- Accept, Reject and Modify must have distinct state effects.
- Rejection preserves the existing Accepted Plan.
- Acceptance updates the Accepted Plan and then its Action Plan.
- A changed strategy or new goal must be evaluated for affected consequences before adoption.
- Multiple strategies may coexist in a coordinated plan when justified; the product must not force one strategy for the entire investor.

## 8. Scenario / What-If / execution change

A what-if is an isolated scenario against the Accepted Plan. It may change contribution, lump sum, timing, asset use, borrowing, debt execution or other relevant parameters.

The scenario must:
1. remain separate from the Accepted Plan;
2. calculate the consequences for the goal and, when material, other goals/plan;
3. show the relevant impact dimensions;
4. assess whether the existing strategy remains appropriate;
5. trigger targeted strategy re-evaluation only if needed;
6. preserve the original Accepted Plan until the investor adopts a change.

Execution change does not automatically mean strategy change.

## 9. Change, adaptation and targeted revalidation

Materiality must be assessed before replanning. The exact numerical thresholds are **OPEN POLICY**.

Potential triggers include material changes to income, expenses, assets, liabilities, surplus, liquidity, goal target/date/horizon, goal cancellation/addition, debt structure or implementation.

Required flow:
1. detect a proposed or actual change;
2. assess materiality and dependency scope;
3. if immaterial, retain the current plan;
4. if material, recalculate affected goal feasibility;
5. assess whole-plan impact only when cross-goal/accepted-plan consequences warrant it;
6. revalidate the affected strategy and implementation;
7. retain the strategy if it remains appropriate;
8. if not, present alternatives and their trade-offs;
9. obtain investor decision;
10. only on acceptance update the Accepted Plan and Action Plan.

Do not automatically rebuild unrelated goals or replace the whole plan.

The system must support repeated iterations through strategy, execution, what-if and revalidation without confusing proposals with accepted state.

## 10. Investor-designed / open strategy

If no standard system path is acceptable, the investor may reject all paths or propose a custom strategy.

The system must:
- represent a custom/investor-designed strategy as such, not falsely relabel it as a standard library strategy;
- capture its assumptions, components, intended outcome and provenance;
- evaluate feasibility, hard constraints, impact and stress/resilience;
- explain risks and trade-offs;
- require explicit investor adoption before it enters the Accepted Plan.

A single rejection is not evidence that the investor is a poor product fit. Do not manufacture a solution, silently change priorities, sacrifice another goal, or hide a funding gap.

The detailed custom-strategy data contract remains **OPEN POLICY**.

## 11. Stress / resilience

Stress and resilience assess whether the proposed path remains acceptable under changed assumptions. They must reuse the same canonical decision logic; they must not become an independent competing decision-maker.

A stress result can trigger targeted re-evaluation and a new proposal, but cannot silently overwrite the Accepted Plan.

The complete stress taxonomy, scenario set, pass/fail thresholds and re-selection rules remain **OPEN POLICY**.

## 12. Canonical lifecycle

### New plan / first decision
Financial State + Investor Intent/Goals  
→ Goal Planning / Feasibility  
→ [conditional] Whole-Plan / Multi-Goal Impact  
→ Strategy Decision  
→ Implementation Design  
→ Stress / Resilience  
→ Decision / Recommendation  
→ Investor Decision / Adoption  
→ Accepted Plan  
→ Action Plan  
→ Execution

### Proposed new goal or plan-level change
Proposed Goal/Change  
→ Goal Feasibility  
→ [when plan-level] Whole-Plan Impact  
→ Alternatives and trade-offs  
→ Investor Decision  
→ Reject: existing Accepted Plan remains  
→ Accept: affected Strategy/Implementation updates → Accepted Plan → Action Plan

### Change / what-if loop
Accepted Plan  
→ Execution Change / What-If  
→ Impact Analysis  
→ Materiality + Targeted Revalidation  
→ If still valid: continue with same strategy and proposed execution update  
→ If not valid: strategy re-evaluation and alternatives  
→ Investor Decision  
→ Updated Accepted Plan if accepted  
→ Updated Action Plan

## 13. Decision output contract

A completed Strategy Decision should explain:
1. goal and actual requirement;
2. relevant Financial State;
3. Goal Planner feasibility/funding evidence;
4. applicable hard constraints and advisory priorities;
5. applicable strategies and why;
6. viability failures and reasons;
7. why the selected strategy is preferable;
8. why the variant fits;
9. required and conditional techniques, with reasons;
10. method/policy and concrete solution;
11. stress/resilience result;
12. trade-offs, uncertainties and actions;
13. whether the result is a proposal, rejected option or accepted plan.

## 14. Explicitly open—not to be guessed

These topics have established ownership/direction but need a separate explicit policy decision before numerical rules or migrations are finalized:
- Goal Planner funding-path optimization and assumptions;
- return/risk uncertainty and projection methodology;
- materiality thresholds and targeted-revalidation triggers;
- multi-goal priority weighting and resource-conflict optimization;
- full hard-constraint catalogue and thresholds;
- stress/resilience scenarios and pass/fail/reselection policy;
- investor-designed strategy schema;
- persistence/API migration for removing Goal Funding from the Strategy Builder peer set;
- handling legacy runs/versions and historical data.

## 15. Case sources incorporated

- `00-GOAL_FUNDING_CONCEPT_CHANGE_LOG.md` — Goal Funding ownership, opportunity cost and financial-path comparison.
- `03-CASE_3_MULTI_GOAL_FEASIBILITY_AND_ACTION_PLAN.md` — shared resources, combined feasibility and downstream Action Plan.
- `04-CASE_4_BETTER_PATH_STRATEGY_AND_IMPLEMENTATION.md` — compare better paths without auto-adoption.
- `05-CASE_5_PLAN_ADAPTATION_AFTER_FINANCIAL_STATE_CHANGE.md` — materiality and targeted revalidation.
- `06-CASE_6_GOAL_INTENT_CHANGE_AND_RECALCULATION.md` — recalculate from full changed goal definition.
- `07-CASE_7_NEW_GOAL_AGAINST_EXISTING_PLAN.md` — scenario first; preserve plan until accepted.
- `08-CASE_8_INVESTOR_STRATEGY_CHANGE_AND_MULTI_STRATEGY_PLAN.md` — investor authority, hard constraints vs advisory priority, multi-strategy plans.
- `09-CASE_9_EXECUTION_PLAN_WHAT_IF_AND_IMPACT_GUIDANCE.md` — isolated execution what-if.
- `10-CASE_10_EXECUTION_CHANGE_TRIGGERING_STRATEGY_REEVALUATION.md` — targeted strategy re-evaluation only when required.
- `11-CASE_11_ITERATIVE_STRATEGY_EXECUTION_AND_REVALIDATION.md` — repeated strategy/execution loop.
- `12-CASE_12_NO_ACCEPTABLE_PATH_AND_INVESTOR_DESIGNED_STRATEGY.md` — valid no-path result and custom strategy.
- `13-DECISION_TREE_SYSTEM_UPDATE_AND_FEATURE_IMPLEMENTATION_PLAN.md` — implementation gap evidence, not authority over business rules.
- `14-REAL_LIFE_CASES_CANONICAL_SYSTEM_STRUCTURE_AND_ALIGNMENT.md` — cross-case lifecycle and ownership map.
- `15-CANONICAL_ASSET_MAPPING_VS_ASSET_EARMARKING_DECISION_CASE.md` — mapping vs earmarking.
- `strategy-decision-tree.md` — individual-goal strategy/variant/technique decision rules.

This source of truth consolidates the case library; it does not replace the case documents as evidence for their concrete scenarios.
