import { supabase } from "../supabase";

const DIRECT_TABLES = ["investors", "income", "expenses", "assets", "liabilities", "goals"] as const;
const RELATION_TABLES = ["asset_owners", "liability_responsibilities", "expense_participants"] as const;

type Cleanup = () => void;

export function subscribeToFinancialChanges(
  planningUnitId: string,
  onChange: () => void,
): Cleanup {
  const channel = supabase.channel(`dashboard:${planningUnitId}`);
  let timer: ReturnType<typeof setTimeout> | null = null;

  const refresh = () => {
    if (timer) clearTimeout(timer);
    timer = setTimeout(onChange, 350);
  };

  for (const table of DIRECT_TABLES) {
    channel.on(
      "postgres_changes",
      {
        event: "*",
        schema: "public",
        table,
        filter: `planning_unit_id=eq.${planningUnitId}`,
      },
      refresh,
    );
  }

  // These child tables do not carry planning_unit_id. RLS must scope them to the
  // signed-in planning unit; any change can affect the derived financial state.
  for (const table of RELATION_TABLES) {
    channel.on(
      "postgres_changes",
      { event: "*", schema: "public", table },
      refresh,
    );
  }

  channel.subscribe();

  return () => {
    if (timer) clearTimeout(timer);
    void supabase.removeChannel(channel);
  };
}
