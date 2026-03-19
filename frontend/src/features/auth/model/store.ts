import { create } from "zustand";
import { createJSONStorage, persist } from "zustand/middleware";

interface AuthStore {
  token:        string | null;
  refreshToken: string | null;
  /** true once localStorage has been read — guards against flash-redirect on refresh */
  hydrated:     boolean;
  setTokens:    (access: string, refresh: string) => void;
  logout:       () => void;
}

export const useAuthStore = create<AuthStore>()(
  persist(
    (set) => ({
      token:        null,
      refreshToken: null,
      hydrated:     false,
      setTokens: (access, refresh) => {
        set({ token: access, refreshToken: refresh });
        // Keep localStorage in sync for the axios interceptor
        localStorage.setItem("token", access);
        localStorage.setItem("refresh_token", refresh);
      },
      logout: () => {
        set({ token: null, refreshToken: null });
        if (typeof window !== "undefined") {
          localStorage.removeItem("token");
          localStorage.removeItem("refresh_token");
        }
      },
    }),
    {
      name: "auth",
      // Lazy localStorage — no-op on the server, real storage on the client
      storage: createJSONStorage(() => {
        if (typeof window === "undefined") {
          return { getItem: () => null, setItem: () => {}, removeItem: () => {} };
        }
        return localStorage;
      }),
      partialize: (state) => ({ token: state.token, refreshToken: state.refreshToken }),
      skipHydration: true,
      // Flip hydrated=true once localStorage has been read — lets the auth guard wait
      onRehydrateStorage: () => () => {
        useAuthStore.setState({ hydrated: true });
      },
    },
  ),
);
