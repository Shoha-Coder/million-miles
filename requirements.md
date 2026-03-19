# Requirements

## Position
Fullstack Developer — Million Miles

## Task Overview
Build a full-stack web application that:
1. Scrapes used car listings from CarSensor.net (Japanese site)
2. Stores data in a database
3. Exposes a REST API with JWT auth
4. Displays data in a Next.js web app

---

## 1. Scraper (Worker)

- Source: https://www.carsensor.net/
- Fields to collect: make, model, grade, year, mileage, price, color, body type, fuel type, transmission, drivetrain, doors, seats, repair history, inspection date, prefecture, dealer name, photos
- Site language: Japanese → translate all fields to English using Google Translate (`deep-translator`)
- Schedule: run every 1 hour
- Save results to PostgreSQL database (upsert by car ID)

## 2. Backend

- Framework: FastAPI (Python)
- Two endpoints:
  - `POST /auth/login` — JWT authentication (no auth required)
  - `GET /api/cars` — list cars with filters, sorting, pagination (JWT required)
  - `GET /api/cars/{id}` — single car detail (JWT required)
- Credentials: `admin` / `admin123`

### Filters for /api/cars
- `make`, `body_type`, `fuel_type`
- `year_min`, `year_max`
- `price_min`, `price_max`
- `mileage_max`
- `sort` (price | year | mileage | scraped_at)
- `order` (asc | desc)
- `page`, `limit`

## 3. Frontend

- Framework: Next.js (React)
- Pages:
  - `/login` — login form (admin:admin123), JWT stored in Zustand + localStorage
  - `/cars` — car listing grid with filters, sorting, pagination
  - `/cars/[id]` — car detail page with full specs and photo gallery
- Requirements:
  - Responsive design (desktop + mobile)
  - Fast page load

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11+, FastAPI, SQLAlchemy, Alembic |
| Scraper | httpx, BeautifulSoup4, APScheduler, deep-translator |
| Frontend | Next.js 14, TypeScript, Tailwind CSS, Zustand, TanStack Query |
| Database | PostgreSQL |
| Cache | Translation cache table in PostgreSQL |
| Infra | Docker, Docker Compose, Nginx |

---

## Delivery Format

- GitHub repository link with source code
- Deployed web application link
- Deadline: 2 days from receipt
