import { supabase } from "../supabase";

/**
 * Structured error for API responses with non-ok status codes.
 * Extends `Error` so existing `catch` blocks that check `.message` remain compatible.
 */
export class ApiError extends Error {
  constructor(
    message: string,
    public readonly status: number,
    public readonly detail: string | null,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL;
const DEFAULT_TIMEOUT_MS = 30_000;

/**
 * Centralized API request function.
 *
 * Handles:
 * - Backend base URL resolution
 * - Supabase auth token injection
 * - Default headers (Content-Type, Authorization)
 * - JSON response parsing (safe)
 * - Error normalization (extracts `detail` from FastAPI errors)
 * - Configurable timeout via AbortController
 */
export async function apiRequest<T>(
  path: string,
  init?: RequestInit,
  options?: { timeout?: number },
): Promise<T> {
  if (!BACKEND_URL) throw new Error("Backend URL is not configured.");

  const { data, error } = await supabase.auth.getSession();
  if (error) throw error;
  if (!data.session) throw new Error("Authentication required.");

  const timeout = options?.timeout ?? DEFAULT_TIMEOUT_MS;
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeout);

  try {
    const response = await fetch(`${BACKEND_URL}${path}`, {
      ...init,
      signal: init?.signal ?? controller.signal,
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${data.session.access_token}`,
        ...(init?.headers ?? {}),
      },
    });

    let body: unknown = null;
    try {
      body = await response.json();
    } catch {
      // Keep non-JSON server errors generic.
    }

    if (!response.ok) {
      const detail =
        typeof body === "object" && body !== null && "detail" in body
          ? String((body as { detail: unknown }).detail)
          : `Request failed with status ${response.status}.`;
      throw new ApiError(detail, response.status, detail);
    }

    return body as T;
  } finally {
    clearTimeout(timer);
  }
}

/**
 * Read the active planning unit ID from localStorage.
 * Returns null on the server or if unset.
 */
export function getPlanningUnitId(): string | null {
  if (typeof window === "undefined") return null;
  return window.localStorage.getItem("planvesto-planning-unit-id");
}
