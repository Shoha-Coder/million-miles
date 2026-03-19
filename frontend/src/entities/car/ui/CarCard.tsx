import Image from "next/image";
import Link from "next/link";

import { Badge } from "@/shared/ui/Badge";
import { formatMileage, formatPrice, truncate } from "@/shared/lib/format";
import { ROUTES } from "@/shared/config/routes";
import type { Car } from "../model/types";

interface CarCardProps {
  car: Car;
}

const FUEL_BADGE: Record<string, "blue" | "green" | "gray" | "yellow"> = {
  Electric: "green",
  Hybrid:   "blue",
  Gasoline: "gray",
  Diesel:   "yellow",
};

export function CarCard({ car }: CarCardProps) {
  const photo     = car.photos[0] ?? null;
  const fuelColor = FUEL_BADGE[car.fuel_type] ?? "gray";

  return (
    <Link
      href={ROUTES.car(car.id)}
      className="group flex flex-col rounded-xl border border-gray-200 bg-white overflow-hidden shadow-sm hover:shadow-md hover:border-brand-300 transition-all duration-200"
    >
      {/* Photo */}
      <div className="relative aspect-[4/3] bg-gray-100 overflow-hidden">
        {photo ? (
          <Image
            src={photo}
            alt={`${car.make} ${car.model}`}
            fill
            sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
            className="object-cover group-hover:scale-105 transition-transform duration-300"
            unoptimized
          />
        ) : (
          <div className="flex h-full items-center justify-center text-4xl text-gray-300">
            🚗
          </div>
        )}

        {/* Fuel type badge top-right */}
        <div className="absolute top-2 right-2">
          <Badge variant={fuelColor}>{car.fuel_type}</Badge>
        </div>

        {/* Repair history warning */}
        {car.repair_history && (
          <div className="absolute top-2 left-2">
            <Badge variant="red">Repaired</Badge>
          </div>
        )}
      </div>

      {/* Info */}
      <div className="flex flex-col gap-2 p-4">
        <div>
          <p className="text-xs font-medium text-brand-600 uppercase tracking-wide">
            {car.make}
          </p>
          <h3 className="mt-0.5 text-base font-semibold text-gray-900 leading-tight">
            {car.model}
            {car.grade && (
              <span className="ml-1 text-sm font-normal text-gray-500">{car.grade}</span>
            )}
          </h3>
        </div>

        {/* Key stats row */}
        <div className="flex items-center gap-3 text-xs text-gray-500">
          <span>{car.year}</span>
          <span className="text-gray-300">·</span>
          <span>{formatMileage(car.mileage)}</span>
          <span className="text-gray-300">·</span>
          <span>{car.body_type}</span>
        </div>

        {/* Price + location */}
        <div className="flex items-end justify-between mt-1">
          <p className="text-lg font-bold text-gray-900">{formatPrice(car.price)}</p>
          <p className="text-xs text-gray-400">{truncate(car.prefecture, 16)}</p>
        </div>
      </div>
    </Link>
  );
}
