from datetime import UTC, datetime

from fastapi.testclient import TestClient

from saastesa.api.main import create_app


def test_health_endpoint() -> None:
    client = TestClient(create_app())
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["database_engine"] in {"sqlite", "postgresql"}


def test_ingest_and_query_endpoints() -> None:
    client = TestClient(create_app())
    payload = {
        "signals": [
            {
                "source": "iam",
                "signal_type": "stale_admin_credential",
                "severity": 5,
                "detected_at": datetime.now(tz=UTC).isoformat(),
                "metadata": {"privileged_access": True},
            }
        ]
    }

    ingest = client.post("/api/v1/signals", json=payload)
    assert ingest.status_code == 200
    assert ingest.json()["ingested"] == 1
    finding = ingest.json()["findings"][0]
    assert finding["standard"] == "OCSF"
    assert finding["domain"] in {"application", "infrastructure", "other"}
    assert finding["risk_score"] >= 10

    findings = client.get("/api/v1/findings")
    assert findings.status_code == 200
    assert len(findings.json()) == 1

    summary = client.get("/api/v1/summary")
    assert summary.status_code == 200
    assert summary.json()["critical"] >= 1


def test_direct_standardized_finding_ingest() -> None:
    client = TestClient(create_app())
    now = datetime.now(tz=UTC).isoformat()
    payload = {
        "findings": [
            {
                "finding_uid": "finding-123",
                "standard": "OCSF",
                "schema_version": "1.1.0",
                "status": "open",
                "severity_id": 4,
                "severity": "high",
                "risk_score": 85,
                "title": "Public bucket allows anonymous read",
                "description": "Storage bucket is publicly readable.",
                "category_name": "Infrastructure Security",
                "class_name": "Security Finding",
                "type_name": "Storage Misconfiguration",
                "domain": "infrastructure",
                "activity_name": "Create",
                "time": now,
                "source": "cspm",
                "resource": {
                    "uid": "bucket-1",
                    "name": "logs-bucket",
                    "type": "storage_bucket",
                    "platform": "aws",
                },
                "references": {
                    "cve": [],
                    "cwe": ["CWE-200"],
                    "owasp": [],
                    "mitre_attack": ["T1530"],
                },
                "raw_data": {"region": "us-east-1"},
            }
        ]
    }

    response = client.post("/api/v1/findings", json=payload)
    assert response.status_code == 200
    assert response.json()["ingested"] == 1
