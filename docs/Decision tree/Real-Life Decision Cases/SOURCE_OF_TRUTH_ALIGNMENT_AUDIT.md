# Canonical Source of Truth — Cross-Repository Alignment Audit

**Business baseline:** `docs/Decision tree/Real-Life Decision Cases/00-CANONICAL_SOURCE_OF_TRUTH.md`  
**Audit date:** 2026-10-12  
**Repository:** `Bhardwaj1-star/planvesto`  
**Scope:** Compare the business baseline against other Decision Tree/architecture/implementation documentation and active code paths.  
**Status:** Static code/document audit; no code migration or runtime test suite claimed by this document.

---

## 1. Executive result

The canonical source of truth has been consolidated from the Real-Life Decision Cases folder. The repository is **not fully aligned** with it.

The most consequential mismatches are:
1. Goal Funding is still a peer Strategy Builder strategy in the active canonical registry and strategy pipeline.
2. Strategy scoring still refers to legacy strategy IDs that do not match the canonical strategy IDs.
3. The strategy engine's processing order needs restructuring/verification against the required decision order.
4. Variant selection and final recommendation stages are not cleanly separated as an authoritative pipeline.
5. The strategy solution matrix does not consistently enforce the Strategy → Variant → Technique → Method/Policy → Solution hierarchy.
6. Multi-goal orchestration allocates shared surplus, but its output/action-plan ownership is not yet the complete accepted-plan → Action Plan contract.
7. What-if, adoption, materiality and targeted revalidation are not yet one complete lifecycle.
8. Existing documentation outside the Real-Life Decision Cases folder still asserts conflicting current/canonical models.

**Important:** This is an alignment audit, not permission to delete code. Migration of IDs, registries, saved versions, API contracts and historical data requires an explicit implementation plan.

## 2. Alignment matrix

| ID | Source-of-truth requirement | Evidence in other docs / active code | Status | Required resolution |
|---|---|---|---|---|
| ALIGN-01 | Goal Funding is Goal Planner / Feasibility, not a fifth peer Strategy Builder strategy. | `backend/library/strategies/canonical.py` registers `strat-goal-funding`; `backend/library/strategies/variants.py`, `scenario.py`, `decision.py`, `variant_selector.py` and `solution_matrix.py` contain dedicated Goal Funding paths. Some older Decision Tree and architecture docs still describe five strategies. | **CONTRADICTORY — P0** | Separate feasibility/funding-path responsibility from Strategy Builder. Define migration for registry, variants, scenario generation, scoring, API, persistence, saved versions and tests before removing the peer strategy. |
| ALIGN-02 | Strategy Builder peer set is four strategies: Progressive De-risking, Capital Preservation, Debt Reduction, Credit Utilisation. | Canonical registry currently contains these four plus Goal Funding. Legacy docs include `docs/Decision tree/04-STRATEGY_SELECTION_CURRENT_STATE_AND_RECOMMENDATION.md`, `docs/architecture/strategy-matrix.md` and `docs/architecture/strategy-architecture-composition.md` with five-strategy language. | **CONTRADICTORY — P0** | Update code-oriented docs only after migration design is agreed; label the four-strategy set as business authority now. |
| ALIGN-03 | Strategy scoring must use current canonical IDs and meaningful decision criteria. | `backend/rules/strategy_decision.py` references stale IDs: `strat-dynamic-accumulation`, `strat-calibrated-growth`, `strat-high-liquidity-flex`, `strat-cap-preservation`. | **CONTRADICTORY / LIKELY INEFFECTIVE SCORING — P0** | Map scoring policy to approved canonical strategy IDs and add tests that prove every active strategy receives intended horizon/fit behavior. Do not do a blind string replacement; define semantic mapping first. |
| ALIGN-04 | Applicability, viability and strategy selection are separate decisions; failed candidates cannot be recommended. | Strategy pipeline includes applicability, eligibility/fit evaluation, architecture composition and decision scoring; tests in `backend/tests/test_strategy_decision_authority.py` assert decision authority constraints. | **PARTIALLY ALIGNED** | Preserve decision authority tests while ensuring each stage is explicit and no score/diagnostic bypasses hard viability failures. |
| ALIGN-05 | Decision order is context/feasibility/constraints → applicability → viability → selection → variant → techniques → method/policy → solution → stress → recommendation. | `backend/engines/strategy/engine.py` currently composes architectures and executes candidate techniques before final decision evaluation; `backend/engines/strategy/recommendation.py` performs variant selection after the decision. | **ORDER MISMATCH / NEEDS REFACTOR — P0** | Define candidate-evidence vs selected-path execution explicitly. Make selected variant/technique/solution stages auditable; do not execute a selected implementation before the authoritative selection. |
| ALIGN-06 | Variant is a subtype/form of strategy, not a technique or solution. | `backend/library/strategies/variants.py` has strategy variants. `backend/library/strategies/solution_matrix.py` generates Goal Funding solutions from variants but builds other strategies' solutions from technique IDs. | **PARTIALLY ALIGNED / TAXONOMY MISMATCH — P1** | Normalize the solution schema and enforce explicit strategy_id + variant_id + technique policy + method/policy + solution relationships. Preserve valid differences in execution without using mixed entity types. |
| ALIGN-07 | Techniques and solutions are distinct; technique policy has Required/Conditional/Optional/Not Applicable/Insufficient Inputs. | `backend/engines/technique/engine.py` can return `insufficient_inputs` and `not_implemented`; existing tests cover some techniques, but the registry/matrix/tests do not comprehensively enforce the entire canonical variant-to-technique policy. | **PARTIALLY ALIGNED** | Add complete mapping/coverage tests and ensure `not_implemented` is surfaced as implementation gap, not confused with policy `Not Applicable`. |
| ALIGN-08 | Asset Mapping is upstream planning evidence; Asset Earmarking is downstream strategic reservation/protection. | Case 15 defines the boundary. Canonical strategy code currently includes `tech-asset-earmarking` within Goal Funding's technique set, so ownership must be checked during Goal Funding separation. | **BUSINESS DEFINITION ESTABLISHED; CODE OWNERSHIP UNVERIFIED** | Keep mapping out of Strategy Builder techniques. Re-home earmarking only through selected strategy/variant/technique paths, with explicit persistence/release/conflict semantics. |
| ALIGN-09 | Goal feasibility belongs to Goal Planner; Strategy Builder consumes the result instead of recalculating it. | The repository has Goal Planner/goal funding logic and Strategy Builder scenario logic; Goal Funding-specific scenario code still generates funding variants from the strategy path. | **OVERLAPPING RESPONSIBILITIES — P0** | Define a stable feasibility output contract and make Strategy Builder consume it. Test that Strategy Builder does not independently re-solve goal feasibility. |
| ALIGN-10 | Individual-goal decision is separate from conditional Whole-Plan/Multi-Goal Impact. | `backend/engines/orchestration/engine.py` evaluates goals via strategy evaluator, resolves priority, allocates shared surplus, returns GoalResolution; comments indicate executable ActionPlan records belong to ActionPlanService and orchestrator outputs `actions=[]`. | **PARTIALLY ALIGNED** | Preserve individual-goal decision boundary; add a separate plan-level impact/feasibility contract and make downstream Action Plan generation explicit. |
| ALIGN-11 | Action Plan is downstream of investor adoption and represents concrete accepted actions. | `backend/rules/action_plan.py` builds generic strategy/technique action specs; multi-goal orchestrator does not itself provide the complete execution plan. | **INCOMPLETE — P1** | Define action generation from accepted implementation/plan, with dependencies, status, sequencing and completed-action history. Ensure a recommendation or rejected what-if does not create active actions. |
| ALIGN-12 | A better path/new goal/strategy change is a proposal; reject preserves existing Accepted Plan. | Strategy service persists StrategyRun, previews implementation without persistence and finalizes StrategyVersion only when finalized. This supports part of the distinction, but is not proof of the complete plan-adoption lifecycle. | **PARTIALLY ALIGNED** | Audit persistence/state transitions for Accept/Reject/Modify, proposed vs accepted plan, and action-plan updates. Add tests for rejected proposals leaving active state unchanged. |
| ALIGN-13 | What-if scenarios remain separate; execution changes trigger impact analysis and targeted revalidation, not automatic replacement. | Scenario/what-if support exists, but Case 13 and Case 14 identify lifecycle/adaptation gaps; complete materiality → impact → targeted revalidation → investor decision flow is not established end-to-end. | **INCOMPLETE — P1** | Implement a single controlled change pipeline and tests for unchanged strategy, re-evaluation needed, reject, and accept. |
| ALIGN-14 | Materiality assessment prevents unnecessary full replanning. | Cases 5/6/10/11 establish this; exact thresholds are open. Implementation docs describe missing/incomplete workflow. | **OPEN POLICY + IMPLEMENTATION GAP** | Do not invent thresholds. First approve policy inputs and dependency scope; then implement configurable materiality and targeted revalidation. |
| ALIGN-15 | Investor priority influences recommendations but does not silently override the investor; hard constraints differ from advisory signals. | Case 3/8/12 and Case 14 establish this. Case 13 reports investor-priority authority is not fully explicit; Money Wheel/ratio logic contains decision-like threshold behavior. | **PARTIALLY ALIGNED / POLICY GAP — P1** | Separate diagnostics, advisory priority and hard constraint policy. Define authority, tie-breaks and investor override behavior. |
| ALIGN-16 | No Acceptable Path is valid; custom strategy remains identifiable and validated. | Strategy decision docs include rejection logic, but Case 13 reports investor rejection/open strategy mode is not complete as a product capability. | **PARTIALLY ALIGNED / INCOMPLETE — P1** | Standardize a typed no-acceptable-path output and define custom strategy schema, provenance, validation and adoption lifecycle. |
| ALIGN-17 | Stress/resilience reuses the decision logic and cannot silently replace accepted state. | Stress/scenario mechanisms exist, but Case 13/14 state that complete stress taxonomy and re-selection/revalidation policy are not frozen. | **OPEN POLICY + PARTIAL IMPLEMENTATION** | Approve stress scenarios, thresholds, failure outputs and the re-evaluation contract before freezing behavior. |
| ALIGN-18 | Other folders are implementation/current-state evidence, not competing business authorities. | `docs/audit/DOCUMENT_DISCREPANCY_AUDIT.md`, `docs/audit/CANONICAL_MASTER_REGISTER.md`, `docs/Decision tree/00.6-RULE_OWNERSHIP_KEEP_MERGE_REPLACE_REMOVE_NEW_AUDIT.md` and `docs/Decision tree/04-STRATEGY_SELECTION_CURRENT_STATE_AND_RECOMMENDATION.md` contain useful discrepancy findings, but some documents repeat legacy five-strategy language. | **DOCUMENTATION CONFLICT — P1** | Update or label conflicting docs as historical/current-state after the canonical baseline is approved; do not edit them to imply code already conforms. |

## 3. Verified code-path references

- `backend/library/strategies/canonical.py` — canonical strategy registry currently includes `strat-goal-funding` and the four intended peer strategies.
- `backend/library/strategies/variants.py` — includes Goal Funding funding-mechanism variants alongside variants for the four strategies.
- `backend/engines/strategy/scenario.py` — has Goal Funding-specific scenario generation.
- `backend/engines/strategy/decision.py` — has Goal Funding-specific candidate scenario selection/evaluation.
- `backend/engines/strategy/variant_selector.py` — has Goal Funding-specific variant selection.
- `backend/rules/strategy_decision.py` — references legacy strategy IDs.
- `backend/engines/strategy/engine.py` — current orchestration order requires alignment against the canonical stages.
- `backend/library/strategies/solution_matrix.py` — strategy solutions are not generated from one uniformly enforced hierarchy.
- `backend/engines/orchestration/engine.py` — multi-goal evaluation/allocation exists, but Action Plan remains downstream.
- `backend/rules/action_plan.py` — action specs are generic and narrower than the end-to-end Action Plan requirement.
- `backend/services/strategy_service.py` — run/preview/finalization distinction exists; complete Accepted Plan adoption must be checked separately.
- `backend/engines/technique/engine.py` — dispatch and input/implementation statuses exist; taxonomy/policy coverage needs completion.

## 4. Documentation outside the source folder that needs reconciliation

Treat these as **current-state evidence or documents to update**, not as authorities over the canonical business baseline:

- `docs/audit/CANONICAL_MASTER_REGISTER.md`
- `docs/audit/DOCUMENT_DISCREPANCY_AUDIT.md`
- `docs/Decision tree/00.6-RULE_OWNERSHIP_KEEP_MERGE_REPLACE_REMOVE_NEW_AUDIT.md`
- `docs/Decision tree/01-STRATEGY_APPLICABILITY_CURRENT_STATE_AND_RECOMMENDATION.md`
- `docs/Decision tree/04-STRATEGY_SELECTION_CURRENT_STATE_AND_RECOMMENDATION.md`
- `docs/Decision tree/09-FINAL_DECISION_AND_RECOMMENDATION_CURRENT_STATE_AND_RECOMMENDATION.md`
- `docs/architecture/strategy-matrix.md`
- `docs/architecture/strategy-architecture-composition.md`
- `docs/Implementation/00-IMPLEMENTATION_SYSTEM_MAP.md`
- `docs/Implementation/03-GOAL_PLANNING_IMPLEMENTATION.md`

Do not rewrite these all at once. First mark the source-of-truth link and whether each document is current-state, target architecture, implementation plan or historical. Then reconcile one subsystem at a time.

## 5. Implementation order

### P0 — Decision authority and ownership
1. Freeze this business baseline's established rules; keep OPEN POLICY items explicitly open.
2. Design Goal Funding separation/migration from Strategy Builder.
3. Replace stale strategy-ID scoring semantics with explicit canonical mapping.
4. Restructure the strategy pipeline to make applicability, viability, selection, variant and implementation stages auditable.
5. Preserve hard rejection and decision-authority tests; add regression tests for the four-strategy peer set.

### P1 — End-to-end planning lifecycle
6. Normalize the variant/technique/method/solution relationship.
7. Define and implement feasibility output consumed by Strategy Builder.
8. Separate individual-goal decisions from conditional whole-plan impact.
9. Complete proposed-vs-accepted plan state transitions and isolated what-if.
10. Implement materiality, impact and targeted revalidation with explicit approved thresholds.
11. Complete accepted-plan-driven Action Plan generation.
12. Define investor-designed strategy and No Acceptable Path output contracts.

### P2 — Policy completion and cleanup
13. Approve stress/resilience policy and thresholds.
14. Resolve Asset Earmarking lifecycle/persistence and conflicts.
15. Reconcile remaining docs, registries, tests and historical references.
16. Only then remove genuinely obsolete code after usage, persistence, API and test references are verified.

## 6. Audit boundaries

- This audit does not claim the full test suite was run.
- Static references establish the described code paths; they do not prove all runtime edge cases.
- No production code has been changed by creating this audit.
- The four-strategy peer set and Goal Funding ownership are business requirements; the exact migration strategy remains engineering work.
- An item marked OPEN POLICY must not be converted into a guessed threshold or rule by implementation.
