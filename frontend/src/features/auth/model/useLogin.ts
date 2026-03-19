"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

import { login } from "@/shared/api/auth";
import { ROUTES } from "@/shared/config/routes";
import { useAuthStore } from "./store";

export function useLogin() {
  const [error, setError]     = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const setTokens             = useAuthStore((s) => s.setTokens);
  const router                = useRouter();

  async function submit(username: string, password: string) {
    setError(null);
    setLoading(true);
    try {
      const { access_token, refresh_token } = await login({ username, password });
      setTokens(access_token, refresh_token);
      router.push(ROUTES.cars);
    } catch {
      setError("Wrong username or password");
    } finally {
      setLoading(false);
    }
  }

  return { submit, error, loading };
}
