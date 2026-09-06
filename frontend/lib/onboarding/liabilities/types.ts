export const liabilityTypes = [
  "Home Loan",
  "Car Loan",
  "Personal Loan",
  "Education Loan",
  "Business Loan",
  "Credit Card",
  "Other",
] as const;
export const liabilityFrequencies = ["Monthly", "Quarterly", "Annual"] as const;

export type LiabilityType = (typeof liabilityTypes)[number];
export type LiabilityFrequency = (typeof liabilityFrequencies)[number];

export type Liability = {
  id: string;
  liabilityType: LiabilityType | "";
  description: string;
  outstandingAmount: string;
  interestRate: string;
  regularPayment: string;
  frequency: LiabilityFrequency | "";
  endDate: string;
};

export type LiabilityField = keyof Omit<Liability, "id">;
export type LiabilityErrors = Partial<Record<LiabilityField, string>>;

export const emptyLiability: Omit<Liability, "id"> = {
  liabilityType: "",
  description: "",
  outstandingAmount: "",
  interestRate: "",
  regularPayment: "",
  frequency: "Monthly",
  endDate: "",
};