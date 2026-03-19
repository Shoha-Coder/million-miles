import asyncio
import logging
from datetime import datetime, timezone
from functools import lru_cache

from deep_translator import GoogleTranslator
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.interfaces.translator_service import TranslatorService
from src.infrastructure.database.models import TranslationModel

logger = logging.getLogger(__name__)


class GoogleTranslatorService(TranslatorService):
    """
    Wraps deep-translator's GoogleTranslator with a DB-backed cache so we
    don't hammer Google on every scrape run for the same strings.
    """

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def translate(self, text: str) -> str:
        if not text or not text.strip():
            return text

        # Try the cache first
        cached = await self._session.execute(
            select(TranslationModel).where(TranslationModel.jp_text == text)
        )
        row = cached.scalar_one_or_none()
        if row:
            return row.en_text

        # Not cached — call Google Translate in a thread so we don't block the event loop
        translated = await asyncio.to_thread(self._call_google, text)

        # Persist for next time
        stmt = (
            insert(TranslationModel)
            .values(jp_text=text, en_text=translated, cached_at=datetime.now(timezone.utc))
            .on_conflict_do_nothing(index_elements=["jp_text"])
        )
        await self._session.execute(stmt)
        await self._session.commit()

        return translated

    @staticmethod
    def _call_google(text: str) -> str:
        try:
            return GoogleTranslator(source="ja", target="en").translate(text) or text
        except Exception as exc:
            logger.warning("Google Translate failed for %r: %s", text, exc)
            return text


@lru_cache(maxsize=1)
def _get_sync_translator() -> GoogleTranslator:
    """Reusable sync translator for one-off calls outside async context."""
    return GoogleTranslator(source="ja", target="en")
