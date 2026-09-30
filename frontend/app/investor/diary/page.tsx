"use client";

import { useEffect, useState } from "react";
import { getDiaryEntries, getDecisions, type DiaryEntry, type FinancialDecision } from "../../../lib/diary/diaryStore";
import DiaryBook from "../../../components/diary/DiaryBook";
import DiaryActionPlan from "../../../components/diary/DiaryActionPlan";
import DecisionHistoryView from "../../../components/diary/DecisionHistoryView";
import BackendWriteEntryModal from "../../../components/diary/BackendWriteEntryModal";
import InvestorHeader from "../../../components/InvestorHeader";

export default function InvestorDiaryPage() {
  const [activeTab, setActiveTab] = useState<"diary" | "decisions">("diary");
  const [entries, setEntries] = useState<DiaryEntry[]>([]);
  const [decisions, setDecisions] = useState<FinancialDecision[]>([]);
  const [isWriteModalOpen, setIsWriteModalOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadDiary = async () => {
    setLoading(true);
    setError(null);
    try {
      const [nextEntries, nextDecisions] = await Promise.all([getDiaryEntries(), getDecisions()]);
      setEntries(nextEntries);
      setDecisions(nextDecisions);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to load Investor Diary.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { void loadDiary(); }, []);

  const handleEntrySaved = async () => {
    setIsWriteModalOpen(false);
    await loadDiary();
  };

  return (
    <main className="min-h-screen bg-[#f6f8fb] text-slate-900 pb-20">
      <InvestorHeader eyebrow="Memory Layer" title="Investor Diary">
        <div className="flex flex-wrap items-center gap-3">
          <div className="inline-flex rounded-xl bg-slate-100 p-1 text-xs font-bold shadow-inner">
            <button type="button" onClick={() => setActiveTab("diary")} className={`rounded-lg px-3.5 py-2 transition ${activeTab === "diary" ? "bg-white text-navy-900 shadow-sm" : "text-slate-600 hover:text-slate-900"}`}>📖 Diary (Open Book)</button>
            <button type="button" onClick={() => setActiveTab("decisions")} className={`rounded-lg px-3.5 py-2 transition ${activeTab === "decisions" ? "bg-white text-navy-900 shadow-sm" : "text-slate-600 hover:text-slate-900"}`}>⏱ Decision History ({decisions.length})</button>
          </div>
          <button type="button" onClick={() => setIsWriteModalOpen(true)} className="inline-flex items-center gap-2 rounded-xl bg-navy-900 px-4 py-2.5 text-xs font-bold uppercase tracking-wider text-white shadow-sm transition hover:bg-navy-800 focus:outline-none focus:ring-4 focus:ring-teal-100"><span className="text-sm">✎</span><span>Write in Diary</span></button>
        </div>
      </InvestorHeader>

      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8 pt-8">
        {loading ? (
          <div className="mx-auto max-w-5xl rounded-[32px] border border-slate-200 bg-white p-10 text-center shadow-sm"><p className="font-serif text-lg font-bold">Opening your financial memory…</p></div>
        ) : error ? (
          <div className="mx-auto max-w-3xl rounded-2xl border border-red-200 bg-red-50 p-6 text-sm text-red-700"><p className="font-bold">Unable to load Investor Diary</p><p className="mt-1">{error}</p><button type="button" onClick={() => void loadDiary()} className="mt-4 rounded-xl bg-navy-900 px-4 py-2 text-xs font-bold text-white">Retry</button></div>
        ) : activeTab === "diary" ? (
          <div>
            <div className="mb-6 text-center max-w-xl mx-auto"><p className="text-xs font-serif italic text-slate-500">“A personal financial diary that remembers your aspirations, reflects your decisions, and connects your thoughts to real strategy.”</p></div>
            <DiaryBook entries={entries} onWriteNew={() => setIsWriteModalOpen(true)} />
            <DiaryActionPlan />
          </div>
        ) : (
          <DecisionHistoryView decisions={decisions} />
        )}
      </div>

      <BackendWriteEntryModal isOpen={isWriteModalOpen} onClose={() => setIsWriteModalOpen(false)} onEntrySaved={handleEntrySaved} />
    </main>
  );
}
