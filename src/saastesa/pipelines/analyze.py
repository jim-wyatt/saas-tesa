from saastesa.core.models import SecurityFinding, ThreatSignal
from saastesa.core.risk_scoring import build_finding


def analyze_signals(signals: list[ThreatSignal]) -> list[SecurityFinding]:
    return [build_finding(signal) for signal in signals]
