# Goal Planner — Asset Mapping and Funding Projections

**Source revision:** `5a3b060e1b27915ede226f5173364e23dca1263e`

## 1. Mapping semantics implemented in code

Request model: [backend/schemas/goals.py](`https://github.com/Bhardwaj1-star/planvesto/blob/5a3b060e1b27915ede226f5173364e23dca1263e/backend/schemas/goals.py#L9-L21`).  
Calculation: [backend/engines/goal/engine.py](`https://github.com/Bhardwaj1-star/planvesto/blob/5a3b060e1b27915ede226f5173364e23dca1263e/backend/engines/goal/engine.py#L45-L91`).  
Projection functions: [backend/engines/goal/asset_projection.py](`https://github.com/Bhardwaj1-star/planvesto/blob/5a3b060e1b27915ede226f5173364e23dca1263e/backend/engines/goal/asset_projection.py#L1-L74`).

Each request mapping identifies an existing asset and supplies:
- allocation type: currency or percentage;
- allocation value;
- optional expected annual return assumption;
- return compounding frequency.

The engine requires the asset ID to exist in the planning-unit asset lookup and requires the asset to have an asset name; otherwise it raises ValueError (GoalEngine lines 48–55).

## 2. Default expected-return lookup

`DEFAULT_ASSET_RETURNS` in `asset_projection.py:4-20` uses substring matching against lowercased asset names:

| Matched key | Annual return assumption |
|---|---:|
| bank, cash | 4% |
| fixed deposit, fd | 7% |
| mutual fund, stock, equity | 12% |
| bond, debt | 7% |
| epf, ppf, provident | 8% |
| nps | 9% |
| gold | 8% |
| real estate, property | 9% |

Fallback is 8% (`DEFAULT_RETURN_FALLBACK`, line 22). If request `expected_return` is provided, GoalEngine uses it instead of the asset-name default.

These are code defaults, not guaranteed returns and not a statement of live portfolio assumptions.

## 3. Allocation and projection formula

`calculate_asset_projection`, lines 46–74, returns allocated amount, allocated percentage and projected value.

- Current asset value and allocation input are clamped to non-negative values.
- Percentage allocation is capped at 100% in the calculation; the request validator also rejects values above 100%.
- Currency allocation is capped at current asset value.
- If duration or allocated amount is non-positive, projected value equals allocated amount.
- Otherwise, compounding frequency maps monthly→12, quarterly→4, semi-annual variants→2, and everything else→annual (1).
- Projection: `allocated_amount × (1 + expected_return / n) ** (n × duration_years)`.

## 4. Aggregate mapped assets and funding return

GoalEngine adds every mapping's projected value to `projected_mapped_asset_value`.

`calculate_funding_return_assumption` in [funding_gap.py lines 67–90](`https://github.com/Bhardwaj1-star/planvesto/blob/5a3b060e1b27915ede226f5173364e23dca1263e/backend/engines/goal/funding_gap.py#L67-L90`) computes a weighted return based on allocated current amount:
`sum(allocated_amount × normalized_expected_return) / sum(allocated_amount)`.
If there are no mappings or their total allocated amount is non-positive, it uses `DEFAULT_FUNDING_RETURN_ASSUMPTION` from `rules.assumptions`.

## 5. Funding gap and required monthly contribution

Source: [backend/engines/goal/funding_gap.py](`https://github.com/Bhardwaj1-star/planvesto/blob/5a3b060e1b27915ede226f5173364e23dca1263e/backend/engines/goal/funding_gap.py#L9-L65`).

- Funding gap delegates to `calculate_goal_funding_gap` in `engines.calculation.canonical`.
- A gap whose absolute value is below 0.01 is normalized to zero and status `On Track`.
- Positive gap → `Shortfall`; negative gap → `Overfunded`.
- Required contribution is zero for non-positive gap or non-positive duration.
- For positive gap and duration, months are `max(1, round(years × 12))`; monthly rate is annual return divided by 12. The function computes the end-of-month contribution needed to reach the gap, and rejects annual returns ≤ -100%.

## 6. Additional funding-path evaluations

Source: [backend/engines/goal/funding_strategies.py](`https://github.com/Bhardwaj1-star/planvesto/blob/5a3b060e1b27915ede226f5173364e23dca1263e/backend/engines/goal/funding_strategies.py#L1-L198`).

The engine resolves each displayed funding path through canonical strategy-variant definitions via `_variant` (lines 8–20). It evaluates these IDs:
- `existing_assets` when the gap is non-positive;
- `lumpsum` alone when target duration is immediate;
- otherwise `sip`, `lumpsum`, `lumpsum_plus_sip`, `lumpsum_plus_step_up_sip`, `step_up_sip`.

Path outputs include status, required lump sum, required monthly contribution, starting monthly contribution, annual step-up, remaining gap, reason, constraints, description and trade-offs where populated by the code.

Notable actual implementation details:
- SIP fit compares required SIP with available surplus plus 0.01.
- Lump sum is discounted by `(1 + annual_return) ** years`.
- The mixed lump-sum + SIP path uses all available monthly surplus for its recurring leg and discounts residual gap into upfront capital.
- Step-up solving uses binary search for up to 60 iterations with a maximum annual step-up of 100%.
- Existing mapped assets are already reflected in the gap; these paths calculate additional funding from that point forward.

These are Goal Feasibility funding evaluations. Their presence does not by itself prove that a Strategy Builder strategy has been selected or that an investor accepted a path.
