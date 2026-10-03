"use client";

import { useEffect, useMemo, useState, Suspense } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import Link from "next/link";
import InvestorHeader from "../../../components/InvestorHeader";
import StrategyWorkflowNav from "../../../components/StrategyWorkflowNav";
import { InvestorButton, InvestorStatus } from "../../../components/InvestorUI";
import { getPlanningUnitId, getStrategyRunById, type StrategyRun } from "../../../lib/api/strategy";

function StrategyComparisonContent() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const [run, setRun] = useState<StrategyRun | null>(null);
  const [error, setError] = useState<string | null>(null);

  const goalId = searchParams.get("goalId") ?? "";
  const strategyRunId = searchParams.get("strategyRunId") ?? "";
  const recommendedStrategyId = searchParams.get("recommendedStrategyId") ?? "";
  const alternativeStrategyId = searchParams.get("alternativeStrategyId") ?? "";

  useEffect(() => {
    let active = true;
    (async () => {
      try {
        const planningUnitId = getPlanningUnitId();
        if (!planningUnitId || !strategyRunId) throw new Error("Comparison context is missing.");
        const next = await getStrategyRunById(planningUnitId, strategyRunId);
        if (active) setRun(next);
      } catch (err) {
        if (active) setError(err instanceof Error ? err.message : "Unable to load strategy comparison.");
      }
    })();
    return () => { active = false; };
  }, [strategyRunId]);

  const comparison = useMemo(() => {
    if (!run) return null;
    const recommended = run.applicable_strategies.find((item) => item.strategy_id === recommendedStrategyId);
    const alternative = run.applicable_strategies.find((item) => item.strategy_id === alternativeStrategyId);
    const recommendedRanking = run.rankings.find((item) => item.strategy_id === recommendedStrategyId);
    const alternativeRanking = run.rankings.find((item) => item.strategy_id === alternativeStrategyId);
    const recommendedArchitecture = run.architectures.find((item) => item.primary_strategy_id === recommendedStrategyId);
    const alternativeArchitecture = run.architectures.find((item) => item.primary_strategy_id === alternativeStrategyId);
    return { recommended, alternative, recommendedRanking, alternativeRanking, recommendedArchitecture, alternativeArchitecture };
  }, [run, recommendedStrategyId, alternativeStrategyId]);

  return (
    <main className="min-h-screen bg-[#f6f8fb] pb-16 text-slate-900">
      <InvestorHeader
        eyebrow="Understand"
        title="Strategy Comparison"
        description="Understand how the recommended strategy differs from the alternative, and why the decision engine produced these two paths."
      />
      <div className="mx-auto max-w-6xl space-y-6 p-4 sm:p-6 lg:p-10">
        <StrategyWorkflowNav />
        {error && <InvestorStatus tone="error">{error}</InvestorStatus>}
        {!comparison ? (
          <section className="rounded-3xl border border-slate-200 bg-white p-10 text-center">
            <p className="text-sm text-slate-500">Loading comparison…</p>
          </section>
        ) : (
          <>
            <section className="grid gap-5 lg:grid-cols-2">
              {[{ label: "Recommended Strategy", strategy: comparison.recommended, ranking: comparison.recommendedRanking, architecture: comparison.recommendedArchitecture, recommended: true },
                { label: "Alternative Strategy", strategy: comparison.alternative, ranking: comparison.alternativeRanking, architecture: comparison.alternativeArchitecture, recommended: false }].map((item) => (
                <article key={item.strategy?.strategy_id ?? item.label} className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
                  <p className="text-xs font-bold uppercase tracking-wider text-slate-400">{item.label}</p>
                  <h2 className="mt-2 text-2xl font-extrabold text-slate-900">{item.strategy?.name ?? "Unavailable"}</h2>
                  <p className="mt-2 text-sm leading-6 text-slate-600">{item.strategy?.description ?? "No description available."}</p>
                  <div className="mt-5 space-y-3 text-sm">
                    <div><span className="font-bold">Objective:</span> {item.strategy?.strategic_objective ?? item.strategy?.tagline ?? "—"}</div>
                    <div><span className="font-bold">Feasibility:</span> {item.architecture?.feasibility_status ?? "—"}</div>
                    <div><span className="font-bold">Scenario:</span> {item.ranking?.scenario_name ?? "—"}</div>
                  </div>
                  {item.strategy?.trade_offs?.length ? (
                    <div className="mt-5 rounded-2xl bg-slate-50 p-4">
                      <p className="text-xs font-bold uppercase tracking-wider text-slate-500">Known Trade-offs</p>
                      <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-slate-600">
                        {item.strategy.trade_offs.map((tradeoff, index) => <li key={index}>{tradeoff}</li>)}
                      </ul>
                    </div>
                  ) : null}
                </article>
              ))}
            </section>

            <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
              <h2 className="text-lg font-bold">Why this recommendation?</h2>
              <p className="mt-3 text-sm leading-7 text-slate-600">{run?.recommendation.complete_reasoning ?? "No recommendation reasoning available."}</p>
              {run?.recommendation.short_reasons?.length ? (
                <ul className="mt-4 list-disc space-y-2 pl-5 text-sm text-slate-600">
                  {run.recommendation.short_reasons.map((reason, index) => <li key={index}>{reason}</li>)}
                </ul>
              ) : null}
            </section>

            <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
              <h2 className="text-lg font-bold">What will be compared later?</h2>
              <p className="mt-2 text-sm leading-6 text-slate-500">
                The comparison contract is intentionally limited at this stage. Detailed scoring, parameter-by-parameter differences,
                and additional explainability rules will be defined in a later product stage rather than invented here.
              </p>
            </section>

            <div className="flex flex-wrap gap-3">
              <InvestorButton onClick={() => router.push(`/investor/strategy-builder?goalId=${encodeURIComponent(goalId)}`)}>
                Back to Strategy Builder
              </InvestorButton>
              <Link
                href={`/investor/strategy-scenarios?goalId=${encodeURIComponent(goalId)}&strategyRunId=${encodeURIComponent(strategyRunId)}&strategyId=${encodeURIComponent(recommendedStrategyId)}&goalVersion=${encodeURIComponent(String(run?.defined_goal_version ?? ""))}`}
                className="inline-flex items-center rounded-xl border border-slate-200 bg-white px-5 py-3 text-sm font-bold text-slate-700"
              >
                Plan Recommended Strategy →
              </Link>
            </div>
          </>
        )}
      </div>
    </main>
  );
}


export default function StrategyComparisonPage() {
  return (
    <Suspense
      fallback={
        <main className="min-h-screen bg-[#f6f8fb] p-6 lg:p-10">
          <div className="mx-auto max-w-6xl space-y-6">
            <div className="h-10 w-80 animate-pulse rounded-xl bg-slate-200" />
            <div className="h-96 animate-pulse rounded-3xl bg-white" />
          </div>
        </main>
      }
    >
      <StrategyComparisonContent />
    </Suspense>
  );
}
