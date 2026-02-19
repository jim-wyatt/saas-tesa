from saastesa.connectors.base import ThreatSignalProvider
from saastesa.core.models import SecurityFinding
from saastesa.pipelines.analyze import analyze_signals
from saastesa.pipelines.ingest import ingest_signals


class TESAService:
    def __init__(self, provider: ThreatSignalProvider) -> None:
        self.provider = provider

    def run_once(self) -> list[SecurityFinding]:
        signals = ingest_signals(self.provider)
        return analyze_signals(signals)
