from datetime import UTC, datetime

from saastesa.core.models import ThreatSignal
from saastesa.core.risk_scoring import build_finding, compute_risk_score, summarize_scores


def test_compute_risk_score_caps_at_ten() -> None:
    signal = ThreatSignal(
        source="iam",
        signal_type="overprivileged_token",
        severity=5,
        detected_at=datetime.now(tz=UTC),
        metadata={"internet_exposed": True, "privileged_access": True},
    )

    assert compute_risk_score(signal) == 10


def test_summarize_scores_buckets() -> None:
    signals = [
        ThreatSignal("a", "s1", 1, datetime.now(tz=UTC), {}),
        ThreatSignal("b", "s2", 3, datetime.now(tz=UTC), {"internet_exposed": True}),
        ThreatSignal("c", "s3", 5, datetime.now(tz=UTC), {"privileged_access": True}),
    ]

    findings = [build_finding(signal) for signal in signals]
    summary = summarize_scores(findings)

    assert summary["low"] >= 1
    assert summary["critical"] >= 1


def test_build_finding_is_ocsf_aligned() -> None:
    signal = ThreatSignal(
        source="sast",
        signal_type="sql_injection",
        severity=4,
        detected_at=datetime.now(tz=UTC),
        metadata={"domain": "application", "cwe": ["CWE-89"], "owasp": ["A03:2021"]},
    )

    finding = build_finding(signal)

    assert finding.standard == "OCSF"
    assert finding.domain == "application"
    assert finding.risk_score > 0
    assert "CWE-89" in finding.references.cwe
