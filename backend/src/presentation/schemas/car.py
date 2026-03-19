from datetime import datetime

from pydantic import BaseModel


class CarSchema(BaseModel):
    id: str
    make: str
    model: str
    grade: str
    year: int
    mileage: int
    price: int
    body_price: int
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
    photos: list[str]
    features: list[str]
    scraped_at: datetime | None
    created_at: datetime | None
    updated_at: datetime | None

    model_config = {"from_attributes": True}


class CarListResponse(BaseModel):
    total: int
    page: int
    limit: int
    pages: int
    items: list[CarSchema]
