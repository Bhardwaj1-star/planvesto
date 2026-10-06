"use client";

import { Suspense, useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import InvestorHeader from "../../../components/InvestorHeader";
import { downloadGoalStrategyReportPdfByStrategyVersion, getPlanningUnitId } from "../../../lib/api/strategy";

function GoalReportContent() {
  const searchParams = useSearchParams();
  const strategyVersionId = searchParams.get("strategyVersionId");
  const goalId = searchParams.get("goalId");
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

        const blob = await downloadGoalStrategyReportPdfByStrategyVersion(
          planningUnitId,
          strategyVersionId,
        );
        objectUrl = URL.createObjectURL(blob);

        if (active) {
          // Navigate the current tab directly to the PDF. This avoids the
          // intermediate iframe/PDF "Open" screen on mobile browsers.
          window.location.replace(objectUrl);
        }
      } catch (err) {
        if (active) {
          setError(
            err instanceof Error ? err.message : "Unable to load the goal report.",
          );
        }
      }
    })();

    return () => {
      active = false;
      // Do not revoke here: the browser is navigating to the object URL.
    };
  }, [strategyVersionId]);

  return (
    <main className="min-h-screen bg-[#f6f8fb] pb-10 text-slate-900">
      <InvestorHeader
        eyebrow="Goal Report"
        title="Goal Strategy Report"
        description="Opening your finalized goal strategy report."
      />
      <div className="mx-auto max-w-7xl p-4 sm:p-6 lg:p-8">
        {error ? (
          <div className="rounded-2xl border border-rose-200 bg-rose-50 p-5 text-sm text-rose-800">
            {error}
          </div>
        ) : (
          <div className="flex h-[70vh] items-center justify-center rounded-2xl border border-slate-200 bg-white text-sm text-slate-500">
            Opening your goal report…
          </div>
        )}
      </div>
    </main>
  );
}

function GoalReportFallback() {
  return (
    <main className="min-h-screen bg-[#f6f8fb] pb-10 text-slate-900">
      <InvestorHeader
        eyebrow="Goal Report"
        title="Goal Strategy Report"
        description="Opening your finalized goal strategy report."
      />
      <div className="mx-auto flex h-[70vh] max-w-7xl items-center justify-center p-4 text-sm text-slate-500 sm:p-6 lg:p-8">
        Opening your goal report…
      </div>
    </main>
  );
}

export default function GoalReportPage() {
  return (
    <Suspense fallback={<GoalReportFallback />}>
      <GoalReportContent />
    </Suspense>
  );
}
