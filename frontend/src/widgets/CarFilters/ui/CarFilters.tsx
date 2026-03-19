"use client";

import { Button } from "@/shared/ui/Button";
import { Input }  from "@/shared/ui/Input";
import { Select } from "@/shared/ui/Select";
import type { FilterState } from "@/features/car-filter";

interface CarFiltersProps {
  filters:      FilterState;
  onChange:     (key: keyof FilterState, value: string) => void;
  onReset:      () => void;
  /** Mobile drawer open state */
  open?:        boolean;
  onClose?:     () => void;
}

const BODY_TYPES = [
  { value: "Sedan",     label: "Sedan" },
  { value: "Hatchback", label: "Hatchback" },
  { value: "SUV",       label: "SUV" },
  { value: "Wagon",     label: "Wagon" },
  { value: "Minivan",   label: "Minivan" },
  { value: "Coupe",     label: "Coupe" },
  { value: "Truck",     label: "Truck" },
];

const FUEL_TYPES = [
  { value: "Gasoline", label: "Gasoline" },
  { value: "Hybrid",   label: "Hybrid" },
  { value: "Electric", label: "Electric" },
  { value: "Diesel",   label: "Diesel" },
];

const SORT_OPTIONS = [
  { value: "scraped_at", label: "Newest first" },
  { value: "price",      label: "Price" },
  { value: "year",       label: "Year" },
  { value: "mileage",    label: "Mileage" },
];

const ORDER_OPTIONS = [
  { value: "desc", label: "High → Low" },
  { value: "asc",  label: "Low → High" },
];

export function CarFilters({ filters, onChange, onReset, open, onClose }: CarFiltersProps) {
  return (
    <>
      {/* Mobile overlay */}
      {open && (
        <div
          className="fixed inset-0 bg-black/40 z-20 lg:hidden"
          onClick={onClose}
          aria-hidden
        />
      )}

      <aside
        className={[
          // Base styles
          "flex flex-col gap-5 bg-white border-r border-gray-200 p-5 overflow-y-auto",
          // Desktop: always visible sidebar
          "lg:static lg:translate-x-0 lg:w-64 lg:shrink-0 lg:rounded-xl lg:shadow-none lg:border",
          // Mobile: fixed drawer slides in from left
          "fixed inset-y-0 left-0 w-72 z-30 shadow-xl transition-transform duration-300 lg:transition-none",
          open ? "translate-x-0" : "-translate-x-full",
        ].join(" ")}
      >
        <div className="flex items-center justify-between">
          <h2 className="text-sm font-semibold text-gray-900 uppercase tracking-wide">
            Filters
          </h2>
          {/* Close button — mobile only */}
          <button
            onClick={onClose}
            className="lg:hidden text-gray-400 hover:text-gray-600 p-1"
            aria-label="Close filters"
          >
            ✕
          </button>
        </div>

        {/* Sort */}
        <div className="flex flex-col gap-3 pb-4 border-b border-gray-100">
          <Select
            id="sort"
            label="Sort by"
            options={SORT_OPTIONS}
            value={filters.sort}
            onChange={(value) => onChange("sort", value)}
          />
          <Select
            id="order"
            label="Order"
            options={ORDER_OPTIONS}
            value={filters.order}
            onChange={(value) => onChange("order", value)}
          />
        </div>

        {/* Search */}
        <div className="flex flex-col gap-3 pb-4 border-b border-gray-100">
          <Input
            id="make"
            label="Make"
            placeholder="Toyota, Honda…"
            value={filters.make}
            onChange={(e) => onChange("make", e.target.value)}
          />
          <Select
            id="body_type"
            label="Body type"
            placeholder="All body types"
            options={BODY_TYPES}
            value={filters.body_type}
            onChange={(value) => onChange("body_type", value)}
          />
          <Select
            id="fuel_type"
            label="Fuel type"
            placeholder="All fuel types"
            options={FUEL_TYPES}
            value={filters.fuel_type}
            onChange={(value) => onChange("fuel_type", value)}
          />
        </div>

        {/* Year range */}
        <div className="flex flex-col gap-2 pb-4 border-b border-gray-100">
          <p className="text-sm font-medium text-gray-700">Year</p>
          <div className="flex gap-2">
            <Input
              id="year_min"
              placeholder="From"
              type="number"
              min={1990}
              max={2030}
              value={filters.year_min}
              onChange={(e) => onChange("year_min", e.target.value)}
            />
            <Input
              id="year_max"
              placeholder="To"
              type="number"
              min={1990}
              max={2030}
              value={filters.year_max}
              onChange={(e) => onChange("year_max", e.target.value)}
            />
          </div>
        </div>

        {/* Price range */}
        <div className="flex flex-col gap-2 pb-4 border-b border-gray-100">
          <p className="text-sm font-medium text-gray-700">Price (¥)</p>
          <Input
            id="price_min"
            placeholder="Min price"
            type="number"
            min={0}
            value={filters.price_min}
            onChange={(e) => onChange("price_min", e.target.value)}
          />
          <Input
            id="price_max"
            placeholder="Max price"
            type="number"
            min={0}
            value={filters.price_max}
            onChange={(e) => onChange("price_max", e.target.value)}
          />
        </div>

        {/* Mileage */}
        <div className="flex flex-col gap-2">
          <Input
            id="mileage_max"
            label="Max mileage (km)"
            placeholder="e.g. 50000"
            type="number"
            min={0}
            value={filters.mileage_max}
            onChange={(e) => onChange("mileage_max", e.target.value)}
          />
        </div>

        <Button variant="secondary" onClick={onReset} className="mt-auto">
          Reset filters
        </Button>
      </aside>
    </>
  );
}
