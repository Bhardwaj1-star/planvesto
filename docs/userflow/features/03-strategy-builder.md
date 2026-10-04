# Strategy Builder

## 1. Feature Scope

Strategy Builder evaluates strategies for the current DefinedGoal using current Financial State, investor priorities, rules/constraints/risk evidence and the canonical strategy library.

```text
Current DefinedGoal
        +
Current FinancialState
        +
Investor Priorities
        +
Rules / Constraints / Risk Evidence
        ↓
Applicability Filtering
        ↓
Scenarios
        ↓
Architecture Composition
        ↓
Decision Evaluation
        ↓
Ranking / Recommendation
        ↓
User Selection
        ↓
Implementation Preview
        ↓
StrategyVersion Finalization
        ↓
Explicit Current Selection
        ↓
Downstream Action / Report / Planning
```

Strategy Builder does not own:

- Goal definition
- FinancialState construction
- canonical financial formulas
- StrategyRun-as-current authority
- final action execution

## 2. User / Request Inputs

### Build

POST `/api/strategy/build`

Inputs:

- `planning_unit_id`
- `goal_id`
- optional `investor_priorities`

Investor priorities contain:

- safety
- liquidity
- growth
- flexibility

Current build behavior:

```text
request priorities
    ↓
if absent → previous latest StrategyRun priorities
    ↓
if still absent → 400 error
```

The `InvestorPriorities` model itself defaults to equal 25/25/25/25 values when instantiated directly, but the service build path explicitly requires supplied or reusable priorities.

### Selection

Selection request is bound to:

- Planning Unit
- StrategyRun
- selected strategy
- selected scenario
- selected architecture

### Preview / Finalization

Implementation requests include:

- StrategyRun
- exact DefinedGoal version
- selected strategy/scenario/architecture
- assumptions
- funding structure
- implementation parameters

## 3. Source / Authority Boundary

| Source | Role | Authority |
|---|---|---|
| DefinedGoal | goal identity, target, duration, funding state/gap, required contribution, priority, flexibility | Current Goal Planner snapshot |
| FinancialState | income, expenses, surplus, assets, liabilities, net worth and state context | FinancialStateService |
| MoneyWheel | canonical financial diagnostics | MoneywheelEngine / canonical calculation layer |
| Constraints | hard/warning/recommendation evidence | ConstraintAggregator + rule owners |
| Risk | risk-capacity and risk-required evidence | RiskProfilerEngine |
| Strategy library | strategies, components, techniques, implementation definitions | canonical strategy library |
| StrategyRun | evaluation/history/provenance | evaluation artifact |
| StrategyVersion | finalized immutable implementation snapshot | current implementation record |
| goal_strategy_selections | explicit current selection pointer | current StrategyVersion authority |

## 4. Financial Context Boundary

StrategyService builds financial context from the current FinancialState:

```text
FinancialStateService.current()
    ↓
StrategyService._financial_context()
    ├── income
    ├── expenses
    ├── surplus
    ├── assets
    ├── liabilities
    ├── financial assets
    ├── liquid assets
    └── net worth
        ↓
MoneywheelEngine
RiskProfilerEngine
RuleEngine
ConstraintAggregator
```

Asset liquidity / financial classification is resolved through the MoneywheelService asset classification path.

Strategy Builder consumes financial evidence; it does not redefine the underlying financial-state formulas.

## 5. Applicability / Eligibility Boundary

Initial candidate filtering is owned by:

`backend/engines/strategy/applicability.py::filter_applicable_strategies()`

It uses canonical goal identity and the StrategyRuleEngine to select applicable strategies.

Detailed eligibility is owned by:

`backend/engines/strategy/eligibility.py`

The canonical status vocabulary is:

- `pass`
- `conditional`
- `fail`

```text
Strategy
└── EligibilityAssessment
    ├── pass
    ├── conditional
    └── fail
```

Current eligibility fits include:

- `cashflow_fit`
- `liquidity_fit`
- `debt_fit`
- `asset_resource_fit`
- `risk_capacity_fit`
- `goal_constraint_fit`
- `multi_goal_conflict_fit`
- `implementation_fit`

A conditional result can mean missing evidence, a required change, or a defined de-risking step. It is not the same as Goal Planner feasibility `constrained`.

## 6. Decision Evaluation

Decision policy is owned by:

`backend/engines/strategy/decision.py`

Decision evidence includes:

- goal fit
- horizon fit
- funding fit
- feasibility
- component fit
- technique execution
- eligibility status
- investor priorities
- constraints
- scenario evidence

The engine evaluates every composed architecture and produces a `DecisionResult`.

```text
Eligibility
    +
Goal / Horizon / Funding Fit
    +
Feasibility
    +
Component / Technique Fit
        ↓
Decision Score
        ↓
DecisionResult
```

The documented pass/conditional/fail scores are decision-policy values. They are not financial metrics.

## 7. Scenario Generation

StrategyEngine generates:

- baseline scenarios
- investor-modified/custom scenarios supplied through the service
- what-if scenarios

A scenario can contain:

- assumptions
- funding structure
- metrics
- trade-offs
- strategy context
- implementation implications

Scenarios are evaluation artifacts. They do not become current strategy authority merely because they are ranked or recommended.

## 8. Comparison / Ranking / Recommendation

```text
Applicable Strategies
        ↓
Baseline / Custom / What-if Scenarios
        ↓
Comparison Matrix
        ↓
Decision Evaluation
        ↓
Scenario Ranking
        ↓
Recommendation
```

Recommendation is produced by:

`backend/engines/strategy/recommendation.py`

It is an evaluation output, not approval and not current StrategyVersion authority.

## 9. Strategy Architecture Identity

Canonical identity is owned by:

`backend/engines/strategy/identity.py::canonical_architecture_id()`

```text
canonical_architecture_id(
    goal_id,
    primary_strategy_id
)
        ↓
stable architecture_id
```

Identity is therefore:

**Goal ID + Primary Strategy ID**

It is composition-independent.

Supporting strategies, components and techniques are composition data.

Changing supporting composition does not create a new canonical architecture identity unless Goal or Primary Strategy changes.

## 10. Architecture Composition

Architecture composition is owned by:

`backend/engines/strategy/composition.py`

The composition contains:

- primary strategy
- supporting strategies
- technique IDs
- supporting rationale / component information

The architecture object carries the canonical architecture ID plus composition.

This separates:

```text
Identity
└── Goal + Primary Strategy

Composition
└── supporting strategies + techniques + components
```

## 11. StrategyRun Contract

StrategyRun is the evaluation/history record.

It stores:

- evaluated strategies
- scenarios
- what-if scenarios
- investor priorities
- comparison matrix
- rankings
- recommendation
- architectures
- selected transient context
- source DefinedGoal ID/version
- evaluation metadata

`is_latest` identifies the latest evaluation run only.

It does **not** establish current strategy authority.

Latest run, latest ranking or latest recommendation may be used as evaluation/provenance context, but not as the current implementation pointer.

## 12. Strategy Selection vs Finalization

### Selection

`POST /api/strategy/select`

Selection updates transient StrategyRun selection context:

- selected strategy
- selected scenario
- selected architecture

It does not create a StrategyVersion.

### Implementation Preview

`POST /api/strategy/implementation/preview`

Preview evaluates implementation inputs and returns a non-persisted StrategyRun-style result.

### Finalization

`POST /api/strategy/implementation/finalize`

Finalization creates the immutable StrategyVersion.

```text
StrategyRun evaluation
    ↓
user selection
    ↓
implementation preview
    ↓
finalization
    ↓
StrategyVersion
```

## 13. StrategyVersion Contract

Current StrategyVersion model fields include:

- `strategy_version_id`
- `planning_unit_id`
- `strategy_id`
- `version`
- `parent_version`
- `source`
- `library_version`
- `implementation_version`
- `implementation_parameters`
- `goal_id`
- `defined_goal_id`
- `defined_goal_version`
- `architecture`
- `decision_snapshot`
- `source_strategy_run_id`
- `status`
- `created_at`

Goal-bound StrategyVersions require:

- Goal context
- DefinedGoal context
- finalized architecture
- source StrategyRun provenance

`investor_edit` versions require `parent_version`.

The version snapshot is immutable after insertion; lifecycle approval/primary state is not encoded by mutating the snapshot.

## 14. Current Strategy Authority

Current strategy authority is:

```text
Goal
  ↓
goal_strategy_selections
  ↓
StrategyVersion
```

`StrategyRepository.get_selected_strategy_version()` validates:

- current DefinedGoal is still the selected DefinedGoal
- exact DefinedGoal ID/version
- Goal ID
- StrategyVersion identity
- source StrategyRun provenance
- architecture presence
- recommendation strategy identity
- selected scenario consistency
- decision snapshot consistency

A stale DefinedGoal-bound selection returns no current StrategyVersion.

## 15. Downstream Action Boundary

Current action generation is owned by:

`backend/services/strategy_action_generator.py`

Before generating actions, it requires:

1. StrategyVersion approval;
2. valid Goal / DefinedGoal context;
3. finalized architecture;
4. StrategyVersion is the current selected version for the Goal.

Action composition is read from the StrategyVersion architecture plus strategy/technique definitions.

```text
Approved Current StrategyVersion
        ↓
StrategyActionGenerator
        ↓
Architecture
├── primary strategy
├── supporting strategies
└── techniques
        ↓
ActionPlanItem
```

Therefore action generation does not read `run.selected_architecture` as its current authority.

## 16. Approval Boundary

Approval is distinct from:

- recommendation
- selection
- finalization

```text
Recommendation ≠ Selection
Selection ≠ Finalization
Finalization ≠ Approval
Approval ≠ Historical StrategyRun
```

Action generation requires the approved StrategyVersion lifecycle.

The StrategyVersion model's `status` is creation metadata; approval/primary lifecycle is represented outside the immutable snapshot.

## 17. Goal Revision Boundary

Current StrategyRepository prevents a StrategyVersion from remaining current when its DefinedGoal ID/version no longer matches the latest DefinedGoal.

```text
DefinedGoal v1
    ↓
StrategyRun
    ↓
StrategyVersion v1
    ↓
goal_strategy_selections

DefinedGoal v2
    ↓
old selection fails current DefinedGoal validation
    ↓
new strategy evaluation
    ↓
new StrategyVersion
    ↓
new current selection
```

A material Goal Planner revision also triggers StrategyService recalculation for the new DefinedGoal version.

## 18. API Contract

Primary Strategy Builder routes:

- `POST /api/strategy/build`
- `POST /api/strategy/scenarios/custom`
- `POST /api/strategy/priorities`
- `POST /api/strategy/select`
- `POST /api/strategy/implementation/preview`
- `POST /api/strategy/implementation/finalize`
- `GET /api/strategy/runs/{goal_id}/latest`
- `GET /api/strategy/runs/{goal_id}/history`
- `GET /api/strategy/strategy-versions/{strategy_version_id}/report`
- `GET /api/strategy/goals/{goal_id}/selected-version`
- StrategyVersion history/by-ID routes under `/api/strategy/versions/*`

Run-report routes remain available as history/compatibility access. Current strategy report access should use the StrategyVersion route.

## 19. Code Ownership

```text
API
├── backend/api/strategy.py
└── backend/api/strategy_version.py

Request contracts
└── backend/schemas/strategy.py

Orchestration
└── backend/services/strategy_service.py

Candidate filtering
└── backend/engines/strategy/applicability.py

Eligibility
└── backend/engines/strategy/eligibility.py

Decision
└── backend/engines/strategy/decision.py

Scenario generation
└── backend/engines/strategy/scenario.py

Comparison
└── backend/engines/strategy/comparison.py

Ranking
└── backend/engines/strategy/ranking.py

Recommendation
└── backend/engines/strategy/recommendation.py

Architecture identity
└── backend/engines/strategy/identity.py

Architecture composition
└── backend/engines/strategy/composition.py

Strategy engine
└── backend/engines/strategy/engine.py

StrategyRun persistence
└── backend/data/strategy_repository.py

StrategyVersion model
└── backend/models/strategy_version.py

StrategyVersion lifecycle
└── backend/services/strategy_version_service.py

Action generation
└── backend/services/strategy_action_generator.py

Current selection persistence
└── goal_strategy_selections
```

## 20. Regression Contract

### Input / context

- current DefinedGoal is used;
- current FinancialState is obtained through FinancialStateService;
- Planning Unit / Goal ownership is enforced;
- investor priorities are explicit.

### Eligibility

- candidate filtering uses canonical goal identity;
- detailed eligibility remains pass/conditional/fail;
- conditional does not become Goal feasibility constrained.

### Decision

- investor priorities remain decision preferences;
- financial formulas remain outside Strategy Builder ownership;
- decision scoring remains strategy-policy owned.

### Architecture

- architecture ID is stable for the same Goal + Primary Strategy;
- supporting composition does not change canonical identity.

### StrategyRun

- latest run is evaluation history;
- `is_latest` is not current strategy authority.

### StrategyVersion

- goal-bound version contains exact Goal/DefinedGoal context;
- architecture matches primary strategy;
- decision snapshot matches selected scenario/recommendation;
- source StrategyRun provenance is present;
- immutable snapshot is not mutated into approval state.

### Current authority

- `goal_strategy_selections` is the current selection pointer;
- stale DefinedGoal selections are rejected;
- cross-goal/cross-version bindings are rejected.

### Actions

- action generation requires approved current StrategyVersion;
- action composition comes from StrategyVersion architecture and library definitions.

## 21. Current Implementation Notes / Gaps

Confirmed from current code:

1. Build can reuse priorities from the latest StrategyRun when the request omits them; this is an evaluation-input fallback, not current strategy authority.
2. StrategyRun remains callable through latest/history/report routes for evaluation/history compatibility.
3. Approval remains a separate lifecycle record/boundary; StrategyVersion `status` is immutable creation metadata.
4. Goal revision invalidates old selection through exact DefinedGoal ID/version validation.
5. Downstream action generation uses the selected StrategyVersion architecture rather than latest StrategyRun architecture.
6. FinancialPlanService still has independent financial diagnostic formulas; this is a Financial Health boundary issue, not Strategy Builder ownership.

## 22. Important Semantic Boundaries

1. **StrategyRun ≠ current StrategyVersion**
2. **Recommendation ≠ approval**
3. **Selection ≠ finalization**
4. **Finalization ≠ approval**
5. **Ranking ≠ authority**
6. **Goal Planner ≠ Strategy Builder**
7. **FinancialState ≠ strategy-owned calculation**
8. **Eligibility ≠ feasibility**
9. **Funding status ≠ eligibility**
10. **Architecture identity ≠ composition**
11. **StrategyVersion ≠ approval record**
12. **Historical evaluation ≠ current implementation**

## 23. Final Strategy Builder Output

```text
CURRENT DEFINED GOAL
    +
CURRENT FINANCIAL STATE
    +
INVESTOR PRIORITIES
    +
RULES / MONEYWHEEL / RISK / CONSTRAINT EVIDENCE
    ↓
APPLICABLE STRATEGIES
    ↓
ELIGIBILITY
    ├── pass
    ├── conditional
    └── fail
    ↓
SCENARIOS
    ├── baseline
    ├── custom / investor-modified
    └── what-if
    ↓
COMPARISON
    ↓
DECISION
    ↓
RANKING
    ↓
RECOMMENDATION
    ↓
ARCHITECTURE
    └── canonical Architecture ID = Goal ID + Primary Strategy ID
    ↓
USER SELECTION
    ↓
IMPLEMENTATION PREVIEW
    ↓
FINALIZATION
    ↓
IMMUTABLE STRATEGYVERSION
    ↓
goal_strategy_selections
    ↓
CURRENT STRATEGY AUTHORITY
    ↓
APPROVED STRATEGYVERSION
    ↓
ACTION / REPORT / MULTI-GOAL / EXECUTION
```

## 24. Strategy Builder End-to-End Contract

```text
CURRENT DEFINED GOAL
    ↓
CURRENT FINANCIAL STATE
    ↓
INVESTOR PRIORITIES
    ↓
APPLICABILITY FILTER
    ↓
ELIGIBILITY
    ↓
SCENARIO GENERATION
    ↓
ARCHITECTURE COMPOSITION
    ↓
DECISION / COMPARISON / RANKING
    ↓
RECOMMENDATION
    ↓
USER SELECTION
    ↓
IMPLEMENTATION PREVIEW
    ↓
STRATEGYVERSION FINALIZATION
    ↓
EXPLICIT CURRENT SELECTION
    ↓
APPROVAL
    ↓
ACTION / REPORT / MULTI-GOAL / EXECUTION

Scope: this document is verified against the current Strategy Builder, StrategyVersion, selection and action-generation code. Unsupported authority claims and stale ownership paths have been removed; confirmed implementation boundaries are stated explicitly.
```