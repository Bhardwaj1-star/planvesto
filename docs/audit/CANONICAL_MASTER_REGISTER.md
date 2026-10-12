# Canonical Master Register — Planvesto Decision System

**Status:** DRAFT — reconciliation register, not yet a frozen V1 specification  
**Repository:** `Bhardwaj1-star/Planvesto`  
**Purpose:** Establish one index of authoritative sources for decision-system identity, rules, execution, and verification. This register does not invent or silently approve business rules.

## 1. Authority policy

1. **Runtime truth:** what the active code path actually executes, verified through callers, tests, and integration paths.
2. **Approved product truth:** the business rule explicitly approved for V1. Code is not automatically correct merely because it runs.
3. **This register:** the index that records the chosen authority for each domain, its status, and unresolved conflicts. It points to detailed source files; it does not duplicate every rule.
4. If runtime behavior and approved product truth differ, record a conflict here. Do not call either one the final truth until the conflict is resolved.
5. No deletion based only on filenames, duplication appearance, or document age. Verify callers, tests, migrations, and compatibility requirements first.

## 2. Domain authority register

| Domain | Current source / candidate owner | Authority status | Required action |
|---|---|---|---|
| Cleanup inventory and code triage | `docs/audit/SYSTEM_CLEANUP_REGISTER.md` | Inventory only; not business-rule authority | Refresh against a single recorded repository commit before cleanup decisions |
| Strategy Builder target flow and cross-cutting gaps | `docs/Decision tree/00.5-CROSS_CUTTING_REVERIFICATION_AND_GAP_AUDIT.md` | Audit guidance; explicitly not V1-frozen | Resolve listed legacy IDs, runtime order, and rule ownership gaps |
| Rule ownership decisions | `docs/Decision tree/00.6-RULE_OWNERSHIP_KEEP_MERGE_REPLACE_REMOVE_NEW_AUDIT.md` | Proposed ownership decisions; not proof of implementation | Verify each KEEP/MERGE/REPLACE/REMOVE decision against active callers and tests |
| Goal classification | `backend/rules/goals.py` | Candidate runtime owner | Verify all callers and approve definitions |
| Canonical strategy definitions | `backend/library/strategies/canonical.py` | Code registry; five canonical strategy IDs identified in audit | Verify runtime consumers and remove legacy IDs only after migration |
| Strategy selection/scoring | `backend/engines/strategy/decision.py` + `backend/rules/strategy_decision.py` | **CONFLICT — not canonicalized** | Consolidate ownership; resolve stale strategy IDs; add tests for approved behavior |
| Hard constraints | `backend/engines/constraints/*` and `ConstraintAggregator` | Runtime path exists; exact rule ownership needs verification | Establish one owner per constraint, formula, threshold, and status |
| Eligibility fits | `backend/rules/eligibility.py` + `backend/engines/strategy/eligibility.py` | **SPLIT OWNERSHIP** | Separate business-rule ownership from vocabulary/schema and freeze status semantics |
| Variant definitions | `backend/library/strategies/variants.py` | Code registry; audit identifies 22 variants | Verify each variant's canonical ID, parent strategy, and active use |
| Variant selection | `backend/engines/strategy/variant_selector.py` | Executable selector exists; placement/authority conflict remains | Make selection an explicit stage before composition/recommendation, if approved |
| Technique definitions | `backend/library/strategies/techniques_canonical.py` | Code registry; audit identifies 10 canonical techniques | Verify technique IDs, ownership/mapping, and active execution |
| Technique execution | `backend/engines/technique/*` | Implementation layer, not a strategy identity authority | Trace callers and confirm it cannot silently change strategy selection |
| Architecture composition | `backend/engines/strategy/composition.py` | Runtime implementation exists; ordering conflict remains | Verify composition consumes selected strategy/variant/techniques downstream |
| Solution mapping | `backend/library/strategies/solution_matrix.py` | Mapping/library source | Define “solution” precisely; do not mislabel techniques as solutions |
| Stress / resilience | `backend/engines/strategy/scenario.py` | Current scenario/what-if implementation; formal resilience gate not established | Approve stress taxonomy, thresholds, re-selection, and hard-constraint re-check behavior |
| Recommendation output | `backend/engines/strategy/recommendation.py` | Output-layer candidate | Ensure it explains the decision and does not create a second decision |
| Canonical rule metadata | `backend/rules/canonical.py` | **INCOMPLETE** — audit says not every runtime business rule is represented | Inventory executable rules and link each to an approved rule ID/version |
| Calculation formulas | `backend/engines/calculation/canonical.py` and consumers | Candidate calculation authority; duplicate formulas reported | Reconcile DTI and emergency-coverage calculations across every consumer |
| Final decision contract | `backend/engines/strategy/decision.py::evaluate_decision()` and recommendation path | Runtime authority exists; target contract not frozen | Document inputs, output/status vocabulary, ordering, and decision ownership |

## 3. Canonical identity vocabulary

The rule-ownership audit identifies these five canonical strategies:

- `strat-goal-funding`
- `strat-progressive-de-risking`
- `strat-capital-preservation`
- `strat-debt-reduction`
- `strat-credit-utilisation`

The audit identifies **22 variants** and **10 canonical techniques**. Their complete definitions and mappings remain in their code registries; this register does not duplicate them.

**Taxonomy rule to resolve and freeze:** Strategy ≠ Variant ≠ Technique ≠ Method/Policy ≠ Architecture/Composition ≠ Solution/Output. In particular, SIP, lumpsum, and step-up SIP must not be called variants merely because an older document places them in that column.

## 4. Blocking conflicts to resolve

| ID | Conflict | Required proof before closure |
|---|---|---|
| REG-001 | Old strategy IDs remain in scoring/runtime surfaces | Search all executable paths and tests; migrate and test canonical IDs |
| REG-002 | Rule identity metadata does not cover all runtime business rules | Every active rule has an owner, stable ID, version, and test |
| REG-003 | Eligibility business logic is split across modules | One approved owner per rule; other module is schema/vocabulary or adapter |
| REG-004 | Target decision order differs from current runtime order | Trace real call graph and approve the intended order |
| REG-005 | Variant selection is embedded in recommendation path | Test explicit variant output before composition/recommendation |
| REG-006 | Strategy / variant / technique / solution terminology conflicts | One approved taxonomy and mappings; align documents and code |
| REG-007 | DTI and emergency-coverage formulas differ between consumers | Approve one formula per metric; test all consumers against it |
| REG-008 | Status vocabulary and DTI boundary behavior differ | Approve thresholds and statuses; add boundary tests |
| REG-009 | Techniques exist without clear strategy/variant ownership | Assign or explicitly classify as unassigned/not eligible for use |
| REG-010 | Audit documents refer to different repository snapshots | Re-run verification on one commit and record its SHA |

## 5. Closure protocol

For every domain or conflict:

1. Record the exact code paths, documents, tests, and repository commit inspected.
2. Distinguish **observed runtime behavior** from **proposed/approved business behavior**.
3. Obtain explicit product-rule approval for unresolved decisions; do not infer approval from old documents.
4. Add or update tests for the approved rule and its boundaries.
5. Update the implementation and dependent documents only after the decision is recorded.
6. Mark status **VERIFIED** only when code, tests, and approved rule agree. Otherwise use **CONFLICT**, **UNVERIFIED**, or **NOT IMPLEMENTED**.
7. Do not delete a module until callers, imports, tests, migrations, and compatibility requirements are checked.

## 6. Status definitions

- **VERIFIED** — approved rule, active implementation, and tests agree.
- **CONFLICT** — sources disagree; decision required.
- **UNVERIFIED** — not enough runtime/call-graph evidence.
- **NOT IMPLEMENTED** — approved behavior has no verified implementation.
- **INVENTORY ONLY** — useful catalog/triage, not an authority for product behavior.
- **PROPOSED** — design recommendation awaiting approval.

## 7. Audit trail

- Register created as a starting index; it does **not** claim that V1 is frozen.
- Initial findings are based on the existing audit documents and identified code paths.
- Before using this register for destructive cleanup, re-verify every entry against the current target-branch commit and update this section with that commit SHA and date.
