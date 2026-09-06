import { formatCurrency, getAnnualIncome } from "../../../lib/onboarding/income/income";
import type { IncomeSource } from "../../../lib/onboarding/income/types";
import IncomeSourceCard from "./IncomeSourceCard";

type Props = { sources: IncomeSource[]; onEdit: (source: IncomeSource) => void; onRemove: (id: string) => void };

export default function IncomeSummary({ sources, onEdit, onRemove }: Props) {
  const annualIncome = getAnnualIncome(sources);
  if (sources.length === 0) return <div className="rounded-[28px] border border-dashed border-slate-300 bg-white px-6 py-10 text-center sm:px-8"><div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-teal-50 text-teal-700" aria-hidden="true">$</div><h2 className="mt-4 text-lg font-extrabold text-navy-900">No income sources added yet</h2><p className="mx-auto mt-2 max-w-md text-sm leading-6 text-slate-500">Add your income sources so your plan can reflect the full picture. You can continue without adding one right now.</p></div>;

  return <div className="space-y-4"><div className="grid gap-3 sm:grid-cols-2"><div className="rounded-2xl border border-navy-900 bg-navy-900 p-5 text-white"><p className="text-xs font-bold uppercase tracking-[0.14em] text-teal-200">Total annual income</p><p className="mt-2 text-2xl font-extrabold">{formatCurrency(annualIncome)}</p></div><div className="rounded-2xl border border-teal-200 bg-teal-50 p-5 text-navy-900"><p className="text-xs font-bold uppercase tracking-[0.14em] text-teal-700">Total monthly income</p><p className="mt-2 text-2xl font-extrabold">{formatCurrency(annualIncome / 12)}</p><p className="mt-1 text-xs text-slate-500">Annual income divided by 12</p></div></div><div className="space-y-3">{sources.map((source) => <IncomeSourceCard key={source.id} source={source} onEdit={() => onEdit(source)} onRemove={() => onRemove(source.id)} />)}</div></div>;
}