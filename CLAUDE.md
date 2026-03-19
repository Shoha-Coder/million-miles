# Claude Rules for This Project

## Code Style — General

- Senior-level code only. No shortcuts, no lazy abstractions.
- Comments must sound like a developer wrote them, not an AI.
  - Bad:  `# This function handles the authentication process`
  - Good: `# Verify credentials and hand back a signed token`
- No obvious comments. Only comment non-obvious logic, edge cases, or intent.
- Follow KISS, DRY, SOLID strictly.
- No god functions. One function = one job.
- Meaningful names. No `data`, `result`, `temp`, `obj`, `val`.
- Keep functions short. If it scrolls, it needs splitting.
- Explicit over implicit — always.

---

## Python Backend — Clean Architecture

Strictly follow this structure. No exceptions.

```
backend/
├── src/
│   ├── domain/              # Zero dependencies on frameworks
│   │   ├── entities/        # Core business objects (dataclasses/Pydantic)
│   │   ├── value_objects/   # Immutable typed wrappers (Price, Mileage...)
│   │   └── exceptions.py    # Domain-specific exceptions
│   │
│   ├── application/         # Orchestrates domain, calls interfaces
│   │   ├── use_cases/       # One file per use case
│   │   └── interfaces/      # Abstract base classes (ports) for repos/services
│   │
│   ├── infrastructure/      # Everything that touches the outside world
│   │   ├── database/        # SQLAlchemy models, engine, session
│   │   ├── repositories/    # Concrete implementations of interfaces
│   │   └── services/        # Scraper, translator, scheduler
│   │
│   ├── presentation/        # FastAPI only — no business logic here
│   │   ├── api/             # Routers split by resource
│   │   └── schemas/         # Pydantic request/response models
│   │
│   └── main.py              # Wires everything together
│
├── tests/
└── pyproject.toml
```

### Rules
- `domain/` has zero imports from `infrastructure/` or `presentation/`.
- Use cases depend only on interfaces (abstract), never on concrete implementations.
- Inject dependencies — never instantiate repos or services inside use cases directly.
- SQLAlchemy models live in `infrastructure/database/`, never in `domain/`.
- Domain entities are plain dataclasses or Pydantic BaseModel — no ORM logic inside.
- Each use case is a class with a single `execute()` method.
- Raise domain exceptions from use cases, catch and map them in routers.

---

## Frontend — Feature-Sliced Design (FSD)

```
frontend/src/
├── app/                    # Next.js App Router — layout, providers, routing only
│   ├── layout.tsx
│   ├── page.tsx
│   ├── login/page.tsx
│   └── cars/
│       ├── page.tsx
│       └── [id]/page.tsx
│
├── widgets/                # Self-contained UI blocks (composed of features+entities)
│   ├── CarList/
│   │   ├── ui/CarList.tsx
│   │   └── index.ts
│   └── CarFilters/
│       ├── ui/CarFilters.tsx
│       └── index.ts
│
├── features/               # User-facing interactions
│   ├── auth/
│   │   ├── ui/LoginForm.tsx
│   │   ├── model/useLogin.ts
│   │   └── index.ts
│   └── car-filter/
│       ├── model/useCarFilters.ts
│       └── index.ts
│
├── entities/               # Business objects and their UI representations
│   ├── car/
│   │   ├── ui/CarCard.tsx
│   │   ├── model/types.ts
│   │   └── index.ts
│   └── user/
│       ├── model/types.ts
│       └── index.ts
│
└── shared/                 # No business logic — pure reusables
    ├── ui/                 # Generic components (Button, Input, Badge, Spinner...)
    ├── lib/                # Pure utilities (formatPrice, formatMileage...)
    ├── api/                # Axios instance, request helpers
    └── config/             # Constants, env vars wrapper
```

### Rules
- Imports only flow downward: `app → widgets → features → entities → shared`.
- Never import from a higher layer (no `features` importing from `widgets`).
- Each slice has an `index.ts` public API — import from that, never from internals.
- `app/` pages are thin — they compose widgets, nothing more.
- `shared/ui/` components are generic and have zero business logic.
- Split every meaningful UI piece into its own component — no 200-line JSX files.
- Co-locate component styles, hooks, and types inside the slice folder.

---

## Component Rules (Frontend)

- Every component must be a named export (no default-only exports in shared/ui).
- Props interfaces named `{ComponentName}Props`.
- No inline styles — Tailwind classes only.
- Extract repeated class strings into `cn()` utility or component variants.
- Hooks that contain logic must live in `model/` inside the slice.
- No business logic inside JSX — move it to hooks or utility functions.

---

## What to Avoid

- No `any` in TypeScript — ever.
- No `# noqa` without a comment explaining why.
- No hardcoded credentials, URLs, or magic numbers in code.
- No mixing of infrastructure and domain code.
- No barrel re-exports that create circular dependencies.
- No comments that just restate the code.
- No AI-sounding prose in comments or variable names.
