import argparse
from collections.abc import Sequence

from saastesa.agent.runner import main as agent_main
from saastesa.api.main import serve
from saastesa.config import load_settings
from saastesa.connectors.mock import MockThreatSignalProvider
from saastesa.core.risk_scoring import summarize_scores
from saastesa.demo.seed import generate_demo_findings
from saastesa.logging import configure_logging
from saastesa.sdk.api_client import TESAApiClient
from saastesa.services.tesa_service import TESAService


def _run(mock: bool) -> int:
    settings = load_settings()
    configure_logging(settings.log_level)

    provider = MockThreatSignalProvider()
    if not mock:
        raise NotImplementedError("Non-mock providers are not implemented yet.")

    findings = TESAService(provider=provider).run_once()
    summary = summarize_scores(findings)

    print(f"Organization: {settings.organization}")
    print(f"Environment: {settings.environment}")
    print("--- Findings ---")
    for finding in findings:
        print(
            f"[{finding.risk_score}] {finding.title} ({finding.domain}/{finding.type_name}) :: "
            f"{finding.description}"
        )
    print("--- Summary ---")
    print(summary)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="saastesa", description="SaaS TESA CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run one threat analysis cycle")
    run_parser.add_argument("--mock", action="store_true", help="Use mock signal provider")
    subparsers.add_parser("serve-api", help="Run FastAPI server")
    agent_parser = subparsers.add_parser("run-agent", help="Run distributed signal agent")
    agent_parser.add_argument("--api-url", default="http://localhost:8080")
    agent_parser.add_argument("--interval-seconds", type=int, default=30)
    agent_parser.add_argument("--once", action="store_true")

    seed_parser = subparsers.add_parser("seed-demo", help="Seed demo findings for dashboard presentations")
    seed_parser.add_argument("--api-url", default="http://localhost:8080")
    seed_parser.add_argument("--count", type=int, default=250)
    seed_parser.add_argument("--days", type=int, default=30)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "run":
        return _run(mock=args.mock)
    if args.command == "serve-api":
        serve()
        return 0
    if args.command == "run-agent":
        agent_args = ["--api-url", args.api_url, "--interval-seconds", str(args.interval_seconds)]
        if args.once:
            agent_args.append("--once")
        return agent_main(agent_args)
    if args.command == "seed-demo":
        findings = generate_demo_findings(count=args.count, days=args.days)
        result = TESAApiClient(base_url=args.api_url).send_findings(findings)
        print(f"Seeded {result['ingested']} findings to {args.api_url}")
        return 0
    parser.error("Unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
