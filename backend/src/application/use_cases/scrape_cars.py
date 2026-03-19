import logging

from src.application.interfaces.car_repository import CarRepository
from src.application.interfaces.translator_service import TranslatorService

logger = logging.getLogger(__name__)


class ScrapeCars:
    def __init__(
        self,
        repo: CarRepository,
        translator: TranslatorService,
        pages_per_run: int,
    ) -> None:
        self._repo = repo
        self._translator = translator
        self._pages_per_run = pages_per_run

    async def execute(self) -> int:
        # Import here to avoid circular deps — infrastructure stays out of application layer
        from src.infrastructure.services.scraper.parser import CarSensorParser

        parser = CarSensorParser(self._translator)
        cars = await parser.scrape(self._pages_per_run)

        for car in cars:
            await self._repo.upsert(car)

        logger.info("Scrape run finished — %d cars saved", len(cars))
        return len(cars)
