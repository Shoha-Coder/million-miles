from src.application.interfaces.car_repository import (
    CarFilters,
    CarListResult,
    CarRepository,
    CarSort,
    Pagination,
)


class GetCars:
    def __init__(self, repo: CarRepository) -> None:
        self._repo = repo

    async def execute(
        self,
        filters: CarFilters,
        sort: CarSort,
        pagination: Pagination,
    ) -> CarListResult:
        return await self._repo.get_list(filters, sort, pagination)
