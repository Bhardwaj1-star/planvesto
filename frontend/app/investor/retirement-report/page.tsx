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

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const runId = params.get('run_id');
    const planningUnitId = params.get('planning_unit_id');
    if (!runId || !planningUnitId) { setError('A strategy run and planning unit are required.'); return; }
    fetch(`/api/strategy/runs/${encodeURIComponent(runId)}/retirement-report?planning_unit_id=${encodeURIComponent(planningUnitId)}`)
      .then(async r => { if (!r.ok) throw new Error(await r.text()); return r.json(); })
      .then(setReport)
      .catch(e => setError(e.message || 'Unable to load report.'));
  }, []);

  if (error) return <main className="p-8"><h1 className="text-2xl font-semibold">Retirement Planning Report</h1><p className="mt-4">{error}</p></main>;
  if (!report) return <main className="p-8"><p>Loading report…</p></main>;

  return <main className="mx-auto max-w-5xl space-y-6 p-6 md:p-10">
    <header className="border-b pb-6"><p className="text-sm text-gray-500">Planvesto</p><h1 className="mt-2 text-3xl font-semibold">{report.title}</h1></header>
    {report.sections.map(section => <section key={section.id} className="rounded-xl border p-5 shadow-sm"><h2 className="mb-4 text-xl font-semibold">{section.title}</h2><div className="text-sm leading-7"><Value value={section.data} /></div></section>)}
  </main>;
}
