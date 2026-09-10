"use client";

import { useState } from "react";
import { createDiaryEntry } from "../../lib/api/diary";
import { type DiaryEntry } from "../../lib/diary/diaryStore";

type Props = { isOpen: boolean; onClose: () => void; onEntrySaved: (entry: DiaryEntry) => void };

export default function BackendWriteEntryModal({ isOpen, onClose, onEntrySaved }: Props) {
  const today = new Date().toISOString().slice(0, 10);
  const [date, setDate] = useState(today);
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [tagInput, setTagInput] = useState("");
  const [tags, setTags] = useState<string[]>([]);
  const [followUpNote, setFollowUpNote] = useState("");
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);

  if (!isOpen) return null;
  const addTag = () => { const tag = tagInput.trim(); if (tag && !tags.includes(tag)) setTags((current) => [...current, tag]); setTagInput(""); };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!content.trim()) { setError("Please write down your thoughts, questions, or financial notes."); return; }
    setSaving(true); setError("");
    try {
      const saved = await createDiaryEntry({ planningUnitId: (await import("../../lib/api/diary")).getPlanningUnitId() || (() => { throw new Error("Planning unit is not available. Please complete onboarding first."); })(), date, title: title.trim() || undefined, content: content.trim(), tags, followUpNote: followUpNote.trim() || undefined });
      onEntrySaved(saved); setTitle(""); setContent(""); setTags([]); setFollowUpNote(""); onClose();
    } catch (err) { setError(err instanceof Error ? err.message : "Unable to save diary entry."); }
    finally { setSaving(false); }
  };

  const hasHomeKeyword = /home|house|flat|apartment|property/i.test(content) && /50|lakh|crore|cr|down payment/i.test(content);
  const hasLoanKeyword = /loan|debt|emi|prepay|interest/i.test(content);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-navy-950/60 p-4 backdrop-blur-sm">
      <div className="relative w-full max-w-2xl overflow-hidden rounded-3xl border border-[#e8dfcf] bg-[#fdfbf7] shadow-2xl" role="dialog" aria-modal="true">
        <div className="absolute left-0 top-0 bottom-0 w-3 bg-gradient-to-r from-[#2c1810] via-[#4a2e1b] to-transparent opacity-80" />
        <div className="flex items-center justify-between border-b border-[#ebdccb] bg-[#f9f5ed] px-6 py-5 sm:px-8"><div><p className="text-[11px] font-bold uppercase tracking-widest text-[#8c6d48]">Financial Memory</p><h3 className="font-serif text-xl font-bold text-[#1f242e]">Write in your Investor Diary</h3></div><button type="button" onClick={onClose} className="flex h-8 w-8 items-center justify-center rounded-lg text-slate-400 hover:bg-[#eae0d2]">✕</button></div>
        <form onSubmit={handleSave} className="max-h-[80vh] space-y-5 overflow-y-auto p-6 sm:p-8">
          <div className="grid gap-4 sm:grid-cols-3"><div><label className="mb-1.5 block text-xs font-bold uppercase tracking-wider text-slate-500">Date</label><input type="date" value={date} max={today} onChange={(e) => setDate(e.target.value)} className="w-full rounded-xl border border-[#d8c8b4] bg-white px-3.5 py-2.5 text-sm font-semibold" /></div><div className="sm:col-span-2"><label className="mb-1.5 block text-xs font-bold uppercase tracking-wider text-slate-500">Title / Subject <span className="font-normal text-slate-400">(optional)</span></label><input type="text" value={title} onChange={(e) => setTitle(e.target.value)} placeholder="e.g. Planning for our 3BHK flat down payment" className="w-full rounded-xl border border-[#d8c8b4] bg-white px-3.5 py-2.5 text-sm font-semibold" /></div></div>
          <div><div className="mb-1.5 flex items-center justify-between"><label className="block text-xs font-bold uppercase tracking-wider text-slate-500">Your Thoughts, Decisions, or Notes</label><span className="text-[11px] text-[#8c6d48]">Freeform text · No forced fields</span></div><textarea rows={7} value={content} onChange={(e) => { setContent(e.target.value); setError(""); }} placeholder="Write anything on your mind: goals, family discussions, loan repayment plans, questions, or financial decisions you're considering..." className="w-full rounded-2xl border border-[#d8c8b4] bg-[#fffefc] p-4 text-sm leading-relaxed outline-none focus:border-teal-600" />{error && <p className="mt-1.5 text-xs font-medium text-red-600">{error}</p>}</div>
          {(hasHomeKeyword || hasLoanKeyword) && <div className="rounded-2xl border border-teal-200 bg-teal-50/70 p-3.5 text-xs text-teal-900"><p className="font-bold">Intelligent Planvesto connection detected</p><p className="mt-1">{hasHomeKeyword ? "Home purchase reference detected." : "Loan or debt reference detected."}</p></div>}
          <div className="grid gap-4 sm:grid-cols-2"><div><label className="mb-1.5 block text-xs font-bold uppercase tracking-wider text-slate-500">Topic Tags <span className="font-normal text-slate-400">(optional)</span></label><div className="flex gap-2"><input value={tagInput} onChange={(e) => setTagInput(e.target.value)} onKeyDown={(e) => { if (e.key === "Enter") { e.preventDefault(); addTag(); } }} placeholder="e.g. Home, Savings, Bonus" className="w-full rounded-xl border border-[#d8c8b4] bg-white px-3 py-2 text-xs" /><button type="button" onClick={addTag} className="rounded-xl border border-[#d8c8b4] px-3 py-2 text-xs font-bold">Add</button></div>{tags.length > 0 && <div className="mt-2 flex flex-wrap gap-1.5">{tags.map((tag) => <span key={tag} className="rounded-md bg-[#eee4d5] px-2 py-0.5 text-[11px] font-semibold">#{tag} <button type="button" onClick={() => setTags(tags.filter((t) => t !== tag))}>×</button></span>)}</div>}</div><div><label className="mb-1.5 block text-xs font-bold uppercase tracking-wider text-slate-500">Follow-up reminder <span className="font-normal text-slate-400">(optional)</span></label><input value={followUpNote} onChange={(e) => setFollowUpNote(e.target.value)} placeholder="e.g. Recheck circle rate in 3 months" className="w-full rounded-xl border border-[#d8c8b4] bg-white px-3.5 py-2 text-xs" /></div></div>
          <div className="flex justify-end gap-3 border-t border-[#ebdccb] pt-3"><button type="button" onClick={onClose} className="rounded-xl px-4 py-2.5 text-xs font-bold text-slate-500">Cancel</button><button type="submit" disabled={saving} className="rounded-xl bg-navy-900 px-6 py-2.5 text-sm font-bold text-white disabled:opacity-50">{saving ? "Saving…" : "Commit to Diary →"}</button></div>
        </form>
      </div>
    </div>
  );
}
