"use client";

import Link from "next/link";
import { type FinancialDecision } from "../../lib/diary/diaryStore";

type DecisionHistoryViewProps = {
  decisions: FinancialDecision[];
  onLogDecision?: () => void;
};

function metricText(value: unknown) {
  if (value === null || value === undefined) return "";
  if (typeof value === "string" || typeof value === "number" || typeof value === "boolean") return String(value);
  return JSON.stringify(value);
}

export default function DecisionHistoryView({ decisions }: DecisionHistoryViewProps) {
  return (
    <div className="mx-auto max-w-4xl space-y-6">
      <div className="rounded-3xl border border-slate-200 bg-white p-6 sm:p-8 shadow-sm">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <div className="flex items-center gap-2"><span className="flex h-2.5 w-2.5 rounded-full bg-teal-600" /><p className="text-xs font-bold uppercase tracking-wider text-slate-400">Planvesto Memory</p></div>
            <h2 className="mt-1 font-serif text-2xl sm:text-3xl font-bold text-slate-950">Chronological Decision History</h2>
            <p className="mt-1.5 text-sm text-slate-600 max-w-2xl">Every major financial fork in the road—strategy selections, SIP revisions, debt prepayments, and goal pivots—preserved chronologically as historical context.</p>
          </div>
          <Link href="/investor/strategy-builder" className="inline-flex items-center self-start sm:self-center gap-2 rounded-xl bg-navy-900 px-5 py-2.5 text-xs font-bold text-white shadow-sm hover:bg-navy-800 transition"><span>Open Strategy Builder</span><span aria-hidden="true">→</span></Link>
        </div>
      </div>

      <div className="relative pl-6 sm:pl-8 before:absolute before:left-3 sm:before:left-4 before:top-3 before:bottom-3 before:w-0.5 before:bg-gradient-to-b before:from-teal-600 before:via-slate-200 before:to-transparent space-y-6">
        {decisions.map((decision) => (
          <div key={decision.id} className="relative rounded-2xl border border-slate-200 bg-white p-6 shadow-sm transition hover:border-slate-300 hover:shadow-md">
            <div className="absolute -left-9 sm:-left-11 top-6 flex h-6 w-6 items-center justify-center rounded-full bg-white border-2 border-teal-600 text-[10px] font-bold text-teal-700 shadow-xs">●</div>
            <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-3 border-b border-slate-100 pb-4">
              <div>
                <div className="flex flex-wrap items-center gap-2">
                  <span className="inline-flex items-center rounded-md bg-navy-900 px-2.5 py-0.5 text-xs font-black text-white">{decision.displayDate}</span>
                  <span className="text-xs font-semibold text-slate-400">· {decision.fullDate}</span>
                  <span className="inline-flex items-center rounded-md bg-slate-100 px-2 py-0.5 text-[11px] font-bold text-slate-700">{decision.category}</span>
                  <span className="text-[11px] text-teal-700 font-medium">via {decision.source}</span>
                </div>
                <h3 className="mt-2 text-lg sm:text-xl font-extrabold text-slate-950">{decision.title}</h3>
              </div>
            </div>

            <p className="mt-3 text-sm leading-relaxed text-slate-700">{decision.summary}</p>

            {decision.metrics && (
              <div className="mt-4 grid grid-cols-2 gap-3 sm:grid-cols-4 rounded-xl bg-slate-50 p-3.5 border border-slate-100">
                {Boolean(decision.metrics.target) && <div><p className="text-[10px] font-bold uppercase tracking-wider text-slate-400">Target</p><p className="mt-0.5 text-sm font-extrabold text-slate-900">{metricText(decision.metrics.target)}</p></div>}
                {Boolean(decision.metrics.horizon) && <div><p className="text-[10px] font-bold uppercase tracking-wider text-slate-400">Horizon</p><p className="mt-0.5 text-sm font-extrabold text-slate-900">{metricText(decision.metrics.horizon)}</p></div>}
                {Boolean(decision.metrics.monthlyInvestment) && <div><p className="text-[10px] font-bold uppercase tracking-wider text-slate-400">Monthly SIP</p><p className="mt-0.5 text-sm font-extrabold text-teal-700">{decision.metrics.previousMonthlyInvestment ? <span><span className="line-through text-slate-400 font-normal mr-1">{metricText(decision.metrics.previousMonthlyInvestment)}</span>{metricText(decision.metrics.monthlyInvestment)}</span> : metricText(decision.metrics.monthlyInvestment)}</p></div>}
                {Boolean(decision.metrics.expectedReturn) && <div><p className="text-[10px] font-bold uppercase tracking-wider text-slate-400">Return Profile</p><p className="mt-0.5 text-sm font-extrabold text-slate-900">{metricText(decision.metrics.expectedReturn)}</p></div>}
              </div>
            )}

            {decision.notes && <p className="mt-3 text-xs leading-relaxed text-slate-500 italic">“{decision.notes}”</p>}
          </div>
        ))}
      </div>
    </div>
  );
}
