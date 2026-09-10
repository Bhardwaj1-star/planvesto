"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { getPlanningUnitId, getCurrentPrimaryStrategy, getStrategyVersionHistory, type StrategyVersion } from "../../../lib/api/strategy-version";
import { editStrategy } from "../../../lib/api/strategy-edit";

export default function StrategyEditPage() {
  const [primary, setPrimary] = useState<Awaited<ReturnType<typeof getCurrentPrimaryStrategy>>>(null);
  const [versions, setVersions] = useState<StrategyVersion[]>([]);
  const [version, setVersion] = useState(0);
  const [parameters, setParameters] = useState("{}\n");
  const [loading, setLoading] = useState(true);
  const [working, setWorking] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<Awaited<ReturnType<typeof editStrategy>> | null>(null);

  useEffect(() => {
    let active = true;
    (async () => {
      try {
        const pu = getPlanningUnitId();
        if (!pu) throw new Error("Planning unit is not available. Please complete onboarding first.");
        const current = await getCurrentPrimaryStrategy(pu);
        if (!active) return;
        setPrimary(current);
        if (current) {
          const history = await getStrategyVersionHistory(pu, current.strategy_id);
          if (!active) return;
          setVersions(history);
          const currentVersion = history.find((v) => v.strategy_version_id === current.strategy_version_id) ?? history[history.length - 1];
          if (currentVersion) { setVersion(currentVersion.version); setParameters(JSON.stringify(currentVersion.implementation_parameters ?? {}, null, 2)); }
        }
      } catch (err) { if (active) setError(err instanceof Error ? err.message : "Unable to load Primary Strategy."); }
      finally { if (active) setLoading(false); }
    })();
    return () => { active = false; };
  }, []);

  async function submit() {
    const pu = getPlanningUnitId();
    if (!pu || !primary || !version) return setError("A current Primary Strategy and parent version are required.");
    let parsed: Record<string, unknown>;
    try { parsed = JSON.parse(parameters); } catch { setError("Implementation parameters must be valid JSON."); return; }
    if (!parsed || Array.isArray(parsed) || typeof parsed !== "object") { setError("Implementation parameters must be a JSON object."); return; }
    setWorking(true); setError(null); setResult(null);
    try { setResult(await editStrategy({ planning_unit_id: pu, strategy_id: primary.strategy_id, parent_version: version, implementation_parameters: parsed })); }
    catch (err) { setError(err instanceof Error ? err.message : "Strategy edit failed."); }
    finally { setWorking(false); }
  }

  if (loading) return <main className="min-h-screen bg-[#f6f8fb] p-6 lg:p-10"><div className="mx-auto max-w-4xl"><div className="h-10 w-72 animate-pulse rounded-xl bg-slate-200" /><div className="mt-6 h-96 animate-pulse rounded-3xl bg-white" /></div></main>;

  return <main className="min-h-screen bg-[#f6f8fb] pb-16 text-slate-900"><div className="mx-auto max-w-4xl space-y-6 p-6 lg:p-10">
    <header><Link href="/investor/strategy-history" className="text-sm font-semibold text-teal-700">← Strategy History</Link><p className="mt-6 text-sm font-semibold uppercase tracking-[0.16em] text-teal-700">Controlled change</p><h1 className="mt-1 text-3xl font-extrabold tracking-tight">Edit Strategy</h1><p className="mt-2 text-sm leading-6 text-slate-500">Editing never mutates an existing Strategy Version. The backend creates a new investor-edit version and flags suitability reassessment.</p></header>
    {error && <div className="rounded-2xl border border-red-200 bg-red-50 px-5 py-4 text-sm text-red-700">{error}</div>}
    {result && <section className="rounded-3xl border border-emerald-200 bg-emerald-50 p-6"><h2 className="text-lg font-bold text-emerald-900">New Strategy Version created</h2><div className="mt-3 grid gap-3 sm:grid-cols-2 text-sm"><p>Version: <b>v{result.strategy_version}</b></p><p>Parent: <b>v{result.parent_version}</b></p><p>Suitability reassessment: <b>{result.suitability_reassessment_required ? "Required" : "Not required"}</b></p><p>Primary replacement: <b>{result.primary_replacement_required ? "Required" : "Not required"}</b></p></div><p className="mt-4 text-sm text-emerald-800">The new version remains separate from the parent snapshot. Complete the downstream suitability/approval workflow before treating it as a new Primary Strategy.</p></section>}
    {!primary ? <section className="rounded-3xl border border-dashed border-slate-300 bg-white p-10 text-center"><h2 className="text-xl font-bold">No Primary Strategy</h2><p className="mt-2 text-sm text-slate-500">Approve and make a strategy Primary before using the controlled edit workflow.</p><Link href="/investor/strategy-approval" className="mt-6 inline-flex rounded-xl bg-navy-900 px-5 py-3 text-sm font-bold text-white">Open Strategy Approval</Link></section> : <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm space-y-5"><div className="grid gap-4 sm:grid-cols-3"><div><p className="text-xs text-slate-400">Primary Strategy</p><p className="mt-1 font-bold">{primary.strategy_id}</p></div><div><p className="text-xs text-slate-400">Current Version</p><p className="mt-1 font-bold">{primary.strategy_version_id}</p></div><div><p className="text-xs text-slate-400">Available Versions</p><p className="mt-1 font-bold">{versions.length}</p></div></div><label className="block"><span className="text-sm font-bold">Parent version</span><select value={version} onChange={(e) => { const next = Number(e.target.value); setVersion(next); const selected = versions.find((v) => v.version === next); if (selected) setParameters(JSON.stringify(selected.implementation_parameters ?? {}, null, 2)); }} className="mt-2 w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm">{versions.map((v) => <option key={v.strategy_version_id ?? v.version} value={v.version}>v{v.version} · {v.status} · {v.source}</option>)}</select></label><label className="block"><span className="text-sm font-bold">Implementation parameters</span><p className="mt-1 text-xs text-slate-500">Advanced JSON editor; backend remains responsible for validation and version creation.</p><textarea value={parameters} onChange={(e) => setParameters(e.target.value)} rows={16} className="mt-2 w-full rounded-2xl border border-slate-200 px-4 py-3 font-mono text-xs outline-none focus:border-teal-600" /></label><button onClick={() => void submit()} disabled={working} className="w-full rounded-2xl bg-navy-900 px-5 py-4 text-sm font-extrabold text-white disabled:opacity-50">{working ? "Creating new version…" : "Create New Strategy Version"}</button></section>}
  </div></main>;
}
