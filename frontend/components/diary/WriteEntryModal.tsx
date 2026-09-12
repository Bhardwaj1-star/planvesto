"use client";

import { useState } from "react";
import { saveDiaryEntry, type DiaryEntry } from "../../lib/diary/diaryStore";

type WriteEntryModalProps = {
  isOpen: boolean;
  onClose: () => void;
  onEntrySaved: (entry: DiaryEntry) => void;
};

export default function WriteEntryModal({ isOpen, onClose, onEntrySaved }: WriteEntryModalProps) {
  const today = new Date().toISOString().slice(0, 10);
  const [date, setDate] = useState(today);
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [tagInput, setTagInput] = useState("");
  const [tags, setTags] = useState<string[]>([]);
  const [followUpNote, setFollowUpNote] = useState("");
  const [error, setError] = useState("");

  if (!isOpen) return null;

  const handleAddTag = () => {
    const trimmed = tagInput.trim();
    if (trimmed && !tags.includes(trimmed)) {
      setTags([...tags, trimmed]);
      setTagInput("");
    }
  };

  const handleRemoveTag = (tagToRemove: string) => {
    setTags(tags.filter((t) => t !== tagToRemove));
  };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!content.trim()) {
      setError("Please write down your thoughts, questions, or financial notes.");
      return;
    }

    try {
      const saved = await saveDiaryEntry({
        date,
        title: title.trim() || undefined,
        content,
        tags,
        prompts: [],
        followUpNote: followUpNote.trim() || undefined,
        isImportant: false,
      });

      onEntrySaved(saved);
      setTitle("");
      setContent("");
      setTags([]);
      setFollowUpNote("");
      setError("");
      onClose();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to save diary entry.");
    }
  };

  // Detect intelligent prompt keywords dynamically
  const hasHomeKeyword = /home|house|flat|apartment|property/i.test(content) && /50|lakh|crore|cr|down payment/i.test(content);
  const hasLoanKeyword = /loan|debt|emi|prepay|interest/i.test(content);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-navy-950/60 p-4 backdrop-blur-sm">
      <div className="relative w-full max-w-2xl overflow-hidden rounded-3xl border border-[#e8dfcf] bg-[#fdfbf7] shadow-2xl transition-all" role="dialog" aria-modal="true" aria-labelledby="modal-title">
        <div className="absolute left-0 top-0 bottom-0 w-3 bg-gradient-to-r from-[#2c1810] via-[#4a2e1b] to-transparent opacity-80" />
        <div className="flex items-center justify-between border-b border-[#ebdccb] px-6 py-5 sm:px-8 bg-[#f9f5ed]">
          <div className="flex items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-navy-900 text-white shadow-sm"><span aria-hidden="true">✎</span></div>
            <div><p className="text-[11px] font-bold uppercase tracking-widest text-[#8c6d48]">Financial Memory</p><h3 id="modal-title" className="font-serif text-xl font-bold text-[#1f242e]">Write in your Investor Diary</h3></div>
          </div>
          <button type="button" onClick={onClose} className="flex h-8 w-8 items-center justify-center rounded-lg text-slate-400 hover:bg-[#eae0d2] hover:text-slate-700" aria-label="Close modal">✕</button>
        </div>

        <form onSubmit={handleSave} className="p-6 sm:p-8 space-y-5 max-h-[80vh] overflow-y-auto">
          <div className="grid gap-4 sm:grid-cols-3">
            <div><label htmlFor="entry-date" className="block text-xs font-bold uppercase tracking-wider text-slate-500 mb-1.5">Date</label><input id="entry-date" type="date" value={date} max={today} onChange={(e) => setDate(e.target.value)} className="w-full rounded-xl border border-[#d8c8b4] bg-white px-3.5 py-2.5 text-sm font-semibold text-slate-900 shadow-sm focus:border-teal-600 focus:outline-none focus:ring-2 focus:ring-teal-600/20" /></div>
            <div className="sm:col-span-2"><label htmlFor="entry-title" className="block text-xs font-bold uppercase tracking-wider text-slate-500 mb-1.5">Title / Subject <span className="font-normal text-slate-400">(optional)</span></label><input id="entry-title" type="text" value={title} onChange={(e) => setTitle(e.target.value)} placeholder="e.g. Planning for our 3BHK flat down payment" className="w-full rounded-xl border border-[#d8c8b4] bg-white px-3.5 py-2.5 text-sm font-semibold text-slate-900 placeholder:text-slate-400 shadow-sm focus:border-teal-600 focus:outline-none focus:ring-2 focus:ring-teal-600/20" /></div>
          </div>

          <div>
            <div className="flex items-center justify-between mb-1.5"><label htmlFor="entry-content" className="block text-xs font-bold uppercase tracking-wider text-slate-500">Your Thoughts, Decisions, or Notes</label><span className="text-[11px] font-medium text-[#8c6d48]">Freeform text · No forced fields</span></div>
            <div className="relative rounded-2xl border border-[#d8c8b4] bg-[#fffefc] shadow-inner p-4 focus-within:border-teal-600 focus-within:ring-2 focus-within:ring-teal-600/20"><textarea id="entry-content" rows={7} value={content} onChange={(e) => { setContent(e.target.value); if (error) setError(""); }} placeholder="Write anything on your mind: goals, family discussions, loan repayment plans, questions, or financial decisions you're considering..." className="w-full resize-y bg-transparent text-sm leading-relaxed text-slate-800 placeholder:text-slate-400 focus:outline-none font-sans" /></div>
            {error && <p className="mt-1.5 text-xs font-medium text-red-600">{error}</p>}
          </div>

          {(hasHomeKeyword || hasLoanKeyword) && <div className="rounded-2xl border border-teal-200 bg-teal-50/70 p-3.5 text-xs text-teal-900 flex items-start gap-3 shadow-xs"><div className="flex h-6 w-6 shrink-0 items-center justify-center rounded-lg bg-teal-600 text-white font-bold text-[11px]">✦</div><div className="flex-1"><p className="font-bold">Intelligent Planvesto connection detected:</p><p className="mt-0.5 text-teal-800">{hasHomeKeyword ? "We noticed you mentioned a home purchase requirement. Planvesto will surface an action prompt on this diary page linking to Strategy Builder." : "We noticed you mentioned loan or debt obligations. Planvesto will provide quick liability check-ins."}</p></div></div>}

          <div className="grid gap-4 sm:grid-cols-2">
            <div><label className="block text-xs font-bold uppercase tracking-wider text-slate-500 mb-1.5">Topic Tags <span className="font-normal text-slate-400">(optional)</span></label><div className="flex gap-2"><input type="text" value={tagInput} onChange={(e) => setTagInput(e.target.value)} onKeyDown={(e) => { if (e.key === "Enter") { e.preventDefault(); handleAddTag(); } }} placeholder="e.g. Home, Savings, Bonus" className="w-full rounded-xl border border-[#d8c8b4] bg-white px-3 py-2 text-xs font-semibold text-slate-900 placeholder:text-slate-400" /><button type="button" onClick={handleAddTag} className="rounded-xl border border-[#d8c8b4] bg-[#f9f5ed] px-3 py-2 text-xs font-bold text-slate-700 hover:bg-[#ede3d3]">Add</button></div>{tags.length > 0 && <div className="mt-2 flex flex-wrap gap-1.5">{tags.map((t) => <span key={t} className="inline-flex items-center gap-1 rounded-md bg-[#eee4d5] px-2 py-0.5 text-[11px] font-semibold text-slate-700">#{t}<button type="button" onClick={() => handleRemoveTag(t)} className="text-slate-400 hover:text-slate-700 font-bold ml-0.5">×</button></span>)}</div>}</div>
            <div><label htmlFor="entry-followup" className="block text-xs font-bold uppercase tracking-wider text-slate-500 mb-1.5">Follow-up reminder <span className="font-normal text-slate-400">(optional)</span></label><input id="entry-followup" type="text" value={followUpNote} onChange={(e) => setFollowUpNote(e.target.value)} placeholder="e.g. Recheck circle rate in 3 months" className="w-full rounded-xl border border-[#d8c8b4] bg-white px-3.5 py-2 text-xs font-semibold text-slate-900 placeholder:text-slate-400" /></div>
          </div>

          <div className="flex items-center justify-end gap-3 pt-3 border-t border-[#ebdccb]"><button type="button" onClick={onClose} className="rounded-xl px-4 py-2.5 text-xs font-bold uppercase tracking-wider text-slate-500 hover:text-slate-800">Cancel</button><button type="submit" className="inline-flex items-center gap-2 rounded-xl bg-navy-900 px-6 py-2.5 text-sm font-bold text-white shadow-md transition hover:bg-navy-800 focus:outline-none focus:ring-4 focus:ring-teal-100"><span>Commit to Diary</span><span aria-hidden="true">→</span></button></div>
        </form>
      </div>
    </div>
  );
}
