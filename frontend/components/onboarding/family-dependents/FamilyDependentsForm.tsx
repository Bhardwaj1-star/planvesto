"use client";

import FamilyMemberForm from "./FamilyMemberForm";
import FamilySummary from "./FamilySummary";
import { useFamilyDependents } from "../../../hooks/onboarding/family-dependents/useFamilyDependents";

export default function FamilyDependentsForm() {
  const family = useFamilyDependents();

  return (
    <main className="login-grid min-h-screen bg-slate-25 text-slate-900">
      <header className="border-b border-slate-200 bg-white"><div className="mx-auto flex h-20 max-w-[1200px] items-center justify-between px-5 lg:px-8"><a href="/" className="flex items-center gap-2.5" aria-label="Planvesto Home"><div className="flex h-9 w-9 items-center justify-center rounded-xl bg-navy-900"><svg className="h-5 w-5 text-white" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M5 17L10 12L13 15L19 8M15 8H19V12" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" /></svg></div><span className="text-xl font-extrabold tracking-tight text-navy-900">planvesto</span></a><span className="text-sm font-semibold text-slate-500">Your financial plan</span></div></header>
      <div className="mx-auto w-full max-w-[1080px] px-5 py-10 lg:px-8 lg:py-16"><div className="grid gap-10 lg:grid-cols-[220px_minmax(0,1fr)] lg:gap-16">
        <aside className="lg:pt-4"><p className="text-xs font-bold uppercase tracking-[0.16em] text-teal-700">Onboarding</p><div className="mt-5 flex items-center gap-3 lg:block"><div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-teal-600 text-sm font-extrabold text-white ring-8 ring-teal-50">2</div><div className="lg:mt-4"><p className="text-sm font-bold text-navy-900">Family &amp; Dependents</p><p className="mt-1 text-xs text-slate-500">Step 2 of your plan</p></div></div><div className="mt-6 hidden border-l border-slate-200 pl-5 text-xs leading-5 text-slate-400 lg:block">The people in your life help shape the plan you build for the future.</div></aside>
        <section><div className="mb-8 max-w-2xl"><p className="text-xs font-bold uppercase tracking-[0.16em] text-teal-700">Family &amp; Dependents — Step 2</p><h1 className="mt-3 text-3xl font-extrabold tracking-tight text-navy-900 sm:text-4xl">Who is part of your financial life?</h1><p className="mt-3 text-sm leading-6 text-slate-500 sm:text-base">Financial decisions can affect the people you support today, as well as the people you plan to support in the future.</p></div>
          <div className="space-y-5"><FamilySummary members={family.members} onEdit={family.startEditing} onRemove={family.removeMember} />
            <FamilyMemberForm member={family.draft} errors={family.errors} isEditing={Boolean(family.editingMemberId)} onChange={family.updateDraft} onSave={family.saveMember} onCancel={family.cancelEditing} />
            <div className="flex flex-col-reverse items-stretch gap-4 pt-2 sm:flex-row sm:items-center sm:justify-between"><a href="/investor/onboarding/personal-information" className="text-center text-sm font-bold text-slate-500 underline decoration-slate-300 underline-offset-4 hover:text-navy-900 sm:text-left">&lt;- Back</a><button type="button" onClick={family.handleContinue} className="inline-flex items-center justify-center gap-2 rounded-xl bg-navy-900 px-6 py-3.5 text-sm font-bold text-white shadow-sm transition hover:bg-navy-800 focus:outline-none focus:ring-4 focus:ring-teal-100">Continue <span aria-hidden="true">-&gt;</span></button></div>
            {family.isComplete && <p className="rounded-xl border border-teal-200 bg-teal-50 px-4 py-3 text-sm font-semibold text-teal-700" role="status">Family information is complete for this session.</p>}
          </div>
        </section>
      </div></div>
    </main>
  );
}