const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export class ApiError extends Error {
  constructor(message: string, public readonly status: number) {
    super(message);
    this.name = "ApiError";
  }
}

export async function apiRequest<T>(path: string, init: RequestInit = {}): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    credentials: "include",
    headers: { "Content-Type": "application/json", ...init.headers },
  });
  if (!response.ok) {
    const payload: unknown = await response.json().catch(() => null);
    const message = typeof payload === "object" && payload !== null && "detail" in payload && typeof payload.detail === "string"
      ? payload.detail
      : `Request failed (${response.status})`;
    throw new ApiError(message, response.status);
  }
  return response.json() as Promise<T>;
}
