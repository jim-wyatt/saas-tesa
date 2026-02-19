# Standardized Finding Model

SaaS TESA now uses an **OCSF-aligned** normalized finding model for API output and storage.

## Why OCSF

Open Cybersecurity Schema Framework (OCSF) provides a common schema vocabulary for diverse security telemetry and findings across:
- Application security (SAST, DAST, SCA)
- Infrastructure and cloud security (IAM, CSPM, K8s, host)
- Other domains (identity, network, endpoint, container, custom)

## Implemented canonical fields

Each finding includes:
- `finding_uid`, `standard`, `schema_version`
- `status`, `severity_id`, `severity`, `risk_score`
- `title`, `description`
- `category_name`, `class_name`, `type_name`, `domain`, `activity_name`
- `time`, `source`
- `resource { uid, name, type, platform }`
- `references { cve, cwe, owasp, mitre_attack }`
- `raw_data` for provider-specific context

## Domain support

`domain` supports at least:
- `application`
- `infrastructure`
- `identity`
- `cloud`
- `container`
- `other`

If omitted, SaaS TESA infers domain from connector/source and falls back to `other`.

## API behavior

- `POST /api/v1/signals` accepts raw signals and returns normalized findings.
- `POST /api/v1/findings` accepts normalized findings directly.
- `GET /api/v1/findings` returns normalized findings for UI and external consumers.

## Persistence behavior

- Local/development/test environments persist findings in SQLite.
- Non-local environments persist findings in PostgreSQL.
- Both paths use the same normalized finding schema and API contract.
