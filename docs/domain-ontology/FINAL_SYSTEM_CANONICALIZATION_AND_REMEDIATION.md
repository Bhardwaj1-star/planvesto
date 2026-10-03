# Final System Canonicalization & Remediation Record\n\n## Purpose\nThis document records the important architectural conclusions, audit findings, unresolved risks, and final remediation direction established during the system-level review of Planvesto. It is the final reference for the last system-hardening pass and must be re-audited before sign-off.\n\n## 1. Canonical End-to-End Journey\nUser → Authentication / Planning Unit → Onboarding → Raw Financial Data → Financial State → Financial Metrics / Analysis → Goals → Goal Feasibility / Constraints → Strategy Candidates → Recommendation → Strategy Selection → Strategy Comparison → Implementation Preview → Implementation Finalization → StrategyVersion → Report → Action Plan → Execution.\n\n## 2. Core Source-of-Truth Architecture\n- Financial State = canonical representation of the investor's current financial position used by downstream planning logic.\n- Goal Type = canonical domain classification; Goal Name = human-readable specific goal identity.\n- StrategyRun = evaluation, candidate generation, recommendation context, and history.\n- StrategyVersion = authoritative finalized strategy snapshot.\n- Report = detailed representation of the finalized goal decision.\n- Action Plan = execution representation of the finalized decision.\n- Report and Action Plan must derive from the finalized StrategyVersion.\n\n## 3. Critical StrategyRun vs StrategyVersion Rule\nCanonical rule: StrategyRun is evaluation/history; StrategyVersion is finalized decision authority.\nAfter a StrategyVersion is finalized, latest StrategyRun, is_latest, ranking position, or historical recommendation must not drive the current Report, Action Plan, current decision, or restore a decision merely because it is the latest run.\nLegitimate StrategyRun uses: audit/history, historical inspection, evaluation context, and explicitly bounded compatibility.\nFinal audit must search for get_latest_run, is_latest, latest strategy run, selected_strategy_id, selected_strategy_version_id, and strategy_run_id, then classify each use as history, compatibility, or current decision authority.\n\n## 4. Strategy Identity and Implementation\nArchitecture identity is canonical, stable, and composition-independent: Goal ID + Primary Strategy ID. Supporting strategies, techniques, and solutions are composition data and must not change architecture identity.\nStrategy Builder is responsible for strategy building/selection. Selection is transient. Implementation Preview is stateless. StrategyVersion is created only when implementation is finalized.\nStrategy = WHAT approach. Implementation Parameters = HOW the approach is configured. StrategyVersion = immutable finalized snapshot.\n\n## 5. Moneywheel Canonical Contract\nCanonical backend Moneywheel contract = 9 ratios + 2 coverage rules.\nRatios: savings_rate, liquid_asset_ratio, debt_to_income_ratio, leverage_ratio, financial_asset_ratio, insurance_coverage_ratio, goal_funding_ratio, future_funding_ratio, required_rate_of_return.\nRules: expense_coverage, emergency_coverage.\nLegacy 12-ratio representations are compatibility/history data only. The frontend must consume the canonical backend contract.\n\n## 6. Legacy Moneywheel Compatibility\nHistorical snapshots may contain legacy signals. They must be normalized at the compatibility boundary into the current canonical contract.\nKnown legacy aliases include savings_ratio, expense_ratio, emergency_fund_coverage, current_liquidity_ratio, solvency_ratio, and insurance_gap_ratio.\nCompatibility aliases may exist for migration/history support, but must never become authoritative domain vocabulary or current business-rule outputs.\n\n## 7. Goal Canonicalization\nCanonical goal taxonomy is defined centrally in backend/rules/goals.py.\nDownstream engines must consume canonical values rather than directly reading alias maps or independently normalizing strings.\nKnown audit target: backend/engines/strategy/eligibility.py directly accessing GOAL_TYPE_ALIASES instead of the canonical normalization helper.\nGoal specialization and every other goal-dependent branch must normalize through the canonical goal helper before business logic.\n\n## 8. Goal Priority\nGoal priority is centralized through canonical_goal_priority() and get_priority_rank(). Downstream engines must not independently reinterpret priority aliases.\n\n## 9. Constraint Architecture\nCanonical flow: Financial Fact / Metric → Diagnostic Evidence → Goal-specific Business Rule → Constraint Result → Planning Effect.\nA financial metric status is not automatically a constraint severity. A critical ratio may remain diagnostic evidence; a goal-specific rule may convert it into a hard planning constraint.\n\n## 10. Threshold Ownership\nThresholds currently overlap across areas such as backend/rules/constraints.py, backend/rules/moneywheel.py, and backend/engines/constraints/evaluator.py.\nBefore refactoring, classify every threshold as: same business rule duplicated; intentionally different threshold; diagnostic threshold; or planning/eligibility threshold.\nDo not merge thresholds merely because they use the same metric. Each genuinely duplicated business rule should have one authoritative owner.\n\n## 11. Funding and Feasibility Vocabulary\nFunding has multiple semantic layers that must not be merged blindly.\nGoal funding examples: Shortfall, On Track, Overfunded.\nAllocation/execution funding examples: fully_funded, partially_funded, unfunded, within_surplus, surplus_shortfall, requires_review.\nFeasibility currently includes feasible, conditional, infeasible and elsewhere feasible, constrained, infeasible. Final remediation must determine whether conditional and constrained are identical or distinct semantics before changing vocabulary.\n\n## 12. Eligibility\nEligibility must have one canonical vocabulary and one authoritative evaluation path. It must consume canonical Goal Type and canonical constraint results, not raw strings or diagnostic metrics.\n\n## 13. Decision Authority Matrix\nGoal Type → central goal taxonomy.\nGoal Priority → canonical priority rules.\nFinancial State → Financial State builder/snapshot.\nFinancial Metrics → canonical metric definitions.\nConstraints → canonical constraint rules.\nMoneywheel → canonical 9 ratios + 2 rules.\nStrategy Library → strategy registry.\nArchitecture Identity → canonical identity generator.\nRecommendation → strategy recommendation output.\nStrategy Selection → explicit selected strategy context.\nFinalized Strategy → StrategyVersion.\nReport → StrategyVersion.\nAction Plan → StrategyVersion.\nHistory → StrategyRun/history only.\n\n## 14. Report Architecture\nAll individual goals use the same report contract/format; goal-specific data populates the generic structure.\nCanonical individual report source is StrategyVersion.\nCanonical backend version-scoped routes include /api/strategy/strategy-versions/{strategy_version_id}/report and /api/strategy/strategy-versions/{strategy_version_id}/report.pdf.\nLegacy run-based routes may remain for compatibility but must not become current decision authority.\nFrontend Reports Center is /investor/reports.\n\n## 15. Action Plan Architecture\nAction Plan is a goal-first execution workspace.\nCanonical journey: Goals → Select Goal → Find finalized StrategyVersion → Load execution points → Track execution → Completed / Pending / Skipped.\nIf no StrategyVersion exists, show that the goal has no finalized strategy and route to Strategy Builder.\nIf no execution points exist, explicitly show that state and allow generation where supported.\nExisting backend cancelled actions may be presented as Skipped. Do not invent a new persistence status without a separate business/schema decision.\n\n## 16. Frontend / Backend Boundary\nFrontend consumes backend domain contracts. It must not become an independent source of truth for goal taxonomy, thresholds, eligibility, feasibility, recommendation, strategy identity, financial calculations, or canonical Moneywheel definitions.\nUI labels and presentation state are allowed; business semantics remain backend/domain-owned.\n\n## 17. Auth and Ownership\nServer-side authentication and planning-unit ownership are part of the architecture. Final audit must verify ownership consistently across planning units, goals, StrategyRuns, StrategyVersions, reports, action plans, and execution endpoints.\n\n## 18. State Integrity\nFinal audit must identify impossible or ambiguous states across Goal, StrategyRun, Strategy Selection, Implementation, StrategyVersion, Report, Action Plan, and Execution.\nExamples: finalized implementation without StrategyVersion; Report or Action Plan without finalized StrategyVersion; Action Plan sourced from latest historical run; invalid selected StrategyVersion; inconsistent finalized implementation context; current recommendation overriding an already finalized decision.\n\n## 19. Legacy Compatibility Rule\nRequired pattern: Legacy Input → Canonical Adapter → Canonical Domain Model → Business Logic.\nLegacy input must not flow directly into business logic, and legacy output must not become current domain authority.\n\n## 20. Documentation Drift\nSynchronize docs/domain-ontology/CODE_FIRST_DOMAIN_ONTOLOGY.md, docs/domain-ontology/CANONICAL_CENTRALIZATION_AUDIT.md, and docs/domain-ontology/FULL_PRODUCT_SYSTEM_AUDIT_BRIEF.md with verified implementation.\nThis document is the final remediation record and must be updated after the final system-hardening pass.\n\n## 21. Final Audit Protocol\nAudit → Identify authority → Identify duplicates → Identify conflicts → Identify legacy compatibility → Define canonical semantics → Add regression tests → Refactor → Run CI → Re-audit → Update this document.\nDo not refactor based on assumptions. Do not modify schema/migrations merely for canonicalization unless separately justified. Do not redesign frontend merely to satisfy architectural cleanup.\n\n## 22. Final Remediation Priorities\nP0 — Decision Authority: prove StrategyVersion is the sole downstream authority after finalization and remove remaining current-decision dependencies on latest StrategyRun.\nP1 — Threshold Semantics: inventory and resolve genuinely duplicated threshold definitions and establish one owner per business rule.\nP1 — Canonical Domain Vocabulary: resolve feasibility, funding, eligibility, metric naming, and goal-normalization leaks.\nP2 — Legacy Aliases: ensure aliases are compatibility-only and cannot leak into authoritative outputs or business rules.\nP2 — Financial State / Metric Contracts: verify every metric has one canonical name, shape, calculation owner, and documented consumers.\nP2 — Frontend Contract: verify frontend API/domain representations match backend canonical contracts.\nP3 — Documentation: synchronize ontology and architecture documentation with verified implementation.\n\n## 23. Final System Principle\nRaw Data → Canonical Domain State → Business Rules → Decision → Finalized StrategyVersion → Outputs → Execution.\nThe objective is not merely duplicate-code removal. Every important business concept should have one canonical definition, one canonical vocabulary, one normalization boundary, one authoritative calculation/rule owner, one decision authority, clear compatibility boundaries, and tests enforcing the contract.\n\n## 24. Finalization Gate\nFinal sign-off requires: StrategyVersion is the sole finalized decision authority; StrategyRun is history/evaluation; goal taxonomy and priority are centralized; funding and feasibility semantics are explicit; eligibility and constraints are canonical; threshold ownership is resolved; Moneywheel is exactly 9 ratios + 2 rules; legacy aliases cannot become authoritative; financial metrics have canonical definitions; frontend consumes backend contracts; Report and Action Plan are StrategyVersion-sourced; auth/ownership is consistent; state transitions are coherent; tests enforce canonical behavior; and documentation matches the actual system.\n\nOnly after this gate should final system-hardening implementation be considered complete.

## 25. Deep Audit Findings — Must Be Resolved Before Final Sign-off

The read-only code-first audit identified concrete issues beyond the original architectural checklist. These are now part of the final remediation scope.

### 25.1 StrategyRun → Current Output Leakage

The repository contains explicit StrategyVersion-based paths, but consolidated planning/report paths still consume latest StrategyRuns.

Required distinction:

- Individual finalized outputs → StrategyVersion
- History/evaluation → StrategyRun
- Consolidated current decision outputs → must not silently fall back to latest StrategyRun when a finalized StrategyVersion exists

Final remediation must trace every latest-run consumer and classify it as:
1. legitimate history,
2. bounded compatibility,
3. prohibited current-decision authority.

### 25.2 Financial Calculation Semantics Conflict

The audit found a concrete calculation conflict in consolidated planning logic.

Examples identified:
- DTI is calculated from outstanding liabilities divided by annual income rather than debt-payment flow semantics.
- Emergency coverage is estimated using a percentage of financial assets rather than classified liquid assets / expense coverage semantics.

These are not merely duplicate constants. They can produce different financial conclusions for the same investor.

Final remediation must determine the canonical metric definition and make downstream consumers use that definition.

### 25.3 Client-Controlled Financial State at Execution Boundary

Action completion accepts a client-provided `actual_state` object, validates it as FinancialState, and persists it as the latest financial snapshot.

This is a critical integrity boundary.

Final remediation must explicitly determine:
- whether execution completion is allowed to create authoritative FinancialState,
- which fields may legitimately be changed by execution,
- what server-side source should own those values,
- what validation is required before persistence,
- whether client-supplied financial state can overwrite unrelated financial facts.

The execution event itself must not become an uncontrolled alternate source of truth for Financial State.

### 25.4 Approval Lifecycle Ambiguity

The audit found:
- implementation finalization creates an immutable `provisional` StrategyVersion,
- action generation requires an approval snapshot,
- read-side approval checks exist,
- but a clear backend approval-snapshot creation service/API was not established in the searched code.

Therefore the lifecycle currently appears to contain two concepts:

`provisional/finalized StrategyVersion`
and
`approved StrategyVersion / approval snapshot`.

These must be explicitly defined.

Final state machine must answer:

`selected → implementation preview → finalized/provisional → approved → report/action execution`

or establish a different authoritative lifecycle.

No assumption should be made that `provisional` and `approved` are the same state.

### 25.5 Onboarding Data-Ownership Split

The audit found that frontend onboarding directly persists core/raw investor data through Supabase, while backend services construct FinancialState snapshots from those persisted records.

This can be valid, but the ownership boundary must be explicit.

Final audit must establish:
- which layer owns raw data persistence,
- which layer owns FinancialState construction,
- which layer owns calculated metrics,
- whether frontend can ever persist derived financial state,
- whether every downstream planning engine consumes the server-generated snapshot.

### 25.6 Alias Collision — current_liquidity_ratio

A concrete semantic alias collision was identified.

Financial-health diagnostics consume `current_liquidity_ratio`, while normalization fallback can substitute `liquid_asset_ratio`.

These are not automatically equivalent merely because both describe liquidity.

Final remediation must verify:
- definition,
- numerator,
- denominator,
- unit,
- intended business meaning,
- all consumers.

Only then may they be mapped to one canonical concept.

If they are distinct metrics, they must retain distinct canonical names.

### 25.7 Approval Snapshot Integrity

RLS allows authenticated owners to insert their own approval snapshot directly, while backend action-generation logic primarily checks whether an approval snapshot exists.

Final remediation must verify that approval cannot be satisfied merely by inserting an arbitrary snapshot that has not been validated against:
- planning unit,
- goal,
- StrategyVersion,
- suitability/decision context,
- required approval state.

Existence of an approval record must not automatically equal valid approval unless the data itself is integrity-checked.

### 25.8 Test Execution Failure Must Be Resolved

The targeted audit test command failed.

The final audit report must record:
- exact failing test(s),
- failure reason,
- whether failure is a stale test, implementation regression, environment problem, or legitimate contract conflict,
- required remediation.

A failed targeted test suite cannot be treated as a completed validation gate.

---

## 26. Evidence-First Remediation Protocol

The final implementation must NOT begin immediately after identifying these findings.

Required sequence:

1. Complete the read-only audit.
2. Produce exact evidence for every finding.
3. Identify the canonical authority.
4. Identify every affected consumer.
5. Separate actual conflicts from intentional semantic differences.
6. Define the target canonical contract.
7. Define required regression tests.
8. Implement only the approved remediation.
9. Run full CI and targeted regression tests.
10. Perform a second read-only audit against the same findings.
11. Confirm no new competing source of truth was introduced.
12. Update this document with the verified final state.
13. Only then declare final system sign-off.

No finding should be closed merely because code was changed. It is closed only when:
- the canonical authority is explicit,
- the old competing path is removed or bounded,
- tests enforce the intended behavior,
- CI passes,
- and the second audit confirms the result.

---

## 27. Final Remediation Matrix

| Priority | Area | Current Finding | Required Final State |
|---|---|---|---|
| P0 | Decision Authority | Latest StrategyRun still feeds some consolidated outputs | StrategyVersion is sole current finalized authority |
| P0 | Financial State Integrity | Client-provided actual_state can become latest snapshot during action completion | Authoritative financial-state mutation has explicit server-owned boundary |
| P1 | Thresholds / Metrics | FinancialPlanService contains competing financial-health calculations | Canonical metric definitions and threshold ownership |
| P1 | Approval Lifecycle | Provisional StrategyVersion and approval snapshot are separate but lifecycle is unclear | Explicit finalized → approved semantics |
| P1 | Approval Integrity | Approval existence may be sufficient without clear validation | Approval is validated against exact planning context |
| P1 | Metric Collision | current_liquidity_ratio may fall back to liquid_asset_ratio | One proven canonical metric or two explicitly distinct metrics |
| P1 | Onboarding Boundary | Frontend raw-data persistence and backend snapshot construction are split | Explicit ownership boundary with no derived-state bypass |
| P2 | Legacy Aliases | Multiple aliases remain across domains | Compatibility-only aliases with no authoritative leakage |
| P2 | Tests | Targeted audit test command failed | Relevant regression suite passes |
| P2 | Documentation | Architecture docs can drift from implementation | Docs updated only after verified remediation |

---

## 28. Final Audit Deliverable

The completed audit must produce exactly these sections:

1. EXECUTIVE SYSTEM VERDICT
2. STRATEGYR​​UN vs STRATEGYVERSION AUTHORITY AUDIT
3. THRESHOLD OWNERSHIP AUDIT
4. LEGACY ALIAS AUDIT
5. END-TO-END DOMAIN BOUNDARY AUDIT
6. STATE MACHINE AUDIT
7. SOURCE-OF-TRUTH MATRIX
8. CONFLICT / DUPLICATION MATRIX
9. DOCUMENTATION DRIFT
10. STALE TEST / LEGACY CODE FINDINGS
11. PRIORITIZED REMEDIATION BACKLOG
12. CANONICAL TARGET ARCHITECTURE

Every remediation item must include:
- Priority
- Problem
- Evidence
- Affected files
- Current authority
- Proposed canonical authority
- Required change
- Risk if unchanged
- Whether backend/frontend/schema/migration is required

This deliverable is audit-only until the remediation scope is explicitly approved.
