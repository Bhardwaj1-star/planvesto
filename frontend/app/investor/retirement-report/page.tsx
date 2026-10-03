'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { loadGoalPlannerData } from '../../../lib/onboarding/persistence';

/**
 * RetirementReportPage
 * Canonicalized redirect: Unifies retirement planning into the generic Goal Decision Report.
 * All goals (Retirement, Education, Home, Marriage, etc.) share the same institutional
 * decision report architecture instead of maintaining fragmented one-off views.
 */
export default function RetirementReportPage() {
  const router = useRouter();

  useEffect(() => {
    let active = true;

    async function redirect() {
      try {
        const goalData = await loadGoalPlannerData();
        const goals = goalData?.goals ?? [];
        const retirementGoal =
          goals.find(
            (g) =>
              g.name?.toLowerCase().includes('retirement') ||
              (g as { type?: string }).type?.toLowerCase().includes('retirement')
          ) || goals[0];

        if (!active) return;

        if (retirementGoal?.id) {
          router.replace("/investor/reports");
        } else {
          router.replace("/investor/reports");
        }
      } catch {
        if (active) {
          router.replace('/investor/goal-report');
        }
      }
    }

    void redirect();
    return () => {
      active = false;
    };
  }, [router]);

  return (
    <main className="min-h-screen bg-[#f6f8fb] p-6 lg:p-10 text-center">
      <div className="mx-auto max-w-md space-y-4 py-24">
        <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-navy-900 border-t-transparent" />
        <p className="text-sm font-semibold text-slate-600">Loading Goal Decision Report…</p>
      </div>
    </main>
  );
}
