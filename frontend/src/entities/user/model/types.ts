export interface User {
  username: string;
}

export interface AuthState {
  token: string | null;
  user: User | null;
}
