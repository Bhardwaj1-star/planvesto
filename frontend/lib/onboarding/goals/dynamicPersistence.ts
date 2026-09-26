import { supabase } from "../../supabase";
import type { Goal } from "./types";

export async function saveDynamicGoalDetails(goalId: string, goal: Goal) {
  const goalName = goal.goalType === "Others"
    ? goal.dynamicDetails.otherGoalName.trim()
    : goal.goalType;

  const { error } = await supabase
    .from("goals")
    .update({
      goal_name: goalName || goal.name || goal.goalType,
      goal_type: goal.goalType || null,
      dynamic_details: goal.dynamicDetails,
    } as never)
    .eq("goal_id", goalId);

  if (error) throw error;
}

export async function saveDynamicGoalDetailsForList(savedGoals: Goal[], sourceGoals: Goal[]) {
  await Promise.all(
    savedGoals.map((saved, index) => {
      const source = sourceGoals[index];
      return source ? saveDynamicGoalDetails(saved.id, source) : Promise.resolve();
    }),
  );
}
