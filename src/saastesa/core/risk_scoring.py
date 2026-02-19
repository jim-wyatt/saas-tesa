from collections.abc import Iterable
from uuid import NAMESPACE_URL, uuid5

from saastesa.core.models import FindingReferences, FindingResource, SecurityFinding, ThreatSignal


def compute_risk_score(signal: ThreatSignal) -> int:
    severity = max(1, min(signal.severity, 5))
    exposure_factor = 2 if signal.metadata.get("internet_exposed") else 1
    privileged_factor = 2 if signal.metadata.get("privileged_access") else 1
    raw_score = severity * exposure_factor * privileged_factor
    return min(raw_score, 10)


def _severity_label(severity_id: int) -> str:
    mapping = {1: "informational", 2: "low", 3: "medium", 4: "high", 5: "critical"}
    return mapping.get(severity_id, "unknown")


def _domain(signal: ThreatSignal) -> str:
    explicit_domain = str(signal.metadata.get("domain", "")).strip().lower()
    if explicit_domain:
        return explicit_domain

    source = signal.source.lower()
    if source in {"sast", "dast", "sca", "cicd", "code"}:
        return "application"
    if source in {"iam", "cloud", "cspm", "k8s", "host", "network"}:
        return "infrastructure"
    return "other"


def _category_name(domain: str) -> str:
    mapping = {
        "application": "Application Security",
        "infrastructure": "Infrastructure Security",
        "identity": "Identity Security",
        "cloud": "Cloud Security",
        "container": "Container Security",
    }
    return mapping.get(domain, "Security Operations")


def build_finding(signal: ThreatSignal) -> SecurityFinding:
    score_10 = compute_risk_score(signal)
    severity_id = max(1, min(signal.severity, 5))
    domain = _domain(signal)
    finding_uid = str(
        uuid5(NAMESPACE_URL, f"{signal.source}:{signal.signal_type}:{signal.detected_at.isoformat()}")
    )

    resource = FindingResource(
        uid=str(signal.metadata.get("asset_id", signal.source)),
        name=str(signal.metadata.get("asset_name", signal.source)),
        type=str(signal.metadata.get("asset_type", "service")),
        platform=str(signal.metadata.get("platform", "saas")),
    )
    references = FindingReferences(
        cve=tuple(signal.metadata.get("cve", [])),
        cwe=tuple(signal.metadata.get("cwe", [])),
        owasp=tuple(signal.metadata.get("owasp", [])),
        mitre_attack=tuple(signal.metadata.get("mitre_attack", [])),
    )

    return SecurityFinding(
        finding_uid=finding_uid,
        standard="OCSF",
        schema_version="1.1.0",
        status=str(signal.metadata.get("status", "open")),
        severity_id=severity_id,
        severity=_severity_label(severity_id),
        risk_score=score_10 * 10,
        title=str(signal.metadata.get("title", f"{signal.source}:{signal.signal_type}")),
        description=str(
            signal.metadata.get(
                "description", "Derived finding from normalized threat signal and context risk factors."
            )
        ),
        category_name=_category_name(domain),
        class_name="Security Finding",
        type_name=str(signal.metadata.get("type_name", signal.signal_type.replace("_", " ").title())),
        domain=domain,
        activity_name="Create",
        time=signal.detected_at,
        source=signal.source,
        resource=resource,
        references=references,
        raw_data=signal.metadata,
    )


def summarize_scores(findings: Iterable[SecurityFinding]) -> dict[str, int]:
    buckets = {"low": 0, "medium": 0, "high": 0, "critical": 0}
    for finding in findings:
        if finding.risk_score <= 30:
            buckets["low"] += 1
        elif finding.risk_score <= 60:
            buckets["medium"] += 1
        elif finding.risk_score <= 80:
            buckets["high"] += 1
        else:
            buckets["critical"] += 1
    return buckets
