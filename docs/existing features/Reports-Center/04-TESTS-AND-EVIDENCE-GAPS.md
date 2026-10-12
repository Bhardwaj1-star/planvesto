# Reports Center — Tests and Evidence Gaps

**Baseline:** `d7640029310c8e58d4cdd9a033d7683b5ea10002`. Report tests were located but not run.

## Test files located

- `backend/tests/test_goal_report_service.py`
- `backend/tests/test_goal_report_funding.py`
- `backend/tests/test_goal_report_pdf_structure.py`
- `backend/tests/test_basket_report_service.py`
- `backend/tests/test_basket_report_api.py`
- `backend/tests/test_summary_report_api.py`
- `backend/tests/test_retirement_report_pdf.py`

## Verification checklist

1. Strategy-run and exact DefinedGoal-version lineage for individual reports.
2. Basket goal-ID validation, minimum/maximum count and cross-goal ownership.
3. Complete-plan outputs reconcile with Goal Planner/Multi-Goal service.
4. Summary outputs consume canonical Financial State, Moneywheel and risk-profiler results.
5. Report fallbacks do not misrepresent missing values as verified values.
6. PDF generation, content type, filename, empty data and exception handling.
7. JSON/PDF parity and report UI descriptions vs actual sections.
8. Source snapshot/run freshness and provenance.
9. LocalStorage basket handling and missing selected Strategy Version.
10. Production database/security and end-to-end browser tests.

## Evidence boundary

Tests listed above exist in the repository but were not executed. The source pass does not establish deployed report content, production data freshness or passing output structure. These are verification questions, not confirmed defects.
