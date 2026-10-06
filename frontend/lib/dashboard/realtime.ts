/**
 * Dashboard realtime is intentionally disabled for the browser.
 *
 * Supabase Postgres Changes can fail during WebSocket negotiation when Realtime
 * is unavailable or the project's publication/RLS configuration is incomplete.
 * That failure must never take down the financial-state page. The dashboard
 * still loads its canonical state through the authenticated HTTP API.
 *
 * Keep this adapter as a no-op so callers can opt into realtime again once the
 * Supabase Realtime configuration is verified.
 */

type Cleanup = () => void;

export function subscribeToFinancialChanges(
  _planningUnitId: string,
  _onChange: () => void,
): Cleanup {
  return () => undefined;
}
