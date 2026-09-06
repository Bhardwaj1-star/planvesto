export const incomeTypes = [
  "Salary",
  "Business",
  "Professional/Freelance",
  "Rental",
  "Interest",
  "Dividend",
  "Pension",
  "Other",
] as const;
export const incomeFrequencies = ["Monthly", "Annual"] as const;

export type IncomeType = (typeof incomeTypes)[number];
export type IncomeFrequency = (typeof incomeFrequencies)[number];

export type IncomeSource = {
  id: string;
  incomeType: IncomeType | "";
  amount: string;
  frequency: IncomeFrequency | "";
  expectedAnnualGrowth: string;
};

export type IncomeSourceField = keyof Omit<IncomeSource, "id">;
export type IncomeSourceErrors = Partial<Record<IncomeSourceField, string>>;

export const emptyIncomeSource: Omit<IncomeSource, "id"> = {
  incomeType: "",
  amount: "",
  frequency: "",
  expectedAnnualGrowth: "",
};