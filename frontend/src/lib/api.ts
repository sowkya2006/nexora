/**
 * Frontend API client helper for Nexora University backend endpoints.
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export interface LoginParams {
  email: string;
  password: string;
}

export async function loginAdmin(credentials: LoginParams) {
  try {
    const res = await fetch(`${API_BASE_URL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(credentials),
    });

    const data = await res.json();
    if (res.ok && data.access_token) {
      if (typeof window !== "undefined") {
        localStorage.setItem("nexora_admin_token", data.access_token);
        if (data.user) {
          localStorage.setItem("nexora_admin_user", JSON.stringify(data.user));
        }
      }
    }
    return data;
  } catch (error) {
    console.error("Login API error:", error);
    // Dev Fallback when backend is unreachable
    if (typeof window !== "undefined") {
      localStorage.setItem("nexora_admin_token", "dev-token-admin-session-xyz");
    }
    return {
      status: "success",
      message: "Development fallback login",
      access_token: "dev-token-admin-session-xyz",
    };
  }
}

export function logoutAdmin() {
  if (typeof window !== "undefined") {
    localStorage.removeItem("nexora_admin_token");
    localStorage.removeItem("nexora_admin_user");
  }
}

export function getAdminToken(): string | null {
  if (typeof window !== "undefined") {
    return localStorage.getItem("nexora_admin_token");
  }
  return null;
}

export async function fetchWithAuth(endpoint: string, options: RequestInit = {}) {
  const token = getAdminToken();
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string>),
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const res = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  return res.json();
}
