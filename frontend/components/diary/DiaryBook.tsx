"use client";

import { useState } from "react";
import Link from "next/link";
import { type DiaryEntry } from "../../lib/diary/diaryStore";

type DiaryBookProps = {
  entries: DiaryEntry[];
  onWriteNew: () => void;
  onDeleteEntry?: (id: string) => void;
};

export default function DiaryBook({ entries, onWriteNew }: DiaryBookProps) {
  const [currentSpreadIndex, setCurrentSpreadIndex] = useState(0);
  const [isFlipping, setIsFlipping] = useState<"next" | "prev" | null>(null);

  const totalSpreads = Math.max(1, entries.length);
  const currentEntry = entries[currentSpreadIndex] || null;

  const handleNextPage = () => {
    if (currentSpreadIndex < totalSpreads - 1) {
      setIsFlipping("next");
      setTimeout(() => {
        setCurrentSpreadIndex((prev) => prev + 1);
        setIsFlipping(null);
      }, 200);
    }
  };

  const handlePrevPage = () => {
    if (currentSpreadIndex > 0) {
      setIsFlipping("prev");
      setTimeout(() => {
        setCurrentSpreadIndex((prev) => prev - 1);
        setIsFlipping(null);
      }, 200);
    }
  };

  return (
    <div className="relative mx-auto w-full max-w-5xl select-none">
      {/* Silk Ribbon Bookmark hanging from the top edge */}
      <div className="pointer-events-none absolute -top-4 left-1/2 -translate-x-1/2 z-30 flex flex-col items-center">
        <div className="h-10 w-7 bg-gradient-to-b from-[#8b1e1e] to-[#b32b2b] shadow-md relative">
          {/* Ribbon chevron cut */}
          <div className="absolute -bottom-2 left-0 w-0 h-0 border-l-[14px] border-l-[#b32b2b] border-r-[14px] border-r-[#b32b2b] border-b-[8px] border-b-transparent" />
        </div>
      </div>

      {/* Book Outer Leather Binding Shell */}
      <div className="relative rounded-[32px] p-2.5 sm:p-4 bg-gradient-to-b from-[#221711] via-[#1a110c] to-[#120a06] shadow-2xl border border-[#3d2a1f]/70">
        {/* Subtle leather texture embossing & golden corner accents */}
        <div className="absolute top-3 left-3 h-5 w-5 border-t-2 border-l-2 border-[#d4af37]/40 rounded-tl-sm pointer-events-none" />
        <div className="absolute top-3 right-3 h-5 w-5 border-t-2 border-r-2 border-[#d4af37]/40 rounded-tr-sm pointer-events-none" />
        <div className="absolute bottom-3 left-3 h-5 w-5 border-b-2 border-l-2 border-[#d4af37]/40 rounded-bl-sm pointer-events-none" />
        <div className="absolute bottom-3 right-3 h-5 w-5 border-b-2 border-r-2 border-[#d4af37]/40 rounded-br-sm pointer-events-none" />

        {/* Paper Book Block */}
        <div className="relative overflow-hidden rounded-[24px] bg-[#fcf9f2] border border-[#e5dcd0] shadow-inner">
          {/* Central Book Spine & Crease Shadow (Desktop) */}
          <div className="hidden lg:block pointer-events-none absolute top-0 bottom-0 left-1/2 w-16 -translate-x-1/2 z-20 bg-gradient-to-r from-transparent via-black/[0.08] to-transparent" />
          <div className="hidden lg:block pointer-events-none absolute top-0 bottom-0 left-1/2 w-[1px] -translate-x-1/2 z-20 bg-[#d8ccbe]" />

          {/* Two Facing Pages Container */}
          <div
            className={`grid grid-cols-1 lg:grid-cols-2 min-h-[580px] lg:min-h-[620px] transition-opacity duration-200 ${
              isFlipping ? "opacity-60 scale-[0.995]" : "opacity-100 scale-100"
            }`}
          >
            {/* ============================================================== */}
            {/* LEFT PAGE: Raw Freeform Investor Entry                          */}
            {/* ============================================================== */}
            <div className="relative flex flex-col justify-between p-6 sm:p-8 lg:p-10 border-b lg:border-b-0 lg:border-r border-[#ebdccb] bg-[#fdfbf7]">
              {/* Left Page Header */}
              <div>
                <div className="flex items-center justify-between border-b border-[#ebdccb] pb-3 text-xs text-[#8c6d48]">
                  <span className="font-serif italic font-medium tracking-wide">Planvesto Financial Memory</span>
                  <span className="font-mono text-[11px] font-semibold text-slate-400">
                    Folio {currentSpreadIndex * 2 + 1}
                  </span>
                </div>

                {/* Entry Metadata */}
                {currentEntry ? (
                  <div className="mt-5">
                    <div className="flex flex-wrap items-center justify-between gap-2">
                      <p className="font-serif text-sm font-semibold tracking-wide text-[#7d5d36]">
                        {currentEntry.displayDate}
                      </p>
                      {currentEntry.isImportant && (
                        <span className="inline-flex items-center gap-1 rounded-full bg-amber-100 px-2.5 py-0.5 text-[10px] font-bold text-amber-900">
                          ★ Landmark Milestone
                        </span>
                      )}
                    </div>

                    {currentEntry.title && (
                      <h2 className="mt-2 font-serif text-2xl font-bold tracking-tight text-slate-900 sm:text-3xl">
                        {currentEntry.title}
                      </h2>
                    )}

                    {/* Entry Content (Freeform, lined paper aesthetic) */}
                    <div className="mt-5 space-y-4 text-sm sm:text-base leading-relaxed text-slate-800 font-sans whitespace-pre-line">
                      {currentEntry.content}
                    </div>

                    {/* Tags */}
                    {currentEntry.tags && currentEntry.tags.length > 0 && (
                      <div className="mt-6 flex flex-wrap gap-1.5 pt-4 border-t border-[#f0e6d8]">
                        {currentEntry.tags.map((tag) => (
                          <span
                            key={tag}
                            className="inline-flex items-center rounded-md bg-[#f3ece0] px-2.5 py-0.5 text-xs font-semibold text-[#665038]"
                          >
                            #{tag}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                ) : (
                  <div className="mt-16 text-center">
                    <p className="font-serif text-lg font-bold text-slate-700">Your diary is waiting</p>
                    <p className="mt-2 text-xs text-slate-500 max-w-sm mx-auto">
                      Write down any financial aspirations, major family discussions, investment observations, or debt payoff plans.
                    </p>
                    <button
                      type="button"
                      onClick={onWriteNew}
                      className="mt-6 inline-flex items-center gap-2 rounded-xl bg-navy-900 px-5 py-2.5 text-xs font-bold uppercase tracking-wider text-white shadow-sm hover:bg-navy-800"
                    >
                      + First Entry
                    </button>
                  </div>
                )}
              </div>

              {/* Left Page Footer Controls */}
              <div className="mt-8 flex items-center justify-between pt-4 border-t border-[#ebdccb]/60 text-xs">
                <button
                  type="button"
                  onClick={handlePrevPage}
                  disabled={currentSpreadIndex === 0}
                  className="inline-flex items-center gap-1.5 font-semibold text-[#8c6d48] hover:text-slate-900 disabled:opacity-30 disabled:cursor-not-allowed transition"
                  title="Previous page"
                >
                  <span aria-hidden="true">←</span>
                  <span>Previous Page</span>
                </button>
                <span className="font-serif text-slate-400 italic">
                  Entry {currentSpreadIndex + 1} of {totalSpreads}
                </span>
              </div>
            </div>

            {/* ============================================================== */}
            {/* RIGHT PAGE: Intelligent Financial Companion & Contextual Prompts*/}
            {/* ============================================================== */}
            <div className="relative flex flex-col justify-between p-6 sm:p-8 lg:p-10 bg-[#f9f5ed]">
              {/* Dog-ear corner fold on right top */}
              <button
                type="button"
                onClick={handleNextPage}
                disabled={currentSpreadIndex >= totalSpreads - 1}
                className="absolute top-0 right-0 w-8 h-8 bg-gradient-to-bl from-[#dfd0bd] to-transparent opacity-70 hover:opacity-100 transition cursor-pointer"
                title="Turn to next page"
              />

              {/* Right Page Header */}
              <div>
                <div className="flex items-center justify-between border-b border-[#ebdccb] pb-3 text-xs text-[#8c6d48]">
                  <div className="flex items-center gap-1.5">
                    <span className="flex h-2 w-2 rounded-full bg-teal-600" />
                    <span className="font-bold uppercase tracking-wider text-[10px]">
                      Intelligent Companion
                    </span>
                  </div>
                  <span className="font-mono text-[11px] font-semibold text-slate-400">
                    Folio {currentSpreadIndex * 2 + 2}
                  </span>
                </div>

                <div className="mt-5 space-y-6">
                  {/* Contextual Planvesto Prompts */}
                  {currentEntry?.prompts && currentEntry.prompts.length > 0 ? (
                    <div className="space-y-4">
                      <div className="flex items-center gap-2">
                        <span className="text-xs font-bold uppercase tracking-wider text-[#8c6d48]">
                          Contextual Planvesto Prompts
                        </span>
                      </div>

                      {currentEntry.prompts.map((prompt) => (
                        <div
                          key={prompt.id}
                          className="rounded-2xl border border-teal-300/80 bg-gradient-to-br from-teal-50/90 to-[#e8f7f4] p-5 shadow-sm"
                        >
                          <div className="flex items-start gap-3">
                            <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-xl bg-teal-600 text-white shadow-xs">
                              <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                              </svg>
                            </div>
                            <div className="flex-1">
                              <p className="text-xs font-bold uppercase tracking-wider text-teal-800">
                                Detected Reference
                              </p>
                              <p className="mt-1 font-serif text-base font-bold text-slate-900 leading-snug">
                                {prompt.question}
                              </p>
                              <div className="mt-4">
                                <Link
                                  href={prompt.actionHref}
                                  className="inline-flex items-center gap-2 rounded-xl bg-navy-900 px-4 py-2 text-xs font-bold text-white shadow-sm hover:bg-navy-800 transition"
                                >
                                  <span>{prompt.actionText}</span>
                                </Link>
                              </div>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="rounded-2xl border border-[#ebdccb] bg-[#fcf9f2] p-5">
                      <p className="font-serif text-sm font-bold text-slate-800">Financial Observation</p>
                      <p className="mt-1.5 text-xs leading-relaxed text-slate-600">
                        Writing regularly in your diary helps identify subconscious spending patterns, emotional investment reactions, and emerging family goals before they turn into pressure points.
                      </p>
                    </div>
                  )}

                  {/* Follow-up Note / Reminder */}
                  {currentEntry?.followUpNote && (
                    <div className="rounded-2xl border border-amber-200 bg-amber-50/70 p-4">
                      <div className="flex items-center gap-2 text-xs font-bold text-amber-900">
                        <span>⏰ Follow-up Reminder</span>
                      </div>
                      <p className="mt-1.5 text-xs leading-relaxed text-amber-950 font-medium">
                        {currentEntry.followUpNote}
                      </p>
                    </div>
                  )}

                  {/* Planvesto Strategy Integration Callout */}
                  <div className="rounded-2xl border border-dashed border-[#d8c8b4] p-4 bg-white/60">
                    <p className="text-xs font-bold uppercase tracking-wider text-slate-400">
                      Decision Layer Bridge
                    </p>
                    <p className="mt-1 text-xs text-slate-600 leading-relaxed">
                      Important decisions made through Strategy Builder or Goal Planner are chronologically indexed in your <strong>Decision History</strong> tab.
                    </p>
                  </div>
                </div>
              </div>

              {/* Right Page Footer Controls */}
              <div className="mt-8 flex items-center justify-between pt-4 border-t border-[#ebdccb]/60 text-xs">
                <button
                  type="button"
                  onClick={onWriteNew}
                  className="inline-flex items-center gap-1.5 font-bold text-teal-800 hover:text-teal-950"
                >
                  <span className="flex h-5 w-5 items-center justify-center rounded-md bg-teal-100 text-teal-800 text-xs">✎</span>
                  <span>Write new entry</span>
                </button>

                <button
                  type="button"
                  onClick={handleNextPage}
                  disabled={currentSpreadIndex >= totalSpreads - 1}
                  className="inline-flex items-center gap-1.5 font-semibold text-[#8c6d48] hover:text-slate-900 disabled:opacity-30 disabled:cursor-not-allowed transition"
                  title="Next page"
                >
                  <span>Next Page</span>
                  <span aria-hidden="true">→</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Book Bottom Page-Stack Edge (Physical 3D book thickness illusion) */}
      <div className="mx-6 h-2 rounded-b-xl bg-[#dcd0c0] shadow-sm border-t border-[#c5b5a2]" />
      <div className="mx-10 h-1.5 rounded-b-xl bg-[#c5b5a2] shadow-md" />
    </div>
  );
}
