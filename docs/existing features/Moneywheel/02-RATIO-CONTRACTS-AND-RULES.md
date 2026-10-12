# Moneywheel — Ratio Contracts and Rules

**Baseline:** `d7640029310c8e58d4cdd9a033d7683b5ea10002`.

## Contract sources

- Inputs/results: `backend/models/moneywheel.py`
- Request schema: `backend/schemas/moneywheel.py`
- Formula/status rules: `backend/rules/moneywheel.py`
- Calculation orchestration: `backend/engines/moneywheel/engine.py`
- Canonical arithmetic: `backend/engines/calculation/canonical.py`

The model forbids extra fields and validates non-negative numeric inputs; goal duration must be positive. The result contract requires exactly nine ratios. Each ratio carries key, display name, nullable value, unit, status, formula, explanation and availability.

## Canonical ratio inventory

| Key | Meaning / formula described in rules |
|---|---|
| `savings_rate` | Monthly surplus ÷ gross monthly income × 100 |
| `liquid_asset_ratio` | Liquid assets ÷ total assets × 100 |
| `debt_to_income_ratio` | Monthly debt payments ÷ gross monthly income × 100 |
| `leverage_ratio` | Total liabilities ÷ total assets × 100 |
| `financial_asset_ratio` | Financial assets ÷ total assets × 100 |
| `insurance_coverage_ratio` | Existing sum assured ÷ required cover × 100 |
| `goal_funding_ratio` | Current goal funding ÷ goal target × 100 |
| `future_funding_ratio` | Projected goal funding ÷ future goal target × 100 |
| `required_rate_of_return` | Return required to grow current goal funding to the future target over duration |

Rule-set version is currently `2.0`. Statuses are `excellent`, `healthy`, `attention`, `critical`; unavailable inputs use `unavailable`. Exact threshold tuples and boundary comparisons are owned by `rules/moneywheel.py`, not by UI labels.

## Availability and interpretation

The engine rejects unknown ratio keys through canonicalization. Missing inputs, zero denominators, missing goal inputs, zero current goal funding for required-return calculation, or non-finite values produce unavailable outputs. The aggregate `overall_status` becomes `incomplete` when any ratio is unavailable; it is not a substitute for the individual ratio statuses.

The UI groups nine ratios into seven presentation dimensions: Cash Flow, Liquidity, Debt & Solvency, Investment Structure, Financial Protection, Goal Readiness and Required Return. These groupings are display taxonomy, not seven additional engine metrics.

## Cautions

Do not alter thresholds based on UI copy alone. Any formula or threshold change should be tested against canonical calculation functions, classification boundaries and historical snapshots' `rule_set_version`.
