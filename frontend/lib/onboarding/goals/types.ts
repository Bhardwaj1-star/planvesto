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

export const goalStatuses = ["Active", "Completed", "Paused", "Cancelled"] as const;
export type GoalStatus = (typeof goalStatuses)[number];
export type FundingStatus = "Shortfall" | "On Track" | "Overfunded";
export type AssetMappingAllocationType = "currency" | "percentage";
export const returnFrequencies = ["annual", "semi-annual", "quarterly", "monthly"] as const;
export type ReturnFrequency = (typeof returnFrequencies)[number];

export type AssetMappingInput = {
  asset_id: string;
  allocation_type: AssetMappingAllocationType;
  allocation_value: number;
  expected_return: number | null;
  return_frequency: string;
};

export type GoalInput = {
  planning_unit_id: string;
  goal_id?: string | null;
  investor_id?: string | null;
  goal_name: string;
  goal_type: string;
  today_cost: number;
  target_month: number;
  target_year: number;
  inflation_rate: number | null;
  priority: string;
  flexibility: string;
  status: string;
  asset_mappings: AssetMappingInput[];
  specialized_data?: Record<string, unknown>;
};

export type DefinedGoalAssetMapping = {
  mapping_id?: string | null;
  defined_goal_id?: string | null;
  asset_id: string;
  asset_name?: string | null;
  allocation_type: AssetMappingAllocationType;
  allocation_value: number;
  allocated_amount: number;
  allocated_percentage: number;
  expected_return: number;
  return_frequency: string;
  projected_value: number;
  created_at?: string | null;
};

export type DefinedGoal = {
  defined_goal_id?: string | null;
  goal_id: string;
  planning_unit_id: string;
  investor_id?: string | null;
  version: number;
  is_latest: boolean;
  goal_type: string;
  goal_name: string;
  today_cost: number;
  inflation_rate: number;
  inflation_source: string;
  target_month: number;
  target_year: number;
  duration_years: number;
  future_target: number;
  priority: string;
  flexibility: string;
  status: string;
  mapped_assets: DefinedGoalAssetMapping[];
  projected_mapped_asset_value: number;
  funding_gap: number;
  funding_status: FundingStatus;
  version_metadata?: Record<string, unknown>;
  created_at?: string | null;
};