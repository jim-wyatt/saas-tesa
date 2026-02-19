import argparse
from collections.abc import Sequence
import time

from saastesa.connectors.mock import MockThreatSignalProvider
from saastesa.sdk.api_client import TESAApiClient


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="saastesa-agent", description="SaaS TESA distributed agent")
    parser.add_argument("--api-url", default="http://localhost:8080", help="SaaS TESA API base URL")
    parser.add_argument("--interval-seconds", type=int, default=30, help="Polling interval")
    parser.add_argument("--once", action="store_true", help="Send one batch and exit")
    return parser


def _run_once(api_url: str) -> None:
    provider = MockThreatSignalProvider()
    client = TESAApiClient(base_url=api_url)
    result = client.send_signals(provider.fetch_signals())
    print(f"Agent pushed {result['ingested']} signals")


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.once:
        _run_once(args.api_url)
        return 0

    try:
        while True:
            _run_once(args.api_url)
            time.sleep(max(args.interval_seconds, 1))
    except KeyboardInterrupt:
        print("Agent stopped")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
