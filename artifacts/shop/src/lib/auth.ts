import { useState } from "react";

export interface AuthUser {
  id: number;
  username: string;
  email: string;
}

function readStoredToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("token");
}

function readStoredUser(): AuthUser | null {
  if (typeof window === "undefined") return null;
  const storedUser = localStorage.getItem("user");
  if (!storedUser) return null;
  try {
    return JSON.parse(storedUser) as AuthUser;
  } catch {
    return null;
  }
}

export function useAuth() {
  const [token, setToken] = useState<string | null>(readStoredToken);
  const [user, setUser] = useState<AuthUser | null>(readStoredUser);

  const login = (newToken: string, newUser?: AuthUser) => {
    localStorage.setItem("token", newToken);
    setToken(newToken);
    if (newUser) {
      localStorage.setItem("user", JSON.stringify(newUser));
      setUser(newUser);
    }
  };

  const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    setToken(null);
    setUser(null);
  };

  return { token, user, isAuthenticated: !!token, login, logout };
}
