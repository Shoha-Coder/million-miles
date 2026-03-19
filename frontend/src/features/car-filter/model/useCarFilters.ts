"use client";

import { useCallback, useState } from "react";
import type { CarListParams } from "@/entities/car/model/types";

export interface FilterState {
  make:        string;
  body_type:   string;
  fuel_type:   string;
  year_min:    string;
  year_max:    string;
  price_min:   string;
  price_max:   string;
  mileage_max: string;
  sort:        CarListParams["sort"];
  order:       CarListParams["order"];
}

const DEFAULT_FILTERS: FilterState = {
  make:        "",
  body_type:   "",
  fuel_type:   "",
  year_min:    "",
  year_max:    "",
  price_min:   "",
  price_max:   "",
  mileage_max: "",
  sort:        "scraped_at",
  order:       "desc",
};

export function useCarFilters() {
  const [filters, setFilters] = useState<FilterState>(DEFAULT_FILTERS);
  const [page, setPage]       = useState(1);

  const updateFilter = useCallback((key: keyof FilterState, value: string) => {
    setFilters((prev) => ({ ...prev, [key]: value }));
    setPage(1); // reset to first page on filter change
  }, []);

  const resetFilters = useCallback(() => {
    setFilters(DEFAULT_FILTERS);
    setPage(1);
  }, []);

  // Convert string filter state to API params (drop empty strings)
  const toApiParams = useCallback((): CarListParams => {
    const params: CarListParams = { page, limit: 20 };
    if (filters.make)        params.make        = filters.make;
    if (filters.body_type)   params.body_type   = filters.body_type;
    if (filters.fuel_type)   params.fuel_type   = filters.fuel_type;
    if (filters.year_min)    params.year_min    = Number(filters.year_min);
    if (filters.year_max)    params.year_max    = Number(filters.year_max);
    if (filters.price_min)   params.price_min   = Number(filters.price_min);
    if (filters.price_max)   params.price_max   = Number(filters.price_max);
    if (filters.mileage_max) params.mileage_max = Number(filters.mileage_max);
    if (filters.sort)        params.sort        = filters.sort;
    if (filters.order)       params.order       = filters.order;
    return params;
  }, [filters, page]);

  return { filters, page, updateFilter, resetFilters, setPage, toApiParams };
}
