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
