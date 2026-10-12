"use client";

import { useMemo, useState } from "react";

type StrategyId = "progressive_de_risking" | "capital_preservation" | "debt_reduction" | "credit_utilisation";
type TechniqueSet = { required: string[]; conditional: string[] };
type Candidate = { id: StrategyId; name: string; reason: string; variant: string; techniques: TechniqueSet };

const strategyNames: Record<StrategyId, string> = {
  progressive_de_risking: "Progressive De-risking",
  capital_preservation: "Capital Preservation",
  debt_reduction: "Debt Reduction",
  credit_utilisation: "Credit Utilisation",
};

const techniqueRules: Record<string, TechniqueSet> = {
  "Goal-Date Glide Path": { required: ["Glide Path"], conditional: ["Bucketing", "Cash-flow Matching"] },
  "Payment-Tranche Glide Path": { required: ["Glide Path", "Cash-flow Matching"], conditional: ["Bucketing"] },
  "Recurring-Cashflow Glide Path": { required: ["Bucketing", "Cash-flow Matching"], conditional: ["Glide Path"] },
  "Income-Transition Glide Path": { required: ["Glide Path", "Bucketing"], conditional: ["Cash-flow Matching"] },
  "Full-Goal Preservation": { required: ["Bucketing", "Asset Earmarking"], conditional: ["Cash-flow Matching", "Laddering"] },
  "First-Payment Preservation": { required: ["Cash-flow Matching", "Bucketing"], conditional: ["Asset Earmarking"] },
  "Rolling Reserve Preservation": { required: ["Bucketing", "Cash-flow Matching"], conditional: ["Laddering"] },
  "Protected-Core Preservation": { required: ["Asset Earmarking", "Bucketing"], conditional: ["Cash-flow Matching", "Laddering"] },
  "Goal-Gap Debt Reduction": { required: ["Goal Segmentation", "Debt Repayment Prioritisation"], conditional: ["Debt Cost Optimisation", "Cash-flow Matching", "Debt Prepayment Optimisation"] },
  "EMI-Relief Debt Reduction": { required: ["EMI Capacity Analysis", "Debt Cost Optimisation"], conditional: ["Debt Repayment Prioritisation", "Debt Prepayment Optimisation"] },
  "Residual-Gap Debt Reduction": { required: ["Goal Segmentation", "Cash-flow Matching"], conditional: ["Debt Repayment Prioritisation", "Debt Cost Optimisation", "Debt Prepayment Optimisation"] },
  "Goal-Linked Debt Reduction": { required: ["Goal Segmentation", "Cash-flow Matching"], conditional: ["Debt Cost Optimisation", "Debt Prepayment Optimisation"] },
  "Residual-Gap Bridge": { required: ["Borrowing Capacity Analysis", "Financing Cost Comparison"], conditional: ["Cash-flow Matching", "EMI Capacity Analysis"] },
  "Partial-Goal Financing": { required: ["Financing Cost Comparison", "Goal Segmentation"], conditional: ["Borrowing Capacity Analysis", "EMI Capacity Analysis"] },
  "EMI-Cap Financing": { required: ["EMI Capacity Analysis", "Borrowing Capacity Analysis"], conditional: ["Financing Cost Comparison"] },
  "Timing-Bridge Financing": { required: ["Cash-flow Matching", "Financing Cost Comparison"], conditional: ["Borrowing Capacity Analysis", "EMI Capacity Analysis"] },
};

function getCandidates(input: {
  feasibilityReady: boolean;
  futureRequirement: boolean;
  protectionSensitive: boolean;
  recurringPayments: boolean;
  incomeTransition: boolean;
  coreOnlyProtection: boolean;
  materialDebt: boolean;
  emiPressure: boolean;
  multipleGoals: boolean;
  fundingGap: boolean;
  timingGap: boolean;
  partialFinance: boolean;
  borrowingCapacity: boolean;
  emiSustainable: boolean;
  financingJustified: boolean;
  repaymentPath: boolean;
}): Candidate[] {
  if (!input.feasibilityReady) return [];
  const candidates: Candidate[] = [];
  if (input.futureRequirement && !input.protectionSensitive) {
    const variant = input.incomeTransition ? "Income-Transition Glide Path" : input.recurringPayments ? "Payment-Tranche Glide Path" : "Goal-Date Glide Path";
    candidates.push({ id: "progressive_de_risking", name: strategyNames.progressive_de_risking, reason: "A future requirement may benefit from gradually changing the risk/capital position as it approaches.", variant, techniques: techniqueRules[variant] });
  }
  if (input.protectionSensitive) {
    const variant = input.recurringPayments ? "Rolling Reserve Preservation" : input.coreOnlyProtection ? "Protected-Core Preservation" : input.timingGap ? "First-Payment Preservation" : "Full-Goal Preservation";
    candidates.push({ id: "capital_preservation", name: strategyNames.capital_preservation, reason: "Some required capital is now sensitive to loss or timing risk.", variant, techniques: techniqueRules[variant] });
  }
  if (input.materialDebt) {
    const variant = input.multipleGoals ? "Goal-Linked Debt Reduction" : input.emiPressure ? "EMI-Relief Debt Reduction" : input.fundingGap ? "Goal-Gap Debt Reduction" : "Residual-Gap Debt Reduction";
    candidates.push({ id: "debt_reduction", name: strategyNames.debt_reduction, reason: "Debt is marked as materially affecting cash flow, affordability, resilience, or goal funding.", variant, techniques: techniqueRules[variant] });
  }
  if (input.fundingGap || input.timingGap) {
    const creditViable = input.borrowingCapacity && input.emiSustainable && input.financingJustified && input.repaymentPath;
    if (creditViable) {
      const variant = input.timingGap ? "Timing-Bridge Financing" : input.emiSustainable && !input.borrowingCapacity ? "EMI-Cap Financing" : input.partialFinance ? "Partial-Goal Financing" : "Residual-Gap Bridge";
      candidates.push({ id: "credit_utilisation", name: strategyNames.credit_utilisation, reason: "A funding/timing gap exists and all four prototype viability checks are marked as passed.", variant, techniques: techniqueRules[variant] });
    }
  }
  return candidates;
}

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return <label className="block text-sm font-medium text-slate-700"><span className="mb-1.5 block">{label}</span>{children}</label>;
}
function Check({ label, checked, onChange, help }: { label: string; checked: boolean; onChange: (value: boolean) => void; help?: string }) {
  return <label className="flex cursor-pointer items-start gap-3 rounded-xl border border-slate-200 bg-white p-3">
    <input className="mt-1 h-4 w-4 accent-teal-700" type="checkbox" checked={checked} onChange={(event) => onChange(event.target.checked)} />
    <span><span className="block text-sm font-semibold text-slate-800">{label}</span>{help && <span className="mt-0.5 block text-xs leading-5 text-slate-500">{help}</span>}</span>
  </label>;
}

export default function StrategyBuilderPrototypePage() {
  const [goalName, setGoalName] = useState("Education");
  const [feasibilityReady, setFeasibilityReady] = useState(false);
  const [futureRequirement, setFutureRequirement] = useState(true);
  const [protectionSensitive, setProtectionSensitive] = useState(false);
  const [recurringPayments, setRecurringPayments] = useState(false);
  const [incomeTransition, setIncomeTransition] = useState(false);
  const [coreOnlyProtection, setCoreOnlyProtection] = useState(false);
  const [materialDebt, setMaterialDebt] = useState(false);
  const [emiPressure, setEmiPressure] = useState(false);
  const [multipleGoals, setMultipleGoals] = useState(false);
  const [fundingGap, setFundingGap] = useState(false);
  const [timingGap, setTimingGap] = useState(false);
  const [partialFinance, setPartialFinance] = useState(false);
  const [borrowingCapacity, setBorrowingCapacity] = useState(false);
  const [emiSustainable, setEmiSustainable] = useState(false);
  const [financingJustified, setFinancingJustified] = useState(false);
  const [repaymentPath, setRepaymentPath] = useState(false);
  const [selectedId, setSelectedId] = useState<StrategyId | "">("");
  const [decision, setDecision] = useState<"undecided" | "accept" | "reject" | "modify" | "open">("undecided");
  const [investorNotes, setInvestorNotes] = useState("");

  const candidates = useMemo(() => getCandidates({
    feasibilityReady, futureRequirement, protectionSensitive, recurringPayments, incomeTransition, coreOnlyProtection,
    materialDebt, emiPressure, multipleGoals, fundingGap, timingGap, partialFinance,
    borrowingCapacity, emiSustainable, financingJustified, repaymentPath,
  }), [feasibilityReady, futureRequirement, protectionSensitive, recurringPayments, incomeTransition, coreOnlyProtection, materialDebt, emiPressure, multipleGoals, fundingGap, timingGap, partialFinance, borrowingCapacity, emiSustainable, financingJustified, repaymentPath]);
  const selected = candidates.find((candidate) => candidate.id === selectedId) ?? null;
  const creditGap = fundingGap || timingGap;
  const creditFails = creditGap && !(borrowingCapacity && emiSustainable && financingJustified && repaymentPath);

  function toggleCandidate(id: StrategyId) {
    setSelectedId((current) => current === id ? "" : id);
    setDecision("undecided");
  }

  return <main className="min-h-screen bg-slate-50 text-slate-900">
    <div className="mx-auto max-w-6xl px-4 py-8 sm:px-6 lg:px-8">
      <div className="mb-6 flex flex-wrap items-start justify-between gap-4">
        <div>
          <p className="text-xs font-bold uppercase tracking-[0.18em] text-teal-800">PlanVesto · Isolated prototype</p>
          <h1 className="mt-2 text-3xl font-bold tracking-tight sm:text-4xl">Strategy Builder</h1>
          <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-600">Real-life decision cases ke hisaab se goal, financial situation aur constraints se applicable strategies nikaalo. Final choice investor ki hai.</p>
        </div>
        <span className="rounded-full border border-amber-300 bg-amber-50 px-3 py-1.5 text-xs font-bold text-amber-900">Prototype · Not connected to live data</span>
      </div>

      <div className="mb-6 rounded-2xl border border-teal-200 bg-teal-50 p-4 text-sm leading-6 text-teal-950">
        <strong>Decision order:</strong> Goal Planner feasibility → constraints → strategy applicability and viability → strategy → variant → techniques → investor decision. Yeh prototype Goal Planner ka calculation dobara nahi karta.
      </div>

      <div className="grid gap-6 lg:grid-cols-[0.95fr_1.05fr]">
        <section className="space-y-5">
          <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
            <h2 className="text-lg font-bold">1. Goal aur feasibility</h2>
            <p className="mt-1 text-sm text-slate-500">Feasibility ka result Goal Planner se aana chahiye.</p>
            <div className="mt-4 space-y-4">
              <Field label="Goal ka naam">
                <input className="w-full rounded-xl border border-slate-300 px-3 py-2.5 outline-none focus:border-teal-700" value={goalName} onChange={(e) => setGoalName(e.target.value)} placeholder="Jaise Education, Retirement" />
              </Field>
              <Check label="Goal Planner ki feasibility/funding information available hai" checked={feasibilityReady} onChange={setFeasibilityReady} help="Off hone par Strategy Builder koi candidate nahi dikhayega." />
              <Check label="Future mein ek defined requirement hai" checked={futureRequirement} onChange={setFutureRequirement} />
              <Check label="Required capital ko ab loss/timing risk se bachana zaroori hai" checked={protectionSensitive} onChange={setProtectionSensitive} />
              <div className="grid gap-3 sm:grid-cols-2">
                <Check label="Multiple future payments" checked={recurringPayments} onChange={setRecurringPayments} />
                <Check label="Growth se recurring income mein transition" checked={incomeTransition} onChange={setIncomeTransition} />
                <Check label="Sirf core/required capital protect karna hai" checked={coreOnlyProtection} onChange={setCoreOnlyProtection} />
                <Check label="Multiple goals / existing plan par impact" checked={multipleGoals} onChange={setMultipleGoals} />
              </div>
            </div>
          </div>

          <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
            <h2 className="text-lg font-bold">2. Financial problem aur constraints</h2>
            <p className="mt-1 text-sm text-slate-500">Sirf wahi conditions select kar jo is case mein sach hain.</p>
            <div className="mt-4 grid gap-3 sm:grid-cols-2">
              <Check label="Debt financial capacity ko materially affect karta hai" checked={materialDebt} onChange={setMaterialDebt} />
              <Check label="EMI cash-flow ko daba rahi hai" checked={emiPressure} onChange={setEmiPressure} />
              <Check label="Funding gap hai" checked={fundingGap} onChange={setFundingGap} />
              <Check label="Temporary timing gap hai" checked={timingGap} onChange={setTimingGap} />
              <Check label="Goal ka ek defined hissa finance karna hai" checked={partialFinance} onChange={setPartialFinance} />
            </div>
            <h3 className="mt-5 text-sm font-bold text-slate-800">Credit ke zaroori checks</h3>
            <p className="mt-1 text-xs leading-5 text-slate-500">Credit Utilisation tabhi candidate banega jab gap ho aur chaaron checks pass hon.</p>
            <div className="mt-3 grid gap-3 sm:grid-cols-2">
              <Check label="Borrowing capacity sufficient" checked={borrowingCapacity} onChange={setBorrowingCapacity} />
              <Check label="EMI sustainable" checked={emiSustainable} onChange={setEmiSustainable} />
              <Check label="Financing cost justified" checked={financingJustified} onChange={setFinancingJustified} />
              <Check label="Repayment ka credible path hai" checked={repaymentPath} onChange={setRepaymentPath} />
            </div>
          </div>
        </section>

        <section className="space-y-5">
          <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
            <div className="flex flex-wrap items-start justify-between gap-3">
              <div><h2 className="text-lg font-bold">3. Applicable strategies</h2><p className="mt-1 text-sm text-slate-500">Koi strategy sirf goal ke naam se select nahi hoti.</p></div>
              <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-700">{candidates.length} candidate{candidates.length === 1 ? "" : "s"}</span>
            </div>
            {!feasibilityReady ? <div className="mt-4 rounded-xl border border-amber-200 bg-amber-50 p-4 text-sm leading-6 text-amber-950">Pehle Goal Planner ki feasibility/funding information available mark kar. Uske bina strategy decision rukega.</div> :
              candidates.length === 0 ? <div className="mt-4 rounded-xl border border-slate-200 bg-slate-50 p-4"><p className="font-semibold">Abhi koi applicable strategy identify nahi hui.</p><p className="mt-1 text-sm text-slate-600">Agar sab relevant candidates check ho chuke hain, outcome “No Acceptable Strategy” ho sakta hai. Sirf output dene ke liye strategy force nahi hogi.</p></div> :
              <div className="mt-4 space-y-3">{candidates.map((candidate) => <button key={candidate.id} type="button" onClick={() => toggleCandidate(candidate.id)} className={`w-full rounded-xl border p-4 text-left transition ${selectedId === candidate.id ? "border-teal-700 bg-teal-50 ring-1 ring-teal-700" : "border-slate-200 bg-white hover:border-slate-400"}`}>
                <div className="flex flex-wrap items-center justify-between gap-2"><span className="font-bold">{candidate.name}</span><span className="text-xs font-semibold text-teal-800">{selectedId === candidate.id ? "Selected" : "View details"}</span></div>
                <p className="mt-2 text-sm leading-5 text-slate-600">{candidate.reason}</p>
                <p className="mt-3 text-xs font-semibold uppercase tracking-wide text-slate-500">Suggested variant</p><p className="mt-1 text-sm font-semibold">{candidate.variant}</p>
              </button>)}</div>}
            {creditFails && <div className="mt-4 rounded-xl border border-rose-200 bg-rose-50 p-3 text-sm leading-5 text-rose-900"><strong>Credit Utilisation fail:</strong> ek ya zyada viability checks pass nahi hain. Isliye credit ko candidate ke roop mein nahi dikhaya gaya.</div>}
          </div>

          {selected && <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
            <h2 className="text-lg font-bold">4. Variant aur techniques</h2>
            <p className="mt-1 text-sm text-slate-500">{selected.name} → {selected.variant}</p>
            <div className="mt-4">
              <h3 className="text-sm font-bold text-slate-800">Required techniques</h3>
              <div className="mt-2 flex flex-wrap gap-2">{selected.techniques.required.map((item) => <span key={item} className="rounded-lg border border-teal-200 bg-teal-50 px-3 py-2 text-sm font-medium text-teal-950">{item}</span>)}</div>
            </div>
            <div className="mt-4">
              <h3 className="text-sm font-bold text-slate-800">Conditional techniques</h3>
              <div className="mt-2 flex flex-wrap gap-2">{selected.techniques.conditional.map((item) => <span key={item} className="rounded-lg border border-slate-200 bg-slate-50 px-3 py-2 text-sm text-slate-700">{item}</span>)}</div>
              <p className="mt-2 text-xs leading-5 text-slate-500">Conditional ka matlab: technique har case mein zaroori nahi; uski condition verify karni hogi.</p>
            </div>
            <div className="mt-5 border-t border-slate-200 pt-5">
              <h2 className="text-lg font-bold">5. Investor ka decision</h2>
              <p className="mt-1 text-sm text-slate-500">Recommendation final accepted plan nahi hoti.</p>
              <div className="mt-3 grid grid-cols-2 gap-2">
                {([{ id: "accept", label: "Accept path" }, { id: "modify", label: "Modify path" }, { id: "reject", label: "Reject path" }, { id: "open", label: "Apni strategy" }] as const).map((item) => <button key={item.id} type="button" onClick={() => setDecision(item.id)} className={`rounded-xl border px-3 py-2.5 text-sm font-semibold ${decision === item.id ? "border-teal-700 bg-teal-50 text-teal-950" : "border-slate-200 bg-white text-slate-700"}`}>{item.label}</button>)}
              </div>
              <Field label="Investor ke notes / kya badalna hai">
                <textarea className="mt-3 min-h-24 w-full rounded-xl border border-slate-300 px-3 py-2.5 outline-none focus:border-teal-700" value={investorNotes} onChange={(e) => setInvestorNotes(e.target.value)} placeholder="Investor ki preference ya reason..." />
              </Field>
              {decision !== "undecided" && <div className="mt-3 rounded-xl bg-slate-50 p-3 text-sm leading-6 text-slate-700">
                {decision === "accept" && "Investor ne is path ko accept kiya hai — production system mein aage badhne se pehle implementation aur resilience validation chahiye."}
                {decision === "modify" && "Path modify karne ki request hai — badle hue inputs ke saath affected feasibility aur strategy ko dobara validate karna hoga."}
                {decision === "reject" && "Path reject hua hai — system doosra acceptable path dikhaye ya “No Acceptable Strategy” return kare; force na kare."}
                {decision === "open" && "Investor-designed strategy mode — investor ke proposed numbers ko structure, calculate, explain aur validate karna hoga."}
              </div>}
              <button type="button" onClick={() => { setSelectedId(""); setDecision("undecided"); setInvestorNotes(""); }} className="mt-4 rounded-xl border border-slate-300 px-3 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-50">Clear selection</button>
            </div>
          </div>}

          <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
            <h2 className="text-lg font-bold">Prototype guardrails</h2>
            <ul className="mt-3 space-y-2 text-sm leading-5 text-slate-600">
              <li>• Goal Funding/SIP/step-up ko Strategy Builder strategy nahi maana gaya.</li>
              <li>• Asset Mapping upstream planning evidence hai; Asset Earmarking selected path ke baad technique ho sakti hai.</li>
              <li>• Ek financial plan mein alag requirements ke liye multiple strategies ho sakti hain.</li>
              <li>• Financial state ya goal badalne par pehle feasibility, phir sirf affected strategy revalidate hogi.</li>
              <li>• Yeh prototype live Goal Planner, database ya existing Strategy Builder API ko call nahi karta.</li>
            </ul>
          </div>
        </section>
      </div>
      <p className="mt-8 text-xs leading-5 text-slate-500">Prototype note: Applicability flags yahan user manually set karta hai. Yeh business rules ko test karne wala isolated UI hai, financial advice ya verified runtime decision engine nahi. Materiality thresholds aur kuch selection rules abhi real-life cases mein freeze nahi hue hain.</p>
    </div>
  </main>;
}
