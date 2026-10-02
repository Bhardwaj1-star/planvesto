export function withReturnTo(route: string, returnTo: string | null | undefined): string {
  if (!returnTo) return route;
  const separator = route.includes("?") ? "&" : "?";
  return `${route}${separator}returnTo=${encodeURIComponent(returnTo)}`;
}