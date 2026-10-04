# Strategy Builder

## 1. Feature Scope

Strategy Builder evaluates applicable strategies for the current canonical DefinedGoal using the current authoritative Financial State, investor priorities, risk/suitability evidence, constraints and the canonical strategy library.

It is responsible for:

- strategy eligibility
- strategy decision evidence
- scenario generation
- comparison and ranking
- recommendation
- architecture identity
- user selection context
- implementation preview
- immutable StrategyVersion finalization
- explicit current StrategyVersion selection authority

It does **not** own:

- Goal definition
- FinancialState construction
- canonical financial formulas
- final action execution
- historical StrategyRun as current authority

```text
Current DefinedGoal
        +
Current FinancialState
        +
Investor Priorities
        +
Rules / Constraints / Risk Evidence
        ↓
Strategy Eligibility
        ↓
Strategy Scenarios
        ↓
Comparison
        ↓
Decision Evaluation
        ↓
Ranking / Recommendation
        ↓
Architecture
        ↓
User Selection
        ↓
Implementation Preview
        ↓
Finalization
        ↓
Immutable StrategyVersion
        ↓
Explicit Current Selection
        ↓
Downstream Action Plan / Reports / Execution
```

## 2. User / Request Inputs

### Strategy build

POST `/api/strategy/build`

Inputs:

- `planning_unit_id`
- `goal_id`
- optional `investor_priorities`

Investor priorities are:

- safety
- liquidity
- growth
- flexibility

The frontend currently sends equal `0.25` defaults when priorities are absent. The service can reuse prior StrategyRun priorities; if neither is available, build fails.

### Strategy selection

Selection context includes:

- `planning_unit_id`
- `strategy_run_id`
- selected strategy
- selected scenario
- selected architecture
- implementation parameters

### Preview / finalization

Preview and finalization require:

- selected strategy context
- exact DefinedGoal identity/version
- selected scenario
- selected architecture
- implementation configuration

Finalization produces the immutable StrategyVersion.

## 3. Input Source / Authority Boundary

| Source | Examples | Authority |
|---|---|---|
| DefinedGoal | goal identity, target, duration, funding status/gap, required contribution, flexibility, priority | Current DefinedGoal |
| Financial State | income, expenses, surplus, assets, liabilities, net worth, liquidity | FinancialStateService |
| Investor priorities | safety, liquidity, growth, flexibility | Strategy decision input |
| Goal rules | goal-specific evidence / constraints | Goal Rule Engine |
| MoneyWheel | canonical financial ratios/rules and constraint evidence | MoneyWheel / constraint owners |
| Risk / suitability | investor risk and suitability evidence | Risk Profiler / suitability layer |
| Constraint aggregation | applicable planning constraints | ConstraintAggregator |
| Strategy library | strategies, components, techniques, solutions | Canonical strategy library |
| StrategyRun | evaluation context/provenance | Strategy evaluation history, not current authority |

DefinedGoal and FinancialState are consumed as authoritative upstream context. Strategy Builder must not create competing versions of either.

Investor priorities are decision preferences, not financial metrics.

## 4. Input Consumption Boundary

Strategy Builder consumes inputs according to their semantic role.

### Goal-driving inputs

- canonical goal type/name
- target
- duration
- funding status
- funding gap
- required contribution
- priority
- flexibility
- current DefinedGoal version

### Financial decision context

- income
- expenses
- investable surplus
- assets
- liabilities
- net worth
- liquidity
- MoneyWheel ratios/rules
- constraint evidence

These are decision evidence. Strategy Builder does not redefine their formulas.

### Investor decision preferences

- safety
- liquidity
- growth
- flexibility

These affect strategy decision/scoring and must not be treated as financial-health metrics.

### Strategy library inputs

- applicable strategies
- supporting strategies/components
- techniques
- solutions
- library/version metadata

### Historical evaluation context

StrategyRun can provide evaluation provenance, prior investor priorities and generated scenarios. It cannot establish current strategy authority merely because it is latest or marked `is_latest`.

## 5. Canonical Eligibility Rules

Strategy eligibility is evaluated through:

`filter_applicable_strategies()`

Eligibility remains:

- `pass`
- `conditional`
- `fail`

These statuses are intentionally distinct from:

- Goal Planner funding status: `Shortfall / On Track / Overfunded`
- allocation funding status: `fully_funded / partially_funded / unfunded / within_surplus / surplus_shortfall / requires_review`
- goal-level feasibility
- financial ratio classifications

Do not collapse these vocabularies merely because they all describe some form of planning condition.

### Eligibility semantics

```text
Strategy
└── Eligibility evidence
    ├── pass
    ├── conditional
    └── fail
```

A conditional strategy can represent a strategy that becomes suitable after a required change, missing evidence, de-risking step or other explicit condition. It is not automatically equivalent to funding `constrained`.

## 6. Decision Logic and Scoring

Decision evidence includes:

- goal characteristics
- planning horizon
- funding status
- funding gap
- flexibility
- priority
- liabilities
- investor priorities
- eligibility / feasibility evidence
- constraints
- architecture/component fit
- technique evidence

Scoring separates:

- goal fit
- horizon fit
- funding fit
- feasibility
- component fit
- technique execution

Current decision examples documented in the system include:

- pass = 15
- conditional = 8
- fail = 0
- failed eligibility receives an infeasible score

These scores are decision-policy outputs, not financial metrics.

## 7. Strategy Scenarios

Applicable strategies can produce:

- baseline scenarios
- investor-modified scenarios
- custom scenarios
- what-if scenarios

A scenario can carry:

- assumptions
- funding structure
- metrics
- trade-offs
- selected strategy/component context
- implementation implications

Scenarios are evaluation artifacts. They do not become the current strategy merely by being ranked or recommended.

## 8. Comparison / Recommendation Contract

```text
Applicable Strategies
        ↓
Scenarios
        ↓
Comparison Matrix
        ↓
Decision Evaluation
        ↓
Rankings
        ↓
Recommendation
```

Recommendation is an evaluation output.

It may contain:

- recommended strategy IDs
- recommended scenario
- reasons
- architecture
- alternatives
- feasibility status
- constraints

Recommendation is not approval and is not current StrategyVersion authority.

## 9. Strategy Architecture Identity

Canonical architecture identity is:

```text
Goal ID + Primary Strategy ID
```

The architecture identity is composition-independent.

Supporting strategies, components, techniques and solutions are composition data.

Therefore:

- adding/removing supporting techniques does not silently create a new architecture identity;
- changing composition does not redefine the primary architecture identity;
- architecture identity remains stable unless the Goal or Primary Strategy changes.

Architecture is therefore an identity boundary, not a serialized copy of every implementation component.

## 10. Lifecycle / State Transitions

```text
Build
  ↓
StrategyRun
  ↓
Select strategy / scenario / architecture
  ↓
Implementation Preview
  ↓
Finalize
  ↓
Immutable StrategyVersion
  ↓
Explicit current selection
  ↓
Current Strategy Authority
```

StrategyRun represents evaluation/history.

`is_latest` does not establish current strategy authority.

Finalization requires exact:

- Goal
- DefinedGoal ID
- DefinedGoal version
- selected strategy
- selected scenario
- architecture
- implementation configuration

## 11. StrategyRun Boundary

StrategyRun is an evaluation and provenance record.

It may contain:

- evaluated strategies
- scenarios
- rankings
- recommendation
- investor priorities
- decision evidence
- source DefinedGoal ID/version
- evaluation metadata

It may be used to reconstruct how a recommendation was produced.

It must not be used as the current strategy simply because:

- it is the latest run;
- `is_latest=true`;
- it has the highest ranking;
- it contains a recommendation.

Current strategy authority is established only through explicit StrategyVersion selection.

## 12. StrategyVersion Contract

An immutable StrategyVersion contains the finalized implementation context, including:

- `strategy_version_id`
- `planning_unit_id`
- `strategy_id`
- `version`
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

Investor-edited StrategyVersions use `source=investor_edit` and require the appropriate parent version.

The StrategyVersion is the immutable implementation snapshot used by downstream current-strategy consumers.

## 13. Current Strategy Authority

The current strategy authority is:

```text
Goal
  ↓
goal_strategy_selections
  ↓
StrategyVersion
```

The explicit selection must be validated against the current DefinedGoal.

Current StrategyVersion resolution requires consistency of:

- Planning Unit
- Goal
- current DefinedGoal
- exact DefinedGoal ID
- exact DefinedGoal version
- StrategyVersion
- source StrategyRun provenance
- architecture
- recommendation/strategy identity
- selected scenario
- decision snapshot

A StrategyVersion bound to another Goal or another DefinedGoal version cannot become current.

Latest StrategyRun, ranking, recommendation or `is_latest` must never substitute for this explicit authority.

## 14. Selection vs Finalization vs Approval

These are separate lifecycle concepts.

### Selection

User chooses a strategy/scenario/architecture from evaluation output.

### Finalization

The selected implementation context is persisted as an immutable StrategyVersion.

### Approval

Approval is a separate lifecycle boundary and must not be inferred merely from recommendation, selection or finalization.

Therefore:

```text
Recommendation ≠ Selection
Selection ≠ Finalization
Finalization ≠ Approval
Approval ≠ Historical Recommendation
```

Downstream Action Plan generation depends on the appropriate approved current StrategyVersion lifecycle.

## 15. StrategyVersion Validation / Provenance Boundary

Before a StrategyVersion becomes current, the system must be able to prove:

1. it belongs to the authenticated Planning Unit;
2. it belongs to the requested Goal;
3. it is bound to the current DefinedGoal;
4. its DefinedGoal ID/version is exact;
5. its source StrategyRun belongs to the same planning context;
6. its architecture is consistent;
7. its decision snapshot matches the selected recommendation/scenario;
8. it represents the finalized implementation context.

This prevents stale, cross-goal or cross-revision StrategyVersions from becoming current.

## 16. Output Contract

Strategy Builder produces:

### Evaluation outputs

- applicable strategies
- eligibility status
- eligibility evidence
- scenarios
- comparison data
- scoring/decision evidence
- ranking
- recommendation
- alternatives
- feasibility/constraint context

### Selection outputs

- selected strategy
- selected scenario
- selected architecture
- implementation parameters

### Final implementation output

- immutable StrategyVersion
- exact Goal / DefinedGoal binding
- decision snapshot
- architecture identity
- source StrategyRun provenance

### Current authority output

- explicit `goal_strategy_selections` binding
- current StrategyVersion for the current DefinedGoal

The output must make clear the difference between evaluation history, user selection, finalized implementation and current authority.

## 17. Downstream Dependency Boundary

```text
Current StrategyVersion
├── Action Plan
├── Reports
├── Multi-goal Planning
└── Execution
```

Downstream consumers must use the current selected StrategyVersion.

They must not derive current strategy from:

- latest StrategyRun
- ranking
- recommendation
- `is_latest`
- stale StrategyVersion

A revised DefinedGoal requires a new strategy evaluation and a new StrategyVersion lifecycle.

## 18. Versioning / Replanning Boundary

```text
DefinedGoal v1
    ↓
Strategy evaluation
    ↓
StrategyVersion v1
    ↓
Current selection

DefinedGoal v2
    ↓
New strategy evaluation
    ↓
StrategyVersion v2
    ↓
New selection
    ↓
New approval / downstream lifecycle
```

When a material DefinedGoal revision occurs:

1. the old DefinedGoal remains history;
2. the old StrategyVersion remains historical;
3. the old current selection must no longer satisfy current DefinedGoal binding;
4. a new strategy evaluation is required;
5. a new StrategyVersion is finalized;
6. the new StrategyVersion must be explicitly selected;
7. downstream current planning must use the new version.

No silent migration of old strategy/action state is allowed.

## 19. Code Ownership

- Strategy API: `backend/api/strategy.py`
- StrategyVersion API: `backend/api/strategy_version.py`
- Strategy schemas/contracts: `backend/schemas/strategy.py`
- Strategy orchestration: `backend/services/strategy_service.py`
- StrategyVersion lifecycle: `backend/services/strategy_version_service.py`
- Strategy engine: `backend/engines/strategy/engine.py`
- Strategy eligibility: `backend/engines/strategy/applicability.py`
- Strategy decision policy: `backend/rules/strategy_decision.py`
- Strategy selection authority/repository: `backend/data/strategy_repository.py`
- StrategyVersion model: `backend/models/strategy_version.py`
- Frontend strategy contract: `frontend/lib/api/strategy.ts`
- Current selection persistence: `goal_strategy_selections`

The ownership rule is:

```text
Strategy Engine
└── evaluates

Strategy Rules
└── define eligibility / decision policy

StrategyRun
└── records evaluation/history

StrategyVersion
└── owns finalized implementation snapshot

goal_strategy_selections
└── owns current strategy selection

Downstream consumers
└── consume current StrategyVersion
```

No downstream consumer should become a second owner of strategy identity or current strategy authority.

## 20. Regression Contract

Tests must protect these invariants.

### Goal / context

- Strategy Builder uses the current DefinedGoal.
- current FinancialState comes from FinancialStateService.
- Goal ownership and Planning Unit ownership remain enforced.

### Eligibility

- eligibility remains pass / conditional / fail;
- eligibility is not silently merged with funding or allocation status;
- conditional does not automatically mean constrained.

### Decision

- investor priorities remain decision preferences;
- decision evidence remains distinct from financial metrics;
- scoring policy remains owned by strategy decision rules.

### Architecture

- architecture identity remains Goal ID + Primary Strategy ID;
- supporting composition does not silently change architecture identity.

### StrategyRun

- StrategyRun remains evaluation/history;
- `is_latest` cannot establish current authority;
- latest ranking/recommendation cannot substitute for explicit selection.

### StrategyVersion

- StrategyVersion is immutable;
- Goal binding is exact;
- DefinedGoal ID/version binding is exact;
- source StrategyRun provenance is consistent;
- architecture and decision snapshot remain consistent.

### Current authority

- current strategy is resolved through `goal_strategy_selections`;
- stale DefinedGoal-version selections are rejected;
- cross-goal StrategyVersions are rejected;
- stale StrategyVersions cannot become current.

### Downstream

- Action Plan, reports and multi-goal planning consume current StrategyVersion;
- historical StrategyRuns are not used as current strategy authority.

## 21. Known Implementation Notes / Gaps

These are implementation observations already identified by the system documentation/audit:

1. Investor-priority fallback/default behavior must remain explicit.
2. StrategyRun remains evaluation provenance/history and must not become current authority.
3. Approval is a separate lifecycle boundary; recommendation, selection and finalization are not approval.
4. Goal revision must invalidate old current selection through exact DefinedGoal-version binding.
5. Strategy Builder consumes financial/risk/constraint evidence but does not own the underlying financial formulas.
6. Current strategy authority depends on explicit selection plus exact Goal/DefinedGoal/StrategyVersion consistency.

These are implementation points, not new product decisions.

## 22. Important Semantic Boundaries

1. **StrategyRun ≠ current strategy**
2. **Recommendation ≠ approval**
3. **Selection ≠ final implementation**
4. **StrategyVersion ≠ StrategyRun**
5. **Ranking ≠ authority**
6. **Goal Planner ≠ Strategy Builder**
7. **FinancialState ≠ strategy context**
8. **Eligibility ≠ feasibility**
9. **Funding status ≠ strategy eligibility**
10. **Architecture identity ≠ full strategy composition**
11. **StrategyVersion ≠ approval record**
12. **Historical evaluation ≠ current implementation**

These boundaries prevent evaluation artifacts, financial evidence and historical records from becoming competing authorities.

## 23. Final Strategy Builder Output

```text
Current DefinedGoal
    +
Current FinancialState
    +
Investor Priorities
    +
Goal Rules / MoneyWheel / Risk / Constraint Evidence
    ↓
Applicable Strategies
    ├── pass
    ├── conditional
    └── fail
    ↓
Scenarios
    ├── baseline
    ├── investor-modified
    ├── custom
    └── what-if
    ↓
Comparison
    ↓
Decision Evaluation
    ↓
Ranking
    ↓
Recommendation
    ↓
Architecture
    └── Goal ID + Primary Strategy ID
    ↓
User Selection
    ↓
Implementation Preview
    ↓
Finalization
    ↓
Immutable StrategyVersion
    ↓
goal_strategy_selections
    ↓
Current Strategy Authority
    ↓
Downstream
    ├── Action Plan
    ├── Reports
    ├── Multi-goal Planning
    └── Execution
```

The final output must make clear:

- which DefinedGoal version was evaluated;
- which FinancialState was used;
- which investor priorities were applied;
- which strategies were eligible;
- which scenarios were compared;
- why the recommendation was produced;
- which architecture was selected;
- which exact implementation became StrategyVersion;
- which DefinedGoal version the StrategyVersion belongs to;
- and which StrategyVersion is explicitly current.

## 24. Strategy Builder End-to-End Contract

CURRENT DEFINED GOAL
    ↓
CURRENT FINANCIAL STATE
    ↓
INVESTOR PRIORITIES
    ↓
GOAL RULES / MONEYWHEEL / RISK / CONSTRAINT EVIDENCE
    ↓
STRATEGY ELIGIBILITY
    ↓
SCENARIO GENERATION
    ↓
COMPARISON / DECISION
    ↓
RANKING / RECOMMENDATION
    ↓
ARCHITECTURE IDENTITY
    ↓
USER SELECTION
    ↓
IMPLEMENTATION PREVIEW
    ↓
FINALIZATION
    ↓
IMMUTABLE STRATEGYVERSION
    ↓
EXPLICIT CURRENT SELECTION
    ↓
ACTION PLAN / REPORTS / MULTI-GOAL / EXECUTION

Scope: Strategy Builder only.
