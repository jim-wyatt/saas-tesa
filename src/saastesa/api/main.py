from collections.abc import Iterable
import os
from typing import Any

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from saastesa.api.db import create_db_engine, resolve_database_url
from saastesa.api.schemas import (
    FindingReferencesOut,
    FindingResourceOut,
    FindingsSummaryOut,
    IngestFindingsRequest,
    IngestFindingsResponse,
    IngestSignalsRequest,
    IngestSignalsResponse,
    SecurityFindingOut,
)
from saastesa.api.store import SQLAlchemyFindingStore
from saastesa.core.models import FindingReferences, FindingResource, SecurityFinding, ThreatSignal
from saastesa.pipelines.analyze import analyze_signals


def _to_findings_out(findings: Iterable[SecurityFinding]) -> list[SecurityFindingOut]:
    return [
        SecurityFindingOut(
            finding_uid=finding.finding_uid,
            standard=finding.standard,
            schema_version=finding.schema_version,
            status=finding.status,
            severity_id=finding.severity_id,
            severity=finding.severity,
            risk_score=finding.risk_score,
            title=finding.title,
            description=finding.description,
            category_name=finding.category_name,
            class_name=finding.class_name,
            type_name=finding.type_name,
            domain=finding.domain,
            activity_name=finding.activity_name,
            time=finding.time,
            source=finding.source,
            resource=FindingResourceOut(
                uid=finding.resource.uid,
                name=finding.resource.name,
                type=finding.resource.type,
                platform=finding.resource.platform,
            ),
            references=FindingReferencesOut(
                cve=list(finding.references.cve),
                cwe=list(finding.references.cwe),
                owasp=list(finding.references.owasp),
                mitre_attack=list(finding.references.mitre_attack),
            ),
            raw_data=finding.raw_data,
        )
        for finding in findings
    ]


def _from_findings_in(payload_findings: list[SecurityFindingOut]) -> list[SecurityFinding]:
    return [
        SecurityFinding(
            finding_uid=finding.finding_uid,
            standard=finding.standard,
            schema_version=finding.schema_version,
            status=finding.status,
            severity_id=finding.severity_id,
            severity=finding.severity,
            risk_score=finding.risk_score,
            title=finding.title,
            description=finding.description,
            category_name=finding.category_name,
            class_name=finding.class_name,
            type_name=finding.type_name,
            domain=finding.domain,
            activity_name=finding.activity_name,
            time=finding.time,
            source=finding.source,
            resource=FindingResource(
                uid=finding.resource.uid,
                name=finding.resource.name,
                type=finding.resource.type,
                platform=finding.resource.platform,
            ),
            references=FindingReferences(
                cve=tuple(finding.references.cve),
                cwe=tuple(finding.references.cwe),
                owasp=tuple(finding.references.owasp),
                mitre_attack=tuple(finding.references.mitre_attack),
            ),
            raw_data=finding.raw_data,
        )
        for finding in payload_findings
    ]


def create_app(database_url: str | None = None) -> FastAPI:
    app = FastAPI(title="SaaS TESA API", version="0.1.0")
    effective_database_url = database_url or resolve_database_url()
    if database_url is None and "PYTEST_CURRENT_TEST" in os.environ:
        effective_database_url = "sqlite+pysqlite:///:memory:"
    store = SQLAlchemyFindingStore(create_db_engine(effective_database_url))
    store.init()

    cors_origins = os.getenv(
        "TESA_CORS_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173",
    )
    cors_origin_regex = os.getenv(
        "TESA_CORS_ORIGIN_REGEX",
        r"^https?://(localhost|127\.0\.0\.1|192\.168\.\d+\.\d+|10\.\d+\.\d+\.\d+)(:\d+)?$",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[origin.strip() for origin in cors_origins.split(",") if origin.strip()],
        allow_origin_regex=cors_origin_regex,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health")
    def health() -> dict[str, Any]:
        return {"status": "ok", "database": effective_database_url}

    @app.post("/api/v1/signals", response_model=IngestSignalsResponse)
    def ingest_signals(request: IngestSignalsRequest) -> IngestSignalsResponse:
        signals = [
            ThreatSignal(
                source=signal.source,
                signal_type=signal.signal_type,
                severity=signal.severity,
                detected_at=signal.detected_at,
                metadata=signal.metadata,
            )
            for signal in request.signals
        ]
        findings = analyze_signals(signals)
        store.add(findings)
        return IngestSignalsResponse(ingested=len(signals), findings=_to_findings_out(findings))

    @app.post("/api/v1/findings", response_model=IngestFindingsResponse)
    def ingest_findings(request: IngestFindingsRequest) -> IngestFindingsResponse:
        findings = _from_findings_in(request.findings)
        store.add(findings)
        return IngestFindingsResponse(ingested=len(findings))

    @app.get("/api/v1/findings", response_model=list[SecurityFindingOut])
    def list_findings(limit: int = Query(default=100, ge=1, le=1000)) -> list[SecurityFindingOut]:
        return _to_findings_out(store.list(limit=limit))

    @app.get("/api/v1/summary", response_model=FindingsSummaryOut)
    def findings_summary() -> FindingsSummaryOut:
        return FindingsSummaryOut(**store.summary())

    return app


app = create_app()


def serve() -> None:
    host = os.getenv("TESA_API_HOST", "0.0.0.0")
    port = int(os.getenv("TESA_API_PORT", "8080"))
    uvicorn.run("saastesa.api.main:app", host=host, port=port, reload=False)


if __name__ == "__main__":
    serve()
