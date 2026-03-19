"use client";

import { useQuery } from "@tanstack/react-query";

import { CarCard }    from "@/entities/car";
import { Pagination } from "@/shared/ui/Pagination";
import { Spinner }    from "@/shared/ui/Spinner";
import { EmptyState } from "@/shared/ui/EmptyState";
import { fetchCars }  from "@/shared/api/cars";
import type { CarListParams } from "@/entities/car/model/types";

interface CarListProps {
  params:  CarListParams;
  onPageChange: (page: number) => void;
}

export function CarList({ params, onPageChange }: CarListProps) {
  const { data, isLoading, isError } = useQuery({
    queryKey: ["cars", params],
    queryFn:  () => fetchCars(params),
    staleTime: 30_000,
  });

  if (isLoading) {
    return (
      <div className="flex flex-1 items-center justify-center py-20">
        <Spinner size="lg" />
      </div>
    );
  }

  if (isError) {
    return (
      <EmptyState
        title="Failed to load cars"
        description="Something went wrong. Please try again."
      />
    );
  }

  if (!data || data.total === 0) {
    return (
      <EmptyState
        title="No cars found"
        description="Try adjusting your filters."
      />
    );
  }

  return (
    <div className="flex flex-col gap-6">
      <p className="text-sm text-gray-500">
        <span className="font-semibold text-gray-900">{data.total.toLocaleString()}</span> cars found
      </p>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-3">
        {data.items.map((car) => (
          <CarCard key={car.id} car={car} />
        ))}
      </div>

      <Pagination
        page={data.page}
        pages={data.pages}
        total={data.total}
        limit={data.limit}
        onChange={onPageChange}
      />
    </div>
  );
}
