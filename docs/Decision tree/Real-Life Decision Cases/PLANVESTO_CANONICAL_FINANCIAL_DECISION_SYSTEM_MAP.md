# PlanVesto — Canonical Financial Decision System Map

**Document Type:** Product Management / Canonical System Architecture
**Status:** Business/Product Architecture Baseline
**Source:** Real-Life Decision Cases
**Scope:** End-to-end financial decision lifecycle
**Implementation Status:** Architecture defined; implementation alignment to be audited separately.

## 1. Purpose

This document defines the canonical product-level structure of PlanVesto derived from the complete Real-Life Decision Case series. The cases together define how PlanVesto should behave across financial reality, goal planning, feasibility, whole-plan impact, strategy decision, what-if analysis, revalidation, investor choice, accepted planning, action planning, and monitoring.

## 2. Product Vision

PlanVesto is not only a Strategy Builder. It is a financial decision system that takes the investor from **Current Financial Reality → Feasible Goal/Plan → Strategy → Impact Analysis → Investor Decision → Accepted Plan → Action → Adaptation**.

## 3. Canonical End-to-End Product Map

```text
FINANCIAL REALITY
  Financial State + Investor Information
        ↓
GOAL PLANNING
  Goal + Context + Goal Funding + Feasibility
        ↓
WHOLE-PLAN DECISION
  Multi-Goal + Priorities + Trade-offs
        ↓
HARD CONSTRAINTS
  Remove unacceptable paths
        ↓
STRATEGY DECISION
  Applicability → Viability → Selection
  → Variant → Technique → Architecture
        ↓
IMPACT / WHAT-IF
  Goal / Strategy / Execution alternatives
        ↓
REVALIDATION
  Does the current plan still work?
        ↓
INVESTOR DECISION
  Accept / Reject / Modify / Own Strategy
        ↓
ACCEPTED PLAN
        ↓
ACTION PLAN
        ↓
MONITORING & ADAPTATION
        ↺ targeted revalidation
```

## 4. Product Layers and Ownership

| Layer | Primary Question | Canonical Responsibility | Output |
|---|---|---|---|
| Financial State | What is financially true today? | Maintain current financial reality | Canonical financial state |
| Goal Planner | What does the investor want to achieve? | Define and contextualize goals | Defined goal |
| Goal Feasibility / Funding | Can the goal be made financially feasible? | Calculate funding gap, capacity and feasible paths | Feasibility + funding paths |
| Whole-Plan Planning | What happens to the rest of the plan? | Evaluate multi-goal conflicts and trade-offs | Whole-plan impact |
| Hard Constraint Policy | What paths are unacceptable? | Apply genuine non-negotiable constraints | Allowed / rejected paths |
| Strategy Decision | Which strategy should solve the problem? | Applicability, viability, selection | Selected strategy |
| Variant Selection | Which implementation pattern fits? | Select strategy variant | Selected variant |
| Technique Selection | Which planning techniques are needed? | Select required/conditional techniques | Technique set |
| Architecture | How should selected pieces be assembled? | Compose implementation architecture | Strategy architecture |
| Stress / Resilience | Does the plan remain acceptable under stress? | Test same decision logic under changed assumptions | Resilience assessment |
| Impact / What-If | What happens if something changes? | Model alternatives before adoption | Scenario impact |
| Revalidation | Is the existing decision still valid? | Re-check affected parts after material change | Continue / revise |
| Investor Decision | What does the investor choose? | Preserve investor agency | Accepted/rejected decision |
| Accepted Plan | What is currently approved? | Maintain active plan | Accepted plan |
| Action Plan | What needs to be done? | Convert accepted plan into actions | Action plan |
| Monitoring / Adaptation | What changed later? | Detect material changes and trigger targeted revalidation | Updated planning state |

## 5. Critical Boundary: Goal Planner vs Strategy Builder

### Goal Planner

Answers: **Can the goal be made financially feasible, and what funding path can make it feasible?**

It considers the investor's financial state, goal horizon, target, existing funding, surplus, liquidity, liabilities, competing goals and relevant financial conditions.

### Strategy Builder

Answers: **Given the feasible planning path, how should it be strategically implemented?**

It determines strategy, variant, techniques, architecture, implementation structure and strategy-level trade-offs.

```text
Financial State
      ↓
Goal Planner
      ↓
Goal Feasibility / Funding
      ↓
Whole-Plan Impact
      ↓
Strategy Builder
      ↓
Strategy → Variant → Technique → Architecture
```

**Product rule:** Strategy Builder must not independently recreate Goal Planner feasibility.

## 6. Goal Funding Is Not a Fifth Strategy

Goal Funding belongs to the **Goal Planner / Feasibility layer**. It is not a peer Strategy Builder strategy.

Canonical Strategy Builder strategies are:

1. Progressive De-risking
2. Capital Preservation
3. Debt Reduction
4. Credit Utilisation

SIP, lump sum, step-up contribution, existing assets and combinations of funding sources may be part of a feasibility/funding path; they do not automatically become Strategy Builder strategies.

## 7. Strategy Decision Subsystem

The Strategy Decision Tree is a subsystem inside the larger product architecture:

```text
Goal / Financial Context
        ↓
Goal Feasibility
        ↓
Whole-Plan Impact
        ↓
Hard Constraints
        ↓
Strategy Applicability
        ↓
Candidate Strategies
        ↓
Strategy Viability
        ↓
Strategy Selection
        ↓
Variant Selection
        ↓
Technique Selection
        ↓
Technique Method / Policy
        ↓
Architecture
        ↓
Stress / Resilience
        ↓
Decision Output
```

Applicability, viability and selection are separate decisions.

## 8. Whole-Plan Decision Layer

A goal cannot always be evaluated independently. The system must consider other active goals, priorities, shared resources, surplus allocation, timing conflicts, debt-versus-goal trade-offs and the impact of a new goal on the accepted plan.

**Proposal ≠ Adoption.** A proposed new goal is initially a scenario against the existing accepted plan.

## 9. Opportunity Cost and Better-Path Analysis

Financial metrics must not directly dictate strategy. For example, debt existing does not automatically mean Debt Reduction. The system may need to compare debt repayment, investment/goal funding, restructuring or combinations.

Opportunity-cost analysis is a decision-support capability, not a separate Strategy Builder strategy.

## 10. Financial Measurement vs Decision Rule

A measurement is not automatically a planning decision. For example, DTI is a measurement; it does not by itself mean debt must be repaid.

Canonical pattern:

**Measurement → Contextual Analysis → Decision**

not:

**Measurement → Automatic Decision**

This applies especially to Moneywheel and financial-health metrics.

## 11. 8-Fit Eligibility Requires Reconciliation

Existing documentation defines eight fits: Cash-flow, Liquidity, Debt, Asset Resource, Risk Capacity, Goal Constraint, Multi-goal Conflict and Implementation.

Real-Life Cases indicate that these may overlap with Financial State, Goal Feasibility, Whole-Plan Impact, Hard Constraints, Strategy Applicability and Strategy Viability.

Therefore, **8-Fit must not automatically remain an independent decision gate until ownership of each fit is reconciled**.

Each fit must be mapped to its canonical owner. The goal is: **one business rule → one canonical owner**.

## 12. Scenario / What-If Architecture

```text
ACCEPTED PLAN
     │
     ├── What-if A
     ├── What-if B
     └── Investor-designed alternative
              ↓
        Impact Analysis
              ↓
        Investor Decision
          ↙        ↘
       Reject       Accept
         ↓             ↓
    Keep Plan     Update Plan
```

**Product rule:** A scenario must never silently overwrite the accepted plan.

## 13. Change and Revalidation Model

Not every change requires full replanning.

### Execution change

Execution Change → Impact Analysis → Material? → No: continue / Yes: targeted strategy revalidation.

### Financial-state change

Financial State Change → Materiality Check → Affected Goals/Strategies → Targeted Feasibility Recalculation → Targeted Strategy Revalidation.

### Goal change

Goal Change → Funding Recalculation → Feasibility Recalculation → Whole-Plan Impact → Strategy Revalidation → Investor Decision.

**Product principle:** Change does not automatically mean full replanning.

## 14. Stress and Resilience

Stress testing is not a second decision engine. The same accepted/proposed planning logic should be replayed under changed assumptions:

```text
Base Inputs → Base Decision → Stress Inputs → Same Decision Logic → Compare → Resilience Assessment
```

If stress materially changes the outcome, the relevant layer is revalidated.

## 15. Investor Agency

PlanVesto is decision support, not an autonomous authority that silently changes the investor's financial plan.

The investor may accept, reject, modify, change execution, change a goal, test a what-if, or design an alternative strategy. Only an accepted decision becomes part of the active plan.

## 16. Investor-Designed Strategy

```text
Investor Defines Approach
        ↓
PlanVesto Structures It
        ↓
Calculate → Validate → Stress / Impact → Explain Trade-offs
        ↓
Investor Accepts / Modifies / Rejects
```

Investor-designed approaches do not bypass genuine hard constraints.

## 17. No Acceptable Path

**No acceptable strategy/path under the current goals, resources and constraints** is a valid product outcome.

The system must not force a recommendation merely because the interface expects one. It should explain what would need to change: timeline, target, funding, competing commitments, debt, priority or funding structure.

## 18. Accepted Plan and Action Plan

The **Accepted Plan** is the authoritative current planning state. Scenarios, rejected recommendations and unaccepted proposals remain separate.

The **Action Plan** converts the accepted plan into implementation: actions, timing, amounts where applicable, dependencies, active actions and completed actions. Historical completed actions remain historical.

## 19. Monitoring and Adaptation

```text
Accepted Plan → Action Plan → Execution → Monitoring → Change Detected → Impact Analysis → Targeted Revalidation → Investor Decision → Updated Accepted Plan
```

## 20. Canonical Product Ownership Map

| Business Question | Owner |
|---|---|
| What is financially true? | Financial State |
| What does the investor want? | Goal Planner |
| Can the goal be achieved? | Goal Feasibility |
| How can the goal be funded? | Goal Funding / Feasibility |
| What happens to other goals? | Whole-Plan Impact |
| What is non-negotiable? | Hard Constraint Policy |
| Which strategies can apply? | Strategy Applicability |
| Can the strategy work? | Strategy Viability |
| Which strategy is preferred? | Strategy Selection |
| Which variant? | Variant Selection |
| Which techniques? | Technique Selection |
| How are techniques assembled? | Architecture |
| Does it survive stress? | Stress / Resilience |
| What if something changes? | Impact / What-If |
| Does current plan remain valid? | Revalidation |
| What does investor accept? | Investor Decision / Adoption |
| What is currently active? | Accepted Plan |
| What must be executed? | Action Plan |
| What changed later? | Monitoring / Adaptation |

## 21. Real-Life Cases → Product Responsibility

| Case | Product Responsibility |
|---|---|
| Case 1 — Debt vs Retirement Opportunity Cost | Goal feasibility + opportunity-cost analysis |
| Case 2 — Education Feasibility → Execution | Goal Planner → Strategy Builder boundary |
| Case 3 — Multi-Goal Feasibility | Whole-plan planning |
| Case 4 — Better Path | Strategy alternatives + impact comparison |
| Case 5 — Financial State Change | Monitoring + targeted revalidation |
| Case 6 — Goal Intent Change | Goal recalculation + targeted revalidation |
| Case 7 — New Goal | Scenario + whole-plan impact + investor adoption |
| Case 8 — Strategy Change | Strategy selection + investor adoption |
| Case 9 — Execution What-If | Impact engine |
| Case 10 — Execution Change | Impact → strategy revalidation |
| Case 11 — Iterative Strategy Execution | Full iterative lifecycle |
| Case 12 — No Acceptable Path / Investor Strategy | Outcome handling + open strategy mode |

## 22. Product Architecture Hierarchy

```text
PLANVESTO
│
├── Financial Reality
│   └── Financial State
│
├── Goal Planning
│   ├── Goal Definition
│   ├── Goal Context
│   ├── Goal Funding
│   └── Goal Feasibility
│
├── Whole-Plan Planning
│   ├── Multi-Goal
│   ├── Priorities
│   ├── Resource Conflicts
│   └── Trade-offs
│
├── Strategy Decision
│   ├── Hard Constraints
│   ├── Applicability
│   ├── Candidate Strategies
│   ├── Viability
│   ├── Selection
│   ├── Variant
│   ├── Technique
│   ├── Architecture
│   └── Stress / Resilience
│
├── Impact & What-If
├── Revalidation
├── Investor Decision
├── Accepted Plan
├── Action Plan
└── Monitoring & Adaptation
```

## 23. Product Management Guardrails

1. One business rule → one canonical owner.
2. Financial State represents financial reality; it does not silently become a strategy engine.
3. Goal Planner owns goal feasibility.
4. Goal Funding belongs to Goal Planner / Feasibility.
5. Strategy Builder consumes feasibility; it does not independently recreate it.
6. Applicability, viability and selection remain distinct.
7. A measurement does not automatically become a decision rule.
8. 8-Fit must be reconciled before being retained as an independent gate.
9. Scenario does not equal accepted plan.
10. Investor acceptance is required before a proposed change becomes the active plan.
11. Material changes trigger targeted revalidation.
12. Full replanning is not the default response to every change.
13. No Acceptable Path is a valid outcome.
14. Investor-designed strategies must be supported and evaluated.
15. Action Plan is downstream of the accepted plan.
16. Monitoring feeds controlled revalidation rather than uncontrolled replanning.

## 24. Relationship to Strategy Decision Tree

The canonical document `docs/Decision tree/Real-Life Decision Cases/strategy-decision-tree.md` defines the **Strategy Decision subsystem**.

This document defines the **larger product architecture in which that Strategy Decision Tree operates**.

```text
Product System Map
        ↓
Strategy Decision Tree
        ↓
Strategy → Variant → Technique
        ↓
Solution / Architecture
```

The two documents are complementary, not duplicates.

## 25. Next Product Audit

Before implementation changes are made, the existing system should be audited using:

| Responsibility | Real-Life Requirement | Canonical Layer | Existing Documentation | Current Code | Status |
|---|---|---|---|---|---|
| Financial State | | | | | |
| Goal Planning | | | | | |
| Goal Feasibility | | | | | |
| Goal Funding | | | | | |
| Whole-Plan Impact | | | | | |
| Hard Constraints | | | | | |
| Strategy Applicability | | | | | |
| Strategy Viability | | | | | |
| Strategy Selection | | | | | |
| Variant Selection | | | | | |
| Technique Selection | | | | | |
| Architecture | | | | | |
| Stress / Resilience | | | | | |
| Impact / What-If | | | | | |
| Revalidation | | | | | |
| Investor Decision | | | | | |
| Accepted Plan | | | | | |
| Action Plan | | | | | |
| Monitoring / Adaptation | | | | | |

Status values: **Aligned, Partially Aligned, Overlapping, Missing, Contradictory, Needs Business Decision**.

## 26. Final Product Principle

> **PlanVesto should not merely tell an investor which strategy to use. It should understand the investor's financial reality, establish goal and whole-plan feasibility, determine the appropriate strategy, allow alternatives to be tested, preserve investor choice, maintain an authoritative accepted plan, convert that plan into actions, and revalidate only what needs to change as circumstances evolve.**

This is the canonical product-level structure derived from the Real-Life Decision Cases.