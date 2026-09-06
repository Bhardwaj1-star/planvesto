import InvestorSidebar from "../../components/InvestorSidebar";

export default function InvestorLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-[#f6f8fb] text-slate-900">
      <div className="flex min-h-screen">
        <InvestorSidebar />
        <div className="min-w-0 flex-1">{children}</div>
      </div>
    </div>
  );
}