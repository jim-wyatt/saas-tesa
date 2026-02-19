from collections.abc import Iterable

from saastesa.connectors.base import ThreatSignalProvider
from saastesa.core.models import ThreatSignal


def ingest_signals(provider: ThreatSignalProvider) -> list[ThreatSignal]:
    signals: Iterable[ThreatSignal] = provider.fetch_signals()
    return list(signals)
