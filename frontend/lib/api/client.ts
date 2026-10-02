import { supabase } from "../supabase";

/**
 * Structured error for API responses with non-ok status codes.
 * Extends `Error` so existing `catch` blocks that check `.message` remain compatible.
 */
type ApiErrorDetail = unknown;

function formatApiErrorDetail(detail: ApiErrorDetail, fallback: string): string {
  if (typeof detail === "string" && detail.trim()) return detail;
  if (detail && typeof detail === "object") {
    const value = detail as Record<string, unknown>;
    const message = typeof value.message === "string" ? value.message.trim() : "";
    const constraints = Array.isArray(value.constraints)
      ? value.constraints
          .map((constraint) => {
            if (!constraint || typeof constraint !== "object") return null;
            const item = constraint as Record<string, unknown>;
            return typeof item.message === "string" ? item.message.trim() : null;
          })
          .filter((item): item is string => Boolean(item))
      : [];
    const readable = [message, ...constraints].filter(Boolean).join(" ");
    if (readable) return readable;
    try {
      const serialized = JSON.stringify(detail);
      if (serialized && serialized !== "{}") return serialized;
    } catch {
      // Keep the HTTP fallback below.
    }
  }
  return fallback;
}

export class ApiError extends Error {
  constructor(
    message: string,
    public readonly status: number,
    public readonly detail: string | null,
    public readonly rawDetail: ApiErrorDetail = null,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL;
const DEFAULT_TIMEOUT_MS = 30_000;

function isAbortError(error: unknown): boolean {
  return error instanceof DOMException && error.name === "AbortError";
}

async function getSessionWithRetry(retries = 3) {
  for (let attempt = 0; attempt < retries; attempt += 1) {
    try {
      return await supabase.auth.getSession();
    } catch (error) {
      if (!isAbortError(error) || attempt === retries - 1) throw error;
      await new Promise((resolve) => setTimeout(resolve, 150 * (attempt + 1)));
    }
  }
  throw new Error("Unable to read authentication session.");
}

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

  const { data, error } = await getSessionWithRetry();
  if (error) throw error;
  if (!data.session) throw new Error("Authentication required.");

  const timeout = options?.timeout ?? DEFAULT_TIMEOUT_MS;
  const controller = timeout > 0 ? new AbortController() : null;
  const timer = controller ? setTimeout(() => controller.abort(), timeout) : null;

  try {
    const response = await fetch(`${BACKEND_URL}${path}`, {
      ...init,
      signal: init?.signal ?? controller?.signal ?? undefined,
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
      const rawDetail =
        typeof body === "object" && body !== null && "detail" in body
          ? (body as { detail: unknown }).detail
          : null;
      const detail = formatApiErrorDetail(rawDetail, `Request failed with status ${response.status}.`);
      throw new ApiError(detail, response.status, detail, rawDetail);
    }

    return body as T;
  } finally {
    if (timer !== null) clearTimeout(timer);
  }
}

/**
 * Centralized API request function for binary responses (e.g. PDFs).
 */
export async function apiRequestBlob(
  path: string,
  init?: RequestInit,
  options?: { timeout?: number },
): Promise<Blob> {
  if (!BACKEND_URL) throw new Error("Backend URL is not configured.");

  const { data, error } = await getSessionWithRetry();
  if (error) throw error;
  if (!data.session) throw new Error("Authentication required.");

  const timeout = options?.timeout ?? DEFAULT_TIMEOUT_MS;
  const controller = timeout > 0 ? new AbortController() : null;
  const timer = controller ? setTimeout(() => controller.abort(), timeout) : null;

  try {
    const response = await fetch(`${BACKEND_URL}${path}`, {
      ...init,
      signal: init?.signal ?? controller?.signal ?? undefined,
      headers: {
        Authorization: `Bearer ${data.session.access_token}`,
        ...(init?.headers ?? {}),
      },
    });

    if (!response.ok) {
      let detail = `Request failed with status ${response.status}.`;
      let rawDetail: ApiErrorDetail = null;
      try {
        const body = await response.json();
        if (typeof body === "object" && body !== null && "detail" in body) {
          rawDetail = (body as { detail: unknown }).detail;
          detail = formatApiErrorDetail(rawDetail, detail);
        }
      } catch {
        // Non-JSON server error
      }
      throw new ApiError(detail, response.status, detail, rawDetail);
    }

    return await response.blob();
  } finally {
    if (timer !== null) clearTimeout(timer);
  }
}

/**
 * Read the active planning unit ID from localStorage.
 * Supports the legacy underscore key during migration.
 */
export function getPlanningUnitId(): string | null {
  if (typeof window === "undefined") return null;
  return (
    window.localStorage.getItem("planvesto-planning-unit-id") ??
    window.localStorage.getItem("planvesto_planning_unit_id")
  );
}
