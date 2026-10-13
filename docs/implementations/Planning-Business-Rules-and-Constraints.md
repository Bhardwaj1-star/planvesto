# Planning, Business Rules & Constraints — Code Audit Register

**Document type:** Cross-feature business-rule and constraint audit  
**Audience:** Financial planners, product owners and engineering  
**Audit basis:** Existing backend code on the repository's default branch  
**Purpose:** One reference showing the rule, its current behavior, where it is defined, which feature consumes it, and what still needs verification.

> **Audit principle:** This register records behavior found in code. It does not convert a planned business rule into an implemented rule. Where a rule is described in documentation but code evidence is incomplete, that limitation is called out. Thresholds below are code values, not a claim that they are universally suitable financial advice.

---

## 1. Executive Summary

Planvesto has a shared constraint framework, but **not every planning and business rule is fully centralized in one place**.

- `backend/engines/constraints/models.py` defines a common format for constraints, including source, severity, role, evidence, validity and goal association.
- `backend/engines/constraints/aggregator.py` combines rule-engine results, financial-ratio assessments, Moneywheel outputs, risk-profile constraints and strategy constraints into a shared `ConstraintSet`.
- `backend/engines/constraints/policy.py` owns several important constraint IDs, thresholds, priority ranks, source priorities and normalization/conflict-handling helpers.
- `backend/rules/canonical.py` is a metadata registry for canonical rule IDs, scopes and roles. It does **not** own all runtime behavior or every threshold.
- Domain-specific rules remain in files such as `backend/rules/moneywheel.py`, `backend/rules/goals.py`, `backend/rules/multi_goal.py`, `backend/rules/protection.py`, `backend/rules/eligibility.py`, `backend/rules/strategy_decision.py`, and the relevant engines.
- Some logic is duplicated, hardcoded outside the policy file, or represented in the registry without an exact one-to-one connection to runtime behavior. Those are audit findings, not assumptions that the system is fully centralized.

### How to read this document

- **Hard constraint:** can block a path or impose a non-negotiable condition.
- **Eligibility check:** decides whether a strategy can be considered, can proceed conditionally, or fails.
- **Warning / recommendation:** highlights a concern; it is not automatically a hard block.
- **Diagnostic evidence:** a measurement or explanation used by another decision. A “critical” ratio status is not automatically a hard constraint.
- **Transformation / classification rule:** normalizes or calculates data, rather than deciding whether a path is allowed.

---

## 2. Central Constraint Framework

| Area | Current code owner | What it does | Main consumers / features | Audit finding |
|---|---|---|---|---|
| Canonical constraint format | `backend/engines/constraints/models.py` | Standard fields for identity, source, severity, role, value, evidence, validity, pass/fail and optional goal association | Strategy Engine and downstream planning code | Shared format exists. It is a data contract, not the owner of every rule. |
| Constraint policy | `backend/engines/constraints/policy.py` | Selected rule IDs, threshold constants, priority ranks, source priority, normalization, conflict detection, priority validation | Constraint evaluator, Risk Profiler, Profile and Multi-Goal rules | Partial centralization; some benchmarks remain elsewhere. |
| Constraint assembly | `backend/engines/constraints/aggregator.py` | Collects available outputs from RuleEngine, ratio evaluator, Moneywheel, Risk Profiler and strategy rules | Strategy Engine / planning orchestration | Central aggregator exists, but inputs are optional; a caller can aggregate only the sources it supplies. |
| Conversion to common format | `backend/engines/constraints/adapters.py` | Converts each domain's result into canonical constraints | Constraint Aggregator | Adapter maps roles/severity and preserves evidence. It should not be mistaken for the source of business policy. |
| Rule identity catalogue | `backend/rules/canonical.py` | Names rules, their scope, role and source module | Rule discovery and governance | Metadata registry is not the complete runtime rulebook; some active rules are absent or represented differently. |
| Legacy constraint import | `backend/rules/constraints.py` | Re-exports selected symbols from `engines.constraints.policy` | Older callers | Compatibility layer, not a separate intended policy owner. |

### Constraint data handling rules found in code

- Constraint records can preserve source, evidence, confidence and a validity period.
- Supported sources include financial state, observed behavior, declared constraints and preferences.
- Source-priority ordering is: financial state (4), observed behavior (3), declared constraint (2), preference (1).
- If confidence is not supplied, the policy helper derives it from source priority and evidence count.
- Different values for the same constraint key are recorded as an **unresolved conflict**; the helper does not automatically decide which conflicting value is correct.
- Priority validation rejects unknown constraint keys, duplicate keys, non-integer ranks below 1 and duplicate ranks.
- Behavioral observations require a supported dimension and evidence. Missing observations remain `insufficient_evidence`; the system must not invent a behavioral score.
- Behavioral constraints are marked for **product selection only** in the observed-behavior policy. They should not silently become goal-feasibility blockers.

**Important limitation:** the presence of these helpers does not prove that every feature passes all its constraints through the aggregator. Each call path must be checked independently.

---

## 3. Financial Health / Moneywheel Rules

### 3.1 Nine canonical Moneywheel ratios

The canonical ratio list is defined in `backend/rules/moneywheel.py`. `backend/engines/moneywheel/engine.py` calculates these ratios using the shared calculation functions and assigns a status using the benchmark bands.

| Ratio | Current code calculation | Current status bands in code | Feature use / interpretation |
|---|---|---|---|
| Savings Rate | `(Income - Expenses) / Income × 100` | Excellent ≥30%; Healthy ≥20% and <30%; Attention ≥10% and <20%; Critical <10% | Moneywheel financial-health evidence; ratio evaluator can create a savings warning when status is attention/critical. |
| Liquid Asset Ratio | Liquid assets / total assets ×100 | Excellent ≥25%; Healthy 15–<25%; Attention 10–<15%; Critical <10% | Moneywheel liquidity composition evidence. Not, by itself, a goal-specific hard block. |
| Debt-to-Income Ratio | Monthly debt payments / gross monthly income ×100 | Excellent <20%; Healthy 20–<30%; Attention 30–<40%; Critical ≥40% | Moneywheel debt-burden evidence; a critical status can trigger a constraint on high-priority discretionary goals in the ratio evaluator. |
| Leverage Ratio | Total liabilities / total assets ×100 | Excellent <20%; Healthy 20–<30%; Attention 30–<50%; Critical ≥50% | Moneywheel balance-sheet leverage evidence. The benchmark bands are defined in `rules/moneywheel.py`, not wholly in policy.py. |
| Financial Asset Ratio | Financial assets / total assets ×100 | Excellent ≥70%; Healthy 50–<70%; Attention 30–<50%; Critical <30% | Moneywheel asset-composition evidence. |
| Insurance Coverage Ratio | Existing sum assured / required insurance cover ×100 | Excellent ≥80%; Healthy 60–<80%; Attention 40–<60%; Critical <40% | Moneywheel protection evidence; uses required-cover calculation from protection rules. |
| Goal Funding Ratio | Current goal funding / goal target ×100 | Excellent ≥100%; Healthy 80–<100%; Attention 50–<80%; Critical <50% | Goal funding progress evidence. |
| Future Funding Ratio | Projected goal funding / future goal target ×100 | Excellent ≥100%; Healthy 80–<100%; Attention 50–<80%; Critical <50% | Projected goal funding evidence. |
| Required Rate of Return | Required annualized return implied by future target, current funding and duration | Excellent <8%; Healthy 8–<12%; Attention 12–<15%; Critical ≥15% | Goal-level return-requirement evidence. This is a required-return classification, not a return forecast or promise. |

**Ratio availability rule:** if required inputs are missing, a denominator is zero, or a result is not finite, Moneywheel marks that ratio unavailable and records a reason. It does not manufacture a numeric ratio.

**Important distinction:** Moneywheel status bands primarily classify financial evidence. A “critical” label becomes a hard constraint only where a separate policy/evaluator explicitly makes it one.

### 3.2 Additional financial constraints in the ratio evaluator

Owner: `backend/engines/constraints/evaluator.py`  
Main consumers: constraint aggregation, goal prioritization and strategy eligibility where the resulting ConstraintSet is supplied.

| Rule / check | Current code behavior | Effect |
|---|---|---|
| Emergency reserve critical | Emergency coverage below 3 months is classed as critical in the ratio evaluator. High/critical-priority discretionary goals can receive a failed hard constraint and a suggested priority reduction to low. | Can constrain the relevant discretionary goal. It does not automatically make every goal infeasible. |
| Emergency reserve attention | Coverage below the 6-month healthy benchmark but not critical produces a warning. | Advisory warning; not the same as a hard failure. |
| Emergency reserve excellent | Evaluator has a separate ≥9-month excellent band. | This 9-month band is hardcoded in evaluator.py rather than fully owned by policy.py. |
| Debt burden critical | DTI ≥40% is critical; high/critical-priority discretionary goals can receive a failed hard constraint and suggested priority reduction to low. | Can constrain relevant discretionary goals to protect debt serviceability. |
| Debt burden attention | DTI in the 30%–40% range produces a warning. | Advisory warning. |
| Savings rate deficit | Savings rate in critical/attention bands produces a warning that expense reduction may be needed. | Advisory warning; not a hard block by itself. |
| Positive goal horizon | Goal duration must be greater than zero. | Hard goal-validity check. |
| Positive goal target | Future goal target must be greater than zero. | Hard goal-validity check. |
| Leverage benchmark | Moneywheel classifies leverage using 20% / 30% / 50% bands. The ratio evaluator’s displayed benchmark also contains 30% healthy and 50% critical values. | Evidence/benchmark; verify if any downstream rule treats it as blocking. |

**Implementation caveat:** the ratio evaluator reads and calculates financial metrics from the financial context, with fallback field names. A metric can be absent and therefore not evaluated. The exact inputs provided by each feature/API call must be checked before assuming a constraint was applied.

### 3.3 Threshold ownership issues found

- DTI threshold values are referenced by the canonical policy and Moneywheel bands; the status ranges are defined in `rules/moneywheel.py`.
- Savings healthy benchmark is shared from policy, while the other savings bands are in `rules/moneywheel.py`.
- Leverage thresholds (20%, 30%, 50%) remain in `rules/moneywheel.py`; evaluator.py also has a hardcoded benchmark string.
- Emergency reserve has 3-month and 6-month constants in policy, while the ≥9-month “excellent” band is hardcoded in evaluator.py.
- The rule registry in `rules/canonical.py` describes Moneywheel ratios as explanatory evidence. Runtime evaluator logic separately determines when certain metrics create goal-specific hard constraints or warnings.

These are candidates for a later centralization pass; this document does not change code.

---

## 4. Goal Identity, Validity and Priority Rules

**Main owners:** `backend/rules/goals.py`, `backend/engines/goal/engine.py`, `backend/engines/constraints/evaluator.py`.

### 4.1 Canonical goal types

The backend canonical goal list is:

- Retirement
- Marriage
- Vehicle
- Dream Home
- Education
- Vacation
- Debt Freedom
- Wealth Creation
- FIRE / Passive Income
- Others

Goal type is the canonical identity. Beneficiary, child, purpose details and other circumstances belong in contextual/dynamic details, not in a new goal type. The normalizer accepts canonical IDs or display names case-insensitively; unknown values normalize to an empty canonical type rather than becoming a new canonical goal.

### 4.2 Goal priority vocabulary

- Canonical priority levels: Critical, High, Medium, Low.
- Accepted labels such as “must-have”, “important”, “moderate”, “aspirational”, “nice-to-have” and “discretionary” normalize to the canonical levels.
- An unrecognized or missing priority currently defaults to **Medium** in `canonical_goal_priority()`.
- Multi-goal priority ranks are Critical=0, High=1, Medium=2, Low=3 in the shared policy. The Multi-Goal helper also accepts numeric ranks supplied as integers or numeric strings; this behavior needs validation at input boundaries.

### 4.3 Essential vs discretionary classification

Current code classifies as **discretionary**:
- Vehicle
- Dream Home
- Vacation
- Wealth Creation
- Others

Current code classifies as **essential**:
- Retirement
- Marriage
- Education
- Debt Freedom
- FIRE / Passive Income

Policy: a discretionary goal must not preempt an essential goal or safety-reserve funding. This is encoded by `can_discretionary_preempt_essential()` in policy.py and exposed in `rules/multi_goal.py`.

**Audit concern:** these are fixed categories in code. If business policy intends a goal's essential/discretionary status to vary by investor circumstances, current classification alone does not represent that nuance.

---

## 5. Goal Planner Rules and Calculations

**Main owners:** `backend/engines/goal/engine.py`, `target_calculator.py`, `funding_gap.py`, `asset_projection.py`, `backend/rules/assumptions.py`, and canonical calculation functions.

| Rule / calculation | Current code behavior | Goal Planner use | Important limitation |
|---|---|---|---|
| Goal identity | Normalizes goal type/name to the canonical goal taxonomy. | Prevents aliases/beneficiaries from becoming new goal identities. | Unknown goal type should be surfaced/validated by callers; canonical normalizer itself returns empty for unknown values. |
| Duration | Calculates remaining months from target month/year and reference date; past dates return zero duration. | Determines horizon for future cost and funding calculations. | A zero duration is also invalid under the positive-horizon hard constraint. |
| Default inflation | Uses 6% when no goal-specific inflation rate is supplied. | Estimates future goal requirement. | This is a code default, not a universal inflation forecast; the source must be visible to the planner. |
| Future target | Calculates future cost from today’s cost, inflation assumption and duration. | Establishes target-date requirement. | Depends on assumptions and valid inputs. |
| Asset mapping | Each mapped asset must exist in the planning unit and have a name; mapped allocation is projected using current value, allocation type/value, expected return and duration. | Estimates resources considered for the goal. | A missing asset causes an error; mapping is a planning allocation, not proof of legal earmarking. |
| Default funding return | Uses mapped-asset allocated-value-weighted expected returns; if there is no mapped capital, falls back to 8%. | Assumption used in the contribution calculation. | Must not be described as guaranteed/expected market performance. |
| Funding gap | Future target minus projected mapped assets. Positive = Shortfall; near-zero (within ₹0.01) = On Track; negative = Overfunded. | Shows target-date gap/surplus. | A non-calculable gap is currently converted to zero inside the helper; callers must ensure invalid inputs are not confused with “On Track”. |
| Required monthly contribution | For a positive gap and positive duration, calculates an end-of-month monthly contribution using annual return/12 and the number of months. A non-positive gap or zero duration returns zero. | Estimates monthly funding needed. | A zero contribution with an immediate goal can coexist with a funding gap; the gap must remain visible. |
| Retirement corpus | Retirement requires current age and life expectancy in dynamic details; uses a separate retirement corpus calculation and an 8% retirement-return assumption. | Retirement-specific target calculation. | Missing ages raise an error for active goals; cancelled goals have a special fallback of age 30 and life expectancy 85. This fallback needs careful review because it can hide missing data in cancelled records. |
| Required return | Moneywheel/canonical calculation derives return needed from current funding, target and duration. | Return requirement evidence for goal feasibility and strategy-side analysis. | Required return is not a forecast and is undefined when inputs such as current funding are zero or missing. |

### Goal Feasibility ownership boundary

The intended product boundary documented in the user journey is:
- Goal Planner owns goal requirements, funding calculations, funding paths and goal-feasibility assessment.
- Strategy Builder consumes the evidence and develops the strategy-side proposal.
- Strategy Builder should not silently repeat or replace Goal Planner’s feasibility conclusion.

**Audit status:** the Goal Engine calculations above are directly visible in code. The full business sequence of comparing debt prepayment, EMI changes, liquidity, competing goals, opportunity cost and then goal adjustment must be verified against the specific orchestration/service call paths before claiming every branch is implemented.

---

## 6. Multi-Goal Allocation and Shared-Resource Rules

**Main owner:** `backend/rules/multi_goal.py`; related policy in `backend/engines/constraints/policy.py`.

- Priority values are normalized into the canonical vocabulary and mapped to precedence ranks.
- A lower numeric rank represents higher precedence in the priority-rank map (Critical 0, High 1, Medium 2, Low 3).
- A discretionary goal cannot preempt an essential goal.
- Funding statuses include fully funded, partially funded, unfunded, within surplus, surplus shortfall and requires review.
- Feasibility statuses include pass, conditional and infeasible.
- Multi-goal impact should be relevant when goals compete for shared assets, surplus, liquidity or other resources.

**Important distinction:** the rule registry says goal priority order is an architecture constraint. Whether that rule actually blocks, changes ranking, or only informs recommendations depends on the downstream consumer. The rule ID alone does not establish that effect.

---

## 7. Strategy Builder Rules

**Rule definitions / consumers:** `backend/rules/eligibility.py`, `backend/engines/strategy/eligibility.py`, `backend/engines/strategy/decision.py`, `backend/rules/strategy_decision.py`, `backend/engines/rules/engine.py`, and the ConstraintSet.

### 7.1 Eight eligibility checks in backend code

The current backend eligibility module defines these eight checks. They are an internal code-level assessment list; their existence does not mean the UI must display eight separate cards or stages.

| Eligibility check | How code uses it | Result when it fails or evidence is missing |
|---|---|---|
| Cash-flow fit | Compares the strategy’s required monthly contribution with available monthly surplus. If surplus is absent, it attempts to derive it from income minus expenses and EMI. | Missing evidence → Conditional; no/non-positive surplus → Fail; required contribution above surplus → Conditional with a shortfall amount. |
| Liquidity fit | Compares liquid assets with required liquidity/safety reserve. | Missing data → Conditional; reserve shortfall → Conditional with the liquidity gap. |
| Debt fit | Checks debt/EMI serviceability using the available debt and income evidence. | May fail or be conditional depending on the evidence and implemented checks. Verify full call path before claiming all debt cases are covered. |
| Asset-resource fit | Checks whether resources needed for the strategy are available. | Missing evidence or resource gap can require a conditional change. |
| Risk-capacity fit | Compares strategy risk requirement with investor risk capacity. | Missing risk evidence → Conditional; required risk above capacity → Fail. |
| Goal-constraint fit | Checks canonical goal type, horizon and strategy-defined constraints such as `horizon<=`, `horizon>=`, `funding_gap<=` and `funding_gap>=`. | Matching strategy limits can exclude the strategy; malformed numeric constraints are currently ignored by the local parser. |
| Multi-goal-conflict fit | Checks whether the strategy compromises a higher-priority goal or shared resources. | May require resource reallocation without materially compromising higher-priority goals. |
| Implementation fit | Checks whether implementation evidence and required changes are available/feasible. | Missing implementation inputs can make the candidate conditional or fail through other gates. |

Eligibility statuses:
- **PASS:** checks pass.
- **CONDITIONAL:** the strategy may work if specified changes or evidence are supplied.
- **FAIL:** one or more blocking eligibility checks fail.

A conditional candidate is not the same as a fully viable, ready-to-execute proposal. The code's overall status combines the individual fit results and other eligibility gates.

### 7.2 Strategy applicability

The library-level `StrategyRuleEngine` first checks whether the canonical goal type is in the strategy’s applicable goal types. If applicable goal characteristics are configured, it tests signals such as:
- Funding shortfall / on-track / overfunded.
- Near-term (≤5 years) / long-term (≥7 years).
- Fixed / flexible timeline.
- High / critical priority.

A strategy is treated as characteristic-matched when at least one configured characteristic matches. This is distinct from the later financial eligibility check.

### 7.3 Strategy decision scoring found in code

`backend/rules/strategy_decision.py` defines numeric scoring inputs:
- Primary goal-type match: 25; other-goal match: 10.
- Characteristic match: 5 per applicable characteristic.
- Optimal horizon fit: 30; baseline horizon fit: 15.
- Feasibility: pass 15; conditional 8; fail 0.
- Technique execution contribution: capped at 10.
- Failed eligibility returns a decision score of -1000.
- Funding fit adds special scores for selected legacy strategy IDs and funding/debt conditions.
- Component score can add points for component activation/supporting strategies.

**Important discrepancy:** scoring logic still references strategy IDs such as `strat-dynamic-accumulation`, `strat-calibrated-growth`, `strat-high-liquidity-flex`, `strat-cap-preservation`, and `strat-debt-reduction`. These IDs do not map cleanly to the four canonical business strategy names in the simplified Strategy Builder documentation. This needs a code-to-canonical-strategy mapping audit; do not assume the four canonical strategies are already the only runtime strategy identities.

The scoring code is evidence of current runtime behavior. It should not be presented as an approved business weighting policy unless the product owner has explicitly ratified these weights.

### 7.4 Hard constraints passed to Strategy Builder

The Strategy Engine can use a ConstraintSet’s failed hard constraints as ineligibility reasons. However:
- Some financial-state conditions are policy overrides rather than universal build blockers.
- Ratio status alone is adapted as diagnostic evidence; explicit constraint-check results carry goal-specific hard/warning effects.
- The aggregator accepts optional sources, so an omitted source will not contribute constraints to that invocation.
- A code path that falls back to a raw RuleAssessment can behave differently from one that receives a complete ConstraintSet. Callers need consistent use of the canonical aggregator.

---

## 8. Risk Profiler and Behavioral Rules

**Owners:** `backend/engines/risk_profiler/engine.py`, `backend/rules/risk_profiler.py`, `backend/engines/profile/behavioral.py`, `backend/engines/constraints/policy.py`.

### Risk Required
- Consumes the canonical required-risk/return calculation from the calculation layer when the required inputs are available.
- Evidence can include future target, current funding and time horizon.
- If required evidence is unavailable, Risk Required is marked unavailable rather than inventing a value.
- The current implementation also supports an explicit override input; the source and precedence of that override should be governed and auditable.

### Risk Capacity
- Derived from observable financial information such as investable surplus, safety reserve, EMI/debt service, assets and liabilities.
- The comparison helper returns Conditional if either required risk or capacity is missing.
- Returns Pass when required risk is within capacity; Fail when required risk exceeds capacity.
- Strategy definitions can declare the required risk capacity.

### Risk Tolerance / observed behavior
- Uses five supported behavior dimensions: decision consistency, volatility reaction, discipline, intervention tendency and loss/uncertainty response.
- Observations require evidence and retain confidence and validity information.
- Missing behavior remains insufficient evidence; it is not replaced by hypothetical answers.
- Behavior constraints are labelled for product selection only. They must not be converted into invented risk-capacity values or hard goal constraints.

### Constraint provenance
Risk/Profile policy can preserve whether a value came from financial state, observed behavior, a declared constraint or a preference. Conflicting values are recorded as unresolved. Current helpers detect the conflict; they do not establish a complete business resolution policy.

---

## 9. Insurance / Protection Rules

**Owner:** `backend/rules/protection.py`; consumed by Moneywheel and related protection calculations.

- Baseline required insurance cover = **10 × gross annual income + outstanding liabilities**.
- Negative income or liability inputs are floored at zero in the calculation.
- Existing assets are intentionally not netted off against the required cover.
- Recognized life-policy types in code: term insurance, term, endowment, whole life, ULIP and money back.
- Recognized health-policy types: health insurance, health.
- Moneywheel’s Insurance Coverage Ratio compares existing sum assured with the calculated required cover and classifies the coverage ratio into its status bands.

**Audit note:** this is a baseline calculation rule. It does not, by itself, establish a complete insurance suitability recommendation or product-selection rule.

---

## 10. Financial State, Budget and Data Classification Rules

**Owners:** `backend/rules/financial_metrics.py`, canonical calculation functions, and feature-specific engines.

Current classifications in `financial_metrics.py`:

- Short-term liability types: Credit Card, Personal Loan, Consumer Loan, Other.
- Essential expense types: Housing, Utilities, Groceries, Healthcare, Insurance, Education, Debt Payments.
- Unknown expense types default to “Other” in the classification helper and are therefore not classed as essential by this set.
- Financial-state compatibility helpers delegate cash-flow ratio and savings/investment rate calculations to the canonical calculation module; they should not be treated as separate calculation owners.
- Safety-reserve months helper delegates to the canonical calculation function and falls back to 12 when the result is unavailable.

**Audit gaps to verify:**
- Whether frontend/onboarding category options exactly match backend category classification.
- Whether “Other” should ever default to non-essential or unknown instead.
- Whether the safety-reserve fallback of 12 months is an approved business policy or a technical fallback.
- Whether the same income/expense fields and definitions are used consistently by Moneywheel, Goal Planner, Risk Profiler and Strategy Builder.

---

## 11. Action Plan Rules

**Owner:** `backend/rules/action_plan.py`; used when action specifications are generated from a selected strategy architecture.

- The primary strategy produces one **high-priority** action describing execution of the core mechanism.
- Each supporting strategy produces a **medium-priority** action.
- Each implementation technique produces a **medium-priority** action.
- These are action-specification rules. They do not, by themselves, prove that an investor accepted the plan or that execution has happened.

**Required boundary:** accepted-plan status, investor adoption and execution state must remain separate from a strategy recommendation or draft proposal.

---

## 12. Canonical Rule Registry vs Runtime Behavior

`backend/rules/canonical.py` records rule IDs, names, scopes, roles, source modules and version metadata. Examples registered include:
- Goal positive horizon / positive target.
- Canonical goal-type and priority classification.
- Moneywheel ratio classifications.
- Strategy cash-flow, liquidity, debt, asset-resource, risk-capacity, goal-constraint, multi-goal-conflict and implementation fits.
- Goal priority order.
- Discretionary-goal protection of essential goals.
- Required insurance cover.

However, the registry is **not a complete list of all code-backed business behavior**:
- Some active RuleEngine diagnostics (for example priority-sensitive, fixed-timeline, surplus-health and financial-health diagnostics) are defined in runtime code separately.
- Some scoring constants and strategy-ID rules are in `rules/strategy_decision.py`.
- Moneywheel benchmark bands are in `rules/moneywheel.py`.
- Goal calculations and assumptions are in goal-engine modules.
- The eight eligibility fits are in `rules/eligibility.py` and are evaluated by `engines/strategy/eligibility.py`.
- Action generation and protection logic live in separate domain modules.

Therefore, counting entries in `CANONICAL_RULES` would undercount the full set of operational rules.

---

## 13. Cross-Feature Usage Map

| Rule family | Onboarding / Profile | Financial State / Moneywheel | Goal Planner | Risk Profiler | Strategy Builder | Multi-Goal | Action Plan / Investment |
|---|---|---|---|---|---|---|---|
| Canonical goal type / aliases | Input normalization should align | Context | **Direct** | Goal evidence may be consumed | **Direct** for applicability and eligibility | **Direct** for essential/discretionary classification | Indirect |
| Priority vocabulary / ranks | Collects priority input | — | Goal priority context | Constraint provenance possible | Ranking/fit context | **Direct** | May inform priority downstream |
| Financial ratio benchmarks | — | **Direct** | Funding/financial evidence | Capacity inputs | **Direct** when context/ConstraintSet supplied | Shared-resource evidence | Recommendation context |
| Emergency reserve / debt / savings constraints | — | **Direct evidence** | May affect feasibility/priority | **Direct capacity evidence** | Can create goal-specific hard constraints/warnings | Protects essential goals/shared reserve | May affect recommendation/actions |
| Goal validity / target / horizon | — | Goal-related ratios | **Direct** | Required-risk inputs | **Direct** eligibility gates | Goal state | Action context |
| Goal funding gap / required contribution / return | — | Goal ratios / return evidence | **Direct calculation owner** | Required-risk calculation can consume related inputs | Eligibility/scoring can consume required contribution and goal status | Funding status | Proposal/action inputs |
| Essential vs discretionary protection | — | — | Goal classification | Financial constraints can influence | May constrain strategy choices | **Direct policy** | Indirect |
| Risk capacity / tolerance / behavior | Profile inputs | May consume financial metrics | Goal evidence only where passed | **Direct** | **Direct** risk eligibility | Potential shared-plan evidence | Product selection / implementation context |
| Insurance required cover / coverage ratio | Policy data input | **Direct ratio** | May inform protection goal context | Liabilities / financial-state evidence | Could be evidence if passed; not a universal strategy gate | Indirect | Investment/protection decision support |
| Strategy scoring / eligibility | — | Ratio evidence | Supplies goal/funding evidence | Risk capacity evidence | **Direct** | Multi-goal conflict fit | Produces architecture for accepted plan |
| Action generation priority | — | — | — | — | Approved architecture input | — | **Direct** |

“May” and “where supplied” are deliberate: the code contains a rule or consumer interface, but an individual feature only uses it if the active call path passes the relevant inputs/results.

---

## 14. Confirmed Gaps, Overlaps and Risks

1. **Policy is not the sole threshold owner.** Leverage bands, Moneywheel bands and some health diagnostics remain hardcoded outside `engines/constraints/policy.py`.
2. **Rule registry is not exhaustive.** It describes a subset of the runtime rule system and is not sufficient as the only audit source.
3. **Constraint aggregation is optional-input based.** Missing a source from a call means that source’s constraints are absent from that ConstraintSet.
4. **Diagnostic vs blocking semantics need consistency.** A ratio marked “critical” is not automatically a failed hard constraint; the explicit evaluator policy determines whether it affects a goal.
5. **Strategy identities appear inconsistent across policy and documentation.** Scoring functions reference legacy strategy IDs. Map them to the four canonical business strategies before treating score outputs as canonical.
6. **Potential conflicting financial benchmarks exist across consumers.** Audit all thresholds and labels against one approved business policy; do not fix values without product-owner approval.
7. **Goal funding gap fallback may mask invalid data.** The gap helper currently maps a missing/unavailable canonical gap to zero; callers must prevent this from being shown as “On Track”.
8. **Default assumptions require governance.** Goal inflation defaults to 6%; fallback funding return is 8%; retirement return is 8%; required insurance cover uses 10 years of gross income plus liabilities. These values need an explicit owner and user-visible assumption labels.
9. **Unknown priority defaults to Medium.** Confirm whether silent defaulting is acceptable or should instead request investor input.
10. **Essential/discretionary classification is fixed by goal type.** Confirm whether individual circumstances can override that classification.
11. **Eligibility parser silently ignores malformed numeric strategy constraints.** Invalid rule configuration should ideally be visible rather than skipped.
12. **No universal feature-consumption proof from a rule definition alone.** The call path must be traced to establish whether each feature actually supplies and enforces the rule.

---

## 15. Recommended Audit Status Vocabulary

Use these labels in future updates to this register:

- **Code-backed:** behavior is directly visible in an inspected runtime module.
- **Consumed by feature:** the feature call path passes or reads the rule/evidence.
- **Defined but not proven consumed:** a rule exists, but active usage has not been verified.
- **Documented target:** product documentation describes the rule, but current runtime implementation is not confirmed.
- **Conflict / duplicate:** comparable logic or thresholds exist in more than one place.
- **Missing / unclear policy:** code has a fallback or behavior without an approved business definition visible in the inspected sources.

---

## 16. Audit Boundary

This document consolidates the principal backend rule-bearing modules inspected for constraints, Moneywheel, goals, multi-goal logic, Goal Planner calculations, Strategy Builder eligibility/scoring, Risk Profiler, protection, financial classifications and action generation.

It is a **code-audited register, not a claim that every frontend form, API call, database rule, test, scheduled workflow or runtime deployment has been exhaustively traced**. Before calling the entire system fully centralized, the next audit should map every rule to its active call sites and tests, reconcile all duplicate thresholds and legacy strategy IDs, and verify that every relevant feature supplies the canonical ConstraintSet.
