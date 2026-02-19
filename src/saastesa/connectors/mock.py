from datetime import UTC, datetime

from saastesa.core.models import ThreatSignal


class MockThreatSignalProvider:
    def fetch_signals(self) -> list[ThreatSignal]:
        now = datetime.now(tz=UTC)
        return [
            ThreatSignal(
                source="cicd",
                signal_type="public_build_log_leak",
                severity=4,
                detected_at=now,
                metadata={"internet_exposed": True, "privileged_access": False},
            ),
            ThreatSignal(
                source="iam",
                signal_type="stale_admin_credential",
                severity=5,
                detected_at=now,
                metadata={"internet_exposed": False, "privileged_access": True},
            ),
        ]
