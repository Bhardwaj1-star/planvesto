"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { usePathname } from "next/navigation";
import PlanningBasketButton from "./PlanningBasketButton";

export default function StrategyWorkflowNav({ showWorkflow = true }: { showWorkflow?: boolean }) {
  const pathname = usePathname();
  const [goalId, setGoalId] = useState<string | null>(null);

  const [strategyVersionId, setStrategyVersionId] = useState<string | null>(null);

  useEffect(() => {
    if (typeof window !== "undefined") {
      const params = new URLSearchParams(window.location.search);
      setGoalId(params.get("goalId"));
      setStrategyVersionId(params.get("strategyVersionId"));
    }
  }, []);

  return (
    <div className="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
      {isStrategyBuilder && <PlanningBasketButton />}
    </div>
  );
}
