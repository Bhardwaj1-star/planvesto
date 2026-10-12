# History — UI Selection and Navigation

**Baseline:** `d7640029310c8e58d4cdd9a033d7683b5ea10002`.

## Goal History selection

The goal-history page maintains a selected goal and uses it to load versions. Verify what happens when the requested goal is missing, the goal list is empty, or a user changes selection while a request is pending.

## Strategy History selection

The strategy-history page reads `goalId` from `window.location.search`; if it matches a loaded goal it is selected, otherwise the first goal is selected. It requests run history and selected version in parallel, then requests version history for the selected strategy. Effects use an active flag to avoid setting state after unmount or stale requests. If no selected goal exists, run/version state is cleared.

## Interpretation cautions

A history page is a reader, not a lifecycle authority. Display order and labels should come from API/model contracts. “Latest” means latest according to the owning query's ordering—not necessarily accepted, active, approved or best. Navigation to a version/run should preserve identifiers without implying that opening a historical record changes current state.

## Verification gaps

Check deep links, invalid `goalId`, empty goal lists, API failures, loading state, latest ordering, duplicate timestamps, selection races, version-to-run lineage and whether a true cross-feature chronological timeline exists. The current evidence shows feature-specific history surfaces, not a confirmed unified history engine.
