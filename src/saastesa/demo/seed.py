from datetime import UTC, datetime, timedelta
import random
from typing import Any
from uuid import uuid4

DOMAIN_TYPES: dict[str, list[str]] = {
    "application": ["SQL Injection", "Dependency Vulnerability", "Secrets Exposure"],
    "infrastructure": ["Public Storage", "Open Security Group", "Unencrypted Volume"],
    "identity": ["Stale Admin Credential", "MFA Disabled", "Excessive Privilege"],
    "cloud": ["Misconfigured IAM Policy", "Logging Disabled", "Weak KMS Policy"],
    "container": ["Privileged Container", "Outdated Base Image", "Unscanned Image"],
}

SOURCES = ["sast", "dast", "sca", "iam", "cspm", "k8s", "edr", "siem"]
STATUSES = ["open", "open", "open", "in_progress", "resolved"]


def generate_demo_findings(count: int = 200, days: int = 30) -> list[dict[str, Any]]:
    now = datetime.now(tz=UTC)
    findings: list[dict[str, Any]] = []

    for _ in range(max(count, 1)):
        domain = random.choice(list(DOMAIN_TYPES.keys()))
        type_name = random.choice(DOMAIN_TYPES[domain])
        severity_id = random.choices([2, 3, 4, 5], weights=[20, 40, 30, 10], k=1)[0]
        risk_score = random.randint(max(10, severity_id * 18), min(100, severity_id * 22))
        observed = now - timedelta(
            days=random.randint(0, max(days - 1, 0)),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59),
        )

        finding_uid = str(uuid4())
        source = random.choice(SOURCES)
        title = f"{type_name} detected in {domain} stack"
        description = (
            f"{type_name} indicates elevated {domain} exposure and requires triage."
        )

        findings.append(
            {
                "finding_uid": finding_uid,
                "standard": "OCSF",
                "schema_version": "1.1.0",
                "status": random.choice(STATUSES),
                "severity_id": severity_id,
                "severity": _severity_label(severity_id),
                "risk_score": risk_score,
                "title": title,
                "description": description,
                "category_name": _category_name(domain),
                "class_name": "Security Finding",
                "type_name": type_name,
                "domain": domain,
                "activity_name": "Create",
                "time": observed.isoformat(),
                "source": source,
                "resource": {
                    "uid": f"asset-{random.randint(1000, 9999)}",
                    "name": f"{domain}-service-{random.randint(1, 50)}",
                    "type": _resource_type(domain),
                    "platform": random.choice(["aws", "gcp", "azure", "saas"]),
                },
                "references": {
                    "cve": ["CVE-2024-12345"] if random.random() > 0.7 else [],
                    "cwe": ["CWE-79"] if domain == "application" else [],
                    "owasp": ["A05:2021"] if domain == "application" else [],
                    "mitre_attack": ["T1190"] if random.random() > 0.6 else [],
                },
                "raw_data": {
                    "generated": True,
                    "demo": True,
                    "owner": random.choice(["platform", "appsec", "sre", "infra"]),
                },
            }
        )
    return findings


def _severity_label(severity_id: int) -> str:
    return {1: "informational", 2: "low", 3: "medium", 4: "high", 5: "critical"}.get(
        severity_id, "unknown"
    )


def _category_name(domain: str) -> str:
    return {
        "application": "Application Security",
        "infrastructure": "Infrastructure Security",
        "identity": "Identity Security",
        "cloud": "Cloud Security",
        "container": "Container Security",
    }.get(domain, "Security Operations")


def _resource_type(domain: str) -> str:
    return {
        "application": "service",
        "infrastructure": "compute",
        "identity": "identity",
        "cloud": "cloud_resource",
        "container": "container",
    }.get(domain, "asset")
