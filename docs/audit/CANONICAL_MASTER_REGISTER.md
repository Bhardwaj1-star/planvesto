# Canonical Master Register — Planvesto Decision System

**Status:** DRAFT — reconciled index; business rules are not frozen  
**Repository:** `Bhardwaj1-star/Planvesto`  
**Audit baseline:** `main`, tree/commit `9abf78a462cec7331fda1a1f43bbf7cfe7e9f090`  
**Scope:** 98 documentation files under `docs/` were inventoried. This register consolidates the major repeated claims and documented conflicts; it does not claim that every product rule has been approved or that every runtime path has been re-tested in this pass.

## 1. How to use this register

Think of the documents as books that sometimes repeat one another. This file records:
- what several documents agree on;
- where documents disagree;
- which source is authoritative for each kind of information;
- what evidence is still needed before a disagreement can be closed.

**Do not treat the most repeated statement as automatically correct.** Repetition is evidence of agreement, not approval. For each conflict, compare the latest explicit business decision, current code behavior, and tests. Keep those three separate.

### Authority rules

1. **Raw financial inputs:** persisted source records are the source data.
2. **Normalized current financial position:** Financial State service/engine and its current snapshot.
3. **Shared financial formulas:** `backend/engines/calculation/canonical.py`.
4. **Diagnostic classification:** MoneyWheel rules/engine.
5. **Constraint policy and enforcement:** `backend/engines/constraints/`, verified against actual evaluator/aggregator call paths.
6. **Canonical strategy/variant/technique definitions:** their library registries, subject to an explicit product decision on the disputed Goal Funding boundary.
7. **Observed runtime behavior:** active code path plus callers and tests; a registry entry alone does not prove reachability.
8. **Approved business policy:** only a rule explicitly accepted for V1 after resolving conflicts. A document labelled CANONICAL or FINAL is not sufficient if it conflicts with a later explicit business decision or says it is not implemented/frozen.
9. **This register:** conflict index and routing page. It does not override approved rules or replace detailed evidence documents.

## 2. Agreed system principles found repeatedly

These principles recur across the Decision Tree, real-life cases, architecture, user journeys and implementation plans. Keep them aligned unless a deliberate product decision changes them.

| Principle | Consolidated meaning | Primary references |
|---|---|---|
| Financial State is evidence | It represents normalized current financial facts; it does not select strategies. | `docs/architecture/financial-state.md`; `docs/User Journeys/03-FINANCIAL_STATE_JOURNEY.md` |
| One formula owner | Shared metrics are calculated once and reused; downstream services must not create competing formulas. | `docs/architecture/CANONICAL-CALCULATION-SYSTEM.md`; `docs/architecture/code-architecture-consistency-audit.md` |
| Measure ≠ decision | A ratio/diagnostic is evidence. Constraint policy and decision logic determine its consequence. | `docs/architecture/onboarding-to-moneywheel.md`; `docs/product/MONEYWHEEL-CHANGE-REGISTER.md` |
| Applicability ≠ viability/eligibility ≠ selection | A candidate can still fail feasibility; only eligible candidates should enter the selection pool under the approved policy. | `docs/Decision tree/01-STRATEGY_APPLICABILITY_CURRENT_STATE_AND_RECOMMENDATION.md`; Steps 02–04 |
| Strategy ≠ Variant ≠ Technique | Strategy owns the problem/responsibility; Variant is an implementation form; Technique is a reusable method. | `docs/Decision tree/05-22-VARIANT_SELECTION_CURRENT_STATE_AND_RECOMMENDATION.md`; `docs/Decision tree/06-TECHNIQUE_SELECTION_CURRENT_STATE_AND_RECOMMENDATION.md` |
| Recommendation ≠ adoption | The investor accepts, rejects or modifies; a rejected proposal must not overwrite the accepted plan. | `docs/User Journeys/09-DECISION_RECOMMENDATION_JOURNEY.md`; `docs/User Journeys/10-INVESTOR_ADOPTION_JOURNEY.md` |
| Accepted Plan is protected state | Scenarios and proposals do not silently mutate the investor-approved plan. | `docs/User Journeys/11-ACCEPTED_PLAN_JOURNEY.md`; `docs/Implementation/11-ACCEPTED_PLAN_IMPLEMENTATION.md` |
| Whole-Plan Impact is conditional | Use it for material multi-goal/resource competition, not as a mandatory stage for every individual-goal decision. | `docs/Decision tree/Real-Life Decision Cases/14-REAL_LIFE_CASES_CANONICAL_SYSTEM_STRUCTURE_AND_ALIGNMENT.md`; `docs/Implementation/19-MULTI_GOAL_WHOLE_PLAN_IMPLEMENTATION.md` |
| No acceptable path is valid | Never force a strategy just to produce a recommendation. | `docs/Decision tree/Real-Life Decision Cases/strategy-decision-tree.md`; `docs/User Journeys/20-NO_ACCEPTABLE_PATH_JOURNEY.md` |
| Changes require targeted revalidation | Recalculate affected decisions and preserve unrelated accepted plan state. | User Journeys 14–19; Implementation 14–19 |

## 3. Canonical domain register

| Domain | Current source of definition / execution | Register status | Rule |
|---|---|---|---|
| Document inventory / cleanup | `docs/audit/SYSTEM_CLEANUP_REGISTER.md` | INVENTORY ONLY | It is code triage, not product-rule authority. Reconcile its recorded SHA with the current branch before cleanup. |
| Cross-cutting Decision Tree audit | `docs/Decision tree/00.5-CROSS_CUTTING_REVERIFICATION_AND_GAP_AUDIT.md` | AUDIT / NOT FROZEN | Use it to locate unresolved runtime drift; do not treat target flow as current runtime. |
| Rule ownership | `docs/Decision tree/00.6-RULE_OWNERSHIP_KEEP_MERGE_REPLACE_REMOVE_NEW_AUDIT.md` | PROPOSED OWNERSHIP | KEEP/MERGE/REPLACE/REMOVE requires caller, test, migration and compatibility verification. |
| Goal taxonomy | `backend/rules/goals.py` | CODE CANDIDATE | Verify the complete canonical goal vocabulary and all consumers. |
| Goal feasibility | Goal Planner / Goal Feasibility services and goal engines | BUSINESS BOUNDARY AGREEMENT; exact algorithm not frozen | Owns goal funding feasibility and funding paths; does not choose the Strategy Builder strategy. |
| Strategy identities | `backend/library/strategies/canonical.py` | CODE REGISTRY; BUSINESS CONFLICT | Current code/audits list five IDs including Goal Funding; real-life cases specify four peer Strategy Builder strategies. Resolve REG-001 before calling the final set canonical. |
| Applicability | `backend/engines/strategy/applicability.py` + `StrategyRuleEngine` | RUNTIME EXISTS; POLICY NOT FROZEN | Current characteristics use effectively ANY/OR semantics; horizon signal gap exists between 5 and 7 years. |
| Hard constraints | `backend/engines/constraints/policy.py`, evaluator, adapters, aggregator | RUNTIME EXISTS; ENFORCEMENT MUST BE TRACED | A declared/registered rule is not proof that the evaluator invokes it. |
| Eight eligibility fits | `backend/rules/eligibility.py` + `backend/engines/strategy/eligibility.py` | SPLIT OWNERSHIP / DOUBLE CHECK | Fit vocabulary and execution are separate; current decision path also runs a separate eligibility gate. |
| Strategy selection | `backend/engines/strategy/decision.py::evaluate_decision()` and `backend/rules/strategy_decision.py` | CONFLICT | Stale strategy IDs remain in scoring logic; score weights, priorities and architecture timing are not frozen. |
| Variant definitions | `backend/library/strategies/variants.py` | CODE REGISTRY | Audit identifies 22 definitions; definition does not prove selector reachability. |
| Variant selection | `backend/engines/strategy/variant_selector.py`, invoked by recommendation | RUNTIME EXISTS; OWNERSHIP/ORDER CONFLICT | Goal Funding has six defined variants, but fallback selector directly selects only three unless a baseline scenario supplies another ID. |
| Technique definitions | `backend/library/strategies/techniques_canonical.py` | CODE REGISTRY | Audit identifies 10 registered techniques. |
| Strategy-to-technique mapping | `backend/library/strategies/canonical.py` | PARTIAL | Eight techniques are mapped; Barbell and Tax-Loss Harvesting are registered/executable but not attached to a canonical strategy. |
| Technique selection | No complete dedicated canonical policy identified | NOT IMPLEMENTED AS A FULL POLICY LAYER | Mapping, applicability, combinations and variant-level technique selection remain unresolved. |
| Architecture composition | `backend/engines/strategy/composition.py` | RUNTIME EXISTS; ORDER CONFLICT | Runtime composes candidate architectures and executes techniques before final strategy decision; target downstream composition is only proposed. |
| Components | `backend/library/strategies/components.py` + composition engine | DEFINITIONS EXIST; ACTIVATION POLICY PARTLY IN ENGINE | Define which activation rules are business policy and verify them against cases. |
| Solution mapping | `backend/library/strategies/solution_matrix.py` | SEMANTIC CONFLICT | Goal Funding variants are called solutions while other strategy techniques are called solutions; real-life cases insist Technique ≠ Solution. |
| Stress / resilience | `backend/engines/strategy/scenario.py` | PARTIAL IMPLEMENTATION | What-if/scenario sensitivity exists; a complete canonical stress/resilience gate and re-selection policy are not established. |
| Final decision/recommendation | `DecisionResult`, decision engine and `recommendation.py` | RUNTIME AUTHORITY EXISTS; CONTRACT NOT FROZEN | Recommendation should explain the decision, not secretly make another one; variant selection is currently inside recommendation flow. |
| Rule metadata | `backend/rules/canonical.py` | INCOMPLETE | Audit says metadata registry does not contain every important executable business rule. |
| Shared calculations | `backend/engines/calculation/canonical.py` | CANDIDATE FORMULA AUTHORITY; DOWNSTREAM CONFLICTS FOUND | Fix local DTI and emergency coverage formulas in FinancialPlanService and align thresholds. |
| MoneyWheel | `backend/rules/moneywheel.py` + MoneyWheel engine | DIAGNOSTIC AUTHORITY; POLICY BOUNDARY DRIFT | A critical ratio is not by itself a strategy rejection. Constraints own the consequence. |
| Reports | GoalReportService, FinancialPlanService, BasketReportService, SummaryReport | MULTIPLE IMPLEMENTED PATHS; COMMON RENDERER IS TARGET | Variant-driven report configuration is not fully wired; do not delete report paths without consumer/contract review. |
| Investment/product selection | `backend/engines/investment/`, risk profiler, product-selection docs | FOUNDATION / NOT FULLY IMPLEMENTED | Do not invent allocation, product selection, or rebalancing rules from architecture diagrams. |
| Strategy Version / Accepted Plan | StrategyVersion + approval/primary state; accepted-plan docs | SEPARATE LIFECYCLE CONCEPTS | Preserve proposed, rejected, approved, selected and accepted states as distinct contracts; verify actual implementation for each. |
| Action Plan / Execution | Action plan rules, service, repositories and impact flow | IMPLEMENTED IN PART; lifecycle design broader | Actions materialize an approved version; actual execution and material changes feed targeted revalidation. |

## 4. Blocking cross-document conflicts

These are the highest-value conflicts to resolve before implementation or deletion. “Evidence needed” is the condition for closing the item; no item below is silently decided by this register.

### REG-001 — Is Goal Funding a Strategy Builder strategy?

**Conflict**
- Current code-oriented documents and `strategy-matrix.md` describe five strategies including `strat-goal-funding`.
- `docs/Decision tree/Real-Life Decision Cases/00-GOAL_FUNDING_CONCEPT_CHANGE_LOG.md`, `13-DECISION_TREE_SYSTEM_UPDATE_AND_FEATURE_IMPLEMENTATION_PLAN.md`, `14-REAL_LIFE_CASES_CANONICAL_SYSTEM_STRUCTURE_AND_ALIGNMENT.md`, and `strategy-decision-tree.md` state that Goal Funding belongs to Goal Planner / Goal Feasibility and the Strategy Builder has four peer strategies: Progressive De-risking, Capital Preservation, Debt Reduction and Credit Utilisation.
- The concept/change documents also state that this business direction is not yet fully implemented/frozen in code.

**Register decision:** CONFLICT — product approval required. The explicit real-life business direction is the stronger target candidate, but code must not be relabelled or removed until the V1 rule is formally approved and migration is planned.

**Close when:** approve the Strategy Builder set; define what happens to `strat-goal-funding`, its six variants, scenario generation, scoring, persisted StrategyVersions, APIs and old tests.

### REG-002 — Variant vs Technique vs Solution

**Conflict**
- The Goal Funding row in `docs/architecture/strategy-matrix.md` places Existing Assets, SIP, Lumpsum and step-up SIP under Variants and also Solutions.
- `docs/architecture/strategy-architecture-composition.md` calls Goal Funding variants solutions and calls other strategies' techniques solutions.
- `docs/architecture/strategy-variants.md` says SIP/Lumpsum/Step-up SIP are not architectural variants.
- Real-life case documents define the hierarchy Strategy → Variant → Technique → Method/Policy → Solution → Action and explicitly say Technique ≠ Solution; they also place Contribution Escalation in Goal Planner / Goal Funding, not the core Strategy Decision Tree.

**Register decision:** CONFLICT — taxonomy is not consistent. Use the real-life hierarchy as the target candidate, but confirm how existing registry entries are migrated.

**Close when:** each existing ID has exactly one entity type, one parent/owner, and explicit mappings. Do not treat a repeated table entry as proof of correct type.

### REG-003 — Current runtime order vs target decision order

**Conflict**
- The Decision Tree summary/step documents propose Strategy → Variant → Technique → Architecture → Stress/Resilience → Final Decision.
- Current-state audits state that architecture composition and technique execution occur before `evaluate_decision()`; variant selection currently occurs inside recommendation.
- Some architecture documents show different sequences, and report architecture assumes variant is a first-class report input even though wiring is incomplete.

**Register decision:** CURRENT runtime and target flow must be labelled separately. Target order is not proof of runtime behavior.

**Close when:** trace the active call graph and tests, approve the target sequence, then migrate with regression tests.

### REG-004 — Eligibility is checked twice

**Conflict**
- Eight-fit docs present a canonical 8-fit gate.
- Verification correction in `03-8_ELIGIBILITY_FITS_CURRENT_STATE_AND_RECOMMENDATION.md` confirms `evaluate_eligibility_fits()` and a separate `evaluate_eligibility()` goal/constraint gate are both called and combined.

**Register decision:** two checks have overlapping decision authority until their responsibilities are defined.

**Close when:** assign each check a distinct purpose or consolidate them; test PASS, CONDITIONAL, FAIL and missing-evidence boundaries.

### REG-005 — Financial formulas and threshold boundaries disagree

**Confirmed code-audit findings**
- FinancialPlanService computes a DTI-like metric from total liabilities / annual income, while canonical DTI is monthly debt payments / gross monthly income.
- FinancialPlanService uses `financial_assets * 0.2 / monthly_exp` for emergency coverage, while canonical emergency coverage is liquid assets / essential monthly expenses.
- DTI boundary handling differs: MoneyWheel/constraints treat 40% as critical (`>= 40%)); Summary Report checks `> 40`; ConstraintEvaluator wording also says `> 40`.

**Register decision:** P0 calculation conflict and P1 boundary conflict. The canonical calculation/policy files are the intended owners, but every consumer must be verified.

**Close when:** downstream consumers use the shared calculation/threshold; add same-input cross-consumer tests and exact 40% boundary tests.

### REG-006 — MoneyWheel measurement vs decision

**Conflict**
- Product change register says MoneyWheel should measure/classify and not independently decide repayment/investment.
- Existing constraint behavior can use ratio evidence to suggest priority overrides; audits note that generic ratio thresholds and downstream planning effects need reconciliation.

**Register decision:** preserve the distinction between metric, diagnostic classification and policy consequence. Do not simply delete all thresholds; ensure the correct constraint/policy owner interprets them.

**Close when:** test that a MoneyWheel status alone cannot select a strategy or trigger an unapproved action; trace each downstream override to its owning rule.

### REG-007 — Rule registry is metadata, not complete executable policy

**Conflict**
- `backend/rules/canonical.py` describes itself as canonical metadata authority.
- Decision Tree audit explicitly says it does not yet contain every important runtime business rule; important scoring, eligibility, variant and composition policy remains elsewhere.

**Register decision:** do not call the registry the complete business-rule source of truth yet.

**Close when:** every active rule has stable ID, owner, inputs, outputs, version, implementation path, tests and status; all unregistered executable policy is either migrated or explicitly classified.

### REG-008 — Feasibility and decision status vocabulary differs

**Conflict**
- Goal feasibility uses Feasible / Constrained / Infeasible / Unknown.
- Strategy eligibility uses PASS / CONDITIONAL / FAIL, with missing evidence generally becoming CONDITIONAL.
- Strategy decision and multi-goal layers also translate feasible/constrained/pass/conditional.
- The code audit confirms cross-layer status translation.

**Register decision:** preserve domain-specific meanings until a mapping contract is approved; do not equate statuses based only on similar names.

**Close when:** document canonical semantics and explicit adapters, including unavailable/missing evidence, and test every mapping.

### REG-009 — Strategy score and investor priorities are not frozen

**Conflict**
- `backend/rules/strategy_decision.py` contains old strategy IDs that do not match the current five-strategy registry; audits say this is active in scoring.
- `evaluate_decision()` accepts InvestorPriorities but the current selection calculation does not use them; downstream ranking does.
- Architecture/technique readiness can affect the strategy score because these are evaluated before final selection.

**Register decision:** current score is implementation behavior, not approved V1 policy.

**Close when:** approve score dimensions/weights, priority influence, technique-readiness influence, tie-breaking, alternatives and architecture timing; replace stale IDs and add tests.

### REG-010 — Variant registry does not prove selector coverage

**Conflict**
- 22 canonical variants are defined.
- Goal Funding fallback selector directly chooses Existing Assets, Lumpsum and Step-up SIP; SIP and two hybrid variants require a baseline scenario to supply the ID.
- Variant selection is not an independent canonical policy stage.

**Register decision:** registry completeness and selection reachability are separate measures.

**Close when:** create a reachability table for every variant, with conditions, precedence, required inputs, missing-data behavior and tests.

### REG-011 — Technique registry and strategy mapping are different

**Conflict**
- Ten techniques are registered and executable.
- Barbell and Tax-Loss Harvesting have no canonical strategy mapping.
- Real-life Strategy Decision Tree describes a different technique set including debt-specific methods and moves Contribution Escalation/tax methods outside the core four-strategy tree.

**Register decision:** do not attach, rename or delete techniques based on their existence alone.

**Close when:** approve the canonical technique inventory and entity type; map each technique to strategy/variant or explicitly mark catalog-only/future/out-of-scope.

### REG-012 — Audit snapshots and document authority metadata are inconsistent

**Conflict**
- Cleanup and calculation audit documents record different commit SHAs/branch contexts.
- Some documents are marked CANONICAL/FINAL while describing target behavior, incomplete wiring or rules not frozen.

**Register decision:** branch names and document labels alone do not establish authority.

**Close when:** every audit/design file states document type, authority class (runtime evidence / approved policy / target proposal), implementation status, last verified commit SHA and date.

### REG-013 — Multi-Goal Planning vs Whole-Plan Impact

**Conflict**
- Some documents use “Multi-Goal Planning” for both a current consolidated plan and a conditional impact/revalidation operation.
- The discrepancy audit recommends separating the live consolidated multi-goal plan from Whole-Plan Impact Analysis for a proposed change.

**Register decision:** distinguish the persistent/current multi-goal planning operation from conditional change-impact analysis.

**Close when:** name the operations separately and align the relevant user journeys, implementation docs and service contracts.

### REG-014 — Reporting target vs current implementation

**Conflict**
- Variant report architecture describes Variant as a first-class input and a common renderer target.
- The same architecture and current report docs state PDF paths remain distributed, ReportConfig is not first-class, and Variant is not fully wired end-to-end.

**Register decision:** treat common renderer + report config as target architecture; retain current report paths until their contracts/consumers are migrated.

**Close when:** inventory each report surface and verify Variant read/persist/config/render behavior; migrate incrementally with regression tests.

### REG-015 — Canonical strategy profiles look frozen but are not

**Conflict**
- `docs/architecture/strategy-matrix.md` includes numeric Safety/Liquidity/Growth/Flexibility profiles.
- Decision Tree documents say score weights, precedence and selection policy are not frozen.

**Register decision:** matrix numbers are not V1 business policy until explicitly classified.

**Close when:** label every profile as illustrative, current-code value or approved/frozen policy; provide owner and effective version.

## 5. Decision flow — separate target from observed runtime

### Product-level lifecycle (target design)

Onboarding / Financial Inputs  
→ Financial State  
→ Goal Planning / Feasibility  
→ [Whole-Plan Impact only when multi-goal/shared-resource impact is material]  
→ Strategy Decision  
→ Implementation Design  
→ What-if / Stress / Resilience  
→ Decision / Recommendation  
→ Investor Accept / Reject / Modify  
→ Accepted Plan  
→ Action Plan  
→ Execution  
→ Material change → Impact Analysis → Targeted Revalidation

### Individual-goal Strategy Decision (target candidate, pending REG-001)

Goal + Financial State + Goal Feasibility Evidence + Constraints  
→ Applicability  
→ Viability / 8-Fit Eligibility  
→ Strategy Selection  
→ Variant  
→ Technique Selection  
→ Method / Policy  
→ Architecture / Solution  
→ Stress / Resilience / re-selection if required  
→ Final Decision / Recommendation

**Important:** this is the proposed product model, not a claim that the current runtime follows this order. Current runtime has pre-composed candidate architectures, pre-selection technique execution, and variant selection inside recommendation.

## 6. Document authority classes

Use these labels consistently when the documents are next updated:

- **RUNTIME EVIDENCE** — describes verified code behavior at a recorded commit.
- **APPROVED BUSINESS RULE** — explicit V1 product decision, approved and versioned.
- **TARGET DESIGN** — proposed architecture, not necessarily implemented.
- **REAL-LIFE CASE / RATIONALE** — evidence and reasoning used to reach decisions; a case does not automatically freeze a universal rule.
- **USER JOURNEY** — investor/system interactions; not a separate business-rule owner.
- **IMPLEMENTATION PLAN** — engineering steps and acceptance criteria; not proof of implementation.
- **INVENTORY / AUDIT** — findings, provenance, gaps and cleanup triage; not automatic deletion authorization.

Every detailed document should include: `Document Type`, `Authority Class`, `Decision Status`, `Implementation Status`, `Last Verified Commit`, `Last Verified Date`.

## 7. Closure workflow

For each REG item:
1. Keep the current code behavior recorded as observed evidence.
2. Gather the exact document statements, source files, active callers and tests.
3. Decide the business rule explicitly; do not resolve it by majority vote across documents.
4. Add a decision record with owner, rationale, effective version and affected IDs.
5. Add regression/boundary tests.
6. Update canonical implementation and then update dependent documents.
7. Re-run the audit against one commit SHA.
8. Mark VERIFIED only when approved policy, implementation and tests agree.

**Deletion gate:** no code or document is deleted merely because it looks old, duplicates another file, or disagrees with the proposed target. Verify callers/imports/tests/migrations/history and preserve compatibility where required.

## 8. Full documentation inventory reviewed for reconciliation

The following 98 documentation files were present under `docs/` at the audit baseline. They are grouped by their role; the detailed conflict list above records the major cross-document disagreements found in the source audits and decision documents.

### Decision Tree
- `docs/Decision tree/00-DECISION_ENGINE_DESIGN_SUMMARY.md`
- `docs/Decision tree/00.5-CROSS_CUTTING_REVERIFICATION_AND_GAP_AUDIT.md`
- `docs/Decision tree/00.6-RULE_OWNERSHIP_KEEP_MERGE_REPLACE_REMOVE_NEW_AUDIT.md`
- `docs/Decision tree/01-STRATEGY_APPLICABILITY_CURRENT_STATE_AND_RECOMMENDATION.md`
- `docs/Decision tree/02-HARD_CONSTRAINTS_CURRENT_STATE_AND_RECOMMENDATION.md`
- `docs/Decision tree/03-8_ELIGIBILITY_FITS_CURRENT_STATE_AND_RECOMMENDATION.md`
- `docs/Decision tree/04-STRATEGY_SELECTION_CURRENT_STATE_AND_RECOMMENDATION.md`
- `docs/Decision tree/05-22-VARIANT_SELECTION_CURRENT_STATE_AND_RECOMMENDATION.md`
- `docs/Decision tree/06-TECHNIQUE_SELECTION_CURRENT_STATE_AND_RECOMMENDATION.md`
- `docs/Decision tree/07-ARCHITECTURE_COMPOSITION_CURRENT_STATE_AND_RECOMMENDATION.md`
- `docs/Decision tree/08-STRESS_RESILIENCE_CURRENT_STATE_AND_RECOMMENDATION.md`
- `docs/Decision tree/09-FINAL_DECISION_AND_RECOMMENDATION_CURRENT_STATE_AND_RECOMMENDATION.md`

### Real-Life Decision Cases
- `docs/Decision tree/Real-Life Decision Cases/00-GOAL_FUNDING_CONCEPT_CHANGE_LOG.md`
- `docs/Decision tree/Real-Life Decision Cases/03-CASE_3_MULTI_GOAL_FEASIBILITY_AND_ACTION_PLAN.md`
- `docs/Decision tree/Real-Life Decision Cases/04-CASE_4_BETTER_PATH_STRATEGY_AND_IMPLEMENTATION.md`
- `docs/Decision tree/Real-Life Decision Cases/05-CASE_5_PLAN_ADAPTATION_AFTER_FINANCIAL_STATE_CHANGE.md`
- `docs/Decision tree/Real-Life Decision Cases/06-CASE_6_GOAL_INTENT_CHANGE_AND_RECALCULATION.md`
- `docs/Decision tree/Real-Life Decision Cases/07-CASE_7_NEW_GOAL_AGAINST_EXISTING_PLAN.md`
- `docs/Decision tree/Real-Life Decision Cases/08-CASE_8_INVESTOR_STRATEGY_CHANGE_AND_MULTI_STRATEGY_PLAN.md`
- `docs/Decision tree/Real-Life Decision Cases/09-CASE_9_EXECUTION_PLAN_WHAT_IF_AND_IMPACT_GUIDANCE.md`
- `docs/Decision tree/Real-Life Decision Cases/10-CASE_10_EXECUTION_CHANGE_TRIGGERING_STRATEGY_REEVALUATION.md`
- `docs/Decision tree/Real-Life Decision Cases/11-CASE_11_ITERATIVE_STRATEGY_EXECUTION_AND_REVALIDATION.md`
- `docs/Decision tree/Real-Life Decision Cases/12-CASE_12_NO_ACCEPTABLE_PATH_AND_INVESTOR_DESIGNED_STRATEGY.md`
- `docs/Decision tree/Real-Life Decision Cases/13-DECISION_TREE_SYSTEM_UPDATE_AND_FEATURE_IMPLEMENTATION_PLAN.md`
- `docs/Decision tree/Real-Life Decision Cases/14-REAL_LIFE_CASES_CANONICAL_SYSTEM_STRUCTURE_AND_ALIGNMENT.md`
- `docs/Decision tree/Real-Life Decision Cases/15-CANONICAL_ASSET_MAPPING_VS_ASSET_EARMARKING_DECISION_CASE.md`
- `docs/Decision tree/Real-Life Decision Cases/strategy-decision-tree.md`

### Implementation Plans
- `docs/Implementation/00-IMPLEMENTATION_SYSTEM_MAP.md`
- `docs/Implementation/01-ONBOARDING_IMPLEMENTATION.md`
- `docs/Implementation/02-FINANCIAL_STATE_IMPLEMENTATION.md`
- `docs/Implementation/03-GOAL_PLANNING_IMPLEMENTATION.md`
- `docs/Implementation/04-GOAL_FEASIBILITY_IMPLEMENTATION.md`
- `docs/Implementation/05-STRATEGY_DECISION_IMPLEMENTATION.md`
- `docs/Implementation/06-IMPLEMENTATION_DESIGN_IMPLEMENTATION.md`
- `docs/Implementation/07-WHAT_IF_SCENARIO_IMPLEMENTATION.md`
- `docs/Implementation/08-STRESS_RESILIENCE_IMPLEMENTATION.md`
- `docs/Implementation/09-DECISION_RECOMMENDATION_IMPLEMENTATION.md`
- `docs/Implementation/10-INVESTOR_ADOPTION_IMPLEMENTATION.md`
- `docs/Implementation/11-ACCEPTED_PLAN_IMPLEMENTATION.md`
- `docs/Implementation/12-ACTION_PLAN_IMPLEMENTATION.md`
- `docs/Implementation/13-EXECUTION_IMPLEMENTATION.md`
- `docs/Implementation/14-REVALIDATION_IMPLEMENTATION.md`
- `docs/Implementation/15-GOAL_CHANGE_IMPLEMENTATION.md`
- `docs/Implementation/16-FINANCIAL_STATE_CHANGE_IMPLEMENTATION.md`
- `docs/Implementation/17-NEW_GOAL_AGAINST_EXISTING_PLAN_IMPLEMENTATION.md`
- `docs/Implementation/18-STRATEGY_CHANGE_IMPLEMENTATION.md`
- `docs/Implementation/19-MULTI_GOAL_WHOLE_PLAN_IMPLEMENTATION.md`
- `docs/Implementation/20-NO_ACCEPTABLE_PATH_IMPLEMENTATION.md`
- `docs/Implementation/21-INVESTOR_DESIGNED_STRATEGY_IMPLEMENTATION.md`

### User Journeys
- `docs/User Journeys/00-USER_JOURNEY_SYSTEM_MAP.md`
- `docs/User Journeys/01-GOAL_PLANNING_JOURNEY.md`
- `docs/User Journeys/02-ONBOARDING_JOURNEY.md`
- `docs/User Journeys/03-FINANCIAL_STATE_JOURNEY.md`
- `docs/User Journeys/04-GOAL_FEASIBILITY_JOURNEY.md`
- `docs/User Journeys/05-STRATEGY_DECISION_JOURNEY.md`
- `docs/User Journeys/06-IMPLEMENTATION_DESIGN_JOURNEY.md`
- `docs/User Journeys/07-WHAT_IF_SCENARIO_JOURNEY.md`
- `docs/User Journeys/08-STRESS_RESILIENCE_JOURNEY.md`
- `docs/User Journeys/09-DECISION_RECOMMENDATION_JOURNEY.md`
- `docs/User Journeys/10-INVESTOR_ADOPTION_JOURNEY.md`
- `docs/User Journeys/11-ACCEPTED_PLAN_JOURNEY.md`
- `docs/User Journeys/12-ACTION_PLAN_JOURNEY.md`
- `docs/User Journeys/13-EXECUTION_JOURNEY.md`
- `docs/User Journeys/14-REVALIDATION_JOURNEY.md`
- `docs/User Journeys/15-GOAL_CHANGE_JOURNEY.md`
- `docs/User Journeys/16-FINANCIAL_STATE_CHANGE_JOURNEY.md`
- `docs/User Journeys/17-NEW_GOAL_AGAINST_EXISTING_PLAN_JOURNEY.md`
- `docs/User Journeys/18-STRATEGY_CHANGE_JOURNEY.md`
- `docs/User Journeys/19-MULTI_GOAL_WHOLE_PLAN_JOURNEY.md`
- `docs/User Journeys/20-NO_ACCEPTABLE_PATH_JOURNEY.md`
- `docs/User Journeys/21-INVESTOR_DESIGNED_STRATEGY_JOURNEY.md`

### Architecture
- `docs/architecture/BACKEND-FRONTEND-FEATURE-MAP.md`
- `docs/architecture/CANONICAL-CALCULATION-SYSTEM.md`
- `docs/architecture/FINANCIAL-PLANNING-LAYER-MAP.md`
- `docs/architecture/RISK-PROFILER-INVESTMENT-ENGINE-FOUNDATION.md`
- `docs/architecture/action-plan-implementation.md`
- `docs/architecture/code-architecture-consistency-audit.md`
- `docs/architecture/constraints.md`
- `docs/architecture/financial-state.md`
- `docs/architecture/goal-planner.md`
- `docs/architecture/multi-goal-planning.md`
- `docs/architecture/onboarding-to-moneywheel.md`
- `docs/architecture/portfolio-asset-mapping.md`
- `docs/architecture/product-selection.md`
- `docs/architecture/reporting-explanation.md`
- `docs/architecture/strategy-architecture-composition.md`
- `docs/architecture/strategy-matrix.md`
- `docs/architecture/strategy-recommendation-ranking.md`
- `docs/architecture/strategy-scenarios.md`
- `docs/architecture/strategy-versioning-approval.md`
- `docs/architecture/strategy-variants.md`
- `docs/architecture/variant-report-architecture.md`

### Audit, Product and Shared Rules
- `docs/audit/CANONICAL_MASTER_REGISTER.md`
- `docs/audit/DOCUMENT_DISCREPANCY_AUDIT.md`
- `docs/audit/SYSTEM_CLEANUP_REGISTER.md`
- `docs/behavioral-profile-rules.md`
- `docs/product/MONEYWHEEL-CHANGE-REGISTER.md`
- `docs/product/MONEYWHEEL-CONSTRAINTS.md`

## 9. Audit trail and limitation

- This update consolidates the major cross-document agreements and conflicts found in the repository's existing audits, detailed Decision Tree documents, real-life cases, architecture specifications, implementation plans and user journeys.
- The 98-file inventory is the scope manifest for continued line-level verification; it is not a claim that every runtime implementation path has been re-tested.
- Current implementation evidence and target design must remain separate until product decisions are approved and regression tests prove alignment.
- Do not delete code or documents as part of this register update.
