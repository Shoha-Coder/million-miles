import { create } from "zustand";
import { createJSONStorage, persist } from "zustand/middleware";

interface AuthStore {
  token: string | null;
  setToken: (token: string) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthStore>()(
  persist(
    (set) => ({
      token: null,
      setToken: (token) => set({ token }),
      logout: () => {
        set({ token: null });
        if (typeof window !== "undefined") {
          localStorage.removeItem("token");
        }
      },
    }),
    {
      name: "token",
      // Lazy localStorage — only accessed on the client, never during SSR
      storage: createJSONStorage(() => {
        if (typeof window === "undefined") {
          // Return a no-op storage for the server render pass
          return {
            getItem: () => null,
            setItem: () => {},
            removeItem: () => {},
          };
        }
        return localStorage;
      }),
      partialize: (state) => ({ token: state.token }),
      // Let SSR render with token=null; rehydrate runs after mount on the client
      skipHydration: true,
    },
  ),
);
