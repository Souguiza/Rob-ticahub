import { createContext, ReactNode, useContext, useEffect, useMemo, useState } from "react";

import { api } from "../services/api";
import type { User } from "../types/api";

interface LoginPayload {
  email: string;
  password: string;
}

interface RegisterPayload extends LoginPayload {
  full_name: string;
  city?: string;
  state?: string;
  country: string;
  interests: string[];
  robotics_programs: string[];
  accepted_terms: boolean;
  privacy_consent: boolean;
}

interface AuthContextValue {
  user: User | null;
  loading: boolean;
  login: (payload: LoginPayload) => Promise<void>;
  register: (payload: RegisterPayload) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  async function loadMe() {
    const access = localStorage.getItem("roboticahub.access");
    if (!access) {
      setLoading(false);
      return;
    }
    try {
      const response = await api.get<User>("/auth/me/");
      setUser(response.data);
    } catch {
      localStorage.removeItem("roboticahub.access");
      localStorage.removeItem("roboticahub.refresh");
      setUser(null);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void loadMe();
  }, []);

  async function login(payload: LoginPayload) {
    const response = await api.post<{ access: string; refresh: string }>("/auth/login/", payload);
    localStorage.setItem("roboticahub.access", response.data.access);
    localStorage.setItem("roboticahub.refresh", response.data.refresh);
    await loadMe();
  }

  async function register(payload: RegisterPayload) {
    await api.post("/auth/register/", payload);
    await login({ email: payload.email, password: payload.password });
  }

  function logout() {
    localStorage.removeItem("roboticahub.access");
    localStorage.removeItem("roboticahub.refresh");
    setUser(null);
  }

  const value = useMemo(() => ({ user, loading, login, register, logout }), [user, loading]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth precisa estar dentro de AuthProvider");
  }
  return context;
}
