"use client";

import React, { ReactNode } from "react";
import InvestorProfileMenu from "./InvestorProfileMenu";

export interface InvestorHeaderProps {
  eyebrow?: string;
  title: string;
  description?: string;
  children?: ReactNode;
}

export default function InvestorHeader({
  eyebrow = "Planvesto",
  title,
  description,
  children,
}: InvestorHeaderProps) {
  return (
    <header className="border-b border-slate-200 bg-white">
      <div className="flex min-h-[82px] flex-col justify-center gap-3 px-5 py-4 pl-16 sm:flex-row sm:items-center sm:justify-between sm:gap-4 sm:py-0 md:pl-8 lg:px-8">
        <div className="min-w-0 flex-1">
          {eyebrow && (
            <p className="text-xs font-bold uppercase tracking-[0.16em] text-teal-700">
              {eyebrow}
            </p>
          )}
          <h1 className="mt-0.5 truncate text-2xl font-extrabold tracking-tight text-slate-950 sm:text-3xl">
            {title}
          </h1>
          {description && (
            <p className="mt-1 max-w-3xl text-xs text-slate-500 sm:text-sm">
              {description}
            </p>
          )}
        </div>
        <div className="flex shrink-0 items-center gap-3 sm:gap-4">
          {children}
          <InvestorProfileMenu />
        </div>
      </div>
    </header>
  );
}
