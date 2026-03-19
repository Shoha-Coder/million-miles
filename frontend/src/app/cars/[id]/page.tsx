"use client";

import { useQuery }  from "@tanstack/react-query";
import { useParams } from "next/navigation";
import Link          from "next/link";

import { CarDetail } from "@/widgets/CarDetail";
import { Spinner }   from "@/shared/ui/Spinner";
import { fetchCar }  from "@/shared/api/cars";
import { ROUTES }    from "@/shared/config/routes";

export default function CarDetailPage() {
  const { id } = useParams<{ id: string }>();

  const { data: car, isLoading, isError } = useQuery({
    queryKey: ["car", id],
    queryFn:  () => fetchCar(id),
    enabled:  !!id,
  });

  return (
    <div className="mx-auto max-w-screen-xl px-4 py-6 sm:px-6">
      {/* Breadcrumb */}
      <nav className="mb-6 flex items-center gap-2 text-sm text-gray-500">
        <Link href={ROUTES.cars} className="hover:text-brand-600 transition-colors">
          ← Back to listing
        </Link>
        {car && (
          <>
            <span>/</span>
            <span className="text-gray-900 font-medium">{car.make} {car.model}</span>
          </>
        )}
      </nav>

      {isLoading && (
        <div className="flex justify-center py-20">
          <Spinner size="lg" />
        </div>
      )}

      {isError && (
        <div className="rounded-xl border border-red-200 bg-red-50 p-6 text-center text-red-700">
          Car not found or failed to load.
        </div>
      )}

      {car && <CarDetail car={car} />}
    </div>
  );
}
