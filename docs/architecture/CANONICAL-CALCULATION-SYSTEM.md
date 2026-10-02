# Canonical Financial Calculation System & Derived Facts Architecture

**Status:** CANONICAL | **Calculation Version:** 1.0.0 | **Branch:** backend-audit-cleanup

> **Canonical Financial Facts / Calculation Layer is the single source of truth for reusable derived financial facts.**

---

## 1. Architectural Model

```
RAW / PRIMARY FINANCIAL DATA (FinancialState, Assets, Liabilities, Goals)
                              ↓
              CANONICAL FINANCIAL CALCULATIONS
              (`backend/engines/calculation/canonical.py`)
                              ↓
              CANONICAL DERIVED FINANCIAL FACTS
                              ↓
┌─────────────────┬───────────────────┬──────────────────────┬─────────────────────────┐
↓                 ↓                   ↓                      ↓                         ↓
MoneyWheel        Risk Profiler       Goal Engine            Constraint Evaluator      Investment Engine
(Diagnostics &   (Capacity, Exposure (Funding Gap &         (Hard/Soft Constraints    (Allocation Gaps &
 Financial Story) & Risk Required)    Contribution Math)     & Ratio Health Gates)     Portfolio Construction)
└─────────────────┴───────────────────┴──────────────────────┴─────────────────────────┘
                                      ↓
                               Strategy Builder
                                      ↓
                                Financial Plan
                                      ↓
                                    Report
```

### Core Separation of Responsibilities
- **Calculation ownership is centralized**: Pure financial mathematics, mathematical formulas, and derived fact extraction are owned strictly by `backend/engines/calculation/canonical.py`.
- **Decision ownership remains domain-specific**:
  - **MoneyWheel**: interprets numbers into financial evidence, resilience status, and diagnostic stories.
  - **Risk Profiler**: evaluates investor risk capacity, portfolio exposure, and compares risk required against capacity constraints.
  - **Goal Engine**: determines goal feasibility, shortfall classification, and priority-driven timelines.
  - **Strategy Engine**: synthesizes facts, goals, and constraints to recommend strategic architectures.

---

## 2. Canonical Ownership & Consumption Matrix

| Financial Fact / Metric | Formula Identity | Canonical Calculation Owner | Primary Fact Output | Consumers | Action Taken |
|---|---|---|---|---|---|
| **Savings Rate** | `(Monthly Surplus / Monthly Income) * 100` | `calculate_savings_rate` | `fact_savings_rate` | MoneyWheel, FinancialStateEngine, ConstraintEvaluator | Replaced duplicate implementations in `rules/financial_state.py` and `evaluator.py`. |
| **Liquid Asset Ratio** | `(Liquid Assets / Total Assets) * 100` | `calculate_liquid_asset_ratio` | `fact_liquid_asset_ratio` | MoneyWheel, RuleEngine, Diagnostics | Centralized in canonical module. |
| **Expense Coverage** | `Liquid Assets / Monthly Expenses` | `calculate_expense_coverage` | `fact_expense_coverage` | MoneyWheel (`rules`), ConstraintEvaluator | Centralized in canonical module. |
| **Emergency Coverage** | `Liquid Assets / Essential Monthly Expenses` | `calculate_emergency_coverage` | `fact_emergency_coverage` | MoneyWheel (`rules`), RuleEngine (`emergency-reserve-health`) | Centralized in canonical module. |
| **Debt-to-Income Ratio (DTI)** | `(Monthly Debt Payments / Monthly Income) * 100` (or ratio) | `calculate_debt_to_income_ratio` | `fact_debt_to_income_ratio` | MoneyWheel, Risk Profiler (`risk_capacity_debt_service_ratio`), ConstraintEvaluator | Removed ad-hoc `round(emi / income, 6)` calculation in `risk.py`. |
| **Leverage Ratio** | `(Total Liabilities / Total Assets) * 100` | `calculate_leverage_ratio` | `fact_leverage_ratio` | MoneyWheel, RuleEngine (`leverage-health`), ConstraintEvaluator | Centralized in canonical module. |
| **Financial Asset Ratio** | `(Financial Assets / Total Assets) * 100` | `calculate_financial_asset_ratio` | `fact_financial_asset_ratio` | MoneyWheel (`financial_asset_ratio`) | Centralized in canonical module. |
| **Insurance Coverage Ratio** | `(Existing Sum Assured / Required Insurance Cover) * 100` | `calculate_insurance_coverage_ratio` | `fact_insurance_coverage_ratio` | MoneyWheel (`insurance_coverage_ratio`) | Centralized in canonical module. |
| **Goal Funding Ratio** | `(Current Goal Funding / Goal Target Amount) * 100` | `calculate_goal_funding_ratio` | `fact_goal_funding_ratio` | MoneyWheel (`goal_funding_ratio`) | Centralized in canonical module. |
| **Future Funding Ratio** | `(Projected Goal Funding / Future Goal Target) * 100` | `calculate_future_funding_ratio` | `fact_future_funding_ratio` | MoneyWheel (`future_funding_ratio`) | Centralized in canonical module. |
| **Required Rate of Return (Risk Required)** | `((Future Target / Current Funding) ^ (1 / Duration) - 1) * 100` | `calculate_required_rate_of_return` / `calculate_risk_required` | `fact_required_rate_of_return` / `fact_risk_required` | MoneyWheel, Risk Profiler (`risk_need_required_return`), Goal Feasibility | Unified single owner. Risk Profiler consumes from canonical calculation rather than recalculating. |
| **Portfolio Concentration** | `Largest Asset Value / Total Assets` | `calculate_portfolio_concentration` | `fact_portfolio_concentration` | Risk Profiler (`risk_exposure_max_asset_concentration`), MoneyWheel | Removed ad-hoc `round(largest / total_assets, 6)` calculation in `risk.py`. |
| **Goal Future Value (Target)** | `Today Cost * ((1 + Inflation Rate) ^ Duration)` | `calculate_goal_future_target` | Pure / Engine fact | Goal Engine (`calculate_future_target`) | Delegated from `target_calculator.py`. |
| **Goal Funding Gap** | `Future Target - Projected Mapped Asset Value` | `calculate_goal_funding_gap` | `fact_goal_funding_gap` | Goal Engine (`calculate_funding_gap`) | Delegated from `funding_gap.py`. Domain classifies "Shortfall" / "On Track" / "Overfunded". |
| **Required Monthly Contribution** | Amortization of gap at monthly return assumption | `calculate_required_monthly_contribution` | `fact_required_monthly_contribution` | Goal Engine (`funding_gap.py`), MultiGoalOrchestrator | Centralized formula. |

---

## 3. Risk Required Single-Owner Consumption Model

Risk Required represents the annualized compound rate of return needed for current mapped capital to reach the future goal target over the remaining horizon:

$$\text{Risk Required} = \left[\left(\frac{\text{Future Goal Target}}{\text{Current Goal Funding}}\right)^{\frac{1}{\text{Duration Years}}} - 1\right] \times 100$$

- **Canonical Owner:** `backend/engines/calculation/canonical.py::calculate_risk_required` (alias to `calculate_required_rate_of_return`).
- **MoneyWheel:** Reads `required_rate_of_return` as diagnostic financial evidence.
- **Risk Profiler:** Consumes `risk_need_required_return` as the required-risk dimension to compare against investor Risk Capacity and Risk Tolerance. Risk Profiler does **not** recalculate this return assumption independently.

---

## 4. Calculations Intentionally NOT Centralized (Domain-Specific)

To avoid leaking domain-specific business rules into the pure mathematical layer, the following remain strictly owned by their respective domain engines:

1. **Rule Classification / Status Benchmarks (`backend/rules/moneywheel.py`):**
   - Threshold ranges (`excellent`, `healthy`, `attention`, `critical`) remain planning policy rules versioned under `rules/moneywheel.py`.
2. **Goal Feasibility & Classification (`backend/engines/goal/funding_gap.py`):**
   - Categorization into `"Shortfall"`, `"On Track"`, `"Overfunded"` remains in `Goal Engine`.
3. **Specialized Retirement Corpus Math (`backend/engines/goal/target_calculator.py`):**
   - Growing annuity valuation (`calculate_retirement_corpus`) requires mortality assumptions, retirement age projections, and post-retirement drawdown modeling specific to retirement goals.
4. **Strategy Applicability, Scenarios, and Ranking (`backend/engines/strategy/`):**
   - Strategy architecture synthesis, trade-offs, and multi-goal allocation remain in `Strategy Engine`.
5. **Asset Master Type Resolution (`backend/services/moneywheel_service.py`):**
   - Heuristic classification of raw account strings to master flags (`is_liquid`, `is_financial`) remains in data/service layers.

---

## 5. Missing Data Safety & Non-Zero Invariant

- **Rule:** Missing data is **never** silently treated as zero.
- If any required input (`income`, `total_assets`, `duration`, `target`) is `None` or non-positive where positivity is mathematically required (e.g. division by zero, logarithms of non-positive numbers), the canonical function returns `None`.
- Fact objects produce `available=False` and `data_quality="unavailable"` with an explicit explanation. Downstream engines record diagnostic warnings rather than false constraint failures.
