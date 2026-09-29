# Planvesto — Strategy System Business Rules & Correction Spec

## Purpose
This document records the business-rule corrections identified from the current `feature/multi-goal-backend-v2` implementation. It is the reference for the next backend correction pass. No code or schema change is implied until the rules are locked.

## 1. Canonical Goal Taxonomy

The frontend currently defines 11 canonical goal types:

- Retirement / Financial Freedom
- Passive Income
- Education
- Marriage
- Dream Home
- Vehicle
- Vacation
- Wealth Creation
- Debt Repayment
- Philanthropy
- Others

The backend strategy catalog currently uses older labels such as `Child Education`, `Child Marriage`, `Home Purchase`, `Travel`, and `Business`. This taxonomy mismatch must be corrected.

### Rule
The frontend goal taxonomy is the canonical goal taxonomy. Backend strategy applicability must reference canonical goal concepts, not legacy labels.

## 2. Goal-Type Mapping

Canonical semantic mappings:

- Retirement / Financial Freedom → retirement
- Education → education
- Marriage → marriage
- Dream Home → home
- Vehicle → vehicle
- Vacation → vacation
- Wealth Creation → wealth_creation
- Debt Repayment → debt_repayment
- Philanthropy → philanthropy
- Passive Income → passive_income
- Others → other

The mapping should preserve the user's actual goal type. `Passive Income`, `Debt Repayment`, and `Philanthropy` must not be silently collapsed into `Others`.

## 3. Goal Type vs Strategy Eligibility

Goal type identifies the nature of the goal and is used to determine which strategies are relevant candidates.

Goal type alone does not establish investor-strategy fit.

Intended flow:

`Defined Goal → Candidate Strategies → Eligibility Fits → Strategy Decision`

Goal characteristics such as funding status, duration, priority and flexibility provide context for the candidate/fit evaluation.

## 4. Strategy Eligibility Architecture

The Eligibility Engine is the authoritative layer for investor-strategy fit.

The current eight fit dimensions are:

- cashflow_fit
- liquidity_fit
- debt_fit
- asset_resource_fit
- risk_capacity_fit
- goal_constraint_fit
- multi_goal_conflict_fit
- implementation_fit

Each fit evaluates whether the strategy can realistically be applied to this investor and this goal.

## 5. Rule Engine Boundary

The existing Rule Engine contains goal diagnostics and hard/soft constraints. It must not become a second strategy-eligibility engine.

Rule Engine responsibility:
- validate fundamental goal integrity;
- expose diagnostics and hard constraints;
- provide explanatory evidence to downstream decision logic.

Eligibility Engine responsibility:
- determine strategy-level applicability/fit across the eight fit dimensions.

Strategy Library responsibility:
- define reusable strategy architectures, mechanisms, required inputs, applicable goal concepts, techniques and implementation parameters.

## 6. Required Strategy Flow

1. Read an already-defined goal.
2. Validate fundamental goal integrity.
3. Load candidate strategies from the Strategy Library.
4. Evaluate strategy/goal compatibility.
5. Run the eight Eligibility Fits against investor + goal + strategy.
6. Classify strategies as eligible, conditional, or failed according to locked eligibility rules.
7. Pass eligible/conditional strategies into strategy architecture/scenario generation.
8. Produce the final decision/recommendation layer.

The system must not prematurely discard a strategy solely because the current catalog uses a legacy goal label.

## 7. Legacy Strategy Catalog Correction

Replace legacy goal labels in strategy applicability metadata:

- Child Education
- Child Marriage
- Home Purchase
- Travel
- Business
- Emergency Fund, unless and until explicitly added to the canonical frontend goal taxonomy

Do not invent new frontend goal types during this correction.

## 8. Strategy-Level Issues Already Identified

The current catalog contains conceptual mappings requiring later business-rule review:

- Progressive De-risking needs an explicit relationship to goal time-to-target and funding characteristics.
- Capital Preservation overlaps with Progressive De-risking and needs a precise strategy-vs-technique boundary.
- Goal Funding and Long-Term Accumulation overlap and need explicit architecture definitions.
- Goal Reprioritisation & Resource Allocation is an investor-level orchestration function and may need to be treated differently from a normal single-goal strategy.

These are not to be resolved by coding assumptions; they require business-rule decisions.

## 9. Do Not Change Yet

Until remaining business rules are explicitly locked, do not finalize:

- strategy ranking weights;
- aggregation formula across the eight fits;
- exact meaning of CONDITIONAL vs FAIL;
- whether Goal Reprioritisation is a strategy or orchestration layer;
- additional strategies;
- product-level implementation rules.

## 10. Correction Order

1. Canonicalize goal taxonomy.
2. Remove legacy goal labels from strategy applicability.
3. Separate goal-type/goal-characteristic matching from the eight investor-strategy eligibility fits.
4. Keep Rule Engine and Eligibility Engine responsibilities separate.
5. Lock remaining strategy business rules.
6. Modify backend code and tests.
