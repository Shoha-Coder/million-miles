import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.config import settings
from src.infrastructure.database.base import AsyncSessionLocal
from src.infrastructure.repositories.car_repository import SqlCarRepository
from src.infrastructure.services.translator import GoogleTranslatorService

logger = logging.getLogger(__name__)


async def run_scrape_job() -> None:
    """Called by APScheduler every hour. Opens its own DB session."""
    from src.application.use_cases.scrape_cars import ScrapeCars

    async with AsyncSessionLocal() as session:
        repo = SqlCarRepository(session)
        translator = GoogleTranslatorService(session)
        use_case = ScrapeCars(
            repo=repo,
            translator=translator,
            pages_per_run=settings.scraper_pages_per_run,
        )
        try:
            count = await use_case.execute()
            logger.info("Hourly scrape done — %d cars upserted", count)
        except Exception as exc:
            logger.exception("Scrape job failed: %s", exc)


def build_scheduler() -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        run_scrape_job,
        trigger="interval",
        hours=1,
        id="hourly_scrape",
        replace_existing=True,
    )
    return scheduler
