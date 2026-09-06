import { formatCurrency, getTotalAssets, isFinancialAsset, isPhysicalAsset } from "../../../lib/onboarding/assets/assets";
import type { Asset } from "../../../lib/onboarding/assets/types";
import AssetCard from "./AssetCard";

type Props = { assets: Asset[]; onEdit: (asset: Asset) => void; onRemove: (id: string) => void };

export default function AssetSummary({ assets, onEdit, onRemove }: Props) {
  const totalAssets = getTotalAssets(assets);
  const financialAssets = assets.filter(isFinancialAsset).reduce((total, asset) => total + Number(asset.currentValue), 0);
  const physicalAssets = assets.filter(isPhysicalAsset).reduce((total, asset) => total + Number(asset.currentValue), 0);
  if (assets.length === 0) {
    return (
      <div className="rounded-[28px] border border-dashed border-slate-300 bg-white px-6 py-10 text-center sm:px-8">
        <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-teal-50 text-teal-700" aria-hidden="true">
          $
        </div>
        <h2 className="mt-4 text-lg font-extrabold text-navy-900">No assets added yet</h2>
        <p className="mx-auto mt-2 max-w-md text-sm leading-6 text-slate-500">
          Add what you own today so Planvesto can understand your current financial position. You can continue without adding an asset right now.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="grid gap-3 sm:grid-cols-3">
        <div className="rounded-2xl border border-navy-900 bg-navy-900 p-5 text-white">
          <p className="text-xs font-bold uppercase tracking-[0.14em] text-teal-200">Total assets</p>
          <p className="mt-2 text-2xl font-extrabold">{formatCurrency(totalAssets)}</p>
        </div>
        <div className="rounded-2xl border border-teal-200 bg-teal-50 p-5 text-navy-900">
          <p className="text-xs font-bold uppercase tracking-[0.14em] text-teal-700">Financial assets</p>
          <p className="mt-2 text-2xl font-extrabold">{formatCurrency(financialAssets)}</p>
        </div>
        <div className="rounded-2xl border border-slate-200 bg-white p-5 text-navy-900">
          <p className="text-xs font-bold uppercase tracking-[0.14em] text-slate-500">Physical / real assets</p>
          <p className="mt-2 text-2xl font-extrabold">{formatCurrency(physicalAssets)}</p>
        </div>
      </div>
      <div className="space-y-3">
        {assets.map((asset) => (
          <AssetCard key={asset.id} asset={asset} onEdit={() => onEdit(asset)} onRemove={() => onRemove(asset.id)} />
        ))}
      </div>
    </div>
  );
}