# Behavioral Profile Rules

## Purpose

Behavioral Profile describes observed investor behavior for product-selection and implementation compatibility. It does not select a financial strategy and does not infer personality from hypothetical questionnaire answers.

## Dimensions

- `decision_consistency`: consistency between stated/recorded plans and historical actions.
- `volatility_reaction`: actual actions taken during observed market volatility.
- `discipline`: historical consistency of contributions and agreed financial actions.
- `intervention_tendency`: frequency and pattern of discretionary portfolio/product changes.
- `loss_uncertainty_response`: observed response to losses, drawdowns, ambiguity, or incomplete information.

## Evidence rules

1. Evidence must be historical/observable; hypothetical answers are not evidence.
2. Every observed constraint requires at least one evidence item.
3. Unsupported dimensions remain `insufficient_evidence`.
4. Conflicting observations remain unresolved; the engine does not average them into a personality score.
5. Behavioral constraints are `soft` by default and remain separate from financial hard constraints.
6. `downstream_use` is `product_selection`; Strategy Builder must not consume behavioral profile as a strategy-selection score.
7. Confidence is evidence-driven and uses the existing Profile Engine confidence rules; it is not a personality score.
