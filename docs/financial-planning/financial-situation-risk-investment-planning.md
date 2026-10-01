# Planvesto — Financial Situation, Risk Profile & Investment Planning Architecture

**Status:** Planning + Implementation Specification  
**Target branch:** `backend-audit-cleanup`  
**Scope:** Backend/domain architecture and implementation planning  
**Explicit exclusions:** Frontend redesign, Supabase schema changes, SQL migrations, Git CLI commands, and unapproved business-rule invention.

---

## 1. Purpose

This document defines the architecture for three distinct capabilities:

1. **MoneyWheel** — diagnose and balance the investor's financial situation.
2. **Risk Profiler** — determine the investor's investment risk characteristics and strategic asset-allocation envelope.
3. **Investment Planning / Portfolio Construction** — convert the strategic allocation into sub-asset allocation, implementation categories, and eventually specific products.

The key architectural decision is that **MoneyWheel is not a Strategy Builder input that determines the strategy**.

MoneyWheel answers:

> **What is financially happening to this investor?**

Risk Profiler answers:

> **What investment risk and allocation structure is appropriate for this investor?**

Investment Planning answers:

> **How should investable capital actually be allocated?**

Strategy Builder answers a different question:

> **For a particular goal/problem and its constraints, what strategy architecture should be used?**

These systems can exchange facts, but they must not be collapsed into one engine.

---

# 2. Target Decision Architecture

The target architecture is:

```
                    FINANCIAL DATA
                         |
                         v
                   +-------------+
                   |  MoneyWheel |
                   +-------------+
                         |
                         v
              FINANCIAL SITUATION
              /       |        \
       Liquidity   Leverage   Funding
       Concentr.   Debt       Pressure
                         |
                         +--------------------+
                                              |
RISK DATA                                      |
   |                                          |
   v                                          |
+-------------+                               |
| Risk        |                               |
| Profiler    |                               |
+-------------+                               |
   |                                          |
   v                                          |
RISK / INVESTOR PROFILE                       |
   |                                          |
   v                                          |
STRATEGIC ASSET ALLOCATION                    |
   |                                          |
   v                                          |
SUB-ASSET ALLOCATION                          |
   |                                          |
   v                                          |
IMPLEMENTATION / PRODUCT SELECTION             |
                                              |
GOAL DATA ------------------------------------+
   |
   v
GOAL REQUIREMENT / HORIZON / FEASIBILITY
   |
   +------------------> Investment Planning
   |
   +------------------> Strategy Builder
                         |
                         v
                    STRATEGY
                    SCENARIOS
                    DECISION
```

The important separation is:

- **MoneyWheel describes financial condition.**
- **Risk Profiler describes investment risk characteristics.**
- **Goal Engine describes goal requirements.**
- **Investment Engine constructs the portfolio.**
- **Strategy Builder solves a defined financial problem using a strategy architecture.**

---

# 3. What MoneyWheel Must Produce

MoneyWheel should not merely output nine ratios as isolated numbers.

Its output should have three layers.

## 3.1 Layer A — Small Metrics

The current MoneyWheel metric set is:

1. Savings Rate
2. Liquid Asset Ratio
3. Debt-to-Income Ratio
4. Leverage Ratio
5. Financial Asset Ratio
6. Insurance Coverage Ratio
7. Goal Funding Ratio
8. Future Funding Ratio
9. Required Rate of Return

Separate rules:

10. Expense Coverage
11. Emergency Coverage

These are **measurements**, not recommendations.

---

## 3.2 Layer B — Relationships Between Metrics

A single ratio is often insufficient.

Example:

- Liquidity Ratio = low
- Financial Asset Ratio = low
- Portfolio Concentration = high
- Hard-asset share = high

Combined interpretation:

> The investor may have substantial nominal wealth but relatively low immediately deployable financial liquidity because wealth is concentrated in hard / less-liquid assets.

MoneyWheel should therefore support relationship-level diagnostics.

### Examples

**Low liquidity + high hard-asset concentration**

→ Liquidity constraint caused by asset structure.

**High DTI + low Savings Rate**

→ Cash-flow pressure.

**High leverage + low Financial Asset Ratio**

→ Balance-sheet dependency on non-financial assets.

**High Required Return + low existing goal funding**

→ Current capital base is insufficient for the target without additional funding or a materially higher return assumption.

**High Goal Funding Ratio + low Future Funding Ratio**

→ Current position is adequate but future contributions may be insufficient.

The output is a **financial situation**, not a strategy.

---

# 4. Required Rate of Return — Correct Architecture

Required Rate of Return is especially important because it demonstrates the difference between:

- mathematical calculation,
- financial interpretation,
- and strategy.

## 4.1 Formula layer

For a simple lump-sum case:

```
Required Return = (Future Goal Value / Current Investable Capital)^(1/n) - 1
```

Example:

- Current capital = ₹5L
- Future goal = ₹10L
- Horizon = 5 years

Required return is approximately **14.87% p.a.**

The formula answers:

> What annualized return is mathematically required to turn ₹5L into ₹10L over five years?

---

## 4.2 Combined financial interpretation

Now combine:

- current capital,
- goal amount,
- goal horizon,
- monthly surplus,
- current portfolio,
- existing asset allocation,
- risk profile.

The question becomes:

> Is the required return compatible with the investor's available capital, cash flow, horizon and investment-risk envelope?

This is the useful MoneyWheel output.

For example:

```
Required Return = 14.87%
Risk Profile Target = 70% Equity / 25% Debt / 5% Gold
Current Funding = ₹5L
Monthly Surplus = ₹20K
```

MoneyWheel does **not** conclude:

> Buy small-cap funds.

Instead it reports:

> The goal requires a high return relative to the available capital and current funding capacity.

The Goal Engine / Investment Engine can then determine the feasible funding and allocation path.

---

# 5. Portfolio Concentration

Portfolio concentration should be a separate small metric / diagnostic.

It answers:

> **Where is the investor's wealth actually concentrated?**

Example:

Total assets = ₹20L

- Real estate = ₹12L
- Gold = ₹5L
- Equity/MF = ₹2L
- Liquid assets = ₹1L

The portfolio is heavily concentrated outside liquid financial assets.

Combined with Liquidity Ratio:

```
High concentration in hard assets
+
Low liquidity
=
Wealth exists, but deployable financial liquidity is constrained.
```

This is precisely the type of financial-situation insight MoneyWheel should surface.

It should not automatically prescribe an investment transaction.

---

# 6. Risk Profiler Output

Risk Profiler must eventually produce a structured investment profile rather than only a single risk label.

Minimum conceptual output:

## 6.1 Risk Capacity

How much financial loss / volatility the investor's financial situation can absorb.

## 6.2 Risk Tolerance

How much volatility the investor is psychologically willing to tolerate.

## 6.3 Investment Horizon

Relevant horizon for the capital being evaluated.

## 6.4 Investor Identity

The investor's behavioral / decision orientation.

## 6.5 Strategic Asset Allocation

The actual portfolio-level output.

Example:

```
Strategic Asset Allocation
Equity  = 70%
Debt    = 25%
Gold    = 5%
Total   = 100%
```

The exact percentages must come from the finalized Risk Profiler business rules. They must not be hard-coded from this example.

---

# 7. Strategic Asset Allocation → Sub-Asset Allocation

Strategic Asset Allocation is not yet enough for implementation.

Example:

```
Equity 70%
Debt   25%
Gold    5%
```

The next layer is:

### Equity

```
Large Cap = 30%
Mid Cap   = 25%
Small Cap = 15%
Total     = 70%
```

### Debt

```
Short Duration = 10%
Banking & PSU  = 8%
Gilt           = 4%
Liquid         = 3%
Total          = 25%
```

### Gold

```
Gold = 5%
```

This creates the complete target portfolio architecture:

| Category | Target |
|---|---:|
| Large Cap | 30% |
| Mid Cap | 25% |
| Small Cap | 15% |
| Short Duration Debt | 10% |
| Banking & PSU Debt | 8% |
| Gilt | 4% |
| Liquid / Overnight | 3% |
| Gold | 5% |
| **Total** | **100%** |

**Important:** These percentages are architectural examples only. Production values must come from approved allocation rules.

---

# 8. Why This Can Reduce Goal-by-Goal Portfolio Mapping

A major product opportunity is to avoid forcing the investor to create a completely separate portfolio for every goal.

Example:

Investor has:

- Retirement — 20 years
- Home — 5 years
- Education — 6 years
- Wedding — 5 years
- Vacation — 2 years

It may be possible to maintain:

1. a **core long-term portfolio**,
2. a **medium-horizon allocation**, and
3. a **near-term liquidity / capital-preservation allocation**,

rather than five completely independent portfolios.

However, this is only valid when the goals' horizons, liquidity requirements and funding structures permit it.

Therefore the system should distinguish:

### Portfolio-level allocation

What percentage of the investor's investable capital should be in each asset category?

### Goal-level funding requirement

How much capital must be available for each goal at a particular date?

### Goal funding source

Which portion of the portfolio / cash flow is expected to fund that goal?

These are related but not identical concepts.

---

# 9. Goal Data + Risk Profile = Allocation Context

Goal data should not automatically overwrite the investor's risk profile.

Instead it should create **goal-specific constraints on implementation**.

Example:

Investor-level strategic allocation:

```
70% Equity
25% Debt
5% Gold
```

But a vacation goal due in 18 months cannot simply receive 70% equity because the investor is classified as a 70% equity investor.

The system needs:

```
Investor Risk Profile
        +
Goal Horizon
        +
Goal Liquidity Requirement
        +
Funding Requirement
        +
Existing Portfolio
        =
Applicable Investment Allocation
```

This can produce:

- core long-term allocation,
- goal-specific reserve,
- de-risking schedule,
- cash-flow funding requirement.

The investor's **risk identity remains stable**, while the **capital allocation can differ because the capital has different jobs and deadlines**.

---

# 10. Investment Planning Architecture

Investment Planning should be a separate engine.

## Layer 1 — Strategic Asset Allocation

Example:

```
Equity 70%
Debt 25%
Gold 5%
```

## Layer 2 — Sub-Asset Allocation

Example:

```
Equity:
Large 30%
Mid   25%
Small 15%

Debt:
Short Duration 10%
Banking & PSU  8%
Gilt            4%
Liquid          3%

Gold:
Gold 5%
```

## Layer 3 — Product Category

Map each sub-asset class to implementable product categories.

Example:

```
Large Cap
→ Large-cap mutual fund / index category

Mid Cap
→ Mid-cap mutual fund category

Small Cap
→ Small-cap mutual fund category

Short Duration
→ Short-duration debt category

Gold
→ Gold ETF / Gold fund category
```

## Layer 4 — Product Selection

Only after suitability and product rules are available:

```
Sub-Asset Category
→ Eligible Products
→ Product Suitability
→ Product Selection
→ Allocation Amount
```

This layer is **not** the same as Strategy Builder.

---

# 11. Current Portfolio vs Target Portfolio

Investment Planning must compare actual holdings against the target.

Example:

### Target

```
Large Cap       30%
Mid Cap         25%
Small Cap       15%
Debt            25%
Gold             5%
```

### Current

```
Large Cap       10%
Mid Cap          5%
Small Cap       0%
Debt            15%
Gold            20%
Cash            50%
```

The engine calculates:

```
Target Allocation
-
Current Allocation
=
Allocation Gap
```

This produces implementation requirements without requiring a separate goal portfolio for every goal.

---

# 12. Portfolio Concentration vs Allocation Gap

These must remain separate.

### Concentration

Answers:

> Is too much wealth concentrated in one asset / category / issuer / exposure?

### Allocation Gap

Answers:

> How far is the current portfolio from the target allocation?

### Liquidity

Answers:

> How much capital is immediately accessible?

Together:

```
Concentration
+
Liquidity
+
Allocation Gap
=
Portfolio Situation
```

Again, the output is diagnostic before it becomes actionable.

---

# 13. MoneyWheel Output Contract

MoneyWheel should eventually return a structured object similar to:

```json
{
  "metrics": {
    "savings_rate": {},
    "liquid_asset_ratio": {},
    "dti": {},
    "leverage_ratio": {},
    "financial_asset_ratio": {},
    "insurance_coverage_ratio": {},
    "goal_funding_ratio": {},
    "future_funding_ratio": {},
    "required_rate_of_return": {}
  },
  "rules": {
    "expense_coverage": {},
    "emergency_coverage": {}
  },
  "diagnostics": [
    {
      "type": "liquidity",
      "severity": "high",
      "evidence": []
    },
    {
      "type": "concentration",
      "severity": "medium",
      "evidence": []
    }
  ],
  "financial_story": {
    "current_position": "",
    "primary_constraint": "",
    "supporting_evidence": [],
    "goal_impact": "",
    "financial_priorities": []
  }
}
```

The exact schema must be reconciled with the existing backend models before implementation.

---

# 14. Investment Planning Output Contract

Conceptual target:

```json
{
  "investor_profile": {
    "risk_capacity": {},
    "risk_tolerance": {},
    "investor_identity": {}
  },
  "strategic_allocation": [
    {
      "asset_class": "equity",
      "target_pct": 70
    },
    {
      "asset_class": "debt",
      "target_pct": 25
    },
    {
      "asset_class": "gold",
      "target_pct": 5
    }
  ],
  "sub_asset_allocation": [],
  "implementation_categories": [],
  "current_vs_target": [],
  "allocation_gaps": [],
  "rebalance_actions": []
}
```

This is a target architecture, not a final approved production schema.

---

# 15. Strategy Builder Boundary

The Strategy Builder should not become an allocation calculator.

Its responsibility remains:

```
Problem / Goal
+
Constraints
+
Financial Context where relevant
        ↓
Strategy Library
        ↓
Applicable Strategies
        ↓
Strategy Architecture
        ↓
Scenarios
        ↓
Decision
```

Example:

### Home Purchase

Problem:

> Need ₹X for home purchase in 5 years.

Possible strategy architecture:

- Goal Funding
- Progressive De-risking
- Capital Preservation
- Credit Utilisation

The Investment Engine may then determine how the investable capital is implemented.

Therefore:

**Strategy = how the financial problem is approached.**

**Allocation = where investment capital is positioned.**

They must remain separate objects.

---

# 16. Relationship Between MoneyWheel and Strategy Builder

The relationship should be **limited and contextual**, not structural dependency.

MoneyWheel may provide:

- financial context,
- financial priorities,
- constraints/evidence,
- liquidity condition,
- debt condition,
- funding pressure.

Strategy Builder may consume these facts when they are relevant to the strategy decision.

But:

```
MoneyWheel ≠ Strategy Engine
```

and:

```
MoneyWheel should not select a strategy merely because a ratio is high/low.
```

---

# 17. Small Metrics — Recommended Foundation

The implementation should favour small deterministic metrics over a single opaque "financial health score".

Recommended foundation:

### Cash Flow

- Savings Rate
- Monthly Surplus

### Liquidity

- Liquid Asset Ratio
- Expense Coverage
- Emergency Coverage

### Debt

- DTI
- Leverage Ratio

### Wealth Structure

- Financial Asset Ratio
- Portfolio Concentration
- Hard-Asset Concentration

### Protection

- Insurance Coverage Ratio

### Goals

- Goal Funding Ratio
- Future Funding Ratio
- Required Rate of Return

Each metric should have:

- definition,
- formula,
- required inputs,
- unit,
- interpretation range,
- provenance,
- missing-data behaviour,
- confidence/data-quality flag.

Do not hide missing inputs by inventing defaults.

---

# 18. Implementation Plan

## Phase 0 — Business Rule Freeze

Before coding:

1. Freeze exact definitions of all MoneyWheel metrics.
2. Freeze numerator / denominator for every ratio.
3. Freeze treatment of missing values.
4. Freeze whether values are monthly, annual, current-value or future-value.
5. Freeze Risk Profiler output structure.
6. Freeze strategic asset classes.
7. Freeze sub-asset taxonomy.
8. Freeze whether goal horizon can constrain implementation allocation.
9. Freeze product-selection boundary.
10. Freeze MoneyWheel → Strategy Builder information boundary.

**Deliverable:** business-rule specification.

---

## Phase 1 — MoneyWheel Metrics

Implement pure calculation functions.

Suggested module structure:

```
backend/engines/moneywheel/
    __init__.py
    engine.py
    metrics.py
    liquidity.py
    debt.py
    wealth.py
    goals.py
    diagnostics.py
    story.py
```

Each metric should be a pure function where possible.

Example:

```
calculate_savings_rate(...)
calculate_liquid_asset_ratio(...)
calculate_dti(...)
calculate_leverage_ratio(...)
calculate_financial_asset_ratio(...)
calculate_goal_funding_ratio(...)
calculate_future_funding_ratio(...)
calculate_required_return(...)
```

No database access inside calculation functions.

---

## Phase 2 — MoneyWheel Diagnostic Layer

Build relationships between metrics.

Example:

```
if liquidity_ratio < threshold
and hard_asset_concentration > threshold:
    liquidity_diagnostic(...)
```

Diagnostics must expose evidence.

Bad:

> "Liquidity is poor."

Good:

> "Liquid assets are low relative to monthly expenses; a large share of total assets is held in less-liquid/hard assets."

Exact thresholds must be approved before implementation.

---

## Phase 3 — Financial Story

Convert metric results into:

1. Current Position
2. Primary Constraint
3. Supporting Evidence
4. Goal Impact
5. Financial Priorities
6. Strategy Input

Financial Priorities are **not strategies**.

---

## Phase 4 — Risk Profiler Output

Audit the existing risk-profile implementation, then standardize its output into:

```
Risk Capacity
Risk Tolerance
Investor Identity
Horizon
Strategic Asset Allocation
```

Do not invent scoring rules if they do not already exist.

---

## Phase 5 — Strategic Asset Allocation Engine

Create a deterministic mapping:

```
Risk / Investor Profile
        ↓
Strategic Asset Allocation
```

Example only:

```
70% Equity
25% Debt
5% Gold
```

Production values must come from approved rules.

The output must always sum to 100%.

Validation:

```
sum(allocation) == 100%
```

with appropriate tolerance if decimals are supported.

---

## Phase 6 — Sub-Asset Allocation Engine

For each strategic asset class:

```
Asset Class
→ Sub-Asset Allocation
```

Example:

```
Equity 70
→ Large 30
→ Mid 25
→ Small 15
```

Validation:

```
sum(equity_suballocation) == equity_allocation
```

Repeat for Debt and other supported classes.

---

## Phase 7 — Current Portfolio Analysis

Build:

```
Current Holdings
→ Classification
→ Aggregation
→ Current Allocation
→ Target Allocation
→ Gap
→ Concentration
```

This requires reliable holding classification.

Do not guess whether a product is large-cap, mid-cap, small-cap, debt, gold, etc.

---

## Phase 8 — Goal Context

Goal Engine provides:

- target amount,
- target date,
- horizon,
- current funding,
- required funding,
- feasibility.

Investment Engine uses this context to determine whether the target portfolio can be used directly or whether a goal-specific reserve / de-risking layer is required.

The goal engine does not directly select mutual funds.

---

## Phase 9 — Product Selection Boundary

Only after allocation architecture is stable:

```
Sub-Asset Class
→ Product Universe
→ Suitability Rules
→ Product Ranking / Filtering
→ Selected Product
→ Allocation Amount
```

Product selection should remain independently testable.

---

# 19. Testing Strategy

## Unit Tests

Every metric must have:

- normal case,
- zero case,
- boundary case,
- missing-data case,
- invalid-data case.

Example:

```
test_savings_rate()
test_savings_rate_zero_income()
test_dti_zero_debt()
test_liquidity_ratio_zero_liquid_assets()
test_required_return_zero_horizon()
test_required_return_already_funded()
```

## Allocation Tests

Verify:

```
Strategic total = 100%
Equity sub-total = Equity allocation
Debt sub-total = Debt allocation
Full portfolio total = 100%
```

## Portfolio Tests

Verify:

- current allocation aggregation,
- target gap,
- concentration,
- duplicate holdings,
- unknown classification,
- missing classification.

## Integration Tests

Test:

```
Financial State
→ MoneyWheel
→ Risk Profile
→ Allocation
→ Goal Context
→ Investment Plan
```

Separately test:

```
Financial State
→ MoneyWheel
→ Financial Context
→ Strategy Builder
```

The two flows must not accidentally become one coupled engine.

---

# 20. Example End-to-End Investor

## Inputs

- Age: 25
- Income: ₹80,000/month
- Expenses: ₹30,000/month
- Surplus: ₹50,000/month
- Existing assets: ₹5L MF
- Liabilities: ₹0

## MoneyWheel

Example outputs:

- Savings Rate = 62.5%
- DTI = 0%
- Leverage = 0%
- Liquidity = depends on actual liquid-asset classification
- Concentration = depends on actual holdings
- Goal Funding = goal-specific
- Required Return = goal-specific

Financial story might identify:

> Strong current surplus and no debt, but multiple goals compete for the same ₹50K monthly funding capacity.

This is a financial situation statement.

## Risk Profiler

Illustrative output:

```
Equity 70%
Debt 25%
Gold 5%
```

## Sub-Asset Allocation

Illustrative:

```
Large 30%
Mid 25%
Small 15%
Short Debt 10%
Banking & PSU 8%
Gilt 4%
Liquid 3%
Gold 5%
```

## Investment Plan

For ₹10L investable capital:

```
Large Cap       ₹3.00L
Mid Cap         ₹2.50L
Small Cap       ₹1.50L
Short Debt      ₹1.00L
Banking & PSU   ₹0.80L
Gilt            ₹0.40L
Liquid          ₹0.30L
Gold            ₹0.50L
```

The investor now has an implementable portfolio architecture without first creating six separate portfolios.

If a particular goal requires near-term liquidity, the Investment Engine can create a **goal reserve / de-risking sleeve** without changing the investor's overall risk identity.

---

# 21. Important Product Decision

The system should distinguish three concepts:

### A. Target Portfolio

What the investor's investment architecture should look like.

### B. Goal Funding

How much money must be available for each goal and when.

### C. Strategy

How a specific financial problem should be solved.

They should not be represented as the same object.

---

# 22. What NOT to Build

Do not:

- make MoneyWheel choose mutual funds;
- make MoneyWheel select strategies;
- make Risk Profiler directly calculate goal funding;
- create separate full portfolios for every goal by default;
- assume every goal must have a separate folio/bucket;
- hard-code example allocation percentages as production rules;
- infer missing product classifications;
- hide missing financial data;
- turn deterministic metrics into a fake "probability of success";
- merge Strategy Engine and Investment Engine;
- modify frontend during this backend implementation phase;
- modify Supabase schema;
- create or run SQL migrations;
- use Git CLI commands.

---

# 23. Acceptance Criteria

The implementation is complete only when:

### MoneyWheel

- all approved metrics calculate correctly;
- every result has provenance;
- missing data is explicit;
- relationship diagnostics explain the evidence;
- Financial Story is generated from metric evidence;
- no strategy is selected by MoneyWheel.

### Risk Profiler

- risk capacity/tolerance/profile outputs are structured;
- strategic allocation is deterministic from approved rules;
- allocation totals validate.

### Investment Planning

- strategic allocation expands into sub-asset allocation;
- sub-asset totals reconcile;
- current portfolio can be compared with target;
- concentration and allocation gaps are distinct;
- product selection remains a later layer.

### Goal Integration

- goal horizon and funding requirement can influence implementation constraints;
- goal data does not silently overwrite investor risk profile;
- near-term goals can trigger de-risking/reserve requirements;
- no double-counting of capital.

### Strategy Builder

- remains independently testable;
- continues to operate from Goal + Problem + Constraints + applicable context;
- does not become the portfolio-construction engine.

---

# 24. Final Architecture

The final conceptual architecture is:

```
                    FINANCIAL STATE
                          |
              +-----------+-----------+
              |                       |
              v                       v
         MONEYWHEEL              RISK PROFILER
              |                       |
              v                       v
    FINANCIAL SITUATION       INVESTOR / RISK PROFILE
              |                       |
              |                       v
              |               STRATEGIC ALLOCATION
              |                       |
              |                       v
              |                SUB-ASSET ALLOCATION
              |                       |
              |                       v
              |                 PRODUCT SELECTION
              |                       |
              +-----------+-----------+
                          |
                          v
                    GOAL CONTEXT
                          |
              +-----------+-----------+
              |                       |
              v                       v
       STRATEGY BUILDER       INVESTMENT PLANNING
              |                       |
              v                       v
       STRATEGY / SCENARIO       IMPLEMENTATION
              |                       |
              +-----------+-----------+
                          |
                          v
                       DECISION
```

### Core principle

> **MoneyWheel tells us what is happening.**

> **Risk Profiler tells us what investment risk structure fits.**

> **Goal Engine tells us what the money must accomplish and when.**

> **Investment Engine tells us how capital should be allocated and implemented.**

> **Strategy Builder tells us how to solve a specific financial problem.**

> **Product Selection tells us what actual financial products can implement the approved allocation.**

This separation should be treated as the architectural baseline for the next backend implementation phase.
