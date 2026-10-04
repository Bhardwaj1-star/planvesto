# Planvesto — Final System Implementation Plan

## 0. Purpose

This document is the **implementation execution plan** for the system-hardening work defined by:

- `docs/domain-ontology/FINAL_SYSTEM_CANONICALIZATION_AND_REMEDIATION.md`

The governing document contains the completed audit, canonical target architecture, and approved business decisions.

This document answers a different question:

> **Exactly what do we implement, in what order, what depends on what, how do we test it, and when is the system actually finished?**

This is an implementation document, not a second audit.

---

# 1. Current Position

## Completed

- Full repository/system audit: **DONE**
- Canonical architecture direction: **DEFINED**
- D1–D8 business decisions: **RESOLVED**
- Remediation backlog: **DEFINED**
- Dependency order: **DEFINED**

## Remaining

- Canonical definitions must be enforced in code.
- Competing authorities must be removed or explicitly bounded.
- Financial metrics and thresholds must be centralized.
- StrategyVersion must become the finalized decision authority.
- FinancialState freshness/integrity must be enforced.
- Approved D1 execution-state authority must be implemented safely.
- Approval lifecycle must become explicit and version-bound.
- Legacy aliases must become compatibility-only.
- Frontend/backend contracts must converge.
- Regression tests must encode the canonical architecture.
- CI must pass with real dependencies.
- A second read-only audit must verify the implementation.
- Documentation must be synchronized after implementation.

## Important

**Do not perform another broad repository audit before implementing this plan.**

The audit is already complete. Implementation should use the verified findings and exact surfaces recorded in the governing document.

---

# 2. Binding Business Decisions

These decisions are final and must not be silently reinterpreted during implementation.

| ID | Decision | Binding rule |
|---|---|---|
| D1 | Execution / FinancialState authority | Client-submitted full `actual_state` is authoritative and may establish/update FinancialState on action completion. |
| D2 | Report state basis | Provide both finalized-decision state/context and separate current/latest state view. |
| D3 | Liquidity identity | `current_liquidity_ratio` and `liquid_asset_ratio` remain distinct canonical metrics. |
| D4 | Threshold ownership | Centralize only when metric + business purpose are identical. |
| D5 | Emergency coverage | Canonical emergency coverage = liquid assets / essential monthly expenses. 20% financial-assets estimate is not canonical coverage. |
| D6 | Vocabulary | `constrained` = funding/feasibility limitation; `conditional` = strategy eligibility condition. |
| D7 | Approval | Explicit user approval bound to exact StrategyVersion + Goal context. |
| D8 | Goal revision | Old StrategyVersion remains history but loses current authority for revised goal; new version required. |

---

# 3. Implementation Principles

1. **Authority before cleanup.**
2. **Canonicalize at boundaries.**
3. **One calculation definition per metric.**
4. **One authoritative owner per business rule.**
5. **Compatibility adapters may accept legacy input, but business logic emits/uses canonical representations.**
6. **Do not merge concepts merely because names look similar.**
7. **Do not introduce schema changes unless the selected contract requires persisted state.**
8. **Do not invent new business rules.**
9. **Every authority change gets regression coverage.**
10. **A phase is complete only when implementation + tests + CI evidence support it.**

---

# 4. Dependency Graph

The implementation must follow this order:

```
Approved D1–D8
      ↓
P0 — Decision + FinancialState authority
      ↓
P1 — Financial semantics + lifecycle integrity
      ↓
P2 — Compatibility + API/frontend contracts + regression suite
      ↓
P3 — Documentation synchronization
      ↓
Full CI
      ↓
Second read-only audit
      ↓
Final sign-off
```

Do not start a downstream phase when an upstream authority boundary is still unresolved.

---

# 5. P0 — Decision Authority and FinancialState Integrity

## P0.1 StrategyRun → StrategyVersion authority

### Objective

Make finalized StrategyVersion the sole current decision authority.

### Current risk

Current reports, plans, baskets, and actions can obtain decision/composition data through latest or linked StrategyRun state.

### Target

```
StrategyRun
= evaluation / candidate generation / scenarios / history

StrategyVersion
= finalized immutable decision / implementation authority

StrategyVersion
    ↓
Report
    ↓
Action Plan
    ↓
Execution
```

### Audited implementation surfaces

- `MultiGoalPlanningService.build_multi_goal_plan()`
- `BasketReportService.build_report()`
- `GoalReportService._load_by_strategy_version()`
- `GoalReportService.build_report()`
- `StrategyActionGenerator.generate()`
- `StrategyRepository.get_selected_strategy_version_id()`
- StrategyService finalization
- version-scoped report/API surfaces
- legacy run-ID report/retirement routes

### Implementation tasks

1. Identify every current-decision read from StrategyRun.
2. Classify each read as:
   - current decision authority,
   - history,
   - preview,
   - compatibility.
3. Remove StrategyRun as current authority.
4. Ensure StrategyVersion stores or references:
   - Goal identity,
   - exact goal/DefinedGoal version,
   - Strategy Architecture identity/composition,
   - implementation parameters/context.
5. Route current report generation through StrategyVersion.
6. Route current basket/plan outputs through StrategyVersion.
7. Route action generation through StrategyVersion.
8. Restrict run-ID routes to explicitly historical/compatibility behavior.
9. Enforce D8 goal-version consistency.
10. Reject mismatched Goal/DefinedGoal/StrategyVersion combinations.

### Schema impact

Likely, depending on existing persistence:

- StrategyVersion goal/version context
- architecture/composition context
- explicit current-version relationship if required

Do not add fields that are not required by the actual target contract.

### Regression tests

- Finalize StrategyVersion.
- Create/mutate later StrategyRuns.
- Verify current report is unchanged.
- Verify PDF/report is unchanged.
- Verify basket/plan output is unchanged.
- Verify generated actions are unchanged.
- Reject wrong goal-version combinations.
- Verify old version remains available as history after goal revision.
- Verify new goal revision requires new finalized version.

### Exit criteria

No current report, plan, basket, or action path derives finalized decision authority from latest StrategyRun.

---

## P0.2 FinancialState freshness and integrity

### Objective

Prevent stale FinancialState from silently driving current planning decisions.

### Current risk

Consumers can select latest snapshot by `calculated_at` even after raw onboarding data changes.

### Audited surfaces

- `FinancialStateService.build()`
- `FinancialStateEngine.build()`
- `FinancialStateSnapshotRepository.get_latest()`
- GoalService freshness path
- StrategyService consumers
- onboarding raw-data persistence boundary

### Implementation tasks

1. Establish the authoritative raw-input revision boundary.
2. Choose one freshness mechanism:
   - input revision binding, or
   - reliable rebuild-before-current-decision.
3. Bind/rebuild snapshots accordingly.
4. Ensure current consumers reject or refresh stale snapshots.
5. Keep onboarding responsible for raw data only.
6. Keep derived FinancialState ownership in the backend.
7. Ensure all current planning consumers use the same freshness rule.

### Schema impact

Potential:

- raw input revision
- FinancialState source revision
- snapshot lineage

Only implement if required by the selected freshness mechanism.

### Regression tests

- Create snapshot.
- Change raw financial input.
- Request feasibility.
- Request strategy.
- Request analysis.
- Request report.
- Generate actions.
- Verify all current outputs use refreshed state.
- Verify stale snapshot cannot masquerade as current.

### Exit criteria

A current planning decision cannot silently consume FinancialState derived from an obsolete raw-data revision.

---

## P0.3 D1 — Client actual_state authority

### Objective

Implement the explicitly approved D1 decision.

### Binding decision

The client may submit the full `actual_state`.

That submitted full state is authoritative for the resulting FinancialState snapshot.

### Audited surface

- `ActionPlanService.complete_action_with_actual_state()`
- `/api/action-plan/actions/{action_id}/complete`
- FinancialState snapshot persistence
- `ActionPlanService.complete_action()`

### Target

```
Action Completion
      ↓
validated full actual_state
      ↓
authoritative FinancialState Snapshot
      ↓
action → snapshot lineage
      ↓
current FinancialState consumers
```

### Implementation tasks

1. Preserve full `actual_state` in the completion contract.
2. Validate the entire FinancialState shape.
3. Validate authenticated ownership.
4. Validate action/planning-unit scope.
5. Validate the snapshot belongs to the relevant planning context.
6. Persist the authoritative snapshot.
7. Record action-to-snapshot lineage.
8. Ensure current-state selection uses the resulting authoritative snapshot.
9. Prevent unrelated hidden writers from silently superseding it.
10. Review the second completion method:
    - unify it with the authoritative path, or
    - explicitly bound/remove it if it is unused.
11. Make both completion paths consistent if both remain.

### Important

Do **not** replace D1 with server-only derivation. D1 explicitly selected full client-submitted actual_state authority.

### Regression tests

- Valid full snapshot accepted.
- Invalid FinancialState rejected.
- Wrong planning unit rejected.
- Wrong action scope rejected.
- Forged unrelated ownership rejected.
- Valid snapshot becomes authoritative.
- Action-to-snapshot lineage exists.
- Current FinancialState reflects the completed action.
- Second completion path cannot create a conflicting authority.

### Exit criteria

D1 is implemented as an explicit, validated, traceable authority boundary.

---

# 6. P1 — Financial Semantics and Lifecycle Integrity

## P1.1 Canonical financial metric definitions

### Objective

Ensure every financial metric has:

- one name,
- one formula,
- one unit,
- one owner,
- documented consumers.

### Canonical calculation authority

Use:

`backend/engines/calculation/canonical.py`

for verified canonical formulas.

### Tasks

1. Inventory each current consumer of canonical metrics.
2. Replace local duplicate calculations.
3. Remove formula drift.
4. Ensure all consumers use the same canonical value.
5. Add shared fixtures for cross-service equality.
6. Document metric units explicitly.

---

## P1.2 DTI

### Target

All DTI consumers must use the approved canonical definition rather than local competing formulas.

### Tasks

1. Verify canonical DTI calculation.
2. Replace FinancialPlanService local DTI calculation.
3. Remove duplicate DTI formula.
4. Centralize identical diagnostic boundaries per D4.
5. Preserve distinct planning thresholds when their purpose differs.

### Tests

- Formula test.
- Unit test.
- Shared fixture across consumers.
- Boundary tests.
- Diagnostic vs planning threshold tests.

---

## P1.3 Emergency coverage

### Binding decision

Canonical emergency coverage:

`liquid assets / essential monthly expenses`

The 20% financial-assets estimate is not canonical emergency coverage.

### Tasks

1. Replace the current FinancialPlanService emergency coverage calculation.
2. Ensure denominator is essential monthly expenses.
3. Ensure numerator is classified liquid assets.
4. If the 20% estimate is retained, rename it as a separate planning estimate and document its owner.
5. Do not expose the estimate as canonical emergency coverage.

### Tests

- Same fixture across FinancialState/Moneywheel/FinancialPlanService.
- Unit correctness.
- Boundary coverage.
- Ensure estimate and metric cannot be confused.

---

## P1.4 Liquidity metrics

### Binding decision

Keep:

- `current_liquidity_ratio`
- `liquid_asset_ratio`

as distinct canonical metrics.

### Definitions

Current liquidity:

`liquid assets / short-term liabilities`

Liquid asset ratio:

`liquid assets / total assets`

### Tasks

1. Remove incompatible fallback.
2. Ensure no consumer substitutes one for the other.
3. Define units explicitly:
   - current liquidity: multiple
   - liquid asset ratio: percentage/ratio as defined by contract.
4. Assign separate threshold ownership.
5. Preserve legacy names only through explicit compatibility handling.

### Tests

- Formula tests.
- Unit tests.
- Missing-data tests.
- No-fallback test.
- Threshold tests.
- API contract tests.

---

## P1.5 Threshold ownership

### Binding decision

Centralize only when both:

- metric is identical,
- business purpose is identical.

### Audited surfaces

- `backend/rules/moneywheel.py::RULES`
- `backend/rules/constraints.py`
- `backend/engines/constraints/evaluator.py`
- FinancialPlanService thresholds

### Tasks

Classify each threshold as:

1. metric boundary,
2. diagnostic band,
3. planning constraint,
4. eligibility threshold,
5. strategy-selection threshold,
6. distinct benchmark.

Then:

- centralize genuine duplicates,
- retain intentionally distinct thresholds,
- remove duplicated literals only where semantics are identical.

### Required attention

- savings threshold overlap
- DTI overlap
- leverage 30–50% conflict
- financial asset 50% guardrail
- required-return suitability
- FinancialPlanService savings/reserve/DTI policies

No unresolved policy may be silently unified.

### Tests

Boundary tests for every changed threshold.

---

## P1.6 Goal priority canonicalization

### Current risk

Canonical priority normalization exists, but raw priority aliases may still be persisted or consumed.

### Tasks

1. Normalize priority at the input boundary.
2. Ensure RuleEngine consumes canonical priority.
3. Ensure every business consumer uses canonical priority.
4. Keep UI labels presentation-only.
5. Test aliases produce identical behavior.

### Tests

For every supported alias:

`alias → canonical priority → identical ranking/business behavior`

---

## P1.7 Funding / feasibility / eligibility semantics

### Binding decision

Keep distinct:

- `constrained` = funding/feasibility limitation
- `conditional` = strategy eligibility condition

Also preserve separate goal-level funding statuses and allocation statuses.

### Tasks

1. Canonicalize backend status vocabulary.
2. Align frontend status vocabulary.
3. Remove accidental equivalence.
4. Preserve goal funding statuses separately from allocation statuses.
5. Keep eligibility as requirement/evidence comparison.
6. Do not introduce a global numeric risk cutoff.

### Tests

- Funding status tests.
- Feasibility tests.
- Eligibility pass/conditional/fail tests.
- `constrained` vs `conditional` semantic tests.
- Frontend/backend serialization tests.

---

## P1.8 Approval lifecycle

### Binding decision

Approval is an explicit user action bound to:

- Planning Unit
- Goal
- DefinedGoal version
- StrategyVersion
- approved context

### Current risk

Approval-row existence is checked, but an application-level approval writer/transition is not established.

### Tasks

1. Define explicit approval command/API.
2. Validate authenticated ownership.
3. Validate exact planning-unit relationship.
4. Validate exact Goal relationship.
5. Validate exact DefinedGoal version.
6. Validate exact StrategyVersion.
7. Persist approval evidence/context.
8. Implement action-generation approval gate.
9. Implement changed-version invalidation/reapproval.
10. Align StrategyEditService behavior.
11. Keep provisional/finalized distinct from approved.
12. Tighten approval RLS/foreign-record integrity where required.

### Tests

- Valid approval.
- Wrong planning unit.
- Wrong goal.
- Wrong DefinedGoal.
- Wrong StrategyVersion.
- Changed version.
- Edited strategy.
- Action gate.
- Approval persistence.
- RLS integration.

---

## P1.9 D8 — Goal revision and version integrity

### Binding decision

Old StrategyVersion remains history but cannot remain current authority for a revised goal.

### Tasks

1. Bind StrategyVersion to exact goal version.
2. Reject mismatches.
3. Ensure current-version selection does not rely only on run history.
4. Require new finalization after goal revision.
5. Preserve old version as history.
6. Ensure reports/actions use only the valid current version.

### Tests

- Finalize version.
- Revise goal.
- Verify old version remains history.
- Verify old version cannot become current authority.
- Finalize new version.
- Verify new version becomes current.

---

# 7. P2 — Compatibility and Contract Hardening

## P2.1 Legacy aliases

### Objective

Legacy compatibility must never become business authority.

### Required pattern

```
Legacy Input
   ↓
Compatibility Adapter
   ↓
Canonical Domain Model
   ↓
Business Logic
```

### Surfaces

- goal aliases
- priority aliases
- Moneywheel legacy keys
- architecture ID aliases
- legacy report fields
- run-ID routes
- MoneyWheelEngine import alias

### Tasks

1. Keep legacy acceptance only where compatibility is required.
2. Normalize immediately.
3. Emit canonical vocabulary.
4. Prevent legacy values from reaching business logic.
5. Bound run-ID routes to history/compatibility.
6. Remove duplicate frontend canonical maps where backend authority exists.

---

## P2.2 Moneywheel contract validation

### Canonical contract

**9 ratios + 2 rules**

### Ratios

1. savings_rate
2. liquid_asset_ratio
3. debt_to_income_ratio
4. leverage_ratio
5. financial_asset_ratio
6. insurance_coverage_ratio
7. goal_funding_ratio
8. future_funding_ratio
9. required_rate_of_return

### Rules

1. expense_coverage
2. emergency_coverage

### Tasks

1. Validate exact canonical ratio keys.
2. Validate exact canonical rule keys.
3. Validate cardinality.
4. Reject or normalize invalid stored metadata.
5. Tighten frontend TypeScript types.
6. Remove unrestricted rule/key contracts.

### Tests

- exact 9 ratio keys
- exact 2 rule keys
- invalid key rejection
- invalid cardinality
- serialization fixtures
- frontend compile/typecheck

---

## P2.3 Frontend/backend contracts

### Known mismatches

- Moneywheel frontend keys unrestricted.
- StrategyRun frontend has `approval_status` not represented equivalently in backend.
- StrategyRun frontend omits backend `what_if_scenarios`.
- GoalStatus frontend is closed while backend status is open string.
- Priority vocabulary differs between presentation and backend.
- `conditional` / `constrained` semantics need explicit alignment.

### Tasks

1. Backend remains domain contract authority.
2. Align frontend TypeScript contracts.
3. Prefer generated contracts if supported.
4. Otherwise add contract tests.
5. Update frontend only where verified API semantics require it.
6. Ensure no frontend code reimplements business rules.

### Tests

- API serialization fixtures.
- Invalid status tests.
- Moneywheel shape tests.
- TypeScript compile.
- Frontend build.

---

## P2.4 Onboarding boundary

### Target

```
Frontend
→ raw investor data
→ persistence
→ backend FinancialState
→ metrics/planning
```

### Tasks

- Ensure onboarding persists raw inputs only.
- Prevent derived planning state from being persisted as authoritative frontend data.
- Ensure FinancialState is generated/updated through the approved backend boundary.
- Add regression test for raw-vs-derived ownership.

---

## P2.5 Regression suite migration

### Known stale-to-target tests

- `test_financial_ratio_constraints.py`
- `test_multi_goal_planning_service.py`
- `test_basket_report_service.py`

### Tasks

1. Update tests to canonical metric keys.
2. Remove tests that intentionally encode latest-run current authority.
3. Add StrategyVersion authority tests.
4. Add Moneywheel stored-rule validation tests.
5. Add action actual_state authority tests.
6. Add approval lifecycle tests.
7. Add D8 version-integrity tests.
8. Add frontend/backend contract tests.

---

# 8. P3 — Documentation Synchronization

Documentation is updated **after implementation**, not before.

## Required documentation updates

- Domain ontology
- Strategy lifecycle
- StrategyRun vs StrategyVersion authority
- FinancialState ownership
- Metric definitions
- Threshold ownership
- Goal/feasibility/eligibility vocabulary
- Approval lifecycle
- Execution authority
- Moneywheel contract
- Legacy compatibility
- Frontend/backend contracts

## Documentation rule

Documentation must describe verified implementation, not intended implementation.

---

# 9. Test Strategy

## 9.1 Authority tests

Prove:

- StrategyRun mutation does not change current finalized outputs.
- StrategyVersion is authoritative.
- Goal-version mismatch is rejected.
- Old versions remain history.

## 9.2 FinancialState tests

Prove:

- raw-data changes invalidate/refresh state correctly.
- D1 actual_state becomes authoritative after valid completion.
- invalid/mismatched snapshots are rejected.
- action-to-snapshot lineage exists.

## 9.3 Metric tests

Prove:

- one formula per metric.
- one unit per metric.
- identical fixtures produce identical values across consumers.
- liquidity metrics cannot substitute for each other.
- emergency coverage uses canonical formula.

## 9.4 Threshold tests

Prove:

- identical metric/purpose thresholds share authority.
- intentionally distinct thresholds remain distinct.
- every changed boundary has regression coverage.

## 9.5 Lifecycle tests

Prove:

- approval is explicit.
- approval is exact-version-bound.
- changed strategy context requires correct approval behavior.
- revised goals require new StrategyVersion.
- invalid state transitions fail.

## 9.6 Compatibility tests

Prove:

- legacy input normalizes.
- legacy aliases cannot reach business logic.
- canonical output is emitted.
- run-ID compatibility routes cannot become current authority.

## 9.7 Ownership/security tests

Prove cross-planning-unit access is rejected for:

- goals
- DefinedGoals
- FinancialState snapshots
- StrategyRuns
- StrategyVersions
- reports
- action plans
- execution actions
- approvals

---

# 10. CI Validation Plan

## Before implementation

The previous audit environment lacked required tooling/dependencies.

Do not interpret that as a code failure.

## During implementation

Run targeted tests after each affected phase.

### P0

- strategy/version tests
- FinancialState tests
- action completion tests

### P1

- financial metric tests
- threshold tests
- approval tests
- goal/feasibility/eligibility tests

### P2

- Moneywheel tests
- contract tests
- frontend typecheck/tests

## Final CI

Require:

1. backend dependency installation
2. backend targeted tests
3. full backend suite
4. frontend dependency installation
5. frontend tests
6. frontend typecheck
7. frontend build/CI checks
8. migration tests
9. RLS integration tests
10. all CI jobs green

---

# 11. Second Read-Only Audit

Only start after:

- P0 complete
- P1 complete
- P2 complete
- regression suite updated
- full CI green

The second audit must verify:

### Authority

- StrategyVersion is sole current finalized decision authority.
- StrategyRun is history/evaluation only.
- D1 actual_state path is the explicit FinancialState execution authority.

### Freshness

- no stale FinancialState path remains.

### Metrics

- canonical formulas are used everywhere.
- liquidity metrics remain distinct.
- emergency coverage is canonical.
- threshold ownership matches D4.

### Lifecycle

- approval is exact-version-bound.
- D8 version/goal binding is enforced.
- impossible transitions are blocked.

### Compatibility

- aliases cannot regain business authority.
- Moneywheel output is exactly 9 + 2.
- frontend/backend contracts agree.

### Security

- ownership boundaries hold across all child resources.

### Tests

- every critical authority boundary has regression coverage.

---

# 12. Phase Completion Gates

## P0 complete when

- [ ] StrategyVersion controls finalized current output.
- [ ] StrategyRun cannot silently control current output.
- [ ] FinancialState freshness is deterministic.
- [ ] D1 actual_state authority is explicit and validated.
- [ ] Action-to-state lineage exists.
- [ ] P0 regression tests pass.

## P1 complete when

- [ ] DTI is canonical.
- [ ] Emergency coverage is canonical.
- [ ] Liquidity metrics are distinct.
- [ ] Threshold ownership is centralized where appropriate.
- [ ] Goal priority is canonical everywhere.
- [ ] Funding/feasibility/eligibility semantics are explicit.
- [ ] Approval lifecycle is implemented.
- [ ] D8 goal-version binding is enforced.
- [ ] P1 regression tests pass.

## P2 complete when

- [ ] Legacy aliases are compatibility-only.
- [ ] Moneywheel is exactly 9 ratios + 2 rules.
- [ ] Frontend/backend contracts agree.
- [ ] Onboarding raw-data boundary is enforced.
- [ ] Stale tests are migrated to target behavior.
- [ ] P2 regression tests pass.

## P3 complete when

- [ ] Documentation matches verified implementation.
- [ ] No document describes superseded authority.
- [ ] Canonical vocabulary is consistent across docs.

## Final complete when

- [ ] All P0–P3 gates pass.
- [ ] Full CI is green.
- [ ] Migration/RLS integration tests pass where applicable.
- [ ] Second read-only audit passes.
- [ ] No competing current authority remains.
- [ ] All approved D1–D8 decisions are implemented exactly.
- [ ] Final sign-off criteria in the governing document are satisfied.

---

# 13. Final System Completion Definition

The system is finished only when this is true in **code, data flow, tests, and documentation**:

```
RAW DATA
    ↓
CANONICAL FINANCIAL STATE
    ↓
CANONICAL METRICS
    ↓
GOAL + CONSTRAINTS
    ↓
STRATEGY EVALUATION
    ↓
STRATEGY SELECTION
    ↓
IMPLEMENTATION
    ↓
STRATEGY VERSION
    ↓
APPROVAL
    ↓
REPORT
    ↓
ACTION PLAN
    ↓
EXECUTION
    ↓
AUTHORITATIVE FINANCIAL STATE UPDATE
```

With these invariants:

- one canonical definition,
- one authoritative owner,
- explicit lifecycle,
- bounded compatibility,
- test-enforced contracts,
- no silent competing authority.

---

# 14. Execution Rule for the Coding Agent

When implementing this plan:

1. Work in dependency order.
2. Implement one coherent work package at a time.
3. Run targeted tests after each work package.
4. Do not silently change business semantics.
5. If implementation reveals a genuinely new business decision not covered by D1–D8, stop and raise that decision explicitly.
6. Do not perform a broad re-audit.
7. Do not mark a work package complete without its regression evidence.
8. Keep the governing canonicalization document and this implementation plan synchronized when implementation changes materially.
9. Update documentation only after behavior is verified.
10. Finish with CI + second read-only audit + sign-off.

**This document is the execution checklist. The governing canonicalization document remains the source of truth for the audited evidence and approved architecture.**
