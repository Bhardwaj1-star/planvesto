# History — APIs, Repositories and Lifecycle Meaning

**Baseline:** `d7640029310c8e58d4cdd9a033d7683b5ea10002`.

## API/repository boundary

Each history family uses its owning feature's API and repository. Goal versions and strategy versions are not interchangeable. Financial State history is snapshot history; Moneywheel history is diagnostic calculation history; Action Plan decision history records changes/decisions about actions; diary decisions are a historical narrative/evidence surface.

Ordering and retention are family-specific. For example, diary repository orders entries and decisions by date then created time descending; Moneywheel orders snapshots by calculated time; Action Plan repository maintains current action rows and decision-history rows. Do not assume all families share the same pagination, tie-breaking or retention rules.

## Lifecycle distinctions

The following events must remain distinct unless an explicit persisted field/transition connects them:

- calculation run;
- What-If scenario;
- recommendation;
- selected strategy/version;
- investor-accepted plan/approval snapshot;
- action generated/planned;
- action confirmed;
- action completed/cancelled;
- updated Financial State snapshot.

A strategy version existing does not prove investor adoption. A decision record does not automatically imply that a new accepted plan exists. A completed action is execution evidence and does not itself prove that all downstream recalculation/reporting completed.

## Security

Each API must authenticate and enforce the correct ownership checks. Authorization behavior should be inspected per endpoint; this index does not assert a shared history authorization layer or production RLS state.
