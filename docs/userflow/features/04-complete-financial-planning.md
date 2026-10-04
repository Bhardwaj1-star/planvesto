# Complete Financial Planning

## Blueprint vs Current Feature — Summary

| Area | Blueprint / System Requirement | Current Feature Document / Code | Status |
|---|---|---|---|
| Financial planning purpose | Dynamic financial decision engine: state → goals → constraints → action/problem → strategies → calculations → scenarios → optimization → decision → updated state | Complete Financial Planning consolidates current state, goals, constraints, selected StrategyVersions, allocation, trade-offs, actions and evidence | **Available / implemented** |
| Financial State | Authoritative current financial state and feedback into updated state | FinancialStateService is the current authority; plan consumes it | **Available / implemented** |
| Goals | Goals define desired outcomes; goal engine owns goal requirements | Goal Planner owns goal identity/calculation; complete plan consumes goal outputs | **Available / implemented** |
| Goal Funding | Explicit goal funding requirements and cross-goal funding | Goal requirements + consolidated funding + resource allocation + per-goal funding view | **Available / implemented** |
| Constraints | Constraints reduce strategy search space and govern decisions | Constraint evaluation + canonical ConstraintSet + overrides + audit trail | **Available / implemented; canonicalization gaps remain** |
| Proposed Action / Problem | Explicit input to the decision-engine workflow | Plan exposes action requirements, but proposed-action/problem → planning workflow is not a first-class Complete Financial Planning input | **Partially available** |
| Strategy Engine | Generate financially meaningful alternative paths | Strategy Builder owns strategy evaluation/finalization; Complete Plan represents selected StrategyVersion(s) | **Available by boundary; not owned here** |
| Calculation Engine | Calculate mathematical consequences of strategies/actions | Goal calculations and canonical financial calculations exist in upstream authorities; plan aggregates their outputs | **Available by boundary; not owned here** |
| Scenario Engine | Test strategies under changing conditions | Complete plan has contingency matrix and trajectory, but no dedicated scenario engine is represented in this feature | **Partial / missing as dedicated capability** |
| Probability / Uncertainty | Explicit uncertainty/probability layer | No dedicated probability/uncertainty capability is represented in the current feature document | **Not yet represented** |
| Optimization | Compare multiple strategies using fit, liquidity, debt, risk, flexibility, outcome quality and trade-offs | Multi-goal orchestration allocates shared resources and exposes trade-offs; strategy optimization remains upstream | **Partial / boundary exists** |
| Explainability | Explain why options/decisions were produced | Reasons, notes, trade-offs, constraint evidence and audit trail are exposed | **Partially available** |
| Decision | Investor decides among evaluated options; system should not silently decide for investor | StrategyVersion selection/approval is upstream; Complete Plan consolidates finalized decisions | **Available by boundary** |
| Updated Financial State / Feedback Loop | Decision/execution updates state and feeds the next planning cycle | Action Plan and FinancialState authorities define this boundary; Complete Plan itself does not own execution/state mutation | **Available by boundary** |
| Assumptions | Assumptions are explicit model inputs and should not be hidden | Fixed 9% trajectory assumption exists and is explicitly documented as a gap; assumption model is not first-class here | **Partial / gap** |
| Common Data Model | Investor, Financial State, Asset, Liability, Goal, Goal Funding, Constraint, Assumption, Action, Strategy, Scenario, Validation, Decision, Audit | Most appear through existing feature/domain authorities; no single Complete Financial Planning data-model owner | **Available by composition / not centralized here** |
| Audit | Decision/audit history and traceability | Constraint aggregation audit evidence and strategy lineage are exposed | **Partially available** |
| No arbitrary universal return | Required return should be derived; no arbitrary universal 10% assumption | Current trajectory helper uses fixed 9% return assumption and is explicitly flagged as non-canonical | **Known gap** |
| Cross-goal consolidation | Whole financial plan should integrate goals, funding, constraints and trade-offs | Core purpose of this feature; multi-goal orchestration + consolidated output | **Implemented** |
| Plan snapshot / versioning | Blueprint implies decision/history feedback but does not specify this feature's exact persistence model | Current plan is live; no dedicated immutable Complete Financial Plan version/snapshot | **Not yet implemented** |
| Rendering / report | Outputs can feed decision/explainability/reporting | Planning data contract exists; rendering remains a presentation layer | **Available by boundary** |

### Summary

**Blueprint coverage:** The current Complete Financial Planning feature covers the core cross-goal planning/consolidation layer and connects the Blueprint's Financial State, Goals, Constraints, Strategy, Calculation, Decision and Audit concepts through their existing authorities.

**What is already available:** cross-goal consolidation, goal funding, current StrategyVersion lineage, constraint evaluation/aggregation, resource allocation, trade-offs, plan-level action requirements, financial trajectory, contingency/governance evidence, and audit/provenance.

**What is only partial or remains to be built:** first-class Proposed Action/Problem flow, dedicated Scenario Engine, Probability/Uncertainty layer, first-class Optimization/explainability boundaries, explicit Assumption model, immutable plan snapshot/versioning, and removal of the fixed 9% trajectory assumption.

**Important boundary:** These gaps do not mean all of them belong inside `04-complete-financial-planning.md`. The feature should consume or orchestrate the appropriate system-level engines rather than duplicate their ownership.


## 1. Feature Scope

Complete Financial Planning is the system-level feature that consolidates the investor's current financial state, all active goals, goal funding requirements, financial constraints, selected strategy versions, resource allocation, trade-offs, action requirements, and planning evidence into one coherent financial plan.

It is the cross-goal planning layer. It does not replace Goal Planner, Financial Health & Rules, Strategy Builder, or Strategy → Action Plan.

```text
Financial State
    +
Goals / DefinedGoals
    +
Current StrategyVersions
    +
Constraints / Financial Rules
    ↓
Multi-Goal Planning
    ↓
Complete Financial Plan
    ├── Financial position
    ├── Goal portfolio
    ├── Consolidated funding
    ├── Resource allocation
    ├── Strategy summary
    ├── Constraints
    ├── Trade-offs
    ├── Action plan
    ├── Cash-flow trajectory
    ├── MoneyWheel health scan
    ├── Contingency / governance
    └── Audit evidence
```

The current implementation is a live consolidated plan. It does not introduce a separate Complete Financial Plan database table.

## 2. Feature Responsibility

The feature answers:

> "Given the investor's current financial position, goals, constraints and currently selected strategies, what is the coherent financial plan across the whole planning unit?"

It therefore combines:

- current financial position;
- all goals in the planning unit;
- each goal's funding requirement and feasibility;
- current StrategyVersion for every goal;
- shared monthly surplus;
- goal priority and allocation;
- cross-goal resource competition;
- constraints and trade-offs;
- implementation-oriented actions;
- planning trajectory and contingency evidence.

It does not independently redefine:

- goal identity;
- goal calculation formulas;
- canonical financial metrics;
- strategy identity;
- StrategyVersion authority;
- action lifecycle;
- authoritative FinancialState persistence.

## 3. User / Request Inputs

### Build complete plan

POST `/api/strategy/financial-plan/build`

Input:

- `planning_unit_id`
- optional `investor_priorities`

The route authenticates the user and verifies Planning Unit ownership before invoking `FinancialPlanService.build_plan()`.

### Get current complete plan

GET `/api/strategy/financial-plan?planning_unit_id=...`

The route:

1. authenticates the user;
2. verifies Planning Unit ownership;
3. invokes `FinancialPlanService.build_plan()`.

The current implementation therefore builds the plan live from current persisted planning inputs rather than reading a dedicated stored Complete Financial Plan snapshot.

## 4. Planning Unit Ownership

The Complete Financial Plan is scoped to the Planning Unit.

```text
Authenticated User
    ↓
Planning Unit
    ↓
Financial State
    +
Goals
    +
StrategyVersions
    ↓
Complete Financial Plan
```

The API boundary uses:

- `authenticate_user()`
- `verify_planning_unit_ownership()`

Child resources are resolved inside the planning-unit boundary.

## 5. Primary Code Ownership

### API

`backend/api/strategy.py`

Owns:

- `POST /api/strategy/financial-plan/build`
- `GET /api/strategy/financial-plan`

### Orchestration

`backend/services/financial_plan_service.py`

Owns the consolidated plan response and presentation-level aggregation.

### Multi-goal planning

`backend/services/multi_goal_planning_service.py`

Owns cross-goal evaluation orchestration.

### Multi-goal decision orchestration

`backend/engines/orchestration/engine.py`

Owns multi-goal resource allocation / orchestration decisions.

### Goal reporting

`backend/services/goal_report_service.py`

Provides the per-goal decision/report context consumed by the multi-goal planner.

### Strategy authority

`backend/data/strategy_repository.py`

Resolves the current selected StrategyVersion for each goal.

### Financial State

`backend/services/financial_state_service.py`

Owns the authoritative current FinancialState used by the financial planning pipeline.

### Constraints

`backend/engines/constraints/evaluator.py`

Evaluates financial ratio constraints.

`backend/engines/constraints/aggregator.py`

Builds the canonical ConstraintSet attached to the multi-goal plan.

## 6. Source-of-Truth Boundary

The Complete Financial Plan is an aggregation layer.

| Planning concept | Authority |
|---|---|
| Goal identity | Goal taxonomy / Goal Planner |
| DefinedGoal | Goal Planner versioned snapshot |
| Current FinancialState | FinancialStateService |
| Canonical financial formulas | canonical calculation layer |
| MoneyWheel thresholds | MoneyWheel rules |
| Financial constraints | Constraint evaluator / ConstraintAggregator |
| Current strategy | explicitly selected StrategyVersion |
| Strategy identity | canonical architecture / strategy identity |
| Cross-goal allocation | MultiGoalPlanning / orchestration |
| Action lifecycle | Action Plan |
| Actual FinancialState after completion | FinancialStateService |

The Complete Financial Plan must consume these authorities rather than create competing definitions.

## 7. Goal Collection

`MultiGoalPlanningService.build_multi_goal_plan()` starts from:

`GoalRepository.list_goals(planning_unit_id)`

If no goals exist, the current implementation returns HTTP 404.

For every goal, the service requires a current selected StrategyVersion.

```text
Planning Unit
    ↓
List Goals
    ↓
For each Goal
    ├── resolve current StrategyVersion
    ├── build goal report from StrategyVersion
    ├── extract goal calculation
    ├── extract feasibility
    └── create GoalEvaluationInput
```

A goal without a current StrategyVersion cannot currently participate in the current multi-goal plan.

## 8. StrategyVersion Requirement

Current strategy authority is explicit.

For every goal:

`StrategyRepository.get_selected_strategy_version_id(planning_unit_id, goal_id)`

must resolve a current StrategyVersion.

The plan does not use:

- latest StrategyRun as current authority;
- latest ranking as current authority;
- latest recommendation as current authority.

The StrategyVersion is the finalized strategy decision that the Complete Financial Plan is allowed to represent as current.

This preserves the Strategy Builder boundary:

```text
Strategy evaluation
    ↓
Selection
    ↓
Finalized StrategyVersion
    ↓
Complete Financial Plan
```

## 9. Per-Goal Planning Inputs

Each goal contributes:

- goal ID;
- goal name;
- goal type;
- client priority;
- target date;
- target year/month;
- today's cost;
- future target;
- funding gap;
- required monthly contribution;
- flexibility;
- projected mapped asset value;
- available monthly surplus;
- funding strategies;
- feasibility status;
- reasons / notes;
- current StrategyVersion ID;
- recommended strategy identity/name.

These values originate from the goal report and multi-goal evaluation context.

## 10. Goal Evaluation

For each goal:

```text
Goal
    ↓
Current StrategyVersion
    ↓
GoalReportService.build_report()
    ↓
Goal calculation + recommendation + feasibility
    ↓
GoalEvaluationInput
```

The Complete Financial Plan does not recalculate the goal's future target or funding gap itself.

Goal Planner remains the authority for those calculations.

## 11. Financial Context

After collecting goal inputs, the multi-goal service builds a financial context from the current planning state.

The current implementation obtains the first available latest DefinedGoal and passes it to:

`StrategyService._financial_context()`

The Planning Unit ID is then attached to that context.

This financial context is consumed by:

- FinancialRatioConstraintEvaluator;
- ConstraintAggregator;
- MultiGoalOrchestrator.

The financial context must remain derived from current authoritative financial state rather than a stale report snapshot.

## 12. Constraint Evaluation

The Complete Financial Plan evaluates cross-goal financial constraints before orchestration.

```text
GoalEvaluationInputs
        +
Financial Context
        ↓
FinancialRatioConstraintEvaluator
        ↓
Assessment
├── warnings
├── hard constraints
└── suggested overrides
```

The service then builds the canonical constraint set:

`ConstraintAggregator.aggregate(...)`

The resulting ConstraintSet is attached to the plan's audit trail.

## 13. Constraint Override Boundary

Constraint evaluation may produce suggested priority/resource overrides.

Current flow:

```text
Ratio / Financial Constraint Assessment
    ↓
suggested_overrides
    +
explicit rule_overrides
    ↓
effective_overrides
    ↓
MultiGoalOrchestrator
```

Explicit `rule_overrides`, when supplied, are applied after suggested overrides.

Overrides are planning decisions/evidence. They do not redefine canonical metric formulas.

## 14. Multi-Goal Orchestration

The multi-goal planner passes:

- goal evaluation inputs;
- financial context;
- strategy evaluation lookup;
- effective rule overrides;

to:

`MultiGoalOrchestrator.orchestrate()`

The orchestrator is responsible for deciding how multiple goals compete for shared financial resources.

```text
Goals
    +
Financial State
    +
Current Strategy Context
    +
Constraints
    +
Priorities
    ↓
MultiGoalOrchestrator
    ↓
MultiGoalPlanResult
```

## 15. Priority and Goal Ordering

The Complete Financial Plan preserves both:

- client priority;
- resolved planning priority.

The financial plan service also exposes priority ranks in resource allocation.

Priority is planning context, not a strategy identity.

Canonical priority vocabulary remains:

- `critical`
- `high`
- `medium`
- `low`

The canonical priority authority is the existing priority rule layer. The Complete Financial Plan must not create another priority taxonomy.

## 16. Consolidated Financial Position

The plan exposes a consolidated Financial State section containing:

- annual income;
- annual expenses;
- monthly surplus;
- assets;
- liabilities;
- net worth.

```text
Current FinancialState
    ↓
Complete Plan
    └── financial_state
        ├── annual_income
        ├── annual_expenses
        ├── monthly_surplus
        ├── assets
        ├── liabilities
        └── net_worth
```

This is a presentation/aggregation output. It is not a second FinancialState authority.

## 17. Consolidated Funding

The plan aggregates all goals into one funding picture.

Outputs:

- total required monthly contribution;
- total allocated monthly contribution;
- available monthly surplus;
- monthly gap;
- overall funding status;
- competition detected.

```text
Goal Requirements
    ↓
sum required contributions
    ↓
Shared Available Surplus
    ↓
Allocation
    ↓
Consolidated Funding Status
```

This answers whether the investor can support the total goal portfolio from the available monthly cash-flow capacity.

## 18. Goal Funding Portfolio

The plan returns one consolidated row per goal.

Each row can contain:

- goal identity;
- target date;
- today's cost;
- future target;
- funding gap;
- projected mapped asset value;
- required monthly contribution;
- allocated monthly contribution;
- monthly shortfall;
- funding status;
- feasibility status;
- available monthly surplus;
- funding strategies;
- StrategyVersion ID;
- strategy identity/name;
- reasons;
- notes.

The Complete Financial Plan therefore provides a cross-goal view while preserving individual goal ownership.

## 19. Resource Allocation

The current response includes:

`resource_allocation`

with:

- total monthly surplus;
- foundation allocation;
- discretionary surplus;
- goal allocations;
- total allocated monthly amount;
- unallocated surplus.

Each goal allocation can include:

- goal ID;
- goal name;
- requested amount;
- allocated amount;
- shortfall;
- funding percentage;
- priority rank;
- client priority;
- resolved priority;
- override state/reason.

The allocation is a planning output, not a replacement for Goal Planner funding calculations.

## 20. Funding Status Boundary

Goal funding status and allocation status must remain semantically distinct.

Goal Planner owns goal funding status such as:

- Shortfall;
- On Track;
- Overfunded.

The consolidated plan may expose allocation-oriented statuses such as:

- fully_funded;
- partially_funded;
- unfunded;
- within_surplus;
- surplus_shortfall;
- requires_review;

where supplied by the multi-goal orchestration model.

These vocabularies must not be silently merged.

## 21. Strategy Summary

The Complete Financial Plan exposes the current strategy associated with each goal.

The source is the current StrategyVersion / goal report context.

The plan may include:

- StrategyVersion ID;
- strategy ID;
- strategy name;
- selected/recommended strategy context;
- goal-specific reasons;
- trade-offs.

The plan is not allowed to turn the strategy summary into a new strategy-selection engine.

## 22. Goal Plan Output

The response includes `goal_plans`.

Each goal plan can contain:

- goal ID/name/type;
- target amount;
- today's cost;
- target date;
- StrategyVersion ID;
- strategy ID/name;
- required monthly amount;
- allocated monthly amount;
- monthly shortfall;
- funding gap;
- projected mapped asset value;
- funding status;
- feasibility status;
- available monthly surplus;
- funding strategies;
- `is_feasible`;
- reasons;
- notes.

This is the normalized goal-level view used by the consolidated plan.

## 23. Strategy Version Registry

The current plan exposes the StrategyVersion IDs represented in the plan.

```text
Goals
    ↓
Current selected StrategyVersion per goal
    ↓
strategy_versions[]
```

This provides lineage from the complete plan back to finalized per-goal strategy decisions.

It is provenance/aggregation data, not a new authority table.

## 24. Trade-Offs

Cross-goal planning can generate trade-offs when resources are insufficient or constraints compete.

Trade-offs are attached from `MultiGoalPlanResult.trade_offs`.

Examples of the type of planning issue represented:

- one high-priority goal receives more funding;
- another goal receives reduced allocation;
- a constraint forces reprioritization;
- shared surplus cannot fully satisfy every goal.

The plan must expose the trade-off rather than silently hide the allocation consequence.

## 25. Action Plan Boundary

The current Complete Financial Plan response includes an action-oriented summary.

It can expose:

- action ID;
- category;
- title;
- description;
- priority;
- target type;
- target ID;
- monthly commitment;
- lump-sum commitment;
- deadline;
- status.

These are plan-level action requirements.

They must not be confused with the authoritative ActionPlanItem lifecycle.

The Action Plan feature remains responsible for executable action records, decisions, completion, actual state and execution history.

```text
Complete Financial Plan
    ↓
Required actions / plan actions
    ↓
Action Plan feature
    ↓
Executable ActionPlanItems
```

## 26. Cash-Flow Trajectory

The current FinancialPlanService builds a family cash-flow trajectory.

It models, per year:

- opening balance;
- annual investment;
- growth;
- goal outflow;
- maturing goals;
- closing balance.

The current implementation uses a fixed 9% return assumption for this trajectory.

This is an important boundary:

**The trajectory is currently a planning/report projection helper, not a canonical financial-return assumption.**

It must not be confused with Goal Planner's asset-specific expected return or another canonical required-return calculation.

## 27. MoneyWheel Health Scan

The current Complete Financial Plan also exposes a `moneywheel_health_scan`.

It currently reports:

- Savings Rate;
- Debt-to-Income;
- Emergency Fund Buffer;
- Financial Asset Ratio.

The scan is intended as a health summary inside the consolidated plan.

However, the current `FinancialPlanService` implementation contains duplicate local calculations for DTI and emergency coverage.

Known current duplicate formulas:

- DTI uses liabilities / annual income;
- emergency coverage uses `financial_assets * 0.2 / monthly_expenses`.

These do not match the canonical DTI/emergency coverage definitions.

Therefore this section is **not yet fully canonicalized** and must be migrated to the canonical calculation layer.

## 28. Ratio Constraints

The current plan also exposes `ratio_constraints`.

These are presentation-level constraint diagnostics generated by FinancialPlanService.

They must ultimately consume:

- canonical financial formulas;
- purpose-specific canonical thresholds;
- canonical constraint semantics.

The Complete Financial Plan must not become a second rules engine.

## 29. Contingency Matrix

The current plan exposes a family contingency matrix.

Its purpose is to describe how the planning system should respond to adverse events affecting:

- monthly surplus;
- goal cost;
- market conditions;
- goal priority/resource allocation.

This is planning guidance/evidence.

It is not an automatic execution engine.

## 30. Governance Protocol

The current Complete Financial Plan response includes a governance protocol.

Governance belongs at the plan level because a financial plan must define how and when the plan is reviewed or changed.

Governance must preserve:

- current StrategyVersion authority;
- DefinedGoal revision boundaries;
- FinancialState freshness;
- approval boundaries;
- action execution history.

## 31. Audit Trail

The multi-goal plan attaches audit evidence.

The current plan adds a `ConstraintAggregator` audit entry containing:

- canonical ConstraintSet;
- constraint count;
- conflict count;
- hard-failure count.

The Complete Financial Plan therefore provides traceability from consolidated planning output back to constraint evaluation.

The audit trail is evidence/history, not current decision authority.

## 32. Current Complete Plan Output Contract

```text
complete_financial_plan
├── planning_unit_id
├── goals[]
├── goal_count
├── financial_state
│   ├── annual_income
│   ├── annual_expenses
│   ├── monthly_surplus
│   ├── assets
│   ├── liabilities
│   └── net_worth
├── consolidated_funding
│   ├── required_monthly_contribution
│   ├── allocated_monthly_contribution
│   ├── available_monthly_surplus
│   ├── monthly_gap
│   ├── funding_status
│   └── competition_detected
├── summary
├── resource_allocation
├── goal_plans[]
├── strategy_versions[]
├── actions[]
├── action_plan
├── trade_offs[]
├── constraints[]
├── constraint_conflicts[]
├── audit_trail[]
├── ratio_constraints[]
├── family_cash_flow_trajectory[]
├── moneywheel_health_scan[]
├── contingency_matrix[]
└── governance_protocol
```

## 33. Feature End-to-End Flow

```text
AUTHENTICATED USER
    ↓
PLANNING UNIT
    ↓
CURRENT FINANCIAL STATE
    ↓
LIST ACTIVE GOALS
    ↓
FOR EACH GOAL
    ├── CURRENT DEFINED GOAL
    ├── CURRENT SELECTED STRATEGYVERSION
    ├── GOAL CALCULATION
    ├── FEASIBILITY
    └── STRATEGY CONTEXT
    ↓
GOAL EVALUATION INPUTS
    ↓
FINANCIAL CONSTRAINT EVALUATION
    ↓
CANONICAL CONSTRAINT AGGREGATION
    ↓
MULTI-GOAL ORCHESTRATION
    ├── PRIORITY
    ├── SHARED SURPLUS
    ├── GOAL FUNDING
    ├── RESOURCE ALLOCATION
    ├── TRADE-OFFS
    └── CROSS-GOAL PLAN
    ↓
FINANCIAL PLAN AGGREGATION
    ├── FINANCIAL POSITION
    ├── GOALS
    ├── CONSOLIDATED FUNDING
    ├── STRATEGIES
    ├── CONSTRAINTS
    ├── ACTION REQUIREMENTS
    ├── TRAJECTORY
    └── GOVERNANCE
    ↓
COMPLETE FINANCIAL PLAN
```

## 34. Relationship to Other Features

### Goal Planner

Goal Planner answers:

> What does each goal require?

Complete Financial Planning answers:

> How do all goals fit together financially?

### Financial Health & Rules

Financial Health answers:

> What is happening financially, and what constraints exist?

Complete Financial Planning answers:

> What does that financial state mean for the combined plan?

### Strategy Builder

Strategy Builder answers:

> Which strategy should address a goal/problem?

Complete Financial Planning answers:

> How do the selected strategies for all goals coexist within the investor's financial capacity?

### Strategy → Action Plan

Action Plan answers:

> What must the investor execute?

Complete Financial Planning provides the consolidated plan-level action requirements but does not own execution lifecycle.

## 35. What Complete Financial Planning Does Not Own

It does not own:

1. canonical goal taxonomy;
2. DefinedGoal calculation;
3. canonical financial formulas;
4. MoneyWheel threshold definitions;
5. Strategy identity;
6. StrategyRun current authority;
7. StrategyVersion mutation;
8. Action completion;
9. authoritative FinancialState persistence;
10. product selection.

These remain owned by their respective feature/domain authorities.

## 36. Current Implementation Gaps

The following are confirmed implementation gaps relevant to this feature:

### 36.1 FinancialPlanService duplicate financial formulas

`backend/services/financial_plan_service.py` still contains local DTI and emergency coverage calculations.

These must use canonical calculation functions.

### 36.2 MoneyWheel health scan is not fully canonical

The current health scan uses local benchmark values and duplicate formulas.

It must consume the canonical MoneyWheel metric/rule contract.

### 36.3 Ratio constraint presentation duplicates rule logic

The local ratio constraint helper should consume canonical calculation and constraint outputs rather than independently reconstructing financial ratios.

### 36.4 Live plan versus persisted plan snapshot

The current feature builds the Complete Financial Plan live and does not persist a dedicated plan snapshot.

Therefore a historical immutable "Financial Plan Version" is not currently established by this service.

### 36.5 Action plan boundary

The current response includes plan-level action summaries while the executable ActionPlanItem lifecycle belongs to the separate Action Plan feature.

The boundary must remain explicit to avoid duplicate action authorities.

### 36.6 Cash-flow trajectory assumption

The current family trajectory uses a fixed 9% return assumption.

This is a projection helper and must not silently become a canonical return assumption.

### 36.7 Complete plan report rendering

The system already has report-oriented services and report architecture, but the Complete Financial Plan feature document describes the planning data contract separately from any particular PDF/report renderer.

Rendering must remain a presentation layer over the planning outputs.

## 37. Regression Contract

### Planning scope

- only authenticated Planning Unit owners can build/read the plan;
- no-goal planning unit returns the current documented error;
- every goal in the current plan has a usable current StrategyVersion.

### Authority

- current strategy comes from explicit selected StrategyVersion;
- latest StrategyRun cannot become current authority;
- stale DefinedGoal-bound StrategyVersions cannot be treated as current.

### Financial state

- current FinancialState remains owned by FinancialStateService;
- missing/stale financial state must not silently become authoritative;
- plan calculations must consume current financial-state context.

### Goal calculations

- Complete Financial Plan must consume Goal Planner outputs;
- it must not create a competing future-target/funding-gap formula;
- funding status semantics remain aligned with Goal Planner.

### Constraints

- canonical formulas are used;
- canonical constraint set is preserved;
- warnings/hard constraints remain distinguishable;
- constraints do not automatically become goal infeasibility.

### Multi-goal allocation

- priority ordering is deterministic;
- shared surplus allocation is traceable;
- funding competition is visible;
- trade-offs are explicit.

### Strategy lineage

- each goal's current strategy is traceable to StrategyVersion;
- strategy IDs/names do not replace StrategyVersion identity;
- plan output does not mutate strategy authority.

### Actions

- plan-level actions do not replace ActionPlanItem lifecycle;
- executable actions retain StrategyVersion lineage;
- actual-state updates remain under FinancialState authority.

### Auditability

- constraint aggregation evidence remains available;
- plan outputs remain traceable to source feature authorities.

## 38. Final Complete Financial Planning Output

```text
CURRENT FINANCIAL STATE
        +
ALL ACTIVE GOALS
        +
CURRENT STRATEGYVERSION PER GOAL
        +
CANONICAL CONSTRAINTS
        +
MULTI-GOAL RESOURCE ALLOCATION
        ↓
COMPLETE FINANCIAL PLAN
        ├── Where the investor stands
        ├── What each goal requires
        ├── How much total funding is required
        ├── What can actually be funded
        ├── Which strategy is currently selected for each goal
        ├── What trade-offs exist
        ├── What actions are required
        ├── What constraints govern the plan
        ├── How the financial trajectory looks
        └── How the plan should be governed/reviewed
```

## 39. Feature Boundary Contract

```text
GOAL PLANNER
    └── defines and calculates each goal

FINANCIAL HEALTH & RULES
    └── defines current financial state, metrics and constraints

STRATEGY BUILDER
    └── evaluates and finalizes strategy per goal

COMPLETE FINANCIAL PLANNING
    └── consolidates the whole planning unit into one coherent plan

STRATEGY → ACTION PLAN
    └── converts approved strategy into executable actions

FINANCIAL STATE
    └── becomes authoritative again after validated execution/completion
```

The Complete Financial Plan is therefore a **system feature and cross-domain planning layer**, not merely a report template.

Scope: this document records the current code-backed Complete Financial Planning behavior and explicitly identifies implementation gaps where the current code has not yet reached the canonical target architecture.
