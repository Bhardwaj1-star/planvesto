# Financial State Architecture

**Status:** CANONICAL  
**Scope:** Canonical investor financial context consumed by planning engines.

## Purpose

Financial State is the current normalized financial context for a planning unit. It is the shared financial-facts layer used by planning and decision engines.

It answers:

> **“What is the investor / planning unit's current financial position, based on authoritative financial inputs?”**

It does **not** decide which strategy, product, investment, or action should be recommended.

## Architectural Flow

**Authoritative Financial Inputs → Financial State Service → Financial State Engine → Canonical Financial State → Downstream Calculations / Engines**

The Financial State layer normalizes raw financial records into a stable contract. Canonical calculations may derive ratios or other standardized metrics from those facts.

## Scope and Identity

Every Financial State is bound to:

| Field | Meaning |
|---|---|
| `planning_unit_id` | Planning unit whose financial position is represented |
| `scope` | `family` or `individual` |
| `investor_id` | Investor identity when scope is `individual`; null for family scope |

The service validates this context before building or reading state.

## Canonical Financial State Contract

The model is represented by `backend/models/financial_state.py`. Every metric is represented as a `Metric` object:

| Metric field | Meaning |
|---|---|
| `value` | Normalized numeric value, when available |
| `available` | Whether the metric can be reliably derived |
| `reason` | Reason for unavailability when applicable |

The current canonical state contains the following groups.

### 1. Income
- `income_monthly`
- `income_annual`
- `income_breakdown`

### 2. Expenses
- `expenses_monthly`
- `expenses_annual`
- `essential_monthly_expenses`
- `expense_breakdown`

### 3. Cash Flow
- `investable_surplus_monthly`
- `investable_surplus_annual`
- `cash_flow_ratio`
- `savings_investment_rate`

### 4. Assets
- `total_assets`
- `liquid_assets`
- `financial_assets`
- `asset_breakdown`
- `asset_allocation`
- `liquidity_breakdown`

### 5. Liabilities and Debt Service
- `total_liabilities`
- `liability_breakdown`
- `liability_allocation`
- `emi_burden_monthly`

### 6. Net Worth
- `net_worth`

**Net Worth = Total Assets − Total Liabilities**

### 7. Safety Reserve
- `safety_reserve_months`
- `safety_reserve_required_amount`

The complete field contract is intentionally documented here so architecture documentation does not omit fields that exist in the canonical model.

## What the Financial State Engine Actually Normalizes

`backend/engines/financial_state/engine.py` currently consumes:
- income records
- expense records
- asset records
- liability records
- asset ownership records
- liability responsibility records
- expense participant records
- active asset-type master classifications

The engine applies:
- income/expense frequency normalization
- family vs individual ownership/responsibility allocation
- essential-expense classification
- asset liquidity classification
- financial-asset classification
- monthly EMI normalization
- surplus calculation
- net-worth calculation
- safety-reserve derivation

This means Financial State is more than a list of balances: it is a normalized, context-aware financial fact model.

## Data Ownership

| Layer | Responsibility |
|---|---|
| Financial Input Data | Authoritative raw financial records |
| Financial State API | Request boundary and context validation |
| Financial State Service | Current-state orchestration, freshness and snapshot lifecycle |
| Financial State Engine | Normalization and Financial State derivation |
| Financial State Snapshot Repository | Persistent snapshots |
| Canonical Calculation System | Standardized calculations derived from Financial State |
| Downstream Engines | Consume canonical facts/calculations; do not redefine source-of-truth facts |

## Financial State vs Canonical Calculations

These layers must remain distinct.

### Financial State owns facts and state metrics such as
- monthly income
- monthly expenses
- essential monthly expenses
- monthly investable surplus
- total assets
- liquid assets
- financial assets
- total liabilities
- monthly EMI burden
- net worth
- safety-reserve state

### Canonical Calculation System owns standardized cross-engine calculations such as
- Debt-to-Income Ratio (DTI)
- Expense Coverage
- Emergency Coverage
- asset/liability ratios
- other canonical ratios

For example:

**Financial State → Canonical DTI Calculation → MoneyWheel / Constraints / Risk / Reports**

DTI should not be independently recalculated by Financial State consumers.

Likewise, downstream services should not create competing emergency-coverage formulas when the canonical calculation already exists.

## Availability and Missing Data

Financial State does not silently invent unavailable facts.

A metric can carry:
- `available = true`
- `available = false`
- a `reason` explaining why it is unavailable

For example, EMI burden becomes unavailable when a liability does not provide a usable EMI/frequency combination. Asset-derived liquidity and financial-asset values depend on authoritative asset classifications.

Downstream engines should respect metric availability instead of substituting arbitrary defaults.

## Classification and Ownership Rules

### Asset classification

Asset liquidity and financial-asset status are determined from the active `asset_type_master` classification.

If an asset cannot be classified, the engine marks classification-dependent values as unavailable rather than treating the asset as automatically liquid or financial.

### Ownership

For family scope, asset ownership and liability responsibility percentages are aggregated according to authoritative relationship rows.

For individual scope, only the relevant investor's ownership/responsibility is included.

### Expenses

For individual scope, expense participation percentages determine the investor's share of each expense.

## Snapshot and Lineage Architecture

Financial State is both a current-state service and a snapshot-backed decision context.

The service:
1. reads authoritative raw inputs;
2. computes an input revision hash;
3. checks the latest snapshot;
4. reuses it only when the input revision and context still match;
5. rebuilds Financial State when inputs have changed;
6. persists the rebuilt state as a snapshot.

Snapshots can carry authority metadata including source and input revision. Action-completion snapshots also carry action and strategy-version lineage and are validated before reuse.

This provides reproducibility and prevents a stale financial snapshot from silently becoming the current source of truth.

## Current State vs Historical State

Current Financial State is the live normalized financial context used by subsequent workflows.

Historical Financial State snapshots preserve the financial context associated with prior planning/action decisions.

Therefore:
- current state may change as raw financial inputs change;
- historical snapshots should remain reproducible;
- planning decisions should retain enough financial context to explain why the decision was made.

## Consumers

Financial State is consumed by:
- Goal Planner
- Constraints
- Strategy Eligibility / Decision
- Multi-Goal Planning
- Action Plan generation
- MoneyWheel
- Risk/Profile workflows
- Investment planning
- Financial reporting

Consumers should consume Financial State through the service/contract rather than reconstructing the same financial facts independently.

## Insurance and Other Adjacent Financial Inputs

The financial data repository also exposes insurance policy records.

However, insurance policy data is not currently a first-class field in the canonical `FinancialState` model. It should therefore not be documented as an existing Financial State field until the model/engine contract explicitly incorporates it.

Insurance coverage can currently be consumed by downstream financial-health logic where its own contract requires it.

## Non-Responsibilities

Financial State does not:
- select a strategy;
- select a product;
- decide asset allocation;
- rank strategies;
- determine goal priority;
- perform multi-goal resource allocation;
- approve or reject a financial plan;
- replace MoneyWheel diagnostics;
- replace the canonical calculation system.

## Code

### Primary Financial State implementation
- `backend/models/financial_state.py`
- `backend/services/financial_state_service.py`
- `backend/engines/financial_state/engine.py`
- `backend/data/financial_state_repository.py`
- `backend/data/financial_data.py`
- `backend/api/financial_state.py`
- `backend/schemas/financial_state.py`

### Important integration surface
- `backend/engines/moneywheel/financial_state_adapter.py`

## Canonical Boundary

**Raw Financial Data**  
↓  
**Financial State Service**  
↓  
**Financial State Engine**  
↓  
**Canonical Financial State**  
↓  
**Canonical Calculations**  
↓  
**MoneyWheel / Constraints / Risk / Goal / Strategy / Multi-Goal / Reports**

The key rule is:

> **Financial State owns normalized financial facts. Canonical Calculation owns standardized derived calculations. Decision engines own decisions.**

Keeping these boundaries explicit prevents duplicate calculation authority and inconsistent financial interpretations across the product.
