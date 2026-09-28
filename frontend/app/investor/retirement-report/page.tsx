'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import StrategyWorkflowNav from '../../../components/StrategyWorkflowNav';
import InvestorHeader from '../../../components/InvestorHeader';
import {
  getRetirementReport,
  downloadRetirementReportPdf,
  getLatestStrategyRun,
  type RetirementReportData,
  type ReportSection,
} from '../../../lib/api/strategy';
import { getPlanningUnitId } from '../../../lib/api/client';
import { loadGoalPlannerData } from '../../../lib/onboarding/persistence';

function Value({ value }: { value: unknown }) {
  if (value === null || value === undefined || value === '') return <span className="text-gray-400">Not available</span>;
  if (Array.isArray(value)) {
    return (
      <ul className="list-disc pl-5 space-y-1">
        {value.map((v, i) => (
          <li key={i}>
            <Value value={v} />
          </li>
        ))}
      </ul>
    );
  }
  if (typeof value === 'object') {
    return (
      <div className="space-y-1">
        {Object.entries(value as Record<string, unknown>).map(([k, v]) => (
          <div key={k}>
            <span className="font-semibold text-slate-700">{k.replaceAll('_', ' ')}:</span> <Value value={v} />
          </div>
        ))}
      </div>
    );
  }
  return <span>{String(value)}</span>;
}

function Section({ section }: { section: ReportSection }) {
  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <h2 className="mb-2 text-xl font-extrabold text-navy-900">{section.title}</h2>
      {section.description && <p className="mb-4 text-sm text-slate-500">{section.description}</p>}
      {section.columns && section.rows ? (
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead>
              <tr className="border-b bg-slate-50">
                {section.columns.map((column, i) => (
                  <th key={i} className="px-3.5 py-2.5 font-bold text-slate-700">
                    {column}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {section.rows.map((row, i) => (
                <tr key={i} className="border-b border-slate-100 last:border-0 hover:bg-slate-50/50">
                  {row.map((cell, j) => (
                    <td key={j} className="px-3.5 py-2.5 align-top text-slate-600">
                      <Value value={cell} />
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <Value value={section.data} />
      )}
      {section.narratives && (
        <div className="mt-5 space-y-4 border-t border-slate-100 pt-4">
          {Object.entries(section.narratives).map(([label, value]) => (
            <div key={label} className="rounded-2xl bg-slate-50 p-4">
              <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400">{label}</h3>
              <div className="mt-1.5 text-sm leading-6 text-slate-700">
                <Value value={value} />
              </div>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}

export default function RetirementReportPage() {
  const [report, setReport] = useState<RetirementReportData | null>(null);
  const [error, setError] = useState('');
  const [runId, setRunId] = useState('');
  const [planningUnitId, setPlanningUnitId] = useState('');
  const [downloading, setDownloading] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let active = true;

    async function loadReport() {
      try {
        setLoading(true);
        setError('');

        const params = new URLSearchParams(window.location.search);
        let currentRunId = params.get('run_id') || '';
        const currentPlanningUnitId = params.get('planning_unit_id') || getPlanningUnitId() || '';

        if (!currentPlanningUnitId) {
          throw new Error('Planning unit is not available. Please complete onboarding first.');
        }

        // If run_id is not directly in the query parameters, discover it from the investor's latest retirement goal
        if (!currentRunId) {
          const goalData = await loadGoalPlannerData();
          const goals = goalData?.goals ?? [];
          if (!goals.length) {
            throw new Error('No goals found. Please define a retirement goal in Goal Planner first.');
          }

          // Prefer retirement goal, else first available goal
          const targetGoal =
            goals.find(
              (g) =>
                g.name?.toLowerCase().includes('retirement') ||
                (g as { type?: string }).type?.toLowerCase().includes('retirement')
            ) || goals[0];

          const latestRun = await getLatestStrategyRun(currentPlanningUnitId, targetGoal.id);
          if (!latestRun?.strategy_run_id) {
            throw new Error(
              `No Strategy Run found for "${targetGoal.name || 'Retirement'}". Please build and select a strategy in Strategy Builder first.`
            );
          }
          currentRunId = latestRun.strategy_run_id;
        }

        if (!active) return;
        setRunId(currentRunId);
        setPlanningUnitId(currentPlanningUnitId);

        const data = await getRetirementReport(currentPlanningUnitId, currentRunId);
        if (active) {
          setReport(data);
        }
      } catch (err) {
        if (active) {
          setError(err instanceof Error ? err.message : 'Unable to load retirement report.');
        }
      } finally {
        if (active) setLoading(false);
      }
    }

    void loadReport();

    return () => {
      active = false;
    };
  }, []);

  const downloadPdf = async () => {
    if (!runId || !planningUnitId || downloading) return;
    setDownloading(true);
    setError('');
    try {
      const blob = await downloadRetirementReportPdf(planningUnitId, runId);
      const url = URL.createObjectURL(blob);
      const anchor = document.createElement('a');
      anchor.href = url;
      anchor.download = `retirement-planning-report-${runId}.pdf`;
      document.body.appendChild(anchor);
      anchor.click();
      anchor.remove();
      URL.revokeObjectURL(url);
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Unable to generate PDF.');
    } finally {
      setDownloading(false);
    }
  };

  return (
    <main className="min-h-screen bg-[#f6f8fb] pb-16 text-slate-900">
      <InvestorHeader
        eyebrow="Planvesto Report"
        title={report?.title ?? 'Retirement Planning Report'}
        description="Comprehensive report generated from the persisted Strategy Run and recommendation architecture."
      >
        {report && (
          <button
            type="button"
            onClick={downloadPdf}
            disabled={downloading}
            className="inline-flex items-center justify-center gap-2 rounded-xl bg-navy-900 px-4 py-2.5 text-xs font-bold text-white shadow-sm transition hover:bg-navy-800 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {downloading ? (
              <>
                <svg className="h-3.5 w-3.5 animate-spin text-white" viewBox="0 0 24 24" fill="none">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  />
                </svg>
                <span>Generating PDF…</span>
              </>
            ) : (
              <>
                <svg className="h-3.5 w-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                  <polyline points="7 10 12 15 17 10" />
                  <line x1="12" y1="15" x2="12" y2="3" />
                </svg>
                <span>Download PDF</span>
              </>
            )}
          </button>
        )}
      </InvestorHeader>
      <div className="mx-auto max-w-6xl space-y-6 p-4 sm:p-6 lg:p-10">
        <StrategyWorkflowNav />

        {error && (
          <div className="rounded-2xl border border-red-200 bg-red-50 p-5 text-sm text-red-700 shadow-sm">
            <p className="font-bold">{error}</p>
            <div className="mt-3 flex gap-3">
              <Link
                href="/investor/strategy-builder"
                className="inline-flex rounded-xl bg-navy-900 px-4 py-2 text-xs font-bold text-white hover:bg-navy-800"
              >
                Go to Strategy Builder →
              </Link>
              <Link
                href="/investor/goal-planner"
                className="inline-flex rounded-xl border border-slate-300 bg-white px-4 py-2 text-xs font-bold text-slate-700 hover:bg-slate-50"
              >
                Go to Goal Planner
              </Link>
            </div>
          </div>
        )}

        {loading && (
          <div className="space-y-4 py-12 text-center">
            <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-navy-900 border-t-transparent" />
            <p className="text-sm font-semibold text-slate-500">Loading retirement report…</p>
          </div>
        )}

        {!loading && report && (
          <div className="space-y-6">
            {report.sections.map((section) => (
              <Section key={section.id} section={section} />
            ))}
          </div>
        )}
      </div>
    </main>
  );
}
