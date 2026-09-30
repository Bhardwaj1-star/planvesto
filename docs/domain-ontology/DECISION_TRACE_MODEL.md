# Decision Trace Model: Auditability, Provenance & Evidence Thread

> **Document Status:** Authoritative Audit & Target Architecture  
> **Source Primary Reference:** `docs/domain-ontology/CODE_FIRST_DOMAIN_ONTOLOGY.md`  
> **Audit Scope:** Across `backend/models/`, `backend/engines/strategy/`, `backend/services/`, `backend/data/`  
> **Core Principle:** Code-first truth. Auditing the unbroken chain of evidence from Input to Execution.

---

## 1. Canonical Decision Trace Thread

An agentic financial planning system requires full bidirectional auditability: every recommendation, action, and financial state modification must be explainable by tracing back to the inputs, rules, calculations, and constraints that produced it.

```text
[1. INPUT]
FinancialState Snapshot (financial_state_snapshots) + Goal Definition (defined_goals)
       │
       ▼
[2. RULE]
Policy Thresholds (rules/constraints.py) + Goal Taxonomy (rules/goals.py)
       │
       ▼
[3. CALCULATION]
Future Target, Inflation Compounding & Funding Gap (engines/goal/funding_gap.py)
       │
       ▼
[4. CANDIDATE]
Applicable Strategies Filtered (engines/strategy/applicability.py)
       │
       ▼
[5. CONSTRAINT & ELIGIBILITY]
8 Authoritative Fits Evaluated (engines/strategy/eligibility.py)
       │
       ▼
[6. SCENARIO]
Baseline & Custom Variants Simulated (engines/strategy/scenario.py)
       │
       ▼
[7. TRADE-OFF]
Multi-Goal Surplus Competition Evaluated (engines/allocation/engine.py)
       │
       ▼
[8. DECISION]
DecisionResult: Best Architecture Selected (engines/strategy/decision.py)
       │
       ▼
[9. STRATEGY VERSION]
Immutable Parameter Snapshot Committed (models/strategy_version.py)
       │
       ▼
[10. ACTION]
Deterministic ActionPlanItems Generated (rules/action_plan.py)
       │
       ▼
[11. EXECUTION AUDIT]
ActionDecisionRecord Persisted (models/action_plan.py)
```

---

## 2. Granular Traceability Audit Across Pipeline Steps

The table below audits what provenance data is currently tracked in source code vs. what is missing or implicit across each step in the decision chain:

| Pipeline Step | Domain Entity / Record | Provenance Identifiers Present | What is Currently Traceable | What is Missing / Implicit | Trace Status |
|---|---|---|---|---|---|
| **1. Input** | `FinancialState`<br>`DefinedGoal` | `snapshot_id`<br>`goal_id`<br>`version` | Financial inputs and goal targets are timestamped and versioned. | Scope (`family` vs `individual`) is tracked, but input attribution to specific household members is unevidenced. | `CANONICAL` |
| **2. Rule** | `RuleAssessment`<br>`rules/moneywheel.py` | `rule_set_version = '1.3'`<br>`rule_id`<br>`severity` | Rule diagnostics list contains rule ID, pass/fail status, and evidence payload. | Rule versioning is isolated to Moneywheel; other rule files (`constraints.py`, `goals.py`) lack explicit semver strings. | `IMPLICIT` |
| **3. Calculation** | `DefinedGoalAssetMapping`<br>`funding_gap` | `mapping_id`<br>`defined_goal_id` | Compounding formulas, inflation rates, and asset return assumptions are stored on `DefinedGoal`. | Fallback return assumptions used when asset return is missing are not explicitly flagged in metadata. | `CANONICAL` |
| **4. Candidate** | `StrategyRun.applicable_strategies` | `strategy_run_id`<br>`strategy_id` | Applicable strategies matching canonical goal type are embedded directly into `StrategyRun`. | Reason why an inactive or obsolete strategy was skipped is not persisted in the run record. | `CANONICAL` |
| **5. Constraint & Eligibility** | `EligibilityAssessment`<br>`ArchitectureEvaluation` | `fit`<br>`status`<br>`required_changes` | Every candidate architecture records pass/conditional/fail for all 8 fits and required adaptation text. | Hard constraint breaches are recorded, but historical snapshot of the exact constraint evaluator state is transient. | `CANONICAL` |
| **6. Scenario** | `Scenario` | `scenario_id`<br>`strategy_id`<br>`is_investor_modified` | Scenarios track monthly funding structures, return assumptions, and whether investor customized them. | Sensitivity analysis (e.g. +/- 2% return impact) is not generated or stored. | `CANONICAL` |
| **7. Trade-Off** | `ConsolidatedAllocationResult`<br>`GoalResolution` | `goal_id`<br>`resolved_priority`<br>`shortfall` | Identifies whether resource competition was detected and records trade-off notes for subordinated goals. | Interactive trade-off alternatives (what-if scenarios) are not stored as structured artifacts. | `PROVISIONAL` |
| **8. Decision** | `DecisionResult`<br>`StrategyRecommendation` | `recommended_strategy_id`<br>`recommended_architecture_id` | Complete scoring breakdown (goal fit, horizon fit, funding fit, feasibility score) is preserved in `evaluations`. | Fully traceable. Pass precedence over Conditional is auditable via score logs. | `CANONICAL` |
| **9. Strategy Version** | `StrategyVersion`<br>`PrimaryStrategyState` | `strategy_version_id`<br>`parent_version`<br>`approval_snapshot_id` | Selected parameters are locked into an immutable version with reference to parent version and approval ID. | Fully auditable lineage of strategy edits and primary designations. | `CANONICAL` |
| **10. Action** | `ActionPlanItem` | `action_id`<br>`strategy_version_id` | Actions link directly to the strategy version that created them; planned impact is pre-calculated. | `ActionPlanItem` has NO direct `goal_id` column; goal association must be resolved indirectly via `StrategyVersion`. | `IMPLICIT` |
| **11. Execution Audit** | `ActionDecisionRecord` | `decision_id`<br>`action_id`<br>`confirmed_at` | Stores `before_state`, `after_state`, and `decision` verb (`confirm`, `modify`, `complete`). | **CRITICAL GAP:** `complete` decision records `actual_impact`, but does not create a new `financial_state_snapshot_id`. | `MISSING` |

---

## 3. Detailed Evidence from Source Code

### 3.1 Trace from DefinedGoal to StrategyRun
In [`backend/models/strategy.py:170-176`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/models/strategy.py#L170-L176):
```python
class StrategyRun(BaseModel):
    strategy_run_id: str | None = None
    planning_unit_id: str
    goal_id: str
    defined_goal_id: str
    defined_goal_version: int
    run_version: int
    is_latest: bool
```
- **Evidence:** `defined_goal_id` and `defined_goal_version` explicitly bind the StrategyRun to the exact calculated goal version.
- **Trace Gap:** Notice that `financial_state_snapshot_id` is missing as a top-level typed attribute, stored only implicitly inside `run_metadata: dict`.

### 3.2 Trace from StrategyRun to StrategyVersion
In [`backend/services/strategy_service.py:100-125`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/services/strategy_service.py#L100-L125):
```python
    # Creates immutable version from selected strategy
    version = self.version_service.create_version(
        planning_unit_id=planning_unit_id,
        strategy_id=selected_strategy_id,
        source="investor_edit" if custom_params else "library",
        implementation_parameters=params,
    )
```
- **Evidence:** Explicitly preserves whether the parameters originated from the standard library or client modification.

### 3.3 Trace from StrategyVersion to ActionPlanItem
In [`backend/models/action_plan.py:11-20`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/models/action_plan.py#L11-L20):
```python
class ActionPlanItem(BaseModel):
    action_id: str | None = None
    planning_unit_id: str
    strategy_version_id: str
    title: str
    description: str | None = None
    priority: Literal["high", "medium", "low"]
    status: ActionStatus = "planned"
```
- **Evidence:** Every generated action item carries `strategy_version_id`, maintaining direct lineage back to the strategy approval.

### 3.4 Trace from Action Execution to State Feedback (Broken Link)
In [`backend/services/action_plan_service.py:123-135`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/services/action_plan_service.py#L123-L135):
```python
    updated = self.repository.update_action(
        action.planning_unit_id, action.action_id,
        {"status": "completed", "actual_impact": actual_impact},
    )
    record = self.repository.record_decision(ActionDecisionRecord(
        planning_unit_id=action.planning_unit_id,
        action_id=action.action_id,
        decision="complete",
        before_state=action.model_dump(mode="json"),
        after_state=updated.model_dump(mode="json"),
        impact_preview=completion_preview,
    ))
```
- **Trace Gap Evidence:** The completion record preserves the `after_state` of the *action item*, but does not write to `FinancialStateSnapshotRepository`. Thus, querying the latest `FinancialState` does not reflect the action's execution.

---

## 4. Current Implementation vs. Target Canonical Model

### Current Implementation:
- Strong forward and backward traceability between `DefinedGoal` ➔ `StrategyRun` ➔ `StrategyVersion` ➔ `ActionPlanItem` ➔ `ActionDecisionRecord`.
- Weak trace between `StrategyRun` and `FinancialState` (missing top-level foreign key).
- Missing feedback trace from `ActionPlanItem:completed` back to a new `FinancialStateSnapshot`.

### Target Canonical Model:
- **Unbroken Bidirectional Traceability Envelope:**
  Every `StrategyRun` carries explicit `financial_state_snapshot_id`.
  Every `ActionPlanItem` carries explicit `goal_id` alongside `strategy_version_id`.
  Every completed action produces a new `FinancialStateSnapshot` carrying `trigger_action_id`.

---

## 5. Gaps & Refactoring Implications

1. **Add `financial_state_snapshot_id` to `StrategyRun`:** Explicitly declare this field in `models/strategy.py:StrategyRun` instead of burying it in `run_metadata`.
2. **Add `goal_id` to `ActionPlanItem`:** Allow immediate indexing and querying of action items by financial goal.
3. **Emit Snapshot on Action Completion:** Let `complete_action_with_actual_state` create an official `FinancialStateSnapshot` with `source = 'action_completion'` and `source_action_id = action.action_id`.
4. **Add Rule Engine Version Headers:** Introduce `RULE_VERSION = "1.0"` across `rules/constraints.py`, `rules/goals.py`, `rules/eligibility.py`, and `rules/strategy_decision.py` so that every `StrategyRun` records the exact rule versions that governed its decisions.
