import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.infrastructure.services.scraper.worker import build_scheduler
from src.presentation.api.auth import router as auth_router
from src.presentation.api.cars import router as cars_router

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s — %(message)s")
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    # Fire up the hourly scrape scheduler when the server starts
    scheduler = build_scheduler()
    scheduler.start()
    logger.info("Scheduler started — first scrape runs in 1 hour")

    yield

    scheduler.shutdown(wait=False)
    logger.info("Scheduler stopped")


app = FastAPI(
    title="Million Miles API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(cars_router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
