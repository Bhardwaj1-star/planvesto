'use client';

import { useEffect, useState } from 'react';

interface ReportSection {
  id: string;
  title: string;
  description?: string;
  columns?: string[];
  rows?: unknown[][];
  narratives?: Record<string, unknown>;
}
interface Report { title: string; sections: ReportSection[] }

function Value({ value }: { value: unknown }) {
  if (value === null || value === undefined || value === '') return <span className="text-gray-500">Not available</span>;
  if (Array.isArray(value)) return <ul className="list-disc pl-5 space-y-1">{value.map((v, i) => <li key={i}><Value value={v} /></li>)}</ul>;
  if (typeof value === 'object') return <div className="space-y-1">{Object.entries(value as Record<string, unknown>).map(([k, v]) => <div key={k}><span className="font-medium">{k.replaceAll('_', ' ')}:</span> <Value value={v} /></div>)}</div>;
  return <span>{String(value)}</span>;
}

function Section({ section }: { section: ReportSection }) {
  return <section className="rounded-xl border bg-white p-5 shadow-sm">
    <h2 className="mb-2 text-xl font-semibold">{section.title}</h2>
    {section.description && <p className="mb-4 text-sm text-gray-600">{section.description}</p>}
    {section.columns && section.rows ? <div className="overflow-x-auto"><table className="w-full text-left text-sm"><thead><tr className="border-b bg-gray-50">{section.columns.map((column, i) => <th key={i} className="px-3 py-2 font-semibold">{column}</th>)}</tr></thead><tbody>{section.rows.map((row, i) => <tr key={i} className="border-b last:border-0">{row.map((cell, j) => <td key={j} className="px-3 py-2 align-top"><Value value={cell} /></td>)}</tr>)}</tbody></table></div> : <Value value={(section as any).data} />}
    {section.narratives && <div className="mt-5 space-y-4">{Object.entries(section.narratives).map(([label, value]) => <div key={label}><h3 className="font-semibold">{label}</h3><div className="mt-1 text-sm leading-6"><Value value={value} /></div></div>)}</div>}
  </section>;
}

export default function RetirementReportPage() {
  const [report, setReport] = useState<Report | null>(null);
  const [error, setError] = useState('');
  const [runId, setRunId] = useState('');
  const [planningUnitId, setPlanningUnitId] = useState('');
  const [downloading, setDownloading] = useState(false);

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const currentRunId = params.get('run_id') || '';
    const storedPlanningUnitId = typeof window !== 'undefined'
      ? (window.localStorage.getItem('planvesto-planning-unit-id') || window.localStorage.getItem('planvesto_planning_unit_id') || '')
      : '';
    const currentPlanningUnitId = params.get('planning_unit_id') || storedPlanningUnitId;
    setRunId(currentRunId); setPlanningUnitId(currentPlanningUnitId);
    if (!currentRunId || !currentPlanningUnitId) { setError('A strategy run and planning unit are required.'); return; }
    fetch(`/api/strategy/runs/${encodeURIComponent(currentRunId)}/retirement-report?planning_unit_id=${encodeURIComponent(currentPlanningUnitId)}`)
      .then(async r => { if (!r.ok) throw new Error(await r.text()); return r.json(); })
      .then(setReport).catch(e => setError(e.message || 'Unable to load report.'));
  }, []);

  const downloadPdf = async () => {
    setDownloading(true); setError('');
    try {
      const response = await fetch(`/api/strategy/runs/${encodeURIComponent(runId)}/retirement-report.pdf?planning_unit_id=${encodeURIComponent(planningUnitId)}`);
      if (!response.ok) throw new Error('Unable to generate PDF.');
      const blob = await response.blob(); const url = URL.createObjectURL(blob); const anchor = document.createElement('a');
      anchor.href = url; anchor.download = `retirement-planning-report-${runId}.pdf`; document.body.appendChild(anchor); anchor.click(); anchor.remove(); URL.revokeObjectURL(url);
    } catch (e) { setError(e instanceof Error ? e.message : 'Unable to generate PDF.'); } finally { setDownloading(false); }
  };

  if (error && !report) return <main className="p-8"><h1 className="text-2xl font-semibold">Retirement Planning Report</h1><p className="mt-4 text-red-600">{error}</p></main>;
  if (!report) return <main className="p-8"><p>Loading report…</p></main>;

  return <main className="mx-auto max-w-6xl space-y-6 bg-gray-50 p-6 md:p-10">
    <header className="flex flex-col gap-4 border-b pb-6 md:flex-row md:items-end md:justify-between"><div><p className="text-sm text-gray-500">Planvesto</p><h1 className="mt-2 text-3xl font-semibold">{report.title}</h1></div><button type="button" onClick={downloadPdf} disabled={downloading} className="rounded-lg border bg-white px-4 py-2 text-sm font-medium shadow-sm disabled:opacity-50">{downloading ? 'Generating PDF…' : 'Download PDF'}</button></header>
    {error && <p className="rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-700">{error}</p>}
    {report.sections.map(section => <Section key={section.id} section={section} />)}
  </main>;
}
