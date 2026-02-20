# SaaS TESA

SaaS TESA (Threat Environment Situational Awareness) is a platform scaffold for SaaS engineering security teams with:

- A FastAPI backend for ingest + analytics
- A distributed Python agent client for signal submission
- A React + Vite dashboard frontend for rich visualization

## Stack choices

- **Backend API:** FastAPI + Pydantic
- **Distributed client SDK/agent:** Python + HTTPX
- **Frontend UI library (recommended OSS):** MUI (Material UI Community)
- **Visualization:** Recharts + MUI Data Grid

## Persistence

- Local/development/test defaults to **SQLite** at `./saastesa.db`
- Non-local environments default to **PostgreSQL**
- Override any environment with `TESA_DATABASE_URL`

### Schema migration runbook

- On API startup, SaaS TESA now runs an automatic schema check and migration step.
- If the legacy denormalized `security_findings` schema is detected, startup migrates data in-place to the normalized model (`finding_resources`, `security_findings`, `finding_reference_items`).
- Migration is idempotent: once upgraded, later starts skip the conversion and run normally.
- Startup blocks until migration completes, so large datasets may increase cold-start time for the first upgraded boot.
- Back up production data before first deploy with this version and validate migration in a staging environment first.
- Postgres sequences are re-synced after migration; SQLite requires no sequence maintenance.

## Serverless deployment target (Vercel + Neon)

This repo is now wired for:

- **Web tier:** Vercel static hosting for the Vite frontend
- **App tier:** Vercel Python Serverless Function (`api/index.py`) serving FastAPI
- **Data tier:** Neon Postgres via `TESA_DATABASE_URL`

### Deploy steps

1. Create a Neon project and copy the pooled connection string.
2. Import this repo into Vercel.
3. Set Vercel environment variables:

   - `TESA_ENV=production`
   - `TESA_DATABASE_URL=<your_neon_postgres_url>`
   - `TESA_CORS_ORIGINS=https://<your-vercel-domain>`

4. Deploy.

Notes:

- `vercel.json` handles frontend build output and rewrites `/api/*` to the Python function.
- Frontend defaults to same-origin API in deployed environments, so no extra `VITE_API_BASE_URL` is required.

Full step-by-step guide: [DEPLOY_VERCEL.md](DEPLOY_VERCEL.md)

## CI/CD (GitHub Actions)

Included workflows:

- [CI](.github/workflows/ci.yml): backend tests + frontend build on PRs/pushes
- [CD - Vercel](.github/workflows/cd-vercel.yml): preview deploys on PRs and production deploys from `main`

Set these GitHub repository secrets to enable CD:

- `VERCEL_TOKEN`
- `VERCEL_ORG_ID`
- `VERCEL_PROJECT_ID`

## Dev bootstrap with live reload

Use one script for setup and live reload of API + frontend.

```bash
scripts/bootstrap.sh setup
scripts/bootstrap.sh up
```

`setup` installs Python dependencies and installs Node.js/npm automatically if missing, then installs frontend dependencies. `up` launches:

- Backend with Uvicorn `--reload`
- Frontend with Vite dev server

Environment knobs:

- `TESA_API_HOST`, `TESA_API_PORT`
- `TESA_FRONTEND_HOST`, `TESA_FRONTEND_PORT`
- `TESA_DATABASE_URL` or `TESA_DB_HOST`/`TESA_DB_PORT`/`TESA_DB_USER`/`TESA_DB_PASSWORD`/`TESA_DB_NAME`

## Demo workflow for engineering + leadership reviews

One-command executive demo mode:

```bash
scripts/demo.sh
```

This command installs dependencies, starts backend + frontend with live reload, seeds realistic findings, and opens the dashboard.

```bash
scripts/bootstrap.sh up
saastesa seed-demo --api-url http://localhost:8080 --count 400 --days 45
```

The dashboard now includes:

- Executive KPI cards
- Severity distribution
- Domain distribution
- Top source systems
- 14-day findings trend
- Detailed findings table

## Quick start (backend)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
saastesa-api
```

In another terminal, push mock data once:

```bash
source .venv/bin/activate
saastesa-agent --api-url http://localhost:8080 --once
```

## Quick start (frontend)

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

## Key commands

- `saastesa run --mock` : local non-API pipeline run
- `saastesa serve-api` : start FastAPI server
- `saastesa run-agent --once` : send one signal batch to API
- `scripts/demo.sh` : one-command executive demo mode (live reload + seed + open dashboard)
- `saastesa seed-demo --count 400 --days 45` : generate realistic cross-domain demo findings
- `pytest` : run backend tests
- `TESA_RUN_SMOKE=1 TESA_SMOKE_BASE_URL=https://saastesa.vercel.app pytest -q tests/smoke` : run deployment smoke tests

## Standardized findings model

SaaS TESA now stores and serves findings using an **OCSF-aligned** normalized model designed to support application, infrastructure, identity, cloud, container, and other domains.

See [docs/finding-model.md](docs/finding-model.md).

Architecture UML diagrams (PlantUML): [docs/uml/README.md](docs/uml/README.md)

## Monorepo layout

- `src/saastesa/api/` FastAPI app and schemas
- `src/saastesa/agent/` distributed client runner
- `src/saastesa/sdk/` API client for remote communication
- `src/saastesa/core/` threat domain models + scoring
- `frontend/` React Vite dashboard
- `tests/unit/` backend unit/API tests
