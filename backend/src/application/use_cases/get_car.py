from src.application.interfaces.car_repository import CarRepository
from src.domain.entities.car import Car


class GetCar:
    def __init__(self, repo: CarRepository) -> None:
        self._repo = repo

    async def execute(self, car_id: str) -> Car:
        return await self._repo.get_by_id(car_id)
