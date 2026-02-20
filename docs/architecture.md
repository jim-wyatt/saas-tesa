# SaaS TESA Architecture

## Runtime components

1. **Distributed Agent** (`src/saastesa/agent/`): Collects threat signals from connectors and posts to API.
2. **API Service** (`src/saastesa/api/`): Ingests signals, computes findings, serves query endpoints.
3. **Dashboard UI** (`frontend/`): React/Vite console for summary + findings visualization.

## Backend layers

1. **Connectors**: Gather raw threat signals (mock now, provider-specific later).
2. **Pipelines**: Convert raw signals into scored findings.
3. **Core**: Threat domain models and scoring logic.
4. **API**: HTTP interface for ingest and read operations.

Findings are normalized into an **OCSF-aligned** security finding schema for cross-domain interoperability.

Persistence is environment-aware:
- Local/development/test defaults to **SQLite** (`saastesa.db`)
- Non-local environments default to **PostgreSQL** (via `TESA_DATABASE_URL` or `TESA_DB_*` vars)

## Current API endpoints

- `GET /health`
- `POST /api/v1/signals`
- `POST /api/v1/findings`
- `GET /api/v1/findings?limit=...`
- `GET /api/v1/summary`

## End-to-end flow

1. Agent fetches threat signals from connector(s).
2. Agent sends signals to API ingest endpoint.
3. API computes findings and stores them in the configured relational database.
4. Frontend polls summary/findings endpoints and renders KPI cards, domain/source/trend charts, and a detailed findings grid.

## Planned production upgrades

- Replace in-memory storage with PostgreSQL/ClickHouse
- Add authn/authz (OIDC/JWT)
- Add event streaming path for high-volume ingestion
- Add tenant-aware data partitioning and RBAC

## UML diagrams

PlantUML source files for the architecture are available in [uml/README.md](uml/README.md), including:

- Component diagram
- Domain class diagram
- Ingestion sequence diagram
- Deployment diagram
