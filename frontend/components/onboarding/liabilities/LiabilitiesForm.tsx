"use client";

import LiabilityForm from "./LiabilityForm";
import LiabilitySummary from "./LiabilitySummary";
import { useLiabilities } from "../../../hooks/onboarding/liabilities/useLiabilities";
import OnboardingShell from "../OnboardingShell";

export default function LiabilitiesForm() {
  const liabilities = useLiabilities();
  return (
    <OnboardingShell currentStep={5} title="What do you owe today?" subtitle="Understanding your existing debt and loan terms helps us accurately model your debt payoff and interest load." stepContext="Liabilities & Debt" badge={liabilities.liabilities.length > 0 ? `${liabilities.liabilities.length} liabilit${liabilities.liabilities.length > 1 ? "ies" : "y"} added` : undefined}>
      <div className="space-y-6">
        <LiabilitySummary liabilities={liabilities.liabilities} onEdit={liabilities.startEditing} onRemove={liabilities.removeLiability} />
        {!liabilities.editingLiabilityId && <div className="flex justify-start"><button type="button" onClick={liabilities.startAdding} className="inline-flex items-center justify-center gap-2 rounded-xl border border-teal-600 bg-white px-5 py-3 text-sm font-bold text-teal-700 shadow-sm transition hover:bg-teal-50">+ Add new liability</button></div>}
        {(liabilities.editingLiabilityId || liabilities.liabilities.length === 0) && <LiabilityForm liability={liabilities.draft} errors={liabilities.errors} isEditing={Boolean(liabilities.editingLiabilityId)} onChange={liabilities.updateDraft} onSave={liabilities.saveLiability} onCancel={liabilities.cancelEditing} />}
        <div className="flex flex-col-reverse items-stretch gap-4 pt-4 sm:flex-row sm:items-center sm:justify-between border-t border-slate-200/80">
          <button type="button" onClick={liabilities.goPrevious} className="inline-flex items-center justify-center gap-2 rounded-xl border border-slate-200 bg-white px-5 py-3 text-sm font-bold text-slate-700 shadow-sm">&larr; Back to Assets</button>
          <button type="button" onClick={liabilities.handleContinue} className="inline-flex items-center justify-center gap-2 rounded-xl bg-navy-900 px-7 py-3.5 text-sm font-bold text-white shadow-sm">Continue to Goals &rarr;</button>
        </div>
        {liabilities.isComplete && <p className="rounded-xl border border-teal-200 bg-teal-50 px-4 py-3 text-sm font-semibold text-teal-700" role="status">Liability information is complete for this session.</p>}
      </div>
    </OnboardingShell>
  );
}