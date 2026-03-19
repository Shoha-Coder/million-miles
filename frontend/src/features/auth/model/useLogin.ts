"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

import { login } from "@/shared/api/auth";
import { ROUTES } from "@/shared/config/routes";
import { useAuthStore } from "./store";

export function useLogin() {
  const [error, setError]     = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const setToken              = useAuthStore((s) => s.setToken);
  const router                = useRouter();

  async function submit(username: string, password: string) {
    setError(null);
    setLoading(true);
    try {
      const { access_token } = await login({ username, password });
      // Store in Zustand (persisted) and in localStorage for the axios interceptor
      setToken(access_token);
      localStorage.setItem("token", access_token);
      router.push(ROUTES.cars);
    } catch {
      setError("Wrong username or password");
    } finally {
      setLoading(false);
    }
  }

  return { submit, error, loading };
}
