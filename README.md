# Planvesto

## What is Planvesto?
Planvesto is a goal-first personal financial planning and decision system. It converts an investor's real financial state into goals, constraints and trade-offs, financial strategies, and actionable planning outputs.

**Core idea:** Financial planning is personal — the system should determine what is appropriate for **this investor, for this goal, given this financial state and these priorities**.

## Core Flow

```text
Investor Data
    ↓
Financial State
    ↓
Goals
    ↓
Priorities + Constraints + Trade-offs
    ↓
Strategy Builder
    ↓
Multi-Goal Orchestration
    ↓
Financial Plan
    ↓
Goal Reports / PDF
```

## Core Planning Components

- **Financial State** — income, expenses, assets, liabilities and other relevant financial facts.
- **Goals** — investor-defined objectives with amount, horizon and priority.
- **Strategy Engine** — evaluates a strategy for one goal.
- **Multi-Goal Orchestrator** — coordinates several goals competing for the same resources.
- **Financial Ratios / Constraints** — checks whether the investor's financial condition supports the selected strategy/priority.
- **Financial Plan** — consolidated result across all goals.
- **Report Generation** — explains the plan, trade-offs, constraints and required actions.

## Goal Priority Rule

The **client chooses goal priority**.

Planvesto does not blindly execute that priority. Relevant financial ratios and defined business rules are checked. If a defined rule conflicts with the requested priority, the system may change the resulting allocation/strategy outcome.

Important distinction:

- Client priority = what the client selected.
- Resolved outcome = what the planning system determines after applying approved rules.
- The UI should not present a system resolution as if the client changed their priority.
- The final report must explain the reason for any material system resolution/override.

## Strategy Architecture

The existing **single-goal Strategy Engine remains responsible for single-goal strategy evaluation**.

The Multi-Goal Orchestrator must call that engine for each goal and then coordinate the results. Do not duplicate or move single-goal strategy logic into the orchestrator.

```text
Single Goal
    → Strategy Engine
    → Goal Strategy Result

Multiple Goals
    → Strategy Engine (per goal)
    → Constraints / Ratios
    → Multi-Goal Orchestrator
    → Resource Allocation
    → Consolidated Financial Plan
```

## Backend Rules

1. Business logic belongs in engines/services, not API routes.
2. Existing calculation and single-goal strategy logic should be reused.
3. Multi-goal logic must be deterministic and testable.
4. Client inputs and system-resolved outcomes must remain traceable.
5. Do not invent financial-ratio thresholds or business rules without an approved decision.
6. Do not silently hide infeasible goals or resource conflicts.
7. Reports must consume the finalized Financial Plan rather than recalculate it.

## Current Backend Scope

The current backend work is focused on completing the planning system. The implementation sequence is documented in `docs/backend/`.

```text
docs/backend/
├── STEP-01-*.md
├── STEP-02-MULTI-GOAL-ORCHESTRATOR.md
├── STEP-03-FINANCIAL-RATIO-CONSTRAINTS.md
├── STEP-04-RESOURCE-ALLOCATION.md
├── STEP-05-CONSOLIDATED-FINANCIAL-PLAN.md
├── STEP-06-REPORT-GENERATION.md
├── STEP-07-API-INTEGRATION.md
└── STEP-08-QA-AND-BACKEND-CLOSURE.md
```

**Coding agent rule:** Read the relevant Step document before implementing that step. Treat those documents and approved business decisions as the implementation source of truth.

## Explicit Non-Scope for This Backend Phase

- No frontend redesign.
- No frontend feature work unless strictly required for an already-defined backend contract.
- No Supabase schema redesign.
- No SQL migrations.
- No unrelated product features.
- No duplicate implementation in parallel branches.

## Product Direction

Planvesto is not intended to be a product-pushing system. Its planning sequence is:

**Financial State → Goals → Constraints/Trade-offs → Strategy → Decision Output.**

Financial products, portfolios and implementation choices are downstream of the financial planning decision; they should not drive the core planning engine.

## Development Principle

Build the system as a **financial decision system**, not as a collection of calculators. Each calculation is a component; the final output must remain coherent at the investor level and across all goals.
