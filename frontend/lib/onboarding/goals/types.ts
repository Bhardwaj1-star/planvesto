export const goalTypes = [
  "Emergency Fund",
  "Child Education",
  "Child Marriage",
  "Home Purchase",
  "Vehicle",
  "Retirement",
  "Travel",
  "Business",
  "Wealth Creation",
  "Other",
] as const;
export const goalPriorities = ["Critical", "Important", "Aspirational"] as const;
export const goalFlexibilities = ["Fixed", "Flexible"] as const;
export const targetModes = ["Date", "Age"] as const;
export const inflationOptions = ["Yes", "No"] as const;

export type GoalType = (typeof goalTypes)[number];
export type GoalPriority = (typeof goalPriorities)[number];
export type GoalFlexibility = (typeof goalFlexibilities)[number];
export type TargetMode = (typeof targetModes)[number];
export type InflationOption = (typeof inflationOptions)[number];

export type Goal = {
  id: string;
  name: string;
  goalType: GoalType | "";
  targetAmount: string;
  targetMode: TargetMode | "";
  targetDate: string;
  targetAge: string;
  currentSavedAmount: string;
  monthlyContribution: string;
  priority: GoalPriority | "";
  flexibility: GoalFlexibility | "";
  inflationApplicability: InflationOption | "";
  notes: string;
};

export type GoalField = keyof Omit<Goal, "id">;
export type GoalErrors = Partial<Record<GoalField, string>>;

export const emptyGoal: Omit<Goal, "id"> = {
  name: "",
  goalType: "",
  targetAmount: "",
  targetMode: "",
  targetDate: "",
  targetAge: "",
  currentSavedAmount: "",
  monthlyContribution: "",
  priority: "",
  flexibility: "",
  inflationApplicability: "",
  notes: "",
};