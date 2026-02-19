from collections.abc import Iterable
from datetime import datetime
from threading import Lock

from sqlalchemy import Engine, select
from sqlalchemy.orm import Session

from saastesa.api.db_models import Base, SecurityFindingRecord
from saastesa.core.models import FindingReferences, FindingResource, SecurityFinding
from saastesa.core.risk_scoring import summarize_scores


class InMemoryFindingStore:
    def __init__(self) -> None:
        self._lock = Lock()
        self._findings: list[SecurityFinding] = []

    def add(self, findings: list[SecurityFinding]) -> None:
        with self._lock:
            self._findings.extend(findings)

    def list(self, limit: int = 100) -> list[SecurityFinding]:
        with self._lock:
            if limit <= 0:
                return []
            return self._findings[-limit:]

    def summary(self) -> dict[str, int]:
        with self._lock:
            return summarize_scores(self._findings)


class SQLAlchemyFindingStore:
    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    def init(self) -> None:
        Base.metadata.create_all(self.engine)

    def add(self, findings: list[SecurityFinding]) -> None:
        if not findings:
            return

        with Session(self.engine) as session:
            for finding in findings:
                existing = session.scalar(
                    select(SecurityFindingRecord).where(SecurityFindingRecord.finding_uid == finding.finding_uid)
                )
                if existing is None:
                    session.add(self._to_record(finding))
                else:
                    self._update_record(existing, finding)
            session.commit()

    def list(self, limit: int = 100) -> list[SecurityFinding]:
        if limit <= 0:
            return []

        with Session(self.engine) as session:
            rows = session.scalars(
                select(SecurityFindingRecord)
                .order_by(SecurityFindingRecord.time.desc(), SecurityFindingRecord.id.desc())
                .limit(limit)
            ).all()

        findings = [self._from_record(row) for row in rows]
        findings.reverse()
        return findings

    def summary(self) -> dict[str, int]:
        return summarize_scores(self.list(limit=100000))

    def _to_record(self, finding: SecurityFinding) -> SecurityFindingRecord:
        return SecurityFindingRecord(
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
            resource_uid=finding.resource.uid,
            resource_name=finding.resource.name,
            resource_type=finding.resource.type,
            resource_platform=finding.resource.platform,
            references_json={
                "cve": list(finding.references.cve),
                "cwe": list(finding.references.cwe),
                "owasp": list(finding.references.owasp),
                "mitre_attack": list(finding.references.mitre_attack),
            },
            raw_data=finding.raw_data,
        )

    def _update_record(self, record: SecurityFindingRecord, finding: SecurityFinding) -> None:
        record.standard = finding.standard
        record.schema_version = finding.schema_version
        record.status = finding.status
        record.severity_id = finding.severity_id
        record.severity = finding.severity
        record.risk_score = finding.risk_score
        record.title = finding.title
        record.description = finding.description
        record.category_name = finding.category_name
        record.class_name = finding.class_name
        record.type_name = finding.type_name
        record.domain = finding.domain
        record.activity_name = finding.activity_name
        record.time = finding.time
        record.source = finding.source
        record.resource_uid = finding.resource.uid
        record.resource_name = finding.resource.name
        record.resource_type = finding.resource.type
        record.resource_platform = finding.resource.platform
        record.references_json = {
            "cve": list(finding.references.cve),
            "cwe": list(finding.references.cwe),
            "owasp": list(finding.references.owasp),
            "mitre_attack": list(finding.references.mitre_attack),
        }
        record.raw_data = finding.raw_data

    def _from_record(self, record: SecurityFindingRecord) -> SecurityFinding:
        references_payload = record.references_json or {}
        return SecurityFinding(
            finding_uid=record.finding_uid,
            standard=record.standard,
            schema_version=record.schema_version,
            status=record.status,
            severity_id=record.severity_id,
            severity=record.severity,
            risk_score=record.risk_score,
            title=record.title,
            description=record.description,
            category_name=record.category_name,
            class_name=record.class_name,
            type_name=record.type_name,
            domain=record.domain,
            activity_name=record.activity_name,
            time=_ensure_datetime(record.time),
            source=record.source,
            resource=FindingResource(
                uid=record.resource_uid,
                name=record.resource_name,
                type=record.resource_type,
                platform=record.resource_platform,
            ),
            references=FindingReferences(
                cve=tuple(references_payload.get("cve", [])),
                cwe=tuple(references_payload.get("cwe", [])),
                owasp=tuple(references_payload.get("owasp", [])),
                mitre_attack=tuple(references_payload.get("mitre_attack", [])),
            ),
            raw_data=record.raw_data or {},
        )


def _ensure_datetime(value: datetime) -> datetime:
    return value
