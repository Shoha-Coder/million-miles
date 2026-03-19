# Build Steps

## Phase 1 — Backend

### 1.1 Project Scaffold
- [ ] Create `backend/` folder structure (Clean Architecture)
- [ ] `pyproject.toml` with all dependencies
- [ ] `.env.example`
- [ ] `Dockerfile`

### 1.2 Domain Layer
- [ ] `src/domain/entities/car.py` — Car entity (dataclass)
- [ ] `src/domain/entities/translation.py` — Translation entity
- [ ] `src/domain/value_objects/` — Price, Mileage typed wrappers
- [ ] `src/domain/exceptions.py` — NotFound, Unauthorized, etc.

### 1.3 Application Layer
- [ ] `src/application/interfaces/car_repository.py` — abstract repo
- [ ] `src/application/interfaces/translator_service.py` — abstract translator
- [ ] `src/application/use_cases/get_cars.py` — list with filters/sort/pagination
- [ ] `src/application/use_cases/get_car.py` — single car by id
- [ ] `src/application/use_cases/login.py` — verify credentials, return JWT
- [ ] `src/application/use_cases/scrape_cars.py` — orchestrate scrape run

### 1.4 Infrastructure Layer
- [ ] `src/infrastructure/database/base.py` — SQLAlchemy engine + session
- [ ] `src/infrastructure/database/models.py` — ORM models (Car, Translation)
- [ ] `src/infrastructure/database/migrations/` — Alembic setup
- [ ] `src/infrastructure/repositories/car_repository.py` — concrete repo
- [ ] `src/infrastructure/services/scraper/parser.py` — httpx + BeautifulSoup
- [ ] `src/infrastructure/services/scraper/worker.py` — APScheduler hourly job
- [ ] `src/infrastructure/services/translator.py` — deep-translator + cache

### 1.5 Presentation Layer
- [ ] `src/presentation/api/auth.py` — POST /auth/login
- [ ] `src/presentation/api/cars.py` — GET /api/cars, GET /api/cars/{id}
- [ ] `src/presentation/schemas/auth.py` — request/response schemas
- [ ] `src/presentation/schemas/car.py` — car list/detail schemas
- [ ] `src/presentation/dependencies.py` — JWT dependency injection
- [ ] `src/main.py` — app factory, router registration, scheduler start

### 1.6 Backend Done Check
- [ ] Server starts with `uvicorn`
- [ ] `/auth/login` returns JWT for admin:admin123
- [ ] `/api/cars` returns paginated list (JWT protected)
- [ ] `/api/cars/{id}` returns car detail (JWT protected)
- [ ] Scraper runs and populates DB
- [ ] Translations cached correctly

---

## Phase 2 — Frontend

### 2.1 Project Scaffold
- [ ] Create Next.js app with TypeScript + Tailwind CSS
- [ ] FSD folder structure
- [ ] `Dockerfile`
- [ ] Environment config (`NEXT_PUBLIC_API_URL`)

### 2.2 Shared Layer
- [ ] `shared/api/` — Axios instance with JWT interceptor + refresh logic
- [ ] `shared/ui/` — Button, Input, Badge, Spinner, Pagination, EmptyState
- [ ] `shared/lib/` — formatPrice, formatMileage, formatYear utils
- [ ] `shared/config/` — env vars, routes constants

### 2.3 Entities Layer
- [ ] `entities/car/model/types.ts` — Car, CarListItem TypeScript interfaces
- [ ] `entities/car/ui/CarCard.tsx` — car thumbnail card component
- [ ] `entities/user/model/types.ts` — User, AuthToken interfaces

### 2.4 Features Layer
- [ ] `features/auth/model/useLogin.ts` — login mutation + JWT store update
- [ ] `features/auth/ui/LoginForm.tsx` — form with validation
- [ ] `features/car-filter/model/useCarFilters.ts` — filter state management
- [ ] `features/car-filter/ui/FilterPanel.tsx` — filter controls

### 2.5 Widgets Layer
- [ ] `widgets/CarList/ui/CarList.tsx` — grid of CarCards + loading/empty states
- [ ] `widgets/CarFilters/ui/CarFilters.tsx` — full filter sidebar/drawer
- [ ] `widgets/CarDetail/ui/CarDetail.tsx` — full detail layout
- [ ] `widgets/PhotoGallery/ui/PhotoGallery.tsx` — image gallery with thumbnails

### 2.6 App Layer (Pages)
- [ ] `app/login/page.tsx` — login page
- [ ] `app/cars/page.tsx` — listing page (filters + grid + pagination)
- [ ] `app/cars/[id]/page.tsx` — detail page
- [ ] `app/layout.tsx` — providers (QueryClient, Zustand)
- [ ] Route guard — redirect unauthenticated users to /login

### 2.7 Frontend Done Check
- [ ] Login works, JWT stored, redirects to /cars
- [ ] Car list loads with pagination
- [ ] Filters and sort work correctly
- [ ] Car detail page shows all specs + photos
- [ ] Fully responsive (mobile + desktop)

---

## Phase 3 — Infrastructure

### 3.1 Docker
- [ ] `docker-compose.yml` — postgres, backend, frontend, nginx
- [ ] `nginx.conf` — route /api/* and /auth/* to backend, /* to frontend
- [ ] Test full stack with `docker compose up`

### 3.2 Deployment
- [ ] Push to GitHub
- [ ] Deploy to server
- [ ] Verify live URL works end to end

---

## Current Status
> Phase 1 — Backend (in progress)
