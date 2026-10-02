# Planvesto Canonical Domain Model

## Status

- Repository: `Bhardwaj1-star/planvesto`
- Branch: `backend-audit-cleanup`
- Basis: code-first audit from `CODE_FIRST_DOMAIN_ONTOLOGY.md`, verified against repository source
- Scope: domain consolidation only; no production-code changes
- Principle: preserve business meaning while reducing implementation-level concepts

---

# 1. Executive Conclusion

The repository contains substantially more implementation models than canonical business concepts. The minimum canonical domain model is:

```text
PlanningUnit
├── FinancialState
├── InvestorProfile / Preferences
├── Goal
│   └── GoalFunding
├── StrategyDefinition
├── StrategyArchitecture
├── Scenario
├── Decision
├── StrategyVersion
└── ActionPlan
```

Everything else should be classified as a value object, derived result, catalog/reference object, rule, calculation, workflow artifact, read model, or history/audit record.

The most important architectural correction is to establish `Decision` as a genuine domain concept, make `FinancialState` the single quantitative source of truth, reduce goal/result models into state plus calculations, and make the sequence `Applicability → Eligibility → Architecture → Scenario → Trade-off Evaluation → Decision` explicit.

---

# 2. Canonical Entity List

| Concept | Type | Purpose | Canonical Source | Consumers | Duplicate/Conflict | Keep/Merge/Remove |
|---|---|---|---|---|---|---|
| PlanningUnit | Aggregate identity | Defines planning scope | `planning_unit_id` across backend/API | All planning concepts | No single explicit backend domain object | **Keep / make explicit** |
| FinancialState | Aggregate/state | Current quantitative financial position | `models/financial_state.py` + financial-state engine | Goals, diagnostics, strategy, actions | Some downstream recomputation | **Keep** |
| Metric | Value object | Availability-aware numeric measurement | `models/financial_state.py` | FinancialState | None material | **Keep** |
| InvestorProfile | Entity/profile | Risk capacity, tolerance, constraints and preferences | profile models/engines | Strategy/decision | Preferences represented separately | **Keep; consolidate inputs** |
| Goal | Entity | Desired financial outcome | `DefinedGoal` and goal schemas | Allocation, strategy, decision | Goal summaries/version summaries | **Merge into Goal** |
| GoalFunding | Value object/derived state | Target, projected funding, gap, contribution | Goal engine + DefinedGoal fields | Allocation, strategy | Funding vocabulary differs | **Keep as Goal substructure** |
| GoalBasket / GoalGroup | Optional grouping | Groups goals for planning/reporting | `goal_basket.py` | Multi-goal workflows | Product need must justify it | **Keep only if product requires** |
| StrategyDefinition | Catalog/reference | Reusable strategy knowledge | strategy library/catalog | Applicability/composition | Several implementation classes | **Keep** |
| TechniqueDefinition | Catalog/reference | Reusable implementation mechanism | strategy library | Composition | None material | **Keep as catalog child** |
| StrategyArchitecture | Candidate configuration | Primary/supporting strategies and techniques | strategy composition models/engine | Eligibility/decision | StrategyComponent/StrategyPlan overlap | **Keep; absorb composition representations** |
| Scenario | Evaluation value object | One set of assumptions/funding parameters | scenario engine/models | Decision | Can be confused with StrategyVersion | **Keep** |
| Decision | Domain entity | Authoritative choice among eligible candidates | Currently represented by DecisionResult/engine output | StrategyVersion, ActionPlan, history | No first-class canonical entity | **Introduce canonical concept** |
| StrategyVersion | Immutable implementation snapshot | Locks selected strategy parameters | strategy-version model/service | Actions | Correctly distinct from Decision | **Keep** |
| ActionPlan | Execution entity | Concrete implementation work | action plan models/service | Execution/history | Action records are audit | **Keep** |
| ActionDecisionRecord | Audit/history | Records execution decisions | action service/repository | Audit/UI | Not core planning state | **Keep as history** |
| MoneywheelAssessment | Derived diagnostic | Interprets financial state | Moneywheel engine/result | Dashboard/strategy evidence | Not independent financial state | **Keep as derived result** |
| GoalAllocationPlan | Derived planning result | Allocates finite resources across goals | multi-goal allocation/orchestration | Planning UI/actions | Multiple result models | **Merge result models** |
| Diary / FinancialDecision history | Supporting history | Qualitative/history records | diary models/services | UI | Peripheral to core planning | **Keep outside core domain** |

Do **not** promote the following into canonical entities merely because classes exist:

```text
StrategyRun
StrategyRankingItem
EligibilityAssessment
ArchitectureEvaluation
DecisionResult
MultiGoalPlanResult
GoalResolution
MoneywheelResult
MoneywheelRatio
ActionImpactPreview
GoalSummary
DefinedGoalVersionSummary
RuleAssessment
```

These are primarily execution outputs, projections, evaluation records, value objects, or read models.

---

# 3. Canonical Relationship Map

```text
                    ┌──────────────────┐
                    │   PlanningUnit   │
                    └────────┬─────────┘
                             │
          ┌──────────────────┼────────────────────┐
          ▼                  ▼                    ▼
   FinancialState      InvestorProfile          Goals
          │                  │                    │
          │                  │                    ▼
          │                  │             GoalFunding State
          │                  │                    │
          └──────────┬───────┴────────────────────┘
                     ▼
              Financial Rules
                     │
                     ▼
             Strategy Candidates
                     │
          Applicability / Eligibility
                     │
                     ▼
          Strategy Architecture(s)
                     │
                     ▼
                Scenarios
                     │
                     ▼
                 Decision
                     │
                     ▼
             StrategyVersion
                     │
                     ▼
                ActionPlan
                     │
                     ▼
             Actual FinancialState
                     │
                     └──────────────► new planning state
```

## Relationship ownership

| Relationship | Meaning | Current implementation | Target owner |
|---|---|---|---|
| PlanningUnit → FinancialState | State belongs to planning scope | `planning_unit_id` | PlanningUnit / FinancialState |
| PlanningUnit → Goal | Planning scope owns goals | `DefinedGoal` | Goal |
| Goal → GoalFunding | Goal's calculated funding position | Goal engine | Goal calculation |
| FinancialState → MoneywheelAssessment | Diagnostic derived from state | Moneywheel engine/adapter | Diagnostic calculation |
| Goal → Strategy candidates | Which strategies address goal | Applicability engine | Applicability rules |
| Strategy → Eligibility | Can it operate under current conditions | Eligibility engine | Eligibility rules |
| Strategy + Goal → Architecture | How strategies compose | Composition engine | StrategyArchitecture |
| Architecture + assumptions → Scenario | Outcome under assumptions | Scenario engine | Scenario calculation |
| Candidates → Decision | Which valid option is selected | `evaluate_decision()` | Decision |
| Decision → StrategyVersion | Approved implementation snapshot | strategy-version service | Decision / StrategyVersion |
| StrategyVersion → ActionPlan | Implementation work | action generator/service | ActionPlan |
| Action → FinancialState | Execution changes actual state | currently represented through actual impact | Execution workflow → FinancialState |

The last relationship is incomplete in the current implementation: action completion validates/stores actual impact but the architecture should eventually feed the authoritative FinancialState back into the planning state.

---

# 4. Domain Boundary Map

## 4.1 Financial State

Owns:

```text
FinancialState
Metric
income
expenses
surplus
assets
liabilities
liquidity
net worth
debt burden
reserve
```

Must not own strategy selection.

## 4.2 Goals

Owns:

```text
Goal
GoalFunding
Goal priority
Goal timeline
Goal flexibility
Goal → funding allocation
```

Calculations include:

```text
duration
future target
asset projection
funding gap
required contribution
```

The current `DefinedGoal` mixes identity/input with calculated funding state; the target separates those concerns conceptually without requiring an immediate code rewrite.

## 4.3 Risk / Investor Context

Owns:

```text
Risk capacity
Risk tolerance
constraints
investor preferences
decision priorities
```

Behavioral observations remain contextual evidence rather than independent strategy-selection authorities unless code evidence later establishes otherwise.

## 4.4 Strategy Knowledge

Owns reusable catalog knowledge:

```text
StrategyDefinition
TechniqueDefinition
implementation parameter definitions
compatibility metadata
applicability metadata
```

This is a catalog, not a planning decision.

## 4.5 Strategy Evaluation

Owns transient evaluation concepts:

```text
Applicability
Eligibility
StrategyArchitecture
Scenario
```

These do not all need persistence identities.

## 4.6 Decision

Owns:

```text
eligible candidates
hard-constraint outcome
trade-off evaluation
investor preferences
scenario evidence
selected architecture
selected scenario
decision rationale
```

This is the main area where the current architecture needs conceptual clarification.

## 4.7 Execution

Owns:

```text
StrategyVersion
ActionPlan
Action lifecycle
ActionDecisionRecord
actual outcome
```

Execution must not redefine financial-state calculations.

---

# 5. Ontology vs Rules vs Calculations vs Workflow

These four categories must remain separate.

| Category | Examples |
|---|---|
| **Ontology** | PlanningUnit, FinancialState, Goal, StrategyDefinition, StrategyArchitecture, Decision, StrategyVersion, ActionPlan |
| **Rules** | Goal taxonomy, hard constraints, applicability, eligibility, compatibility, allocation precedence, decision policy |
| **Calculations** | Future target, funding gap, PMT, financial ratios, Moneywheel ratios, scenario projections, decision scores |
| **Workflow** | Build state → define goal → evaluate candidates → decide → approve version → generate actions → execute → recalculate state |

A rule should state what must hold. A calculation should derive a value. A workflow should coordinate sequence. A domain entity should represent meaningful business state.

---

# 6. Authority / Ownership Map

| Concept | Current authorities | Conflict | Recommended authority |
|---|---|---|---|
| Financial metrics | FinancialStateEngine + downstream rules | Some values reconstructed downstream | **FinancialState calculation layer** |
| Health status | Moneywheel + constraint evaluation | Threshold duplication | **Diagnostic/constraint policy** |
| Constraints | `rules/constraints.py`, moneywheel rules, RuleEngine | Potential threshold duplication | **One constraint policy set** |
| Goal funding | GoalEngine | Status vocabulary differs elsewhere | **GoalFunding calculation** |
| Goal priority | goal rules + multi-goal engine + orchestration | Multiple ranking maps | **Goal policy** |
| Risk | Profile engines | Strategy consumes pieces | **InvestorProfile / Risk context** |
| Strategy applicability | Applicability engine + rule engine | Two evaluation paths | **Applicability policy** |
| Strategy eligibility | Eligibility engine + RuleEngine | Overlap | **Eligibility policy** |
| Strategy scoring | `strategy_decision.py` | Preference input is not visibly applied in current arithmetic | **Decision policy** |
| Strategy composition | Composition engine + StrategyComponent + StrategyPlan + Architecture | Multiple representations | **StrategyArchitecture** |
| Investor priorities | `InvestorPriorities` | Passed into decision flow but not visibly incorporated into current scoring formula | **Decision policy input** |
| Scenario assumptions | Scenario engine | Some assumptions represented as generic mappings | **Scenario** |
| Decision output | DecisionResult embedded in StrategyRun | No canonical first-class decision | **Decision** |
| Action outcome | ActionPlan service | Actual impact remains attached to action | **Execution → FinancialState** |

The investor-priority issue should be treated as **CONFLICTING/INCOMPLETE**, not guessed: priorities are passed into the decision flow, but the current scoring function does not visibly weight them.

---

# 7. Duplicate & Conflict Map

## 7.1 Goal priority

Current representations include goal rules, allocation models, orchestration models and allocation engines.

Target:

```text
ONE GoalPriority vocabulary
```

## 7.2 Funding status

Current representations include statuses such as `Shortfall`, `On Track`, `Overfunded`, plus allocation-specific statuses such as `fully_funded` and `partially_funded`.

These should **not automatically be collapsed into one enum** because they may represent different semantic levels:

```text
GoalFundingStatus
AllocationStatus
```

## 7.3 Feasibility

Strategy feasibility and allocation feasibility use overlapping terminology. Verify semantic equivalence before merging. Until verified, mark the relationship **UNCERTAIN**.

## 7.4 Goal taxonomy

The current goal normalization maps several inputs to `other`, including debt repayment, while essential-goal classification independently contains `debt_repayment`. This can erase identity needed by later classification.

Target:

```text
One canonical GoalType registry
        ↓
normalization aliases
        ↓
classification policies
```

## 7.5 Priority ranking

The repository contains inconsistent numeric priority schemes (`1..4` versus `0..3`). Numeric rank is an implementation detail and should be generated from one canonical ordering.

## 7.6 Strategy composition

`StrategyComponent`, `StrategyPlan`, and `StrategyArchitecture` overlap.

Target:

```text
StrategyArchitecture
├── primary strategy
├── supporting strategies
└── techniques / implementation components
```

---

# 8. Decision Model

The canonical decision pipeline is:

```text
DecisionContext
├── FinancialState
├── InvestorProfile
├── Goal
├── applicable strategies
└── candidate scenarios

              ↓

1. Applicability
   "Can this strategy address this goal?"

              ↓

2. Eligibility
   "Can it operate under current constraints?"

   HARD FAILURE → reject
   CONDITIONAL   → adaptation required

              ↓

3. Architecture
   "What valid composition can be constructed?"

              ↓

4. Scenario Evaluation
   "What does each valid option produce under assumptions?"

              ↓

5. Trade-off Evaluation
   goal fit
   horizon fit
   funding fit
   risk fit
   liquidity
   investor preferences
   scenario outcomes

              ↓

6. Decision
   selected architecture
   selected scenario
   alternatives
   rationale
   constraints
```

## Critical separation

**Eligibility is not scoring.**

The target decision architecture is:

```text
Eligibility
    ↓
Hard admissibility

Trade-off evaluation
    ↓
Preference-sensitive comparison

Decision
    ↓
Selection
```

The current code already separates eligibility assessment from decision scoring to a meaningful degree. Preserve that distinction during refactoring.

## Current score components

The current decision score is composed from:

```text
Goal fit
+ Horizon fit
+ Funding fit
+ Feasibility
+ Component fit
= Decision score
```

The investor-priority input is structurally present in the decision flow but is not visibly incorporated into the current scoring arithmetic. This is therefore **INCOMPLETE/UNCERTAIN as an implemented business rule**.

---

# 9. Current → Target Mapping

| Current | Target |
|---|---|
| `FinancialState` | **FinancialState** |
| `Metric` | **Metric** |
| `DefinedGoal` | **Goal + GoalFunding** |
| `DefinedGoalAssetMapping` | **GoalFunding allocation** |
| `GoalSummary` | Goal projection/read model |
| `DefinedGoalVersionSummary` | Goal history/read model |
| `GoalBasket` | Optional GoalGroup |
| `MoneywheelInput` | Calculation input |
| `MoneywheelResult` | MoneywheelAssessment |
| `MoneywheelRatio` | Diagnostic value object |
| `InvestorProfile` | **InvestorProfile** |
| `InvestorPriorities` | Decision preference input |
| `StrategyDefinition` | **StrategyDefinition** |
| `TechniqueDefinition` | Strategy catalog child |
| `StrategyComponent` | Architecture composition detail |
| `StrategyPlan` | Merge/remove as separate domain concept |
| `StrategyArchitecture` | **StrategyArchitecture** |
| `Scenario` | **Scenario** |
| `EligibilityFitResult` | Eligibility assessment value object |
| `EligibilityAssessment` | Rule/evaluation result |
| `StrategyRankingItem` | Derived ranking/read model |
| `StrategyRecommendation` | Decision projection |
| `DecisionResult` | **Decision** |
| `StrategyRun` | Evaluation/run history |
| `StrategyVersion` | **StrategyVersion** |
| `PrimaryStrategyState` | Strategy activation/approval state |
| `MultiGoalPlanResult` | GoalAllocationPlan |
| `GoalResolution` | GoalAllocation |
| `ActionPlanItem` | **ActionPlan item** |
| `ActionDecisionRecord` | Execution audit/history |
| `ActionImpactPreview` | Calculation result |
| `DiaryEntry` | Supporting history |
| `FinancialDecision` | Decision history/read model |

---

# 10. Simplification Opportunities

## 10.1 Consolidate goal representations

Reduce the conceptual surface from:

```text
DefinedGoal
GoalSummary
DefinedGoalVersionSummary
GoalEvaluationInput
GoalResolution
```

to:

```text
Goal
GoalFunding
GoalAllocation
```

The latter two are derived/plan state rather than necessarily independent entities.

## 10.2 Consolidate strategy composition

Reduce:

```text
StrategyComponent
StrategyPlan
StrategyArchitecture
component contracts
```

to:

```text
StrategyArchitecture
```

with references to catalog strategies and techniques.

## 10.3 Demote StrategyRun

`StrategyRun` currently contains candidates, scenarios, rankings, recommendations, architectures and selections. Treat it as an evaluation/workflow snapshot, not the canonical strategy domain entity.

## 10.4 Demote Moneywheel

Moneywheel is a diagnostic projection of FinancialState:

```text
FinancialState
      ↓
MoneywheelAssessment
```

not a competing financial state.

## 10.5 Demote multi-goal result wrappers

Replace multiple orchestration result models conceptually with:

```text
GoalAllocationPlan
├── GoalAllocation*
├── trade-offs
└── funding outcome
```

## 10.6 Avoid pass-through abstractions

A class/service should survive consolidation only if it owns business meaning, a rule, a calculation, persistence semantics, or an application boundary. Pure forwarding wrappers should not become canonical domain concepts.

---

# 11. Target Architecture

```text
┌──────────────────────────────────────────────┐
│              CANONICAL DOMAIN                │
│                                              │
│ PlanningUnit                                  │
│ FinancialState                                │
│ InvestorProfile                               │
│ Goal + GoalFunding                            │
│ StrategyDefinition                            │
│ StrategyArchitecture                          │
│ Scenario                                      │
│ Decision                                      │
│ StrategyVersion                               │
│ ActionPlan                                    │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│                 DOMAIN RULES                 │
│                                              │
│ Goal taxonomy                                │
│ Constraints                                  │
│ Applicability                                │
│ Eligibility                                  │
│ Compatibility                                │
│ Priority / allocation rules                  │
│ Decision policy                              │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│          CALCULATION / SIMULATION            │
│                                              │
│ Financial calculations                       │
│ Goal projections                             │
│ Funding calculations                         │
│ Moneywheel diagnostics                       │
│ Scenario simulation                          │
│ Decision scoring                             │
│ Impact analysis                              │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│              APPLICATION SERVICES            │
│                                              │
│ Planning workflow                            │
│ Goal planning                                │
│ Strategy evaluation                          │
│ Decision / approval                          │
│ Action execution                             │
│ Multi-goal orchestration                     │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│                API / PERSISTENCE             │
└──────────────────────────────────────────────┘
```

## Layer constraints

### Canonical Domain

Must contain business concepts and meaningful state.

Must not contain HTTP concerns, database-specific DTOs, UI projections, or workflow orchestration.

### Domain Rules

Must express conditions/policies.

Must not own application sequencing or persistence.

### Calculation / Simulation

Must derive values from domain inputs.

Must not become alternative sources of truth for domain state.

### Application Services

Must coordinate workflows and invoke domain policies/calculations.

Must not invent business rules that belong in domain policy.

### API / Persistence

Must translate external/storage representations.

Must not become the authority for business semantics.

---

# 12. Phased Refactoring Plan

## Phase 0 — Freeze semantics

No production behavior changes.

Capture tests/characterization around:

- canonical goal types
- funding status meanings
- feasibility meanings
- eligibility semantics
- decision authority
- priority semantics

## Phase 1 — Establish vocabulary

Create one authoritative conceptual vocabulary for:

```text
GoalType
GoalPriority
FundingStatus
Feasibility
EligibilityStatus
ActionStatus
```

First map existing strings; do not immediately delete aliases.

## Phase 2 — Consolidate calculations

Establish one authority for:

```text
financial metrics
reserve thresholds
debt thresholds
goal funding
goal priority
```

Remove duplicates only after equivalence is demonstrated by tests.

## Phase 3 — Separate strategy decision stages

Explicitly isolate:

```text
Applicability
→ Eligibility
→ Architecture
→ Scenario
→ Trade-off Evaluation
→ Decision
```

Initially preserve current outputs/behavior.

## Phase 4 — Introduce first-class Decision

Move authoritative selection out of `StrategyRun`/`DecisionResult` into canonical `Decision` state.

`StrategyRun` becomes historical evaluation context.

## Phase 5 — Consolidate multi-goal planning

Move toward:

```text
GoalAllocationPlan
GoalAllocation*
TradeOff*
```

while preserving existing allocation behavior.

## Phase 6 — Close execution feedback loop

Target lifecycle:

```text
Action completed
      ↓
Actual FinancialState
      ↓
FinancialState authority
      ↓
new diagnostics / goal calculations
      ↓
planning state refreshed
```

## Phase 7 — Remove dead/duplicate abstractions

Only after migration and regression validation, remove duplicate components, priority aliases, duplicated thresholds, redundant goal summaries, unused abstractions and pass-through services.

---

# 13. Uncertainty Register

The following items should not be resolved by assumption:

| Item | Status | Required evidence |
|---|---|---|
| Whether strategy and allocation feasibility are exactly the same concept | **UNCERTAIN** | Compare all call sites and business semantics |
| Whether GoalBasket is required as a real domain concept | **UNCERTAIN** | Product/persistence usage |
| Exact intended weighting of InvestorPriorities in decision score | **INCOMPLETE** | Product/business rule or authoritative implementation |
| Whether all Moneywheel health thresholds have one intended authority | **UNCERTAIN** | Rule call graph and tests |
| Whether FinancialDecision is an event/history entity or read model | **UNCERTAIN** | Persistence and product usage |

No target architecture decision should silently convert these uncertainties into invented business rules.

---

# 14. Minimum Canonical Domain Model

If rebuilding the backend today using the existing business knowledge, the minimum canonical domain concepts are:

```text
1. PlanningUnit
2. FinancialState
3. InvestorProfile
4. Goal
5. GoalFunding
6. StrategyDefinition
7. StrategyArchitecture
8. Scenario
9. Decision
10. StrategyVersion
11. ActionPlan
```

Supporting concepts:

```text
Value Objects:
Metric, preferences, constraints, eligibility results,
diagnostic results, allocations, trade-offs

Catalog:
StrategyDefinition, TechniqueDefinition

Rules:
Goal taxonomy, financial constraints, applicability,
eligibility, composition, allocation, decision policy

Calculations:
FinancialState calculations, Goal calculations, Moneywheel,
Scenario simulation, Decision scoring, Impact analysis

Workflow:
Planning → Goal funding → Strategy evaluation → Decision
→ Strategy approval → Action execution → FinancialState refresh
```

The current repository already contains most of the required business knowledge. The rebuild should therefore consolidate competing representations and clarify authority rather than introduce more domain entities.
