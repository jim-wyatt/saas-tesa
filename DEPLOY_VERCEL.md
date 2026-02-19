# SaaS TESA: Vercel + Neon Deployment Guide

This guide walks through account signup, project setup, and first deployment for:

- Web tier: Vercel (Vite frontend)
- App tier: Vercel Python Serverless Function (FastAPI)
- Data tier: Neon Postgres

## 1) Prerequisites

- GitHub account
- Vercel account
- Neon account
- Project code pushed to a GitHub repository

## 1.1) Use GitHub sign-in for everything

You can use your GitHub account as the identity provider for:

- Neon
- Vercel

Recommended: sign up to both services using **Continue with GitHub** and grant access to the same repository owner/account.

## 2) Sign up and create Neon database

1. Go to Neon and sign in with GitHub.
2. Create a new project (for example: `saastesa-prod`).
3. Create database and user if prompted.
4. Open the Connection Details page.
5. Copy the pooled Postgres connection string.

You will use this value for `TESA_DATABASE_URL` in Vercel.

## 3) Sign up and import project in Vercel

1. Go to Vercel and sign in with GitHub.
2. Click Add New Project.
3. Select your SaaS TESA repository.
4. Keep the project root at repository root (the existing `vercel.json` is used).
5. Click Continue to project configuration.

## 3.1) Link Vercel project for CLI/GitHub Actions

After creating the Vercel project, run locally from repo root:

- `npx vercel link`

This ensures local and CI use the same `VERCEL_ORG_ID` and `VERCEL_PROJECT_ID` context.

## 4) Configure environment variables in Vercel

In Vercel project settings, add these variables for Production and Preview:

- `TESA_ENV` = `production`
- `TESA_DATABASE_URL` = your Neon pooled connection string
- `TESA_CORS_ORIGINS` = your Vercel frontend origin (example: `https://your-app.vercel.app`)
- `TESA_CORS_ORIGIN_REGEX` = leave empty for strict single-origin CORS, or set if you need multiple domains

Optional:

- `TESA_ORGANIZATION` = your org name
- `TESA_LOG_LEVEL` = `INFO`

## 4.1) Configure GitHub Actions repository secrets

In GitHub repository settings, add these Actions secrets:

- `VERCEL_TOKEN`
- `VERCEL_ORG_ID`
- `VERCEL_PROJECT_ID`

How to get values:

- `VERCEL_TOKEN`: create in Vercel account settings -> tokens
- `VERCEL_ORG_ID` and `VERCEL_PROJECT_ID`: from `.vercel/project.json` after `npx vercel link`

Optional (if you want CI to use explicit app env vars for integration tests later):

- `TESA_DATABASE_URL`
- `TESA_ENV`

## 5) First deployment

1. In Vercel, click Deploy.
2. Wait for build + deployment to complete.
3. Open your deployment URL.
4. Verify API endpoint:
   - `https://your-app.vercel.app/health`
5. Verify app endpoint:
   - `https://your-app.vercel.app/`

If the UI loads but has no data, continue to the seed step.

## 6) Seed initial demo data (first time)

Option A: from your local machine

1. Activate local venv.
2. Run:
   - `saastesa seed-demo --api-url https://your-app.vercel.app --count 250 --days 30`

Option B: post normalized findings directly to `/api/v1/findings` from your own script/integration.

## 7) Smoke test checklist

- `GET /health` returns status `ok`
- Dashboard loads without connection errors
- `GET /api/v1/summary` returns non-zero buckets after seed
- `GET /api/v1/findings?limit=10` returns normalized OCSF-style records
- Dark/light theme toggle works in the UI

## 8) Preview and production flow

Recommended branch flow:

- Push feature branches -> Vercel Preview deployments
- Merge to main -> Vercel Production deployment

Use separate Neon databases per environment if possible:

- `saastesa-preview`
- `saastesa-production`

## 8.1) GitHub Actions pipeline behavior

This repo includes:

- `.github/workflows/ci.yml`
  - Runs backend tests and frontend build on PRs and pushes
- `.github/workflows/cd-vercel.yml`
  - Deploys Preview on pull requests
  - Deploys Production on push to `main`

Recommended branch policy:

- Require CI checks before merge
- Protect `main`
- Use pull requests for all production changes

## 9) Common issues and fixes

### Issue: UI says unable to load API data

- Confirm `https://your-app.vercel.app/health` works.
- Confirm `TESA_CORS_ORIGINS` exactly matches frontend origin.
- Ensure environment variables are set for the correct Vercel environment (Preview vs Production).
- Redeploy after env changes.

### Issue: Database errors at runtime

- Verify Neon connection string is pooled/serverless-safe.
- Confirm database is active and network policy allows Vercel.
- Check Vercel function logs for SQLAlchemy/connection errors.

### Issue: Empty dashboard after deployment

- Seed data using `saastesa seed-demo` command.
- Confirm seed command targets deployed URL, not localhost.

## 10) Recommended next hardening steps

- Add auth (OIDC/JWT)
- Add request rate-limiting and abuse controls
- Add structured log shipping and error alerting
- Add separate staging environment with staged data
