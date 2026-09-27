'use client';

import { useEffect, useState } from 'react';

interface ReportSection { id: string; title: string; data: unknown }
interface Report { title: string; sections: ReportSection[] }

function Value({ value }: { value: unknown }) {
  if (value === null || value === undefined || value === '') return <span>—</span>;
  if (Array.isArray(value)) return <ul className="list-disc pl-5 space-y-1">{value.map((v, i) => <li key={i}><Value value={v} /></li>)}</ul>;
  if (typeof value === 'object') return <div className="space-y-2">{Object.entries(value as Record<string, unknown>).map(([k, v]) => <div key={k}><span className="font-medium">{k.replaceAll('_', ' ')}:</span> <Value value={v} /></div>)}</div>;
  return <span>{String(value)}</span>;
}

export default function RetirementReportPage() {
  const [report, setReport] = useState<Report | null>(null);
  const [error, setError] = useState('');
  const [runId, setRunId] = useState('');
  const [planningUnitId, setPlanningUnitId] = useState('');

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const currentRunId = params.get('run_id') || '';
    const currentPlanningUnitId = params.get('planning_unit_id') || '';
    setRunId(currentRunId);
    setPlanningUnitId(currentPlanningUnitId);
    if (!currentRunId || !currentPlanningUnitId) { setError('A strategy run and planning unit are required.'); return; }
    fetch(`/api/strategy/runs/${encodeURIComponent(currentRunId)}/retirement-report?planning_unit_id=${encodeURIComponent(currentPlanningUnitId)}`)
      .then(async r => { if (!r.ok) throw new Error(await r.text()); return r.json(); })
      .then(setReport)
      .catch(e => setError(e.message || 'Unable to load report.'));
  }, []);

  const downloadPdf = async () => {
    const response = await fetch(`/api/strategy/runs/${encodeURIComponent(runId)}/retirement-report.pdf?planning_unit_id=${encodeURIComponent(planningUnitId)}`);
    if (!response.ok) { setError('Unable to generate PDF.'); return; }
    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement('a');
    anchor.href = url;
    anchor.download = `retirement-planning-report-${runId}.pdf`;
    document.body.appendChild(anchor);
    anchor.click();
    anchor.remove();
    URL.revokeObjectURL(url);
  };

  if (error) return <main className="p-8"><h1 className="text-2xl font-semibold">Retirement Planning Report</h1><p className="mt-4">{error}</p></main>;
  if (!report) return <main className="p-8"><p>Loading report…</p></main>;

  return <main className="mx-auto max-w-5xl space-y-6 p-6 md:p-10">
    <header className="flex flex-col gap-4 border-b pb-6 md:flex-row md:items-end md:justify-between">
      <div><p className="text-sm text-gray-500">Planvesto</p><h1 className="mt-2 text-3xl font-semibold">{report.title}</h1></div>
      <button type="button" onClick={downloadPdf} className="rounded-lg border px-4 py-2 text-sm font-medium shadow-sm">Download PDF</button>
    </header>
    {report.sections.map(section => <section key={section.id} className="rounded-xl border p-5 shadow-sm"><h2 className="mb-4 text-xl font-semibold">{section.title}</h2><div className="text-sm leading-7"><Value value={section.data} /></div></section>)}
  </main>;
}
