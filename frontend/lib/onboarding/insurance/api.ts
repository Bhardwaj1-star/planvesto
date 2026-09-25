import { supabase } from "../../supabase";

export type ExtractedInsuranceFields = {
  policy_name?: string | null;
  insurer?: string | null;
  policy_number?: string | null;
  policy_type?: string | null;
  premium?: string | null;
  premium_frequency?: string | null;
  sum_assured?: string | null;
  maturity_date?: string | null;
  maturity_value?: string | null;
  current_surrender_value?: string | null;
};

export async function extractInsurancePolicyPdf(file: File): Promise<ExtractedInsuranceFields> {
  const { data, error } = await supabase.auth.getSession();
  if (error) throw error;
  if (!data.session) throw new Error("Authentication required.");

  const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL;
  if (!backendUrl) throw new Error("Backend URL is not configured.");

  const form = new FormData();
  form.append("file", file);
  const response = await fetch(`${backendUrl}/api/insurance/extract-policy-pdf`, {
    method: "POST",
    headers: { Authorization: `Bearer ${data.session.access_token}` },
    body: form,
  });

  const body = await response.json().catch(() => null);
  if (!response.ok) {
    const detail = body && typeof body === "object" && "detail" in body ? String((body as { detail: unknown }).detail) : "Unable to read policy PDF.";
    throw new Error(detail);
  }
  return (body?.fields || {}) as ExtractedInsuranceFields;
}
