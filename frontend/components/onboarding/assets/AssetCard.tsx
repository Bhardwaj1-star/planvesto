import { annualAssetValue, formatCurrency, isFinancialAsset, isPhysicalAsset } from "../../../lib/onboarding/assets/assets";
import type { Asset } from "../../../lib/onboarding/assets/types";

type Props = { asset: Asset; onEdit: () => void; onRemove: () => void };

export default function AssetCard({ asset, onEdit, onRemove }: Props) {
  const kind = isFinancialAsset(asset) ? "Financial asset" : isPhysicalAsset(asset) ? "Physical / real asset" : "Asset";
  return (
    <article className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h3 className="font-extrabold text-navy-900">{asset.description}</h3>
          <p className="mt-1 text-sm text-slate-500">{asset.assetType}</p>
        </div>
        <div className="flex shrink-0 gap-3 text-sm font-bold">
          <button type="button" onClick={onEdit} className="text-teal-700 underline decoration-teal-200 underline-offset-4 hover:text-teal-800">
            Edit
          </button>
          <button type="button" onClick={onRemove} className="text-slate-500 underline decoration-slate-200 underline-offset-4 hover:text-red-600">
            Remove
          </button>
        </div>
      </div>
      <div className="mt-4 flex flex-wrap gap-2 text-xs font-semibold">
        <span className="rounded-full bg-slate-100 px-3 py-1 text-slate-700">
          {formatCurrency(annualAssetValue(asset))} current value
        </span>
        {asset.purchaseValue && (
          <span className="rounded-full bg-slate-100 px-3 py-1 text-slate-600">
            Cost {formatCurrency(Number(asset.purchaseValue))}
          </span>
        )}
        {asset.purchaseDate && (
          <span className="rounded-full bg-slate-100 px-3 py-1 text-slate-600">
            Purchased {asset.purchaseDate}
          </span>
        )}
        <span className="rounded-full bg-slate-100 px-3 py-1 text-slate-600">{kind}</span>
      </div>
    </article>
  );
}