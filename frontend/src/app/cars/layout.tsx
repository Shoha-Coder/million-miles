"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

import { useAuthStore } from "@/features/auth";
import { Button }       from "@/shared/ui/Button";
import { ROUTES }       from "@/shared/config/routes";

export default function CarsLayout({ children }: { children: React.ReactNode }) {
  const token  = useAuthStore((s) => s.token);
  const logout = useAuthStore((s) => s.logout);
  const router = useRouter();

  // Client-side auth guard — redirect to login if no token
  useEffect(() => {
    if (!token) router.replace(ROUTES.login);
  }, [token, router]);

  if (!token) return null;

  return (
    <div className="min-h-screen flex flex-col">
      {/* Top nav */}
      <header className="sticky top-0 z-10 bg-white border-b border-gray-200 shadow-sm">
        <div className="mx-auto flex h-14 max-w-screen-xl items-center justify-between px-4 sm:px-6">
          <Link href={ROUTES.cars} className="text-lg font-bold text-gray-900">
            Million Miles
          </Link>
          <Button variant="ghost" size="sm" onClick={logout}>
            Sign out
          </Button>
        </div>
      </header>

      <main className="flex-1">
        {children}
      </main>
    </div>
  );
}
