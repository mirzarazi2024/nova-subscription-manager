import { apiClient } from "@/lib/api/client";

const TOKEN_KEY = "token";

export async function getAuthToken(): Promise<string> {
  if (typeof window === "undefined") return "";

  const existing = localStorage.getItem(TOKEN_KEY);
  if (existing) return existing;

  const response = await apiClient.post<{ access_token: string }>("/auth/login", {
    username: "admin",
    password: "admin",
  });
  localStorage.setItem(TOKEN_KEY, response.data.access_token);
  return response.data.access_token;
}

export async function authHeaders(): Promise<{ Authorization: string }> {
  const token = await getAuthToken();
  return { Authorization: `Bearer ${token}` };
}
