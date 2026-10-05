# Portfolio & Asset Mapping Architecture

**Status:** CANONICAL  
**Scope:** Mapping existing assets to goals and projecting their contribution toward future funding.

## Boundary

Asset mapping is a Goal Planning responsibility. It answers:

**Which existing resources are assigned to this goal, and what will those resources contribute at the goal date?**

It does not select investment products.

## Flow

**Existing Assets → Goal Mapping → Allocated Amount/Percentage → Projection → Future Funding Resources → Funding Gap**

## Goal Ownership

The Goal Planner:
- maps assets to a defined goal;
- records allocated amount/percentage;
- projects mapped asset value;
- combines projected mapped resources with future contributions;
- passes the resulting funding gap to Strategy.

## Strategy Boundary

Strategy consumes:
- future target
- projected mapped asset value
- funding gap
- duration
- available surplus

Strategy decides the funding architecture; it does not redefine the asset mapping calculation.

## Product Boundary

Asset mapping is not Product Selection. A mapped existing asset represents a planning resource. Product Selection is a downstream investment implementation concern.

## Related Code

- `backend/engines/goal/asset_projection.py`
- `backend/engines/goal/engine.py`
- `backend/engines/goal/funding_gap.py`
- `backend/models/defined_goal.py`
- `backend/services/goal_service.py`

## Decision Flow

**Asset Mapping → Projection → Funding Gap → Goal Feasibility → Strategy Applicability/Eligibility → Strategy Decision**

## Data Ownership

| Data | Owner |
|---|---|
| Existing asset data | Financial/portfolio data source |
| Goal-to-asset mapping | Goal Planner |
| Projected mapped value | Goal Asset Projection |
| Future target | Goal Target Calculation |
| Funding gap | Goal Funding Gap |
| Funding solution | Strategy/Goal Funding |

