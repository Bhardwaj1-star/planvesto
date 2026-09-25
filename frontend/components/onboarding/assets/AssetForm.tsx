"use client";

import { useState } from "react";
import { usePathname } from "next/navigation";
import { assetTypes, type Asset, type AssetErrors } from "../../../lib/onboarding/assets/types";
import { supportsPurchaseValue } from "../../../lib/onboarding/assets/assets";

type Props = {
  asset: Asset;
  errors: AssetErrors;
  isEditing: boolean;
  onChange: (changes: Partial<Asset>) => void;
  onSave: (event: React.FormEvent<HTMLFormElement>) => boolean | Promise<boolean>;
  onCancel: () => void;
};

function fieldClasses(hasError = false) { return `form-field w-full rounded-xl border bg-white px-4 py-3.5 text-sm text-navy-900 placeholder:text-slate-400 ${hasError ? "border-red-300" : "border-slate-200"}`; }
function ErrorMessage({ id, message }: { id: string; message?: string }) { return message ? <p id={id} className="mt-2 text-xs font-medium text-red-600" role="alert">{message}</p> : null; }

export default function AssetForm({ asset, errors, isEditing, onChange, onSave, onCancel }: Props) {
  const pathname = usePathname();
  const isProfile = pathname === "/investor/profile";
  const [profileOpen, setProfileOpen] = useState(false);
  const showPurchaseValue = supportsPurchaseValue(asset.assetType);
  const today = new Date().toISOString().slice(0, 10);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    const saved = await onSave(event);
    if (saved && isProfile) setProfileOpen(false);
  }

  if (isProfile && !isEditing && !profileOpen) {
    return <div className="flex justify-start"><button type="button" onClick={() => setProfileOpen(true)} className="inline-flex items-center justify-center gap-2 rounded-xl border border-teal-600 bg-white px-5 py-3 text-sm font-bold text-teal-700 shadow-sm transition hover:bg-teal-50">+ Add new asset</button></div>;
  }

  return (
    <form noValidate onSubmit={handleSubmit} className="rounded-[28px] border border-teal-200 bg-teal-50/50 p-6 shadow-soft sm:p-8">
      <div className="mb-6 flex items-start justify-between gap-4 border-b border-teal-100 pb-5"><div><p className="text-xs font-bold uppercase tracking-[0.14em] text-teal-700">{isEditing ? "Edit asset" : "New asset"}</p><h2 className="mt-2 text-xl font-extrabold text-navy-900">Describe what you own</h2></div>{isEditing && <button type="button" onClick={onCancel} className="text-sm font-bold text-slate-500 underline decoration-slate-300 underline-offset-4 hover:text-navy-900">Cancel</button>}</div>
      <div className="grid gap-5 sm:grid-cols-2">
        <div><label htmlFor="assetType" className="mb-2 block text-sm font-semibold text-navy-900">Asset type</label><select id="assetType" value={asset.assetType} onChange={(event) => onChange({ assetType: event.target.value as Asset["assetType"] })} aria-invalid={Boolean(errors.assetType)} aria-describedby={errors.assetType ? "assetType-error" : undefined} className={`${fieldClasses(Boolean(errors.assetType))} appearance-none`}><option value="">Select an asset type</option>{assetTypes.map((type) => <option key={type} value={type}>{type}</option>)}</select><ErrorMessage id="assetType-error" message={errors.assetType} /></div>
        <div><label htmlFor="description" className="mb-2 block text-sm font-semibold text-navy-900">Name / description</label><input id="description" value={asset.description} onChange={(event) => onChange({ description: event.target.value })} aria-invalid={Boolean(errors.description)} aria-describedby={errors.description ? "description-error" : undefined} placeholder="e.g. Emergency savings, Family home" className={fieldClasses(Boolean(errors.description))} /><ErrorMessage id="description-error" message={errors.description} /></div>
        <div><label htmlFor="currentValue" className="mb-2 block text-sm font-semibold text-navy-900">Current value</label><div className="relative"><span className="pointer-events-none absolute left-4 top-3.5 text-sm text-slate-400">₹</span><input id="currentValue" type="number" min="0.01" step="0.01" inputMode="decimal" value={asset.currentValue} onChange={(event) => onChange({ currentValue: event.target.value })} onKeyDown={(event) => ["e", "E", "+", "-"].includes(event.key) && event.preventDefault()} aria-invalid={Boolean(errors.currentValue)} aria-describedby={errors.currentValue ? "currentValue-error" : undefined} placeholder="0.00" className={`${fieldClasses(Boolean(errors.currentValue))} pl-8`} /></div><ErrorMessage id="currentValue-error" message={errors.currentValue} /></div>
        {showPurchaseValue && <div><label htmlFor="purchaseValue" className="mb-2 block text-sm font-semibold text-navy-900">Purchase / cost value <span className="font-normal text-slate-400">(optional)</span></label><div className="relative"><span className="pointer-events-none absolute left-4 top-3.5 text-sm text-slate-400">₹</span><input id="purchaseValue" type="number" min="0.01" step="0.01" inputMode="decimal" value={asset.purchaseValue} onChange={(event) => onChange({ purchaseValue: event.target.value })} onKeyDown={(event) => ["e", "E", "+", "-"].includes(event.key) && event.preventDefault()} aria-invalid={Boolean(errors.purchaseValue)} aria-describedby={errors.purchaseValue ? "purchaseValue-error" : undefined} placeholder="0.00" className={`${fieldClasses(Boolean(errors.purchaseValue))} pl-8`} /></div><ErrorMessage id="purchaseValue-error" message={errors.purchaseValue} /></div>}
        <div className={showPurchaseValue ? "" : "sm:col-span-2"}><label htmlFor="purchaseDate" className="mb-2 block text-sm font-semibold text-navy-900">Purchase date <span className="font-normal text-slate-400">(optional)</span></label><input id="purchaseDate" type="date" max={today} value={asset.purchaseDate} onChange={(event) => onChange({ purchaseDate: event.target.value })} aria-invalid={Boolean(errors.purchaseDate)} aria-describedby={errors.purchaseDate ? "purchaseDate-error" : undefined} className={fieldClasses(Boolean(errors.purchaseDate))} /><ErrorMessage id="purchaseDate-error" message={errors.purchaseDate} /></div>
      </div>
      <div className="mt-7 flex flex-col-reverse gap-3 sm:flex-row sm:justify-end">{isEditing && <button type="button" onClick={onCancel} className="rounded-xl border border-slate-200 bg-white px-5 py-3 text-sm font-bold text-navy-900 transition hover:border-slate-300">Cancel</button>}<button type="submit" className="rounded-xl bg-teal-700 px-5 py-3 text-sm font-bold text-white shadow-sm transition hover:bg-teal-800 focus:outline-none focus:ring-4 focus:ring-teal-100">{isEditing ? "Save changes" : "Add asset"}</button></div>
    </form>
  );
}