"use client";

import { useEffect } from "react";

const AUTO_REFRESH_MS = 60_000;

export default function ManualTestAutoRefresh() {
  useEffect(() => {
    if (process.env.NODE_ENV !== "development") return;

    const timer = window.setInterval(() => {
      window.location.reload();
    }, AUTO_REFRESH_MS);

    return () => window.clearInterval(timer);
  }, []);

  return null;
}
