# Canonical Constraints Architecture & Specification

## 1. Executive Summary & Core Principles

Planvesto me har constraint ek **Canonical ID**, strictly typed **Inputs**, deterministic **Outputs**, aur explicit **Downstream Lifecycle Actions** ke sath define hota hai. 

Constraints system me do primary roles nibhate hain:
1. **Hard Gates:** Jo invalid goals ya financially unsafe strategies ko execution se block karte hain.
2. **Diagnostic & Advisory Rules:** Jo risk profile, ratio health, aur multi-goal surplus allocation me priority overrides aur client explanations generate karte hain.

```
+-----------------------------------------------------------------------------------+
|                                DOMAIN ENGINES                                     |
|  [Financial State]   [MoneyWheel / Ratios]   [RuleEngine]   [Strategy Library]    |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                        CONSTRAINT ADAPTERS & EVALUATOR                           |
|             FinancialRatioConstraintEvaluator | RuleEngine.assess()              |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                       CENTRAL CONSTRAINT AGGREGATOR                               |
|       Aggregates into CanonicalConstraint instances -> ConstraintSet Container    |
+-----------------------------------------------------------------------------------+
                                         |
           +-----------------------------+-----------------------------+
           |                                                           |
           v                                                           v
+------------------------------------+      +-------------------------------------+
|      STRATEGY DECISION ENGINE      |      |     MULTI-GOAL ORCHESTRATION        |
|  - Ineligible if Hard Gate fails   |      |  - Applies Priority Overrides       |
|  - 8-Fit Pass vs Conditional pool  |      |  - Reallocates Surplus Cash Flow    |
|  - Explanatory diagnostics in PDF  |      |  - Resolves Trade-offs              |
+------------------------------------+      +-------------------------------------+
```

---

## 2. Canonical Constraints Inventory (ID, Inputs, Outputs & Actions)

### A. Goal Validity & Integrity Constraints (`domain: goal_eligibility`)

| Canonical ID (`rule_id`) | Inputs Required | Logic & Evaluation | Output Produced | Output Dene Ke Baad Kya Karega (Lifecycle Action) |
|---|---|---|---|---|
| `goal-positive-horizon` | • `goal.duration_years` (float)<br>• `goal.goal_id` (str) | Check if `duration_years > 0` | • `severity`: `"hard"`<br>• `role`: `"hard_constraint"`<br>• `passed`: `True / False`<br>• `message`: `"Goal horizon must be positive."` | • **If Failed:** Strategy Engine me eligibility reject karta hai (`gate_ok = False`). Strategy recommendation block ho jati hai aur UI me validation error show hota hai.<br>• **If Passed:** Normal strategy applicability evaluate hoti hai. |
| `goal-positive-target` | • `goal.future_target` (float)<br>• `goal.goal_id` (str) | Check if `future_target > 0` | • `severity`: `"hard"`<br>• `role`: `"hard_constraint"`<br>• `passed`: `True / False`<br>• `message`: `"Goal target must be positive."` | • **If Failed:** Strategy calculation execute nahi hoti. Ineligible reason banta hai.<br>• **If Passed:** Funding gap calculation aur strategy scenarios calculate hote hain. |

---

### B. Financial Ratio & Health Constraints (`domain: financial_ratio`)

Inhe `FinancialRatioConstraintEvaluator` evaluate karta hai using canonical ratio formulas.

| Canonical ID (`rule_id`) | Inputs Required | Logic & Thresholds | Output Produced | Output Dene Ke Baad Kya Karega (Lifecycle Action) |
|---|---|---|---|---|
| `RULE_EMERGENCY_RESERVE_CRITICAL` | • `liquid_assets` (float)<br>• `essential_monthly_expenses` (float)<br>• `goals` (list[GoalEvaluationInput]) | `emergency_coverage < 3.0` months (Critical zone) aur goal `is_discretionary == True` (e.g. Vacation, Vehicle) with priority `critical/high` | • `severity`: `"hard"`<br>• `role`: `"hard_constraint"`<br>• `passed`: `False`<br>• `suggested_override_priority`: `"low"`<br>• `override_reason`: Emergency coverage critical zone me hai. | • **Multi-Goal Orchestrator Action:** Discretionary goal ki priority ko automatically demote karke `"low"` kar deta hai taaki investable surplus sabse pehle Emergency Fund corpus banane me jaye.<br>• **Report Action:** Goal Report aur Action Plan me "Critical Reserve Alert" show hota hai. |
| `WARN_EMERGENCY_RESERVE_ATTENTION` | • `emergency_coverage` (float) | `3.0 <= emergency_coverage < 6.0` months (Attention zone) | • `severity`: `"warning"`<br>• `role`: `"recommendation_only"`<br>• `passed`: `True`<br>• `message`: Buffer warning | • Strategy execution block nahi hoti.<br>• Strategy Recommendation aur PDF me advisory warning attach hoti hai. |
| `RULE_DEBT_BURDEN_EXCEEDED` | • `monthly_emi` (float)<br>• `monthly_income` (float)<br>• `goals` (list[GoalEvaluationInput]) | `debt_to_income_ratio > 40.0%` (Critical ceiling) aur discretionary goal prioritized | • `severity`: `"hard"`<br>• `role`: `"hard_constraint"`<br>• `passed`: `False`<br>• `suggested_override_priority`: `"low"`<br>• `override_reason`: Debt solvency threat | • **Multi-Goal Action:** Discretionary commitments ko deprioritize karta hai aur Debt Reduction strategy ko primary pipeline me suggest karta hai.<br>• Cash flow priority debt repayment ko di jati hai. |
| `WARN_DEBT_BURDEN_ATTENTION` | • `debt_to_income_ratio` (float) | `20.0% <= DTI <= 40.0%` | • `severity`: `"warning"`<br>• `role`: `"recommendation_only"`<br>• `passed`: `True` | • Explanatory evidence ke roop me Strategy Recommendation notes me add hota hai. |
| `WARN_SAVINGS_RATE_DEFICIT` | • `monthly_surplus` (float)<br>• `monthly_income` (float) | `savings_rate < 20.0%` | • `severity`: `"warning"`<br>• `role`: `"recommendation_only"`<br>• `passed`: `True`<br>• `message`: Low savings rate warning | • Hard gate nahi banta. Budgeting module aur Action Plan me expense reduction recommendation trigger karta hai. |

---

### C. Strategy 8-Fit Eligibility Gates (`domain: strategy`)

Har candidate strategy par 8 independent business fits evaluate hote hain:

| Fit Canonical ID (`fit_id`) | Inputs Required | Logic & Evaluation | Output Status (`Pass / Conditional / Fail`) | Output Dene Ke Baad Kya Karega (Lifecycle Action) |
|---|---|---|---|---|
| `cashflow_fit` | • `strategy_required_monthly_contribution`<br>• `investable_surplus_monthly` | • `surplus <= 0` -> Fail<br>• `required <= surplus` -> Pass<br>• `required > surplus` -> Conditional (with shortfall ₹) | `Pass` / `Conditional` / `Fail` + `required_changes` | • **Fail:** Strategy recommendation pool se bahar nikal di jati hai.<br>• **Conditional:** Recommendation pool me tabhi aati hai jab koi Pass strategy na bache. Strategy report me required surplus increment display hota hai. |
| `liquidity_fit` | • `liquid_assets`<br>• `required_liquidity` | • `liquid >= reserve` -> Pass<br>• `liquid < reserve` -> Conditional (liquidity gap ₹) | `Pass` / `Conditional` | • Conditional aane par required liquidity buffer accumulate karne ka milestone add hota hai. |
| `debt_fit` | • `emi_burden_monthly`<br>• `investable_surplus_monthly` | • Non-negative surplus -> Pass<br>• Negative surplus with debt -> Fail | `Pass` / `Fail` | • Fail hone par strategy reject hoti hai aur Debt Reduction architecture recommend hota hai. |
| `asset_resource_fit` | • `available_asset_resource`<br>• `strategy_required_asset_resource` | • `available >= required` -> Pass<br>• `available < required` -> Conditional | `Pass` / `Conditional` | • Conditional aane par re-allocation recommendation surface hoti hai. |
| `risk_capacity_fit` | • `strategy_required_risk`<br>• `risk_capacity`<br>• `de_risked_strategy_risk` | • `required <= capacity` -> Pass<br>• De-risked variant fits -> Conditional<br>• Exceeds capacity -> Fail | `Pass` / `Conditional` / `Fail` | • Exceeds capacity hone par high-risk strategy reject hoti hai; conservative/de-risked variant ko promote kiya jata hai. |
| `goal_constraint_fit` | • `goal_type`<br>• `duration_years`<br>• `funding_gap`<br>• `strategy.constraints` | Library constraints (e.g. `horizon>=7`, `funding_gap<=limit`) check hote hain | `Pass` / `Fail` | • Fail hone par strategy ineligible ho jati hai. |
| `multi_goal_conflict_fit` | • `higher_priority_goal_conflict` | High-priority goal funding compromise ho rahi hai ya nahi | `Pass` / `Conditional` / `Fail` | • Hard conflict hone par current goal ki strategy block hoti hai taaki higher-priority goal safe rahe. |
| `implementation_fit` | • Strategy implementation parameters & regulatory readiness | Strategy practical roop se investable hai ya nahi | `Pass` / `Conditional` / `Fail` | • Fail hone par alternative execution path choose hota hai. |

---

### D. Strategy Library Numerical Constraints (`domain: strategy`)

Har Strategy Definition (`backend/library/strategies/canonical.py`) ke paas library-level constraints hote hain:

| Canonical ID Pattern | Example | Inputs Required | Output | Output Dene Ke Baad Kya Karega |
|---|---|---|---|---|
| `horizon<=X` | `horizon<=5` | `duration_years` | Ineligibility Reason string | Agar goal horizon limit se bahar hai toh candidate strategy list se filter out ho jati hai. |
| `horizon>=X` | `horizon>=7` | `duration_years` | Ineligibility Reason string | Long-term strategies (e.g. wealth creation) near-term goals ke liye eliminate ho jati hain. |
| `funding_gap<=X` | `funding_gap<=5000000` | `funding_gap` | Ineligibility Reason string | Capacity constraint cross hone par strategy reject hoti hai. |

---

## 3. Unified Output Data Model (`CanonicalConstraint` & `ConstraintSet`)

Har domain engine ka output central container me convert hota hai:

```python
class CanonicalConstraint(BaseModel):
    constraint_id: str                # Unique identifier
    rule_id: str                      # Canonical business rule ID
    domain: ConstraintDomain          # financial_ratio | risk_capacity | goal_eligibility | strategy
    source: str                       # e.g. "financial_state", "observed_behavior"
    source_engine: str                # e.g. "FinancialRatioConstraintEvaluator", "RuleEngine"
    severity: ConstraintSeverity      # "hard" | "warning" | "info"
    role: ConstraintRole              # "hard_constraint" | "eligibility" | "ranking_input" | "recommendation_only"
    passed: bool                      # True if rule satisfied, False if violated
    message: str                      # Human-readable diagnostic text
    value: float | None               # Numeric ratio/value (e.g. 45.2% DTI)
    unit: str | None                  # "%" | "months" | "INR"
    goal_id: str | None               # Specific goal linked to this constraint
    evidence: dict[str, Any]          # Underlying data (e.g. {"monthly_emi": 50000, "income": 100000})
    suggested_override_priority: str  # "low" (if override suggested)
    override_reason: str | None       # Rationale for downstream engines
```

`ConstraintSet` typed accessors provide karta hai:
- `constraint_set.hard_constraints`: Sirf wahi constraints jinki severity `"hard"` hai aur `passed == False`.
- `constraint_set.warnings`: Informational/planning alerts (`severity == "warning"`).
- `constraint_set.conflicts`: Jab do alag engines same metric par disagree karein (`ConstraintConflict`).

---

## 4. Output Dene Ke Baad Downstream Lifecycle ("Output Ke Baad Kya Hota Hai?")

Jab `ConstraintAggregator.aggregate()` output generate karta hai, system 4 sequential stages me act karta hai:

### Step 1: Strategy Ineligibility Gating (`evaluate_eligibility`)
- Har candidate strategy ke liye check hota hai:
  ```python
  if constraint_set is not None:
      for constraint in constraint_set.hard_constraints:
          if not constraint.passed:
              reasons.append(constraint.message)
  ```
- **Action:** Agar ek bhi hard constraint fail hua, toh wo candidate strategy `ineligible` mark ho jati hai (`status = FAIL`). Wo strategy recommendation pool se instantly bahar ho jati hai.

### Step 2: Pool Precedence Filtering (`evaluate_decision`)
- Remaining strategies ko unke 8-fit results ke aadhar par segregate kiya jata hai:
  - `passes`: Jinke sabhi fits `Pass` hain.
  - `conditionals`: Jinka koi fit `Conditional` hai par koi `Fail` nahi hai.
- **Action:**
  - Agar `passes` pool me strategies hain, toh sirf **Pass** strategies me se best score wali select hoti hai.
  - Conditional strategies tabhi consider hoti hain jab **zero Pass** strategies bachein.
  - Agar dono khali hain, toh system recommendation ko `infeasible` mark karta hai aur failure reasons expose karta hai.

### Step 3: Multi-Goal Priority Override Engine (`MultiGoalPlanningService`)
- Jab `suggested_overrides` me koi goal aata hai (e.g. Vacation goal demoted to low due to emergency deficit):
- **Action:**
  - Multi-Goal Orchestrator investor ki draft priority ko bypass/demote karta hai.
  - Cash flow simulation me essential goals ko pehle surplus allocate karta hai.
  - Output me audit log generate karta hai: `"Discretionary commitment deprioritized to preserve essential safety reserves."`

### Step 4: Decision Report & PDF Generation (`GoalReportService`)
- Output constraints strategy run metadata me persist hoti hain.
- **Action:**
  - PDF export (`generate_pdf`) ke "Risk & Contingency" table me constraints render hoti hain.
  - Investor ko exact actionable advice milti hai: *"Increase monthly available surplus by ₹12,000 to move from Conditional to Feasible."*
