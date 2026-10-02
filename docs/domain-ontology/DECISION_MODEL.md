# Decision Model: Strategy, Eligibility, Architecture & Trade-Offs

> **Document Status:** Authoritative Audit & Target Architecture  
> **Source Primary Reference:** `docs/domain-ontology/CODE_FIRST_DOMAIN_ONTOLOGY.md`  
> **Audit Scope:** `backend/engines/strategy/`, `backend/library/strategies/`, `backend/rules/strategy_decision.py`, `backend/rules/eligibility.py`, `backend/rules/adaptation.py`, `backend/engines/allocation/`, `backend/engines/orchestration/`, `backend/services/strategy_service.py`  
> **Core Principle:** Code-first truth. Every finding verified against source code with exact file, class, function, and line evidence.

---

## 1. End-to-End Decision Flow

The Planvesto decision model progresses through an explicit multi-stage pipeline from strategy candidate retrieval to final investor selection and primary strategy assignment.

```text
1. STRATEGY CATALOG
   (backend/library/strategies/catalog.py)
   Reads all active strategies and technique definitions.
            │
            ▼
2. APPLICABILITY FILTERING
   (backend/engines/strategy/applicability.py: filter_applicable_strategies)
   Filters catalog by canonical_goal_type (rules/goals.py) and StrategyRuleEngine.evaluate.
            │
            ▼
3. ARCHITECTURE COMPOSITION
   (backend/engines/strategy/composition.py: compose_architectures)
   Composes primary strategy with supporting strategies and techniques based on component roles.
            │
            ▼
4. ELIGIBILITY EVALUATION (8 FITS)
   (backend/engines/strategy/eligibility.py: evaluate_eligibility_fits)
   Evaluates 8 mandatory fits; gates feasibility (Pass vs Conditional vs Fail).
            │
            ▼
5. CONDITIONAL ADAPTATION
   (backend/rules/adaptation.py)
   Generates structured required changes if any fit returns CONDITIONAL.
            │
            ▼
6. SCENARIO GENERATION
   (backend/engines/strategy/scenario.py: generate_baseline_scenarios)
   Generates baseline scenarios (conservative, moderate, aggressive) with monthly funding structures.
            │
            ▼
7. DECISION SCORING & SELECTION
   (backend/rules/strategy_decision.py & backend/engines/strategy/decision.py: evaluate_decision)
   Computes Total Decision Score; enforces Pass precedence over Conditional; selects Best Architecture.
            │
            ▼
8. MULTI-GOAL TRADE-OFF & ALLOCATION
   (backend/engines/allocation/engine.py: ResourceAllocationEngine)
   Allocates available surplus across competing goals; records trade-off impacts.
            │
            ▼
9. RECOMMENDATION & RANKING
   (backend/engines/strategy/recommendation.py & ranking.py)
   Generates explainable recommendation payload (reasons, constraints, alternatives).
            │
            ▼
10. INVESTOR SELECTION & PRIMARY STRATEGY TRANSITION
   (backend/services/strategy_service.py & models/primary_strategy.py)
   Locks chosen strategy into immutable StrategyVersion and updates PrimaryStrategyState.
```

---

## 2. Decision Pipeline Stages & Code Evidence

### Stage 1: Strategy Library Knowledge
- **Location:** [`backend/library/strategies/catalog.py`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/library/strategies/catalog.py) and [`backend/library/strategies/techniques.py`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/library/strategies/techniques.py)
- **Role:** Pure catalog of reusable financial strategies (e.g. `bucket_strategy`, `aggressive_growth`, `debt_avalanche`).
- **Classification:** `CANONICAL`. Contains no client-specific decision logic.

### Stage 2: Applicability Filtering
- **Location:** [`backend/engines/strategy/applicability.py:16-40`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/engines/strategy/applicability.py#L16-L40) (`filter_applicable_strategies`)
- **Role:** Selects candidate strategies matching the goal. Calls `_rule_engine.canonical_goal_type(goal_type)` and checks `strategy.applicable_goal_types`.
- **Classification:** `CANONICAL`. Gated strictly by goal type; component activation cannot disqualify an applicable strategy.

### Stage 3: Architecture Composition
- **Location:** [`backend/engines/strategy/composition.py:1-75`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/engines/strategy/composition.py#L1-L75) (`compose_architectures`)
- **Role:** Pairs an applicable primary strategy with compatible supporting strategies and techniques (e.g. pairing `bucket_strategy` with `tech_stp` or `tech_swp`).
- **Classification:** `CANONICAL`. Evaluates component compatibility via [`engines/strategy/components/compatibility.py`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/engines/strategy/components/compatibility.py).

### Stage 4: Eligibility Assessment (The 8 Fits)
- **Location:** [`backend/engines/strategy/eligibility.py:69-128`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/engines/strategy/eligibility.py#L69-L128) (`evaluate_eligibility_fits`)
- **Authoritative Definition:** [`backend/rules/eligibility.py:14-23`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/rules/eligibility.py#L14-L23) (`ELIGIBILITY_FITS`)
- **The 8 Mandatory Fits:**
  1. `cashflow_fit`: Monthly required strategy contribution $\le$ available surplus.
  2. `liquidity_fit`: Liquid assets $\ge$ required emergency reserve.
  3. `debt_fit`: Debt payments serviceable under available surplus.
  4. `asset_resource_fit`: Available assets $\ge$ strategy resource requirements.
  5. `risk_capacity_fit`: Strategy required risk $\le$ investor risk capacity.
  6. `goal_constraint_fit`: Goal horizon and funding gap satisfy strategy constraints (`_goal_gate()`).
  7. `multi_goal_conflict_fit`: Evaluates whether higher-priority goals are compromised.
  8. `implementation_fit`: Confirms operational feasibility of required action items.
- **Classification:** `CANONICAL`. Evaluated independently for every candidate architecture.

### Stage 5: Conditional Adaptation
- **Location:** [`backend/rules/adaptation.py:1-150`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/rules/adaptation.py#L1-L150)
- **Role:** Generates precise formatting for required financial adjustments (e.g., `format_cashflow_adaptation`, `format_liquidity_adaptation`, `format_resource_adaptation`).
- **Classification:** `CANONICAL`. Translates numeric deficits into concrete investor instructions.

### Stage 6: Scenario Generation
- **Location:** [`backend/engines/strategy/scenario.py:1-90`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/engines/strategy/scenario.py#L1-L90) (`generate_baseline_scenarios`)
- **Role:** Simulates 3 baseline variants (Conservative, Moderate, Aggressive) with deterministic returns, calculating required monthly contribution and projected funding.
- **Classification:** `CANONICAL`. Also supports custom investor scenario creation via `create_custom_scenario()`.

### Stage 7: Decision Scoring & Selection Authority
- **Location:** [`backend/rules/strategy_decision.py`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/rules/strategy_decision.py) & [`backend/engines/strategy/decision.py:53-103`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/engines/strategy/decision.py#L53-L103) (`evaluate_decision`)
- **Scoring Breakdown:**
  $$\text{Total Score} = \text{Goal Fit} + \text{Horizon Fit} + \text{Funding Fit} + \text{Feasibility Score} + \text{Component Fit}$$
  - $\text{Feasibility Score}$: `pass` = +50.0; `conditional` = +25.0; `fail` = -100.0.
  - If status is `fail`, `evaluate_decision_score` immediately overrides total score to `-100.0` (`INFEASIBLE_DECISION_SCORE`).
- **Selection Precedence:**
  - Evaluates `passes` vs `conditionals`.
  - Pass pool takes strict precedence over Conditional pool.
  - Ineligible strategies (`fail`) are never recommended.
- **Classification:** `CANONICAL`. Verified by [`tests/test_strategy_decision_authority.py`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/tests/test_strategy_decision_authority.py).

### Stage 8: Multi-Goal Trade-Off & Allocation
- **Location:** [`backend/engines/allocation/engine.py:25-110`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/engines/allocation/engine.py#L25-L110) (`ResourceAllocationEngine.allocate`)
- **Role:** When multiple goals compete for a finite monthly surplus, sorts goals by priority rank and sequential target dates. Deducts contributions until surplus is exhausted.
- **Preemption Rule:** [`rules/multi_goal.py:can_discretionary_preempt_essential()`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/rules/multi_goal.py#L26) ensures discretionary goals cannot take funding from essential goals.
- **Classification:** `CANONICAL`.

### Stage 9: Recommendation & Ranking Separation
- **Location:** [`backend/engines/strategy/ranking.py`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/engines/strategy/ranking.py) & [`backend/engines/strategy/recommendation.py`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/engines/strategy/recommendation.py)
- **Role:** `rank_scenarios()` calculates dimension scores based on `InvestorPriorities` for comparative display. `generate_recommendation()` derives recommendation strictly from `DecisionResult`, NOT from composite ranking scores.
- **Classification:** `CANONICAL`. Prevents preference weights from overruling eligibility evidence.

### Stage 10: Investor Selection & Primary Strategy Transition
- **Location:** [`backend/services/strategy_service.py:100-140`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/services/strategy_service.py#L100-L140) & [`backend/models/primary_strategy.py`](file:///C:/Users/lenovo/.gemini/antigravity/scratch/planvesto/backend/models/primary_strategy.py)
- **Role:** Persists selected strategy as an immutable `StrategyVersion` in `data/strategy_version_repository.py`. Updates `PrimaryStrategyState` and archives previous primary version.
- **Classification:** `CANONICAL`.

---

## 3. Missing and Implicit Decision Steps

Comparing the current backend implementation with the intended Financial Decision Engine Blueprint reveals key missing or implicit decision steps:

| Decision Step | Expected Blueprint Capability | Current Code Reality | Status | Evidence |
|---|---|---|---|---|
| **Probability & Uncertainty Modeling** | Monte Carlo or stochastic return simulation with probability of goal success. | Pure deterministic compound return formulas (`engines/goal/target_calculator.py`, `engines/goal/funding_gap.py`). | `MISSING` | `engines/goal/target_calculator.py:16-35` |
| **Mathematical Optimization Engine** | Linear/quadratic programming solver to find optimal asset allocation or goal funding split. | Greedy priority-ordered heuristic deduction in `ResourceAllocationEngine`. | `PROVISIONAL` | `engines/allocation/engine.py:49-85` |
| **Interactive Trade-Off Negotiation** | Interactive solver allowing investor to adjust horizon/amount sliders and see real-time trade-off options. | Backend records competition and emits warnings; solver logic does not exist. | `IMPLICIT` | `engines/orchestration/models.py:58-60` |
| **Behavioral Bias Resistance Gating** | Behavioral traits evaluate whether client can adhere to strategy execution under drawdown. | Behavioral profile is explicitly quarantined from Strategy Builder to prevent unauthorized gating. | `CANONICAL` (By Design) | `docs/behavioral-profile-rules.md:20-25` |

---

## 4. Current Implementation vs. Target Canonical Model

### Current Implementation:
- Strategy selection is cleanly separated from ranking weights (achieved in commit `30-09-2026`).
- Eligibility evaluation is standardized on 8 fits.
- However, multi-goal trade-offs use a simple greedy allocation loop without constraint optimization.
- Feasibility vocabulary conflicts between `models/strategy.py` (`conditional`) and `engines/allocation/models.py` (`constrained`).

### Target Canonical Model:
- **`DecisionResult` is the sole authority for strategy recommendations.**
- Standardize feasibility state across all single-goal and multi-goal models to: `PASS | CONDITIONAL | INFEASIBLE`.
- Connect `ResourceAllocationEngine` trade-off outputs directly to Action Plan generator to create explicit trade-off resolution actions.

---

## 5. Gaps & Refactoring Implications

1. **Reconcile Feasibility Enum:** Replace `constrained` in `engines/allocation/models.py:8` and `engines/orchestration/models.py:8` with `conditional` to match `rules/eligibility.py` and `models/strategy.py`.
2. **Standardize Strategy Component Contracts:** Delete duplicate `StrategyComponent` in `models/strategy.py:198` and maintain single definition in `engines/strategy/components/contracts.py`.
3. **Formalize Decision Tracing Object:** Add explicit `DecisionContext` embedding inputs, rule assessment IDs, and eligibility fit summaries into `StrategyRun` metadata.
