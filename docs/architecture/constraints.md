## Constraints Architecture

The Constraints layer evaluates financial and goal-level constraints that can restrict planning decisions. It is distinct from Goal Planner feasibility and from Strategy Eligibility: constraints can create hard gates, warnings, suggested priority overrides, and explanatory ratio evidence.

| Constraint Stage | Input / Data | Logic / Rule | Output | Downstream Use |
|---|---|---|---|---|
| Financial Context | Income; expenses; surplus; assets; liabilities; EMI; liquid assets; liquidity breakdown | Extract and normalise available financial metrics | Canonical financial inputs for constraint evaluation | Ratio evaluation |
| Financial Ratios | Financial Context | Calculate Savings Rate, Emergency Coverage, Debt-to-Income Ratio, and Leverage Ratio; classify each against approved thresholds | Ratio values + status + benchmark + evidence | Constraint assessment; diagnostics |
| Goal Validity Constraints | Defined Goal | Check mandatory goal horizon and future target are positive | Hard constraint checks: Goal Positive Horizon; Goal Positive Target | Rule Assessment; Strategy eligibility |
| Emergency Reserve Constraint | Emergency Coverage + Goals | Critical reserve can hard-constrain high/critical-priority discretionary goals; attention range creates a warning | Hard constraint / warning; suggested priority override where applicable | Strategy decisioning; priority resolution |
| Debt Burden Constraint | Debt-to-Income Ratio + Goals | Critical debt burden can hard-constrain high/critical-priority discretionary goals; attention range creates a warning | Hard constraint / warning; suggested priority override where applicable | Strategy decisioning; priority resolution |
| Savings Rate Constraint | Savings Rate | Critical/attention savings rate produces a planning warning | Warning evidence | Planning explanation; no direct hard gate |
| Constraint Assessment | All ratio results + goal checks | Separate hard constraints, warnings, and suggested overrides | `RatioConstraintAssessment` | Rule/constraint consumers |
| Strategy Eligibility Constraint Gate | Constraint assessment + candidate strategy + goal | Hard constraint failures are added to strategy ineligibility reasons | Eligible / Ineligible | Strategy decision ranking |
| 8-Fit Eligibility | Strategy + Defined Goal + financial context | Evaluate the common eight eligibility fits independently of the constraint diagnostics | Pass / Conditional / Fail per fit | Strategy ranking and recommendation |

## Constraint Reference Matrix

| Domain | Constraint | How It Works |
|---|---|---|
| Goal | Positive Horizon | Goal duration must be greater than zero. If the horizon is zero or negative, the goal fails a hard validity constraint and cannot proceed normally into strategy decisioning. |
| Goal | Positive Future Target | Future target must be greater than zero. A zero or negative target is a hard goal-validity failure. |
| Liquidity | Emergency Reserve | Emergency coverage is evaluated against approved thresholds. A critical reserve condition can hard-constrain high/critical-priority discretionary goals; an attention condition produces a warning. A priority override may be suggested. |
| Debt | Debt-to-Income Ratio | Monthly/annual debt burden is evaluated against approved DTI thresholds. A critical condition can hard-constrain high/critical-priority discretionary goals; an attention condition produces a warning. |
| Savings | Savings Rate | Savings capacity is evaluated against approved savings-rate thresholds. Critical or attention classifications generate planning warnings; this constraint does not directly create a hard strategy gate. |
| Leverage | Leverage Ratio | Total liabilities are evaluated relative to the relevant asset/equity base using the canonical financial-ratio calculation. The result provides financial-risk evidence for constraint assessment. |
| Cash Flow | Cash-flow Fit | Required monthly strategy contribution is compared with available monthly surplus. Missing data is Conditional; no surplus is Fail; sufficient surplus is Pass; insufficient surplus is Conditional with the required increase identified. |
| Liquidity | Liquidity Fit | Available liquid assets are compared with required liquidity. Missing evidence is Conditional; sufficient liquidity is Pass; insufficient liquidity remains Conditional rather than automatically failing. |
| Debt | Debt Fit | Debt/EMI evidence is checked against the strategy context. Missing EMI evidence is Conditional; a non-negative surplus passes; negative surplus fails. |
| Assets | Asset Resource Fit | Required strategy resources are compared with available strategy asset resources. Missing evidence is Conditional; sufficient resources Pass; insufficient resources are Conditional. |
| Risk | Risk Capacity Fit | Required strategy risk is compared with investor risk capacity. Missing evidence is Conditional; within capacity Pass; a de-risked strategy may remain Conditional; exceeding capacity fails. |
| Goal Constraints | Goal Constraint Fit | Strategy-specific goal constraints such as goal type, horizon and funding-gap conditions are evaluated. Satisfied constraints Pass; violated hard constraints Fail. |
| Multi-Goal | Multi-goal Conflict Fit | Higher-priority goal/conflict evidence is checked against the candidate strategy. Missing evidence is Conditional; an actual conflict fails; an explicitly conditional conflict remains Conditional. |
| Implementation | Implementation Fit | Implementation readiness/evidence is checked. Missing evidence is Conditional; ready/pass is Pass; conditional readiness is Conditional; an invalid implementation state fails. |

## Constraint Failure and Strategy Selection

A failed constraint does not mean the system blindly selects another strategy. The failure is evaluated against each candidate strategy, and only the affected strategy is removed when the failure becomes a strategy-level hard gate.

| Step | What Happens | Result |
|---|---|---|
| 1. Applicable Strategies | Goal type and configured goal characteristics determine which canonical strategies enter the candidate set. | Multiple strategies may remain candidates. |
| 2. Constraint Gate | Hard constraint failures are passed into the strategy eligibility gate for each candidate. | A candidate with a hard-gate failure becomes ineligible. |
| 3. 8-Fit Evaluation | Every remaining candidate is evaluated against the same eight fits: Cash-flow, Liquidity, Debt, Asset Resource, Risk Capacity, Goal Constraint, Multi-goal Conflict, Implementation. | Each candidate gets Pass / Conditional / Fail. |
| 4. Remove Failed Candidates | Any candidate with an overall Fail is excluded from the recommendation pool. | Failed strategy is not selected. Other eligible candidates remain. |
| 5. Prefer Pass | If one or more candidates are Pass, only Pass candidates form the primary recommendation pool. | Conditional candidates are not preferred while a Pass exists. |
| 6. Consider Conditional | If there are no Pass candidates, Conditional candidates form the recommendation pool. | A Conditional strategy may be recommended with required changes. |
| 7. Rank | Candidates in the active pool are scored using Goal Fit, Horizon Fit, Funding Fit, Feasibility, Component Fit, and Technique Execution. | Highest-ranked eligible candidate wins. |
| 8. No Candidate | If every candidate is Fail, no strategy is recommended. | Decision returns infeasible and exposes eligibility failures / required changes. |

### Example: One Strategy Fails, Another Gets Selected

| Candidate Strategy | Hard Constraint / 8-Fit Result | Overall Status | Selection Outcome |
|---|---|---|---|
| Goal Funding | Cash-flow Fit = Fail | FAIL | Removed from recommendation pool |
| Progressive De-risking | All required fits Pass | PASS | Remains in primary pool |
| Capital Preservation | Liquidity Fit = Conditional | CONDITIONAL | Kept, but not preferred while a Pass exists |
| Debt Reduction | Goal Constraint Fit = Fail | FAIL | Removed from recommendation pool |
| Credit Utilisation | All required fits Pass | PASS | Remains in primary pool |
| Final Decision | Compare remaining Pass candidates by decision score | PASS pool exists | Highest-ranked Pass strategy is recommended |

**Important distinction:** a financial constraint and an 8-fit failure are not always the same thing. A constraint becomes decisive for strategy selection when it is converted into a hard strategy eligibility reason. Warnings and Conditional fits do not automatically eliminate a strategy.

## Constraint Decision Flow

| Goal / Planning Context | Financial Condition | Constraint Evaluation | Constraint Outcome | Strategy Impact |
|---|---|---|---|---|
| Defined Goal(s) | Income, expenses, surplus, assets, liabilities, EMI and liquidity evidence | Calculate financial ratios → evaluate goal validity → apply emergency reserve, debt burden and savings-rate policies | Hard constraints, warnings, ratio evidence and suggested priority overrides | Hard constraint failures make the affected strategy ineligible; warnings remain explanatory/planning evidence |
| Candidate Strategy | Defined Goal + financial context + constraint set | Apply strategy-specific goal constraints and any hard constraint messages | Eligible / Ineligible | Ineligible strategies are removed from the recommendation pool |
| Eligible Strategy | Same context | Run common 8-fit eligibility framework: Cash-flow, Liquidity, Debt, Asset Resource, Risk Capacity, Goal Constraint, Multi-goal Conflict, Implementation | Pass / Conditional / Fail | Pass preferred; Conditional considered only when no Pass exists |

## Constraint Data Ownership

| Data / Decision | Source of Truth | Role |
|---|---|---|
| Constraint Policy Thresholds | `backend/engines/constraints/policy.py` | Approved financial constraint thresholds and rule identifiers |
| Financial Ratio Calculation | `backend/engines/calculation/canonical.py` | Canonical ratio calculations consumed by constraint evaluation |
| Ratio Classification | `rules/moneywheel.py` + constraint policy thresholds | Healthy / attention / critical classification |
| Goal Validity Checks | `FinancialRatioConstraintEvaluator.evaluate_goal_constraints()` | Hard validation of positive horizon and positive target |
| Constraint Assessment | `FinancialRatioConstraintEvaluator.assess_constraints()` | Hard constraints, warnings, ratio evidence, suggested overrides |
| Strategy Constraint Gate | `evaluate_eligibility()` in `backend/engines/strategy/eligibility.py` | Converts hard constraint failures into strategy ineligibility reasons |
| 8-Fit Eligibility | `rules/eligibility.py` + `backend/engines/strategy/eligibility.py` | Common strategy eligibility framework |
| Final Strategy Recommendation | `backend/engines/strategy/decision.py` | Applies hard gates, Pass/Conditional precedence, scoring and ranking |

## Constraint vs Feasibility vs Eligibility

| Layer | Primary Question | Status / Output | Scope |
|---|---|---|---|
| Goal Feasibility | Can this defined goal's required funding fit current monthly capacity? | Feasible / Constrained / Infeasible / Unknown | Goal |
| Constraints | Are there financial or goal conditions that impose hard limits, warnings, or overrides? | Hard constraint / Warning / Evidence / Override | Financial plan and goals |
| Strategy Eligibility | Can this particular strategy be implemented for this goal under the available evidence and constraints? | Pass / Conditional / Fail | Strategy |
| Decision Ranking | Which eligible strategy is preferred? | Ranked eligible strategies | Candidate strategies |
