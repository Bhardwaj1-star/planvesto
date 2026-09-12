import InvestorSidebar from "../../components/InvestorSidebar";
import ClientThemeWrapper from "../../components/ClientThemeWrapper";

export default function InvestorLayout({ children }: { children: React.ReactNode }) {
  return (
    <ClientThemeWrapper>
      <InvestorSidebar />
      <div className="min-w-0 flex-1">{children}</div>
    </ClientThemeWrapper>
  );
}