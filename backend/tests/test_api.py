"""
Full API test suite. Run with:
    python tests/test_api.py
"""

import asyncio
import sys
from datetime import datetime, timezone

import httpx

from src.infrastructure.database.base import AsyncSessionLocal
from src.infrastructure.database.models import CarModel

BASE = "http://localhost:8000"

CARS = [
    dict(id="CAR001", make="Toyota", model="Corolla", grade="1.5 X", year=2022,
         mileage=15000, price=2500000, body_price=2300000, color="White",
         engine_cc=1500, transmission="CVT", body_type="Sedan", fuel_type="Gasoline",
         drivetrain="2WD", doors=4, seats=5, repair_history=False,
         inspection_date="2027-06", prefecture="Tokyo", dealer_name="Toyota Shinjuku",
         photos=["https://example.com/1.jpg"], features=["Cruise Control"]),

    dict(id="CAR002", make="Honda", model="Fit", grade="1.3 G", year=2020,
         mileage=42000, price=1200000, body_price=1100000, color="Blue",
         engine_cc=1300, transmission="AT", body_type="Hatchback", fuel_type="Gasoline",
         drivetrain="2WD", doors=5, seats=5, repair_history=False,
         inspection_date="2026-03", prefecture="Osaka", dealer_name="Honda Namba",
         photos=["https://example.com/2.jpg"], features=["ETC"]),

    dict(id="CAR003", make="Nissan", model="Leaf", grade="e+", year=2023,
         mileage=8000, price=4200000, body_price=4000000, color="Black",
         engine_cc=None, transmission="AT", body_type="Hatchback", fuel_type="Electric",
         drivetrain="2WD", doors=5, seats=5, repair_history=False,
         inspection_date="2028-01", prefecture="Kanagawa", dealer_name="Nissan Yokohama",
         photos=["https://example.com/3.jpg"], features=["Fast Charge"]),

    dict(id="CAR004", make="Toyota", model="Prius", grade="Z", year=2019,
         mileage=88000, price=1800000, body_price=1650000, color="Silver",
         engine_cc=1800, transmission="CVT", body_type="Sedan", fuel_type="Hybrid",
         drivetrain="2WD", doors=4, seats=5, repair_history=True,
         inspection_date="2025-11", prefecture="Aichi", dealer_name="Toyota Nagoya",
         photos=["https://example.com/4.jpg"], features=["Navigation"]),

    dict(id="CAR005", make="Suzuki", model="Jimny", grade="XC", year=2021,
         mileage=31000, price=2900000, body_price=2750000, color="Green",
         engine_cc=660, transmission="MT", body_type="SUV", fuel_type="Gasoline",
         drivetrain="4WD", doors=3, seats=4, repair_history=False,
         inspection_date="2027-09", prefecture="Hokkaido", dealer_name="Suzuki Sapporo",
         photos=["https://example.com/5.jpg"], features=["4WD Lock"]),
]


# ── helpers ──────────────────────────────────────────────────────────────────

passed = 0
failed = 0


def check(label: str, expected, got) -> None:
    global passed, failed
    if got == expected:
        print(f"  PASS  {label}")
        passed += 1
    else:
        print(f"  FAIL  {label}  —  expected={expected!r}  got={got!r}")
        failed += 1


async def seed_db() -> None:
    from sqlalchemy import delete
    now = datetime.now(timezone.utc)
    async with AsyncSessionLocal() as s:
        await s.execute(delete(CarModel))
        for c in CARS:
            await s.merge(CarModel(**c, scraped_at=now, created_at=now, updated_at=now))
        await s.commit()


# ── tests ─────────────────────────────────────────────────────────────────────

async def run_tests() -> None:
    await seed_db()

    async with httpx.AsyncClient(base_url=BASE, timeout=10) as client:

        # ── Health ────────────────────────────────────────────────────────────
        print("\n━━━ HEALTH ━━━")
        r = await client.get("/health")
        check("GET /health → 200",          200,  r.status_code)
        check("status = ok",                "ok", r.json().get("status"))

        # ── Auth ──────────────────────────────────────────────────────────────
        print("\n━━━ AUTH ━━━")

        r = await client.post("/auth/login", json={"username": "admin", "password": "wrong"})
        check("wrong password → 401",       401,      r.status_code)

        r = await client.post("/auth/login", json={"username": "nobody", "password": "admin123"})
        check("wrong username → 401",       401,      r.status_code)

        r = await client.post("/auth/login", json={"username": "admin", "password": "admin123"})
        check("correct login → 200",        200,      r.status_code)
        check("response has access_token",  True,     "access_token" in r.json())
        check("token_type = bearer",        "bearer", r.json().get("token_type"))

        token = r.json()["access_token"]
        auth  = {"Authorization": f"Bearer {token}"}

        # ── Auth guard ────────────────────────────────────────────────────────
        print("\n━━━ AUTH GUARD ━━━")

        r = await client.get("/api/cars")
        check("no token → 401",             401, r.status_code)

        r = await client.get("/api/cars", headers={"Authorization": "Bearer garbage.token"})
        check("invalid token → 401",        401, r.status_code)

        r = await client.get("/api/cars/CAR001")
        check("detail no token → 401",      401, r.status_code)

        # ── List – response shape ─────────────────────────────────────────────
        print("\n━━━ LIST SHAPE ━━━")

        r = await client.get("/api/cars", headers=auth)
        d = r.json()
        check("GET /api/cars → 200",        200, r.status_code)
        check("total = 5",                    5, d["total"])
        check("page = 1",                     1, d["page"])
        check("limit = 20",                  20, d["limit"])
        check("pages = 1",                    1, d["pages"])
        check("items count = 5",              5, len(d["items"]))

        # every item has required fields
        required = {"id","make","model","year","mileage","price","body_type",
                    "fuel_type","photos","features","transmission"}
        first = d["items"][0]
        check("item has all required fields", True, required.issubset(first.keys()))

        # ── Filters ───────────────────────────────────────────────────────────
        print("\n━━━ FILTERS ━━━")

        async def total(url: str) -> int:
            return (await client.get(url, headers=auth)).json()["total"]

        check("make=Toyota",                  2, await total("/api/cars?make=Toyota"))
        check("make=Honda",                   1, await total("/api/cars?make=Honda"))
        check("make=BMW (no match)",           0, await total("/api/cars?make=BMW"))
        check("make case-insensitive",         2, await total("/api/cars?make=toyota"))
        check("body_type=Sedan",              2, await total("/api/cars?body_type=Sedan"))
        check("body_type=Hatchback",          2, await total("/api/cars?body_type=Hatchback"))
        check("body_type=SUV",                1, await total("/api/cars?body_type=SUV"))
        check("fuel_type=Electric",           1, await total("/api/cars?fuel_type=Electric"))
        check("fuel_type=Hybrid",             1, await total("/api/cars?fuel_type=Hybrid"))
        check("fuel_type=Gasoline",           3, await total("/api/cars?fuel_type=Gasoline"))
        check("year_min=2021",                3, await total("/api/cars?year_min=2021"))
        check("year_max=2020",                2, await total("/api/cars?year_max=2020"))
        check("year range 2020–2022",         3, await total("/api/cars?year_min=2020&year_max=2022"))
        check("price_min=4000000",            1, await total("/api/cars?price_min=4000000"))
        check("price_max=1500000",            1, await total("/api/cars?price_max=1500000"))
        check("price range 1M–3M",            4, await total("/api/cars?price_min=1000000&price_max=3000000"))
        check("mileage_max=10000",            1, await total("/api/cars?mileage_max=10000"))
        check("mileage_max=50000",            4, await total("/api/cars?mileage_max=50000"))
        check("make=Toyota + fuel=Hybrid",    1, await total("/api/cars?make=Toyota&fuel_type=Hybrid"))
        check("make=Toyota + body=Hatchback", 0, await total("/api/cars?make=Toyota&body_type=Hatchback"))

        # ── Sort ──────────────────────────────────────────────────────────────
        print("\n━━━ SORT ━━━")

        r = await client.get("/api/cars?sort=price&order=asc", headers=auth)
        prices = [item["price"] for item in r.json()["items"]]
        check("sort=price&order=asc",  True, prices == sorted(prices))

        r = await client.get("/api/cars?sort=price&order=desc", headers=auth)
        prices = [item["price"] for item in r.json()["items"]]
        check("sort=price&order=desc", True, prices == sorted(prices, reverse=True))

        r = await client.get("/api/cars?sort=year&order=asc", headers=auth)
        years = [item["year"] for item in r.json()["items"]]
        check("sort=year&order=asc",   True, years == sorted(years))

        r = await client.get("/api/cars?sort=mileage&order=desc", headers=auth)
        miles = [item["mileage"] for item in r.json()["items"]]
        check("sort=mileage&order=desc", True, miles == sorted(miles, reverse=True))

        r = await client.get("/api/cars?sort=INVALID", headers=auth)
        check("invalid sort → 422",    422, r.status_code)

        # ── Pagination ────────────────────────────────────────────────────────
        print("\n━━━ PAGINATION ━━━")

        r = await client.get("/api/cars?page=1&limit=2", headers=auth)
        d = r.json()
        check("limit=2 → 2 items",     2, len(d["items"]))
        check("limit=2 → pages=3",     3, d["pages"])
        check("limit=2 → total=5",     5, d["total"])

        r = await client.get("/api/cars?page=3&limit=2", headers=auth)
        check("page=3 limit=2 → 1 item", 1, len(r.json()["items"]))

        r = await client.get("/api/cars?page=99&limit=20", headers=auth)
        check("page beyond range → 0 items", 0, len(r.json()["items"]))

        r = await client.get("/api/cars?limit=0", headers=auth)
        check("limit=0 → 422",         422, r.status_code)

        r = await client.get("/api/cars?limit=101", headers=auth)
        check("limit=101 → 422",       422, r.status_code)

        # ── Detail ────────────────────────────────────────────────────────────
        print("\n━━━ DETAIL ━━━")

        r = await client.get("/api/cars/CAR003", headers=auth)
        check("GET /api/cars/CAR003 → 200", 200,        r.status_code)
        d = r.json()
        check("id correct",             "CAR003",    d["id"])
        check("make correct",           "Nissan",    d["make"])
        check("model correct",          "Leaf",      d["model"])
        check("fuel_type Electric",     "Electric",  d["fuel_type"])
        check("engine_cc null",         None,        d["engine_cc"])
        check("photos is list",         True,        isinstance(d["photos"], list))
        check("features is list",       True,        isinstance(d["features"], list))
        check("repair_history bool",    False,       d["repair_history"])

        r = await client.get("/api/cars/CAR004", headers=auth)
        check("repair_history=true car", True, r.json()["repair_history"])

        r = await client.get("/api/cars/DOESNOTEXIST", headers=auth)
        check("unknown id → 404",       404, r.status_code)

        r = await client.get("/api/cars/CAR001", headers=auth)
        detail_fields = {"id","make","model","grade","year","mileage","price","body_price",
                         "color","engine_cc","transmission","body_type","fuel_type",
                         "drivetrain","doors","seats","repair_history","inspection_date",
                         "prefecture","dealer_name","photos","features","scraped_at"}
        check("detail has all fields",  True, detail_fields.issubset(r.json().keys()))

    # ── summary ───────────────────────────────────────────────────────────────
    total_tests = passed + failed
    print(f"\n{'━'*45}")
    print(f"  {passed}/{total_tests} passed   {failed} failed")
    print(f"{'━'*45}")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(run_tests())
