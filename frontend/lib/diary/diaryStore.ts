export interface ContextualPrompt {
  id: string;
  triggerText: string;
  question: string;
  actionText: string;
  actionHref: string;
  type: "goal" | "strategy" | "liability" | "investment" | "budget";
}

export interface DiaryEntry {
  id: string;
  date: string; // ISO or YYYY-MM-DD
  displayDate: string; // e.g. "Thursday, September 3, 2026"
  title?: string;
  content: string;
  tags?: string[];
  prompts?: ContextualPrompt[];
  followUpNote?: string;
  isImportant?: boolean;
}

export interface FinancialDecision {
  id: string;
  date: string; // YYYY-MM
  displayDate: string; // e.g. "Sep 2026"
  fullDate: string; // e.g. "Sep 15, 2026"
  title: string;
  summary: string;
  category: "Strategy" | "Investment" | "Debt" | "Goal" | "Allocation";
  source: string; // e.g. "Strategy Builder", "Manual Note"
  metrics?: {
    target?: string;
    horizon?: string;
    monthlyInvestment?: string;
    previousMonthlyInvestment?: string;
    expectedReturn?: string;
  };
  notes?: string;
}

const DIARY_STORAGE_KEY = "planvesto_investor_diary_entries";
const DECISIONS_STORAGE_KEY = "planvesto_investor_diary_decisions";

// Initial realistic seed entries that bring the diary to life
const INITIAL_ENTRIES: DiaryEntry[] = [
  {
    id: "entry-1",
    date: "2026-06-14",
    displayDate: "Sunday, June 14, 2026",
    title: "A bigger home for the family",
    content: `Visited Sector 48 over the weekend to look at the 3BHK residential flats. The kids are growing up fast and having their own study space is becoming really important for Priya and me. 

Roughly ₹50 to 60 lakh will be required for the down payment and initial registry, factoring in the appreciation over the next 5 years. Need to see whether we can set aside ₹35,000 to ₹40,000 every month without cutting back on our annual vacations.

Should sit down with Planvesto to simulate whether our current mutual fund growth and equity SIPs can carry this goal.`,
    tags: ["Home Goal", "Real Estate", "Family"],
    prompts: [
      {
        id: "prompt-home-goal",
        triggerText: "₹50 lakh home goal",
        question: "You mentioned a ₹50 lakh home goal. Want to complete the numbers and build a strategy?",
        actionText: "Build Strategy →",
        actionHref: "/investor/strategy-builder",
        type: "strategy",
      },
    ],
    followUpNote: "Check property circle rates in Sector 48 before year-end.",
    isImportant: true,
  },
  {
    id: "entry-2",
    date: "2026-07-22",
    displayDate: "Wednesday, July 22, 2026",
    title: "Annual performance bonus & loan prepayment",
    content: `Received ₹2,50,000 after-tax performance bonus from work today! 

Was tempted to put it all into an aggressive flexi-cap index fund, but the car loan EMI (₹14,200/mo at 8.8% interest) is still weighing on our monthly cash flow. 

Decided to split it pragmatically:
• ₹1,00,000 kept into our liquid emergency reserve.
• ₹1,50,000 directed towards principal prepayment on the car loan.

This should bring our loan tenure down by 14 months and immediately free up surplus cash flow.`,
    tags: ["Bonus", "Debt Prepayment", "Cash Flow"],
    prompts: [
      {
        id: "prompt-car-loan",
        triggerText: "prepayment on car loan",
        question: "Prepaying ₹1.5L will save approximately ₹21,400 in total interest. Want to update your liabilities?",
        actionText: "Update Liabilities →",
        actionHref: "/investor/financial-state",
        type: "liability",
      },
    ],
    followUpNote: "Review updated bank amortization schedule after payment reflects.",
  },
  {
    id: "entry-3",
    date: "2026-08-18",
    displayDate: "Tuesday, August 18, 2026",
    title: "Insurance review & Aarav's higher education",
    content: `Did an annual review of our pure term cover today. ₹1.5 Crore sum assured is sufficient for now given our current outstanding liabilities and family expense burn rate.

However, started calculating the inflation on international tuition for Aarav's undergrad (10 years away). Even at 7% education inflation, a 4-year degree will likely cost ₹45-50 Lakhs. 

Need to start a dedicated equity child-education basket. Even ₹15,000 per month starting this year will compound substantially over a decade.`,
    tags: ["Education", "Insurance", "Long-term"],
    prompts: [
      {
        id: "prompt-education-goal",
        triggerText: "Aarav's higher education",
        question: "Map out Aarav's education timeline and target in Goal Planner?",
        actionText: "Open Goal Planner →",
        actionHref: "/investor/goal-planner",
        type: "goal",
      },
    ],
  },
  {
    id: "entry-4",
    date: "2026-09-04",
    displayDate: "Friday, September 4, 2026",
    title: "Home Strategy finalized",
    content: `Ran the complete optimization in Strategy Builder for our Home Goal today. Selected the Balanced Capital Growth route:
• Target corpus: ₹50,00,000
• Horizon: 5 years
• Monthly SIP: ₹35,000

Feeling much more grounded having this written down and committed into our plan. Knowing where every rupee goes takes away the ambient anxiety of big life milestones.`,
    tags: ["Milestone", "Strategy Confirmed"],
    prompts: [
      {
        id: "prompt-strategy-check",
        triggerText: "Balanced Capital Growth",
        question: "Your Home Goal strategy is active. Check your financial health score with this allocation?",
        actionText: "View Health Score →",
        actionHref: "/investor/health-score",
        type: "strategy",
      },
    ],
    isImportant: true,
  },
];

// Initial realistic decision history
const INITIAL_DECISIONS: FinancialDecision[] = [
  {
    id: "dec-1",
    date: "2026-09",
    displayDate: "Sep 2026",
    fullDate: "Sep 4, 2026",
    title: "Home Goal Strategy created",
    summary: "Committed to 5-year balanced growth pathway for the ₹50L family residence down-payment.",
    category: "Strategy",
    source: "Strategy Builder",
    metrics: {
      target: "₹50,00,000",
      horizon: "5 years",
      monthlyInvestment: "₹35,000",
      expectedReturn: "11.5% CAGR",
    },
    notes: "Allocated across diversified equity and debt funds to manage drawdown risk in year 4 and 5.",
  },
  {
    id: "dec-2",
    date: "2026-10",
    displayDate: "Oct 2026",
    fullDate: "Oct 1, 2026",
    title: "Monthly investment increased ₹35K → ₹45K",
    summary: "Stepped up monthly SIP allocation following annual compensation increment.",
    category: "Investment",
    source: "Investor Diary Note",
    metrics: {
      previousMonthlyInvestment: "₹35,000",
      monthlyInvestment: "₹45,000",
      target: "₹50,00,000",
    },
    notes: "Accelerates projected goal attainment by approximately 9 months.",
  },
];

export function getDiaryEntries(): DiaryEntry[] {
  if (typeof window === "undefined") return INITIAL_ENTRIES;
  try {
    const raw = localStorage.getItem(DIARY_STORAGE_KEY);
    if (!raw) {
      localStorage.setItem(DIARY_STORAGE_KEY, JSON.stringify(INITIAL_ENTRIES));
      return INITIAL_ENTRIES;
    }
    return JSON.parse(raw);
  } catch {
    return INITIAL_ENTRIES;
  }
}

export function saveDiaryEntry(entry: Omit<DiaryEntry, "id" | "displayDate"> & { id?: string }): DiaryEntry {
  const entries = getDiaryEntries();
  const dateObj = new Date(entry.date || Date.now());
  const displayDate = dateObj.toLocaleDateString("en-US", {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
  });

  // Automated intelligent prompt detection based on freeform text
  const prompts: ContextualPrompt[] = [...(entry.prompts || [])];
  const lower = entry.content.toLowerCase();

  if ((lower.includes("home") || lower.includes("house") || lower.includes("flat")) && (lower.includes("50") || lower.includes("lakh") || lower.includes("cr"))) {
    if (!prompts.some((p) => p.id === "prompt-home-goal")) {
      prompts.push({
        id: "prompt-home-goal",
        triggerText: "home goal",
        question: "You mentioned a home goal requirement. Want to test realistic numbers in Strategy Builder?",
        actionText: "Build Strategy →",
        actionHref: "/investor/strategy-builder",
        type: "strategy",
      });
    }
  }

  if (lower.includes("loan") || lower.includes("debt") || lower.includes("emi") || lower.includes("interest")) {
    if (!prompts.some((p) => p.id === "prompt-loan")) {
      prompts.push({
        id: "prompt-loan",
        triggerText: "loan obligations",
        question: "Managing liabilities efficiently boosts investable surplus. View your liability breakdown?",
        actionText: "Check Liabilities →",
        actionHref: "/investor/financial-state",
        type: "liability",
      });
    }
  }

  if (lower.includes("sip") || lower.includes("invest") || lower.includes("mutual fund") || lower.includes("stocks")) {
    if (!prompts.some((p) => p.id === "prompt-invest")) {
      prompts.push({
        id: "prompt-invest",
        triggerText: "monthly investments",
        question: "Review your portfolio asset allocation and savings rate in Budgeting?",
        actionText: "Open Budgeting →",
        actionHref: "/investor/budgeting",
        type: "budget",
      });
    }
  }

  const newEntry: DiaryEntry = {
    id: entry.id || `entry-${Date.now()}`,
    date: entry.date,
    displayDate,
    title: entry.title?.trim() || undefined,
    content: entry.content.trim(),
    tags: entry.tags && entry.tags.length > 0 ? entry.tags : ["General Note"],
    prompts: prompts.length > 0 ? prompts : undefined,
    followUpNote: entry.followUpNote?.trim() || undefined,
    isImportant: entry.isImportant,
  };

  const updated = entry.id
    ? entries.map((item) => (item.id === entry.id ? newEntry : item))
    : [newEntry, ...entries];

  // Sort chronological descending (latest first)
  updated.sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());

  if (typeof window !== "undefined") {
    localStorage.setItem(DIARY_STORAGE_KEY, JSON.stringify(updated));
  }

  return newEntry;
}

export function deleteDiaryEntry(id: string): void {
  const entries = getDiaryEntries().filter((e) => e.id !== id);
  if (typeof window !== "undefined") {
    localStorage.setItem(DIARY_STORAGE_KEY, JSON.stringify(entries));
  }
}

export function getDecisions(): FinancialDecision[] {
  if (typeof window === "undefined") return INITIAL_DECISIONS;
  try {
    const raw = localStorage.getItem(DECISIONS_STORAGE_KEY);
    if (!raw) {
      localStorage.setItem(DECISIONS_STORAGE_KEY, JSON.stringify(INITIAL_DECISIONS));
      return INITIAL_DECISIONS;
    }
    return JSON.parse(raw);
  } catch {
    return INITIAL_DECISIONS;
  }
}

export function recordDecision(decision: Omit<FinancialDecision, "id" | "date" | "displayDate" | "fullDate"> & { date?: string }): FinancialDecision {
  const decisions = getDecisions();
  const dateObj = new Date(decision.date || Date.now());
  const displayDate = dateObj.toLocaleDateString("en-US", { month: "short", year: "numeric" });
  const fullDate = dateObj.toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" });

  const newDecision: FinancialDecision = {
    id: `decision-${Date.now()}`,
    date: dateObj.toISOString().slice(0, 7),
    displayDate,
    fullDate,
    title: decision.title,
    summary: decision.summary,
    category: decision.category,
    source: decision.source,
    metrics: decision.metrics,
    notes: decision.notes,
  };

  const updated = [newDecision, ...decisions];
  if (typeof window !== "undefined") {
    localStorage.setItem(DECISIONS_STORAGE_KEY, JSON.stringify(updated));
  }

  // Also write a matching diary entry so the physical diary captures it!
  const content = `Decision Logged: ${newDecision.title}

${newDecision.summary}
${newDecision.metrics?.target ? `• Target: ${newDecision.metrics.target}` : ""}
${newDecision.metrics?.horizon ? `• Horizon: ${newDecision.metrics.horizon}` : ""}
${newDecision.metrics?.monthlyInvestment ? `• Monthly investment: ${newDecision.metrics.monthlyInvestment}` : ""}
${newDecision.notes ? `\nContext: ${newDecision.notes}` : ""}`;

  saveDiaryEntry({
    date: dateObj.toISOString().slice(0, 10),
    title: newDecision.title,
    content,
    tags: ["Financial Decision", newDecision.category],
    isImportant: true,
  });

  return newDecision;
}
