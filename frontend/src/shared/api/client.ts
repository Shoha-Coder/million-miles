import axios, { type InternalAxiosRequestConfig } from "axios";

import { API_URL } from "@/shared/config/env";

export const apiClient = axios.create({
  baseURL: API_URL,
  headers: { "Content-Type": "application/json" },
});

// Attach the access token to every outgoing request
apiClient.interceptors.request.use((config) => {
  if (typeof window !== "undefined") {
    const token = localStorage.getItem("token");
    if (token) config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Queue of requests that arrived while a token refresh was in flight
type QueueEntry = { resolve: (token: string) => void; reject: (err: unknown) => void };
let refreshing = false;
let queue: QueueEntry[] = [];

function drainQueue(token: string | null, err: unknown) {
  queue.forEach((entry) => (token ? entry.resolve(token) : entry.reject(err)));
  queue = [];
}

function clearSession() {
  localStorage.removeItem("token");
  localStorage.removeItem("refresh_token");
  window.location.href = "/login";
}

// Silent token refresh on 401 — retry the original request with the new token
apiClient.interceptors.response.use(
  (res) => res,
  async (err) => {
    const original = err.config as InternalAxiosRequestConfig & { _retry?: boolean };

    // Don't try to refresh if the refresh call itself failed, or it's not a 401
    if (err.response?.status !== 401 || original._retry || typeof window === "undefined") {
      return Promise.reject(err);
    }

    // Requests that land here while a refresh is already running go into the queue
    if (refreshing) {
      return new Promise<string>((resolve, reject) => queue.push({ resolve, reject }))
        .then((token) => {
          original.headers.Authorization = `Bearer ${token}`;
          return apiClient(original);
        });
    }

    original._retry = true;
    refreshing      = true;

    const stored = localStorage.getItem("refresh_token");
    if (!stored) {
      drainQueue(null, err);
      clearSession();
      return Promise.reject(err);
    }

    try {
      // Import here to avoid a circular module dependency
      const { rotateTokens } = await import("./auth");
      const tokens = await rotateTokens(stored);

      localStorage.setItem("token", tokens.access_token);
      localStorage.setItem("refresh_token", tokens.refresh_token);

      original.headers.Authorization = `Bearer ${tokens.access_token}`;
      drainQueue(tokens.access_token, null);
      return apiClient(original);
    } catch (refreshErr) {
      drainQueue(null, refreshErr);
      clearSession();
      return Promise.reject(refreshErr);
    } finally {
      refreshing = false;
    }
  },
);
