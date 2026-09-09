"use client";

import { useEffect, useState, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import { supabase } from "../../../lib/supabase";
import { useOnboardingStore } from "../../../components/onboarding/OnboardingProvider";
import InvestorProfileMenu from "../../../components/InvestorProfileMenu";
import FinancialInformationSection from "../../../components/profile/FinancialInformationSection";

function ProfileContent() {
  const searchParams = useSearchParams();
  const initialTab = searchParams.get("tab") === "financial-information" ? "financial" : "account";
  const [activeTab, setActiveTab] = useState<"account" | "financial">(initialTab);

  const { personalInformation, incomeSources, expenses, assets, liabilities, goals } = useOnboardingStore();
  const [userEmail, setUserEmail] = useState<string>("investor@planvesto.com");
  const [isSigningOut, setIsSigningOut] = useState(false);

  useEffect(() => {
    supabase.auth.getUser().then(({ data }) => {
      if (data?.user?.email) {
        setUserEmail(data.user.email);
      }
    });
  }, []);

  // Sync tab if URL query changes
  useEffect(() => {
    const tabParam = searchParams.get("tab");
    if (tabParam === "financial-information") {
      setActiveTab("financial");
    }
  }, [searchParams]);

  const handleSignOut = async () => {
    setIsSigningOut(true);
    try {
      await supabase.auth.signOut().catch(() => null);
    } finally {
      setIsSigningOut(false);
      window.location.assign("/login");
    }
  };

  const displayName = personalInformation.fullName || "Investor";
  const initials = displayName
    .split(" ")
    .filter(Boolean)
    .slice(0, 2)
    .map((w) => w[0].toUpperCase())
    .join("") || "IN";

  // Calculate profile completion
  let completedCount = 0;
  if (personalInformation.fullName) completedCount++;
  if (incomeSources.length > 0) completedCount++;
  if (expenses.length > 0) completedCount++;
  if (assets.length > 0) completedCount++;
  if (liabilities.length > 0) completedCount++;
  if (goals.length > 0) completedCount++;
  const completionPercentage = Math.round((completedCount / 6) * 100);

  return (
    <main className="min-h-screen bg-[#f6f8fb] text-slate-900 pb-20">
      {/* Top Header with Profile Menu */}
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex min-h-[80px] max-w-6xl items-center justify-between gap-6 px-4 sm:px-6 lg:px-8">
          <div>
            <div className="flex items-center gap-2">
              <span className="inline-flex items-center rounded-md bg-teal-50 px-2 py-0.5 text-xs font-semibold text-teal-700 ring-1 ring-inset ring-teal-600/20">
                Personal Control Center
              </span>
              <p className="text-xs font-bold uppercase tracking-[0.14em] text-slate-400">
                Planvesto Account
              </p>
            </div>
            <h1 className="mt-1 text-2xl font-extrabold tracking-tight text-slate-950 sm:text-3xl">
              Investor Profile
            </h1>
          </div>

          <div className="flex items-center gap-3">
            <InvestorProfileMenu />
          </div>
        </div>
      </header>

      {/* Main Container */}
      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8 pt-8">
        {/* Profile Hero Card */}
        <div className="mb-8 rounded-3xl border border-slate-200 bg-white p-6 sm:p-8 shadow-sm">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-6">
            <div className="flex items-center gap-4 sm:gap-6">
              <div className="flex h-16 w-16 sm:h-20 sm:w-20 items-center justify-center rounded-3xl bg-navy-900 text-xl sm:text-2xl font-black text-white shadow-md">
                {initials}
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <h2 className="text-xl sm:text-2xl font-black text-slate-950">
                    {displayName}
                  </h2>
                  <span className="rounded-full bg-teal-50 px-2.5 py-0.5 text-[10px] font-bold text-teal-800 border border-teal-200">
                    Active Investor
                  </span>
                </div>
                <p className="text-xs sm:text-sm text-slate-500 font-medium mt-0.5">
                  {userEmail}
                </p>
                {personalInformation.occupation && (
                  <p className="text-xs text-slate-600 mt-1">
                    {personalInformation.occupation} {personalInformation.city ? `· ${personalInformation.city}` : ""}
                  </p>
                )}
              </div>
            </div>

            {/* Profile Completion Widget */}
            <div className="rounded-2xl bg-slate-50 p-4 border border-slate-100 sm:w-72">
              <div className="flex items-center justify-between text-xs font-bold mb-1.5">
                <span className="text-slate-700">Financial Profile</span>
                <span className="text-teal-700">{completionPercentage}% Completed</span>
              </div>
              <div className="h-2 w-full overflow-hidden rounded-full bg-slate-200">
                <div
                  className="h-full rounded-full bg-gradient-to-r from-teal-500 to-teal-600 transition-all duration-300"
                  style={{ width: `${completionPercentage}%` }}
                />
              </div>
              <p className="mt-2 text-[11px] text-slate-500">
                {completedCount} of 6 financial categories completed.
              </p>
            </div>
          </div>

          {/* Primary View Switcher Tabs */}
          <div className="mt-8 flex gap-2 border-t border-slate-100 pt-6">
            <button
              type="button"
              onClick={() => setActiveTab("account")}
              className={`rounded-xl px-5 py-2.5 text-xs font-bold uppercase tracking-wider transition ${
                activeTab === "account"
                  ? "bg-navy-900 text-white shadow-sm"
                  : "bg-slate-100 text-slate-600 hover:bg-slate-200 hover:text-navy-900"
              }`}
            >
              Account &amp; Security
            </button>
            <button
              type="button"
              onClick={() => setActiveTab("financial")}
              className={`rounded-xl px-5 py-2.5 text-xs font-bold uppercase tracking-wider transition ${
                activeTab === "financial"
                  ? "bg-navy-900 text-white shadow-sm"
                  : "bg-slate-100 text-slate-600 hover:bg-slate-200 hover:text-navy-900"
              }`}
            >
              Financial Information ({completedCount}/6)
            </button>
          </div>
        </div>

        {/* Tab 1: Account & Security */}
        {activeTab === "account" ? (
          <div className="space-y-6">
            <div className="grid gap-6 md:grid-cols-2">
              {/* Account Details */}
              <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm space-y-4">
                <div className="border-b border-slate-100 pb-4">
                  <h3 className="text-base font-extrabold text-navy-900">User Details</h3>
                  <p className="text-xs text-slate-500 mt-0.5">Primary login and contact credentials</p>
                </div>

                <div className="space-y-3 text-xs">
                  <div>
                    <span className="font-bold text-slate-400 uppercase tracking-wider text-[10px]">Email Address</span>
                    <p className="mt-0.5 font-semibold text-slate-900 text-sm">{userEmail}</p>
                  </div>
                  <div>
                    <span className="font-bold text-slate-400 uppercase tracking-wider text-[10px]">Full Name</span>
                    <p className="mt-0.5 font-semibold text-slate-900 text-sm">{personalInformation.fullName || "Not provided"}</p>
                  </div>
                  <div>
                    <span className="font-bold text-slate-400 uppercase tracking-wider text-[10px]">Mobile</span>
                    <p className="mt-0.5 font-semibold text-slate-900 text-sm">{personalInformation.mobileNumber || "Not provided"}</p>
                  </div>
                  <div>
                    <span className="font-bold text-slate-400 uppercase tracking-wider text-[10px]">Location</span>
                    <p className="mt-0.5 font-semibold text-slate-900 text-sm">
                      {[personalInformation.city, personalInformation.state, personalInformation.country].filter(Boolean).join(", ") || "Not provided"}
                    </p>
                  </div>
                </div>

                <div className="pt-3 border-t border-slate-100">
                  <button
                    type="button"
                    onClick={() => setActiveTab("financial")}
                    className="inline-flex items-center gap-1.5 text-xs font-bold text-teal-700 hover:text-teal-900"
                  >
                    <span>Edit in Financial Information</span>
                    <span aria-hidden="true">→</span>
                  </button>
                </div>
              </div>

              {/* Security & Authentication */}
              <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm space-y-4 flex flex-col justify-between">
                <div>
                  <div className="border-b border-slate-100 pb-4">
                    <h3 className="text-base font-extrabold text-navy-900">Security &amp; Session</h3>
                    <p className="text-xs text-slate-500 mt-0.5">Manage session and account authentication</p>
                  </div>

                  <div className="mt-4 space-y-3">
                    <div className="flex items-center justify-between rounded-xl bg-slate-50 p-3 border border-slate-100">
                      <div>
                        <p className="text-xs font-bold text-slate-900">Authentication Provider</p>
                        <p className="text-[11px] text-slate-500">Supabase Secure Auth</p>
                      </div>
                      <span className="rounded-full bg-teal-50 px-2 py-0.5 text-[10px] font-bold text-teal-700">
                        Active
                      </span>
                    </div>

                    <div className="flex items-center justify-between rounded-xl bg-slate-50 p-3 border border-slate-100">
                      <div>
                        <p className="text-xs font-bold text-slate-900">End-to-End Privacy</p>
                        <p className="text-[11px] text-slate-500">Row-Level Security Enabled</p>
                      </div>
                      <span className="rounded-full bg-slate-200 px-2 py-0.5 text-[10px] font-bold text-slate-700">
                        Protected
                      </span>
                    </div>
                  </div>
                </div>

                {/* Sign Out Action */}
                <div className="pt-4 border-t border-slate-100">
                  <button
                    type="button"
                    onClick={handleSignOut}
                    disabled={isSigningOut}
                    className="inline-flex w-full items-center justify-center gap-2 rounded-xl border border-red-200 bg-red-50/50 px-4 py-2.5 text-xs font-bold text-red-700 hover:bg-red-100 transition disabled:opacity-50"
                  >
                    <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                    </svg>
                    <span>{isSigningOut ? "Signing out..." : "Sign Out from Planvesto"}</span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        ) : (
          /* Tab 2: Financial Information (The 6 Structured Categories) */
          <div>
            <div className="mb-6 rounded-2xl border border-teal-200 bg-teal-50/60 p-4 text-xs text-teal-950 flex items-start gap-3">
              <div className="flex h-6 w-6 shrink-0 items-center justify-center rounded-lg bg-teal-600 text-white font-bold text-[11px]">
                ℹ
              </div>
              <div>
                <p className="font-bold">Your Financial Profile Hub</p>
                <p className="mt-0.5 text-teal-900">
                  All 6 areas of your financial model are directly editable here. Updates automatically calibrate your Health Score, Budgeting, and Strategy calculations.
                </p>
              </div>
            </div>

            <FinancialInformationSection />
          </div>
        )}
      </div>
    </main>
  );
}

export default function InvestorProfilePage() {
  return (
    <Suspense fallback={<div className="p-8 text-center text-sm font-semibold text-slate-500">Loading profile...</div>}>
      <ProfileContent />
    </Suspense>
  );
}
