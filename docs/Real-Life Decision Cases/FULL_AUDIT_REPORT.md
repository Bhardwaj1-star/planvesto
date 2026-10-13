# PlanVesto Decision Tree — Full Documentation & Taxonomy Audit

**Audit date:** 12 October 2026  
**Repository:** `Bhardwaj1-star/planvesto`  
**Branch:** `main`  
**Scope:** `docs/Decision tree/Real-Life Decision Cases/`, canonical Strategy Decision Tree, related architecture documents, discrepancy audit, and targeted code definitions.

## 1. Executive conclusion

At the time of this audit, the documents did not establish one consistent, implementation-ready relationship between Strategy, Variant, Technique, Architecture, Solution and Action. The canonical Strategy Decision Tree was clearer than several older architecture documents and case bodies. The Goal Funding classification in the target case documents has since been corrected; other architecture/solution and runtime gaps described in this report remain audit findings until separately resolved.

The most important verified problem is not merely wording: `backend/library/strategies/solution_matrix.py` constructs “solutions” differently by strategy. For Goal Funding, each solution record wraps a **variant**; for the other four strategies, each wraps a **technique**. `Solution` is therefore not one consistent business abstraction across the strategy set.

**No application code or existing case files were changed as part of this audit.** This report records findings and recommendations, not implemented fixes.

## 2. Audit inventory and limitations

### Real-Life Decision Cases folder

The following 13 accessible files were inspected:

1. `00-GOAL_FUNDING_CONCEPT_CHANGE_LOG.md` — historical discussion covering Case 1 and Case 2.
2. `03-CASE_3_MULTI_GOAL_FEASIBILITY_AND_ACTION_PLAN.md`
3. `04-CASE_4_BETTER_PATH_STRATEGY_AND_IMPLEMENTATION.md`
4. `05-CASE_5_PLAN_ADAPTATION_AFTER_FINANCIAL_STATE_CHANGE.md`
5. `06-CASE_6_GOAL_INTENT_CHANGE_AND_RECALCULATION.md`
6. `07-CASE_7_NEW_GOAL_AGAINST_EXISTING_PLAN.md`
7. `08-CASE_8_INVESTOR_STRATEGY_CHANGE_AND_MULTI_STRATEGY_PLAN.md`
8. `09-CASE_9_EXECUTION_PLAN_WHAT_IF_AND_IMPACT_GUIDANCE.md`
9. `10-CASE_10_EXECUTION_CHANGE_TRIGGERING_STRATEGY_REEVALUATION.md`
10. `11-CASE_11_ITERATIVE_STRATEGY_EXECUTION_AND_REVALIDATION.md`
11. `12-CASE_12_NO_ACCEPTABLE_PATH_AND_INVESTOR_DESIGNED_STRATEGY.md`
12. `15-CANONICAL_ASSET_MAPPING_VS_ASSET_EARMARKING_DECISION_CASE.md`
13. `strategy-decision-tree.md`

Separate Case 2, Case 13 and Case 14 files were not found on `main` through exact-path fetches and repository search. Case 2 is represented in the 00 change log. The older `docs/audit/DOCUMENT_DISCREPANCY_AUDIT.md` references a Case 14 file; that reference should be checked and either restored, redirected or marked stale.

### Supporting sources inspected

- `docs/architecture/strategy-matrix.md`
- `docs/architecture/strategy-variants.md`
- `docs/architecture/strategy-architecture-composition.md`
- `docs/Decision tree/07-ARCHITECTURE_COMPOSITION_CURRENT_STATE_AND_RECOMMENDATION.md`
- `docs/Decision tree/00.6-RULE_OWNERSHIP_KEEP_MERGE_REPLACE_REMOVE_NEW_AUDIT.md`
- `docs/audit/DOCUMENT_DISCREPANCY_AUDIT.md`
- `backend/library/strategies/solution_matrix.py`
- `backend/models/strategy.py`

This is a documentation and taxonomy audit with targeted inspection of code models/registries. It is not a full runtime test, a line-by-line audit of every repository file, or proof that target behavior is implemented.

## 3. Findings ranked by severity

### F-01 — `Solution` has inconsistent meaning in current code
**Severity: Critical**

`backend/library/strategies/solution_matrix.py` documents Solution as a concrete implementation path inside a strategy, but construction differs by strategy:
- Goal Funding: one solution record per Goal Funding variant; `variant_id` is populated and `technique_ids` is empty.
- Progressive De-risking, Capital Preservation, Debt Reduction and Credit Utilisation: one solution record per declared technique; `technique_ids` contains that technique and `variant_id` is empty.

The `StrategyArchitecture` model separately stores `solution_ids` and `technique_ids`, so the data model contains both concepts, while the registry uses Solution as a wrapper for different types. This makes IDs, selection, reporting and persistence semantics ambiguous.

**Required resolution:** Use one definition for every strategy. Recommended target: Solution is the assembled investor-specific implementation outcome, not a second catalog label for a Variant or Technique. It should reference selected Strategy, Variant, Technique set, method/policy and calculated implementation parameters. If a standalone Solution registry is unnecessary, remove it from the taxonomy only after callers and persisted records are migrated. Do not silently rename technique records as solution records.

### F-02 — Goal Funding is both inside and outside the canonical Strategy set
**Severity: Critical**

The canonical `strategy-decision-tree.md` defines four Strategy Builder strategies: Progressive De-risking, Capital Preservation, Debt Reduction and Credit Utilisation. It explicitly places Goal Funding in Goal Planner / Goal Feasibility, not as a fifth Strategy Builder strategy.

Contradictory sources:
- At the time of this audit, Case 8 listed Goal Funding as “Strategy A” for an Education goal; that case has since been corrected.
- At the time of this audit, Cases 10 and 11 labelled Goal Funding as a strategy; both case documents have since been corrected.
- The earlier audit referenced `docs/architecture/strategy-matrix.md`, `docs/architecture/strategy-architecture-composition.md`, and `docs/architecture/strategy-variants.md` as sources that classified Goal Funding as a Strategy or listed its six options as variants. Those paths are absent from the current repository tree; these are historical audit references, not current document paths.
- The 00 change log preserves an earlier Goal Funding-as-strategy statement, although later parts reject it.

**Documentation resolution:** The target documents now use **Goal Funding / Feasibility** or **Goal Planner funding path**. Case 8 no longer labels Goal Funding as Strategy A; Cases 10–11 distinguish funding-path changes from changes to one of the four canonical strategies. The change log retains earlier claims only as rejected/superseded history. Runtime code has not been changed by these documentation edits.

### F-03 — Six Goal Funding “variants” conflict with the four-strategy target
**Severity: Critical**

The canonical tree defines four strategies and four variants under each. Older current-state/rule-ownership material describes five active strategies and 22 active variants, including Goal Funding; those are legacy-runtime/audit observations, not target taxonomy. The earlier audit referenced architecture files under `docs/architecture/` that are absent from the current repository tree. Six historical Goal Funding options—Existing Assets, SIP, Lumpsum, Lumpsum + SIP, Lumpsum + Step-up SIP and Step-up SIP—must be treated as Goal Planner funding paths, not Strategy Builder variants.

The canonical variant document also says SIP, Lumpsum and Step-up SIP are not Strategy Variants. The matrix repeats funding mechanisms in both Variants and Solutions columns.

**Remaining runtime/migration requirement:** Publish a single versioned registry with exactly one primary type and owner per ID. The documentation target now classifies these six choices as **Goal Planner funding paths/mechanisms**, not Strategy Builder variants. Describe the 22-variant registry as legacy current state until migration is verified; do not call it the target registry.

### F-04 — Case 3 puts Action Plan before Strategy Builder
**Severity: High**

`03-CASE_3_MULTI_GOAL_FEASIBILITY_AND_ACTION_PLAN.md`, in “Correct Overall Flow”, places Action Plan immediately after “Construct a Feasible Overall Path”, then runs Strategy Builder → Strategy → Variant → Technique → Architecture → Strategy Execution Actions.

This contradicts the lifecycle at the top of the case and the canonical tree, which places Investor Decision / Adoption → Accepted Plan → Action Plan → Execution after strategy/implementation work.

**Required resolution:** Use this flow: Goal Feasibility / Whole-Plan Planning → Strategy Decision → Variant → Technique / Method → Architecture / Solution → Stress / Resilience → Decision / Recommendation → Investor Decision → Accepted Plan → Action Plan → Execution. If a feasibility action does not require Strategy Builder, label it **Goal Planner prerequisite action**, not the accepted Action Plan.

### F-05 — Architecture and Solution are combined in one place and separate in another
**Severity: High**

The canonical tree sometimes uses `Architecture / Solution` as one step, while its hierarchy omits Architecture. The architecture-composition document defines Architecture as a composed object containing primary/supporting strategies, solution IDs and technique IDs, and describes Solutions as concrete implementation paths within that architecture.

**Required resolution:** Define once and use consistently:
- **Architecture:** structural composition/container for the selected path.
- **Solution:** concrete investor-specific implementation outcome assembled within that architecture.
- **Action:** executable step generated from the accepted implementation.

### F-06 — Strategy Matrix duplicates and misclassifies Goal Funding mechanisms
**Severity: High**

The earlier audit reported that `docs/architecture/strategy-matrix.md` repeated Goal Funding mechanisms in Variants and Solutions columns and included Contribution Escalation and Tax-Efficient Sequencing under Goal Funding techniques. That referenced architecture path is absent from the current repository tree; treat this as a historical audit finding, not a current document location.

**Target rule:** Any current or recreated matrix must reflect the authoritative type registry. Keep funding paths in Goal Planner ownership unless a deliberate business decision changes that classification.

### F-07 — Case 8 contradicts its own header
**Severity: High**

At the time of this audit, Case 8’s header said Goal Funding was not a Strategy Builder strategy, but its body called it Strategy A. The case document has since been corrected: Education funding is shown as a Goal Planner funding path, separate from the four canonical strategies.

**Documentation status:** Corrected in Case 8. A single investor plan may use a Goal Planner funding path and one or more of the four Strategy Builder strategies without making the funding path a strategy.

### F-08 — Cases 10–11 treat a funding-path change as a strategy change
**Severity: High**

At the time of this audit, Cases 10 and 11 called Goal Funding a strategy. Those case documents have since been corrected to recalculate the Goal Planner funding path first and re-evaluate a canonical Strategy Builder decision only when materially affected.

**Documentation status:** Corrected in Cases 10–11. Model the change first as a Goal Planner funding-path/execution change. Re-evaluate the four Strategy Builder strategies only when the change materially affects their constraints, applicability, viability or outcomes.

### F-09 — Historical change log mixes past and current policy
**Severity: Medium-High**

`00-GOAL_FUNDING_CONCEPT_CHANGE_LOG.md` preserves an older claim that Goal Funding is a strategy as rejected/superseded historical evidence and explicitly identifies the current ownership.

**Documentation status:** The change log now labels the earlier claim as rejected/superseded history and states that it is not a coding specification. Do not erase the decision history.

### F-10 — Asset Mapping vs Asset Earmarking boundary is conceptually sound, implementation status is vague
**Severity: Medium-High**

Case 15 distinguishes Asset Mapping as upstream Goal Planner feasibility evidence and Asset Earmarking as a downstream technique when a selected path requires reservation/protection. But its “not implemented in code” statement is too broad because technique registry references exist.

**Required resolution:** Separate status for definition, selection, execution, persistence and accepted-plan enforcement. A registry reference alone does not prove runtime execution is implemented.

### F-11 — “Canonical”, “final” and “not frozen” have no common status model
**Severity: Medium-High**

The Strategy Decision Tree says “Final Business Architecture”, while other audits say rules are not frozen and architecture/selection rules remain design-only. Case 15 calls itself canonical while also saying it is not implemented. Authority, approval and implementation status are different dimensions but are not consistently recorded.

**Required resolution:** Add metadata to each document: authority type (business decision / target architecture / current-state audit / historical record), decision status (proposed / approved / frozen), implementation status (not started / partial / implemented / verified), last verified commit, and supersedes/superseded-by.

### F-12 — Case series has numbering and authority gaps
**Severity: Medium**

The folder contains the Case 1–2 change log, Cases 3–12, Case 15 and the canonical tree. Separate Case 2, 13 and 14 files were not found in the current search/fetch results, although an older discrepancy audit cites Case 14.

**Required resolution:** Add a case register listing each case ID, file, question tested, decision established, status and canonical rules affected. Mark Case 2 as embedded in the 00 change log; state whether Cases 13–14 were removed, renamed or remain to be authored. Update stale references.

### F-13 — Target pipeline and current runtime are not clearly separated
**Severity: Medium-High**

Existing discrepancy and rule-ownership audits report that runtime composes architecture and executes techniques before the authoritative strategy decision, while the target pipeline places Strategy → Variant → Technique → Architecture downstream of selection. Older architecture documents still present the earlier composition order as “Runtime Flow”.

**Required resolution:** Label every pipeline `CURRENT RUNTIME` or `TARGET BUSINESS FLOW`. Do not treat a target flow as proof of implementation. Resolve current composition/decision ordering only after taxonomy and rule ownership are frozen.

## 4. Case-by-case audit summary

| File | Result | Key observation |
|---|---|---|
| `00-GOAL_FUNDING_CONCEPT_CHANGE_LOG.md` | Historical claims labelled | Preserves old Goal Funding-as-strategy wording as rejected history; canonical ownership is stated explicitly. |
| `03-CASE_3_MULTI_GOAL_FEASIBILITY_AND_ACTION_PLAN.md` | Correction required | Main body places Action Plan before Strategy Builder. |
| `04-CASE_4_BETTER_PATH_STRATEGY_AND_IMPLEMENTATION.md` | Mostly aligned | Separates Goal Planner, Strategy Builder, Implementation and Action Plan; optimization/comparison rules remain unfrozen. |
| `05-CASE_5_PLAN_ADAPTATION_AFTER_FINANCIAL_STATE_CHANGE.md` | Mostly aligned | Materiality and targeted revalidation are sound; thresholds remain unfrozen and adoption/version states are abbreviated. |
| `06-CASE_6_GOAL_INTENT_CHANGE_AND_RECALCULATION.md` | Mostly aligned | Recalculates changed inputs without automatically replacing the whole plan; formulas and asset reassignment remain unfrozen. |
| `07-CASE_7_NEW_GOAL_AGAINST_EXISTING_PLAN.md` | Mostly aligned | Treats new goal as scenario and preserves accepted plan pending investor adoption. |
| `08-CASE_8_INVESTOR_STRATEGY_CHANGE_AND_MULTI_STRATEGY_PLAN.md` | Documentation corrected | Education funding is a Goal Planner path; the four canonical Strategy Builder strategies are listed separately. |
| `09-CASE_9_EXECUTION_PLAN_WHAT_IF_AND_IMPACT_GUIDANCE.md` | Mostly aligned | Separates execution what-if from strategy change; funding options need clear Goal Planner terminology. |
| `10-CASE_10_EXECUTION_CHANGE_TRIGGERING_STRATEGY_REEVALUATION.md` | Documentation corrected | Recalculate the Goal Planner funding path first; re-evaluate a canonical strategy only if materially affected. |
| `11-CASE_11_ITERATIVE_STRATEGY_EXECUTION_AND_REVALIDATION.md` | Documentation corrected | Funding-path iterations remain in Goal Planner; Strategy Builder decisions remain separate. |
| `12-CASE_12_NO_ACCEPTABLE_PATH_AND_INVESTOR_DESIGNED_STRATEGY.md` | Mostly aligned | Valid outcome subject to constraints, impact review and explicit adoption. |
| `15-CANONICAL_ASSET_MAPPING_VS_ASSET_EARMARKING_DECISION_CASE.md` | Clarification required | Boundary is sound; split implementation status into definition/selection/execution/persistence/enforcement. |
| `strategy-decision-tree.md` | Best target authority; cleanup needed | Four-strategy set and Strategy → Variant → Technique are clear; Architecture vs Solution needs consistent layering. |

“Mostly aligned” does not mean implementation is verified. Math, thresholds, scenario mechanics, stress triggers, adoption and persistence behavior remain unfrozen in source documents.

## 5. Canonical relationship recommended for the target model

Use this as the single target contract:

```text
GOAL PLANNER
  Goal definition
  Asset Mapping
  Goal target / funding gap / feasibility
  Funding paths and contribution mechanisms
             |
             v
STRATEGY DECISION (individual goal)
  Constraints and safety evaluation
  Strategy applicability
  Candidate viability
  Strategy selection
             |
             v
  Variant selection
             |
             v
  Technique selection
             |
             v
  Method / Policy
             |
             v
  Architecture composition
             |
             v
  Investor-specific Solution
             |
             v
  Stress / Resilience and targeted revalidation
             |
             v
  Decision / Recommendation
             |
             v
INVESTOR DECISION / ADOPTION
             |
             v
ACCEPTED PLAN
             |
             v
ACTION PLAN
             |
             v
EXECUTION
```

Canonical Strategy Builder candidates:
1. Progressive De-risking
2. Capital Preservation
3. Debt Reduction
4. Credit Utilisation

**Goal Funding / Feasibility is upstream in Goal Planner, not a fifth Strategy Builder strategy.** SIP, Lumpsum, Step-up SIP and combinations belong to Goal Planner funding/execution paths unless an explicit business decision changes their canonical type.

### Type definitions

- **Strategy:** high-level financial responsibility chosen for the situation.
- **Variant:** structural form of that strategy for a particular funding, protection or liability situation.
- **Technique:** reusable mechanism selected because the chosen Strategy + Variant needs it.
- **Method / Policy:** rule for applying a technique in this specific context.
- **Architecture:** composed structure bringing selected strategies, variant, techniques, dependencies and constraints together.
- **Solution:** investor-specific implementation outcome derived from architecture and actual financial inputs; it must not merely duplicate a Variant or Technique under a different ID.
- **Action:** concrete step generated from the accepted solution and included in the Action Plan.

Example:

```text
Progressive De-risking             Strategy
  → Payment-Tranche Glide Path     Variant
  → Cash-flow Matching             Technique
  → match upcoming liabilities     Method / Policy
  → compose tranche funding        Architecture
  → calculated payment protection  Solution
  → move required amount by date   Action
```

Asset Mapping is upstream feasibility evidence. Asset Earmarking is a downstream technique when the selected variant/path calls for deliberate reservation or protection; they must not be aliases.

## 6. Recommended correction order

1. **Documentation taxonomy:** Goal Funding ownership is now explicit in the canonical tree and Strategy Builder implementation contract; the four-strategy allowlist is stated for coding agents.
2. **Runtime registry/migration remains open:** keep Goal Funding out of the target Strategy Builder set; map legacy funding options to Goal Planner funding-path concepts; do not delete or migrate records solely by name. Any registry or matrix that exists or is recreated must keep funding paths out of Strategy/Variant columns.
3. Correct case bodies: Case 3 lifecycle order; Case 8 multi-strategy example; Cases 10–11 terminology; mark historical statements in the 00 change log as superseded.
4. Standardize document metadata and case register: authority type, approval/freeze status, implementation status, commit and supersession links.
5. Separate target architecture from runtime: mark current code order as current state and canonical decision flow as target state until runtime tests prove alignment.
6. Verify implementation separately: variant selection reachability, technique selection by variant, solution-matrix semantics, architecture composition timing, stress/revalidation, and Accepted Plan / Action Plan persistence.

## 7. Final decision

**Do not refactor or delete records based only on their names.** First freeze the canonical type and ownership for every ID, then map every existing registry entry and caller to that type. The current solution matrix demonstrates why this matters: the same Solution abstraction currently means “variant wrapper” for one strategy and “technique wrapper” for the others.

This report is a recommendation only. No files were changed and no implementation behavior is claimed to be fixed.
