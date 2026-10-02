import { supabase } from "./supabase";

const planningUnitStorageKey = "planvesto-planning-unit-id";
let planningUnitPromise: Promise<string> | null = null;
let planningUnitUserId: string | null = null;

async function getAuthenticatedUser() {
  const { data, error } = await supabase.auth.getUser();
  if (error) throw error;
  if (!data.user) throw new Error("You must be signed in to access planning data.");
  return data.user;
}

function isUuid(value: string) {
  return /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(value);
}

export async function getPlanningUnitId(): Promise<string> {
  const user = await getAuthenticatedUser();
  if (planningUnitPromise && planningUnitUserId === user.id) return planningUnitPromise;

  planningUnitUserId = user.id;
  planningUnitPromise = (async (): Promise<string> => {
    const storedId = typeof window !== "undefined"
      ? window.localStorage.getItem(planningUnitStorageKey)
      : null;

    const { data: userUnits, error: unitsError } = await supabase
      .from("planning_units")
      .select("planning_unit_id")
      .eq("user_id", user.id)
      .order("planning_unit_id", { ascending: true });

    if (unitsError) throw unitsError;

    const unitIds = (userUnits || []).map((unit) => unit.planning_unit_id);
    let chosenId: string | null = null;

    if (storedId && isUuid(storedId) && unitIds.includes(storedId)) {
      chosenId = storedId;
    }

    if (unitIds.length) {
      const { data: investor, error: investorError } = await supabase
        .from("investors")
        .select("planning_unit_id")
        .in("planning_unit_id", unitIds)
        .order("planning_unit_id", { ascending: true })
        .limit(1)
        .maybeSingle();

      if (investorError) throw investorError;

      if (investor?.planning_unit_id) {
        chosenId = investor.planning_unit_id;
      } else if (!chosenId) {
        chosenId = unitIds[0];
      }
    }

    if (!chosenId) {
      const { data: newUnit, error: newUnitError } = await supabase
        .from("planning_units")
        .insert({ user_id: user.id })
        .select("planning_unit_id")
        .single();

      if (newUnitError) throw newUnitError;
      chosenId = newUnit.planning_unit_id;
    }

    if (typeof window !== "undefined") {
      window.localStorage.setItem(planningUnitStorageKey, chosenId);
    }

    return chosenId;
  })();

  try {
    return await planningUnitPromise;
  } catch (error) {
    planningUnitPromise = null;
    planningUnitUserId = null;
    throw error;
  }
}
