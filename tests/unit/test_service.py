from saastesa.connectors.mock import MockThreatSignalProvider
from saastesa.services.tesa_service import TESAService


def test_service_run_once_returns_findings() -> None:
    service = TESAService(provider=MockThreatSignalProvider())
    findings = service.run_once()

    assert len(findings) == 2
    assert all(finding.risk_score > 0 for finding in findings)
