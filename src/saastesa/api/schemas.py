from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class ThreatSignalIn(BaseModel):
    source: str
    signal_type: str
    severity: int = Field(ge=1, le=5)
    detected_at: datetime
    metadata: dict[str, Any] = Field(default_factory=dict)


class FindingResourceOut(BaseModel):
    uid: str
    name: str
    type: str
    platform: str


class FindingReferencesOut(BaseModel):
    cve: list[str] = Field(default_factory=list)
    cwe: list[str] = Field(default_factory=list)
    owasp: list[str] = Field(default_factory=list)
    mitre_attack: list[str] = Field(default_factory=list)


class SecurityFindingOut(BaseModel):
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
    resource: FindingResourceOut
    references: FindingReferencesOut
    raw_data: dict[str, Any]


class IngestSignalsRequest(BaseModel):
    signals: list[ThreatSignalIn]


class IngestSignalsResponse(BaseModel):
    ingested: int
    findings: list[SecurityFindingOut]


class IngestFindingsRequest(BaseModel):
    findings: list[SecurityFindingOut]


class IngestFindingsResponse(BaseModel):
    ingested: int


class FindingsSummaryOut(BaseModel):
    low: int
    medium: int
    high: int
    critical: int
