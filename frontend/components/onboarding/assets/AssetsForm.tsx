"use client";

import AssetForm from "./AssetForm";
import AssetSummary from "./AssetSummary";
import { useAssets } from "../../../hooks/onboarding/assets/useAssets";
import OnboardingShell from "../OnboardingShell";

export default function AssetsForm() {
  const assets = useAssets();

  return (
    <OnboardingShell
      currentStep={4}
      title="What do you own today?"
      subtitle="Cataloging your current savings, investments, and property establishes your balance sheet baseline."
      stepContext="Assets & Investments"
      badge={assets.assets.length > 0 ? `${assets.assets.length} asset${assets.assets.length > 1 ? "s" : ""} added` : undefined}
    >
      <div className="space-y-6">
        <AssetSummary
          assets={assets.assets}
          onEdit={assets.startEditing}
          onRemove={assets.removeAsset}
        />

        <AssetForm
          asset={assets.draft}
          errors={assets.errors}
          isEditing={Boolean(assets.editingAssetId)}
          onChange={assets.updateDraft}
          onSave={assets.saveAsset}
          onCancel={assets.cancelEditing}
        />

        {/* Consistent Action Bar */}
        <div className="flex flex-col-reverse items-stretch gap-4 pt-4 sm:flex-row sm:items-center sm:justify-between border-t border-slate-200/80">
          <button
            type="button"
            onClick={assets.goPrevious}
            className="inline-flex items-center justify-center gap-2 rounded-xl border border-slate-200 bg-white px-5 py-3 text-sm font-bold text-slate-700 shadow-sm transition hover:bg-slate-50 hover:text-navy-900"
          >
            <span aria-hidden="true">&larr;</span>
            Back to Expenses
          </button>

          <button
            type="button"
            onClick={assets.handleContinue}
            className="inline-flex items-center justify-center gap-2 rounded-xl bg-navy-900 px-7 py-3.5 text-sm font-bold text-white shadow-sm transition hover:bg-navy-800 focus:outline-none focus:ring-4 focus:ring-teal-100 disabled:cursor-not-allowed disabled:opacity-60"
          >
            Continue to Liabilities
            <span aria-hidden="true">&rarr;</span>
          </button>
        </div>

        {assets.isComplete && (
          <p className="rounded-xl border border-teal-200 bg-teal-50 px-4 py-3 text-sm font-semibold text-teal-700" role="status">
            Asset information is complete for this session.
          </p>
        )}
      </div>
    </OnboardingShell>
  );
}