from collections.abc import Iterable
from dataclasses import asdict
from datetime import datetime
from typing import cast
from typing import Any

import httpx

from saastesa.core.models import ThreatSignal


class TESAApiClient:
    def __init__(self, base_url: str, timeout: float = 10.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _serialize_signal(self, signal: ThreatSignal) -> dict[str, Any]:
        payload = asdict(signal)
        detected_at = payload.get("detected_at")
        if isinstance(detected_at, datetime):
            payload["detected_at"] = detected_at.isoformat()
        return payload

    def send_signals(self, signals: Iterable[ThreatSignal]) -> dict[str, Any]:
        payload = {"signals": [self._serialize_signal(signal) for signal in signals]}
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(f"{self.base_url}/api/v1/signals", json=payload)
            response.raise_for_status()
            return cast(dict[str, Any], response.json())

    def send_findings(self, findings: Iterable[dict[str, Any]]) -> dict[str, Any]:
        payload = {"findings": list(findings)}
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(f"{self.base_url}/api/v1/findings", json=payload)
            response.raise_for_status()
            return cast(dict[str, Any], response.json())

    def get_summary(self) -> dict[str, Any]:
        with httpx.Client(timeout=self.timeout) as client:
            response = client.get(f"{self.base_url}/api/v1/summary")
            response.raise_for_status()
            return cast(dict[str, Any], response.json())
