"use client";

import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import Link from "next/link";
import InvestorHeader from "../../../components/InvestorHeader";
import { downloadGoalStrategyReportPdfByStrategyVersion, getPlanningUnitId } from "../../../lib/api/strategy";

export default function GoalReportPage() {
  const searchParams = useSearchParams();
  const strategyVersionId = searchParams.get("strategyVersionId");
  const goalId = searchParams.get("goalId");
  const [pdfUrl, setPdfUrl] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    let objectUrl: string | null = null;

    if (!strategyVersionId) {
      setError("A finalized Strategy Version is required to view this report.");
      return () => undefined;
    }

    (async () => {
      try {
        const planningUnitId = getPlanningUnitId();
        if (!planningUnitId) throw new Error("Planning unit is not available.");
        const blob = await downloadGoalStrategyReportPdfByStrategyVersion(planningUnitId, strategyVersionId);
        objectUrl = URL.createObjectURL(blob);
        if (active) setPdfUrl(objectUrl);
      } catch (err) {
        if (active) setError(err instanceof Error ? err.message : "Unable to load the goal report.");
      }
    })();

    return () => {
      active = false;
      if (objectUrl) URL.revokeObjectURL(objectUrl);
    };
  }, [strategyVersionId]);

  return (
    <main className="min-h-screen bg-[#f6f8fb] pb-10 text-slate-900">
      <InvestorHeader
        eyebrow="Goal Report"
        title="Goal Strategy Report"
        description="Your finalized goal strategy report, generated from the selected Strategy Version."
      />
      <div className="mx-auto max-w-7xl space-y-4 p-4 sm:p-6 lg:p-8">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div className="text-xs text-slate-500">
            {goalId ? "Goal: " + goalId : "Finalized Strategy Version"}
            {strategyVersionId ? " · Version: " + strategyVersionId : ""}
          </div>
          <div className="flex gap-2">
            <Link href="/investor/reports" className="rounded-xl border border-slate-200 bg-white px-4 py-2 text-xs font-bold text-slate-700">
              Reports Center
            </Link>
            {pdfUrl && (
              <a href={pdfUrl} target="_blank" rel="noreferrer" className="rounded-xl bg-slate-900 px-4 py-2 text-xs font-bold text-white">
                Open PDF ↗
              </a>
            )}
          </div>
        </div>

        {error ? (
          <div className="rounded-2xl border border-rose-200 bg-rose-50 p-5 text-sm text-rose-800">{error}</div>
        ) : pdfUrl ? (
          <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
            <iframe title="Goal Strategy Report" src={pdfUrl} className="h-[78vh] w-full" />
          </div>
        ) : (
          <div className="flex h-[70vh] items-center justify-center rounded-2xl border border-slate-200 bg-white text-sm text-slate-500">
            Loading your goal report…
          </div>
        )}
      </div>
    </main>
  );
}
