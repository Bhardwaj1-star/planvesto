# Planvesto Backend — Blueprint Gap Analysis

## Purpose

This document compares the **current backend architecture** with the uploaded **Financial Decision Engine System Creation Blueprint — Updated**.

This is a gap-analysis document, not a rebuild plan.

The existing backend should be preserved where its responsibility already matches the blueprint. The objective is to identify:

- what already exists;
- what is only partially implemented;
- what is missing;
- where the current Strategy Builder differs from the blueprint;
- what must be completed before the backend can represent the intended Financial Decision Engine.

---

# 1. Blueprint Target Flow

The blueprint defines the complete decision cycle as:

```text
FINANCIAL STATE
      ↓
GOALS
      ↓
CONSTRAINTS
      ↓
PROPOSED ACTION / PROBLEM
      ↓
STRATEGY ENGINE
      ↓
CALCULATION ENGINE
      ↓
SCENARIO ENGINE
      ↓
PROBABILITY / UNCERTAINTY
      ↓
OPTIMIZATION
      ↓
EXPLAINABILITY
      ↓
DECISION OPTIONS
      ↓
INVESTOR DECISION
      ↓
UPDATED FINANCIAL STATE
```

The blueprint explicitly defines Strategy Engine as the layer that **generates possible financial paths**, not merely the layer that selects a pre-existing strategy. Calculation and Scenario engines then evaluate those paths. fileciteturn69file0L131-L155

---

# 2. Current Backend — High-Level Position

The current backend already contains substantial infrastructure for:

- Financial State
- Goals
- Financial calculations
- Constraints
- Moneywheel / financial metrics
- Strategy Library
- Strategy eligibility
- Strategy applicability
- Strategy decision/scoring
- Strategy scenarios
- Action-plan generation
- Multi-goal structures
- Strategy versioning / runs
- Reporting structures

Therefore this is **not an empty architecture**.

The main gap is that the current implementation is more mature as a **strategy selection and planning system** than as the complete dynamic Financial Decision Engine described in the blueprint.

---

# 3. Layer-by-Layer Gap Map

| Blueprint Layer | Current Backend | Status | Main Gap |
|---|---|---|---|
| Common Financial Data Model | Existing investor/financial-state/goal/assets/liabilities structures | 🟢 | Verify full normalization and derived-vs-raw separation |
| Financial State | Existing | 🟢 | Need complete coverage of blueprint inputs |
| Goals | Existing | 🟢 | Goal flexibility/versioning should be fully connected to decisions |
| Constraints | Existing | 🟢 | Centralization done; final business policies still evolving |
| Proposed Action / Problem | Partial | 🟠 | Not yet a first-class driver of every strategy-building cycle |
| Strategy Engine | Existing | 🟠 | Current emphasis is applicability/eligibility/selection; blueprint requires path generation |
| Calculation Engine | Existing | 🟠 | Goal/strategy calculations exist; needs broader strategy-level consequence evaluation |
| Scenario Engine | Partial | 🟠 | Scenario infrastructure exists but is not yet the full evaluation layer for every strategy path |
| Probability / Uncertainty | Limited/partial | 🔴 | Not yet a complete decision-layer capability |
| Optimization | Partial | 🟠 | Scoring exists; broader trade-off optimization is not yet complete |
| Explainability | Partial | 🟠 | Results/reasons exist, but full explainability layer is not yet established |
| Decision | Partial | 🟠 | Strategy decision exists; investor decision record is not yet the full blueprint cycle |
| Updated Financial State | Partial | 🟠 | Persistence exists, but complete post-decision feedback loop is not the core active cycle |
| Action Plan | Existing/partial | 🟠 | Structure exists; final condition → action policy remains to be finalized |
| Multi-Goal | Existing/partial | 🟠 | Central rules exist; complete optimization/allocation behaviour remains to be finalized |

---

# 4. Financial State — Target vs Current

## Blueprint requires

Financial State should represent the investor's current reality, including:

- income
- expenses
- surplus
- cash/liquidity
- assets
- liabilities
- existing investments
- dependents
- commitments
- insurance/protection
- locked assets
- tax obligations
- net worth

These are intended as evidence describing the current state. fileciteturn69file0L48-L67

## Current position

The backend already has Financial State, assets, liabilities, income and expenses, plus derived financial metrics.

## Gap

The main requirement is **completeness and authority**, not another Financial State engine.

Financial State must remain the starting snapshot consumed by every decision cycle.

---

# 5. Goal Engine — Target vs Current

## Blueprint requires

Goals provide:

- type
- target amount
- target date
- current funding
- contribution
- criticality
- priority
- date flexibility
- amount flexibility
- funding flexibility
- expected outcome
- funding source
- shortfall tolerance
- version/history

The blueprint treats goals as dynamic and requires current active versions to drive decisions. fileciteturn69file0L71-L103

## Current position

Goal structures and goal calculations already exist.

## Gap

The remaining work is primarily to ensure **goal flexibility and goal versions actually influence Strategy generation, Calculation, Optimization and Decision** rather than merely existing as stored data.

---

# 6. Constraints — Target vs Current

## Blueprint requires

Constraints define what can and cannot change.

They may apply at:

- global level
- goal level
- action level

They can be hard/soft and fixed/flexible. fileciteturn69file0L120-L128

## Current position

The backend has a centralized constraint/rule structure and constraint evaluation.

## Gap

The architecture is ready; the remaining work is to finalize **which Planvesto constraints are hard, which are soft, and how each affects strategy generation and comparison**.

---

# 7. Proposed Action / Problem — Major Gap

The blueprint introduces an important input that is not merely a goal:

> What am I considering?

An investor may propose an action/change, and the system should test it against the current state, goals and constraints. fileciteturn69file0L25-L43

Examples from the blueprint include:

- investing a lump sum;
- increasing contribution;
- changing allocation;
- prepaying debt;
- changing a goal date;
- reducing a target.

## Current gap

The current Strategy Builder is primarily **goal-driven**.

The blueprint requires a broader **problem/action-driven decision mode** as well.

This should not replace the existing Goal Planner; it should become another valid input to the decision engine.

---

# 8. Strategy Engine — Most Important Gap

## Blueprint definition

Strategy is a possible financial path from the current state toward a goal/problem.

The blueprint explicitly includes strategy types such as:

- contribution strategy
- goal strategy
- capital deployment strategy
- debt strategy
- portfolio strategy
- cash-flow strategy
- combination strategy
- withdrawal strategy

The engine should generate relevant combinations rather than blindly generating every possible combination. Rules and constraints should reduce the search space. fileciteturn69file0L156-L171

## Current backend position

The current system has a Strategy Library plus applicability, eligibility and decision/scoring layers.

## Gap

The major conceptual gap is:

```text
CURRENT
Strategy Library
       ↓
Applicable / Eligible Strategies
       ↓
Score / Select
```

versus:

```text
BLUEPRINT
Current State + Goal + Constraints + Problem/Action
       ↓
Generate possible strategy paths
       ↓
Evaluate each path
       ↓
Compare paths
       ↓
Decision options
```

Therefore, **do not immediately add more selection rules** until we decide how Strategy Generation should work within the existing architecture.

---

# 9. Calculation Engine — Gap

## Blueprint role

The Calculation Engine answers:

> What does each strategy mathematically produce?

The blueprint expects calculations such as:

- future value;
- required contribution;
- required return;
- debt interest saved;
- cash-flow changes;
- portfolio projection;
- goal funding impact;
- combination strategy outcomes.

Each strategy should be quantitatively evaluated. fileciteturn69file0L203-L220

## Current position

The backend already has reusable calculation engines for goals and strategy scenarios.

## Gap

The missing piece is **unifying calculations around a generated Strategy object**, so every candidate strategy can be evaluated consistently.

---

# 10. Scenario Engine — Gap

## Blueprint role

Scenario testing asks:

> What if conditions change?

Examples:

- lower/base/higher returns;
- different contribution levels;
- different goal dates;
- different target amounts;
- different repayment dates;
- different portfolio outcomes.

The blueprint expects strategy-specific scenarios with explicit assumptions. fileciteturn69file0L203-L220

## Current position

Scenario infrastructure exists.

## Gap

It needs to become a standard evaluation stage for **all relevant generated strategies**, not only a specialized strategy scenario/report path.

---

# 11. Probability / Uncertainty — Major Missing Layer

The blueprint explicitly includes:

```text
Scenario
   ↓
Probability / Uncertainty
   ↓
Optimization
```

and defines uncertainty as part of the decision architecture. fileciteturn69file0L131-L151

## Current position

There is no equivalent fully developed probability/uncertainty decision layer in the current backend.

## Status

🔴 **Future capability — not required to invent during structural cleanup.**

This must later be designed around the actual Planvesto methodology rather than adding arbitrary statistical machinery.

---

# 12. Optimization — Partial

## Blueprint role

Optimization should compare strategies across:

- goal fit
- cash-flow fit
- liquidity fit
- debt fit
- portfolio fit
- risk fit
- flexibility fit
- outcome quality
- trade-offs

It should not simply maximize return. The output should preferably expose grouped/ranked best-fit options with reasons. fileciteturn69file0L222-L237

## Current position

The backend has strategy decision/scoring rules.

## Gap

Current scoring should eventually expand into the blueprint's broader **trade-off comparison model**.

Do not assume the existing score is the final Planvesto optimization model.

---

# 13. Explainability — Partial

## Blueprint role

The system must explain:

- what happened;
- why a strategy was considered;
- why another strategy was rejected;
- what assumptions were used;
- what trade-offs exist;
- what changes would alter the result.

The blueprint explicitly places Explainability after optimization and before decision options. fileciteturn69file0L238-L249

## Current position

Some strategy reasoning and result metadata exist.

## Gap

There is not yet a clearly separated, complete Explainability layer responsible for the whole decision chain.

---

# 14. Decision — Partial

## Blueprint definition

The system should expose decision options and consequences; the investor makes the final decision.

The system should not silently decide the investor's goals or preferences. fileciteturn69file0L16-L43

## Current position

Strategy decision/scoring exists.

## Gap

There is a distinction that must remain explicit:

```text
System decision support
≠
Investor's final decision
```

The backend needs a complete decision record containing selected option, relevant strategy, assumptions and outcome/impact.

---

# 15. Updated Financial State / Feedback Loop — Partial

The blueprint closes the cycle by updating Financial State after execution and preserving history. fileciteturn69file0L238-L249

## Current position

Financial state persistence and snapshots exist.

## Gap

The complete operational loop is not yet the primary workflow:

```text
Decision
   ↓
Execution / actual change
   ↓
Updated Financial State
   ↓
Re-analysis
```

This is a later production capability, not a reason to redesign the current architecture now.

---

# 16. Report Structure vs Decision Engine

The three reporting concepts being prepared are:

```text
Complete Financial Report
Goal Report
Planning Basket Report
```

These are **reporting/output layers**.

They should not become separate decision engines.

Correct relationship:

```text
Financial State
Goals
Constraints
Strategies
Calculations
Scenarios
Optimization
Decision
        ↓
REPORTING LAYER
        ├── Complete Financial Report
        ├── Goal Report
        └── Planning Basket Report
```

The report should explain the decision system's outputs; it should not recreate the financial calculations independently.

---

# 17. What We Should NOT Do Yet

Do not:

- rebuild Financial State;
- rebuild Goal Engine;
- create separate engines for every goal;
- replace the current Strategy Library;
- add arbitrary return assumptions;
- create a new scoring system without business approval;
- build probability models without a defined methodology;
- make reports calculate their own financial truth;
- redesign the database merely to match the blueprint wording;
- rewrite working backend connections.

The blueprint itself says reusable calculations should be created rather than duplicating formulas, assumptions should be explicit, and optimization should not equal highest return. fileciteturn69file0L265-L330

---

# 18. Correct Next Development Sequence

## Phase A — Architecture Gap Closure

1. Confirm Financial State is the canonical starting snapshot.
2. Confirm Goals are current-version driven.
3. Confirm Constraints are centralized.
4. Confirm Proposed Action/Problem has a clear place in the model.
5. Confirm Strategy object can represent a possible financial path.
6. Confirm Calculation Engine can evaluate any supported Strategy.
7. Confirm Scenario Engine can evaluate strategy-specific scenarios.

## Phase B — Strategy Generation

1. Define strategy-generation inputs.
2. Define strategy types.
3. Define what variables each strategy can change.
4. Define which combinations are permitted.
5. Use rules/constraints to reduce the search space.
6. Keep generation separate from selection.

## Phase C — Evaluation

```text
Strategy
   ↓
Calculation
   ↓
Scenario
   ↓
Constraint Validation
   ↓
Trade-off Metrics
```

## Phase D — Optimization / Decision

1. Compare candidate strategies.
2. Apply finalized Planvesto decision rules.
3. Produce explainable decision options.
4. Preserve investor choice.
5. Store the decision.

## Phase E — Reporting

Generate:

```text
Complete Financial Report
Goal Report
Planning Basket Report
```

from the same underlying decision/result objects.

---

# 19. Final Architecture Target

```text
                  FINANCIAL STATE
                         ↓
                       GOALS
                         ↓
                    CONSTRAINTS
                         ↓
             PROBLEM / PROPOSED ACTION
                         ↓
                STRATEGY GENERATION
                         ↓
                 STRATEGY CANDIDATES
                         ↓
                    CALCULATION
                         ↓
                     SCENARIO
                         ↓
              CONSTRAINT / VALIDATION
                         ↓
              OPTIMIZATION / TRADE-OFF
                         ↓
                  EXPLAINABILITY
                         ↓
                  DECISION OPTIONS
                         ↓
                 INVESTOR DECISION
                         ↓
              UPDATED FINANCIAL STATE
                         ↓
                    RE-ANALYSIS
```

Then:

```text
DECISION / RESULTS
       ↓
 ┌─────┼──────────────┐
 ↓     ↓              ↓
Complete Goal     Planning
Report   Report      Basket Report
```

---

# 20. Bottom Line

The current backend should **not be treated as broken**.

It already has much of the required infrastructure.

The main architectural gap is the transition from:

```text
Strategy Library
      ↓
Eligibility
      ↓
Scoring / Selection
```

toward:

```text
State + Goal + Constraints + Problem/Action
      ↓
Generate possible paths
      ↓
Calculate consequences
      ↓
Scenario-test
      ↓
Compare trade-offs
      ↓
Explain
      ↓
Present decision options
      ↓
Investor decides
```

**This gap must be closed deliberately. It should not be solved by adding random new engines.** Existing modules should be reused wherever their responsibility already matches the blueprint.

## Source of Truth

Primary reference for this gap analysis:
**Financial Decision Engine System Creation Blueprint — Updated** (uploaded project blueprint).
