from fastapi import APIRouter, HTTPException, Query, status

from src.application.interfaces.car_repository import CarFilters, CarSort, Pagination
from src.application.use_cases.get_car import GetCar
from src.application.use_cases.get_cars import GetCars
from src.domain.exceptions import CarNotFound
from src.infrastructure.repositories.car_repository import SqlCarRepository
from src.presentation.dependencies import AuthDep, SessionDep
from src.presentation.schemas.car import CarListResponse, CarSchema

router = APIRouter(prefix="/api/cars", tags=["cars"])


@router.get("", response_model=CarListResponse)
async def list_cars(
    session: SessionDep,
    _user: AuthDep,
    make: str | None = Query(None),
    body_type: str | None = Query(None),
    fuel_type: str | None = Query(None),
    year_min: int | None = Query(None, ge=1900),
    year_max: int | None = Query(None, le=2100),
    price_min: int | None = Query(None, ge=0),
    price_max: int | None = Query(None, ge=0),
    mileage_max: int | None = Query(None, ge=0),
    sort: str = Query("scraped_at", pattern="^(price|year|mileage|scraped_at)$"),
    order: str = Query("desc", pattern="^(asc|desc)$"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
) -> CarListResponse:
    repo = SqlCarRepository(session)
    use_case = GetCars(repo)

    result = await use_case.execute(
        filters=CarFilters(
            make=make,
            body_type=body_type,
            fuel_type=fuel_type,
            year_min=year_min,
            year_max=year_max,
            price_min=price_min,
            price_max=price_max,
            mileage_max=mileage_max,
        ),
        sort=CarSort(field=sort, order=order),
        pagination=Pagination(page=page, limit=limit),
    )

    return CarListResponse(
        total=result.total,
        page=result.page,
        limit=result.limit,
        pages=result.pages,
        items=[CarSchema.model_validate(car.__dict__) for car in result.items],
    )


@router.get("/{car_id}", response_model=CarSchema)
async def get_car(car_id: str, session: SessionDep, _user: AuthDep) -> CarSchema:
    repo = SqlCarRepository(session)
    use_case = GetCar(repo)

    try:
        car = await use_case.execute(car_id)
    except CarNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Car '{car_id}' not found")

    return CarSchema.model_validate(car.__dict__)
