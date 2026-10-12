# Dashboard — Financial Metrics and Goal Summaries

**Baseline:** `d7640029310c8e58d4cdd9a033d7683b5ea10002`.

## Financial State subset

`DashboardService` exposes net worth; total assets and asset breakdown/allocation; total liabilities and liability breakdown/allocation; monthly/annual income and expenses; and monthly/annual investable surplus. The source of these values is the Financial State service/engine, not independent dashboard formulas.

Availability and missing-value semantics are inherited from Financial State. The dashboard's use of `.get()` preserves absent values as null/omitted values in the assembled dictionary; it does not justify treating missing as zero.

## Goal-card derivations

When a latest DefinedGoal is available, the service converts target and projected mapped value to floats and computes:

`coverage = clamp(projected_mapped_asset_value / future_target * 100, 0, 100)`

If target is not positive, coverage is set to zero. The displayed value is rounded to one decimal place. The card includes the defined goal's funding status and funding gap. Image key is selected by keyword matching on goal type (home/property, education/college, travel/vacation, retirement, wedding/marriage, business; otherwise default). This is presentation mapping, not goal classification authority.

For a summary row without a defined snapshot, target amount falls back to the summary row and target date/priority/flexibility are carried through where present; funding status, funding gap, projected value and coverage are null.

## Important semantics

- Coverage percentage is a capped display ratio, not a probability of success.
- A cancelled goal is omitted from active dashboard cards but remains a history concern.
- A fallback goal card does not prove feasibility has been calculated.
- Dashboard goal count is not a replacement for Goal Planner's lifecycle or multi-goal feasibility.
