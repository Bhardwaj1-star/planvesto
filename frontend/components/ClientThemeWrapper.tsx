"use client";

import { ThemeProvider, useTheme } from "./ThemeProvider";
import type { ReactNode } from "react";

function ThemeWrapper({ children }: { children: ReactNode }) {
  const { theme } = useTheme();

  return (
    <div data-theme={theme} className="min-h-screen bg-[#F4F7FA] text-slate-900">
      <div className="flex min-h-screen">
        {children}
      </div>
    </div>
  );
}

export default function ClientThemeWrapper({ children }: { children: ReactNode }) {
  return (
    <ThemeProvider>
      <ThemeWrapper>{children}</ThemeWrapper>
    </ThemeProvider>
  );
}
