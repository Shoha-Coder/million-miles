export const ROUTES = {
  login: "/login",
  cars:  "/cars",
  car:   (id: string) => `/cars/${id}`,
} as const;
