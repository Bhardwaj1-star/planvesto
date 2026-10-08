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

## Canonical Boundary: Asset Mapping vs Asset Earmarking

### Asset Mapping

**Owner:** Goal Planner

Asset Mapping answers:

> **Which existing assets does the investor intend to associate with this goal?**

It records the investor's stated goal-to-asset relationship and provides the planning resource used in future-value projection and funding-gap calculation.

Asset Mapping is therefore **intent/input + planning calculation**. It is not a recommendation that the asset is the correct strategic allocation.

### Asset Earmarking

**Owner:** Strategy Builder / Strategy Technique layer

Asset Earmarking answers:

> **Given the selected strategy and variant, which assets should actually be reserved for this goal, and to what extent?**

It evaluates the mapped assets against:
- goal funding requirement;
- time horizon;
- liquidity requirement;
- risk characteristics;
- existing allocation;
- competing goals;
- constraints;
- implementation feasibility.

Its output can be:
- **Confirm** the mapped asset;
- **Partially earmark** it;
- **Change/reallocate** the earmarked asset;
- **Reject** the mapping for strategic use;
- or identify that additional funding is required.

### Canonical Relationship

**Asset Mapping → Projection → Funding Gap → Feasibility → Strategy/Variant → Asset Earmarking → Method/Policy → Solution/Implementation**

The Strategy layer must consume the Goal Planner's mapping evidence rather than recreate it. Asset Earmarking must not duplicate the Goal Planner's asset-projection or funding-gap calculation.

### Why both concepts exist

The investor may reasonably say:

> "I want to use this existing asset for my Education goal."

That is **Mapping**.

The decision engine then asks:

> "Is this actually appropriate to reserve for Education under the selected strategy, and should all or only part of it be earmarked?"

That is **Earmarking**.

This distinction is canonical and should be preserved across frontend, backend, decision-tree documentation, strategy rules, and implementation.

