# Real-Life Decision Cases — Master Register

**Folder:** `docs/Decision tree/Real-Life Decision Cases/`  
**Purpose:** One entry point for the case library: what each document establishes, how the cases connect, and which decisions still need reconciliation.  
**Status:** REGISTER / NAVIGATION + ALIGNMENT — not a new business-rule authority and not proof that every rule is implemented.  
**Reviewed folder contents:** 15 Markdown documents on the inspected `main` tree.  
**Last checked:** 2026-10-12

---

## 1. How to read this folder

The files are not 15 unrelated examples. Together, they describe a financial-planning product from goal feasibility through strategy choice, implementation, investor approval, execution, and later plan changes.

Use this register to find the right case and understand its role. For an unresolved rule, read the source case and the alignment audit; do not resolve conflicts just by counting how many documents repeat a statement.

**Status distinction**
- **Case/business direction:** what the real-life example says the system should do.
- **Target architecture:** how the product is proposed to work.
- **Current implementation:** what active code actually does; must be verified separately.
- **Frozen V1 rule:** only when explicitly approved and tested. The presence of a “canonical” or “final” label alone does not prove this status.

## 2. Case index

| File | Main question | Core conclusion / use |
|---|---|---|
| [00 — Goal Funding Concept Change Log](00-GOAL_FUNDING_CONCEPT_CHANGE_LOG.md) | What does Goal Funding really mean, and which layer owns it? | Establishes the business clarification that Goal Funding / Goal Feasibility belongs to Goal Planner, not automatically as a peer Strategy Builder strategy. Funding mechanisms such as SIP, lump sum and step-up are not the whole feasibility decision. **Concept is not fully implemented/frozen in code.** |
| [03 — Multi-Goal Feasibility and Action Plan](03-CASE_3_MULTI_GOAL_FEASIBILITY_AND_ACTION_PLAN.md) | What if several goals compete for the same surplus/resources? | Evaluate goal-level feasibility, identify resource conflict and trade-offs, and create an Action Plan only downstream of investor adoption. Whole-Plan Impact is conditional on a material plan-level issue. |
| [04 — Better-Path Strategy and Implementation](04-CASE_4_BETTER_PATH_STRATEGY_AND_IMPLEMENTATION.md) | What if the current path works, but another path may work better? | Compare meaningful alternatives and their trade-offs. A better-path proposal does not automatically replace the accepted plan; the investor decides. |
| [05 — Plan Adaptation After Financial State Change](05-CASE_5_PLAN_ADAPTATION_AFTER_FINANCIAL_STATE_CHANGE.md) | What if income, expenses, assets, liabilities or surplus changes? | Assess materiality, identify affected goals/strategies and revalidate only the affected scope. Do not rebuild or replace the entire plan automatically. |
| [06 — Goal / Intent Change and Recalculation](06-CASE_6_GOAL_INTENT_CHANGE_AND_RECALCULATION.md) | What if the investor changes a goal or its assumptions? | Recalculate feasibility first, then check impact on existing strategy/plan. A changed goal remains proposed until the investor adopts the resulting plan. |
| [07 — New Goal Against Existing Plan](07-CASE_7_NEW_GOAL_AGAINST_EXISTING_PLAN.md) | What if the investor adds a goal after a plan already exists? | Check feasibility and resource competition against the Accepted Plan. A rejected new goal must not silently consume committed resources or alter the existing plan. |
| [08 — Investor Strategy Change and Multi-Strategy Plan](08-CASE_8_INVESTOR_STRATEGY_CHANGE_AND_MULTI_STRATEGY_PLAN.md) | What if the investor wants to change or combine strategies? | Multiple strategies may coexist where justified. Compare effects and preserve the current Accepted Plan until the proposed change is explicitly adopted. |
| [09 — Execution Plan, What-If and Impact Guidance](09-CASE_9_EXECUTION_PLAN_WHAT_IF_AND_IMPACT_GUIDANCE.md) | What if the investor experiments with execution amounts or choices? | Keep a what-if scenario separate from the Accepted Plan, calculate its impact and let the investor choose whether to adopt it. |
| [10 — Execution Change Triggering Strategy Re-evaluation](10-CASE_10_EXECUTION_CHANGE_TRIGGERING_STRATEGY_REEVALUATION.md) | When does an execution change mean the current strategy needs another look? | Run impact analysis and targeted strategy revalidation first. An execution change does not automatically mean the strategy must be replaced. |
| [11 — Iterative Strategy, Execution and Revalidation](11-CASE_11_ITERATIVE_STRATEGY_EXECUTION_AND_REVALIDATION.md) | How does planning continue after the first recommendation and execution? | Defines a repeatable loop: Accepted Plan → execution/what-if → impact → targeted revalidation → investor decision → updated Accepted Plan and Action Plan. Scenarios remain separate until adopted. |
| [12 — No Acceptable Path and Investor-Designed Strategy](12-CASE_12_NO_ACCEPTABLE_PATH_AND_INVESTOR_DESIGNED_STRATEGY.md) | What if none of the standard options is acceptable? | “No acceptable path” is a valid result. The investor may change goals/assumptions or propose an alternative; that proposal still needs constraint, impact and stress review plus explicit adoption. |
| [13 — System Update and Feature Implementation Plan](13-DECISION_TREE_SYSTEM_UPDATE_AND_FEATURE_IMPLEMENTATION_PLAN.md) | What gaps separate the desired product from current code? | Audit and implementation plan, **not code changes**. Identifies issues including Goal Funding ownership, stale IDs, variant-selection placement, investor-priority authority, MoneyWheel/constraint boundaries and incomplete lifecycle/revalidation. |
| [14 — Canonical System Structure and Alignment](14-REAL_LIFE_CASES_CANONICAL_SYSTEM_STRUCTURE_AND_ALIGNMENT.md) | What common system model connects all the cases? | Alignment audit defining the broader product lifecycle, the individual-goal Strategy Decision subsystem and the change/revalidation loop. Explicitly **not yet frozen**. |
| [15 — Asset Mapping vs Asset Earmarking](15-CANONICAL_ASSET_MAPPING_VS_ASSET_EARMARKING_DECISION_CASE.md) | Is assigning an asset to a goal the same as reserving/protecting it for that goal? | No. Asset Mapping is a Goal Planning relationship/projection; Asset Earmarking is an intentional reservation/protection decision that may arise during strategy/implementation. **Business decision documented; not yet implemented in code.** |
| [Strategy Decision Tree](strategy-decision-tree.md) | What should the individual-goal Strategy Decision Tree decide? | Defines candidate applicability, viability, strategy selection, variants, techniques and solution derivation. States a four-strategy Strategy Builder and places Goal Funding in Goal Planner. Treat as the business benchmark, not proof that runtime matches it. |

**Numbering note:** the folder contains the Goal Funding concept log labelled “Case 1” and then a file labelled Case 3 onward. No Case 2 document appeared in the inspected folder inventory. This register does not invent or renumber a missing case.

## 3. The combined system these cases describe

### A. Main planning lifecycle

**Financial State + Investor Goals**  
→ Goal Planning / Goal Feasibility  
→ [Whole-Plan Impact only if material cross-goal/resource impact exists]  
→ Strategy Decision  
→ Implementation Design  
→ Stress / Resilience  
→ Decision / Recommendation  
→ Investor Accept / Reject / Modify  
→ Accepted Plan  
→ Action Plan  
→ Execution

### B. Individual-goal Strategy Decision

**Goal context + Financial State + feasibility evidence + constraints**  
→ Applicability  
→ Viability / eligibility  
→ Strategy selection  
→ Variant  
→ Technique selection  
→ Method / Policy  
→ Architecture / Solution  
→ Stress / Resilience and possible re-evaluation  
→ Decision / Recommendation

### C. Change and adaptation loop

**Accepted Plan**  
→ financial-state / goal / new-goal / strategy / execution / assumption change  
→ materiality and impact analysis  
→ targeted revalidation  
→ recommendation if required  
→ investor decision  
→ updated Accepted Plan and Action Plan if accepted

These are the **target business flows documented by the cases**. They are not a claim that current runtime executes these stages in this exact order.

## 4. Rules that recur across the cases

1. **Goal Funding belongs to Goal Planner / Goal Feasibility** as a funding requirement and feasibility/path analysis; do not automatically treat it as a peer Strategy Builder strategy.
2. **Goal feasibility and strategy choice are different decisions.** A funding gap does not by itself mean Debt Reduction or Credit Utilisation should be selected.
3. **A metric is not a decision.** Ratios and diagnostics provide evidence; the responsible constraint/decision policy determines the consequence.
4. **Strategy, Variant, Technique, Method/Policy and Solution are different entity types.** Do not relabel a technique as a solution or a contribution mechanism as a strategy simply because a legacy table does so.
5. **Whole-Plan / Multi-Goal Impact is conditional.** Use it when shared resources, goal conflicts or accepted-plan consequences make the decision plan-level; do not require it for every individual goal.
6. **A better alternative is still a proposal.** The system must show consequences and trade-offs without silently replacing the accepted plan.
7. **Investor authority is explicit.** Recommendation is not adoption; Accept / Reject / Modify must have different state effects.
8. **A what-if scenario does not overwrite the Accepted Plan.** Preserve proposed, rejected and accepted versions separately.
9. **Revalidation should be targeted.** Identify dependencies and affected scope before recalculating; avoid rebuilding unrelated goals.
10. **No acceptable path is a valid outcome.** Do not force a recommendation when candidates fail constraints, viability or resilience.
11. **Investor-designed alternatives are not fake standard strategies.** Capture and validate the proposed logic explicitly, and preserve its origin.
12. **Asset Mapping and Asset Earmarking are distinct.** Mapping records which assets are counted toward a goal; earmarking intentionally reserves/protects resources for implementation.

## 5. Important unresolved decisions — do not silently treat as settled

| ID | Open decision | Why it matters | Main source(s) |
|---|---|---|---|
| RLC-01 | Final Strategy Builder strategy set and fate of `strat-goal-funding` | Current code/audits describe five IDs, while the real-life cases specify four peer strategies and Goal Funding under Goal Planner. Migration affects variants, scenarios, scoring and saved strategy versions. | `00-GOAL_FUNDING_CONCEPT_CHANGE_LOG.md`; `13-DECISION_TREE_SYSTEM_UPDATE_AND_FEATURE_IMPLEMENTATION_PLAN.md`; `14-REAL_LIFE_CASES_CANONICAL_SYSTEM_STRUCTURE_AND_ALIGNMENT.md`; `strategy-decision-tree.md` |
| RLC-02 | Exact Goal Funding / feasibility mathematics | Cases establish the responsibility boundary, but exact optimization, alternative-path comparison and materiality rules are not all frozen. | `00-GOAL_FUNDING_CONCEPT_CHANGE_LOG.md`; Cases 3–7 |
| RLC-03 | Canonical taxonomy and migration of variants/techniques/solutions | Existing architecture tables conflict on whether SIP/lump sum, techniques and solutions are variants or peer entities. | `strategy-decision-tree.md`; `14-REAL_LIFE_CASES_CANONICAL_SYSTEM_STRUCTURE_AND_ALIGNMENT.md`; Decision Tree Steps 05–07 |
| RLC-04 | Target stage order versus active runtime order | Existing audit says architecture/technique processing occurs before final strategy selection and variant selection occurs inside recommendation. | `13-DECISION_TREE_SYSTEM_UPDATE_AND_FEATURE_IMPLEMENTATION_PLAN.md`; `14-REAL_LIFE_CASES_CANONICAL_SYSTEM_STRUCTURE_AND_ALIGNMENT.md` |
| RLC-05 | Whole-Plan Impact versus Multi-Goal Planning contract | Current consolidated planning and conditional change-impact analysis need distinct responsibilities/contracts. | Case 3; Cases 5–7; Cases 13–14 |
| RLC-06 | Materiality thresholds and targeted revalidation policy | Cases establish the workflow, but exact thresholds/algorithms are not all frozen. | Cases 5, 6, 10, 11 |
| RLC-07 | Investor priority and override authority | The system must show conflicts and choices without silently overriding the investor; precise selection influence remains to be approved. | Cases 3, 7, 8, 12–14 |
| RLC-08 | Stress/resilience gate and re-selection rules | Scenario/what-if behavior exists, but a complete canonical stress taxonomy and re-selection policy remain unestablished. | Cases 4, 9–12; Decision Tree Step 08 |
| RLC-09 | Asset Earmarking ownership and execution semantics | Case 15 distinguishes it from mapping, but implementation, persistence, conflict handling and activation rules still need code alignment. | `15-CANONICAL_ASSET_MAPPING_VS_ASSET_EARMARKING_DECISION_CASE.md` |
| RLC-10 | Investor-designed strategy data contract | Needs a clear representation that does not falsely classify an investor proposal as a standard library strategy. | Case 12; Decision Tree Step 13; Journey/Implementation 21 |

## 6. Recommended source order when documents disagree

This is a review procedure, not a declaration that conflicts have already been resolved:

1. **Use the specific case document** for the concrete scenario, investor intent and reasoning.
2. **Use `14-REAL_LIFE_CASES_CANONICAL_SYSTEM_STRUCTURE_AND_ALIGNMENT.md`** to understand the cross-case lifecycle, while respecting its “not yet frozen” status.
3. **Use `strategy-decision-tree.md`** for the stated Strategy Decision business model, but compare its taxonomy with the Goal Funding concept log and system alignment audit.
4. **Use Case 13** for implementation gaps and proposed engineering work; it explicitly is an implementation plan, not code changes.
5. **Check active code paths and tests separately** before claiming behavior is implemented.
6. If sources still disagree, record the conflict and get an explicit product decision. Do not delete or rewrite code based only on a document label.

## 7. How this register should be maintained

When a case is added or changed:
- add it to Section 2 with its purpose, conclusion and implementation/freeze status;
- update Section 4 only for a rule supported by the case;
- add unresolved policy questions to Section 5 rather than guessing;
- preserve the original case's reasoning and examples;
- distinguish case evidence, target design, approved policy and runtime behavior;
- record the commit SHA and date after the next code-level verification.

**Deletion / cleanup rule:** this folder is a business-evidence library. Similar wording does not automatically make a case redundant. Do not delete or merge case documents until their unique scenarios, decisions, dependencies and references have been checked.

---

## 8. Folder file inventory

- `00-GOAL_FUNDING_CONCEPT_CHANGE_LOG.md`
- `03-CASE_3_MULTI_GOAL_FEASIBILITY_AND_ACTION_PLAN.md`
- `04-CASE_4_BETTER_PATH_STRATEGY_AND_IMPLEMENTATION.md`
- `05-CASE_5_PLAN_ADAPTATION_AFTER_FINANCIAL_STATE_CHANGE.md`
- `06-CASE_6_GOAL_INTENT_CHANGE_AND_RECALCULATION.md`
- `07-CASE_7_NEW_GOAL_AGAINST_EXISTING_PLAN.md`
- `08-CASE_8_INVESTOR_STRATEGY_CHANGE_AND_MULTI_STRATEGY_PLAN.md`
- `09-CASE_9_EXECUTION_PLAN_WHAT_IF_AND_IMPACT_GUIDANCE.md`
- `10-CASE_10_EXECUTION_CHANGE_TRIGGERING_STRATEGY_REEVALUATION.md`
- `11-CASE_11_ITERATIVE_STRATEGY_EXECUTION_AND_REVALIDATION.md`
- `12-CASE_12_NO_ACCEPTABLE_PATH_AND_INVESTOR_DESIGNED_STRATEGY.md`
- `13-DECISION_TREE_SYSTEM_UPDATE_AND_FEATURE_IMPLEMENTATION_PLAN.md`
- `14-REAL_LIFE_CASES_CANONICAL_SYSTEM_STRUCTURE_AND_ALIGNMENT.md`
- `15-CANONICAL_ASSET_MAPPING_VS_ASSET_EARMARKING_DECISION_CASE.md`
- `strategy-decision-tree.md`
