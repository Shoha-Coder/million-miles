from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database.base import Base


def _now() -> datetime:
    return datetime.now(timezone.utc)


class CarModel(Base):
    __tablename__ = "cars"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    make: Mapped[str] = mapped_column(String, nullable=False, index=True)
    model: Mapped[str] = mapped_column(String, nullable=False)
    grade: Mapped[str] = mapped_column(String, nullable=False, default="")
    year: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    mileage: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    price: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    body_price: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    color: Mapped[str] = mapped_column(String, nullable=False, default="")
    engine_cc: Mapped[int | None] = mapped_column(Integer, nullable=True)
    transmission: Mapped[str] = mapped_column(String, nullable=False, default="")
    body_type: Mapped[str] = mapped_column(String, nullable=False, index=True)
    fuel_type: Mapped[str] = mapped_column(String, nullable=False, index=True)
    drivetrain: Mapped[str] = mapped_column(String, nullable=False, default="")
    doors: Mapped[int | None] = mapped_column(Integer, nullable=True)
    seats: Mapped[int | None] = mapped_column(Integer, nullable=True)
    repair_history: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    inspection_date: Mapped[str | None] = mapped_column(String, nullable=True)
    prefecture: Mapped[str] = mapped_column(String, nullable=False, default="")
    dealer_name: Mapped[str] = mapped_column(String, nullable=False, default="")
    photos: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    features: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    scraped_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=_now)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=_now, onupdate=_now)


class TranslationModel(Base):
    __tablename__ = "translations"

    jp_text: Mapped[str] = mapped_column(Text, primary_key=True)
    en_text: Mapped[str] = mapped_column(Text, nullable=False)
    cached_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=_now)
