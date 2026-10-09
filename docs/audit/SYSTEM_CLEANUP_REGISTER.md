# System Cleanup Register — Code-Only Baseline

**Repository:** `Bhardwaj1-star/Planvesto`  
**Branch inspected:** `main`  
**Code snapshot:** `62a1c6a3bb94dd090d358bfd9e707ba1a6dacdb4`  
**Method:** Repository tree, implementation files, imports/usages found through code search, and existing automated tests. Product/architecture documents were not used as evidence for this register.  
**Important:** This is an initial code inventory and cleanup triage. A file's existence or a test's existence does not prove that the feature is required, correct, or reachable in production. No code has been deleted by this audit.

---

## 1. Register Status Definitions

- **KEEP-CANDIDATE** — directly participates in an apparent application path; retain pending deeper call-graph verification.
- **VERIFY-USAGE** — module exists, but all runtime entry points and callers must be traced before a decision.
- **DUPLICATION-RISK** — similar responsibilities or overlapping modules exist; compare call sites and contracts before consolidating.
- **CONFLICT-RISK** — code paths appear to make overlapping decisions or own the same rule; identify the single runtime authority.
- **TEST-ONLY** — automated test or fixture; keep if it validates retained behavior, remove only after confirming redundancy.
- **INFRASTRUCTURE** — build, deployment, configuration, persistence or schema; do not delete based only on application-code search.
- **NOT-CLASSIFIED** — tree presence alone is insufficient to decide.

No entry is labelled **DELETE** merely because it looks old, has a similar filename, or was not found in a limited search.

---

## 2. Repository Baseline

At the inspected snapshot, the recursive Git tree contains **557 files**. The following top-level code areas exist:

```text
Planvesto
├── .github/workflows
├── backend
│   ├── api
│   ├── config
│   ├── data
│   ├── engines
│   │   ├── action_plan
│   │   ├── allocation
│   │   ├── basket
│   │   ├── calculation
│   │   ├── constraints
│   │   ├── financial_state
│   │   ├── goal
│   │   ├── investment
│   │   ├── moneywheel
│   │   ├── orchestration
│   │   ├── profile
│   │   ├── risk_profiler
│   │   ├── rules
│   │   ├── strategy
│   │   ├── suitability
│   │   ├── summary_report
│   │   └── technique
│   ├── library/strategies
│   ├── models
│   ├── report_engine
│   ├── rules
│   ├── schemas
│   ├── services
│   └── tests
├── frontend
├── supabase/migrations
└── docs
```

This tree is a structural inventory, not a claim that every listed module is used at runtime.

---

## 3. Code Entry Points and Integration Surface

| Area | Code entry points found | Status | Required verification |
|---|---|---|---|
| Application startup / route registration | `backend/main.py`, `backend/api/*` | KEEP-CANDIDATE / VERIFY-USAGE | Confirm every registered router is needed and reachable; identify unregistered endpoint modules. |
| Authentication | `backend/api/auth.py` | INFRASTRUCTURE | Trace middleware, identity and authorization dependencies. |
| Goals | `backend/api/goals.py`, `backend/services/goal_service.py`, `backend/data/goal_repository.py`, `backend/engines/goal/*` | KEEP-CANDIDATE | Trace route → service → engine → repository; detect duplicate calculations and old goal paths. |
| Financial State | `backend/api/financial_state.py`, `backend/services/financial_state_service.py`, `backend/engines/financial_state/engine.py`, `backend/data/financial_state_repository.py` | KEEP-CANDIDATE / DUPLICATION-RISK | Trace authoritative snapshot creation, reads, derived facts and all alternative financial-data paths. |
| MoneyWheel | `backend/api/moneywheel.py`, `backend/services/moneywheel_service.py`, `backend/engines/moneywheel/*`, `backend/rules/moneywheel.py`, `backend/data/moneywheel_repository.py` | KEEP-CANDIDATE / CONFLICT-RISK | Trace all 9 ratio inputs, outputs, classification, persistence, UI contract and consumers. |
| Canonical calculations | `backend/engines/calculation/canonical.py`, `backend/engines/calculation/engine.py`, `backend/engines/calculation/__init__.py` | KEEP-CANDIDATE | Find every local duplicate formula and verify all consumers use the intended canonical function. |
| Constraints | `backend/engines/constraints/*`, `backend/rules/constraints.py`, `backend/rules/canonical.py`, `backend/engines/rules/*` | CONFLICT-RISK | Identify duplicate rule definitions, threshold authorities, adapters, evaluators and execution effects. |
| Strategy decision | `backend/engines/strategy/*`, `backend/rules/strategy_decision.py`, `backend/services/strategy_service.py` | KEEP-CANDIDATE / CONFLICT-RISK | Trace authoritative selection path; inspect applicability, eligibility, decision, ranking, recommendation, scenario and variant selection order. |
| Strategy catalogue | `backend/library/strategies/*` | DUPLICATION-RISK | Trace registry/catalog imports and runtime IDs; identify legacy aliases and definitions no active path consumes. |
| Technique execution | `backend/engines/technique/*`, `backend/library/strategies/techniques*.py` | DUPLICATION-RISK | Verify one authoritative technique registry and execution path. |
| Multi-goal planning | `backend/services/multi_goal_planning_service.py`, `backend/engines/orchestration/*`, `backend/engines/allocation/*` | DUPLICATION-RISK | Trace resource allocation, orchestration and action-plan handoff; identify overlapping allocators. |
| Action Plan | `backend/api/action_plan.py`, `backend/services/action_plan_service.py`, `backend/engines/action_plan/*`, `backend/data/action_plan_repository.py` | KEEP-CANDIDATE | Trace plan creation, version/state transitions, execution updates and impact/revalidation path. |
| Reports | `backend/services/goal_report_service.py`, `backend/services/basket_report_service.py`, `backend/services/summary_report_service.py`, `backend/report_engine/*` | DUPLICATION-RISK | Compare report generators/renderers and callers; determine which outputs are live. |
| Investor profile / risk | `backend/engines/profile/*`, `backend/engines/risk_profiler/*`, `backend/services/profile_service.py` | DUPLICATION-RISK | Trace whether profile/risk logic is duplicated or split between old and current engines. |
| Strategy versioning/editing | `backend/api/strategy_edit.py`, `backend/api/strategy_version.py`, `backend/services/strategy_edit_service.py`, `backend/services/strategy_version_service.py`, related repositories/models | KEEP-CANDIDATE / VERIFY-USAGE | Trace current version authority, accepted state, edit lifecycle and callers. |
| Persistence / schema | `backend/data/*`, `backend/models/*`, `backend/schemas/*`, `supabase/migrations/*` | INFRASTRUCTURE | Check live imports, table references, migrations and deployed schema before any removal. |
| Frontend | `frontend/*` | VERIFY-USAGE | Trace pages → API clients → backend endpoints and identify orphan pages/components. |
| Tests | `backend/tests/*`, engine-local tests | TEST-ONLY | Map each test to retained behavior; detect duplicate/stale tests, but preserve regression coverage. |
| CI / deployment | `.github/workflows/*`, Dockerfiles, run scripts | INFRASTRUCTURE | Verify active deployment paths and workflow references before editing. |

---

## 4. High-Priority Overlap Register

These are **code-inspection targets**, not automatic deletion decisions.

### SYS-01 — Calculation Ownership

```text
backend/engines/calculation/canonical.py
├── Shared calculation functions
└── DerivedFact builders

Compare all consumers / possible duplicates:
├── backend/rules/financial_state.py
├── backend/rules/financial_metrics.py
├── backend/engines/constraints/evaluator.py
├── backend/services/financial_plan_service.py
├── backend/engines/risk_profiler/*
└── backend/engines/moneywheel/*
```

**Action:** Search each formula, trace every call site, then assign one owner per shared calculation. Do not delete domain-specific transformations unless equivalence is proven.

### SYS-02 — Rule and Constraint Ownership

```text
Rule-related code
├── backend/rules/canonical.py
├── backend/rules/constraints.py
├── backend/rules/eligibility.py
├── backend/rules/financial_state.py
├── backend/rules/financial_metrics.py
├── backend/rules/moneywheel.py
├── backend/rules/strategy_decision.py
├── backend/engines/rules/engine.py
└── backend/engines/constraints
    ├── adapters.py
    ├── evaluator.py
    ├── aggregator.py
    ├── policy.py
    └── models.py
```

**Action:** Build a rule-ID → definition → evaluator → policy → consumer map. Flag duplicate IDs, duplicate thresholds and multiple components able to mutate priority or choose a strategy. Remove only after identifying the runtime authority.

### SYS-03 — Strategy Decision Pipeline

```text
Strategy-related code
├── backend/engines/strategy/applicability.py
├── backend/engines/strategy/eligibility.py
├── backend/engines/strategy/decision.py
├── backend/engines/strategy/ranking.py
├── backend/engines/strategy/comparison.py
├── backend/engines/strategy/recommendation.py
├── backend/engines/strategy/scenario.py
├── backend/engines/strategy/variant_selector.py
├── backend/engines/strategy/composition.py
├── backend/engines/strategy/engine.py
├── backend/services/strategy_service.py
└── backend/api/strategy.py
```

**Action:** Trace the actual call sequence from API to response. Identify duplicate selection/recommendation logic, unreachable branches, legacy IDs and functions called before the authoritative decision.

### SYS-04 — Strategy Definitions and Registries

```text
backend/library/strategies
├── canonical.py
├── catalog.py
├── registry.py
├── variants.py
├── components.py
├── solution_matrix.py
├── techniques.py
└── techniques_canonical.py

Compare with:
├── backend/engines/strategy/components/registry.py
├── backend/engines/strategy/components/definitions.py
├── backend/engines/strategy/components/compatibility.py
└── backend/engines/technique/engine.py
```

**Action:** Inventory every Strategy / Variant / Technique / Component ID, where it is registered, and which runtime path reads it. Remove duplicate definitions only after ID and compatibility contracts are reconciled.

### SYS-05 — Goal Calculation and Funding Paths

```text
backend/engines/goal
├── engine.py
├── target_calculator.py
├── asset_projection.py
├── funding_gap.py
├── funding_strategies.py
└── specialized.py

Compare consumers:
├── backend/services/goal_service.py
├── backend/services/financial_plan_service.py
├── backend/services/goal_report_service.py
└── backend/services/multi_goal_planning_service.py
```

**Action:** Trace each goal calculation from entry point to output. Identify repeated future-target, projection, funding-gap, contribution and feasibility calculations. Keep specialized goal logic if it adds a genuinely distinct requirement.

### SYS-06 — Orchestration and Allocation

```text
backend/engines/orchestration
├── engine.py
└── models.py

backend/engines/allocation
├── engine.py
└── models.py

backend/services
├── planning_orchestration_service.py
└── multi_goal_planning_service.py
```

**Action:** Compare inputs, outputs and callers to determine whether these are distinct layers or overlapping orchestration/allocation paths. Do not merge based on naming alone.

### SYS-07 — Reports and Renderers

```text
backend/services
├── goal_report_service.py
├── basket_report_service.py
├── summary_report_service.py
└── summary_report_renderer.py

backend/report_engine
├── configs.py
├── models.py
└── renderer.py
```

**Action:** Trace API endpoints and UI actions to each generator. Identify unused report paths, repeated rendering responsibilities and shared output contracts.

### SYS-08 — Profile / Risk Ownership

```text
backend/engines/profile
├── engine.py
├── behavioral.py
├── identity.py
├── constraints.py
├── risk.py
└── strategy_context.py

backend/engines/risk_profiler
├── engine.py
├── models.py
└── risk.py

Compare:
├── backend/services/profile_service.py
├── backend/rules/risk_profiler.py
└── backend/engines/suitability/engine.py
```

**Action:** Establish whether each module owns distinct data or repeats profiling, risk scoring, suitability or strategy context. Verify imports/callers before deprecation.

---

## 5. Tests as Runtime Evidence

The repository contains tests for calculations, MoneyWheel, constraints, goals, strategies, versions, reports, action plans and integrations. Tests show intended or historically asserted behavior; they do not alone prove that production code calls that path.

Priority test groups to map to production callers:

- `backend/tests/test_canonical_calculations.py`
- `backend/tests/test_financial_calculations.py`
- `backend/tests/test_financial_ratio_constraints.py`
- `backend/tests/test_canonical_constraints_layer.py`
- `backend/tests/test_moneywheel.py`
- `backend/tests/test_moneywheel_api.py`
- `backend/tests/test_goal_calculations.py`
- `backend/tests/test_goal_feasibility_prerequisites.py`
- `backend/tests/test_multi_goal_orchestrator.py`
- `backend/tests/test_strategy_decision_authority.py`
- `backend/tests/test_strategy_engine.py`
- `backend/tests/test_strategy_run.py`
- `backend/tests/test_strategy_version_authority.py`
- `backend/tests/test_action_plan_lifecycle.py`
- `backend/tests/test_remaining_implementation_gaps_closure.py`

**Required outcome:** every retained business-critical test maps to a real runtime path; tests for removed behavior are updated or removed in the same change; no test is deleted merely to make the suite pass.

---

## 6. Per-Item Register Template

Create one row per function, class, rule ID, endpoint, model/schema, registry entry, migration and frontend API consumer.

| Field | Required evidence |
|---|---|
| Item ID | Stable cleanup ID |
| Symbol | Exact file + function/class/constant/rule/route |
| Direct callers | Imports and call sites |
| Runtime reachability | Entry point and call path, or evidence it is not reachable |
| Responsibility | What the code actually computes or changes |
| Inputs / outputs | Actual types and contracts |
| Overlap | Other symbols with the same responsibility |
| Tests | Tests that exercise this exact behavior |
| External dependency | API, database, migration, scheduled job or frontend usage |
| Classification | KEEP-CANDIDATE / VERIFY-USAGE / DUPLICATION-RISK / CONFLICT-RISK / TEST-ONLY / INFRASTRUCTURE |
| Decision | Keep / merge / replace / delete / investigate |
| Evidence | Search results, call sites and test output |
| Verification | Tests run and result |
| Change commit | Commit that implements the approved cleanup |

---

## 7. Deletion Gate

An item can be marked **DELETE-READY** only when all applicable checks are complete:

```text
Exact symbol identified
    ↓
All direct and dynamic callers searched
    ↓
Entry points / API registration checked
    ↓
Frontend / schema / migration / job references checked
    ↓
Overlapping implementation identified (if any)
    ↓
Replacement owner selected (if required)
    ↓
Tests mapped and updated
    ↓
Targeted tests pass
    ↓
Regression suite passes
    ↓
Deletion approved
```

If any dependency is unknown, status remains **VERIFY-USAGE**. Absence from a simple text search is not proof of unused code.

---

## 8. Initial Priority Order

1. **P0 — Entry points:** `backend/main.py`, router registration, frontend API clients, deployed routes.
2. **P1 — Shared calculation duplicates:** canonical calculation functions and all callers.
3. **P1 — Rule / constraint overlap:** rule IDs, thresholds, evaluator, policy and downstream effects.
4. **P1 — Strategy decision authority:** selection, eligibility, ranking, recommendation and scenario call graph.
5. **P2 — Registries and legacy identifiers:** strategies, variants, components, techniques.
6. **P2 — Goal and feasibility duplication:** goal engine, services, reports and multi-goal paths.
7. **P2 — Orchestration / allocation overlap.**
8. **P3 — Report generation and renderer overlap.**
9. **P3 — Profile / risk / suitability overlap.**
10. **P4 — Orphan tests, stale helpers and cleanup of low-risk unused code.**

This order prioritizes shared decision logic before cosmetic cleanup.

---

## 9. Audit Boundary

This register is based on repository code structure and code-search evidence. It is **not yet a complete symbol-by-symbol call graph** for all 557 files. No code has been classified as safe to delete solely from the initial tree. The next audit pass must populate the per-item register with exact callers, runtime reachability and test evidence before any deletion batch.
