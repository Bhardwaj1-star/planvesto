/**
 * Budgeting Data Layer
 * 
 * Fetches real income, expenses, and liabilities data from Supabase,
 * derives budget items dynamically, and persists user-defined budget limits.
 */

import { supabase } from "../supabase";

// ============================================================================
// Types
// ============================================================================

export type NeedWantClassification = "Need" | "Want";

export interface BudgetLimitRow {
  budget_limit_id: string;
  planning_unit_id: string;
  category: string;
  classification: NeedWantClassification;
  budget_monthly: number;
  created_at: string;
  updated_at: string;
}

export interface BudgetItem {
  id: string;
  category: string;
  classification: NeedWantClassification;
  budgetMonthly: number;
  actualMonthly: number;
  varianceMonthly: number;
  status: "Under Budget" | "On Track" | "Over Budget";
  icon: string;
  percentageOfBudget: number;
}

export interface BudgetOverview {
  totalIncomeMonthly: number;
  totalExpensesMonthly: number;
  surplusMonthly: number;
  savingsTargetMonthly: number;
  savingsTargetPercentage: number;
  needsTotalMonthly: number;
  wantsTotalMonthly: number;
}

export interface BudgetData {
  overview: BudgetOverview;
  items: BudgetItem[];
  planningUnitId: string;
}

// ============================================================================
// Icon mapping for expense categories
// ============================================================================

const CATEGORY_ICONS: Record<string, string> = {
  "Housing": "🏠",
  "Food & Groceries": "🛒",
  "Utilities": "⚡",
  "Transportation": "🚗",
  "Education": "📚",
  "Healthcare": "🩺",
  "Insurance": "🛡️",
  "Debt Payments": "💳",
  "Family Support": "👨‍👩‍👧",
  "Travel": "✈️",
  "Entertainment": "🎬",
  "Shopping": "🛍️",
  "Other": "📦",
  // EMI/Liability categories
  "Home Loan": "🏠",
  "Car Loan": "🚗",
  "Personal Loan": "💳",
  "Education Loan": "🎓",
  "Business Loan": "💼",
  "Credit Card": "💳",
};

// Default classification for expense categories
const DEFAULT_CLASSIFICATIONS: Record<string, NeedWantClassification> = {
  "Housing": "Need",
  "Food & Groceries": "Need",
  "Utilities": "Need",
  "Transportation": "Need",
  "Education": "Need",
  "Healthcare": "Need",
  "Insurance": "Need",
  "Debt Payments": "Need",
  "Family Support": "Need",
  "Travel": "Want",
  "Entertainment": "Want",
  "Shopping": "Want",
  "Other": "Want",
  // EMI/Liability categories
  "Home Loan": "Need",
  "Car Loan": "Need",
  "Personal Loan": "Need",
  "Education Loan": "Need",
  "Business Loan": "Need",
  "Credit Card": "Need",
};

// ============================================================================
// Helpers
// ============================================================================

function getPlanningUnitId(): string | null {
  if (typeof window === "undefined") return null;
  return window.localStorage.getItem("planvesto-planning-unit-id");
}

/** Normalize an amount to monthly based on frequency */
function toMonthly(amount: number, frequency: string): number {
  switch (frequency) {
    case "Annual":
      return amount / 12;
    case "Quarterly":
      return amount / 3;
    case "Monthly":
    default:
      return amount;
  }
}

function deriveStatus(budget: number, actual: number): BudgetItem["status"] {
  if (budget === 0) return actual === 0 ? "On Track" : "Over Budget";
  const variance = actual - budget;
  const threshold = budget * 0.05; // 5% tolerance
  if (variance > threshold) return "Over Budget";
  if (variance < -threshold) return "Under Budget";
  return "On Track";
}

// ============================================================================
// Data Loading
// ============================================================================

export async function loadBudgetData(): Promise<BudgetData | null> {
  const planningUnitId = getPlanningUnitId();
  if (!planningUnitId) return null;

  // Fetch all data in parallel
  const [incomeRes, expensesRes, liabilitiesRes, budgetLimitsRes] = await Promise.all([
    supabase
      .from("income")
      .select("amount, frequency")
      .eq("planning_unit_id", planningUnitId),
    supabase
      .from("expenses")
      .select("expense_id, expense_type, amount, frequency")
      .eq("planning_unit_id", planningUnitId),
    supabase
      .from("liabilities")
      .select("liability_id, liability_name, emi_amount, frequency")
      .eq("planning_unit_id", planningUnitId),
    supabase
      .from("budget_limits")
      .select("*")
      .eq("planning_unit_id", planningUnitId),
  ]);

  if (incomeRes.error) throw incomeRes.error;
  if (expensesRes.error) throw expensesRes.error;
  if (liabilitiesRes.error) throw liabilitiesRes.error;
  // budget_limits table may not exist yet; treat error as empty
  const budgetLimitsData = budgetLimitsRes.error ? [] : (budgetLimitsRes.data || []);

  const incomeRows = incomeRes.data || [];
  const expenseRows = expensesRes.data || [];
  const liabilityRows = liabilitiesRes.data || [];

  // 1. Calculate total monthly income
  const totalIncomeMonthly = incomeRows.reduce(
    (sum, row) => sum + toMonthly(row.amount, row.frequency),
    0,
  );

  // 2. Aggregate expenses by category (monthly)
  const expenseByCategory = new Map<string, number>();
  for (const row of expenseRows) {
    const cat = row.expense_type || "Other";
    const monthly = toMonthly(row.amount, row.frequency);
    expenseByCategory.set(cat, (expenseByCategory.get(cat) || 0) + monthly);
  }

  // 3. Aggregate liabilities as EMI outflows by liability type
  // Extract the primary type from liability_name (e.g. "Home Loan - HDFC" → "Home Loan")
  const liabilityTypes = ["Home Loan", "Car Loan", "Personal Loan", "Education Loan", "Business Loan", "Credit Card", "Other"] as const;
  for (const row of liabilityRows) {
    if (!row.emi_amount || row.emi_amount <= 0) continue;
    const name = row.liability_name || "";
    const matchedType = liabilityTypes.find(
      (t) => name === t || name.startsWith(`${t} - `),
    ) || "Debt Payments";
    const monthly = toMonthly(row.emi_amount, row.frequency || "Monthly");
    expenseByCategory.set(matchedType, (expenseByCategory.get(matchedType) || 0) + monthly);
  }

  // 4. Build budget limits lookup
  const limitsMap = new Map<string, BudgetLimitRow>();
  for (const row of budgetLimitsData) {
    limitsMap.set(row.category, row as BudgetLimitRow);
  }

  // 5. Determine all categories that have actual spend or a budget limit
  const allCategories = new Set<string>();
  for (const cat of expenseByCategory.keys()) allCategories.add(cat);
  for (const row of budgetLimitsData) allCategories.add(row.category);

  // 6. Calculate total actual expenses for percentage computation
  const totalActual = Array.from(expenseByCategory.values()).reduce((a, b) => a + b, 0);

  // 7. Build budget items (only categories with non-zero data)
  const items: BudgetItem[] = [];
  for (const category of allCategories) {
    const actual = Math.round(expenseByCategory.get(category) || 0);
    const limit = limitsMap.get(category);
    const budget = limit ? limit.budget_monthly : 0;
    const classification: NeedWantClassification = limit
      ? (limit.classification as NeedWantClassification)
      : (DEFAULT_CLASSIFICATIONS[category] || "Want");

    // Hide categories with zero actual AND zero budget
    if (actual === 0 && budget === 0) continue;

    const variance = actual - budget;
    const status = deriveStatus(budget, actual);
    const percentage = totalActual > 0 ? Math.round((actual / totalActual) * 100) : 0;

    items.push({
      id: limit?.budget_limit_id || `derived-${category.toLowerCase().replace(/[^a-z0-9]/g, "-")}`,
      category,
      classification,
      budgetMonthly: budget,
      actualMonthly: actual,
      varianceMonthly: variance,
      status,
      icon: CATEGORY_ICONS[category] || "📦",
      percentageOfBudget: percentage,
    });
  }

  // Sort: Needs first, then Wants; within each group sort by actual descending
  items.sort((a, b) => {
    if (a.classification !== b.classification) {
      return a.classification === "Need" ? -1 : 1;
    }
    return b.actualMonthly - a.actualMonthly;
  });

  // 8. Build overview
  const totalExpensesMonthly = Math.round(totalActual);
  const surplusMonthly = Math.round(totalIncomeMonthly - totalExpensesMonthly);
  const savingsTargetPercentage = 30;
  const savingsTargetMonthly = Math.round(totalIncomeMonthly * (savingsTargetPercentage / 100));

  const needsTotalMonthly = Math.round(
    items
      .filter((i) => i.classification === "Need")
      .reduce((s, i) => s + i.actualMonthly, 0),
  );
  const wantsTotalMonthly = Math.round(
    items
      .filter((i) => i.classification === "Want")
      .reduce((s, i) => s + i.actualMonthly, 0),
  );

  return {
    overview: {
      totalIncomeMonthly: Math.round(totalIncomeMonthly),
      totalExpensesMonthly,
      surplusMonthly,
      savingsTargetMonthly,
      savingsTargetPercentage,
      needsTotalMonthly,
      wantsTotalMonthly,
    },
    items,
    planningUnitId,
  };
}

// ============================================================================
// Budget Limits Persistence (Upsert)
// ============================================================================

export async function saveBudgetLimits(
  planningUnitId: string,
  items: Array<{
    category: string;
    classification: NeedWantClassification;
    budgetMonthly: number;
  }>,
): Promise<void> {
  for (const item of items) {
    const { error } = await supabase
      .from("budget_limits")
      .upsert(
        {
          planning_unit_id: planningUnitId,
          category: item.category,
          classification: item.classification,
          budget_monthly: item.budgetMonthly,
          updated_at: new Date().toISOString(),
        },
        { onConflict: "planning_unit_id,category" },
      );
    if (error) throw error;
  }
}

// ============================================================================
// Realtime Subscription
// ============================================================================

type Cleanup = () => void;

export function subscribeToBudgetChanges(
  planningUnitId: string,
  onChange: () => void,
): Cleanup {
  const channel = supabase.channel(`budgeting:${planningUnitId}`);
  let timer: ReturnType<typeof setTimeout> | null = null;

  const refresh = () => {
    if (timer) clearTimeout(timer);
    timer = setTimeout(onChange, 350);
  };

  // Listen to changes on tables that affect the budget view
  for (const table of ["income", "expenses", "liabilities", "budget_limits"] as const) {
    channel.on(
      "postgres_changes",
      {
        event: "*",
        schema: "public",
        table,
        filter: `planning_unit_id=eq.${planningUnitId}`,
      },
      refresh,
    );
  }

  channel.subscribe();

  return () => {
    if (timer) clearTimeout(timer);
    void supabase.removeChannel(channel);
  };
}
