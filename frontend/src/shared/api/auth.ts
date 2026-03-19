import { apiClient } from "./client";

interface LoginPayload {
  username: string;
  password: string;
}

export interface TokenResponse {
  access_token:  string;
  refresh_token: string;
  token_type:    string;
  expires_in:    number;
}

export async function login(payload: LoginPayload): Promise<TokenResponse> {
  const { data } = await apiClient.post<TokenResponse>("/auth/login", payload);
  return data;
}

export async function rotateTokens(refreshToken: string): Promise<TokenResponse> {
  const { data } = await apiClient.post<TokenResponse>(
    "/auth/refresh",
    null,
    { headers: { Authorization: `Bearer ${refreshToken}` } },
  );
  return data;
}
