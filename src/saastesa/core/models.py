from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class ThreatSignal:
    source: str
    signal_type: str
    severity: int
    detected_at: datetime
    metadata: dict[str, Any]


@dataclass(frozen=True)
class FindingResource:
    uid: str
    name: str
    type: str
    platform: str


@dataclass(frozen=True)
class FindingReferences:
    cve: tuple[str, ...]
    cwe: tuple[str, ...]
    owasp: tuple[str, ...]
    mitre_attack: tuple[str, ...]


@dataclass(frozen=True)
class SecurityFinding:
    finding_uid: str
    standard: str
    schema_version: str
    status: str
    severity_id: int
    severity: str
    risk_score: int
    title: str
    description: str
    category_name: str
    class_name: str
    type_name: str
    domain: str
    activity_name: str
    time: datetime
    source: str
    resource: FindingResource
    references: FindingReferences
    raw_data: dict[str, Any]
