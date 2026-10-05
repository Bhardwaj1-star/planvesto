# Product Selection Architecture

**Status:** FOUNDATION / NOT FULLY IMPLEMENTED  
**Scope:** Downstream investment implementation after risk boundary and allocation policy.

## Intended Hierarchy

**Risk Profile → Strategic Asset Allocation → Sub-Asset Allocation → Product Category → Product Selection → Allocation Amount**

This hierarchy is explicitly represented by the Investment Engine.

## Risk Boundary

Investment planning receives:
- Risk Required
- Risk Capacity
- Risk Tolerance
- constraints
- current portfolio allocation

Investment planning must operate within the approved risk boundary.

## Current Engine

`backend/engines/investment/engine.py` currently builds an InvestmentPlan structure with layers:
- strategic_asset_allocation
- sub_asset_allocation
- product_category
- product_selection
- allocation_amount

When all risk dimensions are available, the engine records that the risk boundary has been received. Explicit allocation/product-selection business rules are still pending.

## Product Selection Boundary

Product Selection is downstream of:
1. Goal requirements
2. Strategy architecture
3. Risk boundary
4. Allocation policy
5. Product-category decision

It must not override Strategy Decision or Risk Profiler constraints.

## Current Status

The repository has the architectural foundation but does **not** yet provide a canonical product-selection algorithm. Therefore this document records the intended boundary and current implementation state rather than inventing selection rules.

## Related Code

- `backend/engines/investment/engine.py`
- `backend/engines/investment/models.py`
- `backend/engines/risk_profiler/engine.py`
- `docs/architecture/RISK-PROFILER-INVESTMENT-ENGINE-FOUNDATION.md`
- `docs/product/MONEYWHEEL-CONSTRAINTS.md`
