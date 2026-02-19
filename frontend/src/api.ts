import { FindingsSummary, SecurityFinding } from "./types";

const REQUEST_TIMEOUT_MS = 12000;

function resolveApiBaseUrl(): string {
  const configured = import.meta.env.VITE_API_BASE_URL?.toString().trim();
  const runtimeHost = window.location.hostname || "localhost";
  const runtimeProtocol = window.location.protocol || "http:";
  const isLocalHost = runtimeHost === "localhost" || runtimeHost === "127.0.0.1";
  const runtimeDefault = isLocalHost
    ? `${runtimeProtocol}//${runtimeHost}:8080`
    : window.location.origin;

  if (!configured) {
    return runtimeDefault;
  }

  if (
    runtimeHost !== "localhost" &&
    runtimeHost !== "127.0.0.1" &&
    (configured.includes("localhost") || configured.includes("127.0.0.1"))
  ) {
    return configured
      .replace("localhost", runtimeHost)
      .replace("127.0.0.1", runtimeHost);
  }

  return configured;
}

export const API_BASE_URL = resolveApiBaseUrl();

async function fetchJson<T>(path: string): Promise<T> {
  const controller = new AbortController();
  const timeoutId = window.setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);

  try {
    const response = await fetch(`${API_BASE_URL}${path}`, {
      signal: controller.signal,
      mode: "cors",
    });
    if (!response.ok) {
      throw new Error(`Request failed for ${path}: ${response.status}`);
    }
    return response.json() as Promise<T>;
  } catch (error) {
    if (error instanceof DOMException && error.name === "AbortError") {
      throw new Error(`Request timed out for ${path} after ${REQUEST_TIMEOUT_MS / 1000}s`);
    }
    throw error;
  } finally {
    window.clearTimeout(timeoutId);
  }
}

export function getSummary(): Promise<FindingsSummary> {
  return fetchJson<FindingsSummary>("/api/v1/summary");
}

export function getFindings(limit = 200): Promise<SecurityFinding[]> {
  return fetchJson<SecurityFinding[]>(`/api/v1/findings?limit=${limit}`);
}
