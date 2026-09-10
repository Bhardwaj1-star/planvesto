import {
  createDiaryEntry as apiCreateDiaryEntry,
  getDiaryEntries as apiGetDiaryEntries,
  getFinancialDecisions as apiGetFinancialDecisions,
  getPlanningUnitId,
  type DiaryEntry as ApiDiaryEntry,
  type FinancialDecision as ApiFinancialDecision,
} from "../api/diary";

export type ContextualPrompt = {
  id: string;
  triggerText: string;
  question: string;
  actionText: string;
  actionHref: string;
  type: "goal" | "strategy" | "liability" | "investment" | "budget";
};

export type DiaryEntry = ApiDiaryEntry;
export type FinancialDecision = ApiFinancialDecision;

export async function getDiaryEntries(): Promise<DiaryEntry[]> {
  const planningUnitId = getPlanningUnitId();
  if (!planningUnitId) throw new Error("Planning unit is not available. Please complete onboarding first.");
  return apiGetDiaryEntries(planningUnitId);
}

export async function saveDiaryEntry(entry: Omit<DiaryEntry, "id" | "displayDate" | "planningUnitId" | "createdAt" | "updatedAt"> & { id?: string }): Promise<DiaryEntry> {
  if (entry.id) throw new Error("Updating diary entries is not supported by this compatibility method. Use the Diary API directly.");
  const planningUnitId = getPlanningUnitId();
  if (!planningUnitId) throw new Error("Planning unit is not available. Please complete onboarding first.");
  return apiCreateDiaryEntry({ planningUnitId, date: entry.date, title: entry.title, content: entry.content, tags: entry.tags, prompts: entry.prompts, followUpNote: entry.followUpNote, isImportant: entry.isImportant });
}

export async function getDecisions(): Promise<FinancialDecision[]> {
  const planningUnitId = getPlanningUnitId();
  if (!planningUnitId) throw new Error("Planning unit is not available. Please complete onboarding first.");
  return apiGetFinancialDecisions(planningUnitId);
}

export const recordDecision = undefined;
export const deleteDiaryEntry = undefined;
