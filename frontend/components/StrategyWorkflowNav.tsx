"use client";

import { usePathname } from "next/navigation";
import PlanningBasketButton from "./PlanningBasketButton";

export default function StrategyWorkflowNav() {
  const pathname = usePathname();
  const isStrategyBuilder = Boolean(pathname?.startsWith("/investor/strategy-builder"));

  return (
    <div className="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
      {isStrategyBuilder && <PlanningBasketButton />}
    </div>
  );
}
