from collections.abc import Iterable
from typing import Protocol

from saastesa.core.models import ThreatSignal


class ThreatSignalProvider(Protocol):
    def fetch_signals(self) -> Iterable[ThreatSignal]:
        ...
