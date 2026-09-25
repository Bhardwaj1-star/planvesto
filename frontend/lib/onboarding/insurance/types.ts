export type InsurancePolicy = {
  id: string;
  policyName: string;
  insurer: string;
  policyNumber: string;
  policyType: string;
  premium: string;
  premiumFrequency: "Monthly" | "Quarterly" | "Half-yearly" | "Annual";
  sumAssured: string;
  currentValue: string;
  maturityDate: string;
  maturityValue: string;
  source: "manual" | "pdf";
};

export type InsurancePolicyDraft = Omit<InsurancePolicy, "id" | "source"> & {
  id?: string;
  source?: InsurancePolicy["source"];
};

export const emptyInsurancePolicy: InsurancePolicyDraft = {
  policyName: "",
  insurer: "",
  policyNumber: "",
  policyType: "",
  premium: "",
  premiumFrequency: "Monthly",
  sumAssured: "",
  currentValue: "",
  maturityDate: "",
  maturityValue: "",
  source: "manual",
};
