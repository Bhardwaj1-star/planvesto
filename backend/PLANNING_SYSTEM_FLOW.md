# Personalised Financial Planning System — Canonical Flow

> This is the single working reference for the business flow. Do not change architecture/code based on assumptions outside this document; update the flow here first when a rule is locked.

## Current Canonical Flow

**Investor Financial State + Defined Goals**
→ **Goal / Investor Context & Constraints**
→ **Eligibility Evaluation**
→ **Eligible Strategy Set**
→ **Strategy Variants & Adaptations**
→ **Decision Engine**
→ **Personalised Financial Plan**

## Core Principle

Eligibility does **not** create the personalised plan. Strategy Library provides reusable strategy architectures; investor-specific data, goals, constraints, eligibility results, adaptations and trade-offs determine the personalised strategy variant. Decision Engine makes the final selection/architecture.

## Locked Rules So Far

1. Eligibility Fit is a feasibility/evidence layer, not the final decision-maker.
2. A CONDITIONAL strategy may go through adaptation and must then be re-checked.
3. If it still FAILS after reasonable adaptation, the strategy is removed.
4. Multiple eligible strategies can produce multiple strategy variants; Decision Engine makes the final selection.
5. Decision Engine evaluates goal-fit, financial-state fit and trade-offs.
6. Risk capacity is used for investment implementation / portfolio construction, not as the primary strategy-selection factor.
7. Goal Reprioritisation & Resource Allocation is a **Multi-Goal Orchestration Layer**, not a normal goal-level strategy.
8. Goal Funding + Long-Term Accumulation are unified into **Goal Funding**; long-term accumulation is a Goal Funding variant/architecture.
9. Income Transition is a **Goal Funding variant**, not a standalone strategy.
10. Progressive De-risking and Capital Preservation remain separate strategies.
11. Debt Reduction and Credit Utilisation remain separate strategies.
12. Global investor constraints (e.g. high debt) can affect evaluation of every candidate strategy; they must not be treated as purely strategy-specific conditions.

## Strategy Library — Current Direction

- Goal Funding
- Progressive De-risking
- Capital Preservation
- Debt Reduction
- Credit Utilisation
- Multi-Goal Orchestration (separate orchestration layer)

## Status

This document is intentionally a flow/rules ledger. Detailed Eligibility Fit mappings, strategy rules, adaptation rules and implementation details will be added only after they are explicitly discussed and locked.
