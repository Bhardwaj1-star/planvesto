# Strategy Builder

```text
User
└── Strategy Builder open karta hai
    └── Goal + Current Financial Situation
        └── Possible strategies
            └── Har strategy check hoti hai
                ├── Goal fit
                ├── Funding fit
                ├── Risk fit
                ├── Time / Horizon fit
                └── Other suitability checks
                    └── Eligibility result
                        ├── Pass
                        ├── Conditional
                        └── Fail
                            └── Suitable strategies compare hoti hain
                                └── Decision
                                    ├── Recommended strategy
                                    └── Alternative strategies
                                        └── User strategy select karta hai
                                            └── Strategy Version
```

## 2. Inputs

### Build request
`POST /api/strategy/build`

Inputs:
- planning_unit_id
- goal_id
- investor_priorities (optional)

The API validates Goal ownership before the strategy build.

### Investor priorities
The canonical priority object contains:
- safety
- liquidity
- growth
- flexibility

These priorities are required before comparison and ranking. If not supplied, the service can reuse priorities from the previous StrategyRun; if none exist, build fails.

Frontend currently sends equal defaults when priorities are absent: safety=0.25, liquidity=0.25, growth=0.25, flexibility=0.25.

Priorities are decision preferences, not financial metrics.

## 3. Authoritative Context

Strategy Builder consumes the current DefinedGoal and current Financial State.

DefinedGoal supplies canonical goal identity, target, duration, funding status, funding gap, required contribution, flexibility and priority.

FinancialStateService supplies current financial context. Supporting context includes income, expenses, surplus, assets, liabilities, net worth, liquid assets and financial assets.

Strategy Builder does not become a second Financial State owner.

Rules and constraints are combined through Goal Rule Engine, MoneyWheel financial-ratio constraints, Risk Profiler and ConstraintAggregator. The aggregated ConstraintSet is the downstream decision boundary.

## 4. Strategy Eligibility

Applicable strategies are produced by `filter_applicable_strategies()` through the Strategy Rule Engine against the canonical strategy library.

Only eligible strategies enter the applicable-strategy set. Component activation is a later architecture concern and cannot silently remove an otherwise eligible strategy.

Strategy eligibility uses pass / conditional / fail semantics. These must remain distinct from Goal Planner funding status (Shortfall / On Track / Overfunded) and allocation funding statuses.

## 5. Decision Inputs and Scoring

Decision evidence includes:
- canonical goal type
- goal characteristics
- duration / horizon
- funding status
- flexibility
- priority
- liabilities
- investor priorities
- eligibility / feasibility
- constraint evidence
- architecture/component fit
- technique execution evidence

Decision scoring has explicit components for goal fit, horizon fit, funding fit, feasibility, component fit and technique execution.

Current policy examples:
- pass feasibility = 15
- conditional feasibility = 8
- fail feasibility = 0
- failed eligibility receives the infeasible decision score

Horizon, funding and component scores are policy-owned in `backend/rules/strategy_decision.py` and related decision modules.

## 6. Scenarios

For applicable strategies the engine can create baseline, investor-modified/custom and what-if scenarios.

Scenario data includes strategy ID, scenario type/name, assumptions, funding structure, metrics, trade-off notes and investor-modified state.

Custom scenarios are attached to the StrategyRun evaluation context.

## 7. Comparison, Ranking and Recommendation

Flow:

Applicable Strategies → Scenarios → Comparison Matrix → Decision Evaluation → Rankings → Recommendation

`StrategyRankingItem` contains rank, strategy/scenario IDs, composite score, dimension scores, recommendation flag, evidence scores and eligibility/ineligible reasons.

`StrategyRecommendation` contains recommended strategy/scenario IDs, reasons, architecture, alternative architecture IDs, feasibility status and constraints.

Critical authority rule: ranking and recommendation are evaluation outputs. They do not by themselves establish the current strategy.

## 8. Strategy Architecture

Canonical architecture identity is:

Goal ID + Primary Strategy ID

Supporting strategies, components and techniques are composition data. Changing supporting composition must not silently change the architecture identity.

Architecture may contain primary strategy, supporting strategy IDs, component IDs, technique IDs and rationale/activation evidence.

## 9. StrategyRun

StrategyRun is the evaluation/history record. It captures the exact DefinedGoal version, applicable strategies, scenarios, investor priorities, comparison, rankings, recommendation, architectures, decision evidence and run metadata.

`is_latest` means latest evaluation run for history/retrieval. It does not mean current strategy authority.

Each build creates a new run version for the goal.

## 10. User Selection

`POST /api/strategy/select` accepts:
- planning_unit_id
- strategy_run_id
- selected_strategy_id
- selected_scenario_id
- selected_architecture_id (optional)
- selected implementation parameters

Selection validates strategy/scenario/architecture consistency. Current service behavior treats this as a transient choice; final StrategyVersion authority is created only through implementation finalization.

## 11. Implementation Preview

`POST /api/strategy/implementation/preview` validates selected strategy/scenario/architecture and implementation parameters before finalization.

It can carry implementation parameters, assumptions and funding structure. Preview is not the immutable current StrategyVersion.

## 12. StrategyVersion Finalization

`POST /api/strategy/implementation/finalize` requires the exact DefinedGoal version plus selected strategy, scenario, architecture and implementation configuration.

Finalization validates the selected context against the StrategyRun/current DefinedGoal and creates an immutable StrategyVersion.

A goal-bound StrategyVersion contains:
- strategy_version_id
- planning_unit_id
- strategy_id
- version
- source
- library_version
- implementation_version
- implementation_parameters
- goal_id
- defined_goal_id
- defined_goal_version
- architecture
- decision_snapshot
- source_strategy_run_id
- status
- created_at

Goal-bound versions require finalized architecture and StrategyRun provenance.

## 13. Current Strategy Authority

Current strategy is resolved through explicit `goal_strategy_selections`:

Goal → goal_strategy_selections → StrategyVersion

The selection binds planning_unit_id, goal_id, defined_goal_id, defined_goal_version and strategy_version_id.

The repository accepts the selection only when:
1. the DefinedGoal is still the current goal version;
2. StrategyVersion belongs to the same Goal;
3. StrategyVersion binds to that exact DefinedGoal version;
4. StrategyVersion has StrategyRun provenance;
5. architecture exists;
6. recommendation matches the StrategyVersion strategy;
7. selected scenario matches the decision snapshot.

Latest StrategyRun, ranking, or `is_latest` must never substitute for this authority.

## 14. Goal Revision Boundary

Every strategy decision is bound to an exact DefinedGoal version.

DefinedGoal v1 → StrategyVersion v1

When the goal changes:

DefinedGoal v2 → new strategy evaluation → new StrategyVersion → new current selection

A StrategyVersion bound to an old DefinedGoal version must not remain current.

## 15. StrategyVersion Immutability

StrategyVersion is an immutable implementation snapshot.

Approval and Primary lifecycle are separate records; creation-time StrategyVersion status is not a mutable approval state.

For investor edits, source=`investor_edit` and parent_version is required. Implementation parameters are validated against the strategy definition; unknown parameters and changes to non-editable inherited parameters are rejected.

## 16. Downstream Contract

Current StrategyVersion → Action Plan → Execution → Actual State → Financial State update → future planning.

Action creation validates that the requested StrategyVersion is the current selected version for its Goal. Reports and multi-goal planning likewise resolve the selected StrategyVersion rather than treating the latest StrategyRun as current authority.

## 17. Code Ownership

- Strategy API: `backend/api/strategy.py`
- Strategy Version API: `backend/api/strategy_version.py`
- Request contracts: `backend/schemas/strategy.py`
- Strategy orchestration: `backend/services/strategy_service.py`
- StrategyVersion creation/parameter validation: `backend/services/strategy_version_service.py`
- Strategy Engine: `backend/engines/strategy/engine.py`
- Eligibility/applicability: `backend/engines/strategy/applicability.py`
- Decision policy: `backend/rules/strategy_decision.py`
- Selection authority: `backend/data/strategy_repository.py`
- StrategyVersion model: `backend/models/strategy_version.py`
- Frontend contract: `frontend/lib/api/strategy.ts`

## 18. Regression Contract

Build: Goal ownership, DefinedGoal requirement, priority requirement and current Financial State context must be enforced.

Eligibility: only eligible strategies enter the applicable set; pass/conditional/fail remains distinct from Goal funding status.

Decision: failed eligibility receives infeasible score; decision dimensions remain separated; ranking is not current authority.

Selection: selected strategy/scenario must belong to the same run and architecture must match the selected strategy.

Finalization: exact DefinedGoal version is required; stale versions are rejected; architecture and StrategyRun provenance are required; implementation parameters are validated.

Current authority: goal_strategy_selections must point to a StrategyVersion bound to the current DefinedGoal; stale versions resolve as non-current.

Immutability: StrategyVersion is never updated in place; investor edits require parent_version; historical versions remain available.

## 19. Important Boundaries

1. StrategyRun ≠ current strategy; it is evaluation/history.
2. Recommendation ≠ approval; recommendation is decision output.
3. Selection ≠ final implementation; finalization creates StrategyVersion.
4. StrategyVersion ≠ StrategyRun; it is the immutable implementation snapshot.
5. Ranking ≠ authority.
6. Goal Planner ≠ Strategy Builder; Goal Planner defines/funds the goal, Strategy Builder evaluates strategy suitability.
7. Financial State ≠ strategy context; Financial State remains authoritative.
8. Eligibility ≠ feasibility; strategy eligibility and Goal Planner feasibility are distinct.

## 20. End-to-End Contract

Current DefinedGoal + Current Financial State + Investor Priorities → Rules/Constraints/Risk Evidence → Eligible Strategies → Scenarios → Comparison → Decision Scoring → Ranking → Recommendation → Architecture → User Selection → Implementation Preview → Finalization → Immutable StrategyVersion → goal_strategy_selections → Current Strategy Authority → Action Plan / Reports / Execution.

Scope: this update is limited to Strategy Builder. Other feature documents are intentionally untouched in this step.