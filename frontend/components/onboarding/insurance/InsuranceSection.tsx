"use client";

import { useState } from "react";

type Policy = {
  policyName: string;
  insurer: string;
  policyType: string;
  premium: string;
  premiumFrequency: string;
  sumAssured: string;
  currentValue: string;
  maturityDate: string;
};

const emptyPolicy: Policy = { policyName: "", insurer: "", policyType: "", premium: "", premiumFrequency: "Monthly", sumAssured: "", currentValue: "", maturityDate: "" };

export default function InsuranceSection() {
  const [policy, setPolicy] = useState<Policy>(emptyPolicy);
  const [saved, setSaved] = useState(false);
  const set = (key: keyof Policy, value: string) => setPolicy((p) => ({ ...p, [key]: value }));
  const field = "w-full rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-sm text-navy-900 placeholder:text-slate-400 focus:border-teal-500 focus:outline-none focus:ring-4 focus:ring-teal-50";

  return <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm sm:p-5 space-y-4">
    <div className="border-b border-slate-100 pb-3">
      <h3 className="text-lg font-extrabold text-navy-900">Insurance &amp; Protection</h3>
      <p className="mt-0.5 text-xs text-slate-500">Add insurance policies that may provide both protection and investment value.</p>
    </div>

    <div className="rounded-xl border border-dashed border-teal-200 bg-teal-50/40 p-4">
      <p className="text-sm font-bold text-navy-900">Policy document (optional)</p>
      <p className="mt-1 text-xs text-slate-500">Upload the policy PDF later to auto-fill these details. Manual entry is always available.</p>
      <input type="file" accept="application/pdf" className="mt-3 block w-full text-xs text-slate-600 file:mr-3 file:rounded-lg file:border-0 file:bg-navy-900 file:px-3 file:py-2 file:text-xs file:font-bold file:text-white" />
    </div>

    <div className="grid gap-3 sm:grid-cols-2">
      <div><label className="mb-1 block text-[11px] font-bold uppercase tracking-wider text-slate-500">Policy Name</label><input value={policy.policyName} onChange={(e) => set("policyName", e.target.value)} placeholder="e.g. LIC Jeevan Anand" className={field} /></div>
      <div><label className="mb-1 block text-[11px] font-bold uppercase tracking-wider text-slate-500">Insurer</label><input value={policy.insurer} onChange={(e) => set("insurer", e.target.value)} placeholder="e.g. LIC" className={field} /></div>
      <div><label className="mb-1 block text-[11px] font-bold uppercase tracking-wider text-slate-500">Policy Type</label><select value={policy.policyType} onChange={(e) => set("policyType", e.target.value)} className={field}><option value="">Select type</option><option>Term Insurance</option><option>Endowment</option><option>Money Back</option><option>ULIP</option><option>Whole Life</option><option>Health Insurance</option><option>Other</option></select></div>
      <div><label className="mb-1 block text-[11px] font-bold uppercase tracking-wider text-slate-500">Premium</label><input type="number" min="0" value={policy.premium} onChange={(e) => set("premium", e.target.value)} placeholder="0" className={field} /></div>
      <div><label className="mb-1 block text-[11px] font-bold uppercase tracking-wider text-slate-500">Premium Frequency</label><select value={policy.premiumFrequency} onChange={(e) => set("premiumFrequency", e.target.value)} className={field}><option>Monthly</option><option>Quarterly</option><option>Half-yearly</option><option>Annual</option></select></div>
      <div><label className="mb-1 block text-[11px] font-bold uppercase tracking-wider text-slate-500">Sum Assured</label><input type="number" min="0" value={policy.sumAssured} onChange={(e) => set("sumAssured", e.target.value)} placeholder="0" className={field} /></div>
      <div><label className="mb-1 block text-[11px] font-bold uppercase tracking-wider text-slate-500">Current / Surrender Value</label><input type="number" min="0" value={policy.currentValue} onChange={(e) => set("currentValue", e.target.value)} placeholder="0" className={field} /></div>
      <div><label className="mb-1 block text-[11px] font-bold uppercase tracking-wider text-slate-500">Maturity Date</label><input type="date" value={policy.maturityDate} onChange={(e) => set("maturityDate", e.target.value)} className={field} /></div>
    </div>

    <div className="flex items-center justify-between border-t border-slate-100 pt-3"><span className="text-[11px] text-slate-500">Premium will later be normalized to a monthly expense.</span><button type="button" onClick={() => setSaved(true)} className="rounded-lg bg-navy-900 px-4 py-2 text-[11px] font-bold uppercase tracking-wider text-white hover:bg-navy-800">{saved ? "Saved" : "Save Policy"}</button></div>
  </div>;
}
