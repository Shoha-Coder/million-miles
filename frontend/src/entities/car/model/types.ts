export interface Car {
  id: string;
  make: string;
  model: string;
  grade: string;
  year: number;
  mileage: number;
  price: number;
  body_price: number;
  color: string;
  engine_cc: number | null;
  transmission: string;
  body_type: string;
  fuel_type: string;
  drivetrain: string;
  doors: number | null;
  seats: number | null;
  repair_history: boolean;
  inspection_date: string | null;
  prefecture: string;
  dealer_name: string;
  photos: string[];
  features: string[];
  scraped_at: string | null;
  created_at: string | null;
  updated_at: string | null;
}

export interface CarListResponse {
  total: number;
  page: number;
  limit: number;
  pages: number;
  items: Car[];
}

export interface CarListParams {
  make?: string;
  body_type?: string;
  fuel_type?: string;
  year_min?: number;
  year_max?: number;
  price_min?: number;
  price_max?: number;
  mileage_max?: number;
  sort?: "price" | "year" | "mileage" | "scraped_at";
  order?: "asc" | "desc";
  page?: number;
  limit?: number;
}
