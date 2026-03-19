# Blueprint

## Project Structure

```
million-miles/
├── backend/
│   ├── app/
│   │   ├── main.py                  # FastAPI app entry point
│   │   ├── core/
│   │   │   ├── config.py            # Settings via pydantic-settings (.env)
│   │   │   └── security.py          # JWT encode/decode, password check
│   │   ├── models/
│   │   │   └── car.py               # SQLAlchemy ORM models (Car, Translation)
│   │   ├── schemas/
│   │   │   ├── car.py               # Pydantic response/request schemas
│   │   │   └── auth.py              # Login request/response schemas
│   │   ├── routers/
│   │   │   ├── auth.py              # POST /auth/login
│   │   │   └── cars.py              # GET /api/cars, GET /api/cars/{id}
│   │   ├── scraper/
│   │   │   ├── worker.py            # APScheduler — runs parser every hour
│   │   │   ├── parser.py            # httpx + BeautifulSoup scraping logic
│   │   │   └── translator.py        # deep-translator + DB translation cache
│   │   └── db/
│   │       ├── database.py          # SQLAlchemy engine, session factory
│   │       └── crud.py              # DB read/write operations
│   ├── alembic/                     # DB migrations
│   │   └── versions/
│   ├── alembic.ini
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx             # redirect → /cars or /login
│   │   │   ├── login/
│   │   │   │   └── page.tsx         # Login form
│   │   │   └── cars/
│   │   │       ├── page.tsx         # Car listing with filters
│   │   │       └── [id]/
│   │   │           └── page.tsx     # Car detail page
│   │   ├── components/
│   │   │   ├── CarCard.tsx          # Car thumbnail card
│   │   │   ├── CarFilters.tsx       # Filter sidebar/panel
│   │   │   ├── CarGrid.tsx          # Responsive grid wrapper
│   │   │   ├── Pagination.tsx       # Page controls
│   │   │   └── PhotoGallery.tsx     # Detail page image gallery
│   │   ├── lib/
│   │   │   └── api.ts               # Axios instance with JWT interceptor
│   │   ├── store/
│   │   │   └── auth.ts              # Zustand store (token, user, logout)
│   │   └── types/
│   │       └── car.ts               # TypeScript interfaces
│   ├── Dockerfile
│   ├── next.config.ts
│   └── package.json
├── nginx.conf
├── docker-compose.yml
├── requirements.md
└── blueprint.md
```

---

## Database Schema

### Table: `cars`

| Column | Type | Notes |
|---|---|---|
| id | VARCHAR PK | CarSensor ID, e.g. AU6887604684 |
| make | VARCHAR | e.g. Nissan |
| model | VARCHAR | e.g. Dayz |
| grade | VARCHAR | e.g. 660 X |
| year | INTEGER | e.g. 2026 |
| mileage | INTEGER | km |
| price | INTEGER | total price in yen |
| body_price | INTEGER | vehicle-only price in yen |
| color | VARCHAR | e.g. White Pearl |
| engine_cc | INTEGER | e.g. 660 |
| transmission | VARCHAR | e.g. CVT, Automatic, Manual |
| body_type | VARCHAR | e.g. Hatchback, Sedan, SUV |
| fuel_type | VARCHAR | e.g. Gasoline, Hybrid, Electric |
| drivetrain | VARCHAR | e.g. 2WD, 4WD |
| doors | INTEGER | |
| seats | INTEGER | |
| repair_history | BOOLEAN | false = clean title |
| inspection_date | VARCHAR | e.g. 2029-02 |
| prefecture | VARCHAR | e.g. Tochigi |
| dealer_name | VARCHAR | |
| photos | JSONB | array of image URLs |
| features | JSONB | array of feature strings |
| scraped_at | TIMESTAMP | last scraped time |
| created_at | TIMESTAMP | first seen |
| updated_at | TIMESTAMP | last updated |

### Table: `translations`

| Column | Type | Notes |
|---|---|---|
| jp_text | VARCHAR PK | original Japanese string |
| en_text | VARCHAR | translated English string |
| cached_at | TIMESTAMP | when it was translated |

---

## API Design

### POST /auth/login
```
Request:  { "username": "admin", "password": "admin123" }
Response: { "access_token": "...", "token_type": "bearer" }
```

### GET /api/cars
```
Query params:
  make, body_type, fuel_type      (string filters)
  year_min, year_max              (integer range)
  price_min, price_max            (integer range)
  mileage_max                     (integer)
  sort    = price|year|mileage|scraped_at  (default: scraped_at)
  order   = asc|desc              (default: desc)
  page    = 1                     (default: 1)
  limit   = 20                    (default: 20, max: 100)

Response:
  {
    "total": 1500,
    "page": 1,
    "limit": 20,
    "pages": 75,
    "items": [ ...Car objects... ]
  }
```

### GET /api/cars/{id}
```
Response: full Car object with all fields
```

---

## Scraper Flow

```
APScheduler (every 1 hour)
  └── worker.py: trigger scrape job
        └── parser.py:
              1. fetch /usedcar/index.html, index2.html ... (N pages)
              2. for each listing card: extract car ID + basic fields
              3. fetch /usedcar/detail/{id}/index.html
              4. extract all detail fields (Japanese)
              5. translator.py: translate each field
                    → check translations table (cache hit → use it)
                    → cache miss → GoogleTranslator().translate() → save → use
              6. crud.py: upsert car into DB
```

**Rate limiting:** 1 req/sec + random 0.5–1.5s jitter to avoid blocks
**Pages per run:** first 100 pages (~1000 cars) — configurable via env var

---

## Translation Flow

```python
# translator.py
from deep_translator import GoogleTranslator

async def translate(text: str, db) -> str:
    cached = db.query(Translation).filter_by(jp_text=text).first()
    if cached:
        return cached.en_text
    translated = GoogleTranslator(source='ja', target='en').translate(text)
    db.add(Translation(jp_text=text, en_text=translated))
    db.commit()
    return translated
```

No API key required.

---

## Frontend Pages

### /login
- Simple centered form (username + password)
- On success: store JWT in Zustand + localStorage, redirect to /cars
- On fail: show error message

### /cars
- Filter panel (left sidebar on desktop, collapsible on mobile)
- Car grid (3 cols desktop, 2 cols tablet, 1 col mobile)
- Each card: photo, make+model, year, mileage, price, location
- Sort dropdown + pagination controls
- TanStack Query for data fetching + caching

### /cars/[id]
- Photo gallery (main image + thumbnails)
- Full specs table
- Back button to listing

---

## Docker Compose Services

```yaml
services:
  db:        postgres:16, volume for persistence
  backend:   FastAPI on port 8000, depends on db
  frontend:  Next.js on port 3000, depends on backend
  nginx:     port 80, reverse proxy to backend + frontend
```

### Nginx Routing
```
/api/*      → backend:8000
/auth/*     → backend:8000
/*          → frontend:3000
```

---

## Environment Variables (.env)

```
DATABASE_URL=postgresql://user:password@db:5432/million_miles
JWT_SECRET=your-secret-key
JWT_EXPIRE_MINUTES=1440
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
SCRAPER_PAGES_PER_RUN=100
SCRAPER_REQUEST_DELAY=1.0
```
