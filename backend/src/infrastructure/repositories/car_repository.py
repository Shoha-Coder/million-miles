from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.interfaces.car_repository import (
    CarFilters,
    CarListResult,
    CarRepository,
    CarSort,
    Pagination,
)
from src.domain.entities.car import Car
from src.domain.exceptions import CarNotFound
from src.infrastructure.database.models import CarModel

# Columns we allow sorting by — anything outside this list falls back to scraped_at
_SORTABLE = {"price", "year", "mileage", "scraped_at"}


def _to_entity(row: CarModel) -> Car:
    return Car(
        id=row.id,
        make=row.make,
        model=row.model,
        grade=row.grade,
        year=row.year,
        mileage=row.mileage,
        price=row.price,
        body_price=row.body_price,
        color=row.color,
        engine_cc=row.engine_cc,
        transmission=row.transmission,
        body_type=row.body_type,
        fuel_type=row.fuel_type,
        drivetrain=row.drivetrain,
        doors=row.doors,
        seats=row.seats,
        repair_history=row.repair_history,
        inspection_date=row.inspection_date,
        prefecture=row.prefecture,
        dealer_name=row.dealer_name,
        photos=row.photos or [],
        features=row.features or [],
        scraped_at=row.scraped_at,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


class SqlCarRepository(CarRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_list(
        self,
        filters: CarFilters,
        sort: CarSort,
        pagination: Pagination,
    ) -> CarListResult:
        query = select(CarModel)

        # Apply filters
        if filters.make:
            query = query.where(CarModel.make.ilike(f"%{filters.make}%"))
        if filters.body_type:
            query = query.where(CarModel.body_type.ilike(f"%{filters.body_type}%"))
        if filters.fuel_type:
            query = query.where(CarModel.fuel_type.ilike(f"%{filters.fuel_type}%"))
        if filters.year_min is not None:
            query = query.where(CarModel.year >= filters.year_min)
        if filters.year_max is not None:
            query = query.where(CarModel.year <= filters.year_max)
        if filters.price_min is not None:
            query = query.where(CarModel.price >= filters.price_min)
        if filters.price_max is not None:
            query = query.where(CarModel.price <= filters.price_max)
        if filters.mileage_max is not None:
            query = query.where(CarModel.mileage <= filters.mileage_max)

        # Count before pagination
        count_result = await self._session.execute(
            select(func.count()).select_from(query.subquery())
        )
        total = count_result.scalar_one()

        # Sort
        sort_col = getattr(CarModel, sort.field if sort.field in _SORTABLE else "scraped_at")
        query = query.order_by(sort_col.desc() if sort.order == "desc" else sort_col.asc())

        # Paginate
        query = query.offset(pagination.offset).limit(pagination.limit)

        result = await self._session.execute(query)
        rows = result.scalars().all()

        return CarListResult(
            items=[_to_entity(r) for r in rows],
            total=total,
            page=pagination.page,
            limit=pagination.limit,
        )

    async def get_by_id(self, car_id: str) -> Car:
        result = await self._session.execute(
            select(CarModel).where(CarModel.id == car_id)
        )
        row = result.scalar_one_or_none()
        if row is None:
            raise CarNotFound(car_id)
        return _to_entity(row)

    async def upsert(self, car: Car) -> None:
        now = datetime.now(timezone.utc)
        stmt = (
            insert(CarModel)
            .values(
                id=car.id,
                make=car.make,
                model=car.model,
                grade=car.grade,
                year=car.year,
                mileage=car.mileage,
                price=car.price,
                body_price=car.body_price,
                color=car.color,
                engine_cc=car.engine_cc,
                transmission=car.transmission,
                body_type=car.body_type,
                fuel_type=car.fuel_type,
                drivetrain=car.drivetrain,
                doors=car.doors,
                seats=car.seats,
                repair_history=car.repair_history,
                inspection_date=car.inspection_date,
                prefecture=car.prefecture,
                dealer_name=car.dealer_name,
                photos=car.photos,
                features=car.features,
                scraped_at=now,
                created_at=now,
                updated_at=now,
            )
            .on_conflict_do_update(
                index_elements=["id"],
                set_={
                    "make": car.make,
                    "model": car.model,
                    "grade": car.grade,
                    "year": car.year,
                    "mileage": car.mileage,
                    "price": car.price,
                    "body_price": car.body_price,
                    "color": car.color,
                    "engine_cc": car.engine_cc,
                    "transmission": car.transmission,
                    "body_type": car.body_type,
                    "fuel_type": car.fuel_type,
                    "drivetrain": car.drivetrain,
                    "doors": car.doors,
                    "seats": car.seats,
                    "repair_history": car.repair_history,
                    "inspection_date": car.inspection_date,
                    "prefecture": car.prefecture,
                    "dealer_name": car.dealer_name,
                    "photos": car.photos,
                    "features": car.features,
                    "scraped_at": now,
                    "updated_at": now,
                },
            )
        )
        await self._session.execute(stmt)
        await self._session.commit()
