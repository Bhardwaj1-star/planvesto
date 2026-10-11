# Documentation Discrepancy Audit — Planvesto

**Repository:** `Bhardwaj1-star/planvesto`  
**Branch inspected:** `main`  
**Tree snapshot:** `bfd8271914f71ba1c21eaef09cdc0d14d38500b0`  
**Audit type:** Cross-document, line-referenced discrepancy audit  
**Scope:** Decision Tree, Strategy/Variant architecture, implementation specifications, user journeys, real-life cases, calculation architecture and cleanup register. This report compares what the documents say; it does not use code as proof that a documented design is implemented.  
**Interpretation rule:** “Current state” describes an existing implementation; “target/recommended” describes a proposed design. A difference is a discrepancy only when documents blur these states or make incompatible claims.

---

## Executive result

The highest-impact documentation conflicts concern **Strategy vs Goal Funding ownership**, **Variant vs Technique/Solution taxonomy**, and **the order/authority of the decision pipeline**. Other inconsistencies concern stress testing, asset earmarking, lifecycle scope, reporting readiness and stale snapshot metadata.

## Findings

### D-01 — Goal Funding ownership is contradictory
**Severity:** Critical  
**Conflict:** Is Goal Funding a Strategy Builder strategy, or a Goal Planner/feasibility responsibility?

- `docs/Implementation/00-IMPLEMENTATION_SYSTEM_MAP.md:7` says: “Goal Funding belongs to Goal Planner/feasibility, not Strategy Builder Strategy.”
- `docs/Implementation/03-GOAL_PLANNING_IMPLEMENTATION.md:5` repeats that Goal Funding is a Goal Planner/feasibility function, not a Strategy Builder Strategy.
- `docs/architecture/strategy-architecture-composition.md:44` says Goal Funding remains a “canonical first-class strategy” and its six funding variants are solutions within it.
- `docs/Decision tree/01-STRATEGY_APPLICABILITY_CURRENT_STATE_AND_RECOMMENDATION.md:29-38` lists `strat-goal-funding` among the five canonical strategies.
- `docs/architecture/strategy-matrix.md:5` gives Goal Funding a full Strategy row.

**Why this is a discrepancy:** These statements assign the same concept to two different architectural layers without clearly distinguishing “Goal Funding feasibility calculation” from “Goal Funding implementation strategy.”

**Required resolution:** Define two separate terms and contracts if both are intended:
1. **Goal Funding / Feasibility** — calculates target, gap, required contribution and affordability in Goal Planner.
2. **Funding implementation path** — chooses existing assets/SIP/lumpsum/hybrid as an implementation solution under the selected planning architecture.
Then update every document and table to use those names consistently. Otherwise choose one owner and remove the conflicting claims.

### D-02 — SIP/Lumpsum are both called Variants and explicitly not Variants
**Severity:** Critical  
**Conflict:** Taxonomy of SIP, Lumpsum and Step-up SIP is inconsistent.

- `docs/architecture/strategy-matrix.md:5` lists Existing Assets, SIP, Lumpsum, Lumpsum + SIP, Lumpsum + Step-up SIP and Step-up SIP in the **Variants** column.
- The same row lists those same items again in the **Solutions** column.
- `docs/architecture/strategy-variants.md:25-29` says variants must change architecture and explicitly says SIP, Lumpsum and Step-up SIP are **not Variants**; they remain techniques/components/solutions.
- `docs/architecture/strategy-architecture-composition.md:44` calls the six Goal Funding variants “solutions within that strategy.”
- `docs/Decision tree/05-22-VARIANT_SELECTION_CURRENT_STATE_AND_RECOMMENDATION.md` describes six Goal Funding items as canonical variants.

**Why this is a discrepancy:** The same six items are categorized as variants, solutions, and non-variant mechanisms. A reader cannot know which registry, selector, or report contract should own them.

**Required resolution:** Freeze one taxonomy table with exactly one primary type per ID: Strategy, Variant, Technique, Method/Policy, Solution, or Action. Then align the strategy matrix, variant architecture, Decision Tree step 05, and solution matrix to that table. If Goal Funding needs six selectable funding paths, name the layer explicitly (for example, “funding path”) and avoid calling it a Strategy Variant unless that is the frozen decision.

### D-03 — Decision pipeline order is stated differently across documents
**Severity:** Critical  
**Conflict:** Is architecture composed before or after authoritative strategy selection, and where does technique execution sit?

- `docs/Decision tree/00-DECISION_ENGINE_DESIGN_SUMMARY.md:40-58` presents the intended sequence as applicability → eligibility → strategy selection → variant → technique → architecture → stress → final decision/recommendation.
- `docs/Decision tree/00.5-CROSS_CUTTING_REVERIFICATION_AND_GAP_AUDIT.md:33-35,135-147,490` says current runtime order differs: architecture/technique work occurs before final strategy selection; variant selection occurs inside recommendation. It explicitly labels the canonical order as proposed/target.
- `docs/Decision tree/04-STRATEGY_SELECTION_CURRENT_STATE_AND_RECOMMENDATION.md:4` describes the current pipeline as scenario generation → architecture composition → technique execution → eligibility evaluation → decision score.
- `docs/architecture/strategy-architecture-composition.md:21-23` says “Decision → Architecture Composition → Technique Execution.”
- `docs/Implementation/05-STRATEGY_DECISION_IMPLEMENTATION.md:3` puts strategy selection → variant → technique → method/policy → architecture/solution → stress → decision/recommendation.
- `docs/Implementation/06-IMPLEMENTATION_DESIGN_IMPLEMENTATION.md:3` says architecture is downstream of authoritative Strategy selection.

**Why this is a discrepancy:** Current runtime, target pipeline, and implementation sequence are mixed together, and even the target documents differ on whether technique selection precedes architecture composition.

**Required resolution:** Label every flow as **CURRENT RUNTIME** or **TARGET FLOW**. Freeze one target order and define the interface between selection, composition and execution. Avoid calling a target flow “current” in summary tables.

### D-04 — Variant selection is described as both a current stage and a recommendation sub-step
**Severity:** High  
**Conflict:** Does VariantSelector make an independent authoritative decision, or does Recommendation choose the variant after strategy selection?

- `docs/Decision tree/00-DECISION_ENGINE_DESIGN_SUMMARY.md:75-83,285-293` lists VariantSelector as the current owner but also says selection is inside recommendation and not independent.
- `docs/Decision tree/00.5-CROSS_CUTTING_REVERIFICATION_AND_GAP_AUDIT.md:143,187-205` says variant selection happens inside recommendation and is not yet an independent stage.
- `docs/Decision tree/09-FINAL_DECISION_AND_RECOMMENDATION_CURRENT_STATE_AND_RECOMMENDATION.md:121-123,504-506` says current order is Strategy Decision → Recommendation → Variant Selection → Recommendation Output, while target architecture should make variant selection explicit before final recommendation.
- `docs/architecture/strategy-variants.md:111-113` says variant selection should occur after Strategy eligibility and before report/scenario generation.

**Why this is a discrepancy:** A registry/selector existing is not the same as an independent decision stage. Some documents describe the intended architecture while others describe runtime, without consistently marking the distinction.

**Required resolution:** State one current-state sentence and one target-state sentence in every relevant summary. Keep “selector exists” separate from “selector is an authoritative stage in the pipeline.”

### D-05 — Variant → Technique → Solution hierarchy is not stable
**Severity:** High  
**Conflict:** The canonical relationship among Variant, Technique, Method/Policy, Solution and Action changes by document.

- `docs/Implementation/00-IMPLEMENTATION_SYSTEM_MAP.md:7` says preserve **Strategy → Variant → Technique → Method/Policy → Solution → Action**.
- `docs/Implementation/05-STRATEGY_DECISION_IMPLEMENTATION.md:3` uses the same hierarchy before architecture/solution.
- `docs/architecture/strategy-variants.md:11` gives **Strategy → Variant → Report Architecture → Scenario → Actions**, omitting Technique, Method/Policy and Solution from that hierarchy.
- `docs/architecture/strategy-architecture-composition.md:14-18,44` treats Techniques, Components and Solutions as separate responsibilities, but calls the six Goal Funding variants “solutions.”
- `docs/Decision tree/Real-Life Decision Cases/14-REAL_LIFE_CASES_CANONICAL_SYSTEM_STRUCTURE_AND_ALIGNMENT.md:19` uses Strategy → Variant → Technique → Method/Policy → Architecture/Solution.

**Why this is a discrepancy:** A single hierarchy is needed for IDs, selection, persistence, report rendering and action generation. The current documents do not define whether “Report Architecture” is a layer, an output representation, or a synonym for Solution/Architecture.

**Required resolution:** Publish one canonical glossary + hierarchy diagram. Define whether Architecture is a container composed from techniques/solutions or a node between Method/Policy and Solution. Update every flow to reference the same hierarchy.

### D-06 — Stress/resilience has two different decision contracts
**Severity:** High  
**Conflict:** Is stress only explanatory evidence for the investor, or does it trigger re-selection of strategy/variant and a re-run of hard constraints?

- `docs/Decision tree/08-STRESS_RESILIENCE_CURRENT_STATE_AND_RECOMMENDATION.md:30,63-65,152-166` says current what-if functionality is not a complete stress engine and lacks a formal re-selection/resilience gate.
- `docs/Decision tree/00-DECISION_ENGINE_DESIGN_SUMMARY.md:65-67,408-426` proposes replaying the same decision logic under shocked inputs and lists stress-triggered re-selection as missing.
- `docs/Decision tree/Real-Life Decision Cases/14-REAL_LIFE_CASES_CANONICAL_SYSTEM_STRUCTURE_AND_ALIGNMENT.md:542-568` says stress is not a second engine and may trigger targeted revalidation; exact thresholds/categories remain unfrozen.
- `docs/User Journeys/08-STRESS_RESILIENCE_JOURNEY.md:9-27` describes stress results being shown to the investor and says stress testing does not silently change the plan.
- `docs/Implementation/08-STRESS_RESILIENCE_IMPLEMENTATION.md:3-5` requires recalculation of affected funding, affordability, cash-flow and risk outputs, while stress supports decision-making rather than hidden Strategy selection.

**Why this is a discrepancy:** These can be compatible, but only if the trigger contract is explicit: stress must not silently mutate the accepted plan, yet it may trigger a new proposed decision/recommendation after re-evaluation. The documents do not consistently state that distinction.

**Required resolution:** Specify a state machine: baseline → stressed evidence → (stable: explain only) or (material failure: rerun constraints/eligibility/strategy/variant) → proposed recommendation → investor accept/modify/reject. Never auto-overwrite the Accepted Plan.

### D-07 — Asset Mapping vs Asset Earmarking implementation status is ambiguous
**Severity:** High  
**Conflict:** Is Asset Earmarking merely a proposed technique, already part of the canonical strategy matrix, or an implemented runtime behavior?

- `docs/Decision tree/Real-Life Decision Cases/15-CANONICAL_ASSET_MAPPING_VS_ASSET_EARMARKING_DECISION_CASE.md:4-5` marks the distinction as a canonical business decision document **not yet implemented in code**.
- The same document `:15-19,252-288` says Asset Mapping is upstream Goal Planner work and Asset Earmarking may be a Technique downstream of Strategy/Variant.
- `docs/architecture/portfolio-asset-mapping.md:3-21` marks Asset Mapping architecture as **CANONICAL** and assigns mapping/projection to Goal Planner.
- `docs/architecture/strategy-matrix.md:5` lists Asset Earmarking under Goal Funding techniques.
- `docs/architecture/strategy-variants.md:19` also names Asset Earmarking as a technique distinct from variants.

**Why this is a discrepancy:** The conceptual boundary is clear, but the phrase “not yet implemented” is broad: it does not say whether the boundary is unimplemented, whether the technique registry entry exists but execution is incomplete, or whether actual earmarking decisions are persisted/enforced.

**Required resolution:** Split status into **definition exists**, **selection policy exists**, **execution/persistence exists**, and **accepted-plan enforcement exists**. Mark each separately. Do not use “implemented” as a single all-or-nothing status.

### D-08 — “Canonical” status is mixed with “not frozen” / “not implemented”
**Severity:** High  
**Conflict:** Readers cannot reliably distinguish an approved concept from a proposed architecture or an implemented feature.

- `docs/architecture/strategy-architecture-composition.md:3`, `docs/architecture/multi-goal-planning.md:3`, `docs/architecture/portfolio-asset-mapping.md:3` use **Status: CANONICAL**.
- `docs/Decision tree/00-DECISION_ENGINE_DESIGN_SUMMARY.md:5` says rules are **not frozen**.
- `docs/Decision tree/00.5-CROSS_CUTTING_REVERIFICATION_AND_GAP_AUDIT.md:11` says not ready for V1 freeze.
- `docs/Decision tree/Real-Life Decision Cases/14-REAL_LIFE_CASES_CANONICAL_SYSTEM_STRUCTURE_AND_ALIGNMENT.md:5` says the business structure is **not yet frozen**.
- `docs/Decision tree/Real-Life Decision Cases/15-CANONICAL_ASSET_MAPPING_VS_ASSET_EARMARKING_DECISION_CASE.md:5` says the decision is not yet implemented.

**Why this is a discrepancy:** “Canonical” is used for architecture, vocabulary, policy, and sometimes business decisions without a shared status model. A canonical architecture can exist while rules are unfrozen, but the documents do not consistently define that distinction.

**Required resolution:** Add a required metadata block to every design doc: **Decision status** (proposed/approved/frozen), **Implementation status** (not started/partial/implemented/verified), **Authority type** (business rule/architecture/reference/audit), **Last verified commit**. Reserve “CANONICAL” for a clearly defined authority type, not as a synonym for approved and implemented.

### D-09 — Goal-level Strategy decision and whole-plan multi-goal impact are sometimes collapsed
**Severity:** Medium-High  
**Conflict:** Is Whole-Plan / Multi-Goal Impact a mandatory stage for every strategy decision, or a conditional branch?

- `docs/Decision tree/Real-Life Decision Cases/14-REAL_LIFE_CASES_CANONICAL_SYSTEM_STRUCTURE_AND_ALIGNMENT.md:16-24,58-60` explicitly says Whole-Plan/Multi-Goal Impact is conditional, not mandatory for every individual-goal Strategy Decision.
- `docs/Implementation/05-STRATEGY_DECISION_IMPLEMENTATION.md:5` agrees it is conditional.
- `docs/Implementation/17-NEW_GOAL_AGAINST_EXISTING_PLAN_IMPLEMENTATION.md:3-5` requires Whole-Plan impact for a new goal against an existing plan.
- `docs/Implementation/19-MULTI_GOAL_WHOLE_PLAN_IMPLEMENTATION.md:3-5` defines the conditional plan-level flow.
- `docs/architecture/multi-goal-planning.md:3-20` describes Multi-Goal Planning as a canonical cross-goal layer that consumes per-goal Strategy Versions.

**Why this is a discrepancy:** The conceptual distinction is mostly aligned, but “Multi-Goal Planning” is used both for a live consolidated plan and for conditional Whole-Plan Impact/revalidation. Those are not necessarily the same operation.

**Required resolution:** Name the two operations separately:
1. **Consolidated Multi-Goal Plan** — builds the current view across goals.
2. **Whole-Plan Impact Analysis** — conditionally compares a proposed change against existing goals/accepted plan.
Then reference the appropriate operation in each flow.

### D-10 — Reporting architecture is described as target state and current capability without a clear boundary
**Severity:** Medium  
**Conflict:** Is Variant already a first-class report input, or is variant-driven rendering still proposed?

- `docs/architecture/variant-report-architecture.md:1-20` defines a variant-based reporting architecture and calls Variant a direct input for the Goal Report.
- The same document `:335-378` says PDF paths are not fully consolidated, ReportConfig is not yet first-class, and Variant is not yet fully wired into report configuration/rendering.
- `docs/architecture/strategy-variants.md:29` says reports should expose the Variant; `:370-372` says Variant is not yet a first-class PDF selection input.
- `docs/Decision tree/09-FINAL_DECISION_AND_RECOMMENDATION_CURRENT_STATE_AND_RECOMMENDATION.md:121-123` says variant selection currently happens inside recommendation and should become an explicit stage.

**Why this is a discrepancy:** The report design is expressed as an established architecture while the same source describes key wiring as incomplete.

**Required resolution:** Mark report tables/flows as **target architecture** and add a per-surface status table (Goal Report, Basket, Complete Plan, Summary Report) showing whether Variant is read, persisted, used to select sections, and rendered.

### D-11 — Calculation architecture metadata does not match the inspected repository snapshot
**Severity:** Medium  
**Conflict:** The calculation architecture document claims a different branch than the branch inspected for this audit.

- `docs/architecture/CANONICAL-CALCULATION-SYSTEM.md:3` says **Branch: backend-audit-cleanup**.
- `docs/audit/SYSTEM_CLEANUP_REGISTER.md:3-5` identifies its own snapshot SHA as `62a1c6a3bb94dd090d358bfd9e707ba1a6dacdb4`.
- This audit inspected `main`, tree snapshot `bfd8271914f71ba1c21eaef09cdc0d14d38500b0`.

**Why this is a discrepancy:** Readers cannot tell whether these docs describe the same code revision. The branch label alone does not prove the content is wrong, but the provenance is not aligned.

**Required resolution:** Add “last verified commit” to each audit/architecture document. Re-verify the document against that commit or label it as historical/stale. Do not treat branch names as durable version identifiers.

### D-12 — The Strategy Matrix presents design values as if they were frozen policy
**Severity:** Medium  
**Conflict:** The matrix provides numeric baseline profiles and a selection contract, while the Decision Tree says scores/weights and some precedence rules are not frozen.

- `docs/architecture/strategy-matrix.md:5-9` assigns numeric Safety/Liquidity/Growth/Flexibility profiles to strategies.
- The same document `:15-19` states the common 8-fit, Pass/Conditional/Fail and ranking behavior in declarative language.
- `docs/Decision tree/00-DECISION_ENGINE_DESIGN_SUMMARY.md:243-250` says score weights/precedence and alternative strategy policy are not yet frozen.
- `docs/Decision tree/04-STRATEGY_SELECTION_CURRENT_STATE_AND_RECOMMENDATION.md` distinguishes current selection logic from rules to be frozen.
- `docs/Decision tree/00.6-RULE_OWNERSHIP_KEEP_MERGE_REPLACE_REMOVE_NEW_AUDIT.md:21` says its canonical flow is target state, not proof of current runtime.

**Why this is a discrepancy:** Numeric profiles and matrix decision language look normative, but no status or source is given to show whether these are illustrative heuristics, approved business policy, or current executable constants.

**Required resolution:** Mark every score/profile as **illustrative**, **current-code value**, or **approved/frozen policy**; add its source/owner and effective version. Do not present illustrative values in the same table style as frozen rules without a status label.

---

## Recommended correction order

1. **Freeze terminology:** Goal Funding vs funding implementation path; Variant vs Technique vs Solution; Architecture vs Report Architecture.
2. **Freeze one target pipeline:** applicability → constraints/eligibility → strategy selection → variant → technique/method → composition/solution → stress/revalidation → final decision/recommendation.
3. **Separate current runtime from target design** in every Decision Tree and architecture flow.
4. **Define stress re-selection and investor adoption** as an explicit state machine.
5. **Split Multi-Goal Plan from Whole-Plan Impact Analysis.**
6. **Add standard document metadata:** authority type, decision status, implementation status, last verified commit.
7. **Reconcile reporting and calculation documents** against the current code snapshot.

## Reference index

All references above are repository-relative paths with 1-based line numbers. Line numbers are for the inspected `main` snapshot and can shift after edits. This audit records documentation discrepancies; it does not itself approve business rules, declare runtime implementation complete, or authorize code changes.
