# Goal Planner — Final Implementation Specification

**Document type:** Authoritative implementation specification  
**Scope:** Goal definition, funding requirement, feasibility, funding-gap analysis, alternative funding paths, and conditional multi-goal impact  
**Status:** Business rules consolidated from the feature specification, existing-code evidence, and Real-Life Decision Cases. This document does not claim every required workflow is currently implemented.  
**Existing-code audit baseline:** `5a3b060e1b27915ede226f5173364e23dca1263e` for the cited Goal Planner backend evidence; confirm current `main` before implementation.

## 1. Purpose and ownership

Goal Planner answers: **What does this goal require, can it be funded under explicit assumptions, what is the funding gap, and which feasible funding paths are available?**

It owns goal-level requirements and feasibility—not the final strategy choice or execution design.

- **Goal Planner / Goal Feasibility:** Goal definition, target-date requirement, mapped-resource projections, funding gap, required contribution, feasibility evidence, and comparison of goal funding paths.
- **Moneywheel:** Canonical financial metrics and their availability/metadata. Goal Planner consumes these results where relevant; it must not recreate Moneywheel formulas or thresholds.
- **Budgeting:** Supplies cash-flow and surplus facts. Goal Planner must not silently invent available monthly surplus.
- **Whole-Plan / Multi-Goal Impact Analysis:** Evaluates shared-resource conflicts and effects on other goals when a change materially affects the broader plan. This is conditional, not required for every local goal edit.
- **Strategy Builder:** Consumes Goal Planner's feasibility and funding context to decide how to implement a feasible path. It must not silently redefine Goal Planner feasibility or treat a funding mechanism as a strategy.
- **Implementation Design:** Where available, models concrete implementation alternatives for a selected path.
- **Accepted Plan / Investor Decision lifecycle:** Only an explicit investor acceptance transition makes a proposed funding path or goal-condition change active. Calculation or preview must not itself overwrite the canonical goal or Accepted Plan.
- **Action Plan:** Turns an adopted plan into execution actions; it is not the goal-feasibility engine.

## 2. Core business rules

| ID | Rule | Required disposition |
|---|---|---|
| GP-BR-01 | A goal's type, target amount/cost, target date, priority, flexibility, status, inflation assumption, and relevant goal-specific details must be explicit inputs. | Preserve valid existing contracts; identify missing required inputs. |
| GP-BR-02 | Target-date requirement, mapped-resource projection, funding gap, and required contribution must be traceable to their assumptions. | Preserve existing calculations where verified; document formula and assumption source. |
| GP-BR-03 | Missing or invalid data must not be disguised as a successful feasibility result. | Return incomplete/unavailable with a reason and required inputs. |
| GP-BR-04 | Goal Funding is a feasibility/funding-path responsibility, not a fifth Strategy Builder strategy. | Enforce cross-feature boundary. |
| GP-BR-05 | SIP, lump sum, step-up contribution, asset use, and combinations are funding mechanisms/options; none independently proves feasibility. | Compare their modeled consequences rather than labeling them as strategies. |
| GP-BR-06 | Debt existence, DTI, leverage, or a negative Investment–Debt Spread must not alone select Debt Reduction. | Compare complete relevant financial paths. |
| GP-BR-07 | An investment return assumption exceeding a debt rate does not by itself prove that investing is best. | Include uncertainty, cash flow, liquidity, debt terms, goal timing, and competing goals. |
| GP-BR-08 | Asset mapping is planning association, not asset earmarking or commitment. | Never infer that a mapped asset is locked, sold, reserved, or unavailable elsewhere. |
| GP-BR-09 | The same asset or surplus must not be silently treated as fully available to multiple goals. | Detect and disclose shared-resource conflicts. |
| GP-BR-10 | Whole-plan analysis is triggered by relevant cross-goal dependencies or material impact, not by every individual-goal change. | Assess local impact first; escalate conditionally. |
| GP-BR-11 | Alternative paths and What-If results remain proposals until explicit investor adoption. | Preserve Accepted Plan until adoption. |
| GP-BR-12 | “No acceptable path” is a valid result. | Explain the gap, constraints, assumptions, and possible changes; never force a recommendation. |
| GP-BR-13 | Material changes require targeted recalculation/revalidation of affected goals and decisions. | Do not rebuild unrelated decisions without a material dependency. |
| GP-BR-14 | Goal cancellation does not delete the underlying asset from Financial State. | Treat earmark release/remapping as a separate lifecycle action. |
| GP-BR-15 | Goal Planner owns its feasibility result; Strategy Builder consumes that result and handles strategy/execution decisions. | Avoid duplicate or conflicting feasibility logic downstream. |
| GP-BR-16 | Goal-Level Return Required is scenario-specific and distinct from required contribution and expected return. | Calculate and expose it in Goal Planner when the cash-flow inputs support a valid solution. |
| GP-BR-17 | Goal Feasibility follows two ordered approaches: first optimize available financial capacity/surplus using relevant financial alternatives and Opportunity Cost; only if the goal remains infeasible, calculate the goal-condition adjustments required. | Use one feasibility engine for both approaches; never invent surplus, bypass constraints, or force an acceptable path. |
| GP-BR-18 | If financial optimization is insufficient, the system calculates what target-amount reduction and/or target-date extension would be required; it does not modify the investor's goal automatically. | Present the calculated adjustment and consequences for investor decision; preserve the original goal until explicitly accepted. |

## 3. Goal inputs and canonical context

The goal input contract should represent, as applicable:

- Canonical goal type and name.
- Current cost/target amount and target date.
- Priority, flexibility, and lifecycle status.
- Inflation assumption, including whether it is user-supplied or a default.
- Goal-specific details (for example, retirement age, current age, and life expectancy for retirement goals).
- Asset IDs mapped to the goal, resolved against authoritative server-side asset records.
- Relevant server-owned Financial State: assets, liabilities, income/expenses and other available financial context.
- Relevant debt terms and cash-flow facts when comparing financing alternatives.
- Assumptions for each funding scenario: return, contribution, timing, debt repayment, and any other modeled change.
- Existing Accepted Plan / relevant plan version when evaluating a change to an active plan.
- Reference date and calculation/version metadata.

Do not treat a client-supplied financial snapshot as the authoritative source if a server-owned source exists. Validate ownership and scope for goal, planning unit, assets, and persisted versions.

If a field is required for a particular goal type or calculation and cannot be resolved, return a clear incomplete result instead of silently using a fabricated value. Existing defaults must be explicitly labeled with their source and must not be mistaken for investor-provided assumptions.

## 4. Calculation and feasibility pipeline

The following is the required logical contract. Preserve existing implementation details only where code evidence confirms them.

1. **Validate and canonicalize goal input.** Validate goal type, status, target, target date, and goal-specific requirements.
2. **Resolve authoritative context.** Resolve mapped asset IDs, server-owned Financial State, planning-unit ownership, relevant debt/cash-flow facts, and existing plan context when applicable.
3. **Establish assumptions.** Record reference date, inflation, projection return assumptions, and source of each assumption. Avoid hidden defaults.
4. **Calculate duration and target-date requirement.** Apply the canonical target/inflation calculation for the goal type. Retirement goals may require a distinct retirement corpus calculation and explicit retirement inputs.
5. **Project mapped assets.** Project only resolved eligible assets under declared assumptions. Show that mapping does not earmark or reserve an asset.
6. **Calculate funding evidence.** Return projected mapped resources, target-date requirement, funding gap/surplus, and required monthly contribution where inputs support those calculations.
7. **Run Goal Feasibility — Approach 1: financial optimization.** Before changing goal conditions, evaluate whether the goal can be funded better from the investor's actual financial capacity. Compare relevant uses of money—such as goal contributions, debt prepayment, investment, loan/EMI changes, liquidity preservation, and other goals—using Opportunity Cost where relevant. Estimate only evidenced, constraint-compatible surplus that can realistically be freed or generated. Do not assume that every alternative improves surplus or that the highest nominal surplus is automatically best.
8. **Recalculate feasibility after Approach 1.** Apply the same feasibility rules to the resulting funding path, including contribution fit, debt obligations, liquidity, risk limits, shared resources, and other applicable constraints. If feasible, return the path and its trade-offs; do not proceed to goal-condition changes as if they were necessary.
9. **Run Goal Feasibility — Approach 2 only if still infeasible.** Calculate the goal-condition changes that would be needed to make it feasible under the evidenced financial capacity—principally a lower target amount, a later target date, or a combination. Quantify the required adjustment and recalculate the requirement, contribution, funding gap, and feasibility. These are feasibility adjustments identified by Goal Planner, not an independent What-If feature or separate engine. The investor's canonical goal must not be changed without explicit acceptance.
10. **Assess broader impact conditionally.** If shared resources, other goals, or an Accepted Plan may be materially affected, invoke Whole-Plan / Multi-Goal Impact Analysis and identify affected decisions for revalidation.
11. **Return a typed result.** Include calculations, assumptions, missing inputs, feasibility state, Approach 1 findings, any necessary Approach 2 adjustment, funding paths, trade-offs, and traceability metadata.
12. **Persist only through the appropriate lifecycle.** Calculation/preview must not accidentally become an accepted plan. Versioned goal persistence and investor acceptance are separate transitions.

### Feasibility semantics

Use distinct states for at least:
- **Feasible under stated assumptions:** required funding fits the declared resource/contribution constraints.
- **Feasible only with changes:** identify the specific contribution, target, date, resource, or other assumption change needed.
- **Not feasible under stated assumptions:** explain the shortfall or binding condition.
- **Incomplete / cannot determine:** required inputs or authoritative evidence are missing/invalid.
- **No acceptable path:** modeled options fail investor-defined or canonical constraints; do not force a path.

Exact status names and mapping to existing response schemas must be reconciled with the current implementation before changing contracts. Do not turn a diagnostic or warning into a hard block without an explicitly owned canonical rule.

## 5. Funding gap and funding mechanisms
## 4.1 Goal-Level Required Return

Goal Planner owns **Goal-Level Return Required**. It must calculate the annualized return required for a specific goal under a clearly defined funding scenario before using that result to explain or compare feasibility. This is a Goal Planner calculation, not a strategy recommendation.

The calculation must use the goal's target-date requirement, time remaining, eligible mapped resources/current funding, and the contribution schedule for the scenario. It must identify whether the scenario assumes no future contributions, regular contributions, step-up contributions, lump sums, or a combination. Different funding schedules can produce different required-return results.

Rules:
- Do not calculate required return from target amount and duration alone when current funding or future contributions materially affect the result.
- Define the cash-flow timing convention (for example, contribution at period start/end), compounding frequency, annualization convention, and inflation/target-date treatment.
- If the cash-flow pattern cannot support a unique or meaningful required-return solution, return unavailable/indeterminate with a reason; do not fabricate a percentage.
- Label required return as the return mathematically needed under the stated scenario, not as an expected, achievable, guaranteed, or risk-adjusted return.
- Compare required return with a separately sourced, risk-appropriate projection assumption only when the assumptions are comparable. A gap between required and assumed return is evidence for feasibility analysis, not an automatic verdict by itself.
- Goal-Level Return Required must be recalculated when the target amount/date, mapped resources, contribution schedule, or other material scenario input changes.

### Required-return versus required-contribution calculations

These are two distinct calculation directions and both must be supported where inputs permit:

1. **Required return:** given the target, timeline, eligible current resources, and contribution schedule, solve for the annualized return needed.
2. **Required contribution:** given the target, timeline, eligible resources, and a declared return assumption, solve for the contribution needed.

Do not treat one as a substitute for the other. The output must record which variable was solved for and which assumptions were held fixed.

## 4.2 Constraint-Aware Goal Feasibility: Two Ordered Approaches

Goal Feasibility must evaluate the current goal against explicit financial and investor-defined constraints. Relevant evidence can include available monthly surplus, eligible assets/resources, accepted risk limits, declared return assumptions, target date/amount, debt obligations, and permitted funding sources. Moneywheel remains the owner of its canonical metrics; Goal Planner consumes their values and metadata rather than duplicating their formulas.

Constraint roles must remain distinct:
- **Hard constraint:** cannot be overridden by the planner; a breach makes the affected path unacceptable under the rule.
- **User-adjustable goal parameter:** target date or target amount can be changed only as a proposed scenario and only adopted through the investor-decision lifecycle.
- **Financial-state fact/derived limit:** for example, currently available monthly surplus. Do not treat it as freely editable merely to make a scenario pass.
- **Projection assumption:** a stated return/inflation or other modeling assumption. It must not be silently increased to force feasibility.

Goal Feasibility must use the following two ordered approaches as one decision process, not as separate features or engines.

### Approach 1 — Optimize financial capacity and available surplus first

Keep the investor's current goal amount and target date unchanged while evaluating how its funding position can be improved. Use authoritative Financial State and cash-flow facts to assess income, expenses, existing resources, debt obligations, liquidity needs, and competing goals. Where relevant, use Opportunity Cost to compare plausible uses of money and funding paths—for example, continuing goal contributions versus debt prepayment, changing loan/EMI terms, or a combined path.

The objective is to identify the most suitable feasible use of the investor's actual financial capacity, not to maximize surplus at any cost. Do not invent income, assume unavailable cash flow, count the same asset/surplus twice, assume investment returns are guaranteed, or violate risk, liquidity, debt, or other hard constraints. Explain the trade-offs and recalculate feasibility using the resulting evidenced funding path.

If this approach makes the goal feasible, return the feasible path and its assumptions/trade-offs. Do not proceed to changing the goal's target amount/date as though that were required.

### Approach 2 — Calculate required goal-condition adjustments only if still infeasible

If Approach 1 cannot make the goal feasible within applicable constraints, calculate what change to the goal would be required. At minimum, evaluate:
- **Lower target amount:** calculate the target amount that fits the available funding capacity under the declared assumptions.
- **Later target date:** calculate the additional time required for the goal to fit the available funding capacity under the declared assumptions.
- **Combination, where needed:** if neither single adjustment is sufficient or acceptable, quantify a combined adjustment where the calculation supports it.

For each proposed adjustment, recalculate the target-date requirement, Goal-Level Return Required or required contribution as appropriate, projected resources, funding gap, cash-flow fit, and feasibility. Show the difference from the original goal and state the assumptions and limitations. Do not silently advance the target date, increase the target amount, or alter the canonical goal. These are Goal Feasibility findings and required adjustments—not an independent What-If feature or a separate engine. The investor decides whether to accept a proposed change; until then, the original goal remains unchanged.

If no path or goal adjustment fits the applicable constraints, return **no acceptable path** and explain the binding constraints and shortfall. A high required return does not justify exceeding the investor's risk limit or manufacturing feasibility.


Goal Planner must distinguish these concepts:

- **Goal requirement:** target-date amount needed for the goal.
- **Projected resources:** value of resources under the stated assumptions and mapping.
- **Funding gap/surplus:** difference between requirement and modeled available funding; the sign convention must be explicit in the output contract.
- **Required contribution:** modeled contribution needed to address the gap under a stated timeline and return assumption.
- **Feasibility:** whether the required path fits the relevant resource, cash-flow, timing, and constraint conditions.
- **Funding mechanism:** SIP, lump sum, step-up contribution, use of mapped assets, combinations, or other explicitly modeled source.
- **Strategy:** a separate Strategy Builder decision object, not a synonym for a contribution mechanism or Goal Funding.

For each path, show the contribution schedule, resource use, time horizon, assumed return/inflation, target corpus, projected gap, and relevant limitations. If a path's outcome depends on a return assumption, label it as a projection—not a guarantee.

Do not declare a path feasible merely because its arithmetic produces the target if it violates available monthly cash flow, double-counts resources, ignores debt obligations, or depends on missing inputs.

## 6. Opportunity cost and debt-financing comparison

Opportunity Cost is a Goal Planner / Goal Feasibility business principle: compare the consequences of plausible alternative uses of resources. It is not a rule that automatically selects a particular strategy.

When relevant, alternatives may include:
- Faster debt repayment or prepayment.
- Continuing goal contributions/investment while servicing debt.
- Changing a loan/EMI/tenure structure and evaluating the resulting cash-flow use.
- A combined path that balances debt payments, liquidity and goal contributions.
- Adjusting goal target, timing, contribution, or resources.

Compare paths on a consistent baseline and include applicable factors:

- Goal corpus and residual funding gap.
- Contribution and monthly cash-flow requirements.
- Debt outstanding, interest/payment burden, debt duration and known prepayment/financing terms.
- Liquidity and emergency-resource implications.
- Investment-return assumptions and uncertainty; do not treat assumed returns as guaranteed.
- Goal timing and flexibility.
- Effects on competing goals and an existing Accepted Plan.
- Material constraints, risks, exclusions, and missing data.

Moneywheel is the canonical owner of its financial metrics, including Weighted Debt Rate and Investment–Debt Spread where implemented. Goal Planner must consume their values and metadata instead of duplicating the formulas. The spread is only a comparison of assumptions; it is not a guaranteed or risk-adjusted profit measure and must not independently select debt repayment versus investment.

If a debt rate, repayment term, prepayment charge, investment assumption, or other material input is unavailable, disclose that limitation. Do not fabricate a complete comparison from incomplete evidence.

## 7. Asset mapping, earmarking, and shared resources

**Asset Mapping** associates an asset with a goal for planning and projection. It does not mean the asset has been committed.

**Asset Earmarking** is a separate explicit decision to reserve/protect all or part of a resource for a goal or capital pool. It may affect later availability only through a defined authoritative lifecycle.

Required behavior:
- Resolve mapped assets from authoritative records and preserve asset ownership.
- Show mapped assets and the assumptions used to project them.
- Do not silently mark a mapped asset as sold, locked, reserved, or unavailable for another goal.
- Detect when one asset or shared surplus is being counted as fully available to multiple goals.
- Make shared-resource conflicts visible to the investor and the relevant whole-plan analysis.
- Do not delete an asset from Financial State when a goal is cancelled.
- Define earmark creation, partial allocation, release, and remapping separately; do not infer these transitions from a goal edit or cancellation.

## 8. Local impact versus whole-plan impact

Goal Planner first assesses the affected goal's requirement, mapped resources, gap, and feasibility. Whole-Plan / Multi-Goal Impact Analysis is needed when the change can materially affect shared resources, competing goals, or an Accepted Plan.

Potential triggers include:
- A new goal competes for existing surplus or assets.
- A goal target/date/contribution change consumes resources another goal relies on.
- A material change in income, expenses, debt, asset value, or other Financial State changes feasibility.
- A funding path reallocates resources, changes debt payments, or changes the contribution available to other goals.
- A scenario changes a resource or assumption used by an Accepted Plan.

When triggered, return:
- Affected goals and plan components.
- Shared-resource conflicts and relevant priorities/flexibility.
- Before/after funding gaps and feasibility where available.
- Assumptions and uncertainty.
- Which decisions need recalculation or revalidation.
- Whether investor review/adoption is required.

Do not rebuild unrelated decisions automatically. Materiality thresholds, dependency graphs, and targeted revalidation policy must be defined in the shared planning lifecycle; they must not be invented independently inside Goal Planner.

## 9. Relationship with Strategy Builder and Action Plan

Goal Planner's output should provide a typed, versioned feasibility/funding context, including:
- Goal identity/type and target requirements.
- Target date/duration and calculation assumptions.
- Mapped-resource evidence and availability caveats.
- Funding gap/surplus and required contribution.
- Feasibility state, reasons, and missing inputs.
- Evaluated funding paths and their trade-offs, when available.
- Relevant Moneywheel evidence and freshness/version metadata.
- Whole-plan impact/revalidation information when applicable.

Strategy Builder consumes this context to evaluate strategy/variant eligibility and design execution. It must not:
- Recompute Goal Planner's feasibility using a competing formula.
- Treat SIP, lump sum, step-up contribution, or Goal Funding as a strategy.
- Select Debt Reduction solely because debt exists or a metric is adverse.
- Silently override goal assumptions or mark an unaccepted funding path as adopted.

A selected strategy or implementation becomes an Accepted Plan only through the explicit investor-decision lifecycle. Action Plan generation/synchronization occurs downstream from the accepted plan, not from a mere feasibility preview.

## 10. API, persistence, versioning, and UI contract

- Preserve authentication and planning-unit/goal/asset ownership enforcement.
- Preserve the distinction between preview/calculation and save/persist operations.
- Use typed schemas for goal input, calculation result, feasibility, funding paths, assumptions, and version metadata.
- Persist versioned goal snapshots where the existing save contract requires it; make historical versions distinguishable from current versions.
- Record assumption sources, reference date, calculation version, and relevant source snapshot/version.
- On a material goal update, trigger the existing/defined targeted recalculation and revalidation path; do not silently replace an Accepted Plan.
- Display missing/incomplete inputs and assumptions next to results; do not render unavailable values as zero or as healthy.
- Show projected values as estimates with assumptions, not guarantees.
- Keep Goal History/reporting consistent with the distinction between a saved goal version, a scenario, and an Accepted Plan.
- Verify live database schema, RLS, and production deployment independently; source-level table references do not prove production state.

## 11. Acceptance criteria

1. Goal inputs and goal-type-specific requirements are validated, with missing inputs surfaced explicitly.
2. Target-date requirement, mapped-resource projection, funding gap/surplus, and required contribution are traceable to named assumptions.
3. Feasibility status distinguishes feasible, feasible-with-changes, not-feasible, incomplete, and no-acceptable-path outcomes (or a reviewed compatible equivalent).
4. Funding mechanisms are not misclassified as Strategy Builder strategies.
5. Alternative funding paths use comparable assumptions and expose cash-flow, debt, liquidity, timing, uncertainty, and competing-goal consequences where relevant.
6. Debt existence, DTI, leverage, or a negative Investment–Debt Spread alone never selects a strategy.
7. Goal Planner consumes canonical Moneywheel metrics and metadata without duplicating their formulas.
8. Asset mapping never implicitly earmarks, sells, locks, or commits the asset.
9. Shared assets/surplus are not silently counted as fully available to multiple goals.
10. Whole-plan analysis is invoked when a material cross-goal dependency exists and is not indiscriminately run for every local edit.
11. Calculating feasibility alternatives or proposed goal-condition adjustments does not overwrite the canonical goal or Accepted Plan before explicit investor acceptance.
12. A goal cancellation does not delete the underlying Financial State asset; earmark release/remapping is a separate lifecycle action.
13. Material changes trigger targeted recalculation/revalidation under a shared, explicit policy.
14. Strategy Builder receives a typed feasibility/funding context and does not silently recreate feasibility.
15. Tests cover calculation boundaries, missing/invalid inputs, asset resolution, shared-resource conflicts, funding-path comparisons, version history, ownership, and non-mutation before adoption.
16. Test results, live database/RLS state, and deployment status are reported only when actually verified.
17. Goal-Level Return Required is scenario-specific, traceable to cash-flow timing and assumptions, and distinct from required contribution and expected return.
18. Constraint violations are not bypassed to manufacture feasibility; an unacceptable/no-path result is supported.
19. Goal Feasibility first evaluates financial-capacity/surplus optimization, including relevant Opportunity Cost comparisons, without changing the investor's current target amount or date.
20. If Approach 1 is insufficient, Goal Feasibility calculates the required target-amount reduction and/or target-date extension, quantifies their effects, and leaves the canonical goal unchanged until explicit investor acceptance.
21. Both approaches use the same feasibility rules/engine; there is no separate What-If feasibility engine or duplicate calculation path.
22. If no financially acceptable path or goal adjustment exists within constraints, the result clearly reports no acceptable path and the binding reasons.
23. Both individual-goal feasibility and conditional combined-goal/shared-resource feasibility are covered by tests.

## 12. Source authority and evidence

### Goal Planner feature intent
- `docs/feature/Goal-Planner.md`

### Existing-code evidence (audited at the stated source revision; re-check against current main)
- `docs/existing features/Goal-Planner/00-BACKEND-INDEX.md`
- `docs/existing features/Goal-Planner/01-API-AND-REQUEST-BOUNDARY.md`
- `docs/existing features/Goal-Planner/02-TAXONOMY-AND-DATA-CONTRACTS.md`
- `docs/existing features/Goal-Planner/03-GOAL-CALCULATION-ENGINE.md`
- `docs/existing features/Goal-Planner/04-ASSET-MAPPING-AND-FUNDING-PROJECTIONS.md`
- `docs/existing features/Goal-Planner/05-FEASIBILITY-AND-WORKFLOW-READINESS.md`
- `docs/existing features/Goal-Planner/06-PERSISTENCE-AND-VERSIONING.md`
- `docs/existing features/Goal-Planner/07-MULTI-GOAL-PLANNING.md`
- `docs/existing features/Goal-Planner/08-TESTS-AND-EVIDENCE-GAPS.md`

### Cross-feature business-rule evidence (intent, not proof of runtime implementation)
- `docs/Real-Life Decision Cases/00-GOAL_FUNDING_CONCEPT_CHANGE_LOG.md`
- `docs/Real-Life Decision Cases/16-CONCEPTS_OUTSIDE_EXISTING_FEATURES_REGISTER.md`
- `docs/implementations/Moneywheel.md`

## 13. Explicit non-goals

This specification does not authorize an unreviewed rewrite of all goal formulas, hidden/default assumptions presented as investor facts, automatic selection of Debt Reduction or investment from one metric, treating asset mapping as earmarking, forced recommendations when no path is acceptable, automatic replacement of an Accepted Plan, indiscriminate whole-plan rebuilds, duplicating Moneywheel calculations, or claiming tests/production database/RLS/deployment are verified without evidence.
