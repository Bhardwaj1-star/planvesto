## Goal Planner Architecture

The Goal Planner converts user-defined goal inputs and mapped assets into a canonical `DefinedGoal`, calculates the target-date funding requirement, evaluates funding feasibility against current financial capacity, and exposes the resulting goal state to downstream strategy decisioning.

| Goal Planner Stage | Input / Data | Logic / Rule | Output | Downstream Use |
|---|---|---|---|---|
| Goal Input | Goal type; goal name; today's cost; target month/year; priority; flexibility; status; asset mappings; inflation rate; dynamic details | Validate ownership and request data; canonicalize goal type and name | Validated Goal Input | Goal calculation |
| Goal Normalisation | Raw goal type/name | `canonical_goal_type()` and `canonical_goal_name()` | Canonical goal type and name | DefinedGoal creation; strategy applicability |
| Goal Timeline | Target month/year; reference date | Calculate duration in years | `duration_years` | Future target; applicability characteristics |
| Future Target | Today's cost; inflation rate; duration; goal type; dynamic details | Generic inflation projection; retirement uses retirement-corpus calculation; specialised goal calculations where applicable | `future_target` | Funding-gap calculation |
| Asset Mapping & Projection | Planning-unit assets; allocation type/value; expected return; return frequency; duration | Project mapped asset value to target date | `mapped_assets`; `projected_mapped_asset_value` | Funding gap |
| Funding Gap | Future target; projected mapped asset value | `future_target - projected_mapped_asset_value` | `funding_gap`; Shortfall / On Track / Overfunded | Strategy applicability; funding calculations |
| Required Contribution | Funding gap; funding return assumption; duration | Calculate required monthly contribution for positive gap | `required_monthly_contribution` | Feasibility |
| Financial Capacity | Current Financial State snapshot | Read current `investable_surplus_monthly` | Available monthly surplus | Feasibility |
| Goal Feasibility | Required monthly contribution; available monthly surplus; funding gap | Compare required contribution with available surplus | Feasible / Constrained / Infeasible / Unknown | Workflow readiness; strategy decisioning |
| Funding Strategies | Funding gap; return assumption; duration; available surplus | Build goal-funding implementation scenarios | `funding_strategies` | Goal planning / strategy implementation |
| Defined Goal | All calculated and user-defined goal fields | Persist versioned canonical goal snapshot | `DefinedGoal` | Applicability, eligibility, strategy builder, reports |

## Goal Planner Decision Flow

| Goal | Goal Definition | Target & Funding Calculation | Funding Status | Feasibility | Strategy Handoff |
|---|---|---|---|---|---|
| Defined Goal | Canonical Goal Type + Goal Name + Cost + Target Date + Priority + Flexibility + Status + Mapped Assets | Calculate Duration → Future Target → Mapped Asset Projection → Funding Gap → Required Monthly Contribution | **Shortfall** when funding gap > 0; **On Track** when gap ≈ 0; **Overfunded** when gap < 0 | Compare Required Monthly Contribution with current Investable Monthly Surplus. Return **Feasible**, **Constrained**, **Infeasible**, or **Unknown** when financial-state evidence is unavailable. | Pass the resulting `DefinedGoal` state to Strategy Decisioning, where strategy-specific Applicability is evaluated and the common 8-Fit Eligibility framework is applied. |

## Goal Planner Data Ownership

| Data / Decision | Source of Truth | Role |
|---|---|---|
| Canonical Goal Types | `rules/goals.py` | Goal taxonomy and normalization |
| Goal Definition | `GoalInput` / persisted goal records | User-defined source data |
| Defined Goal | `DefinedGoal` | Canonical calculated goal state |
| Goal Calculations | `backend/engines/goal/` | Target, projection, funding-gap and contribution calculations |
| Financial Capacity | Current Financial State snapshot | Available monthly surplus for feasibility |
| Funding Status | Goal funding-gap calculation | Shortfall / On Track / Overfunded signal |
| Feasibility Status | `GoalService._apply_feasibility()` | Goal-level funding feasibility; not a strategy decision |
| Strategy Applicability | Strategy Library + `StrategyRuleEngine` | Downstream strategy candidate selection |

## Asset Mapping vs Asset Earmarking — Canonical Boundary

These are related but **not the same function**.

**Asset Mapping** is a Goal Planner responsibility. It records the investor's intended relationship between an existing asset/resource and a goal and supplies that relationship to goal funding calculations.

**Asset Earmarking** is a Strategy/Technique responsibility. It evaluates whether the mapped asset should actually be reserved for that goal within the selected funding strategy and variant, considering the goal requirement, time horizon, liquidity, risk, competing goals, constraints, and implementation implications.

### Canonical handoff

**Investor Asset Mapping → Goal Planner Projection → Funding Gap / Feasibility → Strategy + Variant Selection → Asset Earmarking → Method / Policy → Solution / Implementation**

Therefore:
- Mapping does **not** certify that an asset is strategically suitable.
- Earmarking does **not** recreate the Goal Planner's mapping or projection calculation.
- Earmarking may **confirm, modify, partially accept, or reject** the mapped relationship.
- The final earmarked allocation is a strategy decision and must remain traceable to the original investor mapping.

### Example

If an investor maps an existing mutual-fund holding to the Education goal, the Goal Planner treats that holding as a mapped planning resource and projects its contribution. Later, Strategy Builder may determine that the full holding should not be earmarked for Education because of liquidity, risk, competing goals, or other constraints. The Strategy layer can therefore recommend partial earmarking, a different asset, or no earmarking.

This boundary prevents **Asset Mapping** and **Asset Earmarking** from becoming duplicate concepts or duplicate calculations.

