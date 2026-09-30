"use client";

import { useEffect, useMemo, useState } from "react";
import { getDiaryEntries, getDecisions, type DiaryEntry, type FinancialDecision } from "../../../lib/diary/diaryStore";
import BackendWriteEntryModal from "../../../components/diary/BackendWriteEntryModal";
import InvestorHeader from "../../../components/InvestorHeader";

type TimelineItem = { id: string; date: string; title: string; text: string; label: string; };

function humanizeDecision(decision: FinancialDecision): TimelineItem {
  const source = `${decision.source} ${decision.title}`.toLowerCase();
  const category = decision.category;
  if (source.includes("strategy") || category === "Strategy") return { id: `decision-${decision.id}`, date: decision.date, title: "You changed your financial strategy", text: "A change was made to the way this part of your financial plan is being handled. The earlier choice has been kept here so you can look back on it later.", label: "A change in your plan" };
  if (category === "Goal") return { id: `decision-${decision.id}`, date: decision.date, title: "You changed one of your goals", text: "Something about a financial goal was updated. This note keeps the change in your financial story.", label: "A goal changed" };
  if (category === "Allocation") return { id: `decision-${decision.id}`, date: decision.date, title: "You changed how your money is arranged", text: "The way money is being allocated across your plan changed. The previous decision remains part of your history.", label: "Money arrangement changed" };
  if (category === "Investment") return { id: `decision-${decision.id}`, date: decision.date, title: "You made an investment decision", text: "An investment-related decision was recorded in your financial story.", label: "Investment decision" };
  if (category === "Debt") return { id: `decision-${decision.id}`, date: decision.date, title: "You made a change related to debt", text: "A debt-related decision was recorded so you can see how your financial journey has changed over time.", label: "Debt decision" };
  return { id: `decision-${decision.id}`, date: decision.date, title: "You made a financial decision", text: "A decision was recorded in your financial story for future reference.", label: "A decision remembered" };
}

function entryToItem(entry: DiaryEntry): TimelineItem { return { id: `entry-${entry.id}`, date: entry.date, title: entry.title || "A note from your financial life", text: entry.content || "You added a note to your financial diary.", label: entry.isImportant ? "Something worth remembering" : "A note from you" }; }

function formatDate(value: string) { return new Date(value).toLocaleDateString("en-IN", { weekday: "long", day: "numeric", month: "long", year: "numeric" }); }

export default function InvestorDiaryPage() {
  const [entries, setEntries] = useState<DiaryEntry[]>([]);
  const [decisions, setDecisions] = useState<FinancialDecision[]>([]);
  const [isWriteModalOpen, setIsWriteModalOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadDiary = async () => { setLoading(true); setError(null); try { const [nextEntries, nextDecisions] = await Promise.all([getDiaryEntries(), getDecisions()]); setEntries(nextEntries); setDecisions(nextDecisions); } catch (err) { setError(err instanceof Error ? err.message : "Unable to load Investor Diary."); } finally { setLoading(false); } };
  useEffect(() => { void loadDiary(); }, []);
  const timeline = useMemo(() => { const raw = [...entries.map(entryToItem), ...decisions.map(humanizeDecision)]; const unique = new Map<string, TimelineItem>(); for (const item of raw) { const day = new Date(item.date).toISOString().slice(0, 10); const key = `${day}|${item.title}|${item.text}`; if (!unique.has(key)) unique.set(key, item); } return [...unique.values()].sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime()).slice(0, 30); }, [entries, decisions]);
  const handleEntrySaved = async () => { setIsWriteModalOpen(false); await loadDiary(); };

  return (
    <main className="min-h-screen bg-[#f6f8fb] pb-20 text-slate-900">
      <InvestorHeader eyebrow="Your financial life" title="Investor Diary">
        <button type="button" onClick={() => setIsWriteModalOpen(true)} className="inline-flex items-center gap-2 rounded-xl bg-navy-900 px-5 py-3 text-xs font-bold uppercase tracking-wider text-white shadow-sm transition hover:bg-navy-800"><span className="text-sm">✎</span><span>Write in Diary</span></button>
      </InvestorHeader>
      <div className="mx-auto max-w-5xl px-4 pt-9 sm:px-6 lg:px-8">
        <div className="mb-10 text-center"><p className="font-serif text-sm italic text-slate-500">A simple record of what has been happening with your money.</p><h2 className="mt-2 font-serif text-3xl font-bold text-slate-800">My Money Diary</h2></div>
        {loading ? <div className="rounded-[32px] border border-slate-200 bg-white p-12 text-center shadow-sm"><p className="font-serif text-lg font-bold">Opening your financial diary…</p></div> : error ? <div className="mx-auto max-w-3xl rounded-2xl border border-red-200 bg-red-50 p-6 text-sm text-red-700"><p className="font-bold">Unable to open your diary</p><p className="mt-1">{error}</p><button type="button" onClick={() => void loadDiary()} className="mt-4 rounded-xl bg-navy-900 px-4 py-2 text-xs font-bold text-white">Try again</button></div> : !timeline.length ? <div className="rounded-[32px] border border-slate-200 bg-white p-12 text-center shadow-sm"><p className="font-serif text-xl font-bold text-slate-800">Your financial story starts here.</p><p className="mx-auto mt-3 max-w-md font-serif text-sm leading-7 text-slate-500">As things change in your financial life, they will quietly find their place here. You can also write your own note anytime.</p><button type="button" onClick={() => setIsWriteModalOpen(true)} className="mt-6 rounded-xl bg-navy-900 px-5 py-3 text-xs font-bold text-white">Write your first note</button></div> : <div className="relative mx-auto max-w-4xl"><div className="absolute bottom-0 left-[7px] top-0 w-px bg-slate-200 sm:left-[10px]" /><div className="space-y-8">{timeline.map(item => <article key={item.id} className="relative pl-8 sm:pl-12"><span className="absolute left-0 top-8 h-4 w-4 rounded-full border-4 border-[#f6f8fb] bg-slate-400 shadow-sm" /><div className="rounded-[28px] border border-slate-200 bg-white px-6 py-6 shadow-sm sm:px-8"><p className="font-serif text-xs italic text-slate-400">{formatDate(item.date)}</p><h3 className="mt-2 font-serif text-xl font-bold text-slate-800">{item.title}</h3><p className="mt-3 max-w-3xl font-serif text-sm leading-7 text-slate-600">{item.text}</p><p className="mt-5 text-[10px] font-bold uppercase tracking-[0.2em] text-slate-400">{item.label}</p></div></article>)}</div></div>}
      </div>
      <BackendWriteEntryModal isOpen={isWriteModalOpen} onClose={() => setIsWriteModalOpen(false)} onEntrySaved={handleEntrySaved} />
    </main>
  );
}
