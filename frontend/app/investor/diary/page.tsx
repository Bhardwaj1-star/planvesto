"use client";

import { useEffect, useState } from "react";
import { getDiaryEntries, getDecisions, type DiaryEntry, type FinancialDecision } from "../../../lib/diary/diaryStore";
import DiaryBook from "../../../components/diary/DiaryBook";
import DecisionHistoryView from "../../../components/diary/DecisionHistoryView";
import BackendWriteEntryModal from "../../../components/diary/BackendWriteEntryModal";
import InvestorHeader from "../../../components/InvestorHeader";

function MonitoringView({ entries, decisions }: { entries: DiaryEntry[]; decisions: FinancialDecision[] }) {
  const notes = entries.slice(0, 8).map((entry) => ({
    date: new Date(entry.created_at).toLocaleDateString("en-IN", { day: "numeric", month: "short", year: "numeric" }),
    title: entry.title || "A note from your financial life",
    text: entry.content || "You added a new note to your financial diary.",
  }));
  const decisionNotes = decisions.slice(0, 8).map((decision) => ({
    date: new Date(decision.created_at).toLocaleDateString("en-IN", { day: "numeric", month: "short", year: "numeric" }),
    title: decision.title || "A decision was recorded",
    text: decision.summary || decision.description || "A financial decision was recorded and kept for future reference.",
  }));
  const items = [...notes, ...decisionNotes].sort((a, b) => b.date.localeCompare(a.date));

  return (
    <section className="mx-auto max-w-4xl">
      <div className="mb-8 text-center">
        <p className="font-serif text-sm italic text-slate-500">A quieter view of what has been happening with your money.</p>
        <h2 className="mt-2 font-serif text-2xl font-bold text-slate-800">Your Financial Notes</h2>
      </div>
      {items.length === 0 ? (
        <div className="rounded-[32px] border border-slate-200 bg-white p-12 text-center shadow-sm"><p className="font-serif text-lg font-bold">Nothing to note yet.</p><p className="mt-2 text-sm text-slate-500">As you make decisions and write notes, your financial story will appear here.</p></div>
      ) : (
        <div className="space-y-5">
          {items.map((item, index) => (
            <article key={`${item.date}-${index}`} className="rounded-[28px] border border-slate-200 bg-white px-6 py-5 shadow-sm">
              <p className="font-serif text-xs italic text-slate-400">{item.date}</p>
              <h3 className="mt-1 font-serif text-lg font-bold text-slate-800">{item.title}</h3>
              <p className="mt-2 font-serif text-sm leading-7 text-slate-600">{item.text}</p>
            </article>
          ))}
        </div>
      )}
    </section>
  );
}

export default function InvestorDiaryPage() {
  const [activeTab, setActiveTab] = useState<"diary" | "monitoring" | "decisions">("diary");
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
    <main className="min-h-screen bg-[#f6f8fb] text-slate-900 pb-20">
      <InvestorHeader eyebrow="Memory Layer" title="Investor Diary">
        <div className="flex flex-wrap items-center gap-3">
          <div className="inline-flex rounded-xl bg-slate-100 p-1 text-xs font-bold shadow-inner">
            <button type="button" onClick={() => setActiveTab("diary")} className={`rounded-lg px-3.5 py-2 transition ${activeTab === "diary" ? "bg-white text-navy-900 shadow-sm" : "text-slate-600 hover:text-slate-900"}`}>📖 Diary</button>
            <button type="button" onClick={() => setActiveTab("monitoring")} className={`rounded-lg px-3.5 py-2 transition ${activeTab === "monitoring" ? "bg-white text-navy-900 shadow-sm" : "text-slate-600 hover:text-slate-900"}`}>◷ My Money</button>
            <button type="button" onClick={() => setActiveTab("decisions")} className={`rounded-lg px-3.5 py-2 transition ${activeTab === "decisions" ? "bg-white text-navy-900 shadow-sm" : "text-slate-600 hover:text-slate-900"}`}>⏱ Decisions</button>
          </div>
          <button type="button" onClick={() => setIsWriteModalOpen(true)} className="inline-flex items-center gap-2 rounded-xl bg-navy-900 px-4 py-2.5 text-xs font-bold uppercase tracking-wider text-white shadow-sm transition hover:bg-navy-800"><span className="text-sm">✎</span><span>Write in Diary</span></button>
        </div>
      </InvestorHeader>

      <div className="mx-auto max-w-6xl px-4 pt-8 sm:px-6 lg:px-8">
        {loading ? <div className="mx-auto max-w-5xl rounded-[32px] border border-slate-200 bg-white p-10 text-center shadow-sm"><p className="font-serif text-lg font-bold">Opening your financial memory…</p></div> : error ? <div className="mx-auto max-w-3xl rounded-2xl border border-red-200 bg-red-50 p-6 text-sm text-red-700"><p className="font-bold">Unable to load Investor Diary</p><p className="mt-1">{error}</p><button type="button" onClick={() => void loadDiary()} className="mt-4 rounded-xl bg-navy-900 px-4 py-2 text-xs font-bold text-white">Retry</button></div> : activeTab === "diary" ? <div><div className="mb-6 mx-auto max-w-xl text-center"><p className="text-xs font-serif italic text-slate-500">“Your financial life, remembered like a diary.”</p></div><DiaryBook entries={entries} onWriteNew={() => setIsWriteModalOpen(true)} /></div> : activeTab === "monitoring" ? <MonitoringView entries={entries} decisions={decisions} /> : <DecisionHistoryView decisions={decisions} />}
      </div>
      <BackendWriteEntryModal isOpen={isWriteModalOpen} onClose={() => setIsWriteModalOpen(false)} onEntrySaved={handleEntrySaved} />
    </main>
  );
}
