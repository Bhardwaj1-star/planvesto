import { redirect } from "next/navigation";

export default function InvestorDashboardRedirect() {
  redirect("/investor/financial-state");
}
