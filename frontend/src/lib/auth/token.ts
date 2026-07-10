import { apiClient } from "@/lib/api/client";

const TOKEN_KEY = "token";

async function loginAndStoreToken(): Promise<string> {
  const response = await apiClient.post<{ access_token: string }>("/auth/login", {
    username: "admin",
    password: "admin",
  });
  localStorage.setItem(TOKEN_KEY, response.data.access_token);
  return response.data.access_token;
}

export async function getAuthToken(): Promise<string> {
  if (typeof window === "undefined") return "";

  // Always refresh the temporary development token. This avoids stale JWTs after
  // container rebuilds or SECRET_KEY changes, which otherwise produce
  // "Invalid token" on dashboard actions.
  return await loginAndStoreToken();
}

export async function authHeaders(): Promise<{ Authorization: string }> {
  const token = await getAuthToken();
  return { Authorization: `Bearer ${token}` };
}

export function clearAuthToken(): void {
  if (typeof window !== "undefined") localStorage.removeItem(TOKEN_KEY);
}
