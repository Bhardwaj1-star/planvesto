"use client";

import { useEffect, useState } from "react";
import { extractInsurancePolicyPdf } from "../../../lib/onboarding/insurance/api";
import { emptyInsurancePolicy, type InsurancePolicyDraft } from "../../../lib/onboarding/insurance/types";
import { loadInsurancePolicies, removeInsurancePolicy, saveInsurancePolicy } from "../../../lib/onboarding/insurance/persistence";

const frequencyOptions = ["Monthly", "Quarterly", "Half-yearly", "Annual"] as const;
const policyTypes = ["Term Insurance", "Endowment", "Money Back", "ULIP", "Whole Life", "Health Insurance", "Other"];

function normalizeFrequency(value?: string | null): InsurancePolicyDraft["premiumFrequency"] {
  const normalized = (value || "").toLowerCase().replace(/[^a-z]/g, "");
  if (normalized === "quarterly") return "Quarterly";
  if (normalized === "halfyearly" || normalized === "halfyear" || normalized === "halfyearly") return "Half-yearly";
  if (normalized === "annual" || normalized === "yearly") return "Annual";
  return "Monthly";
}

function cleanNumber(value?: string | null) {
  return value ? value.replace(/,/g, "").replace(/^₹|^rs\.?|^inr/i, "").trim() : "";
}

export default function InsuranceSection() {
  const [policies, setPolicies] = useState<Awaited<ReturnType<typeof loadInsurancePolicies>>>([]);
  const [draft, setDraft] = useState<InsurancePolicyDraft>({ ...emptyInsurancePolicy });
  const [editingId, setEditingId] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [extracting, setExtracting] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadInsurancePolicies()
      .then(setPolicies)
      .catch((err: unknown) => setError(err instanceof Error ? err.message : "Unable to load insurance policies."))
      .finally(() => setLoading(false));
  }, []);

  const set = <K extends keyof InsurancePolicyDraft>(key: K, value: InsurancePolicyDraft[K]) => setDraft((current) => ({ ...current, [key]: value }));
  const field = "w-full rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-sm text-navy-900 placeholder:text-slate-400 focus:border-teal-500 focus:outline-none focus:ring-4 focus:ring-teal-50";

  function startNew() {
    setDraft({ ...emptyInsurancePolicy });
    setEditingId(null);
    setMessage(null);
    setError(null);
  }

  function edit(policy: (typeof policies)[number]) {
    setDraft({ ...policy });
    setEditingId(policy.id);
    setMessage(null);
    setError(null);
  }

  async function handlePdf(file: File | undefined) {
    if (!file) return;
    setExtracting(true);
    setError(null);
    setMessage("Reading policy document...");
    try {
      const fields = await extractInsurancePolicyPdf(file);
      setDraft((current) => ({
        ...current,
        policyName: fields.policy_name || current.policyName,
        insurer: fields.insurer || current.insurer,
        policyNumber: fields.policy_number || current.policyNumber,
        policyType: fields.policy_type || current.policyType,
        premium: cleanNumber(fields.premium) || current.premium,
        premiumFrequency: normalizeFrequency(fields.premium_frequency),
        sumAssured: cleanNumber(fields.sum_assured) || current.sumAssured,
        currentValue: cleanNumber(fields.current_surrender_value) || current.currentValue,
        maturityDate: fields.maturity_date || current.maturityDate,
        maturityValue: cleanNumber(fields.maturity_value) || current.maturityValue,
        source: "pdf",
      }));
      setMessage("Policy details extracted. Please verify them before saving.");
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Unable to extract the policy PDF.");
      setMessage(null);
    } finally {
      setExtracting(false);
    }
  }

  async function save() {
    setBusy(true);
    setError(null);
    setMessage(null);
    try {
      const next = await saveInsurancePolicy({ ...draft, id: editingId || undefined });
      setPolicies(next);
      startNew();
      setMessage("Policy saved. Its premium and investment value are now connected to your financial data.");
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Unable to save policy.");
    } finally {
      setBusy(false);
    }
  }

  async function remove(id: string) {
    if (!window.confirm("Remove this policy and its linked insurance asset/expense?")) return;
    setBusy(true);
    setError(null);
    try {
      setPolicies(await removeInsurancePolicy(id));
      if (editingId === id) startNew();
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Unable to remove policy.");
    } finally {
      setBusy(false);
    }
  }

  return <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm sm:p-5 space-y-4">
    <div className="border-b border-slate-100 pb-3">
      <h3 className="text-lg font-extrabold text-navy-900">Insurance &amp; Protection</h3>
      <p className="mt-0.5 text-xs text-slate-500">Protection plus investment-linked insurance, connected to Moneywheel without double-counting.</p>
    </div>

    {loading ? <p className="text-sm text-slate-500">Loading policies...</p> : policies.length > 0 && <div className="space-y-2">
      {policies.map((policy) => <div key={policy.id} className="flex flex-col gap-2 rounded-xl border border-slate-200 p-3 sm:flex-row sm:items-center sm:justify-between">
        <div><p className="text-sm font-bold text-navy-900">{policy.policyName}</p><p className="text-xs text-slate-500">{policy.insurer || "Insurer not specified"}{policy.policyType ? ` · ${policy.policyType}` : ""}</p><div className="mt-1 flex flex-wrap gap-1.5 text-[10px] text-slate-600"><span className="rounded-full bg-slate-100 px-2 py-1">Sum assured ₹{policy.sumAssured || "0"}</span><span className="rounded-full bg-slate-100 px-2 py-1">Value ₹{policy.currentValue || "0"}</span></div></div>
        <div className="flex gap-2"><button type="button" onClick={() => edit(policy)} className="rounded-lg border border-slate-200 px-3 py-1.5 text-xs font-bold text-slate-700">Edit</button><button type="button" onClick={() => void remove(policy.id)} disabled={busy} className="rounded-lg border border-red-200 px-3 py-1.5 text-xs font-bold text-red-600">Remove</button></div>
      </div>)}
    </div>}

    <div className="rounded-xl border border-dashed border-teal-200 bg-teal-50/40 p-4">
      <p className="text-sm font-bold text-navy-900">Policy document (optional)</p>
      <p className="mt-1 text-xs text-slate-500">Upload a PDF to extract policy details locally. You still review and confirm everything before it is saved.</p>
      <input type="file" accept="application/pdf" disabled={extracting || busy} onChange={(e) => void handlePdf(e.target.files?.[0])} className="mt-3 block w-full text-xs text-slate-600 file:mr-3 file:rounded-lg file:border-0 file:bg-navy-900 file:px-3 file:py-2 file:text-xs file:font-bold file:text-white" />
    </div>

    <div className="grid gap-3 sm:grid-cols-2">
      <div><label className="mb-1 block text-[11px] font-bold uppercase tracking-wider text-slate-500">Policy Name</label><input value={draft.policyName} onChange={(e) => set("policyName", e.target.value)} placeholder="e.g. LIC Jeevan Anand" className={field} /></div>
      <div><label className="mb-1 block text-[11px] font-bold uppercase tracking-wider text-slate-500">Insurer</label><input value={draft.insurer} onChange={(e) => set("insurer", e.target.value)} placeholder="e.g. LIC" className={field} /></div>
      <div><label className="mb-1 block text-[11px] font-bold uppercase tracking-wider text-slate-500">Policy Number <span className="font-normal text-slate-400">(optional)</span></label><input value={draft.policyNumber} onChange={(e) => set("policyNumber", e.target.value)} placeholder="Policy number" className={field} /></div>
      <div><label className="mb-1 block text-[11px] font-bold uppercase tracking-wider text-slate-500">Policy Type</label><select value={draft.policyType} onChange={(e) => set("policyType", e.target.value)} className={field}><option value="">Select type</option>{policyTypes.map((type) => <option key={type}>{type}</option>)}</select></div>
      <div><label className="mb-1 block text-[11px] font-bold uppercase tracking-wider text-slate-500">Premium</label><input type="number" min="0" value={draft.premium} onChange={(e) => set("premium", e.target.value)} placeholder="0" className={field} /></div>
      <div><label className="mb-1 block text-[11px] font-bold uppercase tracking-wider text-slate-500">Premium Frequency</label><select value={draft.premiumFrequency} onChange={(e) => set("premiumFrequency", e.target.value as InsurancePolicyDraft["premiumFrequency"])} className={field}>{frequencyOptions.map((frequency) => <option key={frequency}>{frequency}</option>)}</select></div>
      <div><label className="mb-1 block text-[11px] font-bold uppercase tracking-wider text-slate-500">Sum Assured</label><input type="number" min="0" value={draft.sumAssured} onChange={(e) => set("sumAssured", e.target.value)} placeholder="0" className={field} /></div>
      <div><label className="mb-1 block text-[11px] font-bold uppercase tracking-wider text-slate-500">Current / Surrender Value</label><input type="number" min="0" value={draft.currentValue} onChange={(e) => set("currentValue", e.target.value)} placeholder="0" className={field} /></div>
      <div><label className="mb-1 block text-[11px] font-bold uppercase tracking-wider text-slate-500">Maturity Date</label><input type="date" value={draft.maturityDate} onChange={(e) => set("maturityDate", e.target.value)} className={field} /></div>
      <div><label className="mb-1 block text-[11px] font-bold uppercase tracking-wider text-slate-500">Maturity Value <span className="font-normal text-slate-400">(optional)</span></label><input type="number" min="0" value={draft.maturityValue} onChange={(e) => set("maturityValue", e.target.value)} placeholder="0" className={field} /></div>
    </div>

    {(message || error) && <p className={`rounded-lg px-3 py-2 text-xs font-semibold ${error ? "bg-red-50 text-red-700" : "bg-teal-50 text-teal-800"}`}>{error || message}</p>}

    <div className="flex items-center justify-between border-t border-slate-100 pt-3"><span className="text-[11px] text-slate-500">Premium becomes an Insurance expense; current value becomes an asset only when &gt; ₹0.</span><div className="flex gap-2"><button type="button" onClick={startNew} className="rounded-lg border border-slate-200 px-4 py-2 text-[11px] font-bold uppercase tracking-wider text-slate-700">{editingId ? "Cancel" : "Clear"}</button><button type="button" disabled={busy || extracting || !draft.policyName.trim()} onClick={() => void save()} className="rounded-lg bg-navy-900 px-4 py-2 text-[11px] font-bold uppercase tracking-wider text-white disabled:opacity-50">{busy ? "Saving..." : editingId ? "Update Policy" : "Save Policy"}</button></div></div>
    {policies.length > 0 && !editingId && <button type="button" onClick={startNew} className="inline-flex rounded-xl border border-teal-600 bg-white px-4 py-2.5 text-xs font-bold text-teal-700 hover:bg-teal-50">+ Add another policy</button>}
  </div>;
}
