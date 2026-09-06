export const expenseCategories = [
  "Housing",
  "Food & Groceries",
  "Utilities",
  "Transportation",
  "Education",
  "Healthcare",
  "Insurance",
  "Debt Payments",
  "Family Support",
  "Travel",
  "Entertainment",
  "Shopping",
  "Other",
] as const;
export const expenseFrequencies = ["Monthly", "Annual"] as const;

export type ExpenseCategory = (typeof expenseCategories)[number];
export type ExpenseFrequency = (typeof expenseFrequencies)[number];

export type Expense = {
  id: string;
  category: ExpenseCategory | "";
  amount: string;
  frequency: ExpenseFrequency | "";
};

export type ExpenseField = keyof Omit<Expense, "id">;
export type ExpenseErrors = Partial<Record<ExpenseField, string>>;

export const emptyExpense: Omit<Expense, "id"> = {
  category: "",
  amount: "",
  frequency: "",
};