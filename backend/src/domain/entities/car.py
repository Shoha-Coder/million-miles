from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Car:
    id: str
    make: str
    model: str
    grade: str
    year: int
    mileage: int        # km
    price: int          # total price in yen
    body_price: int     # vehicle-only price in yen
    color: str
    engine_cc: int | None
    transmission: str
    body_type: str
    fuel_type: str
    drivetrain: str
    doors: int | None
    seats: int | None
    repair_history: bool
    inspection_date: str | None
    prefecture: str
    dealer_name: str
    photos: list[str] = field(default_factory=list)
    features: list[str] = field(default_factory=list)
    scraped_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
