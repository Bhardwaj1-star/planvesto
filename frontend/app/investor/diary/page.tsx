"use client";

import { useEffect, useState } from "react";
import { getDiaryEntries, getDecisions, type DiaryEntry, type FinancialDecision } from "../../../lib/diary/diaryStore";
import BackendWriteEntryModal from "../../../components/diary/BackendWriteEntryModal";
import InvestorHeader from "../../../components/InvestorHeader";

function MoneyDiary({ entries, decisions }: { entries: DiaryEntry[]; decisions: FinancialDecision[] }) {
  const notes = entries.map((entry) => ({
    date: new Date(entry.createdAt),
    title: entry.title || "A note from your financial life",
    text: entry.content || "You added a note to your financial diary.",
    kind: "note",
  }));
  const decisionNotes = decisions.map((decision) => ({
    date: new Date(decision.createdAt),
    title: decision.title || "A financial decision",
    text: decision.summary || decision.notes || "A financial decision was recorded for future reference.",
    kind: "decision",
  }));
  const items = [...notes, ...decisionNotes].sort((a, b) => b.date.getTime() - a.date.getTime());

  if (!items.length) {
    return (
      <div className="mx-auto max-w-3xl rounded-[32px] border border-slate-200 bg-white px-8 py-16 text-center shadow-sm">
        <div className="text-4xl">📖</div>
        <h2 className="mt-5 font-serif text-2xl font-bold text-slate-800">Your financial story starts here.</h2>
        <p className="mx-auto mt-3 max-w-lg font-serif text-sm leading-7 text-slate-500">As things change in your financial life, this page will quietly keep track of what happened, what you decided, and what deserves your attention next.</p>
      </div>
    );
  }

  return (
    <section className="mx-auto max-w-3xl">
      <div className="mb-10 text-center">
        <p className="font-serif text-sm italic text-slate-500">A simple record of what has been happening with your money.</p>
        <h2 className="mt-2 font-serif text-3xl font-bold text-slate-800">My Money Diary</h2>
      </div>
      <div className="relative pl-7 sm:pl-10">
        <div className="absolute bottom-0 left-2 top-0 w-px bg-slate-200 sm:left-4" />
        <div className="space-y-8">
          {items.map((item, index) => (
            <article key={`${item.date.toISOString()}-${index}`} className="relative rounded-[28px] border border-slate-200 bg-white px-6 py-6 shadow-sm">
              <span className="absolute -left-[31px] top-7 h-3 w-3 rounded-full border-2 border-white bg-slate-400 shadow-sm sm:-left-[39px]" />
              <p className="font-serif text-xs italic text-slate-400">{item.date.toLocaleDateString("en-IN", { weekday: "long", day: "numeric", month: "long", year: "numeric" })}</p>
              <h3 className="mt-2 font-serif text-xl font-bold text-slate-800">{item.title}</h3>
              <p className="mt-3 font-serif text-[15px] leading-8 text-slate-600">{item.text}</p>
              {item.kind === "decision" && <p className="mt-4 text-[10px] font-bold uppercase tracking-[0.16em] text-slate-400">A decision remembered</p>}
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}

export default function InvestorDiaryPage() {
  const [entries, setEntries] = useState<DiaryEntry[]>([]);
  const [decisions, setDecisions] = useState<FinancialDecision[]>([]);
  const [isWriteModalOpen, setIsWriteModalOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadDiary = async () => {
    setLoading(true); setError(null);
    try {
      const [nextEntries, nextDecisions] = await Promise.all([getDiaryEntries(), getDecisions()]);
      setEntries(nextEntries); setDecisions(nextDecisions);
    } catch (err) { setError(err instanceof Error ? err.message : "Unable to load Investor Diary."); }
    finally { setLoading(false); }
  };

  useEffect(() => { void loadDiary(); }, []);
  const handleEntrySaved = async () => { setIsWriteModalOpen(false); await loadDiary(); };

  return (
    <main className="min-h-screen bg-[#f6f8fb] pb-20 text-slate-900">
      <InvestorHeader eyebrow="Your financial life" title="Investor Diary">
        <button type="button" onClick={() => setIsWriteModalOpen(true)} className="inline-flex items-center gap-2 rounded-xl bg-navy-900 px-4 py-2.5 text-xs font-bold uppercase tracking-wider text-white shadow-sm transition hover:bg-navy-800"><span className="text-sm">✎</span><span>Write in Diary</span></button>
      </InvestorHeader>
      <div className="mx-auto max-w-6xl px-4 pt-8 sm:px-6 lg:px-8">
        {loading ? <div className="mx-auto max-w-3xl rounded-[32px] border border-slate-200 bg-white p-12 text-center shadow-sm"><p className="font-serif text-lg font-bold">Opening your financial memory…</p></div> : error ? <div className="mx-auto max-w-3xl rounded-2xl border border-red-200 bg-red-50 p-6 text-sm text-red-700"><p className="font-bold">Unable to load Investor Diary</p><p className="mt-1">{error}</p><button type="button" onClick={() => void loadDiary()} className="mt-4 rounded-xl bg-navy-900 px-4 py-2 text-xs font-bold text-white">Retry</button></div> : <MoneyDiary entries={entries} decisions={decisions} />}
      </div>
      <BackendWriteEntryModal isOpen={isWriteModalOpen} onClose={() => setIsWriteModalOpen(false)} onEntrySaved={handleEntrySaved} />
    </main>
  );
}
