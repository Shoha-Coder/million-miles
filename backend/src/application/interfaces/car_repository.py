from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.domain.entities.car import Car


@dataclass
class CarFilters:
    make: str | None = None
    body_type: str | None = None
    fuel_type: str | None = None
    year_min: int | None = None
    year_max: int | None = None
    price_min: int | None = None
    price_max: int | None = None
    mileage_max: int | None = None


@dataclass
class CarSort:
    field: str = "scraped_at"   # price | year | mileage | scraped_at
    order: str = "desc"         # asc | desc


@dataclass
class Pagination:
    page: int = 1
    limit: int = 20

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.limit


@dataclass
class CarListResult:
    items: list[Car]
    total: int
    page: int
    limit: int

    @property
    def pages(self) -> int:
        # ceiling division without math import
        return -(-self.total // self.limit)


class CarRepository(ABC):
    @abstractmethod
    async def get_list(
        self,
        filters: CarFilters,
        sort: CarSort,
        pagination: Pagination,
    ) -> CarListResult: ...

    @abstractmethod
    async def get_by_id(self, car_id: str) -> Car: ...

    @abstractmethod
    async def upsert(self, car: Car) -> None: ...
