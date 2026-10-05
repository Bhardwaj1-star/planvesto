This document defines the current domain/layer boundaries for Planvesto's financial-planning system. The layer map is anchored to the implemented frontend and backend code. The reference model for this map is the layer structure represented by this document; other documentation is not used as evidence for the code audit.

**Canonical / Centralized Data column:** **Yes** = the layer has an identifiable authoritative persisted/registry source used downstream; **Partial** = a central output/source exists but the layer still recomputes, combines, or duplicates part of the data; **No** = the layer primarily derives/orchestrates/presents data owned by other layers and has no separate canonical data authority.

## Layer Map

| # | Layer | What it is | Purpose | Primary data source | Canonical / Centralized Data | Decision Output | Upstream Dependencies | Downstream Consumers | Rule / Policy Ownership | Implementation Maturity | Current Problems / Gaps | Conflicts / Overlaps |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Onboarding / Financial Inputs | Customer source-input layer | Collect customer's financial picture | Personal/family/income/expense/asset/insurance/liability/goal inputs | **Yes** — persisted source records. | Validated customer financial inputs | User/source inputs | Financial State, Profile/Risk, Budgeting, Goal Planner | Input schemas + persistence/API validation | **Implemented** | Raw inputs are authoritative, but downstream freshness depends on FinancialState rebuild/snapshot usage. | No direct layer conflict identified; multiple downstream consumers correctly depend on this source layer. |
| 2 | Financial State | Authoritative current-state aggregate | Represent current financial position | Persisted financial records | **Yes** — FinancialStateService + snapshots. | Current FinancialState + snapshot | Onboarding/source records | Calculations, MoneyWheel, Constraints, Profile/Risk, Goals, Planning | FinancialStateEngine + FinancialStateService | **Implemented / authoritative** | Snapshot freshness must remain tied to the current raw input revision; otherwise downstream consumers can read stale derived state. | Freshness/lineage can conflict with consumers selecting an older snapshot; the risk is temporal authority, not competing domain ownership. |
| 3 | Financial Calculations / Measures | Canonical calculation layer | Derive standardized measures | Current FinancialState | **Yes** — canonical.py centralizes shared calculations. | Canonical ratios/measures | FinancialState | Health, MoneyWheel, Constraints, Planning, Reports | canonical calculation module | **Implemented / canonical** | Some downstream services still contain local formula implementations instead of consuming the canonical calculation output. | **FinancialPlanService vs canonical calculations**: duplicate DTI and emergency-coverage calculations create competing calculation authority. |
| 4 | Financial Health | Financial-condition assessment | Assess strengths, weaknesses, risks, conditions | FinancialState + canonical metrics | **No** — derived across existing modules. | Health/condition assessment | FinancialState + calculations | MoneyWheel, Constraints, planning/reports | Distributed diagnostic rules; no standalone owner | **Implemented / derived** | No standalone health authority means the assessment remains distributed and can be assembled differently by different consumers. | **Financial Health vs MoneyWheel/Constraints** can overlap when diagnostic thresholds are treated as health decisions rather than module-specific policy. |
| 5 | MoneyWheel | Financial diagnostic framework | Measure financial health via ratios/coverage | FinancialState + calculations + relevant context | **Partial** — snapshots/results exist but shared facts remain upstream-owned. | Diagnostic ratios/status/explanations | FinancialState + calculations | Constraints, planning, reports | MoneyWheel rules/engine | **Implemented / diagnostic** | Compatibility/legacy ratio surfaces and shared diagnostic formulas need to remain subordinate to canonical calculations. | **MoneyWheel vs Constraints** overlap on financial-ratio evaluation; same metric can be calculated/graded in both diagnostic and constraint paths. |
| 6 | Constraints / Rules | Decision-control layer | Identify limits, warnings, hard constraints | FinancialState + metrics + rule definitions | **Partial** — ConstraintAggregator centralizes output, evaluator still overlaps rules. | Constraints, warnings, overrides, conflicts | FinancialState + calculations + MoneyWheel + risk/strategy | Strategy, Multi-Goal, allocation | ConstraintAggregator + rule modules + evaluator | **Implemented / centralized output path** | ConstraintSet is now the single downstream constraint contract; MultiGoalPlanningService no longer evaluates ratios separately and then re-aggregates them. FinancialRatioConstraintEvaluator remains an internal evaluator owned by ConstraintAggregator, while rule modules remain policy/diagnostic sources. | ConstraintAggregator is the single downstream authority for ConstraintSet creation. FinancialRatioConstraintEvaluator is an internal implementation detail of that boundary; other rule engines may provide rule assessments, but consumers should not construct competing ConstraintSets. |
| 7 | Investor Profile / Risk | Suitability/risk/behavioral decision context | Build downstream decision context | Profile inputs + FinancialState + risk evidence | **Yes** — profile/risk outputs are versioned/persisted. | Profile + RiskProfile/risk boundary | FinancialState + profile inputs | Investment foundation, Strategy, Constraints, approval | Profile/Risk engines + rules | **Implemented / versioned** | Suitability is only rules-ready; investment policy mapping is not fully operationalized from the risk boundary. | **Profile/Risk vs legacy/adapter risk surfaces** can duplicate the same RiskProfiler functionality; no separate top-level ownership should emerge. |
| 8 | Budgeting | Cash-flow control layer | Set limits and compare spending vs budget | Expenses + liabilities + budget_limits | **Partial** — limits persist; no single canonical budget-vs-actual aggregate. | Budget limits + budget/actual view | Financial inputs + FinancialState + user settings | Financial review/planning | Budget persistence/API + budgeting calculations | **Implemented / partial aggregate** | There is no single persisted aggregate that owns the complete budget-vs-actual state. | **Budgeting vs FinancialState** must remain separated: budget limits are policy/settings while actual financial facts belong to FinancialState. |
| 9 | Goal Planner | Individual-goal planning layer | Define goals, requirements, funding gap/contribution, feasibility | Goal inputs + DefinedGoal + FinancialState + mapped assets | **Yes** — goal records + versioned DefinedGoal snapshots. | DefinedGoal + target/funding/feasibility | FinancialState + goal inputs + assumptions | Goal Basket, Strategy, Multi-Goal, Reports | Goal rules + goal engines + GoalService | **Implemented / versioned** | Goal planning is implemented, but downstream multi-goal layers use additional status/priority representations that must stay semantically aligned. | **DefinedGoal funding status vs Multi-Goal allocation/orchestration funding status** uses different vocabularies; feasibility vocabulary also differs across planning components. |
| 10 | Goal Basket | Logical goal-grouping layer | Group goals for combined planning/reporting | Existing goals + GoalBasket request | **No** — current API is preview/summary; no dedicated basket persistence authority. | Basket summary/counts/contribution/gap | Goal records/DefinedGoals | Multi-Goal/reporting | GoalBasketEngine + service | **Implemented / runtime grouping** | No persisted basket authority; basket is a runtime grouping/summary surface. | **Goal Basket vs Goal Planner** must remain grouping vs individual-goal ownership; no direct data-authority conflict identified. |
| 11 | Strategy Builder / StrategyRun | Strategy decision/evaluation layer | Filter, compare, rank, recommend strategies/scenarios | DefinedGoal + FinancialState + priorities + constraints/risk | **Yes** — StrategyRun is persisted. | Candidates, scenarios, rankings, recommendation, feasibility | Goals + FinancialState + Profile/Risk + Constraints | StrategyVersion, Complete Plan, Action Plan | Strategy rules + engines + StrategyService | **Implemented / evaluated** | Investment allocation policy is not completed here; StrategyRun should not silently become the owner of product allocation rules. | **Strategy feasibility vocabulary vs allocation/orchestration feasibility vocabulary** differs (`conditional` vs `constrained`). |
| 12 | Strategy Version / Primary Strategy | Strategy governance layer | Persist immutable versions and current primary strategy | StrategyRun + selection + approval | **Yes** — StrategyVersion + PrimaryStrategyState. | Approved/primary strategy configuration | StrategyRun + selection + approval | Action Plan, execution, diary/history | Version lifecycle + PrimaryStrategyState | **Implemented / governed** | Strategy identity is strong, but downstream action lineage is partly indirect through StrategyVersion. | **StrategyRun vs StrategyVersion** are intentionally distinct; conflict occurs only if consumers treat an evaluation run as the active strategy authority. |
| 13 | Planning Orchestration | Workflow/context coordination | Assemble state/goals/strategy/readiness context | FinancialState + goal versions + StrategyVersion/context | **No** — runtime context, not domain authority. | Planning context/readiness | Multiple canonical authorities | Multi-Goal, Complete Plan | Orchestration engine/service | **Implemented / runtime** | Orchestration models duplicate some goal-evaluation/allocation field structures, increasing translation overhead and contract drift risk. | **Orchestration vs Resource Allocation** overlap in goal resolution/allocation fields; both carry related priority/funding representations. |
| 14 | Multi-Goal Planning | Cross-goal planning layer | Coordinate priorities, resources, conflicts, trade-offs | Goals + DefinedGoals + FinancialState + StrategyVersions + constraints | **No** — in-memory plan; no canonical persisted multi-goal entity. | Goal resolutions, trade-offs, funding status | Goals + strategies + FinancialState + Constraints | Resource Allocation, Complete Plan | MultiGoalOrchestrator + constraint integration | **Implemented / runtime planning** | Priority, funding-status, and feasibility contracts are not fully uniform across multi-goal, allocation, and goal/strategy models. | **Multi-Goal Planning vs Resource Allocation** both represent goal allocation/resolution data; priority ranks and funding statuses can diverge. |
| 15 | Resource Allocation | Cross-goal allocation engine | Allocate resources and produce funding outcomes | Goals + priorities + resources + constraints | **No** — derived engine result. | Per-goal allocation, shortfall, priority resolution | Multi-Goal inputs + constraints + surplus | Complete Plan, actions | Allocation engine/rules | **Implemented / derived** | Allocation is deterministic priority-based allocation, not an independent persisted optimization authority; contract normalization is still needed. | **Allocation vs Orchestration priority ranks** differ in numeric indexing/defaults; allocation/orchestration funding and feasibility vocabularies also differ from goal/strategy contracts. |
| 16 | Complete Financial Plan | Cross-domain consolidation layer | Consolidate position, goals, funding, strategy, constraints, actions, trajectory | FinancialState + goals + StrategyVersions + planning/allocation outputs | **No** — live response/PDF; no canonical plan state. | Consolidated plan/report | Major planning authorities | Dashboard, reports, user review | FinancialPlanService; contains local derived scans | **Implemented / consolidation; cleanup needed** | Local derived financial scans can diverge from canonical calculations; the consolidated plan is therefore not a safe second calculation authority. | **FinancialPlanService vs canonical calculation layer/MoneyWheel**: duplicate DTI and emergency-coverage formulas. This is a direct calculation conflict. |
| 17 | Action Plan | Execution layer | Convert approved strategy into executable actions | Approved current StrategyVersion | **Yes** — ActionPlanItem + decision records persist. | Executable actions + lifecycle | StrategyVersion + planning context | Execution/Impact, Diary, history | Action generator + ActionPlanService | **Implemented / executable** | Action-to-goal linkage is indirect through StrategyVersion, and execution impact intelligence is still incomplete. | **Action Plan vs StrategyVersion** is a dependency, not a conflict; the main risk is indirect lineage rather than competing authority. |
| 18 | Execution / Impact Update | Outcome/state-update layer | Capture completion and compare projected vs actual | Action completion + actual FinancialState snapshot | **Yes** — actual snapshots + action decision/impact records persist with lineage. | Projected-vs-actual variance + updated state | ActionPlan + FinancialState authority | Replanning, Dashboard/History, Diary | ActionImpactEngine + FinancialStateService | **Implemented / impact intelligence partial** | Projected-vs-actual variance exists, but materiality and cause attribution are intentionally not determined without configured rules/source data. | **Execution audit vs FinancialState snapshot lineage** needs to stay synchronized; actual impact without a clearly linked snapshot can weaken traceability. |
| 19 | Replanning | Continuous planning layer | Reassess when goals/profile/financial state changes | Updated FinancialState + goals/profile + strategy context | **No** — workflow over existing authorities. | Recomputed planning context/downstream decisions | Updated canonical state | Strategy, Multi-Goal, Complete Plan, Actions | Existing downstream engines/services | **Implemented / workflow** | No dedicated replanning state exists, so correctness depends on all downstream consumers reading current canonical state/version context. | **Replanning vs Strategy/Goal/FinancialState** is intentionally cross-cutting; stale versions can create inconsistent recomputation if lineage is not enforced. |
| 20 | Financial Memory / Investor Diary | User-authored financial context | Persist notes and decision context across cycles | DiaryEntry + FinancialDecision + module histories | **Yes** — diary entries/decisions persist; system decisions read authoritative histories. | User notes + historical decision context | Planning/execution/approval histories + user input | Review + future planning context | DiaryService/repository | **Implemented / persistent context** | System decisions are referenced from other authorities rather than copied into diary data; completeness depends on those source histories. | **Diary vs canonical domain state**: must remain contextual/history storage, not a competing FinancialState or strategy authority. |
| 21 | Dashboard / Reports / History | Presentation/historical-review layer | Present consolidated outputs and historical views | Canonical outputs + historical records | **No** — consumes canonical data/history. | Review views + reports | FinancialState + goals + strategy/actions/history | Investor review | Dashboard/report services; no domain-rule ownership | **Implemented / presentation** | Presentation surfaces inherit any upstream calculation, vocabulary, or freshness inconsistency; they do not resolve those problems themselves. | **Reports vs underlying domain layers** should remain read-only/presentation; duplication becomes a conflict only if report services recalculate authoritative metrics. |
## Code-Verified Layer Boundaries

- FinancialState != FinancialHealth != MoneyWheel != Constraints.
- Investor Profile / Risk is a composite decision-context layer. The backend has ProfileEngine/ProfileService, a dedicated RiskProfilerEngine with RiskProfile and the dimensions risk_required, risk_capacity, and risk_tolerance, plus behavioral and identity profile components.
- Behavioral Profile is implemented as an internal component of the profile/risk context through engines/profile/behavioral.py and BehavioralRules; it is not a separate top-level layer.
- Suitability is not a separate completed layer. SuitabilityEngine exists as a rules-ready assessment boundary, but the code does not expose a separate end-to-end suitability planning workflow comparable to the 21 layers.
- Investment Engine is not a separate top-level layer yet. engines/investment/engine.py and its models exist, but the current frontend/backend surface does not establish an independent end-to-end investment-planning layer with its own user workflow/API authority.
- Insurance / Protection is not a separate top-level layer. Insurance has onboarding data/model/API and policy-PDF extraction, but it currently participates as financial input/protection context rather than an independent planning workflow.
- Scenario Planning is part of Strategy Builder / StrategyRun. Strategy scenario UI and backend scenario logic exist, but do not constitute a separate domain layer.
- Goal Feasibility is part of Goal Planner. The frontend has a dedicated feasibility view, while the backend goal engine owns the calculations.
- Reports are part of Dashboard / Reports / History. Goal reports, basket reports, summary reports, and the complete-plan renderer are reporting outputs rather than independent planning layers.
- PlanningUnit is a root planning context/entity, not a user-facing computational layer.
- Strategy techniques/components are internal strategy mechanisms, not separate top-level layers.
- Decision/audit trace is a cross-cutting governance concern around execution/history, not a separate planning layer.

## Responsibility Boundaries

- FinancialState is the authoritative current financial position.
- Financial Health is an assessment of that position.
- MoneyWheel is the diagnostic framework built from canonical financial metrics and coverage rules.
- Constraints are decision controls evaluated from financial evidence and rule definitions.
- Budgeting controls spending limits/variance; it does not replace FinancialState or MoneyWheel.
- Goal Planner defines/version individual goals; Goal Basket groups existing goals and does not replace them.
- StrategyRun records a strategy evaluation run; it is not the same thing as the current StrategyVersion.
- StrategyVersion is immutable strategy configuration; PrimaryStrategyState identifies the current primary strategy authority.
- Planning Orchestration coordinates workflow context; it does not become the owner of the underlying financial or strategy data.
- Multi-Goal Planning coordinates cross-goal decisions; Resource Allocation performs the concrete allocation calculation.
- Complete Financial Plan consolidates domain outputs; it does not own the underlying canonical calculations or strategy identity.
- Action Plan executes an approved current strategy; execution updates the authoritative financial state for the next planning cycle.
- Financial Memory / Investor Diary stores user-authored notes and decision context; it is not an authoritative FinancialState, strategy authority, or calculated financial-history substitute.
- Dashboard / Reports / History presents and reviews canonical outputs; it does not become the owner of those outputs.

## High-Level Data Flow

Financial Memory / Investor Diary is a review/context layer rather than a mandatory computational step, so it is shown as cross-cutting around the planning cycle:

Customer Inputs
    ↓
Financial State
    ↓
Canonical Calculations
    ↓
Financial Health / MoneyWheel / Constraints
    ↓
Investor Profile / Risk + Budgeting
    ↓
Goal Planner
    ↓
Goal Basket (when grouping goals)
    ↓
Strategy Builder / StrategyRun
    ↓
StrategyVersion + Primary Strategy
    ↓
Planning Orchestration
    ↓
Multi-Goal Planning
    ↓
Resource Allocation
    ↓
Complete Financial Plan
    ↓
Action Plan
    ↓
Execution / Actual Outcome
    ↓
Updated Financial State
    ↺

Financial Memory / Investor Diary
    ↕
Planning and review cycles

## Frontend / Backend Implementation Evidence

- Onboarding: frontend onboarding routes cover personal information, family/dependents, income, expenses, assets, insurance, liabilities, and goals.
- Financial State: financial_state API/service/model/engine provide the authoritative current-state path.
- Calculations: engines/calculation/canonical.py and the calculation engine provide canonical measures consumed downstream.
- MoneyWheel: dedicated frontend page plus backend API/service/engine.
- Constraints: dedicated constraint engine with evaluator, aggregator, adapters, and models.
- Profile / Risk: ProfileEngine, ProfileService, /api/profile, engines/risk_profiler/, RiskProfile, and profile history/latest APIs.
- Budgeting: dedicated frontend investor budgeting page and budget persistence/API/types.
- Goal Planner: goal frontend routes, goal API/service/model, and goal engines including target, funding-gap, asset-projection, and specialized calculations.
- Goal Basket: GoalBasket model, service, engine, API, and basket reporting.
- Strategy Builder / StrategyRun: strategy frontend routes plus strategy service/API and strategy engines for applicability, eligibility, composition, comparison, decision, ranking, recommendation, and scenarios.
- Strategy Version / Primary Strategy: StrategyVersion model/service/API plus PrimaryStrategyState and its repository/persistence.
- Planning Orchestration: orchestration frontend/backend context and service/API.
- Multi-Goal Planning: multi-goal planning service plus allocation/rules integration.
- Resource Allocation: ResourceAllocationEngine and allocation result models.
- Complete Financial Plan: FinancialPlanService and summary/report rendering surface.
- Action Plan / Execution: action-plan frontend/API/service/model plus impact engine and completion/update flow.
- Replanning: implemented through goal/profile/financial-state changes feeding downstream recalculation and strategy context.
- Financial Memory / Investor Diary: frontend /investor/diary, backend diary API/service/repository/model/schema, plus DiaryEntry and FinancialDecision.
- Dashboard / Reports / History: dashboard, reports, goal-history, and strategy-history frontend routes with corresponding backend reporting services/APIs.

## Code-Audit Conclusion

Using only the frontend and backend folders as implementation evidence, the current architecture has 21 top-level layers.

No additional candidate was found that satisfies all three conditions for a separate top-level layer:
1. a distinct domain responsibility,
2. a distinct implemented backend capability, and
3. a distinct frontend/end-user workflow or authoritative system surface.

The main candidates that fail this test are Investment Engine, Suitability, Insurance/Protection, Behavioral Profile, Scenario Planning, Goal Feasibility, Reports, PlanningUnit, Strategy Techniques, and Decision/Audit Trace. They are implemented components or sub-capabilities, but not additional top-level layers.

This conclusion is intentionally code-first and does not infer a layer merely from a folder, class, route, or documentation concept in isolation.