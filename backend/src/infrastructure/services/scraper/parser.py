import asyncio
import logging
import re
from datetime import datetime, timezone

import httpx
from bs4 import BeautifulSoup

from src.application.interfaces.translator_service import TranslatorService
from src.config import settings
from src.domain.entities.car import Car

logger = logging.getLogger(__name__)

BASE_URL = "https://www.carsensor.net"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "ja,en;q=0.9",
}


def _parse_int(text: str | None) -> int | None:
    """Pull the first run of digits out of a string like '660cc' or '2,500km'."""
    if not text:
        return None
    digits = re.sub(r"[^\d]", "", text)
    return int(digits) if digits else None


def _parse_price(text: str | None) -> int:
    """
    CarSensor shows prices as '135.9万円' (man-yen) or plain yen.
    Normalise everything to whole yen.
    """
    if not text:
        return 0
    text = text.replace(",", "").strip()
    # Format: '135.9万円'
    man_match = re.search(r"([\d.]+)\s*万", text)
    if man_match:
        return int(float(man_match.group(1)) * 10_000)
    digits = re.sub(r"[^\d]", "", text)
    return int(digits) if digits else 0


class CarSensorParser:
    def __init__(self, translator: TranslatorService) -> None:
        self._translator = translator

    async def scrape(self, pages: int) -> list[Car]:
        """Entry point — collect car IDs from listing pages, then fetch each detail."""
        async with httpx.AsyncClient(headers=HEADERS, timeout=30, follow_redirects=True) as client:
            car_ids = await self._collect_ids(client, pages)
            logger.info("Found %d car IDs across %d pages", len(car_ids), pages)

            cars: list[Car] = []
            for car_id in car_ids:
                try:
                    car = await self._fetch_detail(client, car_id)
                    if car:
                        cars.append(car)
                except Exception as exc:
                    logger.warning("Skipping %s — %s", car_id, exc)
                await asyncio.sleep(settings.scraper_request_delay)

        return cars

    async def _collect_ids(self, client: httpx.AsyncClient, pages: int) -> list[str]:
        ids: list[str] = []
        for page_num in range(1, pages + 1):
            url = (
                f"{BASE_URL}/usedcar/index.html"
                if page_num == 1
                else f"{BASE_URL}/usedcar/index{page_num}.html"
            )
            try:
                resp = await client.get(url)
                resp.raise_for_status()
                soup = BeautifulSoup(resp.text, "lxml")

                # Each listing card links to /usedcar/detail/{ID}/index.html
                for tag in soup.select("a[href*='/usedcar/detail/']"):
                    href = tag.get("href", "")
                    match = re.search(r"/usedcar/detail/([^/]+)/", href)
                    if match:
                        car_id = match.group(1)
                        if car_id not in ids:
                            ids.append(car_id)

            except Exception as exc:
                logger.warning("Failed to fetch listing page %d: %s", page_num, exc)

            await asyncio.sleep(settings.scraper_request_delay)

        return ids

    async def _fetch_detail(self, client: httpx.AsyncClient, car_id: str) -> Car | None:
        url = f"{BASE_URL}/usedcar/detail/{car_id}/index.html"
        resp = await client.get(url)
        resp.raise_for_status()
        return await self._parse_detail(resp.text, car_id)

    async def _parse_detail(self, html: str, car_id: str) -> Car | None:
        soup = BeautifulSoup(html, "lxml")

        # --- Photos ---
        photos: list[str] = []
        for img in soup.select(".photo img, .carPhoto img, [class*='photo'] img"):
            src = img.get("src") or img.get("data-original", "")
            if src and src.startswith("//"):
                src = "https:" + src
            if src and src not in photos:
                photos.append(src)

        # --- Spec table ---
        # CarSensor detail pages use a definition list or table with Japanese labels
        specs: dict[str, str] = {}
        for row in soup.select("table tr, dl dt, .spec-list li"):
            cells = row.find_all(["td", "dd", "span"])
            if len(cells) >= 2:
                label = row.find(["th", "dt"]) or cells[0]
                value = cells[-1]
                specs[label.get_text(strip=True)] = value.get_text(strip=True)

        # Also grab from definition lists that pair dt/dd
        dts = soup.find_all("dt")
        for dt in dts:
            dd = dt.find_next_sibling("dd")
            if dd:
                specs[dt.get_text(strip=True)] = dd.get_text(strip=True)

        raw_make = self._pick(specs, ["メーカー", "ブランド", "製造会社"])
        raw_model = self._pick(specs, ["車種", "モデル", "車名"])
        raw_grade = self._pick(specs, ["グレード"])
        raw_year = self._pick(specs, ["年式", "モデル年"])
        raw_mileage = self._pick(specs, ["走行距離"])
        raw_price_total = self._pick(specs, ["支払総額", "総額"])
        raw_price_body = self._pick(specs, ["車両本体価格", "車両価格"])
        raw_color = self._pick(specs, ["色", "カラー", "ボディカラー"])
        raw_engine = self._pick(specs, ["排気量"])
        raw_trans = self._pick(specs, ["ミッション", "トランスミッション"])
        raw_body = self._pick(specs, ["ボディタイプ", "ボディ形状"])
        raw_fuel = self._pick(specs, ["燃料", "燃料種別"])
        raw_drive = self._pick(specs, ["駆動方式", "駆動"])
        raw_doors = self._pick(specs, ["ドア数"])
        raw_seats = self._pick(specs, ["乗車定員", "定員"])
        raw_repair = self._pick(specs, ["修復歴"])
        raw_inspection = self._pick(specs, ["車検"])
        raw_prefecture = self._pick(specs, ["地域", "都道府県", "所在地"])
        raw_dealer = self._pick(specs, ["販売店名", "販売店", "ディーラー"])

        # If we couldn't pull basic fields, try the page title as fallback
        if not raw_make or not raw_model:
            title = soup.select_one("h1, .carName, [class*='title']")
            if title:
                parts = title.get_text(strip=True).split()
                raw_make = raw_make or (parts[0] if parts else "Unknown")
                raw_model = raw_model or (" ".join(parts[1:3]) if len(parts) > 1 else "Unknown")

        # Features / equipment list
        raw_features: list[str] = [
            el.get_text(strip=True)
            for el in soup.select(".equipment li, .feature li, [class*='equip'] li, [class*='feature'] li")
            if el.get_text(strip=True)
        ]

        # Translate all Japanese strings concurrently
        (
            make, model, grade, color, transmission,
            body_type, fuel_type, drivetrain, prefecture, dealer_name,
        ) = await asyncio.gather(
            self._translator.translate(raw_make or "Unknown"),
            self._translator.translate(raw_model or "Unknown"),
            self._translator.translate(raw_grade or ""),
            self._translator.translate(raw_color or ""),
            self._translator.translate(raw_trans or ""),
            self._translator.translate(raw_body or ""),
            self._translator.translate(raw_fuel or ""),
            self._translator.translate(raw_drive or ""),
            self._translator.translate(raw_prefecture or ""),
            self._translator.translate(raw_dealer or ""),
        )

        translated_features = await asyncio.gather(
            *[self._translator.translate(f) for f in raw_features]
        )

        return Car(
            id=car_id,
            make=make,
            model=model,
            grade=grade,
            year=_parse_int(raw_year) or 0,
            mileage=_parse_int(raw_mileage) or 0,
            price=_parse_price(raw_price_total),
            body_price=_parse_price(raw_price_body),
            color=color,
            engine_cc=_parse_int(raw_engine),
            transmission=transmission,
            body_type=body_type,
            fuel_type=fuel_type,
            drivetrain=drivetrain,
            doors=_parse_int(raw_doors),
            seats=_parse_int(raw_seats),
            repair_history=raw_repair not in (None, "", "なし"),
            inspection_date=raw_inspection,
            prefecture=prefecture,
            dealer_name=dealer_name,
            photos=photos[:10],  # keep at most 10 photos per car
            features=list(translated_features),
            scraped_at=datetime.now(timezone.utc),
        )

    @staticmethod
    def _pick(specs: dict[str, str], keys: list[str]) -> str | None:
        """Return the first matching value from the spec dict, or None."""
        for key in keys:
            if key in specs and specs[key]:
                return specs[key]
        return None
