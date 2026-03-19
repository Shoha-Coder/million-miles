"use client";

import { useState } from "react";

import { CarList }    from "@/widgets/CarList";
import { CarFilters } from "@/widgets/CarFilters";
import { useCarFilters } from "@/features/car-filter";
import { Button }     from "@/shared/ui/Button";

export default function CarsPage() {
  const { filters, page, updateFilter, resetFilters, setPage, toApiParams } = useCarFilters();
  const [filtersOpen, setFiltersOpen] = useState(false);

  return (
    <div className="mx-auto max-w-screen-xl px-4 py-6 sm:px-6">
      {/* Mobile: filter toggle button */}
      <div className="mb-4 flex items-center justify-between lg:hidden">
        <h1 className="text-xl font-bold text-gray-900">Cars</h1>
        <Button variant="secondary" size="sm" onClick={() => setFiltersOpen(true)}>
          ☰ Filters
        </Button>
      </div>

      <div className="flex gap-6">
        <CarFilters
          filters={filters}
          onChange={updateFilter}
          onReset={resetFilters}
          open={filtersOpen}
          onClose={() => setFiltersOpen(false)}
        />

        <div className="flex-1 min-w-0">
          {/* Desktop page title */}
          <h1 className="hidden lg:block text-2xl font-bold text-gray-900 mb-6">Car inventory</h1>
          <CarList
            params={toApiParams()}
            onPageChange={setPage}
          />
        </div>
      </div>
    </div>
  );
}
