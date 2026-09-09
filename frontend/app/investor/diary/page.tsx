"use client";

import { useEffect, useState } from "react";
import {
  getDiaryEntries,
  getDecisions,
  type DiaryEntry,
  type FinancialDecision,
} from "../../../lib/diary/diaryStore";
import DiaryBook from "../../../components/diary/DiaryBook";
import DecisionHistoryView from "../../../components/diary/DecisionHistoryView";
import WriteEntryModal from "../../../components/diary/WriteEntryModal";
import InvestorProfileMenu from "../../../components/InvestorProfileMenu";

export default function InvestorDiaryPage() {
  const [activeTab, setActiveTab] = useState<"diary" | "decisions">("diary");
  const [entries, setEntries] = useState<DiaryEntry[]>([]);
  const [decisions, setDecisions] = useState<FinancialDecision[]>([]);
  const [isWriteModalOpen, setIsWriteModalOpen] = useState(false);

  // Load entries and decisions
  useEffect(() => {
    setEntries(getDiaryEntries());
    setDecisions(getDecisions());
  }, []);

  const handleEntrySaved = (newEntry: DiaryEntry) => {
    setEntries((prev) => [newEntry, ...prev.filter((e) => e.id !== newEntry.id)]);
    setDecisions(getDecisions());
  };

  return (
    <main className="min-h-screen bg-[#f6f8fb] text-slate-900 pb-20">
      {/* Top Bar Header */}
      <header className="border-b border-slate-200 bg-white shadow-xs">
        <div className="mx-auto flex min-h-[80px] max-w-6xl flex-col sm:flex-row sm:items-center sm:justify-between gap-4 px-4 sm:px-6 lg:px-8 py-4 sm:py-0">
          <div>
            <div className="flex items-center gap-2">
              <span className="inline-flex items-center rounded-md bg-teal-50 px-2 py-0.5 text-xs font-semibold text-teal-700 ring-1 ring-inset ring-teal-600/20">
                Memory Layer
              </span>
              <p className="text-xs font-bold uppercase tracking-[0.15em] text-slate-400">
                Planvesto Investor Diary
              </p>
            </div>
            <h1 className="mt-1 font-serif text-2xl sm:text-3xl font-extrabold tracking-tight text-slate-950">
              Investor Diary
            </h1>
          </div>

          <div className="flex flex-wrap items-center gap-3">
            {/* View Switcher: Diary | Decision History */}
            <div className="inline-flex rounded-xl bg-slate-100 p-1 text-xs font-bold shadow-inner">
              <button
                type="button"
                onClick={() => setActiveTab("diary")}
                className={`rounded-lg px-3.5 py-2 transition ${
                  activeTab === "diary"
                    ? "bg-white text-navy-900 shadow-sm"
                    : "text-slate-600 hover:text-slate-900"
                }`}
              >
                📖 Diary (Open Book)
              </button>
              <button
                type="button"
                onClick={() => setActiveTab("decisions")}
                className={`rounded-lg px-3.5 py-2 transition ${
                  activeTab === "decisions"
                    ? "bg-white text-navy-900 shadow-sm"
                    : "text-slate-600 hover:text-slate-900"
                }`}
              >
                ⏱ Decision History ({decisions.length})
              </button>
            </div>

            {/* Write in Diary CTA Button */}
            <button
              type="button"
              onClick={() => setIsWriteModalOpen(true)}
              className="inline-flex items-center gap-2 rounded-xl bg-navy-900 px-4 py-2.5 text-xs font-bold uppercase tracking-wider text-white shadow-sm transition hover:bg-navy-800 focus:outline-none focus:ring-4 focus:ring-teal-100"
            >
              <span className="text-sm">✎</span>
              <span>Write in Diary</span>
            </button>

            {/* Profile Popover Menu */}
            <InvestorProfileMenu />
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8 pt-8">
        {activeTab === "diary" ? (
          <div>
            <div className="mb-6 text-center max-w-xl mx-auto">
              <p className="text-xs font-serif italic text-slate-500">
                “A personal financial diary that remembers your aspirations, reflects your decisions, and connects your thoughts to real strategy.”
              </p>
            </div>

            <DiaryBook
              entries={entries}
              onWriteNew={() => setIsWriteModalOpen(true)}
            />
          </div>
        ) : (
          <DecisionHistoryView decisions={decisions} />
        )}
      </div>

      {/* Write Entry Modal */}
      <WriteEntryModal
        isOpen={isWriteModalOpen}
        onClose={() => setIsWriteModalOpen(false)}
        onEntrySaved={handleEntrySaved}
      />
    </main>
  );
}
