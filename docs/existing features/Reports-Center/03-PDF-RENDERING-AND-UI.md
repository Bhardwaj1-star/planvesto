# Reports Center — PDF Rendering and UI Behavior

**Baseline:** `d7640029310c8e58d4cdd9a033d7683b5ea10002`.

## Rendering

The shared PDF renderer lives in `backend/report_engine/renderer.py`, with common configurations/models in `configs.py` and `models.py`. Goal, basket and summary services may compose report sections, while `CommonPdfRenderer` centralizes shared layout primitives. `SummaryReportRenderer` builds sections for financial snapshot, goal portfolio, observations, recommended actions and risk profile when data exists.

## Download flow

The reports page delegates PDF downloads to API helpers in `frontend/lib/api/strategy.ts`. It tracks loading/working and error state; verify that each action resets state after both success and failure. UI selection includes goal, basket and report type; selected strategy versions are fetched per goal.

## UI/data mismatches to verify

- The reports page may describe sections such as trade-offs or health scans; verify those sections exist in the response/PDF for the selected report.
- Goal Basket UI selection is stored in localStorage; this is not the same as a server-persisted basket.
- Browser PDF output, filename/content-type, empty-state behavior and JSON/PDF parity are runtime properties not proven by source inspection alone.
- Missing fields should remain visibly unavailable instead of being silently fabricated by report formatting fallbacks.
