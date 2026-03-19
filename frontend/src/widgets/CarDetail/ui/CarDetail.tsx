import { PhotoGallery } from "@/widgets/PhotoGallery";
import { Badge }        from "@/shared/ui/Badge";
import { formatEngine, formatMileage, formatPrice } from "@/shared/lib/format";
import type { Car } from "@/entities/car/model/types";

interface CarDetailProps {
  car: Car;
}

interface SpecRowProps {
  label: string;
  value: React.ReactNode;
}

function SpecRow({ label, value }: SpecRowProps) {
  return (
    <div className="flex items-start justify-between gap-4 py-2.5 border-b border-gray-100 last:border-0">
      <dt className="text-sm text-gray-500 shrink-0 w-40">{label}</dt>
      <dd className="text-sm font-medium text-gray-900 text-right">{value ?? "—"}</dd>
    </div>
  );
}

export function CarDetail({ car }: CarDetailProps) {
  return (
    <div className="grid grid-cols-1 gap-8 lg:grid-cols-5">
      {/* Left — gallery */}
      <div className="lg:col-span-3">
        <PhotoGallery
          photos={car.photos}
          alt={`${car.make} ${car.model}`}
        />
      </div>

      {/* Right — info */}
      <div className="lg:col-span-2 flex flex-col gap-6">
        {/* Title block */}
        <div>
          <p className="text-sm font-semibold text-brand-600 uppercase tracking-wide">{car.make}</p>
          <h1 className="mt-1 text-2xl font-bold text-gray-900">
            {car.model}
            {car.grade && <span className="ml-2 text-lg font-normal text-gray-500">{car.grade}</span>}
          </h1>

          <div className="mt-3 flex flex-wrap gap-2">
            <Badge variant={car.fuel_type === "Electric" ? "green" : car.fuel_type === "Hybrid" ? "blue" : "gray"}>
              {car.fuel_type}
            </Badge>
            <Badge variant="gray">{car.body_type}</Badge>
            <Badge variant="gray">{car.drivetrain}</Badge>
            {car.repair_history && <Badge variant="red">Repair history</Badge>}
          </div>
        </div>

        {/* Price */}
        <div className="rounded-xl bg-gray-50 p-4">
          <p className="text-sm text-gray-500">Total price</p>
          <p className="text-3xl font-bold text-gray-900">{formatPrice(car.price)}</p>
          {car.body_price !== car.price && (
            <p className="text-sm text-gray-400 mt-0.5">
              Vehicle: {formatPrice(car.body_price)}
            </p>
          )}
        </div>

        {/* Key specs */}
        <dl>
          <SpecRow label="Year"         value={car.year} />
          <SpecRow label="Mileage"      value={formatMileage(car.mileage)} />
          <SpecRow label="Transmission" value={car.transmission} />
          <SpecRow label="Engine"       value={formatEngine(car.engine_cc)} />
          <SpecRow label="Doors"        value={car.doors} />
          <SpecRow label="Seats"        value={car.seats} />
          <SpecRow label="Color"        value={car.color} />
          <SpecRow label="Inspection"   value={car.inspection_date} />
          <SpecRow label="Prefecture"   value={car.prefecture} />
          <SpecRow label="Dealer"       value={car.dealer_name} />
        </dl>

        {/* Features */}
        {car.features.length > 0 && (
          <div>
            <p className="text-sm font-semibold text-gray-700 mb-2">Features</p>
            <div className="flex flex-wrap gap-1.5">
              {car.features.map((f) => (
                <Badge key={f} variant="blue">{f}</Badge>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
