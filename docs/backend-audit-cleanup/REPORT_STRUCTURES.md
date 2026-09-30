# Planvesto Report Structures

## Purpose

Define the final structure of three reporting levels without creating duplicate financial calculations or decision engines.

The three reports are:

1. **Complete Financial Report** — investor-level 360° picture.
2. **Goal Report** — one goal's complete planning picture.
3. **Planning Basket Report** — a group of goals planned together.

These are reporting/assembly layers. They must consume existing canonical financial state, metrics, goals, strategies, constraints and multi-goal decisions.

---

# 1. Core Relationship

```text
INVESTOR
  │
  ├── Financial State
  │      ├── Income
  │      ├── Expenses
  │      ├── Assets
  │      ├── Liabilities
  │    
  │
  ├── Financial Metrics / Health
  │
  ├── Goals
  │      └── Goal Report
  │            └── Strategy / Funding / Actions
  │
  ├── Planning Baskets
  │      └── Basket Report
  │            └── Goals + Trade-offs + Allocation
  │
  └── Complete Financial Report
         ├── Financial State
         ├── Financial Health
         ├── Goals Overview
         ├── Basket Overview
         ├── Strategy Overview
         ├── Resource Allocation
         ├── Trade-offs
         └── Action Plan
```

## Critical rule

**Reports do not calculate financial truth again.**

They assemble results from authoritative engines/services.

---

# 2. Complete Financial Report

## Purpose

Answer:

> "Meri overall financial position kya hai, mere goals kya hain, unki current condition kya hai, resources kaha ja rahe hain, aur mujhe overall kya karna hai?"

## Structure

```text
CompleteFinancialReport
│
├── report_metadata
│   ├── report_id
│   ├── planning_unit_id
│   ├── generated_at
│   └── report_version
│
├── executive_summary
│   ├── financial_position
│   ├── financial_health_status
│   ├── monthly_surplus
│   ├── net_worth
│   ├── total_goals
│   ├── overall_funding_status
│   ├── major_constraints
│   └── key_planning_observations
│
├── financial_state
│   ├── income
│   ├── expenses
│   ├── monthly_surplus
│   ├── assets
│   ├── liabilities
│   ├── net_worth
│   └── liquidity
│
├── financial_health
│   ├── canonical_metrics
│   ├── diagnostics
│   ├── constraints
│   └── health_score (only when finalized)
│
├── protection
│   ├── insurance_position
│   ├── required_cover
│   ├── existing_cover
│   └── protection_gap
│
├── goals_overview
│   ├── total_goals
│   ├── essential_goals
│   ├── discretionary_goals
│   ├── funded_goals
│   ├── partially_funded_goals
│   ├── unfunded_goals
│   └── goal_rows[]
│
├── planning_baskets
│   ├── basket_count
│   └── basket_summaries[]
│
├── strategy_overview
│   ├── strategies_selected
│   ├── conditional_strategies
│   ├── unresolved_strategy_decisions
│   └── strategy_rows[]
│
├── resource_allocation
│   ├── available_surplus
│   ├── foundation_requirements
│   ├── goal_allocations[]
│   ├── allocated_total
│   └── unallocated_surplus
│
├── trade_offs
│   ├── detected
│   ├── decisions
│   └── explanations
│
├── action_plan
│   ├── immediate_actions[]
│   ├── goal_actions[]
│   ├── financial_health_actions[]
│   └── review_actions[]
│
└── audit
    ├── source_runs
    ├── rule_version
    └── calculation_version
```

## Report principle

This is the **highest reporting level**. It should not become another planning engine.

---

# 3. Goal Report

## Purpose

Answer:

> "Is goal ko achieve karne ke liye kya required hai, current position kya hai, kaunsi strategy applicable/selected hai, aur investor ko kya karna hai?"

## Structure

```text
GoalReport
│
├── report_metadata
│   ├── report_id
│   ├── planning_unit_id
│   ├── goal_id
│   └── generated_at
│
├── goal
│   ├── name
│   ├── type
│   ├── priority
│   ├── flexibility
│   ├── target_date
│   ├── target_amount_today
│   └── target_amount_future
│
├── goal_calculation
│   ├── current_funding
│   ├── future_target
│   ├── funding_gap
│   ├── required_monthly_contribution
│   ├── existing_assets_applied
│   ├── inflation_assumption
│   ├── return_assumption
│   └── feasibility_status
│
├── constraints
│   ├── financial_constraints[]
│   ├── goal_constraints[]
│   └── blocking_conditions[]
│
├── strategy_decision
│   ├── eligible_strategies[]
│   ├── conditional_strategies[]
│   ├── failed_strategies[]
│   ├── selected_strategy
│   ├── selection_reasons[]
│   └── strategy_parameters
│
├── funding_plan
│   ├── required_monthly
│   ├── allocated_monthly
│   ├── shortfall
│   ├── funding_percentage
│   └── funding_status
│
├── action_plan
│   ├── immediate_actions[]
│   ├── funding_actions[]
│   ├── implementation_actions[]
│   └── review_actions[]
│
├── scenarios
│   ├── base
│   ├── conservative
│   └── stress (when supported)
│
└── audit
    ├── strategy_run_id
    ├── rule_version
    └── calculation_version
```

## Important

A Goal Report is **not** a copy of the Complete Financial Report. It contains only the investor context necessary to explain this goal's decision.

---

# 4. Planning Basket Report

## Purpose

Answer:

> "In goals ko ek saath plan karne par total requirement kya hai, resources kaise compete kar rahe hain, allocation kya hua, aur trade-offs kya hain?"

A basket is a planning group, not a new goal and not a strategy. Existing repository documentation already defines this separation. fileciteturn66file0

## Structure

```text
PlanningBasketReport
│
├── report_metadata
│   ├── report_id
│   ├── planning_unit_id
│   ├── basket_id
│   ├── basket_name
│   └── generated_at
│
├── basket
│   ├── name
│   ├── description
│   ├── goal_count
│   └── planning_intent
│
├── goals
│   ├── goal_rows[]
│   │   ├── goal_id
│   │   ├── goal_name
│   │   ├── priority
│   │   ├── target
│   │   ├── funding_gap
│   │   ├── required_monthly
│   │   ├── allocated_monthly
│   │   ├── funding_status
│   │   └── selected_strategy
│   └── aggregate_goal_requirement
│
├── basket_financial_position
│   ├── available_monthly_surplus
│   ├── total_required_monthly
│   ├── total_allocated_monthly
│   ├── total_shortfall
│   └── funding_status
│
├── resource_allocation
│   ├── allocation_order
│   ├── goal_allocations[]
│   ├── unallocated_surplus
│   └── allocation_method
│
├── conflicts_and_tradeoffs
│   ├── competing_resources
│   ├── priority_conflicts
│   ├── trade_offs[]
│   └── resolutions[]
│
├── strategy_summary
│   ├── goal_strategy_rows[]
│   └── cross_goal_dependencies[]
│
├── action_plan
│   ├── basket_level_actions[]
│   ├── goal_actions[]
│   └── sequencing[]
│
└── audit
    ├── goal_ids
    ├── orchestration_run_id
    ├── rule_version
    └── calculation_version
```

## Basket rule

Basket-level planning may **allocate resources and resolve trade-offs**, but must not replace individual goal calculations or individual strategy decisions.

---

# 5. Relationship Between the Three

```text
                    COMPLETE FINANCIAL REPORT
                              │
             ┌────────────────┼────────────────┐
             ↓                ↓                ↓
       Financial State    Goal Overview    Basket Overview
                                  │                │
                                  ↓                ↓
                           GOAL REPORT      BASKET REPORT
                                  │                │
                                  ↓                ↓
                             Strategy       Allocation
                             Funding        Trade-offs
                             Actions        Collective Actions
```

## Rule

- **Goal Report** = individual decision.
- **Basket Report** = collective planning decision.
- **Complete Financial Report** = complete investor picture.

---

# 6. Single Source of Truth

The reporting layer must consume these existing authorities:

| Data | Source of truth |
|---|---|
| Income/expenses/assets/liabilities | Financial State |
| Financial ratios/diagnostics | Canonical Financial Metrics / Rules |
| Goal target/funding calculations | Goal Engine / Defined Goal |
| Goal constraints | Central Rules + Constraint Engine |
| Strategy definitions | Strategy Library |
| Strategy eligibility | Central Eligibility Rules + Engine |
| Strategy selection | Central Strategy Decision Rules + Engine |
| Multi-goal allocation | Multi-Goal Engine/Service |
| Action decisions | Central Action Rules + Action Plan Engine |
| Report assembly | Report Services |

**Report services must not recalculate these values independently.**

---

# 7. Common Status Vocabulary

Use one status vocabulary across reports where the same concept is represented.

### Funding

- `fully_funded`
- `partially_funded`
- `unfunded`
- `not_applicable`

### Feasibility

- `feasible`
- `conditionally_feasible`
- `not_feasible`
- `not_evaluated`

### Strategy

- `pass`
- `conditional`
- `fail`
- `selected`
- `not_selected`

### Planning

- `no_conflict`
- `conflict_detected`
- `trade_off_required`
- `resolved`

Do not introduce another synonym for an existing status without a business reason.

---

# 8. What Is Already Present vs What Needs Completion

## Already present in backend

- Complete Financial Plan service
- Goal Report service
- Goal Basket service
- Basket Report service
- Multi-goal planning
- Strategy reports
- Action Plan structures

The repository already has a consolidated `FinancialPlanService` that assembles financial state, goals, funding, resource allocation, trade-offs and actions. fileciteturn68file0

## Needs business-rule completion

- Exact financial-health narrative/status policy
- Final strategy eligibility policy
- Final strategy selection policy
- Final conditional/adaptation policy
- Final multi-goal allocation policy
- Final action-generation policy
- Final report interpretation/narrative rules

## Needs structural cleanup where applicable

- Keep report services as assemblers.
- Move any remaining business decisions from report services into the authoritative rule/engine layers.
- Do not create a second calculation system for reports.

---

# 9. Final User Journey

```text
ONBOARDING / FINANCIAL DATA
          ↓
FINANCIAL STATE
          ↓
FINANCIAL HEALTH / METRICS
          ↓
GOALS
          ↓
GOAL REPORT
          ↓
STRATEGY DECISION
          ↓
PLANNING BASKET (when multiple goals are planned together)
          ↓
MULTI-GOAL ALLOCATION + TRADE-OFFS
          ↓
ACTION PLAN
          ↓
COMPLETE FINANCIAL REPORT
```

The exact UI navigation may differ, but the backend reporting hierarchy should remain this way.

---

# 10. Production Rule

**No report should invent a decision.**

If a report needs to say:

- "this goal is infeasible"
- "this strategy is selected"
- "this goal gets priority"
- "this action must happen first"
- "this resource should be allocated here"

then that decision must already exist as an authoritative engine/rule result.

The report only explains and presents it.
