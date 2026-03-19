"use client";

import { type FormEvent, useRef } from "react";

import { Button } from "@/shared/ui/Button";
import { Input }  from "@/shared/ui/Input";
import { useLogin } from "../model/useLogin";

export function LoginForm() {
  const { submit, error, loading } = useLogin();
  const usernameRef = useRef<HTMLInputElement>(null);
  const passwordRef = useRef<HTMLInputElement>(null);

  function handleSubmit(e: FormEvent) {
    e.preventDefault();
    const username = usernameRef.current?.value.trim() ?? "";
    const password = passwordRef.current?.value ?? "";
    if (username && password) submit(username, password);
  }

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-4">
      <Input
        ref={usernameRef}
        id="username"
        label="Username"
        type="text"
        autoComplete="username"
        placeholder="admin"
        required
      />
      <Input
        ref={passwordRef}
        id="password"
        label="Password"
        type="password"
        autoComplete="current-password"
        placeholder="••••••••"
        required
        error={error ?? undefined}
      />
      <Button type="submit" size="lg" loading={loading} className="mt-2 w-full">
        Sign in
      </Button>
    </form>
  );
}
