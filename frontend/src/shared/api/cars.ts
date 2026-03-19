import type { Car, CarListParams, CarListResponse } from "@/entities/car/model/types";
import { apiClient } from "./client";

export async function fetchCars(params: CarListParams): Promise<CarListResponse> {
  const { data } = await apiClient.get<CarListResponse>("/api/cars", { params });
  return data;
}

export async function fetchCar(id: string): Promise<Car> {
  const { data } = await apiClient.get<Car>(`/api/cars/${id}`);
  return data;
}
