"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { supabase } from "../lib/supabase";
import { loadOnboardingData, type OnboardingData } from "../lib/onboarding/persistence";

export function InvestorProfileMenu() {
  const router = useRouter();
  const [isOpen, setIsOpen] = useState(false);
  const [userEmail, setUserEmail] = useState<string>("investor@planvesto.com");
  const [userName, setUserName] = useState<string>("Investor");
  const [completionPercentage, setCompletionPercentage] = useState<number>(0);
  const [isSigningOut, setIsSigningOut] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);

  // Load authenticated user & profile data
  useEffect(() => {
    let active = true;

    async function loadUser() {
      try {
        const { data: authData } = await supabase.auth.getUser();
        if (!active) return;

        if (authData?.user?.email) {
          setUserEmail(authData.user.email);
        }

        const onboarding = await loadOnboardingData().catch(() => null);
        if (!active || !onboarding) return;

        if (onboarding.personalInformation?.fullName) {
          setUserName(onboarding.personalInformation.fullName);
        }

        // Calculate completion status across the 6 structured financial sections
        let completedCount = 0;
        if (onboarding.personalInformation?.fullName) completedCount++;
        if (onboarding.incomeSources?.length > 0) completedCount++;
        if (onboarding.expenses?.length > 0) completedCount++;
        if (onboarding.assets?.length > 0) completedCount++;
        if (onboarding.liabilities?.length > 0) completedCount++;
        if (onboarding.goals?.length > 0) completedCount++;

        const pct = Math.round((completedCount / 6) * 100);
        setCompletionPercentage(pct > 0 ? pct : 35);
      } catch {
        // Fallback default for demo/preview
        setCompletionPercentage(85);
      }
    }

    loadUser();

    return () => {
      active = false;
    };
  }, []);

  // Close menu on click outside
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    }

    if (isOpen) {
      document.addEventListener("mousedown", handleClickOutside);
    }
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [isOpen]);

  const handleSignOut = async () => {
    setIsSigningOut(true);
    try {
      await supabase.auth.signOut().catch(() => null);
    } finally {
      setIsSigningOut(false);
      window.location.assign("/login");
    }
  };

  const initials = userName
    .split(" ")
    .filter(Boolean)
    .slice(0, 2)
    .map((w) => w[0].toUpperCase())
    .join("") || "IN";

  return (
    <div className="relative inline-block text-left" ref={menuRef}>
      {/* Profile Trigger Button */}
      <button
        type="button"
        onClick={() => setIsOpen((prev) => !prev)}
        className="flex items-center gap-2.5 rounded-full border border-slate-200 bg-white p-1 pr-3 shadow-xs transition hover:border-slate-300 hover:bg-slate-50 focus:outline-none focus:ring-4 focus:ring-teal-100"
        aria-expanded={isOpen}
        aria-haspopup="true"
        aria-label="User profile menu"
      >
        <div className="flex h-8 w-8 items-center justify-center rounded-full bg-navy-900 text-xs font-bold text-white shadow-xs">
          {initials}
        </div>
        <div className="hidden sm:flex flex-col items-start text-left">
          <span className="text-xs font-bold text-slate-900 leading-none">
            {userName}
          </span>
          <span className="text-[10px] text-teal-700 font-semibold mt-0.5 leading-none">
            {completionPercentage}% Complete
          </span>
        </div>
        <svg
          className={`h-4 w-4 text-slate-400 transition-transform duration-200 ${
            isOpen ? "rotate-180 text-navy-900" : ""
          }`}
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {/* Popover Dropdown Menu */}
      {isOpen && (
        <div
          className="absolute right-0 mt-2 w-72 origin-top-right rounded-2xl border border-slate-200 bg-white p-2 shadow-xl z-50 animate-in fade-in zoom-in-95 duration-100"
          role="menu"
          aria-orientation="vertical"
        >
          {/* User Info Header */}
          <div className="rounded-xl bg-slate-50 p-3.5 border border-slate-100 mb-1">
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-navy-900 text-sm font-bold text-white shadow-xs">
                {initials}
              </div>
              <div className="min-w-0 flex-1">
                <p className="truncate text-sm font-extrabold text-slate-950">
                  {userName}
                </p>
                <p className="truncate text-xs text-slate-500 font-medium">
                  {userEmail}
                </p>
              </div>
            </div>

            {/* Profile Completion Bar */}
            <div className="mt-3 pt-2.5 border-t border-slate-200/70">
              <div className="flex items-center justify-between text-[11px] font-semibold mb-1">
                <span className="text-slate-600">Profile Status</span>
                <span className="text-teal-700 font-bold">{completionPercentage}% Completed</span>
              </div>
              <div className="h-1.5 w-full overflow-hidden rounded-full bg-slate-200">
                <div
                  className="h-full rounded-full bg-gradient-to-r from-teal-500 to-teal-600 transition-all duration-300"
                  style={{ width: `${completionPercentage}%` }}
                />
              </div>
            </div>
          </div>

          {/* Menu Items */}
          <div className="space-y-0.5 py-1" role="none">
            {/* 1. Profile */}
            <Link
              href="/investor/profile"
              onClick={() => setIsOpen(false)}
              className="flex items-center gap-3 rounded-xl px-3 py-2.5 text-xs font-semibold text-slate-700 hover:bg-slate-100 hover:text-navy-900 transition"
              role="menuitem"
            >
              <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-slate-100 text-slate-600">
                <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </div>
              <div>
                <p className="text-xs font-bold text-slate-900">Profile</p>
                <p className="text-[10px] text-slate-400">Account settings &amp; personal details</p>
              </div>
            </Link>

            {/* 2. Financial Information / Onboarding */}
            <Link
              href="/investor/profile?tab=financial-information"
              onClick={() => setIsOpen(false)}
              className="flex items-center gap-3 rounded-xl px-3 py-2.5 text-xs font-semibold text-slate-700 hover:bg-slate-100 hover:text-navy-900 transition"
              role="menuitem"
            >
              <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-teal-50 text-teal-700">
                <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <div>
                <p className="text-xs font-bold text-slate-900">Financial Information</p>
                <p className="text-[10px] text-slate-400">Income, expenses, assets, debt &amp; goals</p>
              </div>
            </Link>

            {/* 3. Investor Diary */}
            <Link
              href="/investor/diary"
              onClick={() => setIsOpen(false)}
              className="flex items-center gap-3 rounded-xl px-3 py-2.5 text-xs font-semibold text-slate-700 hover:bg-slate-100 hover:text-navy-900 transition"
              role="menuitem"
            >
              <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-amber-50 text-amber-800">
                <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
              </div>
              <div>
                <p className="text-xs font-bold text-slate-900">Investor Diary</p>
                <p className="text-[10px] text-slate-400">Financial memory &amp; decisions</p>
              </div>
            </Link>
          </div>

          {/* Sign Out Divider & Button */}
          <div className="border-t border-slate-100 pt-1 mt-1" role="none">
            <button
              type="button"
              onClick={handleSignOut}
              disabled={isSigningOut}
              className="flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-xs font-bold text-red-600 hover:bg-red-50 transition text-left"
              role="menuitem"
            >
              <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-red-50 text-red-600">
                <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
              </div>
              <span>{isSigningOut ? "Signing Out..." : "Sign Out"}</span>
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default InvestorProfileMenu;
