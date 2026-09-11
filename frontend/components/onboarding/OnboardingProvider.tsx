"use client";

import { createContext, useContext, useEffect, useState } from "react";
import { usePathname, useRouter } from "next/navigation";
import type { PersonalInformation } from "../../lib/onboarding/personal-information/model";
import type { FamilyMember } from "../../lib/onboarding/family-dependents/types";
import type { IncomeSource } from "../../lib/onboarding/income/types";
import type { Expense } from "../../lib/onboarding/expenses/types";
import type { Asset } from "../../lib/onboarding/assets/types";
import type { Liability } from "../../lib/onboarding/liabilities/types";
import type { Goal } from "../../lib/onboarding/goals/types";
import {
  loadOnboardingData,
  saveAssets,
  saveCommitments,
  saveExpenses,
  saveFamilyMembers,
  saveGoals,
  saveIncomeSources,
  saveLiabilities,
  savePersonalInformation,
  type Commitment,
  type OnboardingData,
} from "../../lib/onboarding/persistence";

export const onboardingSteps = [
  { number: 1, slug: "personal-information", title: "Personal Information" },
  { number: 2, slug: "family-dependents", title: "Family & Dependents" },
  { number: 3, slug: "income", title: "Income" },
  { number: 4, slug: "expenses", title: "Expenses" },
  { number: 5, slug: "assets", title: "Assets" },
  { number: 6, slug: "liabilities", title: "Liabilities" },
  { number: 7, slug: "goals", title: "Goals" },
] as const;

type OnboardingState = {
  planningUnitId: string | null;
  investorId: string | null;
  personalInformation: PersonalInformation;
  familyMembers: FamilyMember[];
  incomeSources: IncomeSource[];
  expenses: Expense[];
  assets: Asset[];
  liabilities: Liability[];
  commitments: Commitment[];
  goals: Goal[];
  completedSteps: number[];
  isLoading: boolean;
  persistenceError: string | null;
};

type OnboardingContextValue = OnboardingState & {
  setPersonalInformation: (value: PersonalInformation) => void;
  setFamilyMembers: (value: FamilyMember[] | ((current: FamilyMember[]) => FamilyMember[])) => void;
  setIncomeSources: (value: IncomeSource[] | ((current: IncomeSource[]) => IncomeSource[])) => void;
  setExpenses: (value: Expense[] | ((current: Expense[]) => Expense[])) => void;
  setAssets: (value: Asset[] | ((current: Asset[]) => Asset[])) => void;
  setLiabilities: (value: Liability[] | ((current: Liability[]) => Liability[])) => void;
  setCommitments: (value: Commitment[] | ((current: Commitment[]) => Commitment[])) => void;
  setGoals: (value: Goal[] | ((current: Goal[]) => Goal[])) => void;
  savePersonalInformation: (value: PersonalInformation) => Promise<OnboardingData>;
  saveFamilyMembers: (value: FamilyMember[]) => Promise<OnboardingData>;
  saveIncomeSources: (value: IncomeSource[]) => Promise<OnboardingData>;
  saveExpenses: (value: Expense[]) => Promise<OnboardingData>;
  saveAssets: (value: Asset[]) => Promise<OnboardingData>;
  saveLiabilities: (value: Liability[]) => Promise<OnboardingData>;
  saveCommitments: (value: Commitment[]) => Promise<OnboardingData>;
  saveGoals: (value: Goal[]) => Promise<OnboardingData>;
  completeStep: (step: number) => void;
};

const OnboardingContext = createContext<OnboardingContextValue | null>(null);

export function OnboardingProvider({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const [state, setState] = useState<OnboardingState>({
    planningUnitId: null,
    investorId: null,
    personalInformation: {
      fullName: "",
      dateOfBirth: "",
      gender: "",
      maritalStatus: "",
      mobileNumber: "",
      address: "",
      city: "",
      state: "",
      country: "",
      occupation: "",
    },
    familyMembers: [],
    incomeSources: [],
    expenses: [],
    assets: [],
    liabilities: [],
    commitments: [],
    goals: [],
    completedSteps: [],
    isLoading: true,
    persistenceError: null,
  });

  useEffect(() => {
    const shouldLoad = pathname.startsWith("/investor/onboarding/") || pathname.startsWith("/investor/profile");
    if (!shouldLoad) return;
    let active = true;
    setState((current) => ({ ...current, isLoading: true }));
    loadOnboardingData()
      .then((data) => {
        if (!active) return;
        setState((current) => ({
          ...current,
          ...data,
          completedSteps: [
            data.personalInformation.fullName ? 1 : 0,
            data.familyMembers.length ? 2 : 0,
            data.incomeSources.length ? 3 : 0,
            data.expenses.length ? 4 : 0,
            data.assets.length ? 5 : 0,
            data.liabilities.length ? 6 : 0,
            data.goals.length ? 7 : 0,
          ].filter(Boolean),
          isLoading: false,
          persistenceError: null,
        }));
      })
      .catch((error: unknown) => {
        if (!active) return;
        setState((current) => ({ ...current, isLoading: false, persistenceError: error instanceof Error ? error.message : "Unable to load onboarding data." }));
      });
    return () => {
      active = false;
    };
  }, [pathname]);

  function applySavedData(data: OnboardingData) {
    setState((current) => ({ ...current, ...data, persistenceError: null }));
    return data;
  }

  async function saveSection(save: () => Promise<OnboardingData>) {
    try {
      return applySavedData(await save());
    } catch (error: unknown) {
      const message = error instanceof Error ? error.message : "Unable to save onboarding data.";
      setState((current) => ({ ...current, persistenceError: message }));
      throw error;
    }
  }

  const value: OnboardingContextValue = {
    ...state,
    setPersonalInformation: (personalInformation) => setState((current) => ({ ...current, personalInformation })),
    setFamilyMembers: (familyMembers) => setState((current) => ({ ...current, familyMembers: typeof familyMembers === "function" ? familyMembers(current.familyMembers) : familyMembers })),
    setIncomeSources: (incomeSources) => setState((current) => ({ ...current, incomeSources: typeof incomeSources === "function" ? incomeSources(current.incomeSources) : incomeSources })),
    setExpenses: (expenses) => setState((current) => ({ ...current, expenses: typeof expenses === "function" ? expenses(current.expenses) : expenses })),
    setAssets: (assets) => setState((current) => ({ ...current, assets: typeof assets === "function" ? assets(current.assets) : assets })),
    setLiabilities: (liabilities) => setState((current) => ({ ...current, liabilities: typeof liabilities === "function" ? liabilities(current.liabilities) : liabilities })),
    setCommitments: (commitments) => setState((current) => ({ ...current, commitments: typeof commitments === "function" ? commitments(current.commitments) : commitments })),
    setGoals: (goals) => setState((current) => ({ ...current, goals: typeof goals === "function" ? goals(current.goals) : goals })),
    savePersonalInformation: (value) => saveSection(() => savePersonalInformation(value)),
    saveFamilyMembers: (value) => saveSection(() => saveFamilyMembers(value)),
    saveIncomeSources: (value) => saveSection(() => saveIncomeSources(value)),
    saveExpenses: (value) => saveSection(() => saveExpenses(value)),
    saveAssets: (value) => saveSection(() => saveAssets(value)),
    saveLiabilities: (value) => saveSection(() => saveLiabilities(value)),
    saveCommitments: (value) => saveSection(() => saveCommitments(value)),
    saveGoals: (value) => saveSection(() => saveGoals(value)),
    completeStep: (step) => setState((current) => current.completedSteps.includes(step) ? current : { ...current, completedSteps: [...current.completedSteps, step] }),
  };

  if (pathname.startsWith("/investor/onboarding/") && state.isLoading) {
    return (
      <main className="flex min-h-screen flex-col items-center justify-center bg-[#f8fafc] text-slate-600">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-navy-900 text-white shadow-md animate-pulse">
          <svg className="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2">
            <path d="M5 17L10 12L13 15L19 8" />
            <path d="M15 8H19V12" />
          </svg>
        </div>
        <p className="mt-4 text-sm font-semibold text-navy-900">Loading your financial plan...</p>
        <p className="mt-1 text-xs text-slate-400">Preparing your guided financial workspace</p>
      </main>
    );
  }

  return (
    <OnboardingContext.Provider value={value}>
      {children}
      {state.persistenceError && <p className="fixed bottom-4 left-4 right-4 z-50 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm font-semibold text-red-700" role="alert">{state.persistenceError}</p>}
    </OnboardingContext.Provider>
  );
}

function useOnboardingState() {
  const context = useContext(OnboardingContext);
  if (!context) throw new Error("useOnboardingState must be used within OnboardingProvider");
  return context;
}

export function useOnboardingNavigation(step: number) {
  const router = useRouter();
  const pathname = usePathname();
  const { completedSteps, completeStep } = useOnboardingState();
  const currentStep = onboardingSteps.find((item) => pathname.endsWith(`/${item.slug}`))?.number ?? step;
  const currentIndex = onboardingSteps.findIndex((item) => item.number === currentStep);
  const resumeStep = onboardingSteps.find((item) => !completedSteps.includes(item.number))?.number ?? onboardingSteps.length;
  const highestCompletedStep = completedSteps.length > 0 ? Math.max(...completedSteps) : 0;
  const maxAccessibleStep = Math.min(highestCompletedStep + 1, onboardingSteps.length);

  function goToStep(targetStep: number, allowCurrentStep = false) {
    const target = onboardingSteps.find((item) => item.number === targetStep);
    const canAccess = targetStep <= maxAccessibleStep || (allowCurrentStep && targetStep === currentStep + 1);
    if (target && canAccess) router.push(`/investor/onboarding/${target.slug}`);
  }

  useEffect(() => {
    if (!pathname.startsWith("/investor/onboarding/") || currentIndex < 0) return;
    if (currentStep > maxAccessibleStep) {
      const target = onboardingSteps.find((item) => item.number === resumeStep);
      if (target) router.replace(`/investor/onboarding/${target.slug}`);
    }
  }, [currentIndex, currentStep, maxAccessibleStep, pathname, resumeStep, router]);

  return {
    currentStep,
    steps: onboardingSteps,
    resumeStep,
    isFirstStep: currentIndex === 0,
    isLastStep: currentIndex === onboardingSteps.length - 1,
    canGoPrevious: currentIndex > 0,
    canGoNext: currentStep < maxAccessibleStep,
    progress: Math.round((currentStep / onboardingSteps.length) * 100),
    completedSteps,
    completeStep,
    goToStep,
    goNext: () => goToStep(onboardingSteps[currentIndex + 1]?.number ?? currentStep, true),
    goPrevious: () => goToStep(onboardingSteps[currentIndex - 1]?.number ?? currentStep),
  };
}

export function useOnboardingStore() {
  return useOnboardingState();
}
